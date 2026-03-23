import interface as ui
import publisher as pub
import utils

if not utils.check_settings():
    utils.create_settings()

if not utils.check_data():
    utils.create_data()

utils.create_dirs()

ui.build()
