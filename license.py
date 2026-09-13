def generate_license(hardware_id: int) -> int:
    return (hardware_id % 9000) + 1000
