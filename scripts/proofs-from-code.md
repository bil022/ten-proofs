# What the code alone shows: how the ten proofs are organised

[中文版](proofs-from-code.zh.md) · [Back to the overview](README.md) · [Explained from the paper](proofs.md) · [Start with the simplest leaves](leaves.md)

This summary is based **only on the Lean code itself**, without consulting the paper. It draws on four sources:

1. **Theorem statements**: the main theorems and the definitions they use, translated directly from the source.
2. **The dependency graph**: extracted from the compiled files with `DeclGraph.lean`, showing which theorem uses which.
3. **Declaration names**: the Lean files contain no comments at all, so the names are the only explanation the authors left.
4. **Mathlib usage statistics**: `LibraryUse.lean` counts which parts of Mathlib each file uses, which shows what areas of mathematics it relies on.

Below, the "spine" of a proof means the chain you get by starting at the main theorem and, at each step, moving down to the dependency that supports the most theorems. It roughly follows the heaviest line of reasoning in the proof. **Readings of what the names mean are my inferences**; anything inferred from names alone is marked "judging by the names".

---

## Overview

| File | Lines | Declarations | Theorems / definitions | Share used by the main theorem | Main areas of Mathlib used |
|---|---:|---:|---|---:|---|
| `SpherePacking` | 55,617 | 2,284 | 1,879 / 395 | 92% | special functions, calculus, complex analysis, integration |
| `MetricCodes` | 114,407 | 5,778 | 4,386 / 1,365 | 96% | multivariate polynomials, inner product spaces, special functions, matrices |
| `NonSoficGroup` | 34,441 | 1,501 | 1,108 / 371 | 100% | inner product spaces, normed spaces, partitions |
| `ConnesRigidity` | 37,375 | 2,918 | 2,032 / 856 | 94% | polynomials, topological algebra, inner product spaces, measure theory |
| `Permanent` | 27,564 | 1,434 | 983 / 434 | **23%** | multivariate polynomials, ideals, regular sequences |
| `QuantumParallelRepetition` | 70,981 | 2,739 | 1,849 / 873 | 99% | matrices (positive semidefinite, trace, Kronecker product), logarithms |
| `GapCVP` | 130,431 | 8,230 | 3,719 / **4,458** | 95% | **Turing machines**, polynomials, valuation theory |
| `EhrhartVolumeInequality` | 55,756 | 2,396 | 1,903 / 490 | 99% | differentiation (Fréchet derivatives), integration, measure theory |
| `MulticolorTriangleRamsey` | 3,054 | 146 | 101 / 44 | 92% | logarithms and powers, graph theory |
| `CompactnessAndDegeneracy` | 18,589 | 957 | 665 / 288 | 99% | graph theory, logarithms, binary entropy, finite-dimensional linear algebra |

"Share used by the main theorem" is measured in lines of source taken up by the declarations.

Some things common to all files that the code shows directly:

- **No back doors**: across all ten files, `sorry`, `admit`, `axiom`, `native_decide`, `unsafe` and `implemented_by` each occur 0 times. Every conclusion is fully checked by the Lean kernel from the three standard axioms, with no reliance on the compiler running code to "trust" a computed result.
- **No comments**: not a single one. Names average 22 to 36 characters, the longest is 114 characters, and the names do the job of documentation.
- **The main theorems use almost the whole file**: except in `Permanent`, over 90% of each file serves its main theorem. `Permanent` is the exception because the file also contains a separate, larger result (see section 5).
- **Different tools**: `GapCVP` has more definitions than theorems because it defines a great many Turing machines. The analysis-heavy files (sphere packing, Ehrhart) make heavy use of `linarith`, `positivity` and `calc` for inequality reasoning; the combinatorial and computational files (`GapCVP`, `MetricCodes`) make heavy use of `omega`, `decide` and `induction`.

---

## 1. High-dimensional sphere packing (`SpherePacking.lean`)

**What the main theorem says**: `sharpFullCohnElkiesManuscriptConclusions` takes no arguments; it asserts that a structure of ten conclusions, `SharpFullCohnElkiesManuscriptConclusions`, holds. The central ones are:

