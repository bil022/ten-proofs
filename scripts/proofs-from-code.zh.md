# 只看代码：这十个证明是怎么组织的

[English](proofs-from-code.md) · [返回说明](README.zh.md) · [按论文讲解](proofs.zh.md) · [从最简单的叶子读起](leaves.zh.md)

这份总结**只依据 Lean 代码本身**得出，没有参考论文。信息来源有四种：

1. **定理陈述**：主定理和它用到的定义，直接从源码翻译。
2. **依赖图**：用 `DeclGraph.lean` 从编译结果里提取，从而知道哪个定理用到了哪个。
3. **声明的名字**：Lean 文件没有一行注释，名字是作者留下的唯一说明。
4. **Mathlib 用量统计**：用 `LibraryUse.lean` 统计每个文件用到了 Mathlib 的哪些部分，从而看出它依赖哪些数学领域。

下文中，"主干"是指：从主定理出发，每一步都往下走到"支撑最多定理"的那条依赖，一路走下去得到的链条。它大致对应证明中最重的那条推理路线。**对名字含义的解读是我的推断**，凡是只从名字猜出的内容，都写明了"从名字看"。

---

## 总览

| 文件 | 行数 | 声明数 | 定理 / 定义 | 主定理用到的比例 | 主要依赖的 Mathlib 领域 |
|---|---:|---:|---|---:|---|
| `SpherePacking` | 55,617 | 2,284 | 1,879 / 395 | 92% | 特殊函数、微积分、复分析、积分 |
| `MetricCodes` | 114,407 | 5,778 | 4,386 / 1,365 | 96% | 多元多项式、内积空间、特殊函数、矩阵 |
| `NonSoficGroup` | 34,441 | 1,501 | 1,108 / 371 | 100% | 内积空间、赋范空间、划分 |
| `ConnesRigidity` | 37,375 | 2,918 | 2,032 / 856 | 94% | 多项式、拓扑代数、内积空间、测度 |
| `Permanent` | 27,564 | 1,434 | 983 / 434 | **23%** | 多元多项式、理想、正则序列 |
| `QuantumParallelRepetition` | 70,981 | 2,739 | 1,849 / 873 | 99% | 矩阵（半正定、迹、克罗内克积）、对数 |
| `GapCVP` | 130,431 | 8,230 | 3,719 / **4,458** | 95% | **图灵机**、多项式、赋值论 |
| `EhrhartVolumeInequality` | 55,756 | 2,396 | 1,903 / 490 | 99% | 微分（Fréchet 导数）、积分、测度 |
| `MulticolorTriangleRamsey` | 3,054 | 146 | 101 / 44 | 92% | 对数与幂函数、图论 |
| `CompactnessAndDegeneracy` | 18,589 | 957 | 665 / 288 | 99% | 图论、对数、二元熵、有限维线性代数 |

"主定理用到的比例"按声明所占的源码行数计算。

几个从代码直接看出的共同点：

- **没有任何"后门"**：十个文件里 `sorry`、`admit`、`axiom`、`native_decide`、`unsafe`、`implemented_by` 的出现次数全是 0。也就是说，所有结论都由 Lean 内核从三条标准公理出发完整检查过，没有借助编译器执行代码来"相信"某个计算结果。
- **没有注释**：一行注释都没有。名字平均长 22 到 36 个字符，最长的有 114 个字符，名字承担了说明的作用。
- **主定理几乎用到整个文件**：除了 `Permanent`，各文件 90% 以上的内容都服务于主定理。`Permanent` 的例外，是因为文件里还有一个规模更大、单独的结果（见第 5 节）。
- **用的工具不同**：`GapCVP` 的定义比定理还多，因为它要定义大量图灵机；分析类的文件（球堆积、Ehrhart）大量使用 `linarith`、`positivity`、`calc` 做不等式推导；组合和计算类的文件（`GapCVP`、`MetricCodes`）大量使用 `omega`、`decide`、`induction`。

---

## 1. 高维球堆积（`SpherePacking.lean`）

