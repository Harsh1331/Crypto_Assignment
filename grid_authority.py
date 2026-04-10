import hashlib
import time
import json
import os
import ascon

def generate_hex(input_string):
    sha3_hash = hashlib.sha3_256()
    sha3_hash.update(input_string.encode('utf-8'))
    hex_output = sha3_hash.hexdigest()
    return hex_output[0:16]

class GridAuthority:
    def __init__(self, data_file='grid_data.json'):
        self.data_file = data_file
        self.franchises = {}
        self.users = {}
        self.blockchain_ledger = []
        self.load_data()

    def save_data(self):
        data = {
            "franchises": self.franchises,
            "users": self.users,
            "blockchain_ledger": self.blockchain_ledger
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.franchises = data.get("franchises", {})
                self.users = data.get("users", {})
                self.blockchain_ledger = data.get("blockchain_ledger", [])
                print("Data loaded successfully.")
        else:
            print("No existing data found. Starting fresh.")
            self.save_data()

    def clear_data(self):
        self.franchises = {}
        self.users = {}
        self.blockchain_ledger = []
        self.save_data()
        print("All data cleared.")

    def register_franchise(self, name, zone_code, password, initial_bal):
        timestamp = str(time.time())
        seed = f"{name}{timestamp}{password}"
        fid = generate_hex(seed)
        self.franchises[fid] = {
            "name": name,
            "balance": initial_bal,
            "zone": zone_code
        }
        print(f"Franchise registered: {fid} - {name} in zone {zone_code} with balance {initial_bal}")
        self.save_data()
        return fid

    def register_user(self, name, zone_code, password, initial_bal, pin, phone_number):
        timestamp = str(time.time())
        seed = f"{name}{timestamp}{password}"
        uid = generate_hex(seed)
        vmid_seed = f"{uid}{phone_number}"
        vmid = generate_hex(vmid_seed)
        self.users[vmid] = {
            "uid": uid,
            "name": name,
            "pin": pin,
            "balance": initial_bal,
            "zone": zone_code
        }
        print(f"User registered: {vmid} - {name} in zone {zone_code} with balance {initial_bal}")
        self.save_data()
        return vmid
    
    def process_transaction(self, qr_data, vmid, pin, amount):
        nonce = bytes.fromhex(qr_data["nonce"])
        ciphertext = bytes.fromhex(qr_data["ciphertext"])
        kiosk_key = b"1234567890abcdef"  # This should match the key used by the kiosk

        try:
            plaintext = ascon.decrypt(kiosk_key, nonce, b"", ciphertext, variant="Ascon-128")
            decoded = plaintext.decode('utf-8')
            fid, timestamp = decoded.split("_")
        except Exception:
            return "Invalid QR code data."
        
        if time.time() - float(timestamp) > 300:
            return "QR code has expired."
        
        if vmid not in self.users:
            return "User not found."
        
        if self.users[vmid]["pin"] != pin:
            return "Incorrect PIN."
        
        if self.users[vmid]["balance"] < amount:
            return "Insufficient balance."
        
        if fid not in self.franchises:
            return "Franchise not found."
        
        self.users[vmid]["balance"] -= amount
        self.franchises[fid]["balance"] += amount

        self.create_block(uid=self.users[vmid]["uid"], fid=fid, amount=amount, dispute_flag=False)
        self.save_data()
        return f"Transaction successful! User {self.users[vmid]['name']} charged {amount} units at franchise {self.franchises[fid]['name']}."
    
    def create_block(self, uid, fid, amount, dispute_flag=False):
        timestamp = str(time.time())
        if(len(self.blockchain_ledger) == 0):
            previous_hash = "0" * 64
        else:
            previous_hash = self.blockchain_ledger[-1]["hash"]

        seed = f"{uid}{fid}{amount}{timestamp}"
        block_hash = generate_hex(seed)

        new_block = {
            "hash": block_hash,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "amount": amount,
            "dispute_flag": dispute_flag
        }

        self.blockchain_ledger.append(new_block)
        #self.save_data()

    def report_hw_failure(self, vmid, fid, amount):
        print(f"Hardware failure reported for VMID {vmid} at Franchise {fid} for amount {amount}. Initiating refund...")
        self.users[vmid]["balance"] += amount
        self.franchises[fid]["balance"] -= amount
        self.create_block(uid=self.users[vmid]["uid"], fid=fid, amount=amount, dispute_flag=True)
        self.save_data()
        return f"Refund processed for user {self.users[vmid]['name']} for amount {amount} units from franchise {self.franchises[fid]['name']}."