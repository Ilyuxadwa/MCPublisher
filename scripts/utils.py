import os
from parse import parse
import json


# Directories operations

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


# Mods operations

def get_mods(directory, mod_file_format):
    if os.path.exists(directory):
        raw_files = os.listdir(directory)

    if len(raw_files) > 0:
        logs = []    
        files = [] 
        for file in raw_files:
            final = convert_to_data(file, mod_file_format)
            if final[0] != "Warn" and final[0] != "Error":
                files.append(final)
            else:
                logs.append(final)
        return files, logs
    return [], [["Error", "", "No mods in directory found!"]]

def convert_to_data(file, mod_file_format):
    if "-sources" in file or "-javadoc" in file:
        return ["Warn", file, "This file is not a valid mod file, skipping..."]
    parsed = parse(mod_file_format, file)
    if parsed:
        return [file, parsed["mod_id"], parsed["mod_version"], parsed["loader"], parsed["mc_version"]]
    else:
        return ["Error", file, "This file does not follow the required naming convention, skipping..."]

def save_dict(value):
    return json.dumps(value)

def get_dict(raw):
    default={}
    if raw:
        return json.loads(raw)
    return default

# Logging operations

def error(message):
    print(f"[ERROR] {message}")

def warn(message):
    print(f"[WARN] {message}")

def debug(message):
    print(f"[DEBUG] {message}")

def log(type,message):
    print(f"[{type}] {message}")
