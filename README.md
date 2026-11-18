# Miku Emoji Font

Fan-made **Hatsune Miku** color emoji font: 120 emoji drawn as chibi Miku (59 codepoints + 3 ZWJ sequences),
packaged as a `CBDT/CBLC` color bitmap font (the same format as Noto Color Emoji,
so it works on Linux, Windows and Android, and in all Chromium/Firefox builds).

Anything not in the list below keeps using your normal emoji font.

```
😂 😭 😊 😍 🥰 😡 😴 🤔 😅 👍 🙏 💚 🎧 🎤
🎵 ✨ 😀 😄 😆 😉 😇 😌 😎 😏 😢 😤 😱 🥺
😳 😬 🤯 🥳 😋 😜 🤗 😷 🤒 😵 😃 😁 🙂 😒
😐 😮 🤨 😓 🥱 🙃 😑 😶 🙄 😲 😕 😟 😞 😩
```

## Install

### Arch Linux (package)

Download `ttf-miku-emoji-1.6.0-1-any.pkg.tar.zst` from the
[releases page](../../releases) and install it:

```bash
sudo pacman -U ttf-miku-emoji-1.6.0-1-any.pkg.tar.zst
fc-cache -f
```

Uninstall: `sudo pacman -R ttf-miku-emoji && fc-cache -f`

### Any other Linux (script)

Works on Debian/Ubuntu, Fedora, openSUSE, Alpine … anything with fontconfig:

```bash
git clone https://github.com/BearThomas/miku-emoji-font.git
cd miku-emoji-font

./install.sh          # system-wide (asks for sudo)
# or
./install.sh --user   # current user only, no root
```

Remove with `./uninstall.sh` (add `--user` if you installed that way).

Then restart your browser / terminal so they reload their font tables.

Temporarily disable while keeping the files:

```bash
sudo rm /etc/fonts/conf.d/75-miku-emoji.conf && fc-cache -f
```

### Build from source (Arch)

```bash
git clone https://github.com/BearThomas/miku-emoji-font.git
cd miku-emoji-font
makepkg -si
```

## How it works

ZWJ sequences (😶‍🌫️ 😮‍💨 😵‍💫) are supported: the font carries the component
glyphs plus a `rlig` ligature that maps the whole cluster to a dedicated
glyph. This is why the container's CBLC index subtables are rebuilt as one
dense table per strike.

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
