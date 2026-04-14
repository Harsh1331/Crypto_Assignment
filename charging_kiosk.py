import time
import os
import ascon

class ChargingKiosk:
    def __init__(self, kiosk_id, grid_network):
        self.kiosk_id = kiosk_id
        self.grid = grid_network
        self.kiosk_key, self.franchise_id = self.grid.kiosk_secure_boot(kiosk_id)
        self.kiosk_key = bytes.fromhex(self.kiosk_key)
        if self.kiosk_key is None:
            raise Exception("Failed to secure boot the kiosk. Kiosk ID may be invalid.")

    def generate_qr_code(self):
        timestamp = str(time.time())
        plaintext = f"{self.franchise_id}_{timestamp}"
        plaintext = plaintext.encode('utf-8')
        nonce = os.urandom(16)
        cipher = ascon.encrypt(self.kiosk_key, nonce, b"", plaintext, variant="Ascon-128")
        print(f"Generated QR code for kiosk {self.kiosk_id}")

        return {
            "kiosk_id": self.kiosk_id,
            "nonce": nonce.hex(),
            "ciphertext": cipher.hex()
        }