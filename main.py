import engine.engine as engine_module
import constants


def main() -> None:
    engine = engine_module.Engine(constants.cfg)
    engine.run()


if __name__ == '__main__':
    main()
