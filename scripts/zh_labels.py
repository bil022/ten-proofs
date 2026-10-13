#!/usr/bin/env python3
"""Add a second-language label above each node name of a cone.py graph.

Usage: cone.py ... | tred | zh_labels.py <names.tsv> > out.dot

<names.tsv> has one "<node name><TAB><label>" per line. Nodes without an entry
keep their plain name.
"""
import re, sys

names = dict(line.rstrip("\n").split("\t") for line in open(sys.argv[1]) if "\t" in line)
used = set()
# tred wraps long names over several lines with a trailing backslash; undo that.
for line in sys.stdin.read().replace("\\\n", "").splitlines(keepends=True):
    if m := re.match(r'(\s*)"?([^"\s\[]+)"?(\s*\[)(fillcolor=.*)', line):
        name = m[2]
        if name in names:
            used.add(name)
            line = f'{m[1]}"{name}"{m[3]}label="{names[name]}\\n{name}", {m[4]}\n'
    sys.stdout.write(line)
if missing := sorted(set(names) - used):
    print("no such node:", *missing, file=sys.stderr)
