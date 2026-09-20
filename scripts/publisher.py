import json
from curl_cffi import requests, CurlMime, CurlHttpVersion
import os

import utils



# ---------- Constants ----------

CF_LOADER_NAMES = {
    "fabric":   "Fabric",
    "forge":    "Forge",
    "neoforge": "NeoForge",
    "quilt":    "Quilt",
}



# ---------- Logic ----------

def publish(MODRINTH_TOKEN, CURSEFORGE_TOKEN, mods, register, changelogs, directory, history):
    logs = []
    for mod in mods:
        if mod[1] in register:
            project_cf_id = register[mod[1]]["curseforge_id"]
            project_md_id = register[mod[1]]["modrinth_id"]
            file = directory + "/" + mod[0]
            version = mod[2]
            changelog=""
            if mod[1] in changelogs and mod[2] in changelogs[mod[1]]:
                changelog = utils.format_changes(mod[1], register[mod[1]]["name"], changelogs[mod[1]][version]["name"], mod[2], changelogs[mod[1]][version]["changes"])
            name = f"{register[mod[1]]['name']} {version} for {mod[3].capitalize()} {mod[4]}"
            mc_version = mod[4]
            loader = mod[3]
            mr_dependencies = register[mod[1]]["modrinth_deps"]
            cf_dependencies = register[mod[1]]["curseforge_deps"]
            if project_cf_id != "" and CURSEFORGE_TOKEN != "" and mod[0]+"-cf" not in history:
                response = upload_curseforge(CURSEFORGE_TOKEN, project_cf_id, file, name, version, mc_version, loader, changelog, cf_dependencies)
                logs.append(response)
            if project_md_id != "" and MODRINTH_TOKEN != "" and mod[0]+"-mr" not in history:
                response = upload_modrinth(MODRINTH_TOKEN, project_md_id, file, name, version, mc_version, loader, changelog, mr_dependencies)
                logs.append(response)
    return logs


def upload_modrinth(KEY, project_id, file, name, mod_version, mc_version, loader, changelog, dependencies):
    proj_resp = requests.get(f"https://api.modrinth.com/v2/project/{project_id}", impersonate="chrome")
    if proj_resp.ok:
        project_id = proj_resp.json()["id"]

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
            for dep in dependencies if dep
        ],
    }

    mp = CurlMime()
    mp.addpart(name="data", content_type="application/json", data=json.dumps(version_data).encode())
    mp.addpart(name="jar_file", content_type="application/java-archive", filename=os.path.basename(file), local_path=file)

    response = requests.post(
        "https://api.modrinth.com/v2/version",
        headers={"Authorization": KEY},
        multipart=mp,
        impersonate="safari",
        http_version=CurlHttpVersion.V1_1
    )
    mp.close()

    if response.ok:
        try:
            data = response.json()
            return ["Success", file, f"was published to Modrinth as file {data['id']}"]
        except Exception:
            return ["Error", file, f"Modrinth returned non-JSON response [{response.status_code}]: {response.text[:300]}"]
    else:
        return ["Error", file, f"Modrinth upload failed [{response.status_code}]: {response.text}"]


def upload_curseforge(KEY, project_id, file, name, mod_version, mc_version, loader, changelog, dependencies):
    metadata = {
        "changelog": changelog,
        "changelogType": "markdown",
        "displayName": name,
        "gameVersionNames": ["Client", "Server", mc_version, CF_LOADER_NAMES.get(loader.lower(), loader)],
        "releaseType": "release",
    }

    valid_deps = [dep for dep in dependencies if dep]
    if valid_deps:
        metadata["relations"] = {
            "projects": [
                {"slug": dep, "type": "requiredDependency"}
                for dep in valid_deps
            ]
        }

    mp = CurlMime()
    mp.addpart(name="metadata", content_type="application/json", data=json.dumps(metadata).encode())
    mp.addpart(name="file", content_type="application/java-archive", filename=os.path.basename(file), local_path=file)

    response = requests.post(
        f"https://minecraft.curseforge.com/api/projects/{project_id}/upload-file",
        headers={"X-Api-Token": KEY, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        multipart=mp,
        impersonate="safari",
        http_version=CurlHttpVersion.V1_1
    )
    mp.close()

    if response.ok:
        try:
            data = response.json()
            return ["Success", file, f"was published to CurseForge as file {data['id']}"]
        except Exception:
            return ["Error", file, f"CurseForge returned non-JSON response [{response.status_code}]: {response.text[:300]}"]
    else:
        return ["Error", file, f"CurseForge upload failed [{response.status_code}]: {response.text}"]