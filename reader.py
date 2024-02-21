import io
import pygame

from common import Var, refresh_info

def display_page():
    image_bytes = Var.chapters[Var.chapter_index].get_page(Var.page_index)
    fp = io.BytesIO(image_bytes)
    surf = pygame.image.load(fp)
    Var.context.display_image(surf)
    fp.close()

def next_page():
    Var.page_index += 1

def previous_page():
    Var.page_index -= 1

def next_chapter():
    Var.chapter_index += 1
    Var.page_index = 0
    refresh_info()

def previous_chapter():
    Var.chapter_index -= 1
    Var.page_index = 0
    refresh_info()

def last_page():
    Var.page_index = Var.chapter_page_count - 1

def first_page():
    Var.page_index = 0
    
def skip_pages():
    Var.page_index += 5
    # Set page index to last page if we are beyond page count
    if Var.page_index >= Var.chapter_page_count:
        last_page()
    
def skip_back_pages():
    Var.page_index -= 5
    # Set page index to first page if we are in negative range
    if Var.page_index < 0:
        first_page()

def ending():
    Var.chapter_index = len(Var.chapters) - 1
    Var.page_index = Var.chapter_page_count - 1

def starting():
    Var.chapter_index = 0
    Var.page_index = 0