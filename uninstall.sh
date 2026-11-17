#!/usr/bin/env bash
# Remove the Miku emoji font.
#   ./uninstall.sh          system-wide (needs sudo)
#   ./uninstall.sh --user   current user only
set -euo pipefail

MODE="system"
[ "${1:-}" = "--user" ] && MODE="user"

if [ "$MODE" = "system" ]; then
  if [ "$(id -u)" -ne 0 ]; then
    command -v sudo >/dev/null || { echo "error: need root" >&2; exit 1; }
    exec sudo bash "$0" "$@"
  fi
  rm -f /etc/fonts/conf.d/75-miku-emoji.conf
  rm -f /usr/share/fontconfig/conf.avail/75-miku-emoji.conf
  rm -rf /usr/share/fonts/miku-emoji
  fc-cache -f >/dev/null 2>&1 || true
  echo "removed system-wide install"
else
  rm -f "$HOME/.config/fontconfig/conf.d/75-miku-emoji.conf"
  rm -rf "$HOME/.local/share/fonts/miku-emoji"
  fc-cache -f >/dev/null 2>&1 || true
  echo "removed user install"
fi
echo "restart browsers/terminals to pick the change up."
