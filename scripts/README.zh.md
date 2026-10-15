# 证明依赖图

[English](README.md)

这个仓库里的十个 Lean 文件很难读懂。最短的约 3,000 行，最长的约 130,000 行，
每个文件都是几百到几千条引理的平铺罗列，名字又长又像是机器生成的。从头读到尾，
几乎看不出论证是怎么组织的：哪些引理是基础，哪些是关键的中间结论，主定理到底
依赖哪些。

画成图会好很多。这个文件夹把每个证明变成一张依赖图：每个定理一个方框，只要 `B`
用到了 `A`，就画一条从 `A` 到 `B` 的箭头。从主定理出发，逆着箭头往回看，不用读
任何一行证明，就能看到整个证明的骨架。

## 怎么看图

- **一个方框是一个定理。** 为了让图清楚，定义没有画出来。
- **橙色方框是主定理。** 它是唯一没有向外箭头的方框。
- **箭头从"被使用的"指向"使用它的"。** 图从左往右读，左边是基础引理，右边是结论。
- **没有箭头指入的方框是叶子。** 它们只依赖 Mathlib 和定义。
- **可由更长路径推出的箭头已经去掉。** 如果有 `A → B → C`，就不再画 `A → C`。

### 实线和虚线

- **实线 `A → B`：** `B` 的证明里直接引用了定理 `A`。
- **虚线 `A ⇢ B`：** `B` 通过一个定义依赖 `A`。某个定义在构造时用到了 `A`，`B` 又用了
  这个定义，但 `B` 自己从来没有提到 `A`。

之所以需要虚线，是因为定义被隐藏了。没有虚线的话，一个只在定义里被用到的定理，
看起来就会和其他部分断开。

一个小例子：

```lean
theorem two_is_pos : 0 < 2 := by decide

-- 这个定义需要上面的定理才能成立
def myTwo : {n : ℕ // 0 < n} := ⟨2, two_is_pos⟩

-- 用到了定义 myTwo，但没有提到 two_is_pos
theorem myTwo_ne_zero : myTwo.val ≠ 0 :=
  Nat.pos_iff_ne_zero.mp myTwo.property

-- 直接引用了 two_is_pos
theorem four_is_pos : 0 < 2 + 2 :=
  Nat.add_pos_left two_is_pos 2
```

```
two_is_pos ──────▶ four_is_pos      实线（证明里直接引用）
two_is_pos ─ ─ ─ ▶ myTwo_ne_zero    虚线（经过定义 myTwo）
```

两种都是真实的依赖：去掉箭头尾部的定理，箭头头部的定理就编译不过了。

## 有哪些图

| Lean 文件 | 主定理（也是图的文件名） | 定理数 | 箭头数 |
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

前四张比较小，可以直接在屏幕上看。后八张非常大：它们的 PDF 超过了 Adobe Acrobat
每边 14,400 pt 的页面上限，在 Acrobat 里可能打不开。这时请用浏览器打开 SVG，放大
查看，并用浏览器的搜索功能按名字找定理。

## 文件夹里有什么

| 文件夹 | 内容 |
|---|---|
| `en/svg`、`en/pdf`、`en/png` | 依赖图，使用原始的定理名。 |
| `en/dot` | 同样的图，Graphviz DOT 格式。 |
| `zh/svg`、`zh/pdf`、`zh/png`、`zh/dot` | 每个名字上方加了中文标签的图。 |
| `zh/names` | 每个定理的中文标签，每张图一个表。 |
| `lean` | 每个主定理对应一个只包含它所需内容的 Lean 文件，以及编译日志。 |
| `modules` | 每个 Lean 文件的完整依赖图和源码行号。 |
| `proofs.zh.md`、`proofs-from-code.zh.md`、`leaves.zh.md` | 证明讲解：按论文讲、只看代码的总结、最简单的叶子定理（各有对应的英文 `.md` 版本）。 |
| `duplicates.tsv` | 陈述相同的定理、相同的定义和一行推论（由 `Duplicates.lean` 生成）。 |
| `library_use.tsv` | 每个 Lean 文件用到了哪些 Mathlib 常量（由 `LibraryUse.lean` 生成）。 |

PNG 的长边最多 8,000 像素。四张小图在这个尺寸下文字清晰可读；八张大图被缩得很小，
PNG 只能看出整体形状，要看内容请用 SVG。

`en/svg/MulticolorTriangleRamsey.svg` 是唯一一张整文件图，定理（蓝色）和定义
（绿色）都画了出来。

### 提取出的 Lean 文件

`lean/` 里的每个文件都是原始源码去掉主定理不需要的声明之后的结果。十二个文件都能
独立编译，没有错误，没有 `sorry`，只用到标准公理 `propext`、`Classical.choice` 和
`Quot.sound`。

它们不是严格最小的。类型类实例、带 `@[simp]` 标记的引理和策略宏会影响 Lean 如何
理解证明，却不出现在最终的证明里，所以全部保留。能删掉多少因文件而异：`Permanent`
从 27,563 行缩到 6,741 行，而 `NonSoficGroup` 用到了它的每一个声明。

### 中文标签

`erdos_problem_183_explicit` 的标签是根据定理名手工翻译的。其余十一张图约有
18,600 个名字，是按 `glossary.zh.txt` 逐词对译的，所以读起来是一串词，而不是通顺的
句子。人名和缩写保留英文。

## 重新生成

先运行 `lake build`，然后在项目根目录执行：

```bash
scripts/run_all.sh              # 所有主定理的图和提取出的 Lean 文件
scripts/run_all.sh Permanent    # 只处理一个 Lean 文件
scripts/zh_all.sh               # 带中文标签的图
```

依赖只需用 conda 安装一次：

```bash
conda create -n graphviz --override-channels -c conda-forge graphviz font-ttf-noto-cjk
```

全部重跑大约需要一小时，大部分时间花在 `GapCVP` 那张图的排版上。

| 脚本 | 作用 |
|---|---|
| `roots.tsv` | Lean 文件和各自的主定理。 |
| `DeclGraph.lean` | 读取编译好的文件，输出完整的依赖图。 |
| `cone.py` | 把完整的图裁剪到某一个定理的依赖。 |
| `extract.py` | 生成只包含某个定理所需内容的 Lean 文件。 |
| `check.py` | 执行提取并编译结果，如果有引理需要加回就重试。 |
| `svg2png.sh` | 把 SVG 渲染成 PNG，长边最多 8,000 像素。 |
| `run_all.sh` | 对每个主定理执行以上全部步骤。 |
| `Duplicates.lean` | 在十个文件中找陈述相同的定理、相同的定义和一行推论。 |
| `LibraryUse.lean` | 统计每个文件用到了哪些 Mathlib 常量。 |
| `zh_gloss.py`、`zh_labels.py`、`zh_all.sh` | 生成带中文标签的图。 |