**主定理在说什么**：`sharpFullCohnElkiesManuscriptConclusions` 本身没有参数，它断言一个由十条结论组成的结构 `SharpFullCohnElkiesManuscriptConclusions` 成立。其中最核心的几条：

- `linear_program_root`：`fullLinearProgram d` 的 d 次方根，在 d → ∞ 时趋于 √(e/(2π))。
- `root_before_infimum`：对所有"合格函数"（`FullAdmissible d`）取某个比值（`fullQuotient`）的 d 次方根，其下确界除以 √d，趋于 1/π。
- `universal_nonnegative_delta`：对每个合格函数都成立的一致下界。
- 其余几条是同一结论换成以 2 为底的对数、带误差项的写法等。

也就是说，主定理是关于一个**线性规划的最优值**的渐近结论。

**代码组成**：`CohnElkies` 命名空间占 46,176 行、1,818 个声明，是绝对主体。

**主干**（从主定理往下）：

```
sharpFullCohnElkiesManuscriptConclusions
 ← SharpFullCohnElkiesManuscriptConclusions.components   （拆成十个分量）
 ← SharpFullCohnElkiesManuscriptConclusions.ofRadial     （由径向情形得到）
 ← CohnElkies.sharpCohnElkiesManuscriptConclusions
 ← CohnElkies.exists_manuscriptUniversalPackingIsLittleO
 ← CohnElkies.sharpPackingRootAsymptotic
 ← CohnElkies.sharpAsymptotics
 ← CohnElkies.sharpAsymptotics_of_saddleSourceEventualSigns
 ← CohnElkies.uniformAntiFourierSignRadius
```

从名字看：先把问题化为**径向函数**（`ofRadial`、`fullLinearProgram_eq_radial`），核心是 `sharpAsymptotics`。它由两部分支撑：一部分关于"反傅里叶函数的符号半径"（`uniformAntiFourierSignRadius`，函数满足 f̂ = −f 时从多大半径开始不再变号）；另一部分是用"鞍点"构造的函数（`saddleSource...`）及其最终符号（`EventualSigns`），也就是构造出一个具体的好函数。

**文件里还有什么**：`PackingBounds.PackingBridge.sphere_packing_sharp_asymptotic_upper` 断言真正的**球堆积常数**不超过 (√(e/(2π)) + o(1))^d。它额外用到 264 个声明，来自 `SchwartzMap.PoissonSummation`（泊松求和公式）、`PeriodicSpherePacking`（周期堆积）等命名空间。这部分把线性规划连接到实际的堆积密度，但**不在列出的主定理的依赖范围内**。

**用到的数学**：Mathlib 中用得最多的是特殊函数（幂、三角、对数、Gamma 函数）、Fréchet 导数、Bochner 积分和区间积分、复指数。代码里大量出现 `Mellin`、`saddle`、`contour`（围道）、`Gamma` 等名字，说明用到了 Mellin 变换和复积分的鞍点估计。

---

## 2. 二元码与球面码（`MetricCodes.lean`）

这个文件有两个主定理。

### 2a. 二元码：`binaryRate_lt_mrrw`

**主定理在说什么**：对 0 < d < 1/2，`binaryRate d < mrrwRate d`。

- `binaryRate d` 定义为"长度 n、最小距离至少 ⌈dn⌉ 的二元码的最大码字数"取 log₂ 后除以 n 的上极限，即码率的上限。
- `mrrwRate` 是对一个目标函数 `mrrwObjective` 取最小值，即经典的 MRRW 界。

所以定理说：真正的码率上限**严格小于** MRRW 界。

**主干**：

```
binaryRate_lt_mrrw
 ← binaryRate_le_combinedVariationalRate        （码率 ≤ 一个"组合变分率"）
 ← binaryRate_le_combinedVariationalRate_of_projectionGrams
 ← binaryRate_le_shellRate_of_projectionGrams
 ← SpectralAsymptotics.eventually_spectralGap_lt
 ← SpectralAsymptotics.eventually_topEigenvalue_gt
 ← SpectralAsymptotics.tendsto_terminalRayleigh
 ← SpectralAsymptotics.tendsto_johnsonEdge
```

