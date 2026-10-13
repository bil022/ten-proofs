#!/usr/bin/env bash
# Chinese-labelled SVG, PDF and PNG of each focused graph (en/dot -> zh/dot, zh/svg,
# zh/pdf, zh/png),
# labelled word by word from glossary.zh.txt. A hand-written zh/names/<name>.zh.tsv,
# if present, is used as is.
#
# Usage (from the project root): scripts/zh_all.sh [<Module>]
# Needs the Noto CJK font:  conda install -n graphviz -c conda-forge font-ttf-noto-cjk
set -euo pipefail
cd "$(dirname "$0")"
GV="$HOME/miniconda3/envs/graphviz/bin"
[ -d "$GV" ] && PATH="$GV:$PATH"
export PATH
only="${1:-}"
mkdir -p zh/names zh/dot zh/svg zh/pdf zh/png

awk -v m="$only" 'NF == 2 && (m == "" || $1 == m) {n = split($2, a, "."); print a[n]}' roots.tsv |
  xargs -P 12 -I{} sh -c '
    [ -f zh/names/{}.zh.tsv ] ||
      python3 zh_gloss.py glossary.zh.txt < en/dot/{}.dot > zh/names/{}.zh.tsv
    python3 zh_labels.py zh/names/{}.zh.tsv < en/dot/{}.dot > zh/dot/{}.zh.dot &&
    dot -Nfontname="Noto Sans CJK SC" -Tsvg zh/dot/{}.zh.dot -o zh/svg/{}.zh.svg &&
    rsvg-convert -f pdf --unlimited -o zh/pdf/{}.zh.pdf zh/svg/{}.zh.svg &&
    ./svg2png.sh zh/svg/{}.zh.svg zh/png/{}.zh.png &&
    echo "{} done"'
