from unified_ui import App, Settings, tools
import flet as ft

import info
import main

files_table = None
mods_table = None
changelog_table = None

def get_mods(app):
    global files_table
    files_table.clear()
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
            files_table.add_row(mod[1], mod[2], mod[3], mod[4], color=row_color)
    
    files_table.update()

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



def fill_mods_table():
    global mods_table
    mods_table.clear()
    registered_mods = main.registered_mods
    for mod_id in registered_mods:
        mods_table.add_row(mod_id, registered_mods[mod_id]["name"], registered_mods[mod_id]["curseforge_id"], registered_mods[mod_id]["modrinth_id"])

def open_registering(app):
    mod_id = tools.entry(app, 12, label="Mod ID", hint_text="Enter mod ID")
    name = tools.entry(app, 12, label="Mod Name", hint_text="Enter mod name")
    cf_id = tools.entry(app, 12, label="CurseForge ID", hint_text="Enter CurseForge ID")
    mr_id = tools.entry(app, 12, label="Modrinth ID", hint_text="Enter Modrinth ID")
    message = ft.Text("", style=tools.primary_text_style(app, 12))
    dialog = tools.dialog(app, 12,
        title=ft.Text("Add Mod"),
        content=app.alignment("ccenter", 
            mod_id, name, cf_id, mr_id, message
        ),
        actions=[
            ft.Button("Close", style=tools.cancel_button_style(app, 12), on_click=lambda e: app.page.pop_dialog()),
            ft.Button("Add", style=tools.ok_button_style(app, 12), on_click=lambda e: save_mod(app, mod_id, name, cf_id, mr_id, message))
        ]
    )
    app.page.show_dialog(dialog)

def save_mod(app, mod_id, name, cf_id, mr_id, msg):
    global mods_table
    if not mod_id.value or not name.value:
        msg.value = "Mod ID and names are required!"
        return
    
    elif not cf_id.value and not mr_id.value:
        msg.value = "At least one of CurseForge ID or Modrinth ID is required!"
        return
    elif mod_id.value in main.registered_mods:
        msg.value = "Mod ID already exists!"
        return
    else:
        main.registered_mods[mod_id.value] = {"name": name.value, "curseforge_id": cf_id.value, "modrinth_id": mr_id.value}
        fill_mods_table()
        mods_table.update()
        app.page.run_task(main.save_mods, app)
        app.page.pop_dialog()

def edit_mod(app):
    name = tools.entry(app, 12, label="Mod Name", hint_text="Edit mod name")
    cf_id = tools.entry(app, 12, label="CurseForge ID", hint_text="Edit CurseForge ID")
    mr_id = tools.entry(app, 12, label="Modrinth ID", hint_text="Edit Modrinth ID")
    message = ft.Text("", style=tools.primary_text_style(app, 12))
    mod_id = tools.dropdown(app, 12, label="Mod ID", options=[ft.DropdownOption(mod_id, mod_id) for mod_id in main.registered_mods], on_select=lambda : fill_mod_info(mod_id, name, cf_id, mr_id))
    dialog = tools.dialog(app, 12,
        title=ft.Text("Edit information"),
        content=app.alignment("ccenter", 
            mod_id, name, cf_id, mr_id, message
        ),
        actions=[
            ft.Button("Close", style=tools.cancel_button_style(app, 12), on_click=lambda e: app.page.pop_dialog()),
            ft.Button("Save", style=tools.ok_button_style(app, 12), on_click=lambda e: save_editing_mod(app, mod_id, name, cf_id, mr_id, message))
        ]
    )
    app.page.show_dialog(dialog)

def save_editing_mod(app, mod_id, name, cf_id, mr_id, msg):
    global mods_table
    if not mod_id.value or not name.value:
        msg.value = "Mod ID and names are required!"
        return
    
    elif not cf_id.value and not mr_id.value:
        msg.value = "At least one of CurseForge ID or Modrinth ID is required!"
        return
    
    else:
        main.registered_mods[mod_id.value] = {"name": name.value, "curseforge_id": cf_id.value, "modrinth_id": mr_id.value}
        fill_mods_table()
        mods_table.update()
        app.page.run_task(main.save_mods, app)
        app.page.pop_dialog()

def fill_mod_info(mod_id, name, cf_id, mr_id):
    mod_info = main.registered_mods.get(mod_id.value)
    if mod_info:
        name.value = mod_info["name"]
        cf_id.value = mod_info["curseforge_id"]
        mr_id.value = mod_info["modrinth_id"]

