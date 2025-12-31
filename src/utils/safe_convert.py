#Functions to safely convert data

def get_float(str:str, default = None) -> float:
    """Converts str into float safely"""

    try:
        return float(str)
    except (ValueError,TypeError):
        return default