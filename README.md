# Ruider

> I honestly have no idea why i named it ruider

## About

A very humble manga reader that focuses on reading pre-downloaded mangas with a simple minimal and the "pro" (lies) style keybindings for the casual manga reading experience.

**NOTE:** Ruider is a very simple manga reader that does not download any copyrighted content. The only external assets used are the app icon and font file (icon from "The Gods Lie" manga and "Jetbrains Mono" font from Jetbrains)
**NOTE:** Ruider sets some standards regarding how you store manga files. But they will be easy to follow.

## Manual

### Setup

1. Clone the repo to desired directory
2. Navigate to the directory 
3. Install dependencies using `pip install -r requirements.txt`
4. You can create symlinks or shortcuts so you can run the file from anywhere (optional).
5. Download your favourate mangas to your desired directory. The format should be:
  
  ```python
  /manga_dir
    ./manga name # Your manga name
      1.pdf    # Chapters (can be any name but include chapter number. do not include other numbers. see Naming Convention below for more info.)
      2.pdf
      ...
  ```

6. Create `config.toml` in the installation directory and pecify your manga dir in it
  ```toml
  manga_home = "/path/to/manga/directory" # Highly recommended to use absolute path
  ```

### Usage

1. Run `ruider.py` with the name of the manga you want to read:
  `python ruider.py "Shingeki no kyojin"`
  **NOTE:** Manga name is case in-sensitive.
  Thats it!

2. Navigation through pages using arrow keys.
3. You can navigate through pages using `+` and `-` keys.
4. You can navigate through chapters using numpad's `+` and `-` keys.
5. You can hide image by toggling display_image by pressing `r` key.
  This is useful when navigation as it speeds up the app.
6. You can bookmark the page and chapter by using `b` key.
  You can jump to the bookmark with `k` key.
  There can only be only one bookmark per manga.

### Notes

- Extensive configuration (window size, resizability, fullscreen etc) will be added later. Right now the app launches default fullscreen with detected monitor resolution.
- The app might be buggy or might crash. Please report issues or enhancement requests in `issues` tab of the repo.
- This is personal project dont expect the most professional looking app. It just works.    