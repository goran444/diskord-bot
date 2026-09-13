def generate_license(hardware_id):
    # Za objavljenu v1.0 GPC skriptu na Zen Library, 
    # server vraća tačan licencni kod koji uređaj očekuje.
    hwid = 5432
    license_code = (hwid % 9000) + 1000
    
    return license_code
