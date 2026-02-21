import hashlib
import json
import time
import os

DB_FILE = "logs.json"

# initialize storage
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def load_chain():
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_chain(chain):
    with open(DB_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def calculate_hash(block):
    block_string = f"{block['index']}{block['timestamp']}{block['machine']}{block['event']}{block['value']}{block['prev_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def add_log(machine, event, value):
    chain = load_chain()

    prev_hash = chain[-1]["hash"] if chain else "GENESIS"

    block = {
        "index": len(chain),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "machine": machine,
        "event": event,
        "value": value,
        "prev_hash": prev_hash,
    }

    block["hash"] = calculate_hash(block)
    chain.append(block)
    save_chain(chain)

def verify_chain():
    chain = load_chain()

    for i in range(len(chain)):
        block = chain[i]

        if calculate_hash(block) != block["hash"]:
            return False, f"Tampering detected in block {i}"

        if i > 0 and block["prev_hash"] != chain[i-1]["hash"]:
            return False, f"Chain broken at block {i}"

    return True, "All records valid"

def tamper_block():
    chain = load_chain()
    if len(chain) > 1:
        chain[1]["value"] = 9999  # attacker modifies
        save_chain(chain)
        return "Block modified by attacker"
    return "Not enough logs"