另一条分支 `strict_mrrw2` 证明"组合变分率 < MRRW 界"，下面分成两种情况：`mrrw_endpoint_dichotomy`、`variationalRate_lt_mrrw_of_interior`（最优点在内部）、`combinedVariationalRate_lt_mrrw_of_endpoint`（最优点在端点）。

从名字看，证明分两步：

1. 用"投影 Gram 矩阵"（`projectionGram`）给出码字个数的上界，这个上界取决于某个矩阵的**最大特征值**（`topEigenvalue`、`Rayleigh` 商、谱间隙 `spectralGap`）。这些矩阵来自 Johnson 结构（`johnsonEdge`），也就是固定重量的二元串。
2. 再证明这样得到的率严格优于 MRRW，并按最优点的位置分情况。

### 2b. 球面码：`strict_hierarchy`

**主定理在说什么**：对 0 < s < 1，存在一列率 `levelRate r s`（r = 0, 1, 2, …），每一层都严格小于前一层；另有一个"局部化"版本，满足

```
球面码率 ≤ localizedHierarchyRate < localizedLevelRate 1 < localizedRowRate
        < localizedLevelRate 0 = classicalLocalizedRate
```

也就是一个**严格改进的层级**，第 0 层等于经典的界。

**主干**：

```
strict_hierarchy
 ← fixedLevelHierarchyCodeBound
 ← fixedLevelHierarchyCodeBound_of_actualCharacteristicMinor
 ← …（几层关于 Fischer 递推、Young 盒子表示的充分条件）
 ← fixedLevelHierarchyCodeBound_of_actualRectangularGraphs
 ← eventually_sphericalCode_card_lt_of_eventualGraphCertificates
 ← sphericalCode_bound_of_realized_graph
```

从名字看：每一层的界都来自一个"图证书"（`GraphCertificates`）。构造这些图要用到 Young 图（`Young`、`Box`）、Gelfand–Tsetlin 基（`GelfandTsetlin`）、Weyl 公式（`Weyl`）、Casimir 算子（`Casimir`）等表示论工具。`MetricCodes.Spherical` 命名空间占了 69,180 行，是整个文件的大头。

**文件里还有什么**：`hierarchyPackingExponent_eq_criticalBinaryExponent` 说球面码层级给出的**球堆积指数**等于第 1 题里的临界指数 `CohnElkies.criticalBinaryExponent`。文件里还有若干关于"接吻数"（`kissingNumber`）上界的结果。这些都不在两个主定理的依赖范围内。

**用到的数学**：多元多项式（求导、单项式序、齐次多项式）、内积空间和伴随算子、拉格朗日插值、行列式、三角函数和积分。

---

## 3. 非 sofic 群（`NonSoficGroup.lean`）

**主定理在说什么**：存在一个群 G，它是有限表示的，并且不是 sofic 的。

代码中的定义：sofic 是指存在一列"置换模型"（`SoficApproximation`），使得乘法在归一化汉明距离下渐近成立（`multiplicative`），并且非单位元渐近地移动几乎所有点（`separated`）。

**代码组成**：文件 100% 的内容都在主定理的依赖范围内。名字里 `Kun` 出现得极多（`KunThomFiberCoarea`、`KunResidualExpanderDecomposition` 等），另外有 `Leavitt`、`Thompson`、`Prefix`、`Kazhdan`、`Cheeger`、`Expander` 等主题词。

**主干**：

```
exists_finitelyPresented_nonsofic_group
 ← binaryLeavittElementaryGroup_not_sofic
 ← ninePrefixElementaryGroup_not_sofic
 ← sourceLocalPrefixTranspositionGroup_lef_of_sofic     （若 sofic，则某个群是 LEF 的）
     并且 sourceLocalPrefixTranspositionGroup_notLEF    （但这个群不是 LEF 的）
 ← source_ambient_nonempty_expandingCentralizerFiniteModel
 ← exists_source_selected_components                     （挑选出一块"分量"）
 ← exists_actual_source_u_retained_matching              （一个匹配）
 ← exists_unconditional_actual_source_dual_finpartition_sequences
 ← …
 ← alphaPrefixElementaryGroup_hasPropertyT_unconditional （某个初等群有性质 (T)）
```

