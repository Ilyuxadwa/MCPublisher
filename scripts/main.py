from unified_ui.logger import Logger
import utils
import publisher



logger = Logger()

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



# ---------- Start everything ----------

async def start(app):
    global registered_mods
    global changelogs
    global directory
    global saved_cache
    utils.create_dirs(directory)
    changelogs = utils.get_dict(await app.load("changelogs"))
    registered_mods = utils.get_dict(await app.load("registered_mods"))
    cache = await app.load("history")
    if cache:
        saved_cache = cache


# ---------- Essentials ----------

def get_mods():
    global loaded_mods
    global current_logs
    global saved_cache
    global logger
    logger.clear()
    loaded_mods = utils.get_mods(directory, mod_file_format, saved_cache, logger)
    return loaded_mods

def check_mod(mod_id):
    return mod_id in registered_mods

def check_changelog(mod_id, version):
    return mod_id in changelogs and version in changelogs[mod_id]


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



# ---------- Savers ----------

async def save_mods(app):
    global registered_mods
    await app.save("registered_mods", utils.save_dict(registered_mods))

async def save_changelog(app):
    global changelogs
    await app.save("changelogs", utils.save_dict(changelogs))

async def save_caches(app):
    global registered_mods
    await app.save("history", saved_cache)



# ---------- Publish ----------

def publish():
    global CURSEFORGE_TOKEN
    global MODRINTH_TOKEN
    global logger
    global loaded_mods
    global registered_mods
    global changelogs
    global save_cache
    global saved_cache
    global directory
    logger.clear()
    if not loaded_mods:
        logger.error("No mods loaded for publishing.")
    logs = publisher.publish(MODRINTH_TOKEN, CURSEFORGE_TOKEN, loaded_mods, registered_mods, changelogs, directory, saved_cache)
    for log in logs:
        if log[0]=="Success":
            logger.success(f"{log[1]} {log[2]}")
        elif log[0]=="Warn":
            logger.warn(f"{log[1]} {log[2]}")
        elif log[0]=="Error":
            logger.error(f"{log[1]} {log[2]}")
    if save_cache:
        for log in logs:
            if log[0]=="Success" and "CurseForge" in log[2]:
                saved_cache.append(log[1]+"-cf")
            if log[0]=="Success" and "Modrinth" in log[2]:
                saved_cache.append(log[1]+"-mr")
    return logger