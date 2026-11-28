#!/usr/bin/env python3
"""Build the top-of-proof and folder graphs of a Riemann Hypothesis proof from
the RHRead.lean batches.

Usage: rh_cone.py <project> <dir with b.*.tsv> <out dir>

<project> is a key of projects.PROJECTS (riemannHypothesis, grh, grhCompact),
used as the prefix of the output files. Writes two graphs and a table:

  <out>/<project>.dot          theorems within DEPTH steps of the five
                               theorems of Main.lean, in the style of
                               ../cone.py (solid and dashed arrows)
  <out>/<project>_folders.dot  one box per source folder (see the project's
                               folder()), with an arrow when a declaration in
                               one uses one in another
  <out>/folders.tsv            folder, theorems, definitions, modules

Pipe each .dot through `tred` to remove arrows implied by longer paths.
"""
import collections, os, sys

from projects import PROJECTS, ROOTS, load

key, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
P = PROJECTS[key]
DEPTH = P["depth"]

info, used, _ = load(src)
pred = {n: {u for u in us if u in info and u != n} for n, us in used.items()}

cone, todo = set(), list(ROOTS)
while todo:
    n = todo.pop()
    if n not in cone:
        cone.add(n)
        todo += pred[n]
kinds = collections.Counter(info[n][1] for n in cone)
edges = sum(len(pred[n]) for n in cone)
print(f"{len(info)} declarations, {len(cone)} needed by Main.lean "
      f"({kinds['theorem']} theorems), {edges} arrows, "
      f"{len({info[n][2] for n in cone})} modules", file=sys.stderr)

# --- theorem graph of the top of the proof -----------------------------------
is_thm = lambda n: info[n][1] == "theorem"

def thm_pred(n):
    """Theorems n uses: (cited directly, reached only through a definition)."""
    direct = {d for d in pred[n] if is_thm(d)}
    via, seen, todo = set(), set(), [d for d in pred[n] if not is_thm(d)]
    while todo:
        d = todo.pop()
        if d not in seen:
            seen.add(d)
            for e in pred[d]:
                (via.add if is_thm(e) else todo.append)(e)
    return direct, via - direct

top, layer, tp = set(ROOTS), set(ROOTS), {}
for _ in range(DEPTH):
    nxt = set()
    for n in layer:
        tp[n] = thm_pred(n)
        nxt |= tp[n][0] | tp[n][1]
    layer = nxt - top
    top |= layer
for n in layer:
    tp[n] = thm_pred(n)
# Theorems at the last layer whose own proof uses theorems not drawn.
frontier = {n for n in top if (tp[n][0] | tp[n][1]) - top}

label = lambda n: info[n][0]
with open(os.path.join(out, f"{key}.dot"), "w") as g:
    g.write("digraph G {\n  rankdir=LR;\n  ranksep=0.6; nodesep=0.25;\n")
    g.write('  node [fontname=Helvetica, fontsize=11, style="filled,rounded", shape=box];\n')
    g.write('  edge [color="#8a8a8a", arrowsize=0.7];\n')
    for n in sorted(top, key=label):
        fill = "#ffd58a" if n in ROOTS else "#e8e8e8" if n in frontier else "#cfe8ff"
        g.write(f'  "{label(n)}" [fillcolor="{fill}"];\n')
    for n in sorted(top, key=label):
        direct, via = tp[n]
        for d in sorted(direct & top, key=label):
            g.write(f'  "{label(d)}" -> "{label(n)}";\n')
        for d in sorted(via & top, key=label):
            g.write(f'  "{label(d)}" -> "{label(n)}" [style=dashed];\n')
    g.write("}\n")
print(f"top of the proof: {len(top)} theorems, {len(frontier)} on the frontier", file=sys.stderr)

# --- folder graph --------------------------------------------------------------
folder = lambda n: P["folder"](info[n][2])
stats = collections.defaultdict(lambda: [0, 0, set()])
for n in cone:
    s = stats[folder(n)]
    s[0 if is_thm(n) else 1] += 1
    s[2].add(info[n][2])
links = {(folder(a), folder(n)) for n in cone for a in pred[n]}
links = {(a, b) for a, b in links if a != b}

COLOR = P["color"]
with open(os.path.join(out, "folders.tsv"), "w") as t:
    t.write("folder\ttheorems\tdefinitions\tmodules\n")
    for f in sorted(stats):
        t.write(f"{f}\t{stats[f][0]}\t{stats[f][1]}\t{len(stats[f][2])}\n")
with open(os.path.join(out, f"{key}_folders.dot"), "w") as g:
    g.write("digraph G {\n  rankdir=LR;\n  ranksep=1.2; nodesep=0.2;\n")
    g.write('  node [fontname=Helvetica, fontsize=11, style="filled,rounded", shape=box];\n')
    g.write('  edge [color="#8a8a8a", arrowsize=0.6];\n')
    for f in sorted(stats):
        top_dir, _, rest = f.partition(".")
        text = (f"{top_dir}/\\n{rest.replace('.', '/')}" if rest else top_dir) + f"\\n{stats[f][0]:,} theorems"
        g.write(f'  "{f}" [fillcolor="{COLOR.get(top_dir, "#ffffff")}", label="{text}"];\n')
    for a, b in sorted(links):
        g.write(f'  "{a}" -> "{b}";\n')
    g.write("}\n")
print(f"folders: {len(stats)} folders, {len(links)} arrows", file=sys.stderr)
