import json
import requests
import utils

CF_LOADER_NAMES = {
    "fabric":   "Fabric",
    "forge":    "Forge",
    "neoforge": "NeoForge",
    "quilt":    "Quilt",
}

def publish(MODRINTH_TOKEN, CURSEFORGE_TOKEN, mods, register, changelogs):
    logs = []
    for mod in mods:
        if mod[1] in register:
            project_cf_id = register[mod[1]]["curseforge_id"]
            project_md_id = register[mod[1]]["modrinth_id"]
            file = mod[0]
            version = mod[2]
            changelog=""
            if mod[1] in changelogs and mod[2] in changelogs[mod[1]]:
                changelog = utils.format_changes(mod[1], register[mod[1]]["name"], changelogs[mod[1]][version]["name"], mod[2], changelogs[mod[1]][version]["changes"])
            name = f"{register[mod[1]]['name']} {version} for {mod[3].capitalize()} {mod[4]}"
            mc_version = mod[4]
            loader = mod[3]
            mr_dependencies = register[mod[1]]["modrinth_deps"]
            cf_dependencies = register[mod[1]]["curseforge_deps"]
            if project_cf_id != "" and CURSEFORGE_TOKEN != "":
                pass#response = upload_curseforge(CURSEFORGE_TOKEN, project_cf_id, file, name, version, mc_version, loader, changelog, cf_dependencies)
            if project_md_id != "" and MODRINTH_TOKEN != "":
                response = upload_modrinth(MODRINTH_TOKEN, project_md_id, file, name, version, mc_version, loader, changelog, mr_dependencies)
                logs.append(response)
    return logs

def upload_modrinth(KEY, project_id, file, name, mod_version, mc_version, loader, changelog, dependencies):
    version_data = {
        "project_id": project_id,
        "name": name,
        "version_number": mod_version,
        "changelog": changelog,
        "version_type": "release",
        "loaders": [loader.lower()],
        "game_versions": [mc_version],
        "featured": False,
        "file_parts": ["jar_file"],
        "primary_file": "jar_file",
        "dependencies": [
            {"project_id": dep, "dependency_type": "required"}
            for dep in dependencies
        ],
    }

    with open(file, "rb") as jar:
        response = requests.post(
            "https://api.modrinth.com/v2/version",
            headers={"Authorization": KEY},
            data={"data": json.dumps(version_data)},
            files={"jar_file": (file, jar, "application/java-archive")},
        )

    if response.ok:
        data = response.json()
        return ["Success", file, f"was published to Modrinth as version {data['id']}"]
    else:
        return ["Error", file, f"Modrinth upload failed [{response.status_code}]: {response.text}"]


def upload_curseforge(KEY, project_id, file, name, mod_version, mc_version, loader, changelog, dependencies):
    metadata = {
        "changelog": changelog,
        "changelogType": "markdown",
        "displayName": name,
        "gameVersionNames": ["Client", "Server", mc_version, CF_LOADER_NAMES.get(loader.lower(), loader)],
        "releaseType": "release",
        "relations": {
            "projects": [
                {"slug": dep, "type": "requiredDependency"}
                for dep in dependencies
            ]
        },
    }

    with open(file, "rb") as jar:
        response = requests.post(
            f"https://minecraft.curseforge.com/api/projects/{project_id}/upload-file",
            headers={"X-Api-Token": KEY},
            data={"metadata": json.dumps(metadata)},
            files={"file": (file, jar, "application/java-archive")},
        )

    if response.ok:
        data = response.json()
        return ["Success", file, f"was published to CurseForge as file {data['id']}"]
    else:
        return ["Error", file, f"CurseForge upload failed [{response.status_code}]: {response.text}"]