从这条链可以读出证明的逻辑是**反证法**：

1. 主角是"9 个前缀的初等群"（`ninePrefixElementaryGroup`），位于二元 Leavitt 代数（`binaryLeavitt`）里。
2. 假设它是 sofic 的，就推出另一个群 `sourceLocalPrefixTranspositionGroup` 是 LEF 的。
3. 而那个群本身不是 LEF 的（`notLEF`），矛盾。
4. 第 2 步的推导要用到：有限模型中的"扩张图分量"（`expandingCentralizerFiniteModel`）、从中选出一块分量、在分量之间建立匹配，以及某些群具有 Kazhdan 性质 (T)。
5. 最后从"有限生成的非 sofic 群"得到"有限表示的非 sofic 群"（`exists_finitelyPresented_not_sofic_of_not_sofic`）。

**用到的数学**：内积空间与正交投影、算子范数、划分（`Finpartition`）、汉明距离。值得注意的是，性质 (T) 是在文件里**从头证明**的（`..._hasPropertyT_unconditional`），而不是作为前提引用。

---

## 4. Connes 刚性猜想（`ConnesRigidity.lean`）

**主定理在说什么**：存在一个群 Λ 和一列群 Γ₀, Γ₁, Γ₂, …，满足：

- 它们都是有限生成的、ICC 的、具有 Kazhdan 性质 (T)；
- 每个 Γₙ 的群因子都和 Λ 的同构，并且两两同构（`TracialGroupFactorsIsomorphic`：两个群冯·诺依曼代数之间存在保持迹的正规 *-同构）；
- 但 Γₘ 和 Γₙ（m ≠ n）作为群互不同构，Λ 和每个 Γₙ 也不同构。

**主干**：

```
主定理
 ← PaperAnalyticInput.universalLattice           （"泛格"有性质 (T)）
 ← universalLatticePropertyT_of_suslinRelative
 ← integralElementaryGroup_propertyT
 ← shalomIntegralPolynomialRelativePair
 ← …
 ← integerShalomRelativeKazhdanPair_of_fourierAtomGap
 ← exists_kernel_fixed_of_joint_atom_pos
```

最重的一支是证明某个矩阵群具有**性质 (T)**，占了 1,710 个定理中的 733 个。从名字看，用的是 Shalom 的方法（`shalom...`）、Suslin 的初等生成定理（`suslinRelative`、`ElementaryGeneration`），以及傅里叶分析（`fourierAtomGap`）。

主定理的其余分量各有来源：

| 分量 | 依据 |
|---|---|
| 群因子同构 | `paper_factors_isomorphic`，依赖 `carryCoordinates_measurePreserving`（"进位坐标"保持测度） |
| 不同构 | `gamma_has_order_four`（Γ 有 4 阶元素）、`paperLambda_orderOf_ne_four`（Λ 没有），以及 `paperInvariant_card`（一个可计算的群不变量） |
| ICC | `gamma_isICC`、`lambda_isICC`（轨道无限） |

从这些名字可以拼出证明的轮廓：用"进位"在同一个测度空间上构造出不同的群结构，测度相同所以群因子相同，再用元素的阶等群论不变量把它们区分开。

**文件里还有什么**：`exists_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors` 是"只有两个群"的版本，主定理没有用到它。

**用到的数学**：多项式（求值、次数）、内积空间与正交投影、C*-代数、Bochner 积分、特殊线性群与平延（`transvection`）、半直积、阶。

---

## 5. 积和式的下界（`Permanent.lean`）

**主定理在说什么**：设 n ≥ 32。若一个带除法的公式 f（`RationalFormula`，并要求合法，即分母非零）计算出的结果恰好是 n×n 积和式多项式，那么

```
n⁴ / (192 · log₂ n) ≤ f 中变量出现的次数（variableLeaves）
```

