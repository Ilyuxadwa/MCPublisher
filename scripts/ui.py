from unified_ui import App, Settings
import flet as ft

import info
import main

def build():
    settings = Settings()
    settings_category = settings.add_category("mcpublisher", "Publishing Settings")
    settings_category.add_directory("mods_dir", "Mods Directory", "mods", on_change=lambda value: main.set_directory(value))
    settings_category.add_text("mod_file_format", "Mod file format", "{mod_id}[{mod_version}]-{loader}({mc_version}).jar", on_change=lambda value: main.set_mod_file_format(value))
    settings_category.add_toggle("display_unknown_mods", "Display unknown mods", True, on_change=lambda value: main.set_display_unknown_mods(value))
    settings_category.add_toggle("display_mods_without_changelog", "Display mods without changelog", True, on_change=lambda value: main.set_display_mods_without_changelog(value))
    settings_category.add_toggle("show_logs", "Show logs", True, on_change=lambda value: main.set_show_logs(value))
    settings_category.add_toggle("save_cache", "Save cache", True, on_change=lambda value: main.set_save_cache(value))
    settings_category.add_text("modrinth_token", "Modrinth Token", "", on_change=lambda value: main.set_modrinth_token(value))
    settings_category.add_text("curseforge_token", "CurseForge Token", "", on_change=lambda value: main.set_curseforge_token(value))

    app = App()
    app.set_size("1/2")
    app.is_fixed_size(True)
    app.custom_settings(settings)
    app.set_version(info.VERSION)

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color="#ffffff")),
            ft.DataColumn(ft.Text("Version", color="#ffffff")),
            ft.DataColumn(ft.Text("Loader", color="#ffffff")),
            ft.DataColumn(ft.Text("Minecraft", color="#ffffff"))
        ],
        width = 800,
        height = 350,
        bgcolor="#8df9b4",
        heading_row_color="#5fe28f",
        data_row_color="#8df9b4",
        data_text_style=ft.TextStyle(color="#242424"),
        horizontal_lines=True,
        rows=[] 
    )

    app.add_element(table)
    app.add_element(ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    ft.Icons.GET_APP_ROUNDED,
                    width=40,
                    height=40,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        color="#ffffff",
                        bgcolor="#d9cb35",
                        icon_color="#ffffff",
                        overlay_color="#c1b52f"
                    ),
                    on_click=lambda e: print("Refresh clicked")),
                ft.ElevatedButton(
                    "Publish",
                    width=150,
                    height=50,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        color="#ffffff",
                        bgcolor="#4ee62c",
                        overlay_color="#4ec02f",

                    ),
                    on_click=lambda e: print("Publish clicked"))
            ]
        ))
    return app.run(info.APP_NAME)
    

