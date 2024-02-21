import sys
import time
import pygame

from . import imblit, manga
from .common import Var,refresh_info
from .reader import display_page, next_chapter, next_page, previous_chapter, previous_page, refresh_page, skip_back_pages, skip_pages, toggle_showing
from .tracking import clear_previously_reading, load_bookmark, print_stats, save_bookmark, fix_missing, update_history
from .config import monitor, Config, load_config
from .features import save_page

def mousebuttondown(button):
    if button == 1:
        Var.page_index += 1
    elif button == 3:
        Var.page_index -= 1
    else:
        return # Very important
    refresh_info()
    refresh_page(Var.display_page)

def toggle_fullscreen():
    Var.context.toggle_fullscreen((monitor.width, monitor.height))
    refresh_page(Var.display_page)

def application():
    load_config()
    Var.setup()

    refresh_info()
    Var.context = imblit.IMBlit(Config.resolution, Config.resizable, Config.fullscreen, title=f"Ruider - {Var.manga_name.title()}")
    
    Var.context.scroll_speed = Config.scroll_speed
    Var.context.scroll_scale = Config.scroll_scale

    display_page()

    Var.context.onwindowresize(Var.context.center_image)
    Var.context.onmousebuttondown(mousebuttondown)

    Var.context.bind_key(pygame.K_s, save_page)
    Var.context.bind_key(pygame.K_r, toggle_showing)
    Var.context.bind_key(pygame.K_u, Var.context.toggle_gui)
    Var.context.bind_key(pygame.K_F11, toggle_fullscreen)

    Var.context.bind_key(pygame.K_PLUS, skip_pages) # Just in case
    Var.context.bind_key(pygame.K_EQUALS, skip_pages)
    Var.context.bind_key(pygame.K_MINUS, skip_back_pages)
    Var.context.bind_key(pygame.K_RIGHT, next_page)
    Var.context.bind_key(pygame.K_LEFT, previous_page)
    Var.context.bind_key(pygame.K_KP_PLUS, next_chapter)
    Var.context.bind_key(pygame.K_KP_MINUS, previous_chapter)
    Var.context.bind_key(pygame.K_b, save_bookmark)
    Var.context.bind_key(pygame.K_j, load_bookmark)

    fps = 60
    
    while not Var.context.should_close:
        Var.context.add_gui_item(f"Reading \"{Var.manga_name.title()}\"")
        if Var.chapter_page_count != 1:
            Var.context.add_gui_item(f"Chapter {Var.chapter_number}/{Var.chapters[-1].num}")
            Var.context.add_gui_item(f"Page {Var.page_index+1}/{Var.chapter_page_count}")
        else:
            Var.context.add_gui_item(f"Page {Var.chapter_number}/{len(Var.chapters)}")
        current_time = time.time()
        for message, message_time in Var.temporary_messages:
            Var.context.add_alert(message)
            if current_time - message_time > 3.5:
                Var.temporary_messages.remove((message, message_time))

        if Var.context.framecount % (fps * 1) == 0:
            update_history()

        Var.context.update(fps)

def main():
    load_config()

    list_mangas = "-l" in sys.argv or "--list" in sys.argv
    show_stats = "-s" in sys.argv or "--stats" in sys.argv
    clear = "-c" in sys.argv or "--clear" in sys.argv
    fix = "-f" in sys.argv or "--fix" in sys.argv

    if list_mangas:
        mangas = manga.get_mangas()
        # TODO: Smoothen out
        for n, mg in enumerate(mangas):
            print(f"[{n+1}]: {mg.name} - {mg.get_chapter_count()} chapter(s)")
        exit(0)
    elif show_stats:
        print_stats()
        exit(0)
    elif clear:
        clear_previously_reading()
        exit(0)
    elif fix:
        fix_missing()
        exit(0)
    application()