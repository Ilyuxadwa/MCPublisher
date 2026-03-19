from flet import *

def page(page: Page):
    page.title = "MCPublisher"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.window.width = 960
    page.window.height = 540
    page.bgcolor = "#c1ffe1"

    def get_mods(e):
        pass

    def publish(e):
        pass
    
    def open_settings(e):
        pass

    page.add(
        
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
                Button(
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
                    on_click=get_mods),
            ],
        )
    )

def build():
    run(page)