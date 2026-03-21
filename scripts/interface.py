from flet import *
import utils

def page(page: Page):
    page.title = "MCPublisher"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.window.width = 960
    page.window.height = 540
    page.bgcolor = "#c1ffe1"

    def get_mods(e):
        mods, logs = utils.get_mods()
        table.rows.clear()

        for mod in mods:
            print (mod)
            table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(mod[1])),
                        DataCell(Text(mod[2])),
                        DataCell(Text(mod[3])),
                        DataCell(Text(mod[4])),
                    ]
                )
            )

        table.update()

        
        if logs and utils.get_settings("show_logs"):
            dialog = AlertDialog(
                title=Text("Logs"),
                content=Column(
                    [Text(log[0]+": " + log[1] + " -> " + log[2]) for log in logs],
                    scroll=ScrollMode.AUTO,
                    height=200,
                ),
                actions=[
                    Button("Close", on_click=lambda e: page.pop_dialog())
                ]
            )
            page.show_dialog(dialog)

    def publish(e):
        pass
    
    def open_settings(e):

        directory = TextField(label="Mods directory", value=utils.get_settings("mods_path"))
        unknown_mods = Checkbox(label="Display unknown mods", value=utils.get_settings("diplay_unknown_mods"))
        mods_without_changelog = Checkbox(label="Mods without changelog", value=utils.get_settings("display_mods_without_changelog"))
        show_logs = Checkbox(label="Show logs", value=utils.get_settings("show_logs"))
        save_cache = Checkbox(label="Save cache", value=utils.get_settings("save_cache"))
        dialog = AlertDialog(
            title=Text("Settings"),
            content=Column([
                directory,
                unknown_mods,
                mods_without_changelog,
                show_logs,
                save_cache
            ]),
            actions=[
                Button("Save", on_click=lambda e: save_settings(directory, unknown_mods, mods_without_changelog, show_logs, save_cache)),
                Button("Cancel", on_click=lambda e: page.pop_dialog())
            ]
        )
        page.show_dialog(dialog)

    def save_settings(directory, unknown_mods, mods_without_changelog, show_logs, save_cache):
        settings = {
            "mods_path": directory.value,
            "diplay_unknown_mods": unknown_mods.value,
            "display_mods_without_changelog": mods_without_changelog.value,
            "show_logs": show_logs.value,
            "save_cache": save_cache.value
        }
        utils.save_settings(settings)
        page.pop_dialog()

    table = DataTable(
        columns=[
            DataColumn(Text("ID", color="#ffffff")),
            DataColumn(Text("Version", color="#ffffff")),
            DataColumn(Text("Loader", color="#ffffff")),
            DataColumn(Text("Minecraft", color="#ffffff"))
        ],
        width = 800,
        height = 350,
        bgcolor="#8df9b4",
        heading_row_color="#5fe28f",
        data_row_color="#8df9b4",
        data_text_style=TextStyle(color="#FFFFFF"),
        horizontal_lines=True,
        rows=[] 
    )

    page.add(
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[table]
        ),
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                IconButton(
                    Icons.GET_APP_ROUNDED,
                    width=40,
                    height=40,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=10),
                        color="#ffffff",
                        bgcolor="#d9cb35",
                        icon_color="#ffffff",
                        overlay_color="#c1b52f"
                    ),
                    on_click=get_mods),
                ElevatedButton(
                    "Publish",
                    
                    width=150,
                    height=50,
                    style=ButtonStyle(
                        text_style=TextStyle(size=18, weight=FontWeight.BOLD),
                        shape=RoundedRectangleBorder(radius=10),
                        color="#ffffff",
                        bgcolor="#4ee62c",
                        overlay_color="#4ec02f",

                    ),
                    on_click=publish),
                IconButton(
                    Icons.SETTINGS_ROUNDED,
                    width=40,
                    height=40,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=10),
                        color="#ffffff",
                        bgcolor="#a1a1a1",
                        icon_color="#ffffff",
                        overlay_color="#757575"
                    ),
                    on_click=open_settings),
            ],
        )
    )

def build():
    run(page)