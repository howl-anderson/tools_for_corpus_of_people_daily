import os


def create_if_dir_not_exists(path_dir):
    if os.path.exists(path_dir):
        if not os.path.isdir(path_dir):
            raise ValueError("path: {} exits, but is not a directory!".format(path_dir))
    else:
        os.makedirs(path_dir, exist_ok=True)
