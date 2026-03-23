import os
import json
from parse import parse



settings_template = {
    "mods_path": "mods",
    "mod_file_format": "{mod_id}[{mod_version}]-{loader}({mc_version}).jar",
    "diplay_unknown_mods": True,
    "display_mods_without_changelog": True,
    "show_logs": True,
    "save_cache": True,
}



def get_mods():
    if os.path.exists(get_settings("mods_path")):
        raw_files = os.listdir(get_settings("mods_path"))

    if len(raw_files) > 0:
        logs = []    
        files = [] 
        for file in raw_files:
            final = convert_to_data(file)
            if final[0] != "Warn" and final[0] != "Error":
                files.append(final)
            else:
                logs.append(final)
        return files, logs
    return [], [["Error", "", "No mods in directory found!"]]

def convert_to_data(file):
    if "-sources" in file or "-javadoc" in file:
        return ["Warn", file, "This file is not a valid mod file, skipping..."]
    parsed = parse(get_settings("mod_file_format"), file)
    if parsed:
        return [file, parsed["mod_id"], parsed["mod_version"], parsed["loader"], parsed["mc_version"]]
    else:
        return ["Error", file, "This file does not follow the required naming convention, skipping..."]



def create_dirs():
    if not os.path.exists(os.path.dirname(__file__)+"/../mods"):
        os.makedirs(os.path.dirname(__file__)+"/../mods")

    if not os.path.exists(os.path.dirname(__file__)+"/../changelogs"):
        os.makedirs(os.path.dirname(__file__)+"/../changelogs")



def check_settings():
    return os.path.exists(os.path.dirname(__file__)+"/../settings.json")

def create_settings():
    with open(os.path.dirname(__file__)+"/../settings.json", "w") as f:
        json.dump(settings_template, f)

def get_settings(field):
    with open(os.path.dirname(__file__)+"/../settings.json", "r") as f:
        settings = json.load(f)
        return settings[field]
    
def save_settings(new_settings):
    with open(os.path.dirname(__file__)+"/../settings.json", "w") as f:
        json.dump(new_settings, f)



def check_data():
    return os.path.exists(os.path.dirname(__file__)+"/../access.json")

def create_data():
    with open(os.path.dirname(__file__)+"/../access.json", "w") as f:
        json.dump({
            "curseforge_token": "token",
            "modrinth_token": "token",
            "mods": {
                "mod_id1": {"name": "Mod Name 1", "curseforge": "CF Project ID", "modrinth": "Modrinth Project ID"},
                "mod_id2": {"name": "Mod Name 2", "curseforge": "CF Project ID", "modrinth": "Modrinth Project ID"}
            }
        }, f, indent=4)

def check_mod(mod_id):
    with open(os.path.dirname(__file__)+"/../access.json", "r") as f:
        data = json.load(f)
        return mod_id in data["mods"]
    
def get_access(field, mod_id=None):
    with open(os.path.dirname(__file__)+"/../access.json", "r") as f:
        data = json.load(f)
        if mod_id:
            return data["mods"][mod_id][field]
        else:
            return data[field]

def has_changelog(mod_id):
    return os.path.exists(os.path.dirname(__file__)+"/../changelogs/"+mod_id+".md")

def get_changelog(mod_id):
    with open(os.path.dirname(__file__)+"/../changelogs/"+mod_id+".md", "r") as f:
        return f.read()

def save_cache(cache):
    with open(os.path.dirname(__file__)+"/../cache.json", "w") as f:
        json.dump(cache, f, indent=4) 