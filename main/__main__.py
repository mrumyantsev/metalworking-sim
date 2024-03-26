import sys
import os


# getting the name of the directory
# where the this file is present.
current_dir = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
project_dir = os.path.dirname(current_dir)

# adding the parent directory to
# the sys.path.
sys.path.append(project_dir)


from lib import lib
from config import config
from engine import engine as engine_module


def main() -> None:
    cfg_path = os.path.join(project_dir, 'config.yml')
    cfg = config.load_config(cfg_path)

    engine = engine_module.Engine(cfg)
    engine.run()


if __name__ == '__main__':
    main()
