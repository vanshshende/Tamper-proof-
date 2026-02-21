import streamlit as st
import hashlib, json, time, os, random
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Secure Sentinel", layout="wide")

DB_FILE="logs.json"

# ---------------- DATABASE ----------------
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE,"w") as f:
            json.dump([],f)

def load_chain():
    init_db()
    try:
        with open(DB_FILE,"r") as f:
            data=f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except:
        return []

def save_chain(chain):
    with open(DB_FILE,"w") as f:
        json.dump(chain,f,indent=2)

def calculate_hash(block):
    raw=f"{block['index']}{block['timestamp']}{block['device']}{block['event']}{block['value']}{block['prev_hash']}"
    return hashlib.sha256(raw.encode()).hexdigest()

def add_log(device,event,value):
    chain=load_chain()
    prev_hash=chain[-1]["hash"] if chain else "GENESIS"

    block={
        "index":len(chain),
        "timestamp":time.strftime("%H:%M:%S"),
        "device":device,
        "event":event,
        "value":value,
        "prev_hash":prev_hash
    }

    block["hash"]=calculate_hash(block)
    chain.append(block)
    save_chain(chain)

def verify_chain():
    chain=load_chain()
    for i in range(len(chain)):
        block=chain[i]

        if calculate_hash(block)!=block["hash"]:
            return False,i,block

        if i>0 and block["prev_hash"]!=chain[i-1]["hash"]:
            return False,i,block

    return True,-1,None

def tamper():
    chain=load_chain()
    if len(chain)>2:
        chain[2]["value"]=9999   # attacker modifies
        save_chain(chain)

# ---------------- SEED ----------------
def seed():
    if len(load_chain())==0:
        for _ in range(6):
            add_log(
                random.choice(["Boiler-7","Turbine-3","Reactor-2","Cooling-5"]),
                random.choice(["OVERHEAT","PRESSURE SPIKE","VIBRATION ALERT"]),
                random.randint(80,150)
            )
seed()

chain=load_chain()
df=pd.DataFrame(chain)
valid,bad_index,bad_block=verify_chain()

# ---------------- RED ALERT STYLE ----------------
if not valid:
    st.markdown("""
    <style>
    .alert-box {
        background-color:#3b0000;
        padding:20px;
        border-radius:10px;
        animation: blink 1s infinite;
        text-align:center;
        font-size:28px;
        color:white;
        font-weight:bold;
    }
    @keyframes blink {
        0% {background-color:#5c0000;}
        50% {background-color:#b30000;}
        100% {background-color:#5c0000;}
    }
    </style>
    """,unsafe_allow_html=True)

    st.markdown('<div class="alert-box">⚠ CRITICAL DATA TAMPERING DETECTED ⚠</div>',unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔐 Secure Sentinel")
page=st.sidebar.radio("Navigation",
["Dashboard","Add Critical Log","Attack Lab","Forensics","Blockchain Explorer"])

# ---------------- DASHBOARD ----------------
if page=="Dashboard":
    st.title("Industrial High-Integrity Logging System")

    col1,col2,col3,col4=st.columns(4)

    devices=len(set(df["device"])) if len(df)>0 else 0
    blocks=len(df)
    alerts=0 if valid else 1

    col1.metric("Devices",devices)
    col2.metric("Total Logs",blocks)
    col3.metric("Tamper Alerts",alerts)

    if valid:
        col4.metric("Status","SECURE")
    else:
        col4.metric("Status","COMPROMISED")

    st.markdown("---")

    if len(df)>0:
        chart=px.line(df,x=df.index,y="value",title="Critical Sensor Activity")
        st.plotly_chart(chart,use_container_width=True)

# ---------------- ADD LOG ----------------
if page=="Add Critical Log":
    st.title("Store Critical Industrial Event")

    device=st.selectbox("Device",
    ["Boiler-7","Turbine-3","Reactor-2","Cooling-5"])

    event=st.selectbox("Event",
    ["OVERHEAT","PRESSURE SPIKE","VIBRATION ALERT","COOLANT FAILURE"])

    value=st.slider("Severity",50,200,120)

    if st.button("Store Secure Record"):
        add_log(device,event,value)
        st.success("Stored in tamper-proof blockchain")

# ---------------- ATTACK LAB ----------------
if page=="Attack Lab":
    st.title("⚠ Attack Simulation Lab")

    st.markdown("Simulate insider modifying safety logs.")

    if st.button("Modify Stored Record (ATTACK)"):
        tamper()
        st.error("Attacker modified stored data!")

    if st.button("Run Detection Engine"):
        valid,idx,block=verify_chain()
        if valid:
            st.success("System safe. No tampering.")
        else:
            st.error(f"Tampering detected in block #{idx}")

# ---------------- FORENSICS ----------------
if page=="Forensics":
    st.title("Tamper Forensics Analysis")

    if valid:
        st.success("No compromised records")
    else:
        st.error(f"Compromised Block Index: {bad_index}")
        st.json(bad_block)

# ---------------- BLOCKCHAIN VIEW ----------------
if page=="Blockchain Explorer":
    st.title("Immutable Blockchain Records")
    if len(df)>0:
        st.dataframe(df,use_container_width=True)
    else:
        st.info("No records yet")