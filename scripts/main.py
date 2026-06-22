import utils
import publisher

App = None
directory = ""
mod_file_format = "{mod_id}[{mod_version}]-{loader}({mc_version}).jar"
display_unknown_mods = True
display_mods_without_changelog = True
show_logs = True
save_cache = True

loaded_mods = []
current_logs = []

saved_cache = []
registered_mods = {}
changelogs = {}

MODRINTH_TOKEN = ""
CURSEFORGE_TOKEN = ""

def set_directory(value):
    global directory
    if directory != "MCPublisher/" + value:
        utils.remove_dirs(directory)
        directory = "MCPublisher/" + value
        utils.create_dirs("MCPublisher/" + value)

def set_mod_file_format(value):
    global mod_file_format
    mod_file_format = value

def set_display_unknown_mods(value):
    global display_unknown_mods
    display_unknown_mods = value

def set_display_mods_without_changelog(value):
    global display_mods_without_changelog
    display_mods_without_changelog = value

def set_show_logs(value):
    global show_logs
    show_logs = value

def set_save_cache(value):
    global save_cache
    save_cache = value

def set_modrinth_token(value):
    global MODRINTH_TOKEN
    MODRINTH_TOKEN = value

def set_curseforge_token(value):
    global CURSEFORGE_TOKEN
    CURSEFORGE_TOKEN = value


def get_mods():
    global loaded_mods
    global current_logs
    global saved_cache
    loaded_mods, current_logs = utils.get_mods(directory, mod_file_format, saved_cache)
    return loaded_mods, current_logs

def check_mod(mod_id):
    return mod_id in registered_mods

def check_changelog(mod_id, version):
    return mod_id in changelogs and version in changelogs[mod_id]

async def save_mods(app):
    global registered_mods
    await app.save("registered_mods", utils.save_dict(registered_mods))

async def save_changelog(app):
    global changelogs
    await app.save("changelogs", utils.save_dict(changelogs))

async def save_caches(app):
    global registered_mods
    await app.save("history", saved_cache)

async def start(app):
    global App
    global registered_mods
    global changelogs
    global directory
    global saved_cache
    App = app
    utils.create_dirs(directory)
    changelogs = utils.get_dict(await app.load("changelogs"))
    registered_mods = utils.get_dict(await app.load("registered_mods"))
    saved_cache = await app.load("history")

def publish():
    global CURSEFORGE_TOKEN
    global MODRINTH_TOKEN
    global loaded_mods
    global registered_mods
    global changelogs
    global save_cache
    global saved_cache
    global directory
    if not loaded_mods:
        return [["Error", "Mods are not loaded.", "You should load mods at first"]]
    logs = publisher.publish(MODRINTH_TOKEN, CURSEFORGE_TOKEN, loaded_mods, registered_mods, changelogs, directory)
    if save_cache:
        for log in logs:
            if log[0]=="Success":
                saved_cache.append(log[1])
    return logs
