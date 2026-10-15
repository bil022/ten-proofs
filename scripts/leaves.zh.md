# 从最简单的叶子读起：十个证明各取一个

[English](leaves.md) · [返回说明](README.zh.md)

这十个证明都很长，直接读几乎不可能。但每张依赖图的最左边都有一批"叶子"：它们不依赖本文件里的任何其他定理，只用到 Lean 和 Mathlib 自带的知识。叶子是整座证明大厦的地基，其中有些简单到高中生就能看懂。

下面给每个问题挑了一个这样的叶子，讲清楚三件事：它说了什么、为什么成立、它在整个证明里被谁用到。

挑选标准：只用到高中数学，证明不超过几行，并且确实在通向主定理的路上（每个都出现在对应主定理的依赖图里）。

读之前先说清楚：读懂叶子不等于读懂主定理。叶子离主定理往往隔着几十层，这里只是给你一个"从哪里开始看"的入口。

每节标题下的链接指向 GitHub 上 Lean 源码的对应行。

---

## 1. 高维球堆积

**原题大意**：在高维空间里放互不重叠的同样大小的球，最多能占据多大比例的空间？证明给出了更好的上界。

**叶子定理**：`IsRadial.even`，[SpherePacking.lean 第 270 行](https://github.com/bil022/ten-proofs/blob/main/SpherePacking.lean#L270)

```lean
theorem IsRadial.even {d : ℕ} {f : TestFunction d}
    (hf : IsRadial f) : IsEven f := by
  intro x
  exact hf (-x) x (by simp)
```

**它说了什么**：如果一个函数是"径向的"，那它一定是偶函数。

- **径向函数**：函数值只取决于点到原点的距离 `‖x‖`。距离相同的点，函数值相同。比如 f(x) = x² 在数轴上就是径向的，在平面上 f(x, y) = x² + y² 也是。
- **偶函数**：f(−x) = f(x)。

**为什么成立**：点 x 和点 −x 到原点的距离一样，`‖−x‖ = ‖x‖`。既然径向函数只看距离，那么 f(−x) = f(x)。Lean 的证明就是这一句话：把"径向"的定义用在 −x 和 x 这两个点上，距离相等这一步交给 `simp` 自动验证。

**在证明里的位置**：它被 `fourier_sq_of_radial` 用到。球堆积的 Cohn–Elkies 方法要找一个满足特殊条件的辅助函数，这类辅助函数都是径向的，证明里会反复用到它们的对称性，这条定理就是其中最基本的一条。

---

## 2. 二元码与球面码

**原题大意**：用 0 和 1 组成的长度为 n 的"码字"，要求任意两个码字至少有 d 位不同（这样传输出错时能发现或纠正），最多能选出多少个？证明给出了比以往更强的上界。

**叶子定理**：`hammingDist_self`，[MetricCodes.lean 第 18 行](https://github.com/bil022/ten-proofs/blob/main/MetricCodes.lean#L18)

```lean
def hammingDist {n : ℕ} (x y : BinaryWord n) : ℕ :=
  (Finset.univ.filter fun i => x i ≠ y i).card

@[simp] theorem hammingDist_self {n : ℕ} (x : BinaryWord n) :
    hammingDist x x = 0 := by
  simp [hammingDist]
```

**它说了什么**：先看定义。两个 0/1 串的**汉明距离**，就是它们对应位置上不同的位数。例如：

```
1 0 1 1 0
1 1 1 0 0
  ↑   ↑      有 2 位不同，汉明距离 = 2
```

定理说：一个串和它自己的汉明距离是 0。

**为什么成立**：一个串和它自己每一位都相同，"不同的位置"这个集合是空的，空集的元素个数是 0。

这看起来简单得没必要证明，但计算机证明里每一步都必须明确写出来，后面的推理才能用它。

**在证明里的位置**：它被 `hammingCorrelation_self` 用到。整个证明研究的就是码字之间的汉明距离，这是所有讨论的出发点。

---

## 3. 非 sofic 群

**原题大意**："sofic 群"是可以用有限个元素的置换（重新排列）近似表示的群。长期以来人们不知道是否所有群都是 sofic 的。证明构造了一个不是 sofic 的群，回答了这个问题。

**叶子定理**：`permutationDistance_triangle`，[NonSoficGroup.lean 第 7723 行](https://github.com/bil022/ten-proofs/blob/main/NonSoficGroup.lean#L7723)

```lean
theorem permutationDistance_triangle {V : Type*}
    [Fintype V] [DecidableEq V] (p q r : Equiv.Perm V) :
    permutationDistance p r ≤ permutationDistance p q + permutationDistance q r :=
  hammingDist_triangle _ _ _
```

**它说了什么**：先定义两个置换之间的距离：数一数有多少个元素被这两个置换送到了不同的地方。例如把 {1, 2, 3, 4} 重新排列：

```
p:  1→2  2→1  3→3  4→4
q:  1→2  2→3  3→1  4→4
       不同的是元素 2 和 3，距离 = 2
```

定理说这个距离满足**三角不等式**：d(p, r) ≤ d(p, q) + d(q, r)。就像三角形两边之和大于第三边。

**为什么成立**：假设 p 和 r 在元素 x 上不同，即 p(x) ≠ r(x)。那么 q(x) 不可能同时等于 p(x) 和 r(x)，所以要么 p(x) ≠ q(x)，要么 q(x) ≠ r(x)。也就是说，每个让 p、r 不同的元素，至少会在右边两项里被数到一次。Lean 的证明直接借用了 Mathlib 里已有的汉明距离三角不等式。

**在证明里的位置**：它被 `permutationDistance_mul_le` 等三条定理用到。"用置换近似"中的"近似"，就是用这个距离来衡量的，有了三角不等式才能把很多小误差累加起来估计。

---

## 4. Connes 刚性猜想

**原题大意**：Connes 猜想某一类群可以由它们对应的一种算子代数完全确定。证明给出了反例：无穷多个互不相同的群，它们的算子代数却彼此相同。

**叶子定理**：`vectorGCD_dvd`，[ConnesRigidity.lean 第 33616 行](https://github.com/bil022/ten-proofs/blob/main/ConnesRigidity.lean#L33616)

```lean
theorem vectorGCD_dvd (v : V) (i : Fin 4) :
    vectorGCD v ∣ v i := by
  exact Finset.gcd_dvd (Finset.mem_univ i)
```

**它说了什么**：一个有 4 个分量的向量 v，它 4 个分量的最大公因数能整除其中每一个分量。

用整数举例：v = (12, 18, 30, 42)，最大公因数是 6，而 6 能整除 12、18、30、42 中的每一个。

在这个文件里，分量不是整数，而是系数只取 0 和 1 的多项式（系数按模 2 计算），但"最大公因数整除每一项"的道理完全一样。

**为什么成立**：这就是最大公因数的定义，它首先得是一个公因数，也就是能整除每一个数。Lean 的证明只是说明"第 i 个分量确实在这 4 个分量之中"，然后引用 Mathlib 里最大公因数的这条基本性质。

**在证明里的位置**：它被 `coordinateIdeal_eq_span_vectorGCD` 和 `vectorGCD_natDegree_lt` 用到。证明里需要数某些"本原向量"（分量没有公因数的向量）的个数，最大公因数是判断一个向量是否本原的工具。

---

## 5. 积和式的公式下界

**原题大意**：积和式（permanent）和行列式很像，只是展开时所有项都取加号。证明了：任何只用加减乘除计算 n×n 积和式的公式都很长，其中变量出现的次数至少是 n⁴ / (192 log₂ n)（n ≥ 32 时）。

**叶子定理**：`leafCount_eq_internalGateCount_add_one`，[Permanent.lean 第 20563 行](https://github.com/bil022/ten-proofs/blob/main/Permanent.lean#L20563)

```lean
theorem leafCount_eq_internalGateCount_add_one (f : RationalFormula ι R) :
    leafCount f = internalGateCount f + 1 := by
  induction f <;>
    simp_all [leafCount, internalGateCount, Nat.add_assoc, Nat.add_left_comm,
      Nat.add_comm]
```

**它说了什么**：任何算式里，"数字和字母"的个数总是比"运算符号"的个数多 1。

把算式 (x + y) × (z − 3) 画成一棵树：

```
          ×
        /   \
       +     −
      / \   / \
     x   y z   3
```

- 叶子（变量或常数）：x、y、z、3，共 4 个。
- 运算（加减乘除）：+、−、×，共 3 个。

4 = 3 + 1。换任何算式都成立。

**为什么成立**：用数学归纳法，Lean 的证明里写的正是 `induction`。

- **最简单的算式**只有一个字母或数字：1 个叶子，0 个运算，1 = 0 + 1。
- **由两个小算式 f、g 用一个运算拼成**：如果 f 有 a+1 个叶子、a 个运算，g 有 b+1 个叶子、b 个运算，那么拼起来后叶子有 (a+1) + (b+1) = a+b+2 个，运算有 a+b+1 个（多了中间那一个），仍然是叶子比运算多 1。

**在证明里的位置**：它被 `permanent_size_bounds_of_fourth_power` 用到。主定理要证明"公式必须很长"，就需要在不同的长度度量之间换算，这条等式就是最基本的换算关系。

---

## 6. 量子并行重复

**原题大意**：两个玩家合作玩一个游戏，各自只能看到自己的问题。如果同时玩很多局，全部获胜的概率会怎样下降？证明说明：即使玩家共享量子纠缠，全胜的概率也会随局数呈指数下降。

**叶子定理**：`fairPartitionWeight_sum`，[QuantumParallelRepetition.lean 第 19139 行](https://github.com/bil022/ten-proofs/blob/main/QuantumParallelRepetition.lean#L19139)

```lean
def fairPartitionWeight (α : Type*) [Fintype α] : ℝ :=
  ((2 : ℝ) ^ Fintype.card α)⁻¹

theorem fairPartitionWeight_sum :
    (∑ _s : Finset α, fairPartitionWeight α) = 1 := by
  simp [fairPartitionWeight, Fintype.card_finset]
```

**它说了什么**：一个有 n 个元素的集合，给它的每个子集都分配概率 1/2ⁿ，所有子集的概率加起来恰好是 1。

**为什么成立**：n 个元素的集合一共有 2ⁿ 个子集，因为每个元素都有"选"和"不选"两种可能。2ⁿ 个 1/2ⁿ 加起来就是 1。

这相当于"对每个元素抛一次硬币，正面就放进子集"，每个子集被抽到的概率都是 1/2ⁿ。

**在证明里的位置**：它被 `reversePartition_relativeEntropy_budget` 等两条定理用到。证明里要随机地把所有局分成两组来分析，这条定理保证这种随机分组确实是一个合法的概率分布。

---

## 7. 最近向量问题的困难性

**原题大意**：给定一个格（空间中规则排列的点阵）和一个目标点，找离目标最近的格点。证明了：即使只要求近似到多项式倍数以内，这个问题也是 NP 困难的，也就是说不太可能有快速算法。

**叶子定理**：`binary_add_self`，[GapCVP.lean 第 62385 行](https://github.com/bil022/ten-proofs/blob/main/GapCVP.lean#L62385)

```lean
theorem binary_add_self (value : ZMod 2) : value + value = 0 := by
  have htwo : (2 : ZMod 2) = 0 := by decide
  rw [← two_mul, htwo, zero_mul]
```

**它说了什么**：在"模 2 算术"里，任何数加上它自己都等于 0。

模 2 算术里只有 0 和 1 两个数，加法看奇偶：0 + 0 = 0，0 + 1 = 1，1 + 1 = 2，而 2 是偶数，算作 0。这和计算机里的"异或"运算是一回事。

**为什么成立**：Lean 的证明分三步：

1. 先确认在模 2 里 2 = 0（`decide` 让计算机直接验证）。
2. 把 x + x 改写成 2 × x。
3. 2 × x = 0 × x = 0。

**在证明里的位置**：它被 `addRow_twice` 等三条定理用到。`addRow_twice` 说的是：在模 2 的高斯消元里，把同一行加到另一行上两次，等于什么都没做。证明里要用模 2 线性方程组来编码逻辑问题，这类性质会反复用到。

---

## 8. Ehrhart 体积猜想

**原题大意**：一个凸体（没有凹陷的立体）的重心在原点，并且内部只有原点这一个整数坐标点。这样的凸体体积最大是多少？证明在每个维数下都给出了精确的最大值。

**叶子定理**：`sourceJointIntegral_sin_sq_two_pi`，[EhrhartVolumeInequality.lean 第 29481 行](https://github.com/bil022/ten-proofs/blob/main/EhrhartVolumeInequality.lean#L29481)

```lean
theorem sourceJointIntegral_sin_sq_two_pi :
    (∫ θ in 0..2 * Real.pi, Real.sin θ ^ 2) = Real.pi := by
  rw [integral_sin_sq]
  simp [Real.sin_two_pi, Real.cos_two_pi]
```

**它说了什么**：

$$\int_0^{2\pi} \sin^2\theta \, d\theta = \pi$$

**为什么成立**：用二倍角公式 sin²θ = (1 − cos 2θ) / 2：

$$\int_0^{2\pi} \frac{1 - \cos 2\theta}{2}\, d\theta = \left[\frac{\theta}{2} - \frac{\sin 2\theta}{4}\right]_0^{2\pi} = \pi - 0 = \pi$$

还有一个不用计算的理解方式：sin²θ 和 cos²θ 在一整圈上的平均值相同，而它们加起来恒等于 1，所以各自的平均值都是 1/2。平均值 1/2 乘以区间长度 2π，就是 π。

Lean 的证明先调用 Mathlib 里 sin² 积分的一般公式，再代入 sin 2π = 0、cos 2π = 1 化简。

**在证明里的位置**：它被 `sourceJointCircleQuadratic_average` 用到，用来计算二次式在一个圆周上的平均值。

---

## 9. 多色 Ramsey 数

**原题大意**：用 k 种颜色给完全图的每条边染色，顶点至少要有多少个，才能保证一定出现三条边同色的三角形？这个最小顶点数记作 R(k)。证明了 R(k) 增长得比任何指数函数都快，解决了 Erdős 第 183 号问题。

**叶子定理**：`forcesMonochromaticTriangle_zero`，[MulticolorTriangleRamsey.lean 第 236 行](https://github.com/bil022/ten-proofs/blob/main/MulticolorTriangleRamsey.lean#L236)

```lean
theorem forcesMonochromaticTriangle_zero :
    ForcesMonochromaticTriangle 2 0 := by
  intro C _
  exact Fin.elim0 (C.get (0 : Fin 2) (1 : Fin 2) (by decide))
```

**它说了什么**：用 0 种颜色给 2 个顶点的完全图染色，"每一种染色方式"都会出现同色三角形。

听起来很荒谬：2 个顶点连三角形都没有。

**为什么成立**：关键在于，用 0 种颜色根本没法染色。2 个顶点之间有一条边，这条边必须染一种颜色，可是一种颜色都没有。所以"染色方式"一个都不存在。

"所有不存在的东西都满足某性质"在逻辑上是真的，这叫**空真**。就像"这个房间里所有的独角兽都是紫色的"：房间里没有独角兽，这句话就不会错。

Lean 的证明正是这样：假设有一种染色 C，取出顶点 0 和 1 之间那条边的颜色，这个颜色得是"0 种颜色"里的一种，而那是一个空集，`Fin.elim0` 由此直接推出矛盾。

**在证明里的位置**：它是 `exists_forcesMonochromaticTriangle` 的归纳起点。那条定理要证明对每个 k，R(k) 都存在，用的是对颜色数 k 做数学归纳，k = 0 的情形就是这条叶子。

---

## 10. 极值图论中的两个猜想

**原题大意**：极值图论问：一个图在不包含某种子图的前提下，最多能有多少条边？证明给出了"紧性猜想"和"退化性猜想"的反例，解决了 Erdős 第 146 和 180 号问题。这个文件有两个主定理，所以这里各取一个叶子。

### 10a. 紧性猜想

**叶子定理**：`booleanCut_isBipartite`，[CompactnessAndDegeneracy.lean 第 83 行](https://github.com/bil022/ten-proofs/blob/main/CompactnessAndDegeneracy.lean#L83)

```lean
lemma booleanCut_isBipartite {V : Type*} (G : SimpleGraph V)
    (color : V → Bool) : (booleanCut G color).IsBipartite := by
  simpa using (SimpleGraph.Coloring.mk
    (G := booleanCut G color) color (fun h => h.2)).colorable
```

**它说了什么**：给一个图的每个顶点随便涂上红色或蓝色，然后只保留两端颜色不同的边（红连蓝），删掉同色的边。剩下的图一定是**二部图**。

二部图是指顶点能分成两组，所有边都在两组之间、组内没有边。

**为什么成立**：两组就是"红色顶点"和"蓝色顶点"。剩下的每条边都是一红一蓝，所以都在两组之间，组内一条边都没有。Lean 的证明就是把这个红蓝涂色当作现成的"二着色"交给 Mathlib，由它得出"是二部图"。

**在证明里的位置**：它被 `exists_bipartite_half_edges` 用到。那是一个经典结论：任何图都有一个二部子图，至少保留了原图一半的边。

### 10b. 退化性猜想

**叶子定理**：`twelve_sevenths_lt_sqrt_three`，[CompactnessAndDegeneracy.lean 第 9396 行](https://github.com/bil022/ten-proofs/blob/main/CompactnessAndDegeneracy.lean#L9396)

```lean
theorem twelve_sevenths_lt_sqrt_three : (12 : ℝ) / 7 < Real.sqrt 3 := by
  have hsqrt_nonneg : 0 ≤ Real.sqrt (3 : ℝ) := Real.sqrt_nonneg 3
  have hsqrt_sq : (Real.sqrt (3 : ℝ)) ^ 2 = 3 := by
    exact Real.sq_sqrt (by positivity)
  nlinarith
```

**它说了什么**：12/7 < √3。

（12/7 ≈ 1.714，√3 ≈ 1.732。）

**为什么成立**：两边都是正数，比较平方就行：(12/7)² = 144/49，而 3 = 147/49。因为 144 < 147，所以 12/7 < √3。

Lean 的证明先准备两个事实，√3 ≥ 0 和 (√3)² = 3，然后交给 `nlinarith`（一个能处理不等式的自动工具）完成推理。

**在证明里的位置**：它被 `tau_pos` 等两条定理用到。证明里有一个关键常数 τ = (√3 − 1)/2，需要知道它是正数，以及另一个比值大于 1，都要靠 √3 的精确估计。

---

## 想继续往下读？

在依赖图里找到这些叶子，顺着箭头往右走，就能看到它们被哪些更复杂的定理用到。依赖图在 [`en/svg`](en/svg) 和 [`zh/svg`](zh/svg)，读图方法见[说明](README.zh.md)。
