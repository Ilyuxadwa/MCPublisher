import os


# Directories

def create_dirs(mods_dir):
    if mods_dir == "":
        if not os.path.exists(os.path.dirname(__file__)+"/../mods"):
            os.makedirs(os.path.dirname(__file__)+"/../mods")
    else:
        if not os.path.exists(mods_dir):
            os.makedirs(mods_dir)

def remove_dirs(mods_dir):
    if os.path.exists(mods_dir):
        os.rmdir(mods_dir)


    
def error(message):
    print(f"[ERROR] {message}")

def warn(message):
    print(f"[WARN] {message}")

def debug(message):
    print(f"[DEBUG] {message}")

def log(type,message):
    print(f"[{type}] {message}")
