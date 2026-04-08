import grid_authority
import charging_kiosk
# --- Test Script ---
if __name__ == "__main__":
    from pprint import pprint # Just to make printing dictionaries look nice
    
    # 1. Start the Grid
    my_grid = grid_authority.GridAuthority()
    
    # 2. Register a Franchise (or use an existing one if loaded from JSON)
    # We will grab the FID returned by the registration
    test_fid = my_grid.register_franchise("AdaniPower", "Zone_B", "securePass456", 1000.0)
    
    # 3. Turn on a Charging Kiosk at that Franchise
    station_kiosk = charging_kiosk.ChargingKiosk(franchise_id=test_fid, grid_network=my_grid)
    
    # 4. Generate the QR Code!
    scannable_qr = station_kiosk.generate_qr_code()
    
    print("\n--- What the EV Owner's Phone Scans ---")
    pprint(scannable_qr)

    # ... (your previous test code where you generate the QR code) ...

    print("\n--- EV Owner Scans QR and Requests Charge ---")
    # Let's assume the user we registered earlier wants $25 worth of charge.
    # We pass the QR data they scanned, their VMID, their PIN, and the amount.

    # NOTE: Replace 'test_vmid' with the actual variable holding the VMID 
    # you got when you ran register_user() earlier!
    response = my_grid.process_transaction(
        qr_data=scannable_qr, 
        vmid="c22d36f05fca6b03", 
        pin="1234", # The PIN we set during registration
        amount=25.0
    )

    print(response)

    # Print the balances to prove the money moved!
    print(f"User Balance: {my_grid.users['c22d36f05fca6b03']['balance']}")
    print(f"Franchise Balance: {my_grid.franchises[test_fid]['balance']}")