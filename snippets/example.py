def safe_average(values: list[float], default: float = 0.0) -> float:
    if not values:
        return default
    return sum(values) / len(values)
