#!/usr/bin/env python3
"""Cut a Riemann Hypothesis proof into self-contained blocks.

Usage: rh_blocks.py <project> <dir with b.*.tsv> <out dir> [<min block size>]

A declaration D belongs to theorem X when every chain of dependencies from the
five theorems of Main.lean down to D passes through X: D is then used only in
the proof of X, directly or indirectly (X dominates D). These relations form a
tree, the dominator tree. A block is a declaration whose subtree has at least
<min block size> declarations (default: the project's min_block in
projects.py, 2,000 for riemannHypothesis), together with every
declaration in its subtree that belongs to no smaller block.

Writes
  <out>/<project>_blocks.dot  one box per block, with an arrow from each
                              block to the block whose proof it is part of
  <out>/blocks.tsv            block, parent block, declarations of its own,
                              declarations in its subtree, module

The dominator tree is computed by domtree.py.
"""
import collections, os, sys

import domtree
from projects import PROJECTS

key, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
P = PROJECTS[key]
MIN = int(sys.argv[4]) if len(sys.argv) > 4 else P["min_block"]
t = domtree.Tree(src)
names, idom, kids, size = t.names, t.idom, t.kids, t.size
N = len(names)

# Blocks: the entry, and every node whose subtree is large enough.
block = [0] * N
heads = [0]
stack = [0]
while stack:
    v = stack.pop()
    for k in kids[v]:
        block[k] = k if size[k] >= MIN else block[v]
        if block[k] == k:
            heads.append(k)
        stack.append(k)
own = collections.Counter(block)
# Only the tree is drawn. Arrows for every use between blocks would include each
# block's use of the shared lemmas of the blocks above it, and form cycles.
links = {(v, block[idom[v]]) for v in heads if v}

label, module = t.label, t.module
with open(os.path.join(out, "blocks.tsv"), "w") as t:
    t.write("block\tparent block\town declarations\tsubtree declarations\tmodule\n")
    for v in sorted(heads, key=lambda v: -size[v]):
        parent = "" if v == 0 else label(block[idom[v]])
        t.write(f"{label(v)}\t{parent}\t{own[v] - (v == 0)}\t{size[v] - (v == 0)}\t{module(v)}\n")

COLOR = P["color"]
with open(os.path.join(out, f"{key}_blocks.dot"), "w") as g:
    g.write("digraph G {\n  rankdir=LR;\n  ranksep=0.8; nodesep=0.25;\n")
    g.write('  node [fontname=Helvetica, fontsize=11, style="filled,rounded", shape=box];\n')
    g.write('  edge [color="#8a8a8a", arrowsize=0.6];\n')
    for v in sorted(heads, key=label):
        n = own[v] - (v == 0)
        text = f"{label(v)}\\n{n:,} declarations"
        fill = COLOR.get(module(v).split(".")[0], "#ffffff")
        g.write(f'  "{label(v)}" [fillcolor="{fill}", label="{text}"];\n')
    for a, b in sorted(links):
        g.write(f'  "{label(a)}" -> "{label(b)}";\n')
    g.write("}\n")
print(f"{N - 1} declarations, {len(heads)} blocks of at least {MIN:,}, {len(links)} arrows",
      file=sys.stderr)
