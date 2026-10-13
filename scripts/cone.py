#!/usr/bin/env python3
"""Cut a DeclGraph.lean DOT file down to the proof of one theorem.

Usage: cone.py <in.dot> <root declaration> [--defs] > out.dot

Keeps only what the root transitively depends on, drops Lean's auto-generated
helpers, and prints short names. Definitions are dropped unless --defs is given;
a dashed edge means the dependency goes through a dropped definition.
Pipe the result through `tred` to remove edges implied by longer paths.
"""
import re, sys

src, root = sys.argv[1], sys.argv[2]
keep_defs = "--defs" in sys.argv
AUX = re.compile(r"\.(congr_simp|injEq|inj|noConfusion|noConfusionType|sizeOf_spec|ctorIdx)$")

kind, pred = {}, {}
for line in open(src):
    if m := re.match(r'\s*"([^"]+)" -> "([^"]+)"', line):
        pred.setdefault(m[2], set()).add(m[1])
    elif m := re.match(r'\s*"([^"]+)" \[shape=(\w+)', line):
        kind[m[1]] = "thm" if m[2] == "ellipse" else "def"

root = next(n for n in kind if n == root or n.endswith("." + root))
ns = root.rsplit(".", 1)[0] + "."
cone, todo = set(), [root]
while todo:
    n = todo.pop()
    if n not in cone:
        cone.add(n)
        todo += pred.get(n, ())
cone = {n for n in cone if not AUX.search(n) and (keep_defs or kind[n] == "thm")}

short = lambda n: n.removeprefix(ns)
print("digraph G {\n  rankdir=LR;\n  ranksep=0.6; nodesep=0.25;")
print('  node [fontname=Helvetica, fontsize=11, style="filled,rounded", shape=box];')
print('  edge [color="#8a8a8a", arrowsize=0.7];')
for n in sorted(cone):
    fill = "#ffd58a" if n == root else "#cfe8ff" if kind[n] == "thm" else "#d9f2d0"
    print(f'  "{short(n)}" [fillcolor="{fill}"];')
for n in sorted(cone):
    # A dropped definition would cut the link between a theorem it uses and the
    # theorems that use it, so look through dropped nodes and draw that link dashed.
    direct = {d for d in pred.get(n, ()) if d in cone}
    via, seen, todo = set(), set(), [d for d in pred.get(n, ()) if d not in cone]
    while todo:
        d = todo.pop()
        if d in seen:
            continue
        seen.add(d)
        for e in pred.get(d, ()):
            (via.add if e in cone else todo.append)(e)
    for d in sorted(direct):
        print(f'  "{short(d)}" -> "{short(n)}";')
    for d in sorted(via - direct):
        print(f'  "{short(d)}" -> "{short(n)}" [style=dashed];')
print("}")
