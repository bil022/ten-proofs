#!/usr/bin/env bash
# Dependency graphs of the riemann-hypothesis formalization
# (https://github.com/leanprover-community/riemann-hypothesis).
#
# Usage: scripts/rh/rh_all.sh <riemann-hypothesis clone>
#
# The clone must be built; the project cache is enough:
#   git clone https://github.com/leanprover-community/riemann-hypothesis
#   cd riemann-hypothesis && lake exe cache get    # about 85 GB, needs python3 >= 3.11
#
# Writes, under scripts/:
#   en/{dot,svg,pdf,png}/riemannHypothesis.*          top of the proof, theorem by theorem
#   en/{dot,svg,pdf,png}/riemannHypothesis_folders.*  the whole proof, folder by folder
#   en/{dot,svg,pdf,png}/riemannHypothesis_blocks.*   the whole proof, cut into self-contained blocks
#   zh/...                                            the same with Chinese labels
#   rh/folders.tsv                                    size of each folder
#   rh/blocks.tsv                                     size of each block
#   rh/site/data/                                     data of the explorer website
#
# Needs Graphviz and rsvg-convert, as for ../run_all.sh. Takes about ten minutes
# and roughly 15 GB of memory for each of 16 Lean processes run in parallel.
set -euo pipefail
rh=$(cd "$1" && pwd)
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
  find CompanionTheory Development Formalism GroundTheory Lemmata PositivityTheory \
    ReciprocityTheory -name '*.olean' && ls Main.olean Statements.olean) |
  sed "s|^|$rh/.lake/build/lib/lean/|" > "$work/all.txt"
rm -f "$work"/b.*
split -n l/16 -d "$work/all.txt" "$work/b."
ls "$work"/b.?? | (cd "$rh" && xargs -P 16 -I{} sh -c \
  "lake env lean --run '$S/rh/RHRead.lean' {} > {}.tsv")

# 2. Graphs.
python3 rh/rh_cone.py "$work" "$work"
python3 rh/rh_blocks.py "$work" "$work"
python3 rh/rh_site.py "$work" rh/site "$(git -C "$rh" rev-parse HEAD)"
mv "$work/folders.tsv" "$work/blocks.tsv" rh/
for name in riemannHypothesis riemannHypothesis_folders riemannHypothesis_blocks; do
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
echo "riemann-hypothesis commit: $(git -C "$rh" rev-parse HEAD)"
