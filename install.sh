#!/usr/bin/env bash
# Install the Miku emoji font. It is NOT enabled by default.
#   ./install.sh              install font + conf file (inactive)
#   ./install.sh --enable     also activate it system-wide (needs sudo)
#   ./install.sh --user       install for current user only (inactive)
#   ./install.sh --user --enable   activate for current user
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FONT="$HERE/MikuEmoji.ttf"
CONF="$HERE/75-miku-emoji.conf"
MODE="system"
ENABLE=0
for arg in "$@"; do
  case "$arg" in
    --user) MODE="user" ;;
    --enable) ENABLE=1 ;;
    *) echo "unknown option: $arg" >&2; exit 1 ;;
  esac
done

[ -f "$FONT" ] || { echo "error: MikuEmoji.ttf not found next to this script" >&2; exit 1; }
[ -f "$CONF" ] || { echo "error: 75-miku-emoji.conf not found next to this script" >&2; exit 1; }

if [ "$MODE" = "system" ] && [ "$(id -u)" -ne 0 ]; then
  command -v sudo >/dev/null || { echo "error: need root or sudo" >&2; exit 1; }
  exec sudo bash "$0" "$@"
fi

if [ "$MODE" = "system" ]; then
  install -Dm644 "$FONT" /usr/share/fonts/miku-emoji/MikuEmoji.ttf
  install -Dm644 "$CONF" /usr/share/fontconfig/conf.avail/75-miku-emoji.conf
  echo "font: /usr/share/fonts/miku-emoji/MikuEmoji.ttf"
  echo "conf: /usr/share/fontconfig/conf.avail/75-miku-emoji.conf  (inactive)"
  if [ "$ENABLE" -eq 1 ]; then
    install -d /etc/fonts/conf.d
    ln -sf /usr/share/fontconfig/conf.avail/75-miku-emoji.conf /etc/fonts/conf.d/75-miku-emoji.conf
    echo "ENABLED system-wide"
  fi
else
  install -Dm644 "$FONT" "$HOME/.local/share/fonts/miku-emoji/MikuEmoji.ttf"
  install -Dm644 "$CONF" "$HOME/.config/miku-emoji/75-miku-emoji.conf"
  echo "font: $HOME/.local/share/fonts/miku-emoji/MikuEmoji.ttf"
  echo "conf: $HOME/.config/miku-emoji/75-miku-emoji.conf  (inactive)"
  if [ "$ENABLE" -eq 1 ]; then
    install -Dm644 "$CONF" "$HOME/.config/fontconfig/conf.d/75-miku-emoji.conf"
    echo "ENABLED for $USER"
  fi
fi

fc-cache -f >/dev/null 2>&1 || true
echo
if [ "$ENABLE" -eq 0 ]; then
  echo "To enable later:"
  echo "  system: sudo ln -s /usr/share/fontconfig/conf.avail/75-miku-emoji.conf /etc/fonts/conf.d/"
  echo "  user:   mkdir -p ~/.config/fontconfig/conf.d && cp ~/.config/miku-emoji/75-miku-emoji.conf ~/.config/fontconfig/conf.d/"
fi
echo "verify: fc-match -s ':charset=1F602' | head -1   (after enabling)"
echo "restart browsers/apps so they reload their font tables."
