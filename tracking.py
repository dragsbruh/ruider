import manga

from common import Var, write_data, get_data, flash, refresh_info
from config import history_file, bookmark_filename

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


def bookmark_page():
    bookmarks = get_data(bookmark_filename)

    bookmarks[Var.manga_name.lower()] = {
        "chapter_index": Var.chapter_index,
        "page_index": Var.page_index,
        "chapter_number_readable": Var.chapter_number
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
