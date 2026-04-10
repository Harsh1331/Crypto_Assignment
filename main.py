import grid_authority
import charging_kiosk
import quantum_sim
import time

def print_header(title):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def main():
    print_header("Initializing Grid Authority")
    grid = grid_authority.GridAuthority()

    activate_kiosk = None
    scannable_qr = None
    demo_fid = None

    while True:
        print_header("Main Menu")
        print("1. Register Franchise")
        print("2. Register User")
        print("3. Activate Charging Kiosk")
        print("4. Simulate QR Code Scan")
        print("5. View Blockchain Ledger")
        print("6. Run Shor's Algorithm (Quantum Simulation)")
        print("7. Clear All Data")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print_header("Registering Franchise")
            name = input("Enter franchise name: ")
            zone_code = input("Enter zone code: ")
            password = input("Enter password: ")
            initial_bal = float(input("Enter initial balance: "))
            demo_fid = grid.register_franchise(name, zone_code, password, initial_bal)
            print(f"Franchise registered with ID: {demo_fid}")

        elif choice == '2':
            print_header("Registering User")
            name = input("Enter user name: ")
            zone_code = input("Enter zone code: ")
            password = input("Enter password: ")
            initial_bal = float(input("Enter initial balance: "))
            pin = input("Set a 4-digit PIN: ")
            phone_number = input("Enter phone number: ")
            vmid = grid.register_user(name, zone_code, password, initial_bal, pin, phone_number)
            print(f"User registered with VMID: {vmid}")

        elif choice == '3':
            fid = input("Enter franchise ID to activate kiosk: ")
            if fid not in grid.franchises:
                print("Invalid franchise ID. Please try again.")
                continue
            activate_kiosk = charging_kiosk.ChargingKiosk(demo_fid, grid)
            scannable_qr = activate_kiosk.generate_qr_code()
            print("Charging kiosk activated and QR code generated.")
            print(f"QR Code Data: {scannable_qr}")

        elif choice == '4':
            if scannable_qr is None:
                print("Please activate a charging kiosk first.")
                continue
            vmid = input("Enter your VMID to scan QR code: ")
            pin = input("Enter your PIN: ")
            amount = float(input("Enter amount to charge (units): "))
            result = grid.process_transaction(scannable_qr, vmid, pin, amount)
            print(f"Transaction result: {result}")
            #scannable_qr = None  # Invalidate QR code after one use

        elif choice == '5':
            print_header("Blockchain Ledger")
            if len(grid.blockchain_ledger) == 0:
                print("No transactions recorded yet.")
            else:
                for idx, block in enumerate(grid.blockchain_ledger):
                    timestamp = float(block['timestamp']) if 'timestamp' in block else None
                    timestamp_str = time.ctime(timestamp) if timestamp else 'Unknown'
                    print(f"Block {idx+1}: TXID: {block.get('hash', 'N/A')}, PrevHash: {block.get('previous_hash', 'N/A')}, Dispute: {block.get('dispute_flag', 'N/A')}, Timestamp: {timestamp_str}")

        elif choice == '6':
            public_key_N = int(input("Enter a composite number (public key) to factor: "))
            public_exponent_e = 7
            secret_pin = 123
            encrypted_pin = (secret_pin ** public_exponent_e) % public_key_N
            
            print(f"\n[Network] Grid broadcasts RSA Public Key N={public_key_N}")
            print(f"[Network] User sends encrypted PIN: {encrypted_pin}")
            time.sleep(2)
            
            attacker = quantum_sim.QuantumAttacker()
            cracked_p, cracked_q = attacker.shors_algorithm(public_key_N)
            
            phi_N = (cracked_p - 1) * (cracked_q - 1)
            private_key_d = pow(public_exponent_e, -1, phi_N)
            stolen_pin = (encrypted_pin ** private_key_d) % public_key_N
            
            print(f"\n🔓 ATTACK SUCCESSFUL: Hacker decrypted the PIN: {stolen_pin}")
            print("Demonstration concludes: Post-Quantum defenses are necessary.")

        elif choice == '7':
            grid.clear_data()
        
        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()