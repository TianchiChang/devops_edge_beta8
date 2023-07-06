import os

def is_file_or_dir(path):
    if os.path.isdir(path):
        return False
    elif os.path.isfile(path):
        return True