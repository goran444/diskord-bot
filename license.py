
def generate_license(hardware_id):
    try:
        # Zadržavamo samo cifre iz bilo kog serijskog broja (bilo da ima PE, AB ili druga slova)
        digits_only = ''.join(filter(str.isdigit, str(hardware_id)))
        
        if not digits_only:
            hwid = 5432
        else:
            hwid = int(digits_only)
    except (ValueError, TypeError):
        hwid = 5432

    # Matematika potpuno identična GPC skripti
    license_code = (hwid % 9000) + 1000
    return license_code
