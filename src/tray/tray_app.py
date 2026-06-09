import pystray
import subprocess

from PIL import (
    Image,
    ImageDraw
)


def create_image():

    image = Image.new(
        "RGB",
        (64, 64),
        color="white"
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (10, 10, 54, 54),
        fill="black"
    )

    return image


def search_jobs(
        icon,
        item):

    subprocess.Popen(
        ["python", "run.py"]
    )


def open_dashboard(
        icon,
        item):

    subprocess.Popen(
        [
            "streamlit",
            "run",
            "dashboard/app.py"
        ]
    )


def quit_app(
        icon,
        item):

    icon.stop()


menu = pystray.Menu(

    pystray.MenuItem(
        "Search Jobs Now",
        search_jobs
    ),

    pystray.MenuItem(
        "Open Dashboard",
        open_dashboard
    ),

    pystray.MenuItem(
        "Exit",
        quit_app
    )
)

icon = pystray.Icon(
    "JobAssistant",
    create_image(),
    "Cloud Job Assistant",
    menu
)

icon.run()
