#!/usr/bin/env bash
# Rebuild every graph and standalone proof file under scripts/.
#
# Usage (from the project root, after `lake build`):
#   scripts/run_all.sh            # all theorems listed in scripts/roots.tsv
#   scripts/run_all.sh Permanent  # only the theorems of one file
#
# For each line "<Module> <root declaration>" of roots.tsv this writes, named
# after the last component of the root:
#   modules/<Module>.dot, .decls.tsv   full graph and source positions of the module
#   en/dot, en/svg, en/pdf, en/png     theorem-only dependency graph of the root
#   lean/<root>.lean, .log             what the root needs, as its own Lean file,
#                                      and its compile output
# scripts/zh_all.sh then adds the Chinese-labelled graphs under zh/.
#
# Needs Graphviz (dot, tred) and rsvg-convert:
#   conda create -n graphviz --override-channels -c conda-forge graphviz
set -euo pipefail
cd "$(dirname "$0")/.."
GV="$HOME/miniconda3/envs/graphviz/bin"
[ -d "$GV" ] && PATH="$GV:$PATH"
only="${1:-}"
S=scripts
mkdir -p $S/modules $S/en/dot $S/en/svg $S/en/pdf $S/en/png $S/lean

roots() { awk -v m="$only" 'NF == 2 && (m == "" || $1 == m)' $S/roots.tsv; }
[ -n "$(roots)" ] || { echo "no theorem of '$only' in $S/roots.tsv" >&2; exit 1; }

# 1. Full dependency graph and source positions of each module.
roots | cut -f1 | sort -u | xargs -P 8 -I{} sh -c \
  "lake env lean --run $S/DeclGraph.lean {} --decls $S/modules/{}.decls.tsv > $S/modules/{}.dot"

# 2. Focused graph of each main theorem. The largest layouts take tens of minutes.
roots | while read -r mod root; do
  name="${root##*.}"
  python3 $S/cone.py "$S/modules/$mod.dot" "$root" | tred 2>/dev/null > "$S/en/dot/$name.dot"
done
roots | awk '{n = split($2, a, "."); print a[n]}' | xargs -P 8 -I{} sh -c \
  "dot -Tsvg $S/en/dot/{}.dot -o $S/en/svg/{}.svg &&
   rsvg-convert -f pdf --unlimited -o $S/en/pdf/{}.pdf $S/en/svg/{}.svg &&
   $S/svg2png.sh $S/en/svg/{}.svg $S/en/png/{}.png"

# 3. Standalone Lean file for each main theorem, compiled as a completeness check.
roots | xargs -P 6 -L 1 python3 $S/check.py
