import os
from parse import parse

template = "{mod_id}[{mod_version}]-{loader}({mc_version}).jar"

def get_mods():
    if os.path.exists("mods"):
        raw_files = os.listdir("mods")

    if len(raw_files) > 0:
        logs = []    
        files = [] 
        for file in raw_files:
            final = convert_to_data(file)
            if final[0] != "warn" and final[0] != "error":
                files.append(final)
            else:
                logs.append(final)


def convert_to_data(file):
    if file.contains("-sources") or file.contains("-javadoc"):
        return ["warn", "file", "This file is not a valid mod file, skipping..."]
    parsed = parse(template, file)
    if parsed:
        return [file, parsed["mod_id"], parsed["mod_version"], parsed["loader"], parsed["mc_version"]]
    else:
        return ["error", "file", "This file does not follow the required naming convention, skipping..."]

