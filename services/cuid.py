def fecha_a_cuid(fecha_str: str) -> int:
    """
    yyyy-mm-dd → yyyyMMdd05000000000
    """
    return int(fecha_str.replace("-", "") + "05000000000")