def open_deleting_mod(app):
    mod_id = tools.dropdown(app, 12, label="Mod ID", options=[ft.DropdownOption(mod_id, mod_id) for mod_id in main.registered_mods])
    message = ft.Text("", style=tools.primary_text_style(app, 12))
    dialog = tools.dialog(app, 12,
        title=ft.Text("Edit information"),
        content=app.alignment("ccenter", 
            mod_id, message
        ),
        actions=[
            ft.Button("Cancel", style=tools.ok_button_style(app, 12), on_click=lambda e: app.page.pop_dialog()),
            ft.Button("Delete", style=tools.cancel_button_style(app, 12), on_click=lambda e: delete_mod(app, mod_id.value, message))
        ]
    )
    app.page.show_dialog(dialog)

def delete_mod(app, mod_id, message):
    global mods_table
    if mod_id in main.registered_mods:
        del main.registered_mods[mod_id]
        fill_mods_table()
        mods_table.update()
        app.page.pop_dialog()
    elif mod_id == "":
        message.value = "Please select a mod ID!"
    else:
        message.value = "Mod with selected ID not found!"

def fill_changelogs_table():
    global changelog_table
    changelog_table.clear()
    changelogs = main.changelogs
    for mod in changelogs:
        for version in changelogs[mod]:
            changelog_table.add_row(mod, version, changelogs[mod][version]["name"])

def main_ui(app):
    global files_table

    files_table = tools.Table(app, 24).cols("ID", "Version", "Loader", "Minecraft").heading_height(tools.adapt_dimensions(app, "h", 12)).row_height(tools.adapt_dimensions(app, "h", 8))
    files_table.size(w=88, h=54)

    app.add_element(app.alignment("rcenter", files_table.build(), height = tools.adapt_dimensions(app, "h", 62), expand=True))
    app.add_element(app.alignment("rcenter", 
                        ft.IconButton(ft.Icons.GET_APP_ROUNDED, width = tools.adapt_dimensions(app, "w", 6), height = tools.adapt_dimensions(app, "w", 6), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda : get_mods(app)),
                        ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ROUNDED, width = tools.adapt_dimensions(app, "w", 7), height = tools.adapt_dimensions(app, "w", 7), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda: app.navigate("mods_register_page")),
                        ft.Button("Publish", width = tools.adapt_dimensions(app, "w", 16), height = tools.adapt_dimensions(app, "w", 7.5), style=tools.main_button_style(app, 16, padding = 0), on_click=lambda _: print("Button clicked!")),
                        ft.IconButton(ft.Icons.EDIT_DOCUMENT, width = tools.adapt_dimensions(app, "w", 7), height = tools.adapt_dimensions(app, "w", 7), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda: app.navigate("changelogs_page")),
                        ft.IconButton(ft.Icons.HISTORY_ROUNDED, width = tools.adapt_dimensions(app, "w", 6), height = tools.adapt_dimensions(app, "w", 6), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda _: print("Button clicked!")),
                    expand=True))
    
def mod_register_ui(app):
    global mods_table

    mods_table = tools.Table(app, 24).cols("Mod ID", "Name", "CurseForge ID", "Modrinth ID").heading_height(tools.adapt_dimensions(app, "h", 12)).row_height(tools.adapt_dimensions(app, "h", 8))
    mods_table.size(w=88, h=48)

    fill_mods_table()

    app.add_element(app.alignment("rend", ft.IconButton(ft.Icons.ARROW_BACK_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.main_button_style(app, 8), padding=5, on_click=lambda: app.navigate("main_page"))))
    app.add_element(app.alignment("rcenter", mods_table.build(), height = tools.adapt_dimensions(app, "h", 56), expand=True))
    app.add_element(app.alignment("rcenter", 
                        ft.IconButton(ft.Icons.ADD_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.ok_button_style(app, 8, padding = 5), on_click=lambda: open_registering(app)),
                        ft.IconButton(ft.Icons.EDIT_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.additional_button_style(app, 8, padding = 5), on_click=lambda: edit_mod(app)),
                        ft.IconButton(ft.Icons.DELETE_FOREVER_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.cancel_button_style(app, 8, padding = 5), on_click=lambda: open_deleting_mod(app)),
                    expand=True))
    
def changelogs_ui(app):
    global changelog_table

    changelog_table = tools.Table(app, 24).cols("Mod ID", "Version", "Update Name").heading_height(tools.adapt_dimensions(app, "h", 12)).row_height(tools.adapt_dimensions(app, "h", 8))
    changelog_table.size(w=88, h=48)

    fill_changelogs_table()

    app.add_element(app.alignment("rend", ft.IconButton(ft.Icons.ARROW_BACK_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.main_button_style(app, 8), padding=5, on_click=lambda: app.navigate("main_page"))))
    app.add_element(app.alignment("rcenter", changelog_table.build(), height = tools.adapt_dimensions(app, "h", 56), expand=True))
    app.add_element(app.alignment("rcenter", 
                        ft.IconButton(ft.Icons.ADD_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.ok_button_style(app, 8, padding = 5), on_click=lambda: app.navigate("changelog_adder_page")),
                        ft.IconButton(ft.Icons.EDIT_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.additional_button_style(app, 8, padding = 5), on_click=edit_mod),
                        ft.IconButton(ft.Icons.DELETE_FOREVER_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.cancel_button_style(app, 8, padding = 5), on_click=delete_mod),
                    expand=True))
    
