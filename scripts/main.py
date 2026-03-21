import interface as ui
import publisher as pub
import utils

settings = utils.check_settings()

if not settings:
    utils.create_settings()


ui.build()
