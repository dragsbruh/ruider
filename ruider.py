import io
import os
import sys
import time

import toml
import imblit
import pygame

from manga import MANGA_HOME, Chapter, Manga, extract_number

im = imblit.IMBlit((1920, 1080), True, True)
bookmark_filename = os.path.join(os.path.dirname(__file__), "bookmarks.toml")

class Var:
    manga_name: str
    manga_path: str
    page_index: int
    chapter_index: int
    chapters: list[Chapter]
    chapter_page_count: int
    chapter_path: str
    chapter_number: str
    display_page: bool
    temporary_messages: list[tuple[str, int]]

    mg: Manga

    def setup():
        bookmarks = get_bookmarks()
        if len(sys.argv) > 1:
            manga_name = sys.argv[-1]
        else:
            try:
                manga_name = bookmarks["previously_reading"]
            except KeyError:
                manga_name = None
        
        if manga_name == None:
            print(f"Usage: python ruider.py <manga-name>")
            print(f"Please provide a manga name to read, or run with -l to list available mangas")
            exit(1)
        elif not os.path.exists(os.path.join(MANGA_HOME, manga_name)):
            print(f"Usage: python ruider.py <manga-name>")
            print(f"File not found: Does \'{manga_name}\' exist?")
            exit(1)
        elif os.path.exists(os.path.join(MANGA_HOME, manga_name)) and len(sys.argv) > 1:
            bookmarks["previously_reading"] = manga_name
            write_bookmarks(bookmarks)

        Var.mg = Manga(manga_name)    
        Var.mg.get_chapters()
        Var.display_page = True
        Var.temporary_messages = []

def refresh_info():
    Var.manga_name = Var.mg.name
    Var.chapters = Var.mg.chapters
    if Var.chapter_index < len(Var.chapters):
        Var.chapter_path = Var.chapters[Var.chapter_index].path
        Var.chapter_page_count = Var.chapters[Var.chapter_index].get_page_count()
    Var.manga_path = Var.mg.path
    Var.chapter_number = extract_number(os.path.splitext(os.path.basename(Var.chapter_path))[0])

def display_page():
    fp = io.BytesIO(Var.chapters[Var.chapter_index].get_page(Var.page_index))
    im.display_image(pygame.image.load(fp))
    fp.close()

def refresh_page(call_display: bool=True):
    if Var.page_index > Var.chapter_page_count - 1:
        Var.chapter_index += 1
        Var.page_index = 0
    elif Var.page_index < 0:
        Var.chapter_index -= 1
        Var.page_index = Var.chapters[Var.chapter_index].get_page_count() - 1
     
    if Var.chapter_index >= len(Var.chapters):
        flash("This is the last chapter")
        Var.chapter_index = len(Var.chapters) - 1
        Var.page_index = Var.chapter_page_count - 1
    elif Var.chapter_index < 0:
        flash("You are at first chapter")
        Var.chapter_index = 0
        Var.page_index = 0
    if call_display:
        display_page()
    refresh_info()

def flash(message: str):
    Var.temporary_messages.append((message, time.time()))

def get_bookmarks():
    if os.path.exists(bookmark_filename):
        with open(bookmark_filename, 'r') as f:
            bookmarks = toml.load(f)
    else:
        bookmarks = {}
    return bookmarks

def write_bookmarks(bookmarks: dict[str, any]):
    with open(bookmark_filename, 'w') as f:
        toml.dump(bookmarks, f)

def bookmark_page():
    bookmarks = get_bookmarks()

    bookmarks[Var.manga_name.lower()] = {
        "chapter_index": Var.chapter_index,
        "page_index": Var.page_index,
        "chapter_number_readable": Var.chapter_number # Only in case user wants to manually modify bookmark, not for internal use
    }

    write_bookmarks(bookmarks)
    flash(f"Bookmarked current as {Var.manga_name.lower()}")

def load_bookmark():
    bookmarks = get_bookmarks()
    
    if Var.manga_name.lower() in bookmarks:
        try: 
            Var.chapter_index = bookmarks[Var.manga_name.lower()]["chapter_index"]
            Var.page_index = bookmarks[Var.manga_name.lower()]["page_index"]
        except KeyError:
            flash("Corrupt bookmark")
        else:
            refresh_info()
            flash(f"Jumped to {Var.chapter_number}-{Var.page_index+1}")
    else:
        flash(f"Bookmark not found for {Var.manga_name.lower()}")

@im.onkeypress
def keypress(key):
    refresh_info()

    # Configuration stuff
    if key == pygame.K_r:
        Var.display_page = not Var.display_page
        if im.im_surf != None:
            im.im_surf = None
        else:
            refresh_page(Var.display_page)
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
    elif key == pygame.K_j:
        load_bookmark()
    
    refresh_info()    
    refresh_page(Var.display_page)

@im.onwindowresize
def windowresized():
    if im.im_surf:
        im.center_image()

Var.setup()
Var.page_index = 0
Var.chapter_index = 0
refresh_info()
display_page()

while not im.should_close:
    im.add_gui_item(f"Reading {Var.manga_name.lower()}")
    im.add_gui_item(f"Chapter {Var.chapter_number}")
    im.add_gui_item(f"Page {Var.page_index+1}/{Var.chapter_page_count}")
    curtime = time.time()
    for message, message_time in Var.temporary_messages:
        im.add_gui_item(message)
        if curtime - message_time > 3.5:
            Var.temporary_messages.remove((message, message_time))
    im.update(60)