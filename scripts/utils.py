import os


# Directories

def create_dirs(mods_dir, changelogs_dir):
    if mods_dir == "":
        if not os.path.exists(os.path.dirname(__file__)+"/../mods"):
            os.makedirs(os.path.dirname(__file__)+"/../mods")

        if not os.path.exists(os.path.dirname(__file__)+"/../changelogs"):
            os.makedirs(os.path.dirname(__file__)+"/../changelogs")
    else:
        if not os.path.exists(mods_dir):
            os.makedirs(mods_dir)

        if not os.path.exists(changelogs_dir):
            os.makedirs(changelogs_dir)

def log(message):
    print(message)