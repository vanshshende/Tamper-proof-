
## TEAM NAME:   CHAIN CODER

# Team Member:
        1.Vansh Shende  (Team Leader )
        2.Tanush Bobade
        3.Yash Awari
        4.Shreyanshu Shendre
        5.Pranay Chikankar

<---  IoT systems are vulnerable to hacker attacks that alter data, requiring a blockchain‑based solution to ensure integrity and detect tampering instantly. --- >


## Technologies used are : 

    1.Go(golang) – Backend logic for verification, hash generation, and secure communication between IoT devices and blockchain.
    2.Blockchain Database – Stores immutable hashes of firmware and sensor data for tamper-proof validation.
    3.IoT Sensor Simulation – Virtual environment used to simulate real hardware devices and test security scenarios.
    4.Cryptographic Hashing – Ensures data integrity by generating unique digital fingerprints.
    5.API Communication Layer – Enables secure data exchange between IoT devices, gateway, and blockchain network.


## Setup Step:

Tamper-proof/
│
├── __pycache__/
├── frontend/
├── app.py
├── blockchain.py
├── git
├── logs.json
├── README.md


## Process ﬂow diagram or Use-case diagram

                            Sensor Collects Data
                                    ↓
                            Server Receives Data
                                    ↓
                        Store as Block in Blockchain
                        (Hash + Previous Hash Linked)
                                    ↓
                            Run Verification
                                    ↓
                            Tampering Detected ?
                            ↓                ↓
                            YES              NO
                            ↓                ↓
                    Alert + Timestamp     Data Valid
                    Mark Block Corrupt    Continue System



## Brief :

1.IoT systems are often targeted by hackers who alter or inject malicious data.
2.Traditional databases cannot guarantee tamper-proof security.
3.By storing data hashes on blockchain, every record becomes immutable and verifiable.
4.If a hacker changes the database, the blockchain detects a mismatch.
5.A notification system alerts the user/admin instantly about the unauthorized change.
6.This ensures data integrity, trust, and real-time security in IoT ecosystems .


## USP of the proposed solution :

1.Immutable security: Blockchain ensures data integrity. Instant alerts: Real-time detection of tampering.
2.Scalable design: Works across diverse IoT ecosystems.
3.Prevention-first approach: Stops botnet-style attacks at the root.


## features offered by the solution :

1.Blockchain-Based Security – Stores firmware/data hashes on an immutable ledger.
2. Decentralized Verification – No single point of failure or central authority.
3. Immutable Audit Trail – All updates and transactions are permanently recorded.
4. Lightweight Integration – Designed to work efficiently with low-power IoT devices.
5. Automatic Alert System – Sends notification when suspicious activity is detected.
6. Secure Firmware Updates – Only verified and trusted updates are accepted.
7. Scalable Architecture – Can be deployed across small networks to large IoT ecosystems.


## Research & References

## 🚨 Real-World Attacks That Inspired This Project

1. **Stuxnet Industrial Cyber‑Attack**
    A highly sophisticated worm targeting industrial control systems (SCADA/PLC) used in Iranian nuclear facilities. It altered the sensor/PLC control logic and hid the real physical state from operators so the machines behaved dangerously while reporting normal values

2. **2016 – Shamoon (Shamoon Variant) Attacks**
A destructive malware campaign hit Middle-East energy and infrastructure networks, wiping thousands of systems and disrupting operations. It showed how critical infrastructure can be crippled without strong integrity and monitoring mechanisms.


