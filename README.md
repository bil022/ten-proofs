# Ten Advances in Mathematics and Theoretical Computer Science

This repository contains Lean 4 formalizations of the results presented in
[Ten advances in mathematics and theoretical computer science](https://openai.com/index/ten-advances-in-mathematics/) by OpenAI.

- [Read the paper](https://cdn.openai.com/pdf/ten-proofs-oai.pdf)
- [Read the reasoning walkthroughs](https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf)

> This is a copy of [openai/ten-proofs](https://github.com/openai/ten-proofs)
> with one addition: a **dependency graph of every proof**, in the
> [`scripts/`](scripts/) folder. The Lean files themselves are unchanged.
>
> 本仓库是 [openai/ten-proofs](https://github.com/openai/ten-proofs) 的副本，只多了一样东西：
> **每个证明的依赖图**，放在 [`scripts/`](scripts/) 文件夹里。Lean 文件本身没有改动。

## Proof dependency graphs · 证明依赖图

The ten proofs are hard to read: each Lean file is between 3,000 and 130,000
lines, a flat list of hundreds or thousands of lemmas. The graphs below show how
each proof is organised. Every box is a theorem, and an arrow from `A` to `B`
means `B` uses `A`, so following the arrows leads from the basic lemmas on the
left to the main theorem (orange) on the right.

这十个证明很难读懂：每个 Lean 文件有 3,000 到 130,000 行，是几百到几千条引理的平铺罗列。
下面的图展示了每个证明是怎么组织的。每个方框是一个定理，从 `A` 指向 `B` 的箭头表示 `B` 用到了
`A`，所以顺着箭头看，就是从左边的基础引理走到右边的主定理（橙色）。

[![Dependency graph of the multicolor Ramsey proof](scripts/en/svg/erdos_problem_183_explicit.svg)](scripts/en/svg/erdos_problem_183_explicit.svg)

*The smallest graph: the 95 theorems behind the multicolor Ramsey bound. Click to enlarge.*
*最小的一张图：多色 Ramsey 下界背后的 95 个定理。点击可放大。*

| Result | Theorems | English | 中文 |
|---|---:|---|---|
| 1. Sphere packing | 1,648 | [SVG](scripts/en/svg/sharpFullCohnElkiesManuscriptConclusions.svg) · [PDF](scripts/en/pdf/sharpFullCohnElkiesManuscriptConclusions.pdf) · [PNG](scripts/en/png/sharpFullCohnElkiesManuscriptConclusions.png) | [SVG](scripts/zh/svg/sharpFullCohnElkiesManuscriptConclusions.zh.svg) · [PDF](scripts/zh/pdf/sharpFullCohnElkiesManuscriptConclusions.zh.pdf) · [PNG](scripts/zh/png/sharpFullCohnElkiesManuscriptConclusions.zh.png) |
| 2. Binary codes | 2,468 | [SVG](scripts/en/svg/binaryRate_lt_mrrw.svg) · [PDF](scripts/en/pdf/binaryRate_lt_mrrw.pdf) · [PNG](scripts/en/png/binaryRate_lt_mrrw.png) | [SVG](scripts/zh/svg/binaryRate_lt_mrrw.zh.svg) · [PDF](scripts/zh/pdf/binaryRate_lt_mrrw.zh.pdf) · [PNG](scripts/zh/png/binaryRate_lt_mrrw.zh.png) |
| 2. Spherical codes | 3,569 | [SVG](scripts/en/svg/strict_hierarchy.svg) · [PDF](scripts/en/pdf/strict_hierarchy.pdf) · [PNG](scripts/en/png/strict_hierarchy.png) | [SVG](scripts/zh/svg/strict_hierarchy.zh.svg) · [PDF](scripts/zh/pdf/strict_hierarchy.zh.pdf) · [PNG](scripts/zh/png/strict_hierarchy.zh.png) |
| 3. Non-sofic groups | 1,109 | [SVG](scripts/en/svg/exists_finitelyPresented_nonsofic_group.svg) · [PDF](scripts/en/pdf/exists_finitelyPresented_nonsofic_group.pdf) · [PNG](scripts/en/png/exists_finitelyPresented_nonsofic_group.png) | [SVG](scripts/zh/svg/exists_finitelyPresented_nonsofic_group.zh.svg) · [PDF](scripts/zh/pdf/exists_finitelyPresented_nonsofic_group.zh.pdf) · [PNG](scripts/zh/png/exists_finitelyPresented_nonsofic_group.zh.png) |
| 4. Connes’s rigidity conjecture | 1,710 | [SVG](scripts/en/svg/exists_infinite_pairwise_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors.svg) · [PDF](scripts/en/pdf/exists_infinite_pairwise_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors.pdf) · [PNG](scripts/en/png/exists_infinite_pairwise_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors.png) | [SVG](scripts/zh/svg/exists_infinite_pairwise_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors.zh.svg) · [PDF](scripts/zh/pdf/exists_infinite_pairwise_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors.zh.pdf) · [PNG](scripts/zh/png/exists_infinite_pairwise_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors.zh.png) |
| 5. Permanent lower bound | 247 | [SVG](scripts/en/svg/permanent_rational_formula_logarithmic_lower_bound.svg) · [PDF](scripts/en/pdf/permanent_rational_formula_logarithmic_lower_bound.pdf) · [PNG](scripts/en/png/permanent_rational_formula_logarithmic_lower_bound.png) | [SVG](scripts/zh/svg/permanent_rational_formula_logarithmic_lower_bound.zh.svg) · [PDF](scripts/zh/pdf/permanent_rational_formula_logarithmic_lower_bound.zh.pdf) · [PNG](scripts/zh/png/permanent_rational_formula_logarithmic_lower_bound.zh.png) |
| 6. Quantum parallel repetition | 1,816 | [SVG](scripts/en/svg/distributionUniformExponential.svg) · [PDF](scripts/en/pdf/distributionUniformExponential.pdf) · [PNG](scripts/en/png/distributionUniformExponential.png) | [SVG](scripts/zh/svg/distributionUniformExponential.zh.svg) · [PDF](scripts/zh/pdf/distributionUniformExponential.zh.pdf) · [PNG](scripts/zh/png/distributionUniformExponential.zh.png) |
| 7. Closest vector problem | 3,522 | [SVG](scripts/en/svg/gapCVP400IsNPHard.svg) · [PDF](scripts/en/pdf/gapCVP400IsNPHard.pdf) · [PNG](scripts/en/png/gapCVP400IsNPHard.png) | [SVG](scripts/zh/svg/gapCVP400IsNPHard.zh.svg) · [PDF](scripts/zh/pdf/gapCVP400IsNPHard.zh.pdf) · [PNG](scripts/zh/png/gapCVP400IsNPHard.zh.png) |
| 8. Ehrhart’s volume conjecture | 1,862 | [SVG](scripts/en/svg/ehrhart_volume_inequality_for_sets.svg) · [PDF](scripts/en/pdf/ehrhart_volume_inequality_for_sets.pdf) · [PNG](scripts/en/png/ehrhart_volume_inequality_for_sets.png) | [SVG](scripts/zh/svg/ehrhart_volume_inequality_for_sets.zh.svg) · [PDF](scripts/zh/pdf/ehrhart_volume_inequality_for_sets.zh.pdf) · [PNG](scripts/zh/png/ehrhart_volume_inequality_for_sets.zh.png) |
| 9. Multicolor Ramsey numbers | 95 | [SVG](scripts/en/svg/erdos_problem_183_explicit.svg) · [PDF](scripts/en/pdf/erdos_problem_183_explicit.pdf) · [PNG](scripts/en/png/erdos_problem_183_explicit.png) | [SVG](scripts/zh/svg/erdos_problem_183_explicit.zh.svg) · [PDF](scripts/zh/pdf/erdos_problem_183_explicit.zh.pdf) · [PNG](scripts/zh/png/erdos_problem_183_explicit.zh.png) |
| 10. Compactness conjecture | 355 | [SVG](scripts/en/svg/quantitativeCompactnessCounterexample.svg) · [PDF](scripts/en/pdf/quantitativeCompactnessCounterexample.pdf) · [PNG](scripts/en/png/quantitativeCompactnessCounterexample.png) | [SVG](scripts/zh/svg/quantitativeCompactnessCounterexample.zh.svg) · [PDF](scripts/zh/pdf/quantitativeCompactnessCounterexample.zh.pdf) · [PNG](scripts/zh/png/quantitativeCompactnessCounterexample.zh.png) |
| 10. Two-degenerate graphs | 309 | [SVG](scripts/en/svg/twoDegenerateExtremalCounterexample.svg) · [PDF](scripts/en/pdf/twoDegenerateExtremalCounterexample.pdf) · [PNG](scripts/en/png/twoDegenerateExtremalCounterexample.png) | [SVG](scripts/zh/svg/twoDegenerateExtremalCounterexample.zh.svg) · [PDF](scripts/zh/pdf/twoDegenerateExtremalCounterexample.zh.pdf) · [PNG](scripts/zh/png/twoDegenerateExtremalCounterexample.zh.png) |

- **Solid arrow:** the proof cites that theorem directly.
- **Dashed arrow:** the dependency goes through a definition that is not drawn.
- **Large graphs:** only results 5, 9 and 10 are small enough to read
  comfortably. The others have over a thousand theorems each, and GitHub may
  refuse to preview them; download the SVG and open it in a web browser, then
  zoom and search by name.
- **PNG:** at most 8,000 pixels wide or tall. Readable for results 5, 9 and 10;
  for the others it only shows the overall shape.
- **Chinese labels:** result 9 was translated by hand; the rest are translated
  word by word from a glossary.

How to read the graphs, what else is in the folder, and how to regenerate
everything: [scripts/README.md](scripts/README.md).

中文说明：

- **实线箭头：** 证明里直接引用了那个定理。
- **虚线箭头：** 依赖关系经过一个没有画出来的定义。
- **大图：** 只有第 5、9、10 项结果的图小到可以轻松阅读。其余每张都有上千个定理，GitHub
  可能无法预览；请下载 SVG 后用浏览器打开，再放大并按名字搜索。
- **PNG：** 长边最多 8,000 像素。第 5、9、10 项的图清晰可读；其余的只能看出整体形状。
- **中文标签：** 第 9 项是手工翻译的；其余是按词表逐词对译的。

怎么看图、文件夹里还有什么、如何重新生成：[scripts/README.zh.md](scripts/README.zh.md)。

### Explanations of the proofs · 证明讲解

The Lean files have no comments, so these write-ups explain what each proof does.
Lean 文件里没有注释，下面几份讲解说明每个证明在做什么。

| | English | 中文 |
|---|---|---|
| How each proof works, based on OpenAI's paper · 按论文讲解证明思路 | [proofs.md](scripts/proofs.md) | [proofs.zh.md](scripts/proofs.zh.md) |
| How each proof is organised, from the Lean code alone · 只看代码的总结 | [proofs-from-code.md](scripts/proofs-from-code.md) | [proofs-from-code.zh.md](scripts/proofs-from-code.zh.md) |
| The simplest "leaf" theorem of each proof, at high-school level · 每个证明最简单的叶子定理，高中水平 | [leaves.md](scripts/leaves.md) | [leaves.zh.md](scripts/leaves.zh.md) |

## The results

1. **High-dimensional sphere packing:** Improved asymptotic upper bounds on
   sphere-packing density, reaching the Cohn–Elkies threshold.
   ([`SpherePacking.lean`](SpherePacking.lean))
2. **Binary and spherical codes:** Exponentially stronger upper bounds for
   binary codes at every minimum distance, together with corresponding bounds
   for spherical codes. ([`MetricCodes.lean`](MetricCodes.lean))
3. **Non-sofic groups:** A construction of a non-sofic group, resolving whether
   every group admits finite permutation approximations.
   ([`NonSoficGroup.lean`](NonSoficGroup.lean))
4. **Connes’s rigidity conjecture:** A counterexample to the conjecture that
   certain groups are determined by their group von Neumann algebras.
   ([`ConnesRigidity.lean`](ConnesRigidity.lean))
5. **Arithmetic circuit complexity:** New lower bounds for computing the
   permanent with arithmetic circuits and formulas, including an
   $n^4 / \log n$ formula lower bound.
   ([`Permanent.lean`](Permanent.lean))
6. **Quantum parallel repetition:** Exponential parallel repetition for
   arbitrary finite, two-player quantum games.
   ([`QuantumParallelRepetition.lean`](QuantumParallelRepetition.lean))
7. **Closest vector problem:** Polynomial-factor hardness of approximation for
   the closest vector problem, with related consequences for decoding and
   lattice problems. ([`GapCVP.lean`](GapCVP.lean))
8. **Ehrhart’s volume conjecture:** The sharp maximum volume in every dimension
   for a convex body whose centroid is its only interior lattice point.
   ([`EhrhartVolumeInequality.lean`](EhrhartVolumeInequality.lean))
9. **Multicolor Ramsey numbers:** A superexponential lower bound for multicolor
   triangle Ramsey numbers, resolving Erdős problem 183.
   ([`MulticolorTriangleRamsey.lean`](MulticolorTriangleRamsey.lean))
10. **Extremal number conjectures:** Counterexamples to the compactness and
    degeneracy conjectures in extremal graph theory, resolving Erdős problems
    146 and 180.
    ([`CompactnessAndDegeneracy.lean`](CompactnessAndDegeneracy.lean))

## Building the formalizations

The project uses Lean 4.32.0, mathlib, and Lake. With
[elan](https://github.com/leanprover/elan) installed, fetch the mathlib cache
and build all ten formalizations with:

```sh
lake exe cache get
lake build All
```

To build an individual formalization, pass its module name to Lake:

```sh
lake build SpherePacking
```

## Independent proof checking

For instructions on checking the formalizations with Comparator, see the
[ComparatorChallenges README](ComparatorChallenges/README.md).