- `linear_program_root`: the d-th root of `fullLinearProgram d` tends to √(e/(2π)) as d → ∞.
- `root_before_infimum`: take the d-th root of a certain ratio (`fullQuotient`) over all "admissible functions" (`FullAdmissible d`); its infimum divided by √d tends to 1/π.
- `universal_nonnegative_delta`: a uniform lower bound that holds for every admissible function.
- The rest restate the same conclusion with base-2 logarithms, with explicit error terms, and so on.

In other words, the main theorem is an asymptotic statement about **the optimal value of a linear program**.

**Code layout**: the `CohnElkies` namespace takes up 46,176 lines and 1,818 declarations, by far the bulk of the file.

**Spine** (from the main theorem downward):

```
sharpFullCohnElkiesManuscriptConclusions
 ← SharpFullCohnElkiesManuscriptConclusions.components   (split into the ten parts)
 ← SharpFullCohnElkiesManuscriptConclusions.ofRadial     (obtained from the radial case)
 ← CohnElkies.sharpCohnElkiesManuscriptConclusions
 ← CohnElkies.exists_manuscriptUniversalPackingIsLittleO
 ← CohnElkies.sharpPackingRootAsymptotic
 ← CohnElkies.sharpAsymptotics
 ← CohnElkies.sharpAsymptotics_of_saddleSourceEventualSigns
 ← CohnElkies.uniformAntiFourierSignRadius
```

Judging by the names: the problem is first reduced to **radial functions** (`ofRadial`, `fullLinearProgram_eq_radial`), and the core is `sharpAsymptotics`. It rests on two parts. One is about the "sign radius of anti-Fourier functions" (`uniformAntiFourierSignRadius`: for a function with f̂ = −f, the radius beyond which it stops changing sign). The other is a function built with a "saddle" (`saddleSource...`) and its eventual signs (`EventualSigns`), that is, the construction of a concrete good function.

**What else the file contains**: `PackingBounds.PackingBridge.sphere_packing_sharp_asymptotic_upper` asserts that the actual **sphere-packing constant** is at most (√(e/(2π)) + o(1))^d. It uses 264 additional declarations from namespaces such as `SchwartzMap.PoissonSummation` (the Poisson summation formula) and `PeriodicSpherePacking` (periodic packings). This part connects the linear program to actual packing density, but it is **outside the dependencies of the listed main theorem**.

**Mathematics used**: the most-used parts of Mathlib are special functions (powers, trigonometric functions, logarithms, the Gamma function), Fréchet derivatives, Bochner and interval integrals, and the complex exponential. Names like `Mellin`, `saddle`, `contour` and `Gamma` appear throughout, indicating the Mellin transform and saddle-point estimates for complex integrals.

---

## 2. Binary and spherical codes (`MetricCodes.lean`)

This file has two main theorems.

### 2a. Binary codes: `binaryRate_lt_mrrw`

**What the main theorem says**: for 0 < d < 1/2, `binaryRate d < mrrwRate d`.

- `binaryRate d` is defined as the lim sup of log₂ of "the largest number of codewords in a binary code of length n with minimum distance at least ⌈dn⌉", divided by n: the upper limit of the code rate.
- `mrrwRate` is the minimum of an objective function `mrrwObjective`: the classical MRRW bound.

So the theorem says the true upper limit of the code rate is **strictly below** the MRRW bound.

**Spine**:

```
binaryRate_lt_mrrw
 ← binaryRate_le_combinedVariationalRate        (rate ≤ a "combined variational rate")
 ← binaryRate_le_combinedVariationalRate_of_projectionGrams
 ← binaryRate_le_shellRate_of_projectionGrams
 ← SpectralAsymptotics.eventually_spectralGap_lt
 ← SpectralAsymptotics.eventually_topEigenvalue_gt
 ← SpectralAsymptotics.tendsto_terminalRayleigh
 ← SpectralAsymptotics.tendsto_johnsonEdge
```

