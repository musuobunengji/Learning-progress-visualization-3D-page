def normalize_progress(percent: int | float) -> float:
    """
    turn progrss in data.json to %
    eg:80->0.8 79.3->0.793
    """
    return max(0.0, min(percent / 100.0, 1.0))
