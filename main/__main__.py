import sys
import os


# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)


from lib import lib
from config import config
from engine import engine as engine_module


def main() -> None:
    cfg_path = parent + r'\config.yml'
    cfg = config.load_config(cfg_path)

    engine = engine_module.Engine(cfg)
    engine.run()


if __name__ == '__main__':
    main()
