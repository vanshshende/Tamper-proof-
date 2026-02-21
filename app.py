import streamlit as st
import hashlib, json, time, os, random
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Secure Sentinel", layout="wide")

DB_FILE = "logs.json"

# ---------------- DATABASE ----------------
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def load_chain():
    init_db()
    try:
        with open(DB_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except:
        return []

def save_chain(chain):
    with open(DB_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def calculate_hash(block):
    # Ensure consistency by excluding the 'hash' key itself from the calculation
    block_data = {k: v for k, v in block.items() if k != 'hash'}
    raw = json.dumps(block_data, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()

def add_log(device, event, value):
    chain = load_chain()
    prev_hash = chain[-1]["hash"] if chain else "GENESIS"

    block = {
        "index": len(chain),
        "timestamp": time.strftime("%H:%M:%S"),
        "device": device,
        "event": event,
        "value": value,
        "prev_hash": prev_hash
    }

    block["hash"] = calculate_hash(block)
    chain.append(block)
    save_chain(chain)

def verify_chain():
    chain = load_chain()
    for i in range(len(chain)):
        block = chain[i]
        
        # 1. Check if the data matches the hash stored in the block
        if calculate_hash(block) != block["hash"]:
            return False, i, block

        # 2. Check if the chain link is broken
        if i > 0 and block["prev_hash"] != chain[i-1]["hash"]:
            return False, i, block

    return True, -1, None

# ---- UPDATED ATTACK SIMULATION ----
def tamper(block_index, new_value, recompute_future=False):
    chain = load_chain()
    if 0 <= block_index < len(chain):
        # Attacker modifies the specific block value
        chain[block_index]["value"] = new_value
        
        # Recalculate hash for the modified block
        chain[block_index]["hash"] = calculate_hash(chain[block_index])

        # If recompute_future is True, the attacker attempts to fix the chain 
        # by updating all subsequent 'prev_hash' values.
        if recompute_future:
            for i in range(block_index + 1, len(chain)):
                chain[i]["prev_hash"] = chain[i-1]["hash"]
                chain[i]["hash"] = calculate_hash(chain[i])

        save_chain(chain)
        return True
    return False

# ---- RESET FUNCTION ----
def reset_chain():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()
    seed()

def seed():
    chain = load_chain()
    if len(chain) == 0:
        for _ in range(6):
            add_log(
                random.choice(["Boiler-7", "Turbine-3", "Reactor-2", "Cooling-5"]),
                random.choice(["OVERHEAT", "PRESSURE SPIKE", "VIBRATION ALERT"]),
                random.randint(80, 150)
            )

# ---------------- INITIALIZATION ----------------
seed()
chain = load_chain()
df = pd.DataFrame(chain)
valid, bad_index, bad_block = verify_chain()

# ---------------- UI COMPONENTS ----------------
if not valid:
    st.markdown("""
    <style>
    .alert-box {
        background-color:#3b0000; padding:20px; border-radius:10px;
        animation: blink 1s infinite; text-align:center;
        font-size:28px; color:white; font-weight:bold;
    }
    @keyframes blink { 0% {background-color:#5c0000;} 50% {background-color:#b30000;} 100% {background-color:#5c0000;} }
    </style>
    <div class="alert-box">⚠ CRITICAL DATA TAMPERING DETECTED ⚠</div>
    """, unsafe_allow_html=True)

st.sidebar.title("🔐 Secure Sentinel")
page = st.sidebar.radio("Navigation", ["Dashboard", "Add Critical Log", "Attack Lab", "Forensics", "Blockchain Explorer"])

if st.sidebar.button("Reset Blockchain"):
    reset_chain()
    st.rerun()

# ---------------- PAGES ----------------
if page == "Dashboard":
    st.title("Industrial High-Integrity Logging")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Devices", len(df["device"].unique()) if not df.empty else 0)
    col2.metric("Total Logs", len(df))
    col3.metric("Tamper Alerts", 0 if valid else 1)
    col4.metric("Status", "SECURE" if valid else "COMPROMISED", delta_color="inverse")
    
    if not df.empty:
        st.plotly_chart(px.line(df, x=df.index, y="value", title="Sensor Activity"), use_container_width=True)

if page == "Add Critical Log":
    st.title("Store Critical Event")
    with st.form("log_form"):
        dev = st.selectbox("Device", ["Boiler-7", "Turbine-3", "Reactor-2", "Cooling-5"])
        evt = st.selectbox("Event", ["OVERHEAT", "PRESSURE SPIKE", "VIBRATION ALERT", "COOLANT FAILURE"])
        val = st.slider("Severity", 50, 500, 120)
        if st.form_submit_button("Store Secure Record"):
            add_log(dev, evt, val)
            st.success("Record added to blockchain!")
            st.rerun()

if page == "Attack Lab":
    st.title("⚠ Attack Simulation Lab")
    if not df.empty:
        target_idx = st.number_input("Target Block Index", 0, len(df)-1, 0)
        new_val = st.number_input("New Malicious Value", value=9999)
        
        col1, col2 = st.columns(2)
        if col1.button("Simple Tamper (Breaks Hash)"):
            tamper(target_idx, new_val, recompute_future=False)
            st.error(f"Block #{target_idx} modified!")
            st.rerun()
            
        if col2.button("Sophisticated Tamper (Rebuilds Chain)"):
            tamper(target_idx, new_val, recompute_future=True)
            st.warning("Data changed and hashes re-calculated for future blocks.")
            st.rerun()
    else:
        st.info("No logs available to attack.")

if page == "Forensics":
    st.title("Forensics Analysis")
    if valid:
        st.success("All records verified. Integrity 100%.")
    else:
        st.error(f"Integrity Failure at Block #{bad_index}")
        st.json(bad_block)
        st.info("The stored hash no longer matches the recalculated data hash.")

if page == "Blockchain Explorer":
    st.title("Immutable Records")
    st.dataframe(df, use_container_width=True)