Another branch, `strict_mrrw2`, proves "combined variational rate < MRRW bound", split into cases underneath: `mrrw_endpoint_dichotomy`, `variationalRate_lt_mrrw_of_interior` (optimum in the interior) and `combinedVariationalRate_lt_mrrw_of_endpoint` (optimum at the endpoint).

Judging by the names, the proof has two steps:

1. "Projection Gram matrices" (`projectionGram`) give an upper bound on the number of codewords that depends on the **largest eigenvalue** of a certain matrix (`topEigenvalue`, the `Rayleigh` quotient, the spectral gap `spectralGap`). These matrices come from the Johnson structure (`johnsonEdge`), that is, binary strings of fixed weight.
2. The resulting rate is then shown to be strictly better than MRRW, with a case split on where the optimum lies.

### 2b. Spherical codes: `strict_hierarchy`

**What the main theorem says**: for 0 < s < 1, there is a sequence of rates `levelRate r s` (r = 0, 1, 2, …) with each level strictly below the previous one, and a "localized" version satisfying

```
spherical code rate ≤ localizedHierarchyRate < localizedLevelRate 1 < localizedRowRate
                    < localizedLevelRate 0 = classicalLocalizedRate
```

That is, a **strictly improving hierarchy** whose level 0 equals the classical bound.

**Spine**:

```
strict_hierarchy
 ← fixedLevelHierarchyCodeBound
 ← fixedLevelHierarchyCodeBound_of_actualCharacteristicMinor
 ← … (several layers of sufficient conditions about Fischer recurrences and Young box representations)
 ← fixedLevelHierarchyCodeBound_of_actualRectangularGraphs
 ← eventually_sphericalCode_card_lt_of_eventualGraphCertificates
 ← sphericalCode_bound_of_realized_graph
```

Judging by the names: the bound at each level comes from a "graph certificate" (`GraphCertificates`). Building these graphs uses representation-theory tools: Young diagrams (`Young`, `Box`), Gelfand–Tsetlin bases (`GelfandTsetlin`), the Weyl formula (`Weyl`) and the Casimir operator (`Casimir`). The `MetricCodes.Spherical` namespace takes up 69,180 lines, the bulk of the file.

**What else the file contains**: `hierarchyPackingExponent_eq_criticalBinaryExponent` says the **sphere-packing exponent** given by the spherical-code hierarchy equals the critical exponent `CohnElkies.criticalBinaryExponent` from problem 1. The file also has several upper bounds on the "kissing number" (`kissingNumber`). None of these are in the dependencies of the two main theorems.

**Mathematics used**: multivariate polynomials (derivatives, monomial orders, homogeneous polynomials), inner product spaces and adjoint operators, Lagrange interpolation, determinants, trigonometric functions and integrals.

---

## 3. Non-sofic groups (`NonSoficGroup.lean`)

**What the main theorem says**: there exists a group G that is finitely presented and not sofic.

The definition in the code: a group is sofic if there is a sequence of "permutation models" (`SoficApproximation`) under which multiplication holds asymptotically in normalized Hamming distance (`multiplicative`), and every non-identity element asymptotically moves almost every point (`separated`).

**Code layout**: 100% of the file is in the main theorem's dependencies. The name `Kun` appears extremely often (`KunThomFiberCoarea`, `KunResidualExpanderDecomposition` and so on), along with topic words such as `Leavitt`, `Thompson`, `Prefix`, `Kazhdan`, `Cheeger` and `Expander`.

**Spine**:

```
exists_finitelyPresented_nonsofic_group
 ← binaryLeavittElementaryGroup_not_sofic
 ← ninePrefixElementaryGroup_not_sofic
 ← sourceLocalPrefixTranspositionGroup_lef_of_sofic     (if sofic, then some group is LEF)
     together with sourceLocalPrefixTranspositionGroup_notLEF    (but that group is not LEF)
 ← source_ambient_nonempty_expandingCentralizerFiniteModel
 ← exists_source_selected_components                     (select one "component")
 ← exists_actual_source_u_retained_matching              (a matching)
 ← exists_unconditional_actual_source_dual_finpartition_sequences
 ← …
 ← alphaPrefixElementaryGroup_hasPropertyT_unconditional (an elementary group has property (T))
```

