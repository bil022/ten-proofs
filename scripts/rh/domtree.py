"""Dominator tree of the riemann-hypothesis proof, shared by rh_blocks.py and rh_site.py.

A declaration D belongs to theorem X when every chain of dependencies from the
five theorems of Main.lean down to D passes through X (X dominates D). Computed
with the iterative algorithm of Cooper, Harvey and Kennedy, "A Simple, Fast
Dominance Algorithm" (2001).
"""
import collections, glob, os

ROOTS = ["riemannHypothesis", "riemannZeta_eq_zero_re", "LFunction_ne_zero_of_half_lt_re",
         "LFunction_eq_zero_re", "LFunction_eq_zero_re_of_isPrimitive"]


class Tree:
    """The dependency graph of Main.lean and its dominator tree.

    Node 0 is a virtual entry, "Main.lean", above the five main theorems.
      names[v]   declaration name (node 0: "Main.lean")
      info[name] (name without private prefix, kind, module)
      succ[v]    the nodes v uses
      idom[v]    immediate dominator; kids[v] the nodes it dominates immediately
      size[v]    declarations in the subtree of v, v included
      depth[v]   depth in the tree; rpo: every node after its dominator
      lines[name] first and last source line, when the .olean records them
    """

    def __init__(self, src):
        self.lines = {}  # name -> (first, last) line in its source file, when known
        info, used = {}, collections.defaultdict(set)
        for f in sorted(glob.glob(os.path.join(src, "b.*.tsv"))):
            for line in open(f):
                name, user, kind, mod, us, first, last = line.rstrip("\n").split("\t")
                if name not in info or info[name][1] == "?":
                    info[name] = (user, kind, mod)
                if first != "0":
                    self.lines[name] = (int(first), int(last))
                used[name].update(us.split())
        deps = {n: [u for u in us if u in info and u != n] for n, us in used.items()}
        del used

        cone, todo = set(), list(ROOTS)
        while todo:
            n = todo.pop()
            if n not in cone:
                cone.add(n)
                todo += deps[n]

        names = ["Main.lean"] + sorted(cone)
        idx = {n: i for i, n in enumerate(names)}
        N = len(names)
        succ = [[] for _ in range(N)]
        succ[0] = [idx[r] for r in ROOTS]
        for n in cone:
            succ[idx[n]] = [idx[d] for d in deps[n]]
        pred = [[] for _ in range(N)]
        for a in range(N):
            for b in succ[a]:
                pred[b].append(a)

        order, seen, stack = [], bytearray(N), [(0, 0)]
        seen[0] = 1
        while stack:
            v, i = stack[-1]
            if i < len(succ[v]):
                stack[-1] = (v, i + 1)
                w = succ[v][i]
                if not seen[w]:
                    seen[w] = 1
                    stack.append((w, 0))
            else:
                order.append(v)
                stack.pop()
        rpo = order[::-1]
        num = [0] * N
        for i, v in enumerate(rpo):
            num[v] = i

        idom = [-1] * N
        idom[0] = 0
        changed = True
        while changed:
            changed = False
            for v in rpo[1:]:
                new = -1
                for p in pred[v]:
                    if idom[p] == -1:
                        continue
                    if new == -1:
                        new = p
                        continue
                    a, b = p, new
                    while a != b:
                        while num[a] > num[b]:
                            a = idom[a]
                        while num[b] > num[a]:
                            b = idom[b]
                    new = a
                if idom[v] != new:
                    idom[v] = new
                    changed = True

        kids = [[] for _ in range(N)]
        for v in range(1, N):
            kids[idom[v]].append(v)
        size = [1] * N
        for v in reversed(rpo):
            if v:
                size[idom[v]] += size[v]
        depth = [0] * N
        for v in rpo[1:]:
            depth[v] = depth[idom[v]] + 1

        self.names, self.info, self.succ, self.idom = names, info, succ, idom
        self.kids, self.size, self.depth, self.rpo = kids, size, depth, rpo

    def label(self, v):
        return "Main.lean" if v == 0 else self.info[self.names[v]][0]

    def kind(self, v):
        return "" if v == 0 else self.info[self.names[v]][1]

    def span(self, v):
        return self.lines.get(self.names[v], (0, 0)) if v else (0, 0)

    def module(self, v):
        return "Main" if v == 0 else self.info[self.names[v]][2]
