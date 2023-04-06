import os


def get_app_dir(file_globvar=__file__) -> str:
    return os.path.dirname(os.path.abspath(file_globvar)) + '\\'
