import io
import math
import os
import sys
import time
import toml
import imblit
import pygame
import screeninfo

from tkinter import filedialog

from common import flash, Var, write_data, get_data, refresh_info
from config import history_file, bookmark_filename, monitor, Config, load_config

import manga


def dump_history():
    history = get_data(history_file)
    if "overall" in history:
        overall = history["overall"]
    else:
        overall = 0
    if "mangas" in history:
        if Var.manga.name.lower() in history["mangas"]:
            already_spent = history["mangas"][Var.manga.name.lower()]
        else:
            already_spent = 0
    else:
        history["mangas"] = {}
        already_spent = 0
    history["mangas"][Var.manga.name.lower()] = already_spent + Var.time_spent
    history["overall"] = overall + Var.time_spent
    write_data(history, history_file)
    Var.time_spent = 0

# Refresh basic info like manga name, chapter number etc

# Display the new page to imblit
def display_page():
    fp = io.BytesIO(Var.chapters[Var.chapter_index].get_page(Var.page_index))
    surf = pygame.image.load(fp)
    # pygame.image.save(surf, "test.png")
    Var.context.display_image(surf)
    fp.close()

# Refresh the page by clamping the page and chapter index
def refresh_page(call_display: bool=True):
    if Var.page_index > Var.chapter_page_count - 1:
        Var.chapter_index += 1
        Var.page_index = 0
    elif Var.page_index < 0:
        Var.chapter_index -= 1
        Var.page_index = Var.chapters[Var.chapter_index].get_page_count() - 1
     
    if Var.chapter_index >= len(Var.chapters):
        flash("You are at the last chapter")
        Var.chapter_index = len(Var.chapters) - 1
        Var.page_index = Var.chapter_page_count - 1
    elif Var.chapter_index < 0:
        flash("You are at the first chapter")
        Var.chapter_index = 0
        Var.page_index = 0
    if call_display:
        display_page()
    refresh_info()

# Temporarily show gui message

# Retrieve bookmarks from bookmark file

# Bookmark current page
def bookmark_page():
    bookmarks = get_data(bookmark_filename)

    bookmarks[Var.manga_name.lower()] = {
        "chapter_index": Var.chapter_index,
        "page_index": Var.page_index,
        "chapter_number_readable": Var.chapter_number # Only in case user wants to manually modify bookmark, not for internal use
    }

    write_data(bookmarks, bookmark_filename)
    flash(f"Saved bookmark to ch{Var.chapter_number} pg{Var.page_index+1}")

# Change page to bookmarked page
def load_bookmark():
    bookmarks = get_data(bookmark_filename)
    
    if Var.manga_name.lower() in bookmarks:
        try: 
            Var.chapter_index = bookmarks[Var.manga_name.lower()]["chapter_index"]
            Var.page_index = bookmarks[Var.manga_name.lower()]["page_index"]
        except KeyError:
            flash("Corrupt bookmark")
        else:
            refresh_info()
            flash(f"Jumped to ch{Var.chapter_number} pg{Var.page_index+1}")
    else:
        flash(f"Bookmark not found for {Var.manga_name.lower()}")

def fix_missing():
    history = get_data(history_file)
    manga_names = list(history["mangas"].keys())
    for manga_name in manga_names:
        if not manga.manga_exists(manga_name):
            print("Deleted invalid entry:", manga_name)
            del history["mangas"][manga_name]
    write_data(history, history_file)

# Configuration

def keypress(key):
    refresh_info()

    # Configuration stuff
    if key == pygame.K_r:
        Var.display_page = not Var.display_page
        if Var.context.image_surface != None:
            Var.context.image_surface = None
        else:
            refresh_page(Var.display_page)
        return
    elif key == pygame.K_u:
        Var.context.show_gui = not Var.context.show_gui
        return
    elif key == pygame.K_F11:
        Var.context.toggle_fullscreen((monitor.width, monitor.height))
        refresh_page(Var.display_page)
        return

    # Misc features
    if key == pygame.K_s:
        f = filedialog.asksaveasfile("wb", filetypes=[('PNG Image', '.png')], defaultextension='.png')
        if f == None:
            flash("Save cancelled")
            return
        page_bytes = Var.chapters[Var.chapter_index].get_page(Var.page_index, format="PNG")
        f.write(page_bytes)
        f.close()
        flash(f"Saved to {f.name}")
        return
    
    # Page/Chapter
    if key == pygame.K_PLUS or key == pygame.K_EQUALS: # TODO: Fixme
        Var.page_index += 5
        if Var.page_index >= Var.chapter_page_count: Var.page_index = Var.chapter_page_count - 1
    elif key == pygame.K_MINUS:
        Var.page_index -= 5
        if Var.page_index < 0: Var.page_index = 0
    elif key == pygame.K_LEFT:
        Var.page_index -= 1
    elif key == pygame.K_RIGHT:
        Var.page_index += 1
    elif key == pygame.K_KP_PLUS:
        Var.chapter_index += 1
        Var.page_index = 0
    elif key == pygame.K_KP_MINUS:
        Var.chapter_index -= 1
        Var.page_index = 0
    elif key == pygame.K_b:
        bookmark_page()
        return
    elif key == pygame.K_j:
        load_bookmark()
    else:
        return
    
    refresh_info()    
    refresh_page(Var.display_page)

def windowresized():
    if Var.context.image_surface:
        Var.context.center_image()

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

    Var.context.onwindowresize(windowresized)
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
        

        if Var.context.framecount % (fps * 1) == 0: # Update history every 7 seconds
            # TODO: Find a way to see if user is actively reading or smth
            now = time.time()
            Var.time_spent += now - Var.last_checked_time
            Var.last_checked_time = now
            dump_history()

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
        history = get_data(history_file)
        overall = history["overall"] if "overall" in history else 0
        print(f"You spent exactly {math.floor(overall)} seconds using ruider to read manga.")
        print(f"\tThat is, {math.floor(overall/60)} minutes")
        print(f"\tOr {math.floor(overall/3600)} hours")
        print()
        mangas = history["mangas"] if "mangas" in history else {}
        for mg in mangas.keys():
            print(f"You spent {math.floor(mangas[mg])} seconds ({math.floor(mangas[mg]/3600)} hours {math.ceil((mangas[mg]/60)%60)} minute(s)) reading \"{mg.title()}\"")
        exit(0)
    elif clear:
        bookmarks = get_data(bookmark_filename)
        try: del bookmarks["previously_reading"]
        except KeyError: pass
        write_data(bookmarks, bookmark_filename)
        exit(0)
    elif fix:
        fix_missing()
        exit(0)
    main()