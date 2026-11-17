# Miku Emoji Font

Fan-made **Hatsune Miku** color emoji font: 38 emoji drawn as chibi Miku,
packaged as a `CBDT/CBLC` color bitmap font (the same format as Noto Color Emoji,
so it works on Linux, Windows and Android, and in all Chromium/Firefox builds).

Anything not in the list below keeps using your normal emoji font.

```
faces   😀 😄 😆 😉 😂 😊 😍 🥰 😅 😭 😢 😤 😱 🥺 😡 😬 😌 😎
        😏 😴 🤔 😳 😋 🤯 😜 🥳 🤗 😷 🤒 😵
hands   👍 🙏
icons   💚 🎧 🎤 🎵 ✨
```

## Install on Arch Linux

Download `ttf-miku-emoji-1.0.0-1-any.pkg.tar.zst` from the
[releases page](../../releases) and install it:

```bash
sudo pacman -U ttf-miku-emoji-1.0.0-1-any.pkg.tar.zst
fc-cache -f
```

Then restart your browser / terminal so they reload their font tables.

Uninstall:

```bash
sudo pacman -R ttf-miku-emoji && fc-cache -f
```

Temporarily disable while keeping the package:

```bash
sudo rm /etc/fonts/conf.d/75-miku-emoji.conf && fc-cache -f
```

## Build from source

```bash
git clone https://github.com/BearThomas/miku-emoji-font.git
cd miku-emoji-font
makepkg -si        # builds and installs ttf-miku-emoji
```

## How it works

The font only contains 38 glyphs, but it is **prepended to every font lookup**
(`75-miku-emoji.conf`), because Chromium/Skia resolves emoji through the generic
fontconfig sort instead of a family preference chain. Characters the font does
not contain simply fall through to the next font.

## License

Hatsune Miku is a character owned by Crypton Future Media, Inc.
This is a non-commercial fan work, distributed under the
[Piapro Character License](https://piapro.net/en_for_creators.html).

- Free to use, modify and redistribute for non-commercial purposes.
- Selling it, or bundling it into a paid product, is **not** allowed.
- Keep `LICENSE` with any redistribution.