**代码组成**：这个文件很特别，主定理只用到 23% 的内容。

- `PermanentFormulaLowerBound`（约 6,600 行）：公式下界，主定理只用到这部分。
- `PermanentRollout`（约 19,000 行）：主定理完全没用到，见下面"文件里还有什么"。

**主干**（这是十个主干里最清晰的一条）：

```
permanent_rational_formula_logarithmic_lower_bound
 ← permanent_rational_formula_lower_bound
 ← permanent_rational_formula_fourth_power_lower_bound
 ← matchingCyclicBlock_coefficientTranscendenceDegree_ge_square
                            （一个"匹配块"的系数超越次数 ≥ 平方量级）
 ← matchingMarkedPermanent_bitCoefficient_algebraicIndependent
                            （某些系数代数无关）
 ← matchingPermanentJacobian_det_ne_zero        （一个雅可比行列式非零）
 ← matchingPermanentJacobian_eq_weighted
 ← matchingWeightedCrossBitPermutation_sum
```

另一支 `cyclicMatchingBlock_fourth_power_bound_of_coefficientTranscendenceDegree` 把"超越次数大"换算成"变量出现次数多"；`permanent_size_bounds_of_fourth_power` 在不同的长度度量之间换算（"叶子数 = 运算数 + 1"就用在这里）。

从这些名字可以完整读出证明思路：

1. 选出排成"匹配"的一小块变量。
2. 证明积和式按这些变量展开后，系数里有很多**代数无关**的量。方法是证明一个雅可比行列式在某点非零。
3. 公式里这些变量出现的次数，至少和这个超越次数同阶。
4. 把很多块互不相交的匹配加起来（`cyclic`，循环排列）。

**文件里还有什么**：`PermanentRollout.permanent_circuit_loglog_bigOmega`：存在常数 c > 0，使得对足够大的 n，

```
c · n² · log₂ log₂ n ≤ circuitComplexity(permanent n)
```

也就是**算术电路**（允许复用中间结果）计算积和式的下界。它额外用到 948 个声明，涉及正则序列（`RegularSequence`）、齐次理想、零点定理（`Nullstellensatz`）等交换代数工具。文件里还有不带除法的公式下界 `permanent_divisionFree_formula_logarithmic_lower_bound`。这些都不在列出的主定理里。

---

## 6. 量子并行重复（`QuantumParallelRepetition.lean`）

**主定理在说什么**：存在常数 c > 0，使得对任意有限的双人游戏 G（问题集 X、Y，答案集 A、B 都有限且非空），如果纠缠值 `entangledValue G` 小于 1，那么对每个 n ≥ 1：

```
repeatedEntangledValue G n
  ≤ exp( −c · ε¹³ / (ε + log(|A|·|B|)) · n )，其中 ε = 1 − entangledValue G
```

即重复 n 次后的纠缠值随 n 指数下降。

**代码组成**：主命名空间占 61,916 行，另有 `ClassicalInformation`、`ClassicalSampling`、`Pinsker`（Pinsker 不等式）、`Game`、`Strategy` 等小模块。

**主干**：

```
distributionUniformExponential
 ← pdf_distributionUniformExponential_unconditional
 ← unconditionalSourceOneGameRounding_uniform              （"单局取整"）
 ← unconditionalSourcePhysicalRounding_exists_small
 ← unconditionalActualFairSourceRoundingData_exists_stoppedVerifier
 ← unconditionalActualFairSourceRoundingContext_stoppedVerifier
 ← unconditionalActualFairSourceRoundingContext_analyticLedger
 ← unconditionalActualFairSourceStoppingHazardData_of_positive
 ← unconditionalSourcePhysicalRounding_exists_fairStoppingHazard
 ← unconditionalSourcePhysicalRounding_fairTargetEnergy
```

