from datetime import datetime
import shutil, os


def time_now(formato):
    return datetime.now().strftime(formato)

def set_folder(folder_path, rewrite=False):
    if os.path.exists(folder_path) and rewrite:
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)


