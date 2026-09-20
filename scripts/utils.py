import os
from parse import parse
import shutil
import json


# ---------- Operations with directories ----------

def create_dirs(mods_dir):
    if mods_dir == "":
        if not os.path.exists(os.path.dirname(__file__)+"/../mods"):
            os.makedirs(os.path.dirname(__file__)+"/../mods")
    else:
        if not os.path.exists(mods_dir):
            os.makedirs(mods_dir)

def remove_dirs(mods_dir):
    if os.path.exists(mods_dir):
        shutil.rmtree(mods_dir)



# ---------- Operations with mods ----------

def get_mods(directory, mod_file_format, history):
    if os.path.exists(directory):
        raw_files = os.listdir(directory)

    if len(raw_files) > 0:
        logs = []    
        files = [] 
        for file in raw_files:
            final = convert_to_data(file, mod_file_format, history)
            if final[0] != "Warn" and final[0] != "Error":
                files.append(final)
            else:
                logs.append(final)
        return files, logs
    return [], [["Error", "", "No mods in directory found!"]]


def convert_to_data(file, mod_file_format, history = None):
    if "-sources" in file or "-javadoc" in file:
        return ["Warn", file, "This file is not a valid mod file, skipping..."]
    if history is None:
        history = set()
    parsed = parse(mod_file_format, file)
    if parsed:
        if not file in history:
            return [file, parsed["mod_id"], parsed["mod_version"], parsed["loader"], parsed["mc_version"]]
        else:
            return ["Error", file, "This file was already published."]
    else:
        return ["Error", file, "This file does not follow the required naming convention, skipping..."]



# ---------- Main logic ----------

def save_dict(value):
    return json.dumps(value)


def get_dict(raw):
    default={}
    if raw:
        return json.loads(raw)
    return default



# ---------- Formatting ----------

def format_changes(mod_id, mod_name, name, version, changes):
    final_changes = ""
    for change in changes:
        final_changes += f"- {change}\n"
    return f"# ***{name}***\n###### v{version} for {mod_name}\n---\n ### What's New:\n {final_changes}" 
