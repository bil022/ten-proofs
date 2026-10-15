# Start with the simplest leaves: one from each proof

[中文版](leaves.zh.md) · [Back to the overview](README.md)

All ten proofs are long, and reading them straight through is close to impossible. But at the far left of every dependency graph there is a set of "leaves": theorems that depend on no other theorem in the same file, only on what Lean and Mathlib already provide. The leaves are the foundations of each proof, and some are simple enough for a high-school student to follow.

For each problem below I picked one such leaf and explain three things: what it says, why it is true, and which theorem in the proof uses it.

Selection rules: only high-school mathematics, a proof of a few lines at most, and the leaf must actually be on the path to the main theorem (each one appears in that main theorem's dependency graph).

One caveat before you start: understanding a leaf is not understanding the main theorem. A leaf is often dozens of layers away from it. These are only a place to start reading.

The link under each heading goes to the corresponding line of the Lean source on GitHub.

---

## 1. High-dimensional sphere packing

**The problem**: in high-dimensional space, place non-overlapping balls of equal size. What fraction of space can they fill at most? The proof gives a better upper bound.

**Leaf theorem**: `IsRadial.even`, [SpherePacking.lean line 270](https://github.com/bil022/ten-proofs/blob/main/SpherePacking.lean#L270)

```lean
theorem IsRadial.even {d : ℕ} {f : TestFunction d}
    (hf : IsRadial f) : IsEven f := by
  intro x
  exact hf (-x) x (by simp)
```

**What it says**: a radial function is always an even function.

- **Radial function**: its value depends only on the distance `‖x‖` from the point to the origin. Points at the same distance get the same value. For example f(x) = x² on the number line is radial, and so is f(x, y) = x² + y² in the plane.
- **Even function**: f(−x) = f(x).

**Why it is true**: the points x and −x are at the same distance from the origin, `‖−x‖ = ‖x‖`. A radial function only looks at the distance, so f(−x) = f(x). The Lean proof is exactly this one sentence: apply the definition of "radial" to the two points −x and x, and let `simp` check that the distances are equal.

**Where it is used**: by `fourier_sq_of_radial`. The Cohn–Elkies method for sphere packing needs an auxiliary function satisfying special conditions. These auxiliary functions are radial, and the proof uses their symmetry over and over; this is the most basic such fact.

---

## 2. Binary and spherical codes

**The problem**: take "codewords" that are strings of 0s and 1s of length n, and require any two codewords to differ in at least d positions (so transmission errors can be detected or corrected). How many codewords can you choose at most? The proof gives a stronger upper bound than was known before.

**Leaf theorem**: `hammingDist_self`, [MetricCodes.lean line 18](https://github.com/bil022/ten-proofs/blob/main/MetricCodes.lean#L18)

```lean
def hammingDist {n : ℕ} (x y : BinaryWord n) : ℕ :=
  (Finset.univ.filter fun i => x i ≠ y i).card

@[simp] theorem hammingDist_self {n : ℕ} (x : BinaryWord n) :
    hammingDist x x = 0 := by
  simp [hammingDist]
```

**What it says**: first the definition. The **Hamming distance** between two 0/1 strings is the number of positions where they differ. For example:

```
1 0 1 1 0
1 1 1 0 0
  ↑   ↑      2 positions differ, Hamming distance = 2
```

The theorem says: a string is at Hamming distance 0 from itself.

**Why it is true**: a string agrees with itself in every position, so the set of "positions that differ" is empty, and the empty set has 0 elements.

This looks too obvious to need a proof, but in a machine-checked proof every step has to be written down explicitly before later reasoning can use it.

**Where it is used**: by `hammingCorrelation_self`. The whole proof studies Hamming distances between codewords; this is where all of it starts.

---

## 3. Non-sofic groups

**The problem**: a "sofic group" is one that can be approximately modelled by permutations (rearrangements) of finitely many elements. For a long time nobody knew whether every group is sofic. The proof constructs a group that is not sofic, answering the question.

**Leaf theorem**: `permutationDistance_triangle`, [NonSoficGroup.lean line 7723](https://github.com/bil022/ten-proofs/blob/main/NonSoficGroup.lean#L7723)

```lean
theorem permutationDistance_triangle {V : Type*}
    [Fintype V] [DecidableEq V] (p q r : Equiv.Perm V) :
    permutationDistance p r ≤ permutationDistance p q + permutationDistance q r :=
  hammingDist_triangle _ _ _
```

**What it says**: first define a distance between two permutations: count how many elements the two permutations send to different places. For example, rearranging {1, 2, 3, 4}:

```
p:  1→2  2→1  3→3  4→4
q:  1→2  2→3  3→1  4→4
       they differ at elements 2 and 3, distance = 2
```

The theorem says this distance satisfies the **triangle inequality**: d(p, r) ≤ d(p, q) + d(q, r), just as two sides of a triangle add up to more than the third.

**Why it is true**: suppose p and r differ at an element x, that is, p(x) ≠ r(x). Then q(x) cannot equal both p(x) and r(x), so either p(x) ≠ q(x) or q(x) ≠ r(x). In other words, every element where p and r differ is counted at least once on the right-hand side. The Lean proof simply reuses the triangle inequality for Hamming distance that Mathlib already has.

**Where it is used**: by `permutationDistance_mul_le` and two other theorems. The "approximately" in "approximately modelled by permutations" is measured with this distance, and the triangle inequality is what lets many small errors be added up and bounded.

---

## 4. Connes's rigidity conjecture

**The problem**: Connes conjectured that a certain class of groups is completely determined by an associated operator algebra. The proof gives a counterexample: infinitely many different groups whose operator algebras are all the same.

**Leaf theorem**: `vectorGCD_dvd`, [ConnesRigidity.lean line 33616](https://github.com/bil022/ten-proofs/blob/main/ConnesRigidity.lean#L33616)

```lean
theorem vectorGCD_dvd (v : V) (i : Fin 4) :
    vectorGCD v ∣ v i := by
  exact Finset.gcd_dvd (Finset.mem_univ i)
```

**What it says**: for a vector v with 4 components, the greatest common divisor of its 4 components divides each of them.

With integers: v = (12, 18, 30, 42) has greatest common divisor 6, and 6 divides each of 12, 18, 30 and 42.

In this file the components are not integers but polynomials whose coefficients are only 0 or 1 (with coefficient arithmetic done mod 2). The fact "the gcd divides every entry" holds in exactly the same way.

**Why it is true**: this is the definition of the greatest common divisor: before anything else it must be a common divisor, so it divides each entry. The Lean proof only notes that "component i is one of these 4 components" and then cites this basic property of gcd from Mathlib.

**Where it is used**: by `coordinateIdeal_eq_span_vectorGCD` and `vectorGCD_natDegree_lt`. The proof needs to count certain "primitive vectors" (vectors whose components have no common factor), and the gcd is the tool for deciding whether a vector is primitive.

---

## 5. A formula lower bound for the permanent

**The problem**: the permanent is much like the determinant, except that every term in its expansion has a plus sign. The proof shows that any formula computing the n×n permanent using only addition, subtraction, multiplication and division must be long: its variables must occur at least n⁴ / (192 log₂ n) times (for n ≥ 32).

**Leaf theorem**: `leafCount_eq_internalGateCount_add_one`, [Permanent.lean line 20563](https://github.com/bil022/ten-proofs/blob/main/Permanent.lean#L20563)

```lean
theorem leafCount_eq_internalGateCount_add_one (f : RationalFormula ι R) :
    leafCount f = internalGateCount f + 1 := by
  induction f <;>
    simp_all [leafCount, internalGateCount, Nat.add_assoc, Nat.add_left_comm,
      Nat.add_comm]
```

**What it says**: in any arithmetic expression, the number of "numbers and letters" is always one more than the number of operation symbols.

Draw the expression (x + y) × (z − 3) as a tree:

```
          ×
        /   \
       +     −
      / \   / \
     x   y z   3
```

- Leaves (variables or constants): x, y, z, 3, that is 4.
- Operations (+, −, ×, ÷): +, −, ×, that is 3.

4 = 3 + 1, and the same holds for any expression.

**Why it is true**: by mathematical induction, which is exactly the `induction` in the Lean proof.

- **The simplest expression** is a single letter or number: 1 leaf, 0 operations, and 1 = 0 + 1.
- **Joining two smaller expressions f and g with one operation**: if f has a+1 leaves and a operations, and g has b+1 leaves and b operations, then the combined expression has (a+1) + (b+1) = a+b+2 leaves and a+b+1 operations (one more, the one in the middle). Leaves still exceed operations by exactly 1.

**Where it is used**: by `permanent_size_bounds_of_fourth_power`. The main theorem has to show that "the formula must be long", which requires converting between different ways of measuring a formula's size; this identity is the most basic such conversion.

---

## 6. Quantum parallel repetition

**The problem**: two players cooperate in a game; each sees only their own question. If they play many rounds at once, how fast does the probability of winning every round fall? The proof shows that even if the players share quantum entanglement, the probability of winning all rounds falls exponentially in the number of rounds.

**Leaf theorem**: `fairPartitionWeight_sum`, [QuantumParallelRepetition.lean line 19139](https://github.com/bil022/ten-proofs/blob/main/QuantumParallelRepetition.lean#L19139)

```lean
def fairPartitionWeight (α : Type*) [Fintype α] : ℝ :=
  ((2 : ℝ) ^ Fintype.card α)⁻¹

theorem fairPartitionWeight_sum :
    (∑ _s : Finset α, fairPartitionWeight α) = 1 := by
  simp [fairPartitionWeight, Fintype.card_finset]
```

**What it says**: for a set with n elements, give each of its subsets probability 1/2ⁿ. Then the probabilities of all subsets add up to exactly 1.

**Why it is true**: a set with n elements has 2ⁿ subsets, because each element is either "in" or "out". Adding 2ⁿ copies of 1/2ⁿ gives 1.

This is the same as "flip a coin for each element and put it in the subset on heads": every subset comes up with probability 1/2ⁿ.

**Where it is used**: by `reversePartition_relativeEntropy_budget` and one other theorem. The proof randomly splits the rounds into two groups to analyse them, and this theorem guarantees that the random split really is a valid probability distribution.

---

## 7. Hardness of the closest vector problem

**The problem**: given a lattice (a regularly spaced grid of points in space) and a target point, find the lattice point closest to the target. The proof shows that even approximating the answer to within a polynomial factor is NP-hard, meaning a fast algorithm is unlikely to exist.

**Leaf theorem**: `binary_add_self`, [GapCVP.lean line 62385](https://github.com/bil022/ten-proofs/blob/main/GapCVP.lean#L62385)

```lean
theorem binary_add_self (value : ZMod 2) : value + value = 0 := by
  have htwo : (2 : ZMod 2) = 0 := by decide
  rw [← two_mul, htwo, zero_mul]
```

**What it says**: in "mod 2 arithmetic", any number added to itself is 0.

Mod 2 arithmetic has only the numbers 0 and 1, and addition only tracks even and odd: 0 + 0 = 0, 0 + 1 = 1, and 1 + 1 = 2, which is even and so counts as 0. This is the same as the "exclusive or" (XOR) operation in computers.

**Why it is true**: the Lean proof has three steps:

1. Confirm that 2 = 0 in mod 2 arithmetic (`decide` has the computer check it directly).
2. Rewrite x + x as 2 × x.
3. 2 × x = 0 × x = 0.

**Where it is used**: by `addRow_twice` and two other theorems. `addRow_twice` says that in Gaussian elimination mod 2, adding the same row to another row twice is the same as doing nothing. The proof encodes logic problems as systems of linear equations mod 2, so facts like this come up again and again.

---

## 8. Ehrhart's volume conjecture

**The problem**: a convex body (a solid with no dents) has its centre of mass at the origin, and the origin is the only point with integer coordinates in its interior. How large can its volume be? The proof gives the exact maximum in every dimension.

**Leaf theorem**: `sourceJointIntegral_sin_sq_two_pi`, [EhrhartVolumeInequality.lean line 29481](https://github.com/bil022/ten-proofs/blob/main/EhrhartVolumeInequality.lean#L29481)

```lean
theorem sourceJointIntegral_sin_sq_two_pi :
    (∫ θ in 0..2 * Real.pi, Real.sin θ ^ 2) = Real.pi := by
  rw [integral_sin_sq]
  simp [Real.sin_two_pi, Real.cos_two_pi]
```

**What it says**:

$$\int_0^{2\pi} \sin^2\theta \, d\theta = \pi$$

**Why it is true**: use the double-angle formula sin²θ = (1 − cos 2θ) / 2:

$$\int_0^{2\pi} \frac{1 - \cos 2\theta}{2}\, d\theta = \left[\frac{\theta}{2} - \frac{\sin 2\theta}{4}\right]_0^{2\pi} = \pi - 0 = \pi$$

There is also a way to see it without calculation: over a full turn, sin²θ and cos²θ have the same average, and they always add up to 1, so each averages 1/2. An average of 1/2 times an interval of length 2π gives π.

The Lean proof first calls Mathlib's general formula for the integral of sin², then simplifies using sin 2π = 0 and cos 2π = 1.

**Where it is used**: by `sourceJointCircleQuadratic_average`, to compute the average of a quadratic expression around a circle.

---

## 9. Multicolor Ramsey numbers

**The problem**: colour every edge of a complete graph with k colours. How many vertices are needed to guarantee a triangle whose three edges all have the same colour? Call this smallest number of vertices R(k). The proof shows R(k) grows faster than any exponential function, settling Erdős problem 183.

**Leaf theorem**: `forcesMonochromaticTriangle_zero`, [MulticolorTriangleRamsey.lean line 236](https://github.com/bil022/ten-proofs/blob/main/MulticolorTriangleRamsey.lean#L236)

```lean
theorem forcesMonochromaticTriangle_zero :
    ForcesMonochromaticTriangle 2 0 := by
  intro C _
  exact Fin.elim0 (C.get (0 : Fin 2) (1 : Fin 2) (by decide))
```

**What it says**: if you colour the complete graph on 2 vertices with 0 colours, then "every way of colouring it" contains a monochromatic triangle.

That sounds absurd: 2 vertices cannot even form a triangle.

**Why it is true**: the key is that with 0 colours there is no way to colour at all. The 2 vertices are joined by one edge, that edge must get a colour, and there are no colours. So there are no colourings whatsoever.

"Everything that does not exist has property X" is true in logic; this is called being **vacuously true**. Think of "every unicorn in this room is purple": there are no unicorns in the room, so the sentence cannot be wrong.

The Lean proof does exactly this: assume a colouring C, take the colour of the edge between vertices 0 and 1, and note that this colour would have to be one of "0 colours", an empty set. `Fin.elim0` derives a contradiction from that directly.

**Where it is used**: it is the base case of the induction in `exists_forcesMonochromaticTriangle`. That theorem proves R(k) exists for every k by induction on the number of colours k, and the case k = 0 is this leaf.

---

## 10. Two conjectures in extremal graph theory

**The problem**: extremal graph theory asks how many edges a graph can have if it must avoid a certain subgraph. The proof gives counterexamples to the "compactness conjecture" and the "degeneracy conjecture", settling Erdős problems 146 and 180. This file has two main theorems, so there is one leaf for each.

### 10a. The compactness conjecture

**Leaf theorem**: `booleanCut_isBipartite`, [CompactnessAndDegeneracy.lean line 83](https://github.com/bil022/ten-proofs/blob/main/CompactnessAndDegeneracy.lean#L83)

```lean
lemma booleanCut_isBipartite {V : Type*} (G : SimpleGraph V)
    (color : V → Bool) : (booleanCut G color).IsBipartite := by
  simpa using (SimpleGraph.Coloring.mk
    (G := booleanCut G color) color (fun h => h.2)).colorable
```

**What it says**: paint each vertex of a graph red or blue however you like, then keep only the edges whose two ends have different colours (red to blue) and delete the edges between same-coloured vertices. What remains is always a **bipartite graph**.

A bipartite graph is one whose vertices can be split into two groups so that every edge goes between the groups and no edge stays inside a group.

**Why it is true**: the two groups are "the red vertices" and "the blue vertices". Every remaining edge is red-to-blue, so it goes between the groups, and no edge is left inside a group. The Lean proof hands this red/blue painting to Mathlib as a ready-made "2-colouring" and lets Mathlib conclude that the graph is bipartite.

**Where it is used**: by `exists_bipartite_half_edges`, a classic result: every graph has a bipartite subgraph that keeps at least half of its edges.

### 10b. The degeneracy conjecture

**Leaf theorem**: `twelve_sevenths_lt_sqrt_three`, [CompactnessAndDegeneracy.lean line 9396](https://github.com/bil022/ten-proofs/blob/main/CompactnessAndDegeneracy.lean#L9396)

```lean
theorem twelve_sevenths_lt_sqrt_three : (12 : ℝ) / 7 < Real.sqrt 3 := by
  have hsqrt_nonneg : 0 ≤ Real.sqrt (3 : ℝ) := Real.sqrt_nonneg 3
  have hsqrt_sq : (Real.sqrt (3 : ℝ)) ^ 2 = 3 := by
    exact Real.sq_sqrt (by positivity)
  nlinarith
```

**What it says**: 12/7 < √3.

(12/7 ≈ 1.714 and √3 ≈ 1.732.)

**Why it is true**: both sides are positive, so compare their squares: (12/7)² = 144/49, while 3 = 147/49. Since 144 < 147, we get 12/7 < √3.

The Lean proof first prepares two facts, √3 ≥ 0 and (√3)² = 3, and then hands them to `nlinarith` (an automatic tool for inequalities) to finish.

**Where it is used**: by `tau_pos` and one other theorem. The proof has a key constant τ = (√3 − 1)/2 and needs to know that it is positive and that another ratio exceeds 1; both rely on a precise estimate of √3.

---

## Want to keep going?

Find these leaves in the dependency graphs and follow the arrows to the right to see which more complex theorems use them. The graphs are in [`en/svg`](en/svg) and [`zh/svg`](zh/svg); how to read them is explained in the [overview](README.md).
