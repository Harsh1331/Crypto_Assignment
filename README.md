# Centralized EV Charging Payment Gateway

**Team Members:**   
Vishisht TB - 2023A7PS0042H  
Harsh Gunda - 2023AAPS0246H  
Sailesh Nichenametla - 2023A7PS0147H  
Aditya Prakash Jois - 2023A7PS0126H  
Mohammed Zeeshan Valappil - 2023AAPS0244H


## Overview
This project is a functional, centralized EV Charging Payment Gateway that mimics smart-grid transactions. Built purely in Python (using a json file to act as the database), it demonstrates how low-power edge devices (charging kiosks) can securely communicate with a central banking authority (the Grid) using lightweight cryptography, while protecting user identities and preventing network vulnerabilities.

## Features & Assumptions

**Charging Kiosk:**
* Each charging kiosk is registered with a unique Kiosk ID to identify it along with an FID which is used to generate a QR code for payment.
* In a real world scenario each kiosk generates a QR code which expires after a certain amount of time after which another QR code is generated.
* For this demonstration we manually activate a kiosk by providing the Kiosk ID. Once the QR code is generated it prints the QR data which we need to enter while making a transaction. This is the equivalent of scanning a QR code.
* To make it secure the QR code expires after 120 seconds and the QR code data contains a nonce which is added to a dictionary of used nonces if the transaction is successful to make sure the same QR code cannot be used for multiple payments.

**Blockchain Ledger:**
* Every transaction, including edge-case hardware refunds, is permanently recorded using a SHA3-256 hashed blockchain architecture.

**Quantum Threat Simulation (Shor's Algorithm):**
* Simulates Shor's Algorithm breaking classical RSA public key exchanges, actively factoring composite numbers to decrypt intercepted user credentials (VMID and PIN). 

## File Structure

* `main.py` - The interactive Command Line Interface (CLI) for demonstrating the system flow.
* `grid_authority.py` - The central server. Acts as the Key Management Service (KMS), the transaction verification node, and the blockchain ledger maintainer.
* `charging_kiosk.py` - The edge hardware simulation. Performs a secure boot to pull its unique secret key, then uses ASCON to generate encrypted, time-sensitive tokens.
* `quantum_sim.py` - The quantum attacker module housing the mathematical implementation of Shor's Algorithm.
* `grid_data.json` - The local JSON database storing state, balances, and registered network credentials.

## Installation & Requirements

**Requirements:**
* Python 3.8+
* `ascon` library

**Setup:**
```bash
pip install -r requirements.txt
python main.py
```
* The menu consists of 11 options:
  1. Register Franchise
  2. Register User
  3. Register Charging Kiosk
  4. Activate Charging Kiosk
  5. Make a payment or View Balance
  6. View Blockchain Ledger
  7. Run Shor's Algorithm
  8. Delete User
  9. Clear All Data
  10. Exit
  11. hwf - Simulate Hardware Failure
* The zone code entered must be A1, A2, A3, B1, B2, B3, C1, C2 or C3 since there are only 3 central energy providers with 3 zones each. 
* Upon execution of **4. Activate Charging Kiosk** the QR data must be copy pasted while executing **5. Make a Payment** within 120 seconds or 2 minutes.