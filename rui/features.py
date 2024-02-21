from tkinter import filedialog

from .common import Var, flash

def save_page():
    f = filedialog.asksaveasfile("wb", filetypes=[('PNG Image', '.png')], defaultextension='.png')
    if f == None:
        flash("Save cancelled")
        return
    page_bytes = Var.chapters[Var.chapter_index].get_page(Var.page_index, format="PNG")
    f.write(page_bytes)
    f.close()
    flash(f"Saved to {f.name}")