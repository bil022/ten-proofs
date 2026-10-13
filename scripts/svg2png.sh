#!/usr/bin/env bash
# Render a Graphviz SVG to PNG: twice the natural size for sharp text, scaled
# down when needed so that the longer side stays within 8,000 pixels.
#
# Usage: svg2png.sh <in.svg> <out.png>
set -euo pipefail
GV="$HOME/miniconda3/envs/graphviz/bin"
[ -d "$GV" ] && PATH="$GV:$PATH"
zoom=$(grep -m1 -o '<svg width="[0-9.]*pt" height="[0-9.]*pt"' "$1" | tr -dc '0-9. ' |
  awk '{m = ($1 > $2 ? $1 : $2) * 96 / 72; z = 8000 / m; print (z > 2 ? 2 : z)}')
rsvg-convert -f png -z "$zoom" --unlimited -o "$2" "$1"
