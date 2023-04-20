from libs import lib
from config import config
from engine import engine as engine_module


def main() -> None:
    cfg_path = lib.get_app_dir(__file__) + 'config.yml'
    cfg = config.load_config(cfg_path)

    engine = engine_module.Engine(cfg)
    engine.run()


if __name__ == '__main__':
    main()
