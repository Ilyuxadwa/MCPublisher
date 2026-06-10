import json
import requests
import utils

def publish(MODRINTH_TOKEN, CURSEFORGE_TOKEN, mods, register, changelogs):
    logs = []
    for mod in mods:
        if mod[1] in register:
            project_cf_id = register[mod[1]]["curseforge_id"]
            project_md_id = register[mod[1]]["modrinth_id"]
            file = mod[0]
            version = mod[2]
            changelog = utils.format_changes(mod[1], register[mod[1]]["name"], changelogs[mod[1]][version]["name"], mod[2], changelogs[mod[1]][version]["changes"])
            name = register[mod[1]]["name"] + version + mod[3].capitalize() + mod[4]
            mc_version = mod[4]
            loader = mod[3]
            mr_dependencies = register[mod[1]]["modrinth_deps"]
            cf_dependencies = register[mod[1]]["curseforge_deps"]
            if project_cf_id != "" and CURSEFORGE_TOKEN != "":
                upload_curseforge(CURSEFORGE_TOKEN, project_cf_id, file, name, version, mc_version, loader, changelog, cf_dependencies)
            if project_md_id != "" and MODRINTH_TOKEN != "":
                upload_curseforge(MODRINTH_TOKEN, project_md_id, file, name, version, mc_version, loader, changelog, mr_dependencies)
    return logs

def upload_modrinth(KEY, project_id, file, name, mod_version, mc_version, loader, changelog, dependencies):
    print (KEY, project_id, name, mod_version, mc_version, loader, changelog)

def upload_curseforge(KEY, project_id, file, name, mod_version, mc_version, loader, changelog, dependencies):
    print (KEY, project_id, name, mod_version, mc_version, loader, changelog)