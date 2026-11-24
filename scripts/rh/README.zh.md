# 黎曼猜想形式化证明的依赖图

[English](README.md)

这些图画的是
[leanprover-community/riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis)，
即 2026 年黎曼猜想证明（以及 Dirichlet L 函数的广义黎曼猜想）的 Lean 形式化。图是根据它
`main` 分支的提交
[`6c68212`](https://github.com/leanprover-community/riemann-hypothesis/commit/6c6821263d6b80f4ec3d7479b0159340c1b2f65e)
（2026 年 11 月 24 日）生成的。

## 为什么是三张小图而不是一张大图

本仓库的十个证明各是一个 Lean 文件。黎曼猜想的形式化则有 60,928 个文件、1,690 万行。
它的 `Main.lean` 里的五个定理（`riemannHypothesis` 及四个变体）依赖于：

| | |
|---|---:|
| 声明 | 727,065 |
| 其中定理 | 568,159 |
| 它们之间的箭头 | 9,827,858 |
| 来自的 Lean 文件 | 58,519 |

五十多万个方框的图既画不出来也没法看，所以改成三张小一些的图，各从一个角度看这个证明：

| 图 | 一个方框是 | 方框数 | English | 中文 |
|---|---|---:|---|---|
| 证明的顶层 | 一个定理 | 395 | [SVG](../en/svg/riemannHypothesis.svg) · [PDF](../en/pdf/riemannHypothesis.pdf) · [PNG](../en/png/riemannHypothesis.png) | [SVG](../zh/svg/riemannHypothesis.zh.svg) · [PDF](../zh/pdf/riemannHypothesis.zh.pdf) · [PNG](../zh/png/riemannHypothesis.zh.png) |
| 按文件夹看整个证明 | 一个源码文件夹 | 149 | [SVG](../en/svg/riemannHypothesis_folders.svg) · [PDF](../en/pdf/riemannHypothesis_folders.pdf) · [PNG](../en/png/riemannHypothesis_folders.png) | [SVG](../zh/svg/riemannHypothesis_folders.zh.svg) · [PDF](../zh/pdf/riemannHypothesis_folders.zh.pdf) · [PNG](../zh/png/riemannHypothesis_folders.zh.png) |
| 把整个证明切成独立的块 | 一个子证明及只有它用到的全部内容 | 194 | [SVG](../en/svg/riemannHypothesis_blocks.svg) · [PDF](../en/pdf/riemannHypothesis_blocks.pdf) · [PNG](../en/png/riemannHypothesis_blocks.png) | [SVG](../zh/svg/riemannHypothesis_blocks.zh.svg) · [PDF](../zh/pdf/riemannHypothesis_blocks.zh.pdf) · [PNG](../zh/png/riemannHypothesis_blocks.zh.png) |

### 证明的顶层

离 `Main.lean` 的五个定理最多四步的定理，画法和本文件夹里其他的图一样：五个主定理是橙色，
实线箭头表示直接引用，虚线箭头表示经过某个定义的依赖（见 [../README.zh.md](../README.zh.md)）。

新增的颜色是**灰色**：灰色方框是一个定理，它的证明还用到了图里没画出来的定理。这 119 个灰色
方框是图停下的地方，不是证明停下的地方。

### 按文件夹看整个证明

`src/` 下每个两层深的文件夹（`Formalism/LocalToGlobal`、`Development/WeilBound` 等）是一个
方框，方框里写着证明用到了这个文件夹里的多少个定理。`Lemmata/` 下的 145 个文件夹各只有一个
定理，合并画成一个方框。从文件夹 `A` 指向文件夹 `B` 的箭头表示 `B` 里有声明用到了 `A`
里的声明。颜色表示顶层文件夹。

定理之间不会互相依赖，文件夹之间却可以，所以这张图有环，不能严格地从左往右读。
568,159 个定理里有 248,910 个在 `Development/AbelianVarietyTheory` 这一个文件夹里。

[folders.tsv](folders.tsv) 列出了每个文件夹的定理数、定义数和 Lean 文件数。

### 把整个证明切成独立的块

文件夹是作者存放代码的方式，不一定反映证明本身的结构。这张图改为按证明自己的结构来切。

如果从主定理往下到声明 `D` 的每一条依赖链都经过定理 `X`，就说 `D` **属于** `X`。这时
`D` 只在 `X` 的证明里用到：删掉 `X`，就没有别的地方需要 `D`。（用图论的话说，`X` 支配
`D`。）每个声明都属于离它最近的这样一个定理，于是整个证明构成一棵树。

一个**块**是一个至少有 2,000 个声明属于它的定理，加上所有属于它、但不属于更小的块的内容。
每个方框是一个块，标着它的定理名和它自己独有的声明数。从块 `A` 指向块 `B` 的箭头表示 `A`
是 `B` 的证明的一部分。主定理在最右边，越往左，子证明越深、越独立。

切出来的结果说明：

- **一半的证明是共用的。** 最大的三个块 `everyCharacter`、
  `nonempty_hyps_definite_side_of_closed_bound` 和 `every_character_of_literature_of_vWin`
  自己独有 349,020 个声明，占整个证明的 48%。它们不是各自一段论证，而是被下面几个分支共同
  使用的引理池，所以不属于任何更小的块。
- **有 50 个块是叶子**，即内部没有更小的块、各有 2,000 到 12,000 个声明的独立子证明，合计
  独有 150,195 个声明。这些是可以单独拿出来读的部分。

图里只画了这棵树。一个块还会用到它上面各块的共用引理池；把这些用法也画上，会多出从右往左的
箭头，把树变成一团乱麻。

[blocks.tsv](blocks.tsv) 列出每个块的上级块、独有的声明数和整棵子树的声明数。运行
`rh_blocks.py <dir> <out> N` 可以把块的门槛从 2,000 改成 `N`。

## 浏览网站

[`site/`](site/) 是一个可以一层层浏览整个证明的小网站。它用的是和块图同一棵树，但不设大小门槛：
凡是有内容属于它的声明，都有自己的一页，共 173,224 页。网址是
<https://bil022.github.io/riemann-explorer/>，由仓库
[bil022/riemann-explorer](https://github.com/bil022/riemann-explorer) 发布；
`publish_site.sh <它的本地克隆>` 会把 `site/` 复制过去。在本地运行：

```bash
python3 -m http.server -d scripts/rh/site 8000
```

然后打开 <http://localhost:8000>。（直接双击打开 `index.html` 不行：浏览器不允许
`file://` 页面读取数据文件。）

- **每一页**显示一个声明（橙色）和直接属于它的各部分。每个部分是一个方框，写着名字和包含的
  声明数，蓝色越深越大。画出最大的 40 个部分，右边的表格列出全部。
- **共用组。** 没画出来的部分大多是被几个画出来的部分共用的引理（所以它们不属于其中任何
  一个）。它们按"被哪些画出来的部分用到"（直接或经过其他没画出的部分）分组，比如"A、B 共用"
  "A、B 等 5 个分支共用"。最大的 10 组画成虚线框，箭头指向用到它们的部分。点击一组，会显示
  摘要（定理和定义各多少、代码行数、被用得最多的 10 个和最大的 10 个成员），表格里也只列出这一组。
- **表格各列：** 子树中的声明数、直接下级数、被多少声明直接用到（"被用"）、代码行数。按"被用"
  排序，就能找到最核心的概念。例如在 `everyCharacter` 这一页，47,234 个部分分成 711 组，最大的一组是只被
  它的两个主分支共用的 14,818 个部分。
- **箭头**从一个部分指向用到它的部分，越粗引用越多。能由更长路径推出的箭头默认隐藏，勾选
  右下角的选项可以显示。
- **点击**方框进入它的页面。橙色方框旁边的 **↑ 上一层** 按钮或顶部的路径可以返回上层。
  搜索框可以按名字找到全部 727,065 个声明中的任何一个。
- **Lean 源码。** 点一个内部没有东西的部分，图的下方会显示它的 Lean 代码，带行号，并链接到
  GitHub 上对应的行；任何部分都可以点"Lean 源码"按钮查看。代码是从 GitHub 上上述提交里读取的，
  所以需要联网。行号来自 `.olean` 文件，727,065 个声明中有 725,404 个记录了行号，其余的按名字
  在文件里查找。
- 界面有中文和英文。

数据在 `site/data/`，共 54 MB，由 `rh_site.py` 生成。本仓库不保存这些数据（见 `.gitignore`），
只有 bil022/riemann-explorer 里有；运行 `rh_all.sh` 即可生成。页面用
[Cytoscape.js](https://js.cytoscape.org/) 和 dagre 排版，已连同 MIT 许可证复制到
`site/vendor/`，不联网也能用。

### 中文标签

和其他图一样，按 [../glossary.zh.txt](../glossary.zh.txt) 逐词对译。这个项目的不少词
（`Automorphic`、`Reciprocity` 等）还不在词表里，保留英文。

## 图是怎么生成的

方法和 `../DeclGraph.lean`、`../cone.py` 相同：读取编译好的 `.olean` 文件，把 Lean
自动生成的辅助常量（`foo._proof_1`、`foo.match_1`、构造子、递归子）并入它们所属的声明，
再跟踪每个声明用到了什么。不同之处有两点：

- **模块很多。** `DeclGraph.lean` 只跟踪一个模块内部的依赖；`RHRead.lean` 跟踪项目所有
  模块之间的依赖，忽略 Mathlib 和 Lean 本身。
- **不能一次全部导入。** 一次导入全部 60,928 个模块要把约 180,000 个文件映射进内存，超过
  Linux 的默认上限（`vm.max_map_count` = 65,530），而调高上限需要 root 权限。所以
  `rh_all.sh` 把模块分成 16 批，每批一个 Lean 进程，再由 `rh_cone.py` 合并结果。

## 重新生成

```bash
git clone https://github.com/leanprover-community/riemann-hypothesis
cd riemann-hypothesis
lake exe cache get        # 下载编译好的项目，约 85 GB
cd -
scripts/rh/rh_all.sh path/to/riemann-hypothesis
```

`lake exe cache get` 要求 `PATH` 上的 `python3` 版本不低于 3.11。如果系统的 CA 证书不在
`/etc/ssl/certs/ca-certificates.crt`（Red Hat 等系统），还要设置
`CURL_CA_BUNDLE=/etc/ssl/certs/ca-bundle.crt`。

运行大约需要十分钟，16 批并行读取时每批约占 15 GB 内存。和 `../run_all.sh` 一样需要
Graphviz 和 rsvg-convert。

| 文件 | 作用 |
|---|---|
| `RHRead.lean` | 读取一批编译好的模块，输出每个声明及它用到的内容。 |
| `rh_cone.py` | 合并各批结果，生成前两张图和 `folders.tsv`。 |
| `domtree.py` | 计算支配树，供 `rh_blocks.py` 和 `rh_site.py` 使用。 |
| `rh_blocks.py` | 生成块图和 `blocks.tsv`。 |
| `rh_site.py` | 生成浏览网站的数据。 |
| `site/` | 浏览网站：`index.html`、`app.js`、`style.css`。 |
| `publish_site.sh` | 把 `site/` 复制到 bil022/riemann-explorer 的本地克隆。 |
| `rh_all.sh` | 运行以上全部，再生成中英文的 SVG、PDF 和 PNG。 |
