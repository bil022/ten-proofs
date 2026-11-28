#!/usr/bin/env bash
# Dependency graphs of a Lean proof of the Riemann Hypothesis.
#
# Usage: scripts/rh/rh_all.sh <project> <built Lake project>
#
# <project> is a key of projects.py:
#   riemannHypothesis  a clone of https://github.com/leanprover-community/riemann-hypothesis;
#                      the project cache is enough: lake exe cache get (about 85 GB,
#                      needs python3 >= 3.11)
#   grh                the folder grh/ of a clone of https://github.com/lsernau/grh-lean,
#                      after lake build (one to two hours)
#   grhCompact         its folder grh-compact/, after lake build
#
# Writes, under scripts/:
#   en/{dot,svg,pdf,png}/<project>.*          top of the proof, theorem by theorem
#   en/{dot,svg,pdf,png}/<project>_folders.*  the whole proof, folder by folder
#   en/{dot,svg,pdf,png}/<project>_blocks.*   the whole proof, cut into self-contained blocks
#   zh/...                                    the same with Chinese labels
#   rh/<project>_folders.tsv                  size of each folder
#   rh/<project>_blocks.tsv                   size of each block
#   rh/site/data/<project>/                   data of the explorer website
#
# Needs Graphviz and rsvg-convert, as for ../run_all.sh. For riemannHypothesis it
# takes about ten minutes and roughly 15 GB of memory for each of 16 Lean
# processes run in parallel; the other two take a minute.
set -euo pipefail
key=$1
rh=$(cd "$2" && pwd)
cd "$(dirname "$0")/.."
S=$(pwd)
GV="$HOME/miniconda3/envs/graphviz/bin"
[ -d "$GV" ] && PATH="$GV:$PATH"
export PATH
work="$rh/.lake/rhgraph"
mkdir -p "$work" en/dot en/svg en/pdf en/png zh/names zh/dot zh/svg zh/pdf zh/png

# 1. Read every compiled project module, 16 batches in parallel. One process
#    importing everything would exceed the default vm.max_map_count.
(cd "$rh/.lake/build/lib/lean" &&
  find $(python3 -c "import sys; sys.path.insert(0, '$S/rh'); import projects; print(*projects.PROJECTS['$key']['dirs'])") \
    -name '*.olean' && ls Main.olean Statements.olean) |
  sed "s|^|$rh/.lake/build/lib/lean/|" > "$work/all.txt"
rm -f "$work"/b.*
split -n l/16 -d "$work/all.txt" "$work/b."
ls "$work"/b.?? | (cd "$rh" && xargs -P 16 -I{} sh -c \
  "lake env lean --run '$S/rh/RHRead.lean' {} > {}.tsv")

# 2. Graphs.
python3 rh/rh_cone.py "$key" "$work" "$work"
python3 rh/rh_blocks.py "$key" "$work" "$work"
python3 rh/rh_site.py "$key" "$work" rh/site "$(git -C "$rh" rev-parse HEAD)"
mv "$work/folders.tsv" "rh/${key}_folders.tsv"
mv "$work/blocks.tsv" "rh/${key}_blocks.tsv"
for name in "$key" "${key}_folders" "${key}_blocks"; do
  tred "$work/$name.dot" 2>/dev/null > "en/dot/$name.dot"
  dot -Tsvg "en/dot/$name.dot" -o "en/svg/$name.svg"
  rsvg-convert -f pdf --unlimited -o "en/pdf/$name.pdf" "en/svg/$name.svg"
  ./svg2png.sh "en/svg/$name.svg" "en/png/$name.png"

  python3 zh_gloss.py glossary.zh.txt < "en/dot/$name.dot" > "zh/names/$name.zh.tsv"
  python3 zh_labels.py "zh/names/$name.zh.tsv" < "en/dot/$name.dot" > "zh/dot/$name.zh.dot"
  dot -Nfontname="Noto Sans CJK SC" -Tsvg "zh/dot/$name.zh.dot" -o "zh/svg/$name.zh.svg"
  rsvg-convert -f pdf --unlimited -o "zh/pdf/$name.zh.pdf" "zh/svg/$name.zh.svg"
  ./svg2png.sh "zh/svg/$name.zh.svg" "zh/png/$name.zh.png"
done
echo "$key commit: $(git -C "$rh" rev-parse HEAD)"
