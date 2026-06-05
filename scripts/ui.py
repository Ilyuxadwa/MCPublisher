from unified_ui import App, Settings, tools
import flet as ft

import info
import main

table = None

def get_mods(app):
    global table
    table.clear()
    print("Getting mods...")
    mods, logs = main.get_mods()
    for mod in mods:
        if main.check_mod(mod[1]):
            row_color = "#8df9b4"
            display = True
            checked = True

        else:
            row_color = "#f98d8d"
            display = main.display_unknown_mods
            checked = False

        if not main.check_changelog(mod[1], mod[2]) and checked:
            row_color = "#f9e18d"
            display = main.display_mods_without_changelog

        if display:
            table.add_row(mod[1], mod[2], mod[3], mod[4], color=row_color)
    
    table.update()

    if logs and main.show_logs:
        dialog = tools.dialog(app, 12,
            title=ft.Text("Logs"),
            content=ft.Column( 
                [ft.Text(f"{log[0]}: {log[1]} -> {log[2]}", style = tools.primary_text_style(app, 12)) for log in logs],
            scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.Button("Close", style=tools.cancel_button_style(app, 12), on_click=lambda e: app.page.pop_dialog())
            ]
        )
        app.page.show_dialog(dialog)

def main_ui(app):
    global table

    table = tools.Table(app, 24).cols("ID", "Version", "Loader", "Minecraft").heading_height(tools.adapt_dimensions(app, "h", 12)).row_height(tools.adapt_dimensions(app, "h", 8))
    table.size(w=88, h=54)

    app.add_element(app.alignment("rcenter", table.build(), height = tools.adapt_dimensions(app, "h", 62), expand=True))
    app.add_element(app.alignment("rcenter", 
                        ft.IconButton(ft.Icons.GET_APP_ROUNDED, width = tools.adapt_dimensions(app, "w", 6), height = tools.adapt_dimensions(app, "w", 6), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda : get_mods(app)),
                        ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ROUNDED, width = tools.adapt_dimensions(app, "w", 7), height = tools.adapt_dimensions(app, "w", 7), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda _: print("Button clicked!")),
                        ft.Button("Publish", width = tools.adapt_dimensions(app, "w", 16), height = tools.adapt_dimensions(app, "w", 7.5), style=tools.main_button_style(app, 16, padding = 0), on_click=lambda _: print("Button clicked!")),
                        ft.IconButton(ft.Icons.EDIT_DOCUMENT, width = tools.adapt_dimensions(app, "w", 7), height = tools.adapt_dimensions(app, "w", 7), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda _: print("Button clicked!")),
                        ft.IconButton(ft.Icons.HISTORY_ROUNDED, width = tools.adapt_dimensions(app, "w", 6), height = tools.adapt_dimensions(app, "w", 6), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda _: print("Button clicked!")),
                    expand=True))
    
def build():
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
    