The logic of the proof can be read off this chain as an **argument by contradiction**:

1. The main object is the "elementary group for nine prefixes" (`ninePrefixElementaryGroup`), inside the binary Leavitt algebra (`binaryLeavitt`).
2. Assuming it is sofic, another group, `sourceLocalPrefixTranspositionGroup`, would be LEF.
3. But that group is not LEF (`notLEF`), a contradiction.
4. The derivation in step 2 uses "expander components" in finite models (`expandingCentralizerFiniteModel`), the selection of one component from them, a matching between components, and the fact that certain groups have Kazhdan's property (T).
5. Finally, "a finitely generated non-sofic group" is upgraded to "a finitely presented non-sofic group" (`exists_finitelyPresented_not_sofic_of_not_sofic`).

**Mathematics used**: inner product spaces and orthogonal projections, operator norms, partitions (`Finpartition`), Hamming distance. Notably, property (T) is **proved from scratch** in the file (`..._hasPropertyT_unconditional`) rather than cited as an assumption.

---

## 4. Connes's rigidity conjecture (`ConnesRigidity.lean`)

**What the main theorem says**: there exist a group Λ and a sequence of groups Γ₀, Γ₁, Γ₂, … such that:

- all of them are finitely generated, ICC, and have Kazhdan's property (T);
- the group factor of each Γₙ is isomorphic to Λ's, and they are pairwise isomorphic (`TracialGroupFactorsIsomorphic`: there is a trace-preserving normal *-isomorphism between the two group von Neumann algebras);
- yet Γₘ and Γₙ (m ≠ n) are not isomorphic as groups, and Λ is not isomorphic to any Γₙ.

**Spine**:

```
main theorem
 ← PaperAnalyticInput.universalLattice           (the "universal lattice" has property (T))
 ← universalLatticePropertyT_of_suslinRelative
 ← integralElementaryGroup_propertyT
 ← shalomIntegralPolynomialRelativePair
 ← …
 ← integerShalomRelativeKazhdanPair_of_fourierAtomGap
 ← exists_kernel_fixed_of_joint_atom_pos
```

The heaviest branch proves that a certain matrix group has **property (T)**, accounting for 733 of the 1,710 theorems. Judging by the names, it uses Shalom's method (`shalom...`), Suslin's elementary generation theorem (`suslinRelative`, `ElementaryGeneration`), and Fourier analysis (`fourierAtomGap`).

The other components of the main theorem each have their own source:

| Component | Based on |
|---|---|
| Isomorphic group factors | `paper_factors_isomorphic`, which depends on `carryCoordinates_measurePreserving` (the "carry coordinates" preserve the measure) |
| Non-isomorphic groups | `gamma_has_order_four` (Γ has an element of order 4), `paperLambda_orderOf_ne_four` (Λ has none), and `paperInvariant_card` (a computable group invariant) |
| ICC | `gamma_isICC`, `lambda_isICC` (infinite orbits) |

These names piece together the outline of the proof: use "carry" to build different group structures on the same measure space; equal measures give equal group factors; then group-theoretic invariants such as element orders tell the groups apart.

**What else the file contains**: `exists_nonisomorphic_propertyT_icc_groups_with_isomorphic_factors` is the version with just two groups; the main theorem does not use it.

**Mathematics used**: polynomials (evaluation, degree), inner product spaces and orthogonal projections, C*-algebras, Bochner integrals, special linear groups and transvections (`transvection`), semidirect products, element orders.

---

## 5. Lower bounds for the permanent (`Permanent.lean`)

**What the main theorem says**: let n ≥ 32. If a formula with division f (`RationalFormula`, required to be valid, i.e. with nonzero denominators) computes exactly the n×n permanent polynomial, then

```
n⁴ / (192 · log₂ n) ≤ number of variable occurrences in f (variableLeaves)
```

