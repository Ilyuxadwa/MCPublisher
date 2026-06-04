from unified_ui import App, Settings, tools
import flet as ft

import info
import main

#table = None

def update_table():
    global table
    table.rows.clear()
    mods, logs = main.available_mods()
    for mod in mods:
        display = True
        #if utils.check_mod(mod[1]):
        row_color = "#8df9b4"
        #    display = True
        #if not utils.check_changelog(mod[1]):
        #    row_color = "#f9e18d"
        #    display = main.display_mods_without_changelog

        #else:
        #    row_color = "#f98d8d"
        #    display = main.display_unknown_mods


        if display:
            table.rows.append(
                ft.DataRow(
                    color=row_color,
                    cells=[
                        ft.DataCell(ft.Text(mod[1])),
                        ft.DataCell(ft.Text(mod[2])),
                        ft.DataCell(ft.Text(mod[3])),
                        ft.DataCell(ft.Text(mod[4])),
                    ]
                )
            )

    table.update()

def main_ui(app):
    #global table

    #table = tools.Table(app, 12).cols("ID", "Version", "Loader", "Minecraft")
    #app.add_element(app.alignment("rcenter", table, expand=True))
    app.add_element(app.alignment("rcenter", 
                        ft.IconButton(ft.Icons.GET_APP_ROUNDED, width = tools.adapt_dimensions(app, "w", 6), height = tools.adapt_dimensions(app, "w", 6), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda _: print("Button clicked!")),
                        ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ROUNDED, width = tools.adapt_dimensions(app, "w", 7), height = tools.adapt_dimensions(app, "w", 7), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda _: print("Button clicked!")),
                        ft.Button("Publish", width = tools.adapt_dimensions(app, "w", 16), height = tools.adapt_dimensions(app, "w", 7.5), style=tools.main_button_style(app, 16, padding = 0), on_click=lambda _: print("Button clicked!")),
                        ft.IconButton(ft.Icons.EDIT_DOCUMENT, width = tools.adapt_dimensions(app, "w", 7), height = tools.adapt_dimensions(app, "w", 7), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda _: print("Button clicked!")),
                        ft.IconButton(ft.Icons.HISTORY_ROUNDED, width = tools.adapt_dimensions(app, "w", 6), height = tools.adapt_dimensions(app, "w", 6), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda _: print("Button clicked!")),
                    expand=True))
    
def build():
    global table
    settings = Settings()
    settings_category = settings.add_category("mcpublisher", "App Settings")
    settings_category.add_directory("mods_dir", "Mods Directory", "mods", on_change=lambda value: main.set_directory(value))
    settings_category.add_text("mod_file_format", "Mod file format", "{mod_id}[{mod_version}]-{loader}({mc_version}).jar", on_change=lambda value: main.set_mod_file_format(value))
    settings_category.add_toggle("display_unknown_mods", "Display unknown mods", True, on_change=lambda value: main.set_display_unknown_mods(value))
    settings_category.add_toggle("display_mods_without_changelog", "Display mods without changelog", True, on_change=lambda value: main.set_display_mods_without_changelog(value))
    settings_category.add_toggle("show_logs", "Show logs", True, on_change=lambda value: main.set_show_logs(value))
    settings_category.add_toggle("save_cache", "Save cache", True, on_change=lambda value: main.set_save_cache(value))
    user_category = settings.add_category("user", "User Settings")
    user_category.add_text("modrinth_token", "Modrinth Token", "", on_change=lambda value: main.set_modrinth_token(value))
    user_category.add_text("curseforge_token", "CurseForge Token", "", on_change=lambda value: main.set_curseforge_token(value))

    app = App()
    app.set_size("1/2")
    app.is_fixed_size(True)
    app.custom_settings(settings)
    app.set_version(info.VERSION)
    app.set_ui(main_ui)
    return app.run(info.APP_NAME)
    

