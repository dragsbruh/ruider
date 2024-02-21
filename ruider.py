import sys
import time
import imblit
import pygame

from common import flash, Var,refresh_info
from reader import display_page, ending, last_page, next_chapter, next_page, previous_chapter, previous_page, skip_back_pages, skip_pages, starting
from tracking import clear_previously_reading, load_bookmark, print_stats, save_bookmark, fix_missing, update_history
from config import monitor, Config, load_config
from features import save_page

import manga

def refresh_page(call_display: bool=True):
    if Var.page_index > Var.chapter_page_count - 1:
        next_chapter()
    elif Var.page_index < 0:
        previous_chapter()
        last_page()
    if Var.chapter_index >= len(Var.chapters):
        flash("You are at the last chapter")
        ending()
    elif Var.chapter_index < 0:
        flash("You are at the first chapter")
        starting()
    if call_display:
        display_page()
    refresh_info()

def keypress(key):
    # TODO: Bind the keys directly to imblit
    refresh_info()

    if key == pygame.K_r:
        Var.display_page = not Var.display_page
        if Var.context.image_surface != None:
            Var.context.image_surface = None
        else:
            refresh_page(Var.display_page)
        return
    elif key == pygame.K_u:
        Var.context.toggle_gui()
        return
    elif key == pygame.K_F11:
        Var.context.toggle_fullscreen((monitor.width, monitor.height))
        refresh_page(Var.display_page)
        return

    if key == pygame.K_s:
        save_page()
        return
    
    if key == pygame.K_PLUS or key == pygame.K_EQUALS: # TODO: Fixme
        skip_pages()
    elif key == pygame.K_MINUS:
        skip_back_pages()
    elif key == pygame.K_RIGHT:
        next_page()
    elif key == pygame.K_LEFT:
        previous_page()
    elif key == pygame.K_KP_PLUS:
        next_chapter()
    elif key == pygame.K_KP_MINUS:
        previous_chapter()
    elif key == pygame.K_b:
        save_bookmark()
        return
    elif key == pygame.K_j:
        load_bookmark()
    else:
        return
    
    refresh_info()
    refresh_page(Var.display_page)

def mousebuttondown(button):
    if button == 1:
        Var.page_index += 1
    elif button == 3:
        Var.page_index -= 1
    else:
        return # Very important
    refresh_info()
    refresh_page(Var.display_page)

def main():
    load_config()
    Var.setup()

    refresh_info()
    Var.context = imblit.IMBlit(Config.resolution, Config.resizable, Config.fullscreen, title=f"Ruider - {Var.manga_name.title()}")
    
    Var.context.scroll_speed = Config.scroll_speed
    Var.context.scroll_scale = Config.scroll_scale

    display_page()

    Var.context.onwindowresize(Var.context.center_image)
    Var.context.onkeypress(keypress)
    Var.context.onmousebuttondown(mousebuttondown)

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

if __name__ == "__main__":
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
    main()