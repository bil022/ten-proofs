# Proof dependency graphs

[中文版](README.zh.md)

The ten Lean files in this repository are hard to read. The shortest is about
3,000 lines and the longest about 130,000, each one a flat list of hundreds or
thousands of lemmas with long generated-looking names. Reading a file from top to
bottom tells you very little about how the argument is organised: which lemmas
are the foundations, which are the key intermediate results, and which ones the
main theorem actually rests on.

A picture helps. This folder turns each proof into a dependency graph: one box
per theorem, and an arrow from `A` to `B` whenever `B` uses `A`. Starting from
the main theorem and following the arrows backwards shows the skeleton of the
proof without reading a single tactic.

## How to read a graph

- **One box is one theorem.** Definitions are left out to keep the picture readable.
- **The orange box is the main theorem.** It is the only box with no outgoing arrow.
- **Arrows point from what is used to what uses it.** The graph reads left to
  right, from basic lemmas to the conclusion.
- **Boxes with no incoming arrow are the leaves.** They depend only on Mathlib
  and on definitions.
- **Arrows implied by a longer path are removed.** If `A → B → C`, a direct
  `A → C` arrow is not drawn.

### Solid and dashed arrows

- **Solid, `A → B`:** the proof of `B` cites theorem `A` directly.
- **Dashed, `A ⇢ B`:** `B` depends on `A` through a definition. Some definition
  is built using `A`, and `B` uses that definition, but `B` never names `A`.

Dashed arrows exist because definitions are hidden. Without them, a theorem that
is used only inside a definition would look disconnected from the rest.

A small example:

```lean
theorem two_is_pos : 0 < 2 := by decide

-- a definition that needs the theorem above to be well-formed
def myTwo : {n : ℕ // 0 < n} := ⟨2, two_is_pos⟩

-- uses the definition `myTwo`, never mentions `two_is_pos`
theorem myTwo_ne_zero : myTwo.val ≠ 0 :=
  Nat.pos_iff_ne_zero.mp myTwo.property

-- cites `two_is_pos` directly
theorem four_is_pos : 0 < 2 + 2 :=
  Nat.add_pos_left two_is_pos 2
```

```
two_is_pos ──────▶ four_is_pos      solid   (cited in the proof)
two_is_pos ─ ─ ─ ▶ myTwo_ne_zero    dashed  (through the definition myTwo)
```

Both kinds are real dependencies: remove the theorem at the tail of either arrow
and the one at the head no longer compiles.

## The graphs

| Lean file | Main theorem (file name of the graph) | Theorems | Arrows |
|---|---|---:|---:|
| `MulticolorTriangleRamsey` | `erdos_problem_183_explicit` | 95 | 114 |
| `Permanent` | `permanent_rational_formula_logarithmic_lower_bound` | 247 | 330 |
| `CompactnessAndDegeneracy` | `twoDegenerateExtremalCounterexample` | 309 | 449 |
| `CompactnessAndDegeneracy` | `quantitativeCompactnessCounterexample` | 355 | 573 |
| `NonSoficGroup` | `exists_finitelyPresented_nonsofic_group` | 1,109 | 1,795 |
| `SpherePacking` | `sharpFullCohnElkiesManuscriptConclusions` | 1,648 | 2,591 |
| `ConnesRigidity` | `exists_infinite_pairwise_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors` | 1,710 | 2,638 |
| `QuantumParallelRepetition` | `distributionUniformExponential` | 1,816 | 3,870 |
| `EhrhartVolumeInequality` | `ehrhart_volume_inequality_for_sets` | 1,862 | 3,325 |
| `MetricCodes` | `binaryRate_lt_mrrw` | 2,468 | 4,824 |
| `GapCVP` | `gapCVP400IsNPHard` | 3,522 | 21,490 |
| `MetricCodes` | `strict_hierarchy` | 3,569 | 7,181 |

The first four are small enough to read on screen. The other eight are very
large pictures: their PDFs exceed the 14,400 pt page limit of Adobe Acrobat and
may not open there. Open the SVG in a web browser instead, zoom in, and use the
browser's search to find a theorem by name.

## What is in this folder

| Folder | Contents |
|---|---|
| `en/svg`, `en/pdf`, `en/png` | The graphs, with the original theorem names. |
| `en/dot` | The same graphs in Graphviz DOT format. |
| `zh/svg`, `zh/pdf`, `zh/png`, `zh/dot` | The graphs with a Chinese label above each name. |
| `zh/names` | The Chinese label of every theorem, one table per graph. |
| `lean` | For each main theorem, a Lean file with only what it needs, plus the compile log. |
| `modules` | The full dependency graph and source line numbers of each Lean file. |

The PNGs are at most 8,000 pixels on the longer side. That keeps the text
legible in the four small graphs; the eight large ones are scaled down so far
that the PNG only shows the overall shape, and the SVG is the one to read.

`en/svg/MulticolorTriangleRamsey.svg` is the one whole-file graph, with
definitions (green) as well as theorems (blue).

### The extracted Lean files

Each file in `lean/` is the original source with every declaration the main
theorem does not need cut out. All twelve compile on their own with no errors,
no `sorry`, and only the standard axioms `propext`, `Classical.choice` and
`Quot.sound`.

They are not strictly minimal. Type-class instances, `@[simp]`-tagged lemmas and
tactic macros shape how Lean reads a proof without appearing in the finished
proof, so they are all kept. How much is left varies: `Permanent` shrinks from
27,563 lines to 6,741, while `NonSoficGroup` uses every declaration it has.

### The Chinese labels

The labels of `erdos_problem_183_explicit` were translated by hand from the
theorem names. The other eleven graphs, about 18,600 names, are translated word
by word from `glossary.zh.txt`, so they read as a sequence of words, not as
sentences. Proper names and abbreviations stay in English.

## Regenerating

Run from the project root, after `lake build`:

```bash
scripts/run_all.sh              # graphs and extracted Lean files, all theorems
scripts/run_all.sh Permanent    # one Lean file only
scripts/zh_all.sh               # Chinese-labelled graphs
```

Requirements, installed once with conda:

```bash
conda create -n graphviz --override-channels -c conda-forge graphviz font-ttf-noto-cjk
```

A full run takes about an hour, most of it laying out the `GapCVP` graph.

| Script | What it does |
|---|---|
| `roots.tsv` | The Lean files and their main theorems. |
| `DeclGraph.lean` | Reads a compiled file and writes its full dependency graph. |
| `cone.py` | Cuts the full graph down to one theorem's dependencies. |
| `extract.py` | Writes a Lean file containing only what a theorem needs. |
| `check.py` | Runs the extraction, compiles the result, retries if a lemma must be added back. |
| `svg2png.sh` | Renders an SVG to PNG, at most 8,000 pixels on the longer side. |
| `run_all.sh` | Runs all of the above for every main theorem. |
| `zh_gloss.py`, `zh_labels.py`, `zh_all.sh` | Build the Chinese-labelled graphs. |