def changelog_adder_ui(app):
    def edit_info():
        final_changes = ""
        for change in changes.value.split("\n"):
            final_changes += f"- {change}\n"
        if mod_id.value in main.registered_mods:
            preview.value = f"# ***{name.value}***\n###### v{version.value} for {main.registered_mods[mod_id.value]['name']}\n---\n ### What's New:\n {final_changes}" 
    
    def register_changelog():
        final_changes = ""
        for change in changes.value.split("\n"):
            final_changes += f"- {change}\n"

        changelog = f"# ***{name.value}***\n###### v{version.value} for {main.registered_mods[mod_id.value]['name']}\n---\n ### What's New:\n {final_changes}" 
        if not mod_id.value in main.changelogs:
            main.changelogs[mod_id.value]={}
        if not version.value in main.changelogs[mod_id.value]:
            main.changelogs[mod_id.value][version.value] = {"name": name.value, "changes": changelog}
            app.page.run_task(main.save_changelog, app)
            app.navigate("changelogs_page")

    mod_id = tools.dropdown(app, 12, label="Mod ID", options=[ft.DropdownOption(mod_id, mod_id) for mod_id in main.registered_mods], width = tools.adapt_dimensions(app, "w", 48), height = tools.adapt_dimensions(app, "h", 10), on_select = edit_info)
    version = tools.entry(app, 12, label="Mod version", hint_text="Version", width = tools.adapt_dimensions(app, "w", 48), height = tools.adapt_dimensions(app, "h", 10), fit_parent_size=True, on_change = edit_info)
    name = tools.entry(app, 12, label="Update name", hint_text="Update name", width = tools.adapt_dimensions(app, "w", 48), height = tools.adapt_dimensions(app, "h", 10), fit_parent_size=True, on_change = edit_info)
    changes = tools.entry(app, 12, label="Changes list", hint_text="State all changes", multiline=True, width = tools.adapt_dimensions(app, "w", 48), height = tools.adapt_dimensions(app, "h", 30), fit_parent_size=True, collapsed=True, content_padding=15, on_change = edit_info)
    preview = ft.Markdown(
            value ="",
            md_style_sheet=ft.MarkdownStyleSheet(
                p_text_style=ft.TextStyle(color=app.theme.primary),
                h1_text_style=ft.TextStyle(color=app.theme.primary),
                h3_text_style=ft.TextStyle(color=app.theme.primary),
                h6_text_style=ft.TextStyle(color=app.theme.primary),
                strong_text_style=ft.TextStyle(color=app.theme.primary)
            ),
            width = tools.adapt_dimensions(app, "w", 40),
            height = tools.adapt_dimensions(app, "h", 42)
        )
   
    app.add_element(app.alignment("rend", ft.IconButton(ft.Icons.ARROW_BACK_ROUNDED, width = tools.adapt_dimensions(app, "h", 10), height = tools.adapt_dimensions(app, "h", 10), style=tools.main_button_style(app, 8), padding=5, on_click=lambda: app.navigate("changelogs_page"))))
    app.add_element(app.alignment("rspace_between",
                        app.alignment("cspace_between", 
                            mod_id, version, name, changes, width = tools.adapt_dimensions(app, "w", 48), height = tools.adapt_dimensions(app, "h", 60)),
                        app.alignment("cspace_evenly", 
                            ft.Container(bgcolor = app.theme.entry, padding = tools.adapt_dimensions(app, "w", 4), content=preview, width = tools.adapt_dimensions(app, "w", 48), height = tools.adapt_dimensions(app, "h", 50)),
                            app.alignment("rend", 
                                ft.Button("Close", style=tools.cancel_button_style(app, 12), width = tools.adapt_dimensions(app, "w", 10), height = tools.adapt_dimensions(app, "h", 8), on_click=lambda: app.navigate("changelogs_page")),
                                ft.Button("Save", style=tools.ok_button_style(app, 12), width = tools.adapt_dimensions(app, "w", 10), height = tools.adapt_dimensions(app, "h", 8), on_click=register_changelog),
                            expand = True),
                        width = tools.adapt_dimensions(app, "w", 48)), width = tools.adapt_dimensions(app, "w", 100), height = tools.adapt_dimensions(app, "h", 60)))
    
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
    app.add_page("main_page", main_ui)
    app.add_page("mods_register_page", mod_register_ui)
    app.add_page("changelogs_page", changelogs_ui)
    app.add_page("changelog_adder_page", changelog_adder_ui)
    app.set_async_next(main.start)
    app.run(info.APP_NAME)