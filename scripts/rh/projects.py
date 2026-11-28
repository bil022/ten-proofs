"""The Lean proofs of the Riemann Hypothesis drawn by the scripts in this folder,
and the reading of the RHRead.lean batches that they share.

Each project is named by the prefix of its output files:

  riemannHypothesis  leanprover-community/riemann-hypothesis, the first proof
  grh                lsernau/grh-lean, folder grh/ (readable edition)
  grhCompact         lsernau/grh-lean, folder grh-compact/ (compact edition)

All three prove the same five theorems in Main.lean (ROOTS).
"""
import collections, glob, os

ROOTS = ["riemannHypothesis", "riemannZeta_eq_zero_re", "LFunction_ne_zero_of_half_lt_re",
         "LFunction_eq_zero_re", "LFunction_eq_zero_re_of_isPrimitive"]

RH_COLOR = {"GroundTheory": "#d9f2d0", "Formalism": "#cfe8ff", "Lemmata": "#e3dcf5",
            "Development": "#ffe0e0", "CompanionTheory": "#d5f0f0", "PositivityTheory": "#fff3c4",
            "ReciprocityTheory": "#f5dcef", "Statements": "#eeeeee", "Main": "#ffd58a"}
# Lib: background results missing from Mathlib. New: the argument itself.
GRH_COLOR = {"Lib": "#cfe8ff", "New": "#ffe0e0", "Statements": "#eeeeee", "Main": "#ffd58a"}


def rh_folder(module):
    # Lemmata/ holds about 150 folders of one theorem each: one box for all of them.
    parts = module.split(".")
    return parts[0] if parts[0] == "Lemmata" else ".".join(parts[:2])


def grh_folder(module):
    # The folder of the source file (Lib.Adelic.Adeles, New.Selmer, ...).
    parts = module.split(".")
    return ".".join(parts[:-1]) if len(parts) > 1 else module


PROJECTS = {
    "riemannHypothesis": dict(
        repo="leanprover-community/riemann-hypothesis", src="src",
        dirs=["CompanionTheory", "Development", "Formalism", "GroundTheory", "Lemmata",
              "PositivityTheory", "ReciprocityTheory"],
        color=RH_COLOR, folder=rh_folder, depth=4, min_block=2000),
    "grh": dict(
        repo="lsernau/grh-lean", src="grh/src", dirs=["Lib", "New"],
        color=GRH_COLOR, folder=grh_folder, depth=4, min_block=100),
    "grhCompact": dict(
        repo="lsernau/grh-lean", src="grh-compact/src", dirs=["Lib", "New"],
        color=GRH_COLOR, folder=grh_folder, depth=4, min_block=20),
}


def load(src):
    """Read <src>/b.*.tsv. Returns (info, used, lines):
      info[name]  (name without private prefix, kind, module)
      used[name]  the constants it uses (any, not only those in info)
      lines[name] first and last line in its source file, when recorded

    A name folded from a helper in another module (`foo.match_1` next to `foo`)
    appears in more than one batch: the lines are merged. A name that only ever
    comes from such helpers has kind "?" and is not a declaration of the project:
    it is a Mathlib lemma like `mul_assoc`, whose `mul_assoc._simp_1` a module
    generated for its own use. Those names are dropped."""
    info, used, lines = {}, collections.defaultdict(set), {}
    for f in sorted(glob.glob(os.path.join(src, "b.*.tsv"))):
        for line in open(f):
            name, user, kind, mod, us, first, last = line.rstrip("\n").split("\t")
            if name not in info or info[name][1] == "?":
                info[name] = (user, kind, mod)
            if first != "0":
                lines[name] = (int(first), int(last))
            used[name].update(us.split())
    for n in [n for n, v in info.items() if v[1] == "?"]:
        del info[n], used[n]
    return info, used, lines
