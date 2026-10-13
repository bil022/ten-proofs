#!/usr/bin/env python3
"""Write a Lean file containing only what the given theorems need.

Usage: extract.py <Source.lean> <graph.dot> <decls.tsv> <root>...
           [--keep <file>] [--dropped <file>] > out.lean

<graph.dot> and <decls.tsv> are the DeclGraph.lean outputs for <Source.lean>.
Every declaration the roots do not transitively depend on is cut out of the
source by its line range; everything else is copied unchanged. `--keep` names a
file listing extra declarations (one per line) to retain along with what they need;
`--dropped` writes the names of the declarations that were cut.
"""
import re, sys

args = sys.argv[1:]
extra = []
if "--keep" in args:
    i = args.index("--keep")
    extra = open(args[i + 1]).read().split()
    del args[i:i + 2]
dropped_out = None
if "--dropped" in args:
    i = args.index("--dropped")
    dropped_out = args[i + 1]
    del args[i:i + 2]
lean, dot, tsv, *roots = args

pred, nodes = {}, set()
for line in open(dot):
    if m := re.match(r'\s*"([^"]+)" -> "([^"]+)"', line):
        pred.setdefault(m[2], set()).add(m[1])
    elif m := re.match(r'\s*"([^"]+)" \[', line):
        nodes.add(m[1])
for r in roots + extra:
    if r not in nodes:
        sys.exit(f"{r}: not a declaration of {dot}")
cone, todo = set(), roots + extra
while todo:
    n = todo.pop()
    if n not in cone:
        cone.add(n)
        todo += pred.get(n, ())

src = open(lean).read().split("\n")

HEAD = re.compile(r"((?:private|protected|noncomputable|unsafe|partial|nonrec|scoped|local)\s+)*"
                  r"(theorem|lemma|def|abbrev|instance|structure|inductive|class|opaque)\b")

def head(a, b):
    """(keyword, has attribute) of the declaration on lines a..b, or None if it is
    something else (macro, syntax, notation, ...)."""
    text = "\n".join(src[a - 1:b]).lstrip()
    if text.startswith("/--"):
        text = text[text.index("-/") + 2:].lstrip()
    attr = False
    while text.startswith("@["):
        depth = 0
        for i, ch in enumerate(text):
            depth += (ch == "[") - (ch == "]")
            if ch == "]" and depth == 0:
                break
        attr, text = True, text[i + 1:].lstrip()
    m = HEAD.match(text)
    return (m[2], attr) if m else None

decls = []
for row in open(tsv):
    name, rep, kind, a, b = row.rstrip("\n").split("\t")
    if int(a):
        decls.append((name, rep, int(a), int(b)))

# Instances, abbreviations and attribute-tagged declarations (`@[simp]`, …) steer
# elaboration without showing up in the proof terms that use them, so keep them all.
cand = {}
for name, rep, a, b in decls:
    if name == rep and (h := head(a, b)):
        if h[0] in ("instance", "abbrev", "class") or h[1]:
            todo.append(name)
        else:
            cand[name] = (a, b)
while todo:
    n = todo.pop()
    if n not in cone:
        cone.add(n)
        todo += pred.get(n, ())

# `variable (S : Foo)`, `attribute [instance] foo` and similar commands stay in the
# file, so whatever they mention has to stay too.
covered = [False] * (len(src) + 2)
for name, rep, a, b in decls:
    for i in range(a, b + 1):
        covered[i] = True
mentioned, inside = set(), False
for i, text in enumerate(src, 1):
    if text[:1] not in ("", " ", "\t"):
        inside = bool(re.match(r"(local\s+|scoped\s+)?(variable|attribute|include|omit|export|open)\b", text))
    if inside and not covered[i]:
        mentioned |= set(re.findall(r"[^\W\d][\w'!?]*", text))
todo = [n for n in cand if n.rsplit(".", 1)[-1] in mentioned]
while todo:
    n = todo.pop()
    if n not in cone:
        cone.add(n)
        todo += pred.get(n, ())

# A declaration's lines go only if nothing we keep was declared inside them.
needed = [False] * (len(src) + 2)
for name, rep, a, b in decls:
    if rep in cone:
        for i in range(a, b + 1):
            needed[i] = True
cand = {n: r for n, r in cand.items() if n not in cone}

PREFIX = re.compile(r"(set_option|omit|open|include|variable|universe)\b")
drop, dropped = [False] * (len(src) + 2), []
for name, (a, b) in cand.items():
    if any(needed[a:b + 1]):
        continue
    dropped.append(name)
    # `set_option … in` / `omit … in` lines above a declaration belong to it.
    while True:
        k = a - 1
        while k > 1 and not src[k - 1].strip():
            k -= 1
        if k < 1 or not src[k - 1].rstrip().endswith(" in"):
            break
        while k > 1 and not PREFIX.match(src[k - 1]) and a - k < 6:
            k -= 1
        if not PREFIX.match(src[k - 1]) or any(needed[k:a]):
            break
        a = k
    for i in range(a, b + 1):
        drop[i] = True

out, blank = [], False
for i, text in enumerate(src, 1):
    if drop[i] or (blank and not text.strip() and drop[i - 1]):
        continue
    out.append(text)
    blank = not text.strip()
sys.stdout.write("\n".join(out).rstrip("\n") + "\n\n")
for r in roots:
    print(f"#print axioms {r}")
print(f"{lean}: dropped {len(dropped)} declarations, {len(src)} -> {len(out)} lines",
      file=sys.stderr)
if dropped_out:
    open(dropped_out, "w").write("".join(n + "\n" for n in sorted(dropped)))
