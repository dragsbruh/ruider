import os
import sys
import toml
import time

import rui.manga as manga
import rui.imblit as imblit

from rui.config import bookmark_file

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
    context: imblit.IMBlit
    
    time_spent: float = 0
    last_checked_time: float = time.time()

    def setup():
        bookmarks = get_data(bookmark_file)
        if len(sys.argv) > 1:
            manga_name = sys.argv[-1]
            if not os.path.exists(manga.Manga.get_path(manga_name)):
                names = manga.get_names()
                for name in names:
                    if name.lower().startswith(manga_name.lower()):
                        manga_name = name
                        continue
        else:
            try:
                manga_name = bookmarks["previously_reading"].title()
            except KeyError:
                manga_name = None
        
        found = False
        for home in manga.MANGA_HOMES:
            if manga_name == None:
                continue
            elif not os.path.exists(os.path.join(home, manga_name)):
                continue
            elif os.path.exists(os.path.join(home, manga_name)) and len(sys.argv) > 1:
                bookmarks["previously_reading"] = manga_name
                write_data(bookmarks, bookmark_file)
                found = True
                break
            else:
                found = True
                break
        
        if not found:
            print(f"Usage: python ruider.py <manga-name>")
            print(f"Please provide a valid manga name to read, or run with -l to list available mangas")
            print(f"Either manga home does not exist or your manga ({manga_name}) wasnt found")
            exit(1)

        manga_name = manga_name.title()

        Var.manga = manga.Manga(manga_name)    
        Var.manga.get_chapters()
        Var.display_page = True
        Var.temporary_messages = []
        Var.page_index = 0
        Var.chapter_index = 0

def refresh_info():
    # Make sure this function runs fast, it is called a hell lot of time
    Var.manga_name = Var.manga.name
    Var.chapters = Var.manga.chapters
    if Var.chapter_index < len(Var.chapters):
        Var.chapter_path = Var.chapters[Var.chapter_index].path
        Var.chapter_page_count = Var.chapters[Var.chapter_index].get_page_count()
    Var.manga_path = Var.manga.path
    Var.chapter_number = manga.extract_number(os.path.splitext(os.path.basename(Var.chapter_path))[0])

def flash(message: str):
    Var.temporary_messages.append((message, time.time()))

def get_data(file: str):
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = toml.load(f)
    else:
        data = {}
    return data

# Write to bookmarks file
def write_data(data: dict[str, any], file: str):
    with open(file, 'w') as f:
        toml.dump(data, f)
