from datetime import datetime


def fecha_a_cuid(fecha_str: str) -> int:
    """
    Convert YYYY-MM-DD to cuid short format YYYYMMDD05000000000.
    """
    datetime.strptime(fecha_str, "%Y-%m-%d")
    return int(fecha_str.replace("-", "") + "05000000000")

