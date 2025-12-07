# Python RaaS Simulator (Ransomware-as-a-Service)

An educational research project demonstrating the architecture of modern Ransomware attacks. This tool simulates a full attack lifecycle including **Discovery**, **C2 Communication**, **AES-256 Encryption**, and **Recovery**.

> **AFETY DISCLAIMER:** This software is for **educational purposes and security training only**. It is programmed to operate ONLY within a specific isolated directory (`Ransomware_Test_Folder`) and contains fail-safes to prevent accidental damage.

## Architecture

The project implements a **Client-Server** model typical of RaaS (Ransomware-as-a-Service) operations:

### 1. The C2 Server (`server.py`)
* Acts as the attacker's Command & Control infrastructure.
* Listens on a TCP socket for incoming connections from compromised hosts.
* **Key Management:** Securely receives and logs decryption keys.
* **Handshake:** Sends an acknowledgment ("ACK") signal only after the key is safely stored.

### 2. The Payload (`ransomware_v2.py`)
* **Reconnaissance:** Scans the target directory for valuable file extensions (`.txt`, `.docx`, `.png`, etc.).
* **Cryptography:** Generates a unique, ephemeral **AES-256** key using the `Fernet` library.
* **Fail-Safe Mechanism:** Connects to the C2 server and exfiltrates the key *before* any encryption takes place. If the C2 is unreachable, the encryption aborts.
* **Encryption:** Encrypts files and appends the `.encrypted` extension.

## Getting Started

### Prerequisites
* Python 3.x
* Cryptography library:
  ```bash
  pip install cryptography
  ```

### Usage Guide

To simulate the attack, you will need two separate terminal instances (one for the attacker, one for the victim).

#### Step 1: Prepare the Sandbox
Create the dummy files and target folder to simulate a victim's environment:
```bash
python3 setup_env.py
```

#### Step 2: Start the C2 Server (Attacker)
Open **Terminal #1** and run the listener:
```bash
python3 server.py
```
*Output: `[+] C2 Server Listening on port 5555...`*

#### Step 3: Execute the Malware (Victim)
Open **Terminal #2** and run the payload:
```bash
python3 ransomware_v2.py
```
*The script will generate a key, send it to the server, and encrypt the files in the test folder.*

#### Step 4: Decryption & Recovery
1. Check the server terminal (or `decryption_keys.txt`) to find the victim's key.
2. Paste the key into the payload's recovery prompt to restore the files.

## Skills Demonstrated
* **Malware Development:** Understanding ransomware logic flows.
* **Network Programming:** Python Socket API (TCP/IP).
* **Cryptography:** Symmetric encryption implementation (AES).
* **Defense Evasion:** Understanding C2 traffic patterns (IOCs).
