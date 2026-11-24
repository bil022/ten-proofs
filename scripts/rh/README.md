# Dependency graphs of the Riemann Hypothesis formalization

[中文版](README.zh.md)

These graphs are for
[leanprover-community/riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis),
the Lean formalization of the 2026 proof of the Riemann Hypothesis and of GRH for
Dirichlet L-functions. They were made from commit
[`6c68212`](https://github.com/leanprover-community/riemann-hypothesis/commit/6c6821263d6b80f4ec3d7479b0159340c1b2f65e)
of its `main` branch (24 November 2026).

## Why three small graphs instead of one big one

Each of the ten proofs in this repository is one Lean file. The Riemann
Hypothesis formalization is 60,928 files and 16.9 million lines. The five theorems
of its `Main.lean` (`riemannHypothesis` and four variants) rest on:

| | |
|---|---:|
| declarations | 727,065 |
| of which theorems | 568,159 |
| arrows between them | 9,827,858 |
| Lean files they come from | 58,519 |

A picture with half a million boxes cannot be drawn or read, so there are two
smaller ones, each showing the proof a different way:

| Graph | What a box is | Boxes | English | 中文 |
|---|---|---:|---|---|
| The top of the proof | a theorem | 395 | [SVG](../en/svg/riemannHypothesis.svg) · [PDF](../en/pdf/riemannHypothesis.pdf) · [PNG](../en/png/riemannHypothesis.png) | [SVG](../zh/svg/riemannHypothesis.zh.svg) · [PDF](../zh/pdf/riemannHypothesis.zh.pdf) · [PNG](../zh/png/riemannHypothesis.zh.png) |
| The whole proof by folder | a source folder | 149 | [SVG](../en/svg/riemannHypothesis_folders.svg) · [PDF](../en/pdf/riemannHypothesis_folders.pdf) · [PNG](../en/png/riemannHypothesis_folders.png) | [SVG](../zh/svg/riemannHypothesis_folders.zh.svg) · [PDF](../zh/pdf/riemannHypothesis_folders.zh.pdf) · [PNG](../zh/png/riemannHypothesis_folders.zh.png) |
| The whole proof in self-contained blocks | a sub-proof and everything only it uses | 194 | [SVG](../en/svg/riemannHypothesis_blocks.svg) · [PDF](../en/pdf/riemannHypothesis_blocks.pdf) · [PNG](../en/png/riemannHypothesis_blocks.png) | [SVG](../zh/svg/riemannHypothesis_blocks.zh.svg) · [PDF](../zh/pdf/riemannHypothesis_blocks.zh.pdf) · [PNG](../zh/png/riemannHypothesis_blocks.zh.png) |

### The top of the proof

The theorems at most four steps away from the five theorems of `Main.lean`,
drawn like the other graphs in this folder: orange for the five main theorems,
solid arrows for direct citations, dashed arrows for dependencies through a
definition (see [../README.md](../README.md#solid-and-dashed-arrows)).

The new colour is **grey**: a grey box is a theorem whose proof uses further
theorems that are not drawn. The 119 grey boxes are where the picture stops,
not where the proof does.

### The whole proof by folder

One box per folder of `src/`, two levels deep (`Formalism/LocalToGlobal`,
`Development/WeilBound`, …), with the number of theorems from that folder that
the proof needs. The 145 folders under `Lemmata/`, one theorem each, are drawn as a
single box. An arrow from folder `A` to folder `B` means some declaration in
`B` uses one in `A`. The colour is the top-level folder.

Unlike theorems, folders can depend on each other in both directions, so this
graph has cycles and is not read strictly left to right. One folder,
`Development/AbelianVarietyTheory`, holds 248,910 of the 568,159 theorems.

[folders.tsv](folders.tsv) lists each folder with its theorems, definitions and
Lean files.

### The whole proof in self-contained blocks

Folders are how the authors filed the code, not necessarily how the proof is
built. This graph cuts the proof along its own structure instead.

Say a declaration `D` *belongs to* theorem `X` when every chain of dependencies
from the main theorems down to `D` passes through `X`. Then `D` is used only
inside the proof of `X`: delete `X` and nothing else needs `D`. (In graph theory,
`X` dominates `D`.) Every declaration belongs to a nearest such theorem, so the
whole proof forms a tree.

A **block** is a theorem with at least 2,000 declarations belonging to it,
together with everything that belongs to it and not to a smaller block. Each
box is a block, labelled with its theorem and the number of declarations of its
own. An arrow from block `A` to block `B` means `A` is part of the proof of `B`.
The main theorems are on the right; moving left goes deeper into ever more
self-contained sub-proofs.

What the cut shows:

- **Half the proof is shared.** The three largest blocks,
  `everyCharacter`, `nonempty_hyps_definite_side_of_closed_bound` and
  `every_character_of_literature_of_vWin`, hold 349,020 declarations of their
  own, 48% of the proof. These are not one argument each: they are pools of
  lemmas used by several branches below them, so they belong to no smaller block.
- **50 blocks are leaves**, self-contained sub-proofs of 2,000 to 12,000
  declarations with no smaller block inside. Together they hold 150,195
  declarations of their own. These are the parts that can be read on their own.

Only the tree is drawn. A block also uses lemmas from the shared pools of the
blocks above it; drawing those uses would add arrows pointing right to left and
turn the tree into a tangle.

[blocks.tsv](blocks.tsv) lists each block with its parent, the declarations of
its own and the declarations in its whole subtree. `rh_blocks.py <dir> <out> N`
cuts at blocks of at least `N` declarations instead of 2,000.

## Explorer website

[`site/`](site/) is a small website for going through the whole proof level by
level, on the same tree as the block graph but without a size cut-off: every
declaration with anything that belongs to it has its own page, 173,224 pages in
all. It is published at <https://bil022.github.io/riemann-explorer/> from the
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
  or the path at the top, leads back up. The search box finds any of the 727,065
  declarations by name.
- **Lean source.** Clicking a part with nothing inside it opens its Lean code
  under the graph, with line numbers and a link to the same lines on GitHub; the
  "Lean source" button does the same for any part. The code is read from GitHub
  at the commit above, so this needs an internet connection. The line numbers
  come from the `.olean` files, which record them for 725,404 of the 727,065
  declarations; the others are looked up by name in the file.
- Interface in Chinese and English.

The data, 54 MB in `site/data/`, is written by `rh_site.py`. It is not kept in
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

## Regenerating

```bash
git clone https://github.com/leanprover-community/riemann-hypothesis
cd riemann-hypothesis
lake exe cache get        # downloads the compiled project, about 85 GB
cd -
scripts/rh/rh_all.sh path/to/riemann-hypothesis
```

`lake exe cache get` needs `python3` 3.11 or newer on the `PATH`. On a system
whose CA bundle is not at `/etc/ssl/certs/ca-certificates.crt` (Red Hat and
similar), also set `CURL_CA_BUNDLE=/etc/ssl/certs/ca-bundle.crt`.

The run takes about ten minutes and roughly 15 GB of memory for each of the 16
batches, read in parallel. Graphviz and rsvg-convert are needed as for `../run_all.sh`.

| File | What it does |
|---|---|
| `RHRead.lean` | Reads a batch of compiled modules and prints each declaration with what it uses. |
| `rh_cone.py` | Joins the batches and writes the first two graphs and `folders.tsv`. |
| `domtree.py` | Computes the dominator tree, for `rh_blocks.py` and `rh_site.py`. |
| `rh_blocks.py` | Writes the block graph and `blocks.tsv`. |
| `rh_site.py` | Writes the data of the explorer website. |
| `site/` | The explorer website: `index.html`, `app.js`, `style.css`. |
| `publish_site.sh` | Copies `site/` into a clone of bil022/riemann-explorer. |
| `rh_all.sh` | Runs all of these, then renders the English and Chinese SVG, PDF and PNG. |