从名字看，证明的核心是一个"取整"（`Rounding`）过程：从多局游戏的策略中构造出单局游戏的策略。这个构造用到"停时"（`stopped`、`StoppingHazard`）、"鞅"（`martingaleRate`）、"能量"（`Energy`），以及一本记录各项误差的"账本"（`Ledger`）。另有 `fair`（公平）、`Clipping`（截断）、`cleanBound` 等用于误差控制的名字。

**用到的数学**：半正定矩阵（大量使用）、迹、克罗内克积（双方系统的张量积）、酉矩阵、对数与熵、Pinsker 不等式。

---

## 7. 最近向量问题（`GapCVP.lean`）

**主定理在说什么**：`gapCVP400IsNPHard : IsNPHardPromise gapCVP400Promise`。代码中的定义：

- `gapCVP400Promise` 是一个"承诺问题"。"是"实例（`gapYES400`）是指存在整数向量 z，使目标到格点的距离平方 ≤ r²；"否"实例（`gapNO400`）是指对所有 z，距离平方都 > (因子 · r)²，这个因子是 `gapFactor400`。
- `IsNPHardPromise` 是指：**每个** NP 语言都能通过一个 `PromiseReduction` 归约到它。而 `PromiseReduction` 要求归约映射由一台多项式时间的图灵机（`BitTM`）计算，并满足完备性（是 ↦ 是）和可靠性（否 ↦ 否）。

**代码组成**：定义（4,458 个）比定理（3,719 个）还多，十个文件里唯一如此。Mathlib 中用得最多的是 `Computability.TuringMachine`（约 3 万次引用），远超其他任何部分。434 个命名空间里有大量名字以 `TM`（图灵机）、`CL` 开头。

**主干**：

```
gapCVP400IsNPHard
 ← paperVariableArityPhysicalIntegerTargetNPHardPromise
 ← OriginalThreeSATNPHardness.paperOriginalThreeSATIsNPHard   （3SAT 是 NP 困难的）
 ← fiveFamilyActualSourceSortedIndexedORGadgetPreparationWord_valid
 ← …（一长串关于"五族子句"编码、排序、流处理的有效性证明）
```

主定理的直接依赖还有 `..._completeness`、`..._soundness`（完备性和可靠性）、`paperVariableArityPhysicalShiftedCheckBit_valid`（校验位），以及 `yesLanguage_iff_original`、`noLanguage_iff_original`（编码一致性）。

从代码可以确定的结构：

1. **证明 3SAT 是 NP 困难的**：`paperOriginalThreeSATIsNPHard` 一支就有 1,601 个定理（全部 3,522 个的 45%）。名字带 `CL` 的命名空间（`CLVerifier`、`CLTableau`、`CLLocalWindows` 等）从名字看是 Cook–Levin 定理的构造：把验证者图灵机的运行过程写成一张"表"（tableau），再编码成 CNF 公式。
2. **从 3SAT 归约到 CVP**：中间经过有限域上的多项式（`EffectiveBinaryField`、`Lagrange`、`Interpolation`）、高斯消元（`Gaussian`）和赋值论（`Valuation`）。
3. **每一步都要给出具体的图灵机**并证明运行时间是多项式的：`..._polynomiallyBoundedFoldStates`、`EvalsToInTime` 等。这就是定义特别多的原因。

**文件里还有什么**：同一套归约还推出了三个结果，都不在主定理的依赖范围内：

- `binaryNearestCodewordIsNPHard`：二元最近码字问题；
- `binarySyndromeDecodingIsNPHard`：伴随式译码；
- `finitePNormGapCVPIsNPHard`：ℓp 范数下的最近向量问题。

---

## 8. Ehrhart 体积猜想（`EhrhartVolumeInequality.lean`）

**主定理在说什么**：设 S 是 n 维空间里的凸紧集，内部非空，重心在原点，并且内部的整点只有原点（`interiorLatticePoints S = {0}`）。那么

```
normalizedVolume S ≤ (n + 1)ⁿ / n!
```

**代码组成**：222 个命名空间，几乎都很长，名字里反复出现 `Bergman`、`Jet`、`Torus`、`Bochner`、`Dolbeault`、`Holomorphic`、`Plurisubharmonic`、`Moment`、`Partition`。从名字看，这些是复几何和多复变函数论的术语。

