App = None


directory = ""
mod_file_format = "{mod_id}[{mod_version}]-{loader}({mc_version}).jar"
display_unknown_mods = True
display_mods_without_changelog = True
show_logs = True
save_cache = True

def set_directory(value):
    global directory
    directory = value

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