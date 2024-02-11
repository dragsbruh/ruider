import io
import os
import sys
import time
import toml
import imblit
import pygame
import screeninfo

from tkinter import filedialog

import manga

class Var:
    manga_name: str
    manga_path: str
    page_index: int
    chapter_index: int
    chapters: list[manga.Chapter]
    chapter_page_count: int
    chapter_path: str
    chapter_number: str
    display_page: bool
    temporary_messages: list[tuple[str, int]]

    manga: manga.Manga

    def setup():
        bookmarks = get_bookmarks()
        if len(sys.argv) > 1:
            manga_name = sys.argv[-1]
        else:
            try:
                manga_name = bookmarks["previously_reading"].title()
            except KeyError:
                manga_name = None
        
        if manga_name == None:
            print(f"Usage: python ruider.py <manga-name>")
            print(f"Please provide a manga name to read, or run with -l to list available mangas")
            exit(1)
        elif not os.path.exists(os.path.join(manga.MANGA_HOME, manga_name)):
            print(f"Usage: python ruider.py <manga-name>")
            print(f"File not found: Does \'{manga_name}\' exist?")
            exit(1)
        elif os.path.exists(os.path.join(manga.MANGA_HOME, manga_name)) and len(sys.argv) > 1:
            bookmarks["previously_reading"] = manga_name
            write_bookmarks(bookmarks)

        manga_name = manga_name.title()

        Var.manga = manga.Manga(manga_name)    
        Var.manga.get_chapters()
        Var.display_page = True
        Var.temporary_messages = []
        Var.page_index = 0
        Var.chapter_index = 0
        

# Refresh basic info like manga name, chapter number etc
def refresh_info():
    Var.manga_name = Var.manga.name
    Var.chapters = Var.manga.chapters
    if Var.chapter_index < len(Var.chapters):
        Var.chapter_path = Var.chapters[Var.chapter_index].path
        Var.chapter_page_count = Var.chapters[Var.chapter_index].get_page_count()
    Var.manga_path = Var.manga.path
    Var.chapter_number = manga.extract_number(os.path.splitext(os.path.basename(Var.chapter_path))[0])

# Display the new page to imblit
def display_page():
    fp = io.BytesIO(Var.chapters[Var.chapter_index].get_page(Var.page_index))
    context.display_image(pygame.image.load(fp))
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
def flash(message: str):
    Var.temporary_messages.append((message, time.time()))

# Retrieve bookmarks from bookmark file
def get_bookmarks():
    if os.path.exists(bookmark_filename):
        with open(bookmark_filename, 'r') as f:
            bookmarks = toml.load(f)
    else:
        bookmarks = {}
    return bookmarks

# Write to bookmarks file
def write_bookmarks(bookmarks: dict[str, any]):
    with open(bookmark_filename, 'w') as f:
        toml.dump(bookmarks, f)

# Bookmark current page
def bookmark_page():
    bookmarks = get_bookmarks()

    bookmarks[Var.manga_name.lower()] = {
        "chapter_index": Var.chapter_index,
        "page_index": Var.page_index,
        "chapter_number_readable": Var.chapter_number # Only in case user wants to manually modify bookmark, not for internal use
    }

    write_bookmarks(bookmarks)
    flash(f"Saved bookmark to ch{Var.chapter_number} pg{Var.page_index+1}")

# Change page to bookmarked page
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
            flash(f"Jumped to ch{Var.chapter_number} pg{Var.page_index+1}")
    else:
        flash(f"Bookmark not found for {Var.manga_name.lower()}")


# Constants
bookmark_filename = os.path.join(os.path.dirname(__file__), "bookmarks.toml")
config_file = os.path.join(os.path.dirname(__file__), "config.toml")
monitor = screeninfo.get_monitors()[0]

# Configuration
resolution = pygame.Vector2(monitor.width, monitor.height)
resizable = False
fullscreen = False

with open(config_file, 'r') as f:
    config = toml.load(f)

manga.MANGA_HOME = config["manga_home"]
if "resolution" in config: resolution.x, resolution.y = config["resolution"]
if "resizable" in config: resizable = config["resizable"]
if "fullscreen" in config: fullscreen = config["fullscreen"]

# CLI handling
list_mangas = "-l" in sys.argv or "--list" in sys.argv

if list_mangas:
    mangas = manga.get_mangas()
    # TODO: Smoothen out
    for n, mg in enumerate(mangas):
        print(f"[{n+1}]: {mg.name} - {mg.get_chapter_count()} chapter(s)")
    exit(0)

# Main
Var.setup()
refresh_info()

context = imblit.IMBlit(resolution, resizable, fullscreen, title=f"Ruider - {Var.manga_name.title()}")

@context.onkeypress
def keypress(key):
    refresh_info()

    # Configuration stuff
    if key == pygame.K_r:
        Var.display_page = not Var.display_page
        if context.image_surface != None:
            context.image_surface = None
        else:
            refresh_page(Var.display_page)
        return
    elif key == pygame.K_u:
        context.show_gui = not context.show_gui
        return
    elif key == pygame.K_F11:
        context.toggle_fullscreen((monitor.width, monitor.height))
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
    elif key == pygame.K_j:
        load_bookmark()
    
    refresh_info()    
    refresh_page(Var.display_page)

@context.onwindowresize
def windowresized():
    if context.image_surface:
        context.center_image()

display_page()

while not context.should_close:
    context.add_gui_item(f"Reading \"{Var.manga_name.title()}\"")
    context.add_gui_item(f"Chapter {Var.chapter_number}/{Var.chapters[-1].num}")
    context.add_gui_item(f"Page {Var.page_index+1}/{Var.chapter_page_count}")
    current_time = time.time()
    for message, message_time in Var.temporary_messages:
        context.add_gui_item(message)
        if current_time - message_time > 3.5:
            Var.temporary_messages.remove((message, message_time))
    context.update(60)