**主干**：

```
ehrhart_volume_inequality_for_sets
 ← normalizedVolume_le_sharpConstant_of_momentBodyWeakProbability
 ← momentBodySharpJetScale_le_dimension_of_weakProbability     （某个"尺度" ≤ 维数 n）
 ← integral_momentBodyEnvelopePositiveSecant_le_dimension_mul_exp
 ← one_sub_momentBodyNormalizedPartition_le_dimension_mul
 ← exp_neg_dimension_mul_le_momentBodyNormalizedPartition
 ← momentBodyLogPartition_le_dimension_mul                    （对数配分函数 ≤ n·t）
 ← convexOn_momentBodyLogPartition_Ici                        （对数配分函数是凸的）
 ← convexOn_momentWeakHolomorphicStrictJointLogPartition_Ioi
 ← convexOn_..._of_timeBounds
```

从这条链可以读出证明的核心结构：

1. 定义一个依赖于参数 t 的"对数配分函数"（`LogPartition`），并证明它是**凸函数**。
2. 由凸性和增长估计得到：它不超过 n·t。
3. 一层层换算（配分函数 → 割线积分 → 尺度），得出某个"尺度"不超过维数 n。
4. 这个尺度上界等价于体积上界 (n+1)ⁿ/n!。

凸性的证明（`HolomorphicPhysicalLogConvexity` 等）要用到全纯函数、环面（`Torus`）上的傅里叶分析和 Bochner 恒等式。

**文件里还有什么**：`SimplexVolume.exists_centeredBody_sharp`：在每个维数 n 下，确实存在满足条件的凸体，体积恰好等于这个上界，即界是最优的。主定理没有用到它。

**用到的数学**：Fréchet 导数、光滑函数（`ContDiff`）、Bochner 积分、区间积分、圆周平均、隆起函数（`BumpFunction`）、正定矩阵。

---

## 9. 多色 Ramsey 数（`MulticolorTriangleRamsey.lean`）

**主定理在说什么**：

1. 对每个 k ≥ 2，`triangleRamseyNumber k ≥ (k^(1/3) / (6·e³⁸·log k))^k`；
2. `triangleRamseyNumber k` 的 k 次方根趋于无穷。

`triangleRamseyNumber k` 定义为：最小的 n，使得用 k 种颜色给 n 个顶点的完全图染边，必然出现同色三角形。

**代码组成**：只有一个命名空间，146 个声明，是最小的文件。

**主干**（完整列出，只有十层）：

```
erdos_problem_183_explicit
 ← quantitativeLowerBound_explicit_all          （显式下界，对所有 k ≥ 2）
 ← allColourPaletteRamsey_exponential_bound_sharp
 ← recursivePaletteRamsey_exponential_bound      （递归构造给出的指数界）
 ← exists_recursivePaletteStage                  （每个阶段都存在）
 ← exists_recursivePaletteColouring_fin          （存在递归调色板染色）
 ← exists_coordinate_covering                    （存在坐标覆盖）
 ← exists_saturated_matrix_ceil
 ← exists_saturated_matrix                       （存在饱和矩阵）
 ← card_badSaturationRows_lt_pow                 （"坏行"的个数小于某个幂）
```

这条链从下往上读，就是构造的顺序：

1. 用计数论证（坏的情形少于全部情形）证明**饱和矩阵**存在。
2. 由饱和矩阵得到**坐标覆盖**。
3. 用坐标覆盖递归地构造没有同色三角形的**调色板染色**。
4. 数出顶点数，得到下界。

旁支中：`PaletteBlockCertificate.noMonochromaticTriangle` 证明染色没有同色三角形；`factorial_exp_lower`、`choose_le_exp_mul_div_pow` 是数值估计。

**用到的数学**：几乎只用对数、幂函数、指数，以及 Mathlib 的图论（团、着色）。这是十个文件里最"初等"的一个。

---

## 10. 极值图论（`CompactnessAndDegeneracy.lean`）

