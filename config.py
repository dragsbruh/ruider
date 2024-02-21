import os
import toml
import pygame
import screeninfo

import manga
datadir = os.path.join(os.path.dirname(__file__), "userdata")
os.makedirs(datadir, exist_ok=True)

bookmark_file = os.path.join(datadir, "bookmarks.toml")
config_file = os.path.join(datadir, "config.toml")
history_file = os.path.join(datadir, "history.toml")

monitor = screeninfo.get_monitors()[0]

class Config:
    fullscreen: bool
    resolution: pygame.Vector2 | tuple[int, int]
    resizable: bool
    
    background: tuple[int, int, int]

    scroll_speed: int
    scroll_scale: float

    flash_background: tuple[int, int, int]
    flash_foreground: tuple[int, int, int]

    rgb: bool

    gui_background: tuple[int, int, int]
    gui_foreground: tuple[int, int, int]
    gui_shadow: tuple[int, int, int]

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = toml.load(f)
    else:
        print("Config file not found!")
        config = {
            "manga_homes": []
        }

    manga.MANGA_HOMES = config["manga_homes"]
    # Config.item = config["item"] if "item" in config else default
    Config.resolution = config["resolution"] if "resolution" in config else pygame.Vector2(monitor.width, monitor.height)
    Config.resizable = config["resizable"] if "resizable" in config else False
    Config.fullscreen = config["fullscreen"] if "fullscreen" in config else False
    Config.scroll_speed = config["scroll_speed"] if "scroll_speed" in config else 4
    Config.scroll_scale = config["scroll_scale"] if "scroll_scale" in config else 1.35
    Config.background = config["background"] if "background" in config else None
    Config.gui_background = config["gui_background"] if "gui_background" in config else None
    Config.gui_foreground = config["gui_foreground"] if "gui_foreground" in config else None
    Config.gui_shadow = config["gui_shadow"] if "gui_shadow" in config else None
    Config.flash_background = config["flash_background"] if "flash_background" in config else None
    Config.flash_foreground = config["flash_foreground"] if "flash_foreground" in config else None
    Config.rgb = config["rgb"] if "rgb" in config else True
