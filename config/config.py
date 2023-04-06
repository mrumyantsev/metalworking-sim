import yaml


def load_config(path: str) -> dict:
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def get_color_value(config_value: str) -> tuple:
    rgb_strings = config_value.split(' ')
    rgb_ints = [int(c) for c in rgb_strings]
    return tuple(rgb_ints)