文件分成两个几乎等大的命名空间，各对应一个主定理：`CompactnessConjecture`（8,495 行）和 `TwoDegenerateGraphs`（8,252 行）。

### 10a. 紧性猜想：`quantitativeCompactnessCounterexample`

**主定理在说什么**：存在一个有限的图族 family 和常数 c, C > 0，满足：

- 每个成员都连通、二部、含圈；
- 每个成员单独禁止时，极值数有一致的下界（`UniformMemberLower family c`）；
- 同时禁止整族时，任何不含族中成员的 n 顶点图，其边数的 16 次方 ≤ C·n²¹，即边数 ≤ C′·n^(21/16)；
- 21/16 = 4/3 − 1/48；
- 这个族不满足紧性（`¬ IsCompactFamily family`），所以紧性猜想不成立（`¬ CompactnessConjectureStatement`）。

**主干**：

```
quantitativeCompactnessCounterexample
 ← checkedManuscriptCounterexample
 ← not_erdos_180
 ← proposedFamily_uniformMemberLower           （每个成员的下界）
 ← proposedFamily_even_characteristic_avoidance（特征 2 的构造能避开某些成员）
     并且 proposedFamily_odd_characteristic_avoidance（奇特征的构造能避开其他成员）
 ← symplecticQuadrangle_no_jTemplate_of_char_two
 ← symplecticLine_char_two_pair_avoidance
 ← …
```

另一支 `proposedFamily_familyExtremal_sixteenth_power_le` 给出整族的上界。从名字看：每个成员的下界来自"辛四边形"（`symplecticQuadrangle`，有限域上辛几何构造的图），并且按有限域的**特征是 2 还是奇数**分两种情况，分别避开族里不同的成员。

### 10b. 退化性猜想：`twoDegenerateExtremalCounterexample`

**主定理在说什么**：存在一个图 H，它连通、二部、2-退化（`IsTwoDegenerate H`），并且无论怎样二着色，两侧都各有度数大于 2 的顶点；同时存在 c, ε > 0，使得对足够大的 n，`extremalNumber n H ≥ c·n^(3/2+ε)`。

**主干**：

```
twoDegenerateExtremalCounterexample
 ← eventually_manuscriptVertexCount_power_le_extremalNumber
 ← eventually_expectedRetainedEdge_le_extremalNumber      （随机保留后的期望边数）
 ← eventually_exists_pairGraph_free_dense_retainedHost    （存在稠密且不含 H 的图）
 ← pairGraphOverFin_free_of_manuscript_exclusion
 ← pairGraph_free_of_layer_exclusion_and_disagreement
 ← pairGraphCopy_layer_entropy_upper_of_disagreement      （逐层的熵上界）
 ← pairChildArrayEntropy_empirical_bound
```

从名字看：

1. H 是一个"配对图"（`pairGraph`），一层一层构造。
2. 宿主图从汉明距离图中随机保留顶点得到（`hammingRetention`）。
3. 证明不含 H 用的是**熵**：如果 H 能嵌入，每一层的熵都会受到约束（`layer_entropy_upper`），层数多了就矛盾。
4. 再证明随机保留后边数足够多（`expectedRetainedEdge`），并控制失败事件的概率（`SamplingFailureEvent`）。

**文件里还有什么**：`not_erdos_146`、`compactnessCounterexample_bigO` 是主定理的推论形式。

**用到的数学**：Mathlib 的图论（拷贝、连通性、着色、二部图）、对数与幂、二元熵函数、有限维线性代数（辛几何构造要用到）。

---

## 这份总结是怎么做出来的

所有统计都可以重现，脚本在 `scripts/` 里：

| 脚本 | 作用 |
|---|---|
| `DeclGraph.lean` | 提取依赖图，记录每个声明的源码行号 |
| `LibraryUse.lean` | 统计每个文件用到的 Mathlib 常量，结果在 `library_use.tsv` |
| `Duplicates.lean` | 找陈述相同的定理、相同的定义和一行推论 |

"主干"和"主定理用到的比例"是在依赖图上用 Python 计算的。
