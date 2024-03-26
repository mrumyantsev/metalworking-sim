def get_color_value(config_value: str) -> tuple:
    rgb_strings = config_value.split(' ')
    rgb_ints = [int(c) for c in rgb_strings]
    return tuple(rgb_ints)


# Pseudo banker's rounding.
def pbround(value: float) -> int:
    return round(value + 0.1)
