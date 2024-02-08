import os
import fitz
import string

MANGA_HOME: str = None

class Chapter:
    num: int | float
    path: str
    parent_name: str

    def __init__(self, path: str):
        self.num = extract_number(os.path.basename(path))
        self.path = path
        self.parent_name = os.path.basename(os.path.dirname(path))

    def get_pages(self) -> bytes:
        doc = fitz.open(self.path)

        for page in doc:
            pix = page.get_pixmap()
            img_bytes = pix.pil_tobytes(format="WEBP", optimize=False, dpi=(200, 200))
            yield img_bytes
            

    def to_obj(self):
        obj =  {
            "num": self.num,
            "path": self.path,
            "parent_name": self.parent_name,
        }
        return obj
    
    def get_page_count(self):
        doc = fitz.open(self.path)
        count = len(doc)
        doc.close()
        return count
    
    def get_page(self, number: int):
        doc = fitz.open(self.path)
        if number >= len(doc):
            raise ValueError(f"Page {number} not found")
        page = doc[number].get_pixmap().pil_tobytes(format="WEBP", optimize=True, dpi=(200, 200))
        doc.close()
        return page

class Manga:
    name: str
    path: str
    chapters: list[Chapter] = None

    def __init__(self, name: str | None = None, path : str | None = None):
        if name and not path:
            self.name = name
            self.path = Manga.get_path(name)

        elif path and not name:
            self.path = path
            self.name = os.path.basename(path)
        
        elif path and name:
            self.path = path
            self.name = name
        
        else:
            raise ValueError(f"Expected either name or path or both, got name={name} path={path}")

    def get_chapters(self):
        if self.chapters != None:
            return self.chapters
        chapnums = []
        chapdict = {}
        for file in os.listdir(self.path):
            fullpath = os.path.join(self.path, file)
            if os.path.isfile(fullpath):
                num = extract_number(fullpath)
                chapdict[num] = Chapter(fullpath)
                chapnums.append(num)
        
        chapnums = sorted(chapnums)
        self.chapters = [chapdict[num] for num in chapnums]
        return self.chapters
    
    def get_path(manga_name):
        return os.path.join(MANGA_HOME, manga_name)

    def to_obj(self):
        obj = {
            "name": self.name,
            "path": self.path,
            "chapters": [chobj.to_obj() for chobj in self.chapters] if self.chapters != None else None
        }
        return obj

    def __repr__(self):
        return self.name

    def get_chapter(self, num):
        return self.chapters[num]

def extract_number(text: str):
    extracted = ""
    got_atleast_one = False
    for char in text:
        if char in string.digits + '.':
            extracted += char
            got_atleast_one = True
        elif got_atleast_one: break
    
    
    clean = ""
    period_appeared = False
    number_appeared = True
    for char in extracted:
        if char == '.':
            if period_appeared:
                break
            if not number_appeared:
                raise ValueError(f"Invalid number detected: {extracted}")
            period_appeared = True
        clean += char

    if clean.endswith("."): clean = clean.removesuffix(".")
    if "." in clean:
        return float(clean)
    return int(clean)

def get_mangas():
    return [Manga(name) for name in os.listdir(MANGA_HOME) if os.path.isdir(Manga.get_path(name))]
