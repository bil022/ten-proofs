#!/usr/bin/env python3
"""Write the data of the riemann-hypothesis explorer (scripts/rh/site/).

Usage: rh_site.py <dir with b.*.tsv> <site dir> <riemann-hypothesis commit>

The site walks the dominator tree of domtree.py: the page of a declaration X
shows the declarations that belong directly to X (its children in the tree),
each with the size of its own subtree, and which of them use which.

Every use of b by a, where b belongs directly to X, is a use inside the page of X:
everything that uses b lies under X (that is what "b belongs to X" means), so a
is X itself or under one of X's children. The page of X therefore draws an arrow
from b to that child, or to X.

Writes
  <site>/data/meta.json        commit, totals, number of shards
  <site>/data/v/<k>.json.gz    the pages of every node v with v % SHARDS == k
  <site>/data/names.tsv.gz     name, node, parent, size: for the search box

The children of a page that are not drawn are grouped by which drawn children
use them (see sharing()), so the page shows, for instance, "used by A and B"
instead of one box for everything else.
"""
import collections, gzip, json, os, sys

import domtree

SHARDS = 512
SHOWN = 40  # children drawn on a page; the others are grouped, see sharing()

src, site, commit = sys.argv[1], sys.argv[2], sys.argv[3]
t = domtree.Tree(src)
N = len(t.names)
idom, kids, size, depth, succ = t.idom, t.kids, t.size, t.depth, t.succ
print(f"tree: {N - 1} declarations", file=sys.stderr)

# Uses inside each page: (X, user child or X, used child) -> number of uses.
uses = collections.Counter()
path = []
stack = [0]
while stack:
    a = stack.pop()
    del path[depth[a]:]
    path.append(a)
    for b in succ[a]:
        x = idom[b]
        uses[(x, a if a == x else path[depth[x] + 1], b)] += 1
    stack += kids[a]
print(f"{len(uses)} arrows between children", file=sys.stderr)
per_page = collections.defaultdict(list)
for (x, a, b), w in uses.items():
    per_page[x].append((a, b, w))
del uses


rank = [0] * N
for i, v in enumerate(t.rpo):
    rank[v] = i


def sharing(x, ks, shown, edges):
    """For each child of x that is not drawn, the drawn children (and x itself)
    that use it, directly or through other children that are not drawn.

    Returns {child: bit set}, bit 0 for x and bit i + 1 for the i-th drawn child.
    A use from a child c to a child d means a declaration under c uses d, so c
    comes before d in reverse postorder: one pass in that order is enough."""
    drawn = {v: i for i, v in enumerate(ks[:shown])}
    out = collections.defaultdict(list)
    for a, b, _ in edges:
        out[a].append(b)
    sig = collections.defaultdict(int)
    for a in sorted(out, key=rank.__getitem__):
        s = 1 if a == x else (1 << (drawn[a] + 1)) if a in drawn else sig[a]
        for b in out[a]:
            if b not in drawn:
                sig[b] |= s
    return {v: sig[v] for v in ks[shown:]}


def reduce(nodes, edges):
    """Arrows implied by a longer path, as in Graphviz tred. edges: user -> used."""
    out = collections.defaultdict(set)
    for a, b in edges:
        out[a].add(b)
    redundant = set()
    for a, b in edges:
        # Is b reachable from a without the direct arrow?
        todo, seen = [c for c in out[a] if c != b], set()
        while todo:
            c = todo.pop()
            if c == b:
                redundant.add((a, b))
                break
            if c not in seen:
                seen.add(c)
                todo += out[c]
    return redundant


shards = [dict() for _ in range(SHARDS)]
for x in range(N):
    if not kids[x]:
        continue
    ks = sorted(kids[x], key=lambda v: (-size[v], t.label(v)))
    pos = {v: i for i, v in enumerate(ks)}
    shown = min(len(ks), SHOWN)
    # Display index: 0..shown-1 a child, -1 the page's own node, -2 all other children.
    disp = lambda v: -1 if v == x else (pos[v] if pos[v] < shown else -2)
    agg = collections.Counter()
    for a, b, w in per_page[x]:
        da, db = disp(a), disp(b)
        if da != db:
            agg[(da, db)] += w
    # Children not drawn, grouped by the drawn children that use them.
    groups, group_of = [], {}
    if len(ks) > shown:
        sig = sharing(x, ks, shown, per_page[x])
        by_sig = collections.defaultdict(list)
        for v in ks[shown:]:
            by_sig[sig[v]].append(v)
        order = sorted(by_sig, key=lambda s: (-sum(size[v] for v in by_sig[s]), -len(by_sig[s])))
        for g, s in enumerate(order):
            users = [i - 1 for i in range(shown + 1) if s >> i & 1]  # -1 is x itself
            groups.append([users, len(by_sig[s]), sum(size[v] for v in by_sig[s])])
            for v in by_sig[s]:
                group_of[v] = g
    inner = [e for e in agg if -2 not in e]
    redundant = reduce(set(range(-1, shown)), inner)
    anc, v = [], x
    while v:
        v = idom[v]
        anc.append([v, t.label(v)])
    shards[x % SHARDS][x] = {
        "name": t.label(x), "kind": t.kind(x), "module": t.module(x), "lines": t.span(x),
        "size": size[x] - (x == 0), "path": anc[::-1],  # the entry is not a declaration
        # node, name, kind, module, size, children of its own, first and last source
        # line, group (for children not drawn, else -1)
        "kids": [[v, t.label(v), t.kind(v), t.module(v), size[v], len(kids[v]), *t.span(v),
                  group_of.get(v, -1)] for v in ks],
        # drawn children using the group (-1: the page's own node), parts, declarations
        "groups": groups,
        "shown": shown,
        # user, used, uses, implied by a longer path
        "edges": [[a, b, w, int((a, b) in redundant)] for (a, b), w in sorted(agg.items())],
    }

os.makedirs(os.path.join(site, "data", "v"), exist_ok=True)
for k, pages in enumerate(shards):
    with gzip.open(os.path.join(site, "data", "v", f"{k}.json.gz"), "wt", compresslevel=9) as f:
        json.dump(pages, f, separators=(",", ":"), ensure_ascii=False)
with gzip.open(os.path.join(site, "data", "names.tsv.gz"), "wt", compresslevel=9) as f:
    for v in range(1, N):
        f.write(f"{t.label(v)}\t{v}\t{idom[v]}\t{size[v]}\t{len(kids[v])}\n")
kinds = collections.Counter(t.kind(v) for v in range(1, N))
print(f"source lines known for {sum(1 for v in range(1, N) if t.span(v)[0])} of {N - 1}", file=sys.stderr)
with open(os.path.join(site, "data", "meta.json"), "w") as f:
    json.dump({"commit": commit, "declarations": N - 1, "theorems": kinds["theorem"],
               "pages": sum(len(s) for s in shards), "shards": SHARDS, "shown": SHOWN}, f)
print(f"{sum(len(s) for s in shards)} pages in {SHARDS} shards", file=sys.stderr)
