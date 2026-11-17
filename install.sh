#!/usr/bin/env bash
# Install the Miku emoji font.
#   ./install.sh          system-wide (needs sudo)
#   ./install.sh --user   current user only (no root)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FONT="$HERE/MikuEmoji.ttf"
CONF="$HERE/75-miku-emoji.conf"
MODE="system"
[ "${1:-}" = "--user" ] && MODE="user"

[ -f "$FONT" ] || { echo "error: MikuEmoji.ttf not found next to this script" >&2; exit 1; }
[ -f "$CONF" ] || { echo "error: 75-miku-emoji.conf not found next to this script" >&2; exit 1; }

if [ "$MODE" = "system" ]; then
  if [ "$(id -u)" -ne 0 ]; then
    command -v sudo >/dev/null || { echo "error: need root (run as root or install sudo)" >&2; exit 1; }
    exec sudo bash "$0" "$@"
  fi
  install -Dm644 "$FONT" /usr/share/fonts/miku-emoji/MikuEmoji.ttf
  install -Dm644 "$CONF" /usr/share/fontconfig/conf.avail/75-miku-emoji.conf
  install -d /etc/fonts/conf.d
  ln -sf /usr/share/fontconfig/conf.avail/75-miku-emoji.conf /etc/fonts/conf.d/75-miku-emoji.conf
  fc-cache -f >/dev/null 2>&1 || true
  echo "installed system-wide:"
  echo "  /usr/share/fonts/miku-emoji/MikuEmoji.ttf"
  echo "  /etc/fonts/conf.d/75-miku-emoji.conf"
else
  install -Dm644 "$FONT" "$HOME/.local/share/fonts/miku-emoji/MikuEmoji.ttf"
  install -Dm644 "$CONF" "$HOME/.config/fontconfig/conf.d/75-miku-emoji.conf"
  fc-cache -f >/dev/null 2>&1 || true
  echo "installed for $USER:"
  echo "  $HOME/.local/share/fonts/miku-emoji/MikuEmoji.ttf"
  echo "  $HOME/.config/fontconfig/conf.d/75-miku-emoji.conf"
fi

echo
echo "verify:  fc-match -s ':charset=1F602' | head -1   # should print Miku Emoji"
echo "then restart browsers/terminals so they reload their font tables."
