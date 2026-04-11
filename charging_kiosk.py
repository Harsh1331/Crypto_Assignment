import time
import os
import ascon

class ChargingKiosk:
    def __init__(self, franchise_id, grid_network):
        self.franchise_id = franchise_id
        self.grid = grid_network
        self.kiosk_key = b"1234567890abcdef"  # Fixed key for testing

    def generate_qr_code(self):
        timestamp = str(time.time())
        plaintext = f"{self.franchise_id}_{timestamp}"
        plaintext = plaintext.encode('utf-8')
        nonce = os.urandom(16)
        cipher = ascon.encrypt(self.kiosk_key, nonce, b"", plaintext, variant="Ascon-128")
        print(f"Generated QR code for franchise {self.franchise_id}")

        return {
            "nonce": nonce.hex(),
            "ciphertext": cipher.hex()
        }