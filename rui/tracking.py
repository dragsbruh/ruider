import rui.manga as manga
import math
import time

from .common import Var, write_data, get_data, flash, refresh_info
from .config import history_file, bookmark_file

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

def save_bookmark():
    bookmarks = get_data(bookmark_file)

    bookmarks[Var.manga_name.lower()] = {
        "chapter_index": Var.chapter_index,
        "page_index": Var.page_index,
        "chapter_number_readable": Var.chapter_number
    }

    write_data(bookmarks, bookmark_file)
    flash(f"Saved bookmark to ch{Var.chapter_number} pg{Var.page_index+1}")

# Change page to bookmarked page
def load_bookmark():
    bookmarks = get_data(bookmark_file)
    
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

def print_stats():
    history = get_data(history_file)
    overall = history["overall"] if "overall" in history else 0
    print(f"You spent exactly {math.floor(overall)} seconds using ruider to read manga.")
    print(f"\tThat is, {math.floor(overall/60)} minutes")
    print(f"\tOr {math.floor(overall/3600)} hours")
    print()
    mangas = history["mangas"] if "mangas" in history else {}
    for mg in mangas.keys():
        print(f"You spent {math.floor(mangas[mg])} seconds ({math.floor(mangas[mg]/3600)} hours {math.ceil((mangas[mg]/60)%60)} minute(s)) reading \"{mg.title()}\"")

def clear_previously_reading():
    bookmarks = get_data(bookmark_file)
    try: 
        del bookmarks["previously_reading"]
    except KeyError:
        pass
    else:
        write_data(bookmarks, bookmark_file)

def get_previously_reading():
    bookmarks = get_data(bookmark_file)
    if not "previously_reading" in bookmark_file:
        return None
    return bookmarks["previously_reading"]

def update_history():
    # TODO: Find a way to see if user is actively reading or smth
    now = time.time()
    Var.time_spent += now - Var.last_checked_time
    Var.last_checked_time = now
    dump_history()