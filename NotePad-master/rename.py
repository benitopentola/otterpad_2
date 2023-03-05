import os

def rename_file(current_file, new_name):
    if not current_file:
        return

    os.rename(current_file, new_name)