import os
import json
from parse import parse



template = "{mod_id}[{mod_version}]-{loader}({mc_version}).jar"

settings_template = {
    "mods_path": "mods",
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
    parsed = parse(template, file)
    if parsed:
        return [file, parsed["mod_id"], parsed["mod_version"], parsed["loader"], parsed["mc_version"]]
    else:
        return ["Error", file, "This file does not follow the required naming convention, skipping..."]




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