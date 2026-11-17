#!/usr/bin/env bash
# ch02_env_size.sh -- measure the book environment for Chapter 2's compute note.
#
# Installs setup/pixi.toml + setup/pixi.lock into a fresh folder and reports
# install time, installed size, file count, and how many installed files are
# hard links into pixi's cache (on Linux, when cache and folder share a
# filesystem). Run it on each system you want numbers for (laptop, cluster
# project storage). Nothing is written to your home folder: the cache and
# pixi's home go in the work folder unless you set them yourself.
#
# Usage: scripts/ch02_env_size.sh [work-folder]   (default: ./ch02-env-test)
# Needs: pixi on PATH, GNU du/find.
#
# Values used in the book (draft environment, pixi 0.84.2):
#   WSL Ubuntu laptop, 2026-11-14:  9.8 s, 1.3 GB, 15,524 files
#   Ceres /project, 2026-11-14:     reinstall from cache 57 s, 1.3 GB
#   Nova /work, 2026-11-16:         reinstall from cache 2.4 s, 813 MB
#                                   (same files; compressed storage)
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
work="${1:-ch02-env-test}"
mkdir -p "$work"
work="$(cd "$work" && pwd)"

export PIXI_CACHE_DIR="${PIXI_CACHE_DIR:-$work/pixi-cache}"
export PIXI_NO_TELEMETRY=1

rm -rf "$work/env" && mkdir -p "$work/env"
cp "$repo/setup/pixi.toml" "$repo/setup/pixi.lock" "$work/env/"
cd "$work/env"

echo "pixi:     $(pixi --version)"
echo "system:   $(uname -sm)"
echo "folder:   $work/env"
echo "cache:    $PIXI_CACHE_DIR"
echo

start=$(date +%s)
pixi install --locked
end=$(date +%s)
echo "install:  $((end - start)) s"

pixi run check
echo
echo "size:     $(du -sh .pixi | cut -f1) in .pixi"
echo "files:    $(find .pixi -type f | wc -l | tr -d " ") in .pixi"
echo "linked:   $(find .pixi -type f -links +1 | wc -l | tr -d " ") files with a link count above 1"
echo "cache:    $(du -sh "$PIXI_CACHE_DIR" | cut -f1), $(find "$PIXI_CACHE_DIR" -type f | wc -l | tr -d " ") files"
