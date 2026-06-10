import json
import requests

def publish(MODRINTH_TOKEN, CURSEFORGE_TOKEN, mods, register, curseforge):
    logs = [] # file, parsed["mod_id"], parsed["mod_version"], parsed["loader"], parsed["mc_version"]
    for mod in mods:
        if mod[1] in register:
            project_cf_id = register[mod[1]]["curseforge_id"]
            project_md_id = register[mod[1]]["modrinth_id"]
            file = mod[0]
            if project_cf_id != "":
                upload_curseforge(CURSEFORGE_TOKEN, project_cf_id, file)
            if project_md_id != "":
                upload_curseforge(MODRINTH_TOKEN, project_md_id, file)
    return logs

def upload_modrinth(KEY, project_id):
    pass

def upload_curseforge(KEY, project_id):
    pass