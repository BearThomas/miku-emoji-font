#!/usr/bin/env bash
# Remove the Miku emoji font. Also removes the conf from any activation path.
#   ./uninstall.sh          system-wide (needs sudo)
#   ./uninstall.sh --user   current user only
set -euo pipefail

MODE="system"
[ "${1:-}" = "--user" ] && MODE="user"

if [ "$MODE" = "system" ] && [ "$(id -u)" -ne 0 ]; then
  command -v sudo >/dev/null || { echo "error: need root or sudo" >&2; exit 1; }
  exec sudo bash "$0" "$@"
fi

if [ "$MODE" = "system" ]; then
  rm -f /etc/fonts/conf.d/75-miku-emoji.conf
  rm -f /usr/share/fontconfig/conf.avail/75-miku-emoji.conf
  rm -rf /usr/share/fonts/miku-emoji
  echo "removed system-wide install (symlink and all)"
else
  rm -f "$HOME/.config/fontconfig/conf.d/75-miku-emoji.conf"
  rm -rf "$HOME/.config/miku-emoji"
  rm -rf "$HOME/.local/share/fonts/miku-emoji"
  echo "removed user install"
fi

fc-cache -f >/dev/null 2>&1 || true
echo "restart browsers/apps to pick the change up."