**Code layout**: this file is unusual; the main theorem uses only 23% of it.

- `PermanentFormulaLowerBound` (about 6,600 lines): the formula lower bound; the main theorem uses only this part.
- `PermanentRollout` (about 19,000 lines): not used by the main theorem at all; see "What else the file contains" below.

**Spine** (the clearest of all ten):

```
permanent_rational_formula_logarithmic_lower_bound
 ← permanent_rational_formula_lower_bound
 ← permanent_rational_formula_fourth_power_lower_bound
 ← matchingCyclicBlock_coefficientTranscendenceDegree_ge_square
                            (the coefficients of a "matching block" have transcendence degree ≥ order of a square)
 ← matchingMarkedPermanent_bitCoefficient_algebraicIndependent
                            (certain coefficients are algebraically independent)
 ← matchingPermanentJacobian_det_ne_zero        (a Jacobian determinant is nonzero)
 ← matchingPermanentJacobian_eq_weighted
 ← matchingWeightedCrossBitPermutation_sum
```

Another branch, `cyclicMatchingBlock_fourth_power_bound_of_coefficientTranscendenceDegree`, converts "large transcendence degree" into "many variable occurrences"; `permanent_size_bounds_of_fourth_power` converts between different measures of size (this is where "leaves = operations + 1" is used).

These names spell out the whole idea of the proof:

1. Select a small group of variables arranged as a "matching".
2. Show that expanding the permanent in these variables gives coefficients containing many **algebraically independent** quantities, by showing a Jacobian determinant is nonzero at some point.
3. The number of times these variables occur in the formula is at least of the same order as this transcendence degree.
4. Add up many pairwise disjoint matchings (`cyclic`: arranged cyclically).

**What else the file contains**: `PermanentRollout.permanent_circuit_loglog_bigOmega`: there is a constant c > 0 such that for all large enough n,

```
c · n² · log₂ log₂ n ≤ circuitComplexity(permanent n)
```

that is, a lower bound for **arithmetic circuits** (which may reuse intermediate results) computing the permanent. It uses 948 additional declarations, drawing on commutative algebra such as regular sequences (`RegularSequence`), homogeneous ideals and the Nullstellensatz (`Nullstellensatz`). The file also has a division-free formula lower bound, `permanent_divisionFree_formula_logarithmic_lower_bound`. None of these are part of the listed main theorem.

---

## 6. Quantum parallel repetition (`QuantumParallelRepetition.lean`)

**What the main theorem says**: there is a constant c > 0 such that for every finite two-player game G (question sets X, Y and answer sets A, B finite, answer sets nonempty), if the entangled value `entangledValue G` is below 1, then for every n ≥ 1:

```
repeatedEntangledValue G n
  ≤ exp( −c · ε¹³ / (ε + log(|A|·|B|)) · n ),  where ε = 1 − entangledValue G
```

That is, the entangled value of n repetitions decays exponentially in n.

