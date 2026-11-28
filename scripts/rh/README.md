# Dependency graphs of the Lean proofs of the Riemann Hypothesis

[中文版](README.zh.md)

There are now three Lean proofs of the Riemann Hypothesis and of GRH for
Dirichlet L-functions. All three prove the same five theorems in their
`Main.lean` (`riemannHypothesis` and four variants, with the same statements),
using only the axioms `propext`, `Classical.choice` and `Quot.sound`:

- **The first proof**,
  [leanprover-community/riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis),
  from commit
  [`6c68212`](https://github.com/leanprover-community/riemann-hypothesis/commit/6c6821263d6b80f4ec3d7479b0159340c1b2f65e)
  (24 November 2026). Output files are named `riemannHypothesis*`.
- **Two shorter rewrites** of it in
  [lsernau/grh-lean](https://github.com/lsernau/grh-lean), from commit
  [`72fead1`](https://github.com/lsernau/grh-lean/commit/72fead102f663d5c7a407964a13dc0cf9d977207)
  (25 November 2026): the *readable edition* in its folder `grh/` (files
  `grh*`) and the *compact edition* in `grh-compact/` (files `grhCompact*`).
  They follow the first proof's method, with many steps proved by other
  arguments. We built both here (Lean v4.35.0) with no errors and no `sorry`,
  and `#print axioms` lists only the three axioms above for all five theorems.
  Only machines have checked them; no mathematician has read them through.

| | First proof | Readable `grh` | Compact `grh-compact` |
|---|---:|---:|---:|
| Lean files | 60,928 | 805 | 796 |
| Lines | 16.9 million | 477,151 | 112,854 |
| Declarations the five theorems need | 727,065 | 21,597 | 12,533 |
| of which theorems | 568,159 | 17,156 | 8,802 |
| Arrows between them | 9,827,858 | 382,345 | 233,095 |
| Lean files they come from | 58,519 | 706 | 794 |

The compact edition is about 150 times shorter than the first proof, and its
proof needs 58 times fewer declarations.

## About the proof

What is known about how the proof works and how it was found comes from a
four-page note by Levent Alpöge, <https://alpo.ge/remark.pdf>. It is not a
paper. In summary:

- **The claim.** "I believe I have, working with Claude, discovered a proof of
  the Riemann Hypothesis." The method also gives GRH, and he expects it to
  reach the Extended Riemann Hypothesis. The argument is formalized in Lean
  "without assumptions"; the first proof above is that formalization.
- **The idea, in outline.** The proof descends from Stepanov's method, which
  proves the Riemann Hypothesis over function fields with an auxiliary divisor
  of high multiplicity. Over the integers multiplicity is hard to find
  ("something like differentiating whole numbers"). Here it is imitated by a
  chain of theta lifts, each lift adding one to the multiplicity. For a von
  Mangoldt sum of length X the chain has length √X, a choice he credits to
  Claude.
- **A timeline of 20 steps**, from 6 October 2026 (the "Stepanov determinant")
  to 16 November 2026 (GRH), names the main ingredients: the Guinand–Weil
  explicit formula, CM curves, iterated theta lifts between totally definite
  unitary groups, Chowla–Selberg and the Siegel mass formula, the seesaw
  identity, the Bost slope inequality, an Iwasawa tower, a relative trace
  formula, a weak form of Vandiver's conjecture, and Behrend's construction.
  The timeline was written by Claude and is very compressed. Where Claude was
  the expert, he says, he is paraphrasing its summary, which "might make zero
  sense".
- **Who did what.** He combined two ideas from a toy setting and led the work
  to the analogous situation for the integers; after that Claude "far
  outpaced me near the finish line", with "tens" of steps like the √X one. He
  says he has little mastery of automorphic forms on higher rank groups. The
  note does not say which tools, models or workflow were used.
- **Why only Lean.** Claude also wrote a human-readable version of more than
  250,000 pages. He judged it unreadable and published only the Lean code. He
  writes that he has not yet mastered the mathematics around the argument,
  expects it to be greatly simplified soon, and intends to write it up
  properly.
- **Checking.** The note mentions no referee and no mathematician who has read
  the argument through; the few mathematicians he consulted advised on how to
  announce it.

So the result is public and machine-checked, the mathematical route is known
only in outline, and how it was found is described only in general terms. The
two rewrites in lsernau/grh-lean came later, made by people at Anthropic with
Claude; their README does not say how either.

## Why three small graphs instead of one big one

Each of the ten proofs in this repository is one Lean file. Even the compact
edition has 12,533 declarations: too many for one readable picture. So each
proof gets three smaller ones, each showing it a different way:

| Graph | What a box is | First proof | `grh` | `grh-compact` |
|---|---|---:|---:|---:|
| The top of the proof | a theorem | 395 | 208 | 660 |
| The whole proof by folder | a source folder | 149 | 125 | 155 |
| The whole proof in self-contained blocks | a sub-proof and everything only it uses | 194 | 124 | 75 |

| Graph | English | 中文 |
|---|---|---|
| First proof, top | [SVG](../en/svg/riemannHypothesis.svg) · [PDF](../en/pdf/riemannHypothesis.pdf) · [PNG](../en/png/riemannHypothesis.png) | [SVG](../zh/svg/riemannHypothesis.zh.svg) · [PDF](../zh/pdf/riemannHypothesis.zh.pdf) · [PNG](../zh/png/riemannHypothesis.zh.png) |
| First proof, folders | [SVG](../en/svg/riemannHypothesis_folders.svg) · [PDF](../en/pdf/riemannHypothesis_folders.pdf) · [PNG](../en/png/riemannHypothesis_folders.png) | [SVG](../zh/svg/riemannHypothesis_folders.zh.svg) · [PDF](../zh/pdf/riemannHypothesis_folders.zh.pdf) · [PNG](../zh/png/riemannHypothesis_folders.zh.png) |
| First proof, blocks | [SVG](../en/svg/riemannHypothesis_blocks.svg) · [PDF](../en/pdf/riemannHypothesis_blocks.pdf) · [PNG](../en/png/riemannHypothesis_blocks.png) | [SVG](../zh/svg/riemannHypothesis_blocks.zh.svg) · [PDF](../zh/pdf/riemannHypothesis_blocks.zh.pdf) · [PNG](../zh/png/riemannHypothesis_blocks.zh.png) |
| `grh`, top | [SVG](../en/svg/grh.svg) · [PDF](../en/pdf/grh.pdf) · [PNG](../en/png/grh.png) | [SVG](../zh/svg/grh.zh.svg) · [PDF](../zh/pdf/grh.zh.pdf) · [PNG](../zh/png/grh.zh.png) |
| `grh`, folders | [SVG](../en/svg/grh_folders.svg) · [PDF](../en/pdf/grh_folders.pdf) · [PNG](../en/png/grh_folders.png) | [SVG](../zh/svg/grh_folders.zh.svg) · [PDF](../zh/pdf/grh_folders.zh.pdf) · [PNG](../zh/png/grh_folders.zh.png) |
| `grh`, blocks | [SVG](../en/svg/grh_blocks.svg) · [PDF](../en/pdf/grh_blocks.pdf) · [PNG](../en/png/grh_blocks.png) | [SVG](../zh/svg/grh_blocks.zh.svg) · [PDF](../zh/pdf/grh_blocks.zh.pdf) · [PNG](../zh/png/grh_blocks.zh.png) |
| `grh-compact`, top | [SVG](../en/svg/grhCompact.svg) · [PDF](../en/pdf/grhCompact.pdf) · [PNG](../en/png/grhCompact.png) | [SVG](../zh/svg/grhCompact.zh.svg) · [PDF](../zh/pdf/grhCompact.zh.pdf) · [PNG](../zh/png/grhCompact.zh.png) |
| `grh-compact`, folders | [SVG](../en/svg/grhCompact_folders.svg) · [PDF](../en/pdf/grhCompact_folders.pdf) · [PNG](../en/png/grhCompact_folders.png) | [SVG](../zh/svg/grhCompact_folders.zh.svg) · [PDF](../zh/pdf/grhCompact_folders.zh.pdf) · [PNG](../zh/png/grhCompact_folders.zh.png) |
| `grh-compact`, blocks | [SVG](../en/svg/grhCompact_blocks.svg) · [PDF](../en/pdf/grhCompact_blocks.pdf) · [PNG](../en/png/grhCompact_blocks.png) | [SVG](../zh/svg/grhCompact_blocks.zh.svg) · [PDF](../zh/pdf/grhCompact_blocks.zh.pdf) · [PNG](../zh/png/grhCompact_blocks.zh.png) |

### The top of the proof

The theorems at most four steps away from the five theorems of `Main.lean`,
drawn like the other graphs in this folder: orange for the five main theorems,
solid arrows for direct citations, dashed arrows for dependencies through a
definition (see [../README.md](../README.md#solid-and-dashed-arrows)).

The new colour is **grey**: a grey box is a theorem whose proof uses further
theorems that are not drawn. The grey boxes (119 for the first proof, 79 for
`grh`, 189 for `grh-compact`) are where the picture stops, not where the proof
does.

### The whole proof by folder

One box per source folder, with the number of theorems from that folder that
the proof needs. An arrow from folder `A` to folder `B` means some declaration in
`B` uses one in `A`. The colour is the top-level folder.

- **First proof:** folders of `src/` two levels deep (`Formalism/LocalToGlobal`,
  `Development/WeilBound`, …). The 145 folders under `Lemmata/`, one theorem
  each, are drawn as a single box.
- **`grh` and `grh-compact`:** the folder of each source file
  (`Lib/Adelic/Adeles`, `New/Selmer`, …). Blue is `Lib/`, background results
  that Mathlib lacks; pink is `New/`, the argument itself.

Unlike theorems, folders can depend on each other in both directions, so this
graph has cycles and is not read strictly left to right. In the first proof one
folder, `Development/AbelianVarietyTheory`, holds 248,910 of the 568,159
theorems. The rewrites are spread more evenly: the largest folders hold 703
theorems (`New/Spanning/Unfolding` in `grh`) and 407 (`New/Filling` in
`grh-compact`).

[riemannHypothesis_folders.tsv](riemannHypothesis_folders.tsv),
[grh_folders.tsv](grh_folders.tsv) and
[grhCompact_folders.tsv](grhCompact_folders.tsv) list each folder with its
theorems, definitions and Lean files.

### The whole proof in self-contained blocks

Folders are how the authors filed the code, not necessarily how the proof is
built. This graph cuts the proof along its own structure instead.

Say a declaration `D` *belongs to* theorem `X` when every chain of dependencies
from the main theorems down to `D` passes through `X`. Then `D` is used only
inside the proof of `X`: delete `X` and nothing else needs `D`. (In graph theory,
`X` dominates `D`.) Every declaration belongs to a nearest such theorem, so the
whole proof forms a tree.

A **block** is a theorem with at least a set number of declarations belonging
to it (2,000 for the first proof, 100 for `grh`, 20 for `grh-compact`),
together with everything that belongs to it and not to a smaller block. Each
box is a block, labelled with its theorem and the number of declarations of its
own. An arrow from block `A` to block `B` means `A` is part of the proof of `B`.
The main theorems are on the right; moving left goes deeper into ever more
self-contained sub-proofs.

What the cut shows in the first proof:

- **Half the proof is shared.** The three largest blocks,
  `everyCharacter`, `nonempty_hyps_definite_side_of_closed_bound` and
  `every_character_of_literature_of_vWin`, hold 349,020 declarations of their
  own, 48% of the proof. These are not one argument each: they are pools of
  lemmas used by several branches below them, so they belong to no smaller block.
- **50 blocks are leaves**, self-contained sub-proofs of 2,000 to 12,000
  declarations with no smaller block inside. Together they hold 150,195
  declarations of their own. These are the parts that can be read on their own.

The rewrites are shared even more:

- **`grh`:** the three largest blocks, `New.star_inequality`,
  `New.eventually_primeRemainder_natCast_le` and
  `New.Selmer.exists_mFoldTwist_hasDenominatorsLe`, hold 11,641 declarations
  of their own, 54% of the proof. Its 26 leaves hold 101 to 195 declarations
  each.
- **`grh-compact`:** the three largest, `star_inequality`,
  `eventually_primeError_le_rpow` and `Model.exists_galois_rep`, hold 8,076,
  64% of the proof; `star_inequality` alone has 5,258. Its 29 leaves hold 20
  to 86 declarations each. Shortening the proof mostly removed the
  self-contained sub-proofs and kept the lemmas that many steps share.

Only the tree is drawn. A block also uses lemmas from the shared pools of the
blocks above it; drawing those uses would add arrows pointing right to left and
turn the tree into a tangle.

[riemannHypothesis_blocks.tsv](riemannHypothesis_blocks.tsv),
[grh_blocks.tsv](grh_blocks.tsv) and [grhCompact_blocks.tsv](grhCompact_blocks.tsv)
list each block with its parent, the declarations of its own and the
declarations in its whole subtree. `rh_blocks.py <project> <dir> <out> N` cuts
at blocks of at least `N` declarations instead.

## Explorer website

[`site/`](site/) is a small website for going through a whole proof level by
level, on the same tree as the block graph but without a size cut-off: every
declaration with anything that belongs to it has its own page (173,224 pages
for the first proof, 3,936 for `grh`, 772 for `grh-compact`). It opens on the
compact edition; the menu at the top left switches between the three proofs.
Addresses without a proof name
(`#123`) are pages of the first proof, so earlier links still work; the others
start with the proof's name (`#grhCompact/123`). It is published at <https://bil022.github.io/riemann-explorer/> from the
repository [bil022/riemann-explorer](https://github.com/bil022/riemann-explorer);
`publish_site.sh <clone of it>` copies `site/` there. To run it locally:

```bash
python3 -m http.server -d scripts/rh/site 8000
```

and open <http://localhost:8000>. (Opening `index.html` directly from disk does
not work: browsers do not let a page read data files from `file://`.)

- **A page** shows one declaration (orange) and the parts that belong directly
  to it. Each part is a box with its name and the number of declarations in it;
  darker blue means larger. The 40 largest parts are drawn, and all of them are
  listed in the table on the right.
- **Shared groups.** The parts not drawn are mostly lemmas shared by several of
  the drawn parts (that is why they belong to no single one of them). They are
  grouped by which drawn parts use them, directly or through other parts not
  drawn: "shared by A and B", "shared by A, B and 3 more", and so on. The 10
  largest groups are dashed boxes with arrows to the parts that use them. Click
  one for a summary (how many theorems and definitions, lines of code, its 10
  most used and 10 largest members) and to list only its members.
- **Table columns:** declarations in the part's subtree, children, how many
  declarations use it directly ("Users"), and its lines of code. Sort by Users
  to find the core notions. On the page of `everyCharacter`, for instance,
  47,234 parts fall into 711 groups, the largest being 14,818 parts shared by
  just its two main branches.
- **Arrows** point from a part to the part that uses it, thicker for more uses.
  Arrows implied by a longer path are hidden unless the box at the bottom right
  is ticked.
- **Click** a box to open its page. The **↑ Up** button next to the orange box,
  or the path at the top, leads back up. The search box finds any declaration of
  the proof shown by name.
- **Lean source.** Clicking a part with nothing inside it opens its Lean code
  under the graph, with line numbers and a link to the same lines on GitHub; the
  "Lean source" button does the same for any part. The code is read from GitHub
  at the commit above, so this needs an internet connection. The line numbers
  come from the `.olean` files, which record them for almost every declaration
  (725,404 of 727,065 in the first proof); the others are looked up by name in
  the file.
- Interface in Chinese and English.

The data, in `site/data/<project>/` (54 MB for the first proof, 1.5 MB for
`grh`, 0.7 MB for `grh-compact`), is written by `rh_site.py`. It is not kept in
this repository (see `.gitignore`), only in bil022/riemann-explorer: run
`rh_all.sh` to make it. The page uses
[Cytoscape.js](https://js.cytoscape.org/) with the dagre layout, copied into
`site/vendor/` with their MIT licences, so it works offline.

### Chinese labels

Translated word by word from [../glossary.zh.txt](../glossary.zh.txt), as for the
other graphs. Many words of this project (`Automorphic`, `Reciprocity`, …) are
not in the glossary yet and stay in English.

## How the graphs are made

The method is that of `../DeclGraph.lean` and `../cone.py`: read the compiled
`.olean` files, fold Lean's auxiliary constants (`foo._proof_1`, `foo.match_1`,
constructors, recursors) into the declaration they belong to, and follow what
each declaration uses. Two things differ:

- **Many modules.** `DeclGraph.lean` follows dependencies inside one module;
  `RHRead.lean` follows them across every module of the project, ignoring
  Mathlib and Lean itself.
- **No single import.** Importing all 60,928 modules at once maps about 180,000
  files into memory, more than Linux allows by default
  (`vm.max_map_count` = 65,530), and raising the limit needs root. So
  `rh_all.sh` reads the modules in 16 batches, one Lean process each, and
  `rh_cone.py` joins the results.

A declaration name that only appears through a helper Lean generated for its
own use (`mul_assoc._simp_1` in some module of the project) is a Mathlib lemma,
not part of the project, and is dropped. The first proof's graphs were made
before this rule; in a proof of 727,065 declarations it makes no visible
difference, but in `grh-compact` it removed 581 such names.

## Regenerating

The first argument of `rh_all.sh` names the proof (a key of
[`projects.py`](projects.py), which also holds each proof's settings); the second
is its built Lake project.

```bash
# The first proof: the project cache is enough.
git clone https://github.com/leanprover-community/riemann-hypothesis
cd riemann-hypothesis
lake exe cache get        # downloads the compiled project, about 85 GB
cd -
scripts/rh/rh_all.sh riemannHypothesis path/to/riemann-hypothesis

# The rewrites: build them first (one to two hours each, 24 GB of memory).
git clone https://github.com/lsernau/grh-lean
(cd grh-lean/grh-compact && lake exe cache get && lake build)
scripts/rh/rh_all.sh grhCompact grh-lean/grh-compact
(cd grh-lean/grh && lake exe cache get && lake build)
scripts/rh/rh_all.sh grh grh-lean/grh
```

`lake exe cache get` needs `python3` 3.11 or newer on the `PATH`. On a system
whose CA bundle is not at `/etc/ssl/certs/ca-certificates.crt` (Red Hat and
similar), also set `CURL_CA_BUNDLE=/etc/ssl/certs/ca-bundle.crt`.

For the first proof the run takes about ten minutes and roughly 15 GB of memory
for each of the 16 batches, read in parallel; for the rewrites, under a minute. Graphviz and rsvg-convert are needed as for `../run_all.sh`.

| File | What it does |
|---|---|
| `projects.py` | The three proofs and their settings; reads the batches for the scripts below. |
| `RHRead.lean` | Reads a batch of compiled modules and prints each declaration with what it uses. |
| `rh_cone.py` | Writes the first two graphs of a proof and `<project>_folders.tsv`. |
| `domtree.py` | Computes the dominator tree, for `rh_blocks.py` and `rh_site.py`. |
| `rh_blocks.py` | Writes the block graph and `<project>_blocks.tsv`. |
| `rh_site.py` | Writes the data of the explorer website. |
| `site/` | The explorer website: `index.html`, `app.js`, `style.css`. |
| `publish_site.sh` | Copies `site/` into a clone of bil022/riemann-explorer. |
| `rh_all.sh` | Runs all of these, then renders the English and Chinese SVG, PDF and PNG. |
