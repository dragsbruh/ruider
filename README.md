# Ruider

<img src="assets/icon.png" alt="Icon Image" style="border-radius: 10%; width: 100px; height: 100px;">

![version](https://img.shields.io/badge/version-too%20lazy%20to%20keep%20track%20of-gray?labelColor=blue&style=for-the-badge)
![sacred manga support](https://img.shields.io/badge/sacred%20manga%20support-yes-gray?labelColor=orange&style=for-the-badge)
![free](https://img.shields.io/badge/free-absolutely-gray?labelColor=green&style=for-the-badge)

> A manga reader, nice

## About

A very humble manga reader that focuses on reading pre-downloaded mangas with a simple minimal and the "pro" (lies) style keybindings for the casual manga reading experience.

**NOTE:** Ruider is a very simple manga reader that does not download any copyrighted content. The only external asset used is the font file ("Jetbrains Mono" font from Jetbrains).

**NOTE:** Ruider sets some standards regarding how you store manga files, but they will be easy to follow.

## Manual

### Setup

1. Clone the repo to the desired directory.
2. Navigate to the directory.
3. Install dependencies using `pip install -r requirements.txt`.
4. You can create symlinks or shortcuts so you can run the file from anywhere (optional).
5. Download your favorite mangas to your desired directory. The format should be:
  
  ```python
  /manga_dir
    ./manga name # Your manga name
      1.pdf    # Chapters (can be any name but include the chapter number. Do not include other numbers. See Naming Convention below for more info.)
      2.pdf
      ...
  ```

  You can also download single-chapter image-only mangas, like from *cough cough* nmanga.net.

  ```python
  /manga_dir
  ./manga name
    1.png
    2.png
    3.png
  ```

6. Create `config.toml` in the installation directory and specify your manga dir in it:

  ```toml
  manga_home = ["/path/to/manga/directory"] # Highly recommended to use an absolute path
  ```

### Usage

1. Run `ruider.py` with the name of the manga you want to read:

  For example: `python ruider.py "shingeki no kyojin"`
  
  **NOTE:** Manga names are case-insensitive.

  That's it!

  If you set up with symlinks you can just use `ruider "shingeki no kyojin"`.

2. Navigate through pages using arrow keys.
3. You can navigate through pages using `+` and `-` keys.
4. You can navigate through chapters using numpad `+` and `-` keys.
5. You can hide the image by pressing the `r` key. Press the same key to show the image. This is useful when navigating as it speeds up the app.
6. You can bookmark the page and chapter by using the `b` key. You can jump to the bookmark with the `j` key. There can only be one bookmark per manga.
7. You can save the current page as an image using the `s` key.

### Naming convention

- "Platinum end - 01.pdf" -- works, loads as chapter 1
- "Platinum end - 01.07.pdf" -- works, loads as chapter 1.07 (in manga terms, this is chapters 1-7 or volume 1)
- "1.pdf" -- works, loads as chapter 1
- "Otter no. 11 - 1.pdf" -- doesn't work; it must only contain the chapter number. Otherwise, 11 is taken as the chapter number, and it breaks (doesn't show any error).

### Extra features

- It remembers your last opened manga, so you can just type `python ruider.py` (or `ruider` for symlink (bat script)), and it will open the manga you opened in the previous session.

### Notes

- Extensive configuration will be added later.
- The app might be buggy or might crash. Please report issues or enhancement requests in the `issues` tab of the repo.
- This is a personal project; don't expect the most professional-looking app. It just works.
- I recommend you use Hakuneko for downloading mangas.
- Only PDFs and images are supported.

## Pictures

1. Demo ![demo showing ruider - main](assets/demo_1.png)
2. Jumping to bookmark ![demo showing ruider - jump to bookmark](assets/demo_2.png)
3. Setting a bookmark ![demo showing ruider - set a bookmark](assets/demo_3.png)
4. How bookmarks are stored ![ruider info - internal bookmark representation](assets/demo_4.png)

## Commands

**NOTE:** Some of the stuff below is comedically changed but yeah

```shell
$ ruider -s
You spent exactly 16885 seconds using ruider to read manga.
        That is, 281 minutes
        Or 4 hours

You spent 511 seconds (0 hours 9 minute(s)) reading "Shingeki No Kyojin"
You spent so many seconds (many hours many minute(s)) reading "Mein Kampf"
You spent 5172 seconds (1 hours 27 minute(s)) reading "All You Need Is Kill"
You spent 3049 seconds (0 hours 51 minute(s)) reading "Kimetsu No Yaiba"
You spent 6577 seconds (1 hours 50 minute(s)) reading "Bakuman"
You spent 610 seconds (0 hours 11 minute(s)) reading "secret"
You spent 68 seconds (0 hours 2 minute(s)) reading "secret"
You spent 197 seconds (0 hours 4 minute(s)) reading "secret"
You spent 481 seconds (0 hours 9 minute(s)) reading "secret"
You spent 129 seconds (0 hours 3 minute(s)) reading "secret"
You spent 22 seconds (0 hours 1 minute(s)) reading "Platinum End"
You spent 45 seconds (0 hours 1 minute(s)) reading "Real Account"
$
```

**NOTE:** I lost most of my history when fixing some stuff, but yeah, you won't.

```shell
$ ruider -f
Deleted invalid entry: secret
Deleted invalid entry: secret
Deleted invalid entry: secret
Deleted invalid entry: secret
Deleted invalid entry: secret
$ 
```

**NOTE:** This command deletes invalid entries in the history file, like when you delete mangas.

```shell
$ ruider -l
[1]: All You Need Is Kill - 17 chapter(s)
[2]: Bakuman - 94 chapter(s)
[3]: Kimetsu no Yaiba - 22 chapter(s)
[4]: Koe no Katachi - 20 chapter(s)
[5]: Mein kampf - 1 chapter(s)
[6]: Parasyte - 4 chapter(s)
[7]: Platinum End - 8 chapter(s)
[8]: Pluto - 13 chapter(s)
[9]: Real Account - 10 chapter(s)
[10]: Shingeki no Kyojin - 148 chapter(s)
[11]: The Gods Lie - 1 chapter(s)
$ 
```

**NOTE:** This command lists all mangas from all manga homes in the order it interprets it. So normally when you type the starting characters of the manga name, it autocompletes to the first match, and you can look up the output of this command to know what you can type.