**Code layout**: the main namespace has 61,916 lines, plus small modules such as `ClassicalInformation`, `ClassicalSampling`, `Pinsker` (Pinsker's inequality), `Game` and `Strategy`.

**Spine**:

```
distributionUniformExponential
 ← pdf_distributionUniformExponential_unconditional
 ← unconditionalSourceOneGameRounding_uniform              ("single-game rounding")
 ← unconditionalSourcePhysicalRounding_exists_small
 ← unconditionalActualFairSourceRoundingData_exists_stoppedVerifier
 ← unconditionalActualFairSourceRoundingContext_stoppedVerifier
 ← unconditionalActualFairSourceRoundingContext_analyticLedger
 ← unconditionalActualFairSourceStoppingHazardData_of_positive
 ← unconditionalSourcePhysicalRounding_exists_fairStoppingHazard
 ← unconditionalSourcePhysicalRounding_fairTargetEnergy
```

Judging by the names, the core of the proof is a "rounding" process: building a single-game strategy out of a strategy for the repeated game. The construction uses "stopping times" (`stopped`, `StoppingHazard`), "martingales" (`martingaleRate`), "energy" (`Energy`), and a "ledger" recording the various error terms (`Ledger`). Other names used for error control include `fair`, `Clipping` (truncation) and `cleanBound`.

**Mathematics used**: positive semidefinite matrices (heavily), trace, Kronecker products (tensor products of the two players' systems), unitary matrices, logarithms and entropy, Pinsker's inequality.

---

## 7. The closest vector problem (`GapCVP.lean`)

**What the main theorem says**: `gapCVP400IsNPHard : IsNPHardPromise gapCVP400Promise`. The definitions in the code:

- `gapCVP400Promise` is a "promise problem". A "yes" instance (`gapYES400`) has an integer vector z putting the target within squared distance r² of a lattice point; a "no" instance (`gapNO400`) has squared distance greater than (factor · r)² for every z, where the factor is `gapFactor400`.
- `IsNPHardPromise` means **every** NP language reduces to it via a `PromiseReduction`. A `PromiseReduction` requires the reduction map to be computed by a polynomial-time Turing machine (`BitTM`) and to satisfy completeness (yes ↦ yes) and soundness (no ↦ no).

**Code layout**: there are more definitions (4,458) than theorems (3,719), the only one of the ten files where this is so. Its most-used part of Mathlib is `Computability.TuringMachine` (about 30,000 references), far more than any other. Many of its 434 namespaces have names beginning with `TM` (Turing machine) or `CL`.

**Spine**:

```
gapCVP400IsNPHard
 ← paperVariableArityPhysicalIntegerTargetNPHardPromise
 ← OriginalThreeSATNPHardness.paperOriginalThreeSATIsNPHard   (3SAT is NP-hard)
 ← fiveFamilyActualSourceSortedIndexedORGadgetPreparationWord_valid
 ← … (a long series of validity proofs about encoding, sorting and stream processing of "five-family" clauses)
```

The main theorem's other direct dependencies include `..._completeness` and `..._soundness`, `paperVariableArityPhysicalShiftedCheckBit_valid` (check bits), and `yesLanguage_iff_original` and `noLanguage_iff_original` (consistency of the encodings).

What the code establishes about the structure:

1. **Proving that 3SAT is NP-hard**: the `paperOriginalThreeSATIsNPHard` branch alone has 1,601 theorems (45% of all 3,522). Judging by the names, the namespaces containing `CL` (`CLVerifier`, `CLTableau`, `CLLocalWindows` and others) are the construction for the Cook–Levin theorem: writing out the run of a verifier Turing machine as a "tableau" and encoding it as a CNF formula.
2. **Reducing 3SAT to CVP**: passing through polynomials over finite fields (`EffectiveBinaryField`, `Lagrange`, `Interpolation`), Gaussian elimination (`Gaussian`) and valuation theory (`Valuation`).
3. **Each step needs a concrete Turing machine** with a proof that its running time is polynomial: `..._polynomiallyBoundedFoldStates`, `EvalsToInTime` and so on. This is why there are so many definitions.

**What else the file contains**: the same reduction yields three more results, none in the main theorem's dependencies:

- `binaryNearestCodewordIsNPHard`: the binary nearest codeword problem;
- `binarySyndromeDecodingIsNPHard`: syndrome decoding;
- `finitePNormGapCVPIsNPHard`: the closest vector problem in ℓp norms.

---

## 8. Ehrhart's volume conjecture (`EhrhartVolumeInequality.lean`)

**What the main theorem says**: let S be a compact convex set in n-dimensional space with nonempty interior, barycenter at the origin, and the origin as its only interior lattice point (`interiorLatticePoints S = {0}`). Then

```
normalizedVolume S ≤ (n + 1)ⁿ / n!
```

**Code layout**: 222 namespaces, almost all of them long, whose names repeat `Bergman`, `Jet`, `Torus`, `Bochner`, `Dolbeault`, `Holomorphic`, `Plurisubharmonic`, `Moment` and `Partition`. Judging by the names, these are terms from complex geometry and several complex variables.

**Spine**:

```
ehrhart_volume_inequality_for_sets
 ← normalizedVolume_le_sharpConstant_of_momentBodyWeakProbability
 ← momentBodySharpJetScale_le_dimension_of_weakProbability     (a certain "scale" ≤ the dimension n)
 ← integral_momentBodyEnvelopePositiveSecant_le_dimension_mul_exp
 ← one_sub_momentBodyNormalizedPartition_le_dimension_mul
 ← exp_neg_dimension_mul_le_momentBodyNormalizedPartition
 ← momentBodyLogPartition_le_dimension_mul                    (log partition function ≤ n·t)
 ← convexOn_momentBodyLogPartition_Ici                        (the log partition function is convex)
 ← convexOn_momentWeakHolomorphicStrictJointLogPartition_Ioi
 ← convexOn_..._of_timeBounds
```

The core structure of the proof can be read off this chain:

1. Define a "log partition function" depending on a parameter t (`LogPartition`) and prove it is **convex**.
2. From convexity and a growth estimate, it is at most n·t.
3. Convert step by step (partition function → secant integral → scale) to conclude that a certain "scale" is at most the dimension n.
4. This bound on the scale is equivalent to the volume bound (n+1)ⁿ/n!.

The proof of convexity (`HolomorphicPhysicalLogConvexity` and others) uses holomorphic functions, Fourier analysis on the torus (`Torus`) and Bochner identities.

**What else the file contains**: `SimplexVolume.exists_centeredBody_sharp`: in every dimension n there really is a convex body meeting the conditions whose volume equals the bound exactly, so the bound is optimal. The main theorem does not use it.

**Mathematics used**: Fréchet derivatives, smooth functions (`ContDiff`), Bochner integrals, interval integrals, circle averages, bump functions (`BumpFunction`), positive definite matrices.

---

## 9. Multicolor Ramsey numbers (`MulticolorTriangleRamsey.lean`)

**What the main theorem says**:

1. for every k ≥ 2, `triangleRamseyNumber k ≥ (k^(1/3) / (6·e³⁸·log k))^k`;
2. the k-th root of `triangleRamseyNumber k` tends to infinity.

`triangleRamseyNumber k` is defined as the smallest n such that colouring the edges of the complete graph on n vertices with k colours always produces a monochromatic triangle.

**Code layout**: a single namespace with 146 declarations, the smallest file.

**Spine** (in full; only ten layers):

```
erdos_problem_183_explicit
 ← quantitativeLowerBound_explicit_all          (explicit lower bound for all k ≥ 2)
 ← allColourPaletteRamsey_exponential_bound_sharp
 ← recursivePaletteRamsey_exponential_bound      (exponential bound from the recursive construction)
 ← exists_recursivePaletteStage                  (every stage exists)
 ← exists_recursivePaletteColouring_fin          (a recursive palette colouring exists)
 ← exists_coordinate_covering                    (a coordinate cover exists)
 ← exists_saturated_matrix_ceil
 ← exists_saturated_matrix                       (a saturated matrix exists)
 ← card_badSaturationRows_lt_pow                 (the number of "bad rows" is below some power)
```

Read from the bottom up, this chain is the order of the construction:

1. A counting argument (bad cases are fewer than all cases) shows a **saturated matrix** exists.
2. The saturated matrix gives a **coordinate cover**.
3. The coordinate cover is used to recursively build a **palette colouring** with no monochromatic triangle.
4. Counting the vertices gives the lower bound.

Among the side branches, `PaletteBlockCertificate.noMonochromaticTriangle` proves the colouring has no monochromatic triangle, and `factorial_exp_lower` and `choose_le_exp_mul_div_pow` are numerical estimates.

**Mathematics used**: almost nothing but logarithms, powers and exponentials, plus Mathlib's graph theory (cliques, colourings). It is the most "elementary" of the ten files.

---

## 10. Extremal graph theory (`CompactnessAndDegeneracy.lean`)

The file splits into two nearly equal namespaces, one per main theorem: `CompactnessConjecture` (8,495 lines) and `TwoDegenerateGraphs` (8,252 lines).

### 10a. The compactness conjecture: `quantitativeCompactnessCounterexample`

**What the main theorem says**: there are a finite family of graphs and constants c, C > 0 such that:

- every member is connected, bipartite and contains a cycle;
- forbidding any single member gives a uniform lower bound on the extremal number (`UniformMemberLower family c`);
- forbidding the whole family, every n-vertex graph containing no member has (number of edges)¹⁶ ≤ C·n²¹, i.e. at most C′·n^(21/16) edges;
- 21/16 = 4/3 − 1/48;
- the family is not compact (`¬ IsCompactFamily family`), so the compactness conjecture fails (`¬ CompactnessConjectureStatement`).

**Spine**:

```
quantitativeCompactnessCounterexample
 ← checkedManuscriptCounterexample
 ← not_erdos_180
 ← proposedFamily_uniformMemberLower           (lower bound for each member)
 ← proposedFamily_even_characteristic_avoidance (a characteristic-2 construction avoids some members)
     together with proposedFamily_odd_characteristic_avoidance (an odd-characteristic construction avoids the others)
 ← symplecticQuadrangle_no_jTemplate_of_char_two
 ← symplecticLine_char_two_pair_avoidance
 ← …
```

Another branch, `proposedFamily_familyExtremal_sixteenth_power_le`, gives the upper bound for the whole family. Judging by the names: each member's lower bound comes from a "symplectic quadrangle" (`symplecticQuadrangle`, a graph built from symplectic geometry over a finite field), split into two cases by whether the field's **characteristic is 2 or odd**, each avoiding different members of the family.

### 10b. The degeneracy conjecture: `twoDegenerateExtremalCounterexample`

**What the main theorem says**: there is a graph H that is connected, bipartite and 2-degenerate (`IsTwoDegenerate H`), such that for every 2-colouring both sides contain a vertex of degree greater than 2; and there are c, ε > 0 with `extremalNumber n H ≥ c·n^(3/2+ε)` for all large enough n.

**Spine**:

```
twoDegenerateExtremalCounterexample
 ← eventually_manuscriptVertexCount_power_le_extremalNumber
 ← eventually_expectedRetainedEdge_le_extremalNumber      (expected number of edges after random retention)
 ← eventually_exists_pairGraph_free_dense_retainedHost    (a dense graph containing no H exists)
 ← pairGraphOverFin_free_of_manuscript_exclusion
 ← pairGraph_free_of_layer_exclusion_and_disagreement
 ← pairGraphCopy_layer_entropy_upper_of_disagreement      (an entropy upper bound for each layer)
 ← pairChildArrayEntropy_empirical_bound
```

Judging by the names:

1. H is a "pair graph" (`pairGraph`), built layer by layer.
2. The host graph is obtained by randomly retaining vertices of a Hamming-distance graph (`hammingRetention`).
3. The proof that it contains no H uses **entropy**: if H could be embedded, the entropy of each layer would be constrained (`layer_entropy_upper`), and with enough layers this is a contradiction.
4. It is then shown that enough edges survive the random retention (`expectedRetainedEdge`), with the probability of failure controlled (`SamplingFailureEvent`).

**What else the file contains**: `not_erdos_146` and `compactnessCounterexample_bigO` are restatements of the main theorems as corollaries.

**Mathematics used**: Mathlib's graph theory (copies, connectivity, colourings, bipartite graphs), logarithms and powers, the binary entropy function, and finite-dimensional linear algebra (needed for the symplectic construction).

---

## How this summary was produced

All the statistics can be reproduced; the scripts are in `scripts/`:

| Script | What it does |
|---|---|
| `DeclGraph.lean` | Extracts the dependency graph and records each declaration's source lines |
| `LibraryUse.lean` | Counts the Mathlib constants each file uses; the results are in `library_use.tsv` |
| `Duplicates.lean` | Finds theorems with identical statements, identical definitions and one-line corollaries |

The spines and the "share used by the main theorem" were computed in Python on the dependency graphs.
