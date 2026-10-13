#!/usr/bin/env python3
"""Make a word-by-word Chinese label for every node name of a cone.py graph.

Usage: zh_gloss.py <glossary.txt> < graph.dot > names.tsv

Splits each name at dots, underscores and capital letters and looks every word up
in the glossary ("english=中文" entries separated by whitespace). Words that are
not listed stay in English. The result is the names.tsv that zh_labels.py reads.
"""
import re, sys

gloss = {}
for line in open(sys.argv[1]):
    if not line.startswith("#"):
        gloss.update(t.split("=", 1) for t in line.split())

def part(text):
    out = ""
    for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+|[^\W\d_]+", text):
        zh = gloss.get(w.lower())
        if w.lower() == "sub" and text.lower() != "sub":
            zh = "子"  # `sub` alone is subtraction; inside a longer word it is a prefix
        if zh:
            out += zh
        else:  # keep English and numbers apart from their neighbours
            out += (" " if out and not out.endswith(" ") else "") + w + " "
    return out.strip()

# tred wraps long names over several lines with a trailing backslash; undo that.
for line in sys.stdin.read().replace("\\\n", "").splitlines(keepends=True):
    if m := re.match(r'\s*"?([^"\s\[]+)"?\s*\[fillcolor', line):
        name = m[1]
        label = " · ".join(" ".join(filter(None, map(part, comp.split("_"))))
                           for comp in name.split("."))
        print(f"{name}\t{label}")
