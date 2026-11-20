# Miku Emoji Font

Fan-made **Hatsune Miku** color emoji font: **120 emoji** (117 codepoints +
3 ZWJ sequences), built as a `CBDT/CBLC` color bitmap font — the same format
as Noto Color Emoji, so it works on Linux, Windows, Android and in all
Chromium/Firefox builds.

Anything not in the list below keeps using your normal emoji font.
The full list with names and codepoints is in [`docs/emoji-list.md`](docs/emoji-list.md).


## ⚠️ 双版本画风（v2.0 起）

字体在**大字号（≥40px）使用贴近官方设定的还原版**（细线、冷白肤色、正常眼型），
在**小字号（≤32px）使用高辨识版**（粗描边、大五官）。

> **如果你在聊天窗口（16~24px）觉得某些表情「认不清」或「和预览图不一样」，这是刻意的。**
> 还原版在 16~20px 下几乎不可读，所以小字号走的是高辨识版。
> 想看还原效果，把 emoji 放到 48px 以上。

详见 [`docs/dual-art.md`](docs/dual-art.md)。

## Install

### Arch Linux (package)

Download `ttf-miku-emoji-2.0.0-1-any.pkg.tar.zst` from the
[releases page](../../releases):

```bash
sudo pacman -U ttf-miku-emoji-2.0.0-1-any.pkg.tar.zst
fc-cache -f
```

Uninstall: `sudo pacman -R ttf-miku-emoji && fc-cache -f`

### Any other Linux (script)

```bash
git clone https://github.com/BearThomas/miku-emoji-font.git
cd miku-emoji-font

./install.sh              # install font + conf file (INACTIVE)
./install.sh --enable     # also activate system-wide (needs sudo)
./install.sh --user       # current user only (inactive)
./install.sh --user --enable
```

Remove with `./uninstall.sh` (add `--user` if you installed that way).

### ⚠️ Not enabled by default

Installing the font does **not** change your emoji. The package/script only
places `75-miku-emoji.conf` in `conf.avail` (an inert location). To opt in:

```bash
# system-wide
sudo ln -s /usr/share/fontconfig/conf.avail/75-miku-emoji.conf /etc/fonts/conf.d/
fc-cache -f

# or just for you
mkdir -p ~/.config/fontconfig/conf.d
cp /usr/share/fontconfig/conf.avail/75-miku-emoji.conf ~/.config/fontconfig/conf.d/
fc-cache -f
```

Then restart browsers/terminals so they reload their font tables.
To undo, delete that symlink/file and run `fc-cache -f`.

## Source files

The 120 source PNGs (~158 MB) are **not** in git; they ship as a source
tarball in [Releases](../../releases): `miku-emoji-src-2.0.0.tar.gz`.

It contains `art/` (PNGs + manifests), `scripts/` (builder + checker +
install/uninstall), the built `MikuEmoji.ttf`, the Piapro license and the
prompt template. See [`src-README.md`](src-README.md) for the rebuild steps.

## AUR

The package is not on AUR yet (registration is currently unavailable).
An AUR-ready `PKGBUILD` + `.SRCINFO` are kept in `publish/aur/` in this
repository; once an AUR account is available they can be pushed to
`ssh://aur@aur.archlinux.org/ttf-miku-emoji.git`.

Note: AUR does not accept binary blobs in the git repo, so the AUR package
downloads the *source tarball* from GitHub Releases and installs the TTF
from it. This is the normal pattern for fonts.

## License

Hatsune Miku is a character owned by Crypton Future Media, Inc.
This is a non-commercial fan work under the
[Piapro Character License](https://piapro.net/en_for_creators.html).

- Free to use, modify and redistribute for non-commercial purposes.
- Selling it or bundling it into a paid product is **not** allowed.
- Keep `LICENSE` with any redistribution.

## Links

- Releases: https://github.com/BearThomas/miku-emoji-font/releases
- Prompt template for making a different character: [`PROMPT_TEMPLATE.md`](PROMPT_TEMPLATE.md)
- Full emoji list: [`docs/emoji-list.md`](docs/emoji-list.md)
