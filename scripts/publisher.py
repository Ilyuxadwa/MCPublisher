import utils
import json
import requests

def publish():

    MODRINTH_TOKEN = utils.get_access("modrinth_token")
    CURSEFORGE_TOKEN = utils.get_access("curseforge_token")

    mods, logs = utils.get_mods()

    publish_logs = []

    for mod in mods:
        if utils.check_mod(mod[1]):
            file = utils.get_settings("mods_path") + "/" + mod[0]
            modrinth_project_id = utils.get_access("modrinth", mod[1])
            curseforge_project_id = utils.get_access("curseforge", mod[1])
            version_name = utils.get_access("name", mod[1]) + " v" + mod[2] + " for " + mod[3].capitalize() + " " + mod[4]
            changelog = ""
            if utils.has_changelog(mod[1]):
                changelog = utils.get_changelog(mod[1])
            modrinth = upload_modrinth(MODRINTH_TOKEN, file, modrinth_project_id, version_name, mod[2], changelog, [mod[4]], [mod[3]])
            publish_logs.append(modrinth)
            curseforge = upload_curseforge(CURSEFORGE_TOKEN, file, curseforge_project_id, version_name, changelog, [mod[4]], 1)

    return publish_logs

def upload_modrinth(
    API_TOKEN,
    file_path,
    project_id,
    version_name,
    version_number,
    changelog,
    game_versions,
    loaders
):
    url = "https://api.modrinth.com/v2/version"

    headers = {
        "Authorization": API_TOKEN
    }

    files = {
        "file": open(file_path, "rb")
    }

    data = {
        "name": version_name,
        "version_number": version_number,
        "changelog": changelog,
        "dependencies": json.dumps([]),
        "game_versions": json.dumps(game_versions),
        "version_type": "release",
        "loaders": json.dumps(loaders),
        "project_id": project_id,
        "featured": False
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        return ["Success", version_name, "modrinth uploaded successfully"]
    else:
        return ["Error", version_name, "failed to upload to modrinth: " + response.text]

def upload_curseforge(
    API_KEY,
    file_path,
    project_id,
    version_name,
    changelog,
    game_versions,
    release_type=1   # 1=release, 2=beta, 3=alpha
):
    url = f"https://api.curseforge.com/v1/mods/{project_id}/files"

    headers = {
        "x-api-key": API_KEY
    }

    files = {
        "file": open(file_path, "rb")
    }

    data = {
        "changelog": changelog,
        "changelogType": "markdown",
        "releaseType": release_type,
        "gameVersions": json.dumps(game_versions)
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        return ["Success", version_name, "modrinth uploaded successfully"]
    else:
        return ["Error", version_name, "failed to upload to modrinth: " + response.text]