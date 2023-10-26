def fast_crc8(data):
    """calculate fast crc 8 for data
    Args:
        data (bytes): data for calculation crc 8
    Returns:
        int: crc 8 bit
    """
    res = 0
    for val in data:
        res = 0xff & ((res << 2) | (res >> 6)) ^ val
    return 0xff & ((res << 2) | (res >> 6))
