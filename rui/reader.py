import io
import pygame

from .common import Var, refresh_info, flash

def display_page():
    image_bytes = Var.chapters[Var.chapter_index].get_page(Var.page_index)
    fp = io.BytesIO(image_bytes)
    surf = pygame.image.load(fp)
    Var.context.display_image(surf)
    fp.close()

def next_page():
    Var.page_index += 1
    refresh_info()
    refresh_page(Var.display_page)

def previous_page():
    Var.page_index -= 1
    refresh_info()
    refresh_page(Var.display_page)

def next_chapter():
    Var.chapter_index += 1
    Var.page_index = 0
    refresh_info()
    refresh_page(Var.display_page)

def previous_chapter():
    Var.chapter_index -= 1
    Var.page_index = 0
    refresh_info()
    refresh_page(Var.display_page)

def last_page():
    Var.page_index = Var.chapter_page_count - 1
    refresh_info()
    refresh_page(Var.display_page)

def first_page():
    Var.page_index = 0
    refresh_info()
    refresh_page(Var.display_page)
    
def skip_pages():
    Var.page_index += 5
    # Set page index to last page if we are beyond page count
    if Var.page_index >= Var.chapter_page_count:
        last_page()
    refresh_info()
    refresh_page(Var.display_page)
    
def skip_back_pages():
    Var.page_index -= 5
    # Set page index to first page if we are in negative range
    if Var.page_index < 0:
        first_page()
    refresh_info()
    refresh_page(Var.display_page)

def ending():
    Var.chapter_index = len(Var.chapters) - 1
    Var.page_index = Var.chapter_page_count - 1
    refresh_info()
    refresh_page(Var.display_page)

def starting():
    Var.chapter_index = 0
    Var.page_index = 0
    refresh_info()
    refresh_page(Var.display_page)

def toggle_showing():
    Var.display_page = not Var.display_page
    if Var.context.image_surface != None:
        Var.context.image_surface = None
    else:
        refresh_page(Var.display_page)

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
