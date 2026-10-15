# How the ten proofs work

[中文版](proofs.zh.md) · [Back to the overview](README.md) · [Start with the simplest leaves](leaves.md) · [What the code alone shows](proofs-from-code.md)

The Lean files contain not a single comment, and reading proofs of thousands to over a hundred thousand lines straight through is close to impossible. Fortunately OpenAI released a 253-page paper alongside these proofs ([PDF](https://cdn.openai.com/pdf/ten-proofs-oai.pdf)), and each chapter opens with a proof overview. This document follows those overviews, explains the idea of each proof with as little jargon as possible, and then points to the corresponding key theorems in the Lean files so you can find them in the [dependency graphs](README.md).

A few notes:

- **The ideas come from the paper; I did not read them out of the Lean code.** The Lean proofs follow essentially the same structure as the paper. The theorems listed under "In Lean" in each section are the nodes in the top one or two layers of the main theorem's dependency graph; I matched them to the paper's steps by their names and positions.
- **These are research-level results**, and many steps rest on a great deal of specialist knowledge. This document only covers the skeleton of each proof: what is done first, what comes next, and what the key ideas are.
- **The Lean versions are much longer than the paper.** A single "clearly" or "by a standard argument" in the paper can be hundreds of lines in Lean. Problem 7 is the most extreme case: where the paper says "this reduction runs in polynomial time", the Lean version actually builds the Turing machines and proves their running time. That is why `GapCVP.lean` has 130,000 lines full of names containing `TM`.

---

## 1. High-dimensional sphere packing

**The problem**: in d-dimensional space, place non-overlapping balls of equal size. What fraction of space can they fill at most (call it Δ_d)? In dimensions 8 and 24 the answer was settled completely by Viazovska and coauthors, but in general high dimensions only upper and lower bounds were known, with a huge gap between them.

**The result**: the Cohn–Elkies method is currently the most powerful tool for upper bounds. The paper computes exactly how strong this method becomes as the dimension tends to infinity: the upper bound it gives is about 2^(−0.6044·d). This is the first improvement to the high-dimensional sphere-packing exponent since 1978 (the previous value was 0.5990). The paper also proves that the method cannot do any better.

**The idea of the proof**:

The Cohn–Elkies method works like this. If you can find an "auxiliary function" f satisfying three conditions (f is at most 0 outside radius 1; the Fourier transform of f is nonnegative everywhere; the Fourier transform is positive at the origin), then the packing density is at most a number computed from f(0) and the value of f's Fourier transform at the origin. The better the function, the tighter the bound. So the question becomes: "how good can the best auxiliary function be?" The paper answers from both directions:

1. **Simplify first**: averaging a function over all rotations does not break any of the conditions, so it is enough to consider **radial functions** (functions whose value depends only on the distance to the origin). The leaf theorem "a radial function is even" from the first walkthrough comes from here.
2. **Show it cannot be better**: from any admissible auxiliary function, build a function g with ĝ = −g (its Fourier transform is its own negative) and g(0) = 0. The key estimate is that such a radial function can have only a tiny amount of "mass" inside the ball of radius (1/π)·√d. It follows that the radius at which the auxiliary function starts satisfying its sign conditions is at least (1/π − o(1))·√d.
3. **Show it can be achieved**: modify the Mellin transform of a Gaussian to build a concrete auxiliary function whose sign conditions start holding at radius exactly (1/π + o(1))·√d.
4. **Convert**: the radii from the two directions match, and Stirling's formula converts the radius into the exponent of the packing density, giving √(e/(2π)).

**In Lean**: the main theorem `sharpFullCohnElkiesManuscriptConclusions` is a bundle of ten conclusions, assembled via `SharpFullCohnElkiesManuscriptConclusions.components`. They include `linear_program_root` (the limit of the linear program), `natural_logarithmic_rate`, and `base_two_logarithmic_rate` (the exponent in base 2).

---

## 2. Binary and spherical codes

**The problem**: using 0/1 strings of length n as codewords, and requiring any two codewords to differ in at least δn positions, how many codewords can you choose? Spherical codes are the analogous problem of placing points on a high-dimensional sphere so that any two have inner product at most s. The best upper bounds were the MRRW bound from 1977 and the Kabatianskii–Levenshtein bound from 1978, and neither had been improved in general for nearly fifty years.

**The result**: for every δ (and every s) the new upper bound is strictly better, by an exponential factor.

**The idea of the proof**:

1. **The classical method (Delsarte's linear program)**: find a polynomial satisfying certain sign conditions as a "certificate"; it directly gives an upper bound on the number of codewords. Both the MRRW and KL bounds come from certificates of this kind.
2. **The new idea: attach a subspace to each codeword instead of a single vector.** The classical construction attaches one vector to each codeword. The new construction attaches a d_E-dimensional subspace to each codeword x, inside a common D-dimensional space, and the subspace "moves with the codeword": a symmetry carrying x to y also carries x's subspace to y's subspace. How much two subspaces overlap depends only on the distance between the two codewords. This gives the upper bound

   |C| ≤ (1 − s)/(Λ − s) × D/d_E,

   where Λ is the largest eigenvalue of a "transition matrix". The subspace dimension d_E can be exponentially large, and that is where the improvement comes from.
3. **Binary codes**: the transition matrices are tridiagonal. A "whole cube" construction beats the first MRRW bound, and a "constant-weight layer" construction beats the second MRRW bound when its optimum is in the interior. Splitting into the cases "optimum at the endpoint" and "optimum in the interior" gives a strict improvement for every δ.
4. **Spherical codes**: spherical harmonics replace Boolean functions. The subspaces are labelled by Young diagrams with r rows, and larger r is better, giving a **strictly improving hierarchy**: level r+1 always beats level r, and level 0 is exactly the classical KL bound. In the limit s → 1, this construction also recovers the sphere-packing exponent from problem 1.

**In Lean**:

- Binary codes: `binaryRate_lt_mrrw` has two parts. `binaryRate_le_combinedVariationalRate` gives the new upper bound, and `strict_mrrw2` proves it is strictly below the second MRRW bound. Underneath it is exactly the endpoint/interior case split: `mrrw_endpoint_dichotomy`, `variationalRate_lt_mrrw_of_interior` and `combinedVariationalRate_lt_mrrw_of_endpoint`.
- Spherical codes: `strict_hierarchy` comes from `strict_hierarchy_of_actualCodeBound` and `fixedLevelHierarchyCodeBound`.

---

## 3. Non-sofic groups

**The problem**: a group is called sofic if any finite part of its multiplication table can be approximately simulated by permutations of a finite set, with errors at only a tiny fraction of points. Sofic groups have many good properties, and for decades nobody knew whether **every** group is sofic.

**The result**: non-sofic groups exist. The concrete example is the group of invertible elements of the "binary Leavitt algebra"; a subgroup G of it is already not sofic.

**The idea of the proof** (by contradiction):

1. **The setting**: the binary Leavitt algebra R is generated by four elements s₀, s₁, t₀, t₁ under mod 2 arithmetic, subject to tᵢsⱼ = δᵢⱼ and s₀t₀ + s₁t₁ = 1. It is "self-similar": R and R² are isomorphic as modules, which ties it closely to infinite binary strings and Thompson's group V. Take G to be the group generated by 9×9 elementary matrices over R, embedded into the invertible elements of R using binary prefix codes. G is known to have Kazhdan's property (T).
2. **Assume G is sofic.** By property (T), one can choose an approximation whose "generator graph" is an expander (a graph with excellent connectivity).
3. **Two existing tools**:
   - Kun's theorem: restricting the approximation to a subgroup Γ with property (T), the graph splits into many expander pieces.
   - The Kun–Thom theorem: if a subgroup J commuting with Γ is approximated on a **single** expander piece, then J must be LEF (every finite part of its multiplication table embeds exactly into a finite group).

   The difficulty is that the first tool gives **many** pieces, while the second needs **one**.
4. **The new tool: an expander-matching criterion.** If there are elements tᵢ that "push Γ inward" (tᵢΓtᵢ⁻¹ ⊆ Γ) and also push J into Γ, then each pushed piece lands almost entirely inside another piece, with roughly the same size. (The proof uses a clever function, "piece size relative to the median", that barely changes along the generators.) So the correspondence is one-to-one, and one can select a single expander piece on which J is also well approximated, which makes the Kun–Thom theorem applicable.
5. **The contradiction**: inside G, construct Γ, two elements u and v, and a subgroup J isomorphic to **Thompson's group V**, satisfying all the conditions above. Then V would have to be LEF. But V is finitely presented, infinite and simple, so it cannot be LEF. This contradiction shows G is not sofic.

**In Lean**: the main theorem says "there exists a finitely presented non-sofic group". It comes from `binaryLeavittElementaryGroup_not_sofic` (with `ninePrefixElementaryGroup_not_sofic`, the elementary group for the nine prefixes, underneath), strengthened from "finitely generated" to "finitely presented" by `exists_finitelyPresented_not_sofic_of_not_sofic`.

---

## 4. Connes's rigidity conjecture

**The problem**: every group has an associated operator algebra, its group von Neumann algebra L(G). Connes conjectured that for ICC groups with property (T) (ICC: every non-identity conjugacy class is infinite), L(G) determines G completely. That is, if two such groups have isomorphic algebras, the groups themselves are isomorphic.

**The result**: the conjecture is false. There are infinitely many pairwise non-isomorphic groups of this kind whose group von Neumann algebras are all isomorphic.

**The idea of the proof**:

1. **The key observation**: for a semidirect product A ⋊ K (with A abelian), L(A ⋊ K) ≅ L^∞(Â) ⋊ K. The right-hand side remembers the dual group Â only as a **probability space** (with its uniform Haar measure) together with the action of K on it; it **does not remember the multiplication on Â**. So if you can put two different group structures on the same probability space without changing the action of K, you get examples with the same algebra but different groups.
2. **A four-point example**: consider the set {0,1}².
   - Adding coordinatewise mod 2 gives the Klein four-group (every element added to itself returns to 0).
   - Using instead (x, y)·(x′, y′) = (x + x′, y + y′ + xx′), that is, "binary addition with carry", gives Z/4 (which has elements of order 4).

   Under both structures the uniform measure on the four points is the same.
3. **Scaling up**: take a torsion-free ICC group K with property (T) (a congruence subgroup of SL₄(Z[t])) acting on a large abelian group built from polynomials mod 2. Modifying the group structure with "binary carry" gives two groups Λ and Γ₀. Their group von Neumann algebras are isomorphic, but Γ₀ has elements of order 4 and Λ does not, so they are not isomorphic.
4. **Property (T) and ICC**: these only need to be proved for Λ; they then transfer to Γ₀ through the isomorphic algebras.
5. **Infinitely many**: shifting the position of the carry by n places gives Γₙ. Their algebras are all isomorphic to Λ's. An invariant computable from the group itself (of order 2^(4n)) tells them apart.

**In Lean**: the components of the main theorem correspond directly to these steps, for example `InfinitePropertyTFiber.factors_isomorphic` (isomorphic algebras), `gamma_pairwise_nonisomorphic` (pairwise non-isomorphic), `gamma_propertyT` and `gamma_icc`. Underneath you can see `gamma_has_order_four` (an element of order 4), `paperLambda_orderOf_ne_four` (Λ has no element of order 4) and `paper_factors_isomorphic` (via `carryCoordinates_measurePreserving`: the carry coordinates preserve the measure).

---

## 5. A formula lower bound for the permanent

**The problem**: the permanent of an n×n matrix is almost the same as the determinant, except that its expansion has no plus and minus signs. The determinant can be computed efficiently, but the permanent is believed to be hard; this is the central problem of algebraic complexity theory. The question here: a formula for the permanent built from addition, subtraction, multiplication and division (where each intermediate result can be used only once, so the formula is a tree) must be at least how long?

**The result**: the variables must occur at least n⁴/(192·log₂ n) times in the formula (for n ≥ 32), even if division is allowed. The previous best lower bound was of order n³.

**The idea of the proof** (in four stages):

1. **Measure "information"**: pick a group of variables Y, expand the permanent in Y, and count how many **algebraically independent** quantities appear among the coefficients (the transcendence degree). The key lemma: if variables from Y occur t times in total in the formula, this transcendence degree is at most 4t (6t if division is allowed). The reason is that a formula is a tree. Along a path where only one side contains Y, the other side just applies an affine map (a fractional linear map when division is allowed), and a whole path of such maps is still one such map. New parameters enter only at branch points where both sides contain Y, and there are at most t − 1 of those.
2. **A small group of variables carries a lot of information**: taking only about 2·log₂ n matrix entries arranged as a "matching" (different rows and different columns), one can prove the coefficients contain m² algebraically independent quantities, where m ≥ n/2. The method is to evaluate a Jacobian matrix at a carefully chosen point; it factors as a Kronecker product of two Vandermonde-type matrices, so it is invertible.
3. **Add up many groups**: split the matrix entries into about n²/(2·log₂ n) pairwise disjoint matchings of this kind. Each group forces its variables to occur many times, and the groups share no variables, so the counts add up to a lower bound of order n⁴/log n.
4. **Allow division**: the first two stages concern only the permanent itself and are unaffected; only the counting in stage 1 needs a fractional-linear version, and the constant changes from 4 to 6.

**In Lean**: the main theorem `permanent_rational_formula_logarithmic_lower_bound` comes from `permanent_rational_formula_lower_bound`, which uses `permanent_rational_formula_fourth_power_lower_bound` and `permanent_size_bounds_of_fourth_power`. The leaf "leaves = operations + 1" from the first walkthrough is used in the latter, to convert between different measures of formula size.

---

## 6. Quantum parallel repetition

**The problem**: two players cooperate in a game. The referee sends each a question; they cannot communicate and answer separately. If they play n rounds at once and must win all of them, does the winning probability fall exponentially in n? For ordinary players Raz proved in 1995 that it does. If the players may share quantum entanglement, the question had remained open; the best previous result only proved polynomial decay.

**The result**: for every finite two-player one-round game, even with quantum entanglement allowed, the probability of winning all rounds falls exponentially.

**The idea of the proof** (by contradiction, following Yuen's framework):

1. **Assume** some strategy wins all n rounds with probability above the claimed bound.
2. **Conditioning**: choose a small set D of rounds. Conditioned on "winning every round in D", a further round picked at random is won with high probability.
3. **The ideal experiment**: describe the situation in that round, under the conditioning, as a shared state together with each player's measurements. But this is not yet a legal single-round strategy: the conditioning changes the distribution of questions, the players do not know what happened in the other rounds, and the quantum state depends on both players' questions at once.
4. **The new central lemma**: the two players can **each locally** generate a "history" and a quantum state that approximate this ideal experiment, with an error that **does not depend on the inverse of the conditioning event's probability**. This is crucial because that probability can be exponentially small, which is exactly where earlier methods got stuck, giving only polynomial decay.
5. **Assemble a strategy**: "correlated sampling" techniques, classical and quantum, synchronise the two players' histories and quantum states, giving a genuinely legal single-round strategy.
6. **The contradiction**: this single-round strategy wins with probability above the game's optimal value, which is impossible. The exponent 13 comes from the losses in the quantum correlated-sampling lemma; the paper does not claim it is optimal.

**In Lean**: the main theorem `distributionUniformExponential` and `pdf_distributionUniformExponential_unconditional` have the same statement (the latter is the direct source of the former), with `unconditionalSourceOneGameRounding_uniform` underneath. "Rounding" refers to step 5: "rounding" the ideal experiment into a real single-round strategy.

---

## 7. Hardness of the closest vector problem

**The problem**: given a lattice (a regularly spaced grid of points in space) and a target point, find the lattice point closest to the target. This matters a great deal in cryptography. Solving it exactly is known to be NP-hard; the question is whether approximating it to within a factor n^c (c fixed) is still hard.

**The result**: approximating it to within a factor n^(1/400) is still NP-hard. Moreover the proof starts directly from 3SAT and does not need the PCP theorem.

**The idea of the proof**: the chain of reductions is **3SAT → binary nearest codeword → closest vector problem**. The second step is standard; the new content is in the first.

1. **Encode truth assignments as polynomials**: choose m points a₁, …, aₘ in a finite field of characteristic 2. A truth assignment σ corresponds to a unique interpolation polynomial Q_σ of degree less than m with Q_σ(aᵢ) = σᵢ.
2. **Write the polynomial as 0/1 tables**: for each evaluation point p and each field element w, introduce a binary variable, set to "1 exactly when w = Q_σ(p)". Each clause gets a few similar tables.
3. **Linear constraints make the tables "look like a polynomial"**: require the power sums of each table's support set to be evaluations of a low-degree polynomial (a Reed–Solomon code), each support set to have odd size, and the clause tables to agree with the global table mod 2. All of these are linear equations mod 2, together forming Hx = b.
4. **Completeness**: if the formula is satisfiable, filling the tables as above gives a solution of low weight.
5. **Soundness (the hardest part)**: conversely, if there is a solution of very low weight, every support set is small. A separate algebraic reconstruction lemma says one can rebuild from these power sums a separable polynomial whose roots have exactly these power sums. Valuation theory then reads each clause's truth values off the roots, and matching the clauses against each other assembles an assignment satisfying the whole formula.
6. **Move to lattices**: the standard mod 2 lift turns "the minimum weight of a solution" into "the squared distance from the target to the lattice", so the code problem's approximation factor M^(1/200) becomes the lattice problem's n^(1/400).

**In Lean**: under the main theorem `gapCVP400IsNPHard`, the key node is `paperVariableArityPhysicalIntegerTargetNPHardPromise`, which depends directly on `..._completeness` and `..._soundness`. The Lean file defines NP-hardness as "every NP problem reduces to it by a polynomial-time Turing machine" (see `PromiseReduction` and `NPHardPromise`). So it does two things the paper does not: it proves the Cook–Levin theorem (3SAT itself is NP-hard; the parts whose names contain `CL`, such as `CLVerifier` and `CLTableau`), and it builds concrete Turing machines that carry out the whole reduction and proves they halt in polynomial time (the parts whose names contain `TM`). These two things make up most of the file.

---

## 8. Ehrhart's volume conjecture

**The problem**: a convex body (a solid with no dents) has its centre of mass at the origin, and apart from the origin there is no point with integer coordinates in its interior. How large can its volume be? In 1964 Ehrhart conjectured the answer (n+1)ⁿ/n!, attained by a particular simplex. It had been proved only in special cases such as the plane and simplices; the best general bound was of order 4ⁿ·e^(−cn), far from the conjectured value.

**The result**: in every dimension n, the volume is at most (n+1)ⁿ/n!, and the bound is attained.

**The idea of the proof**: surprisingly, the proof borrows tools from complex geometry.

1. **Turn the convex body into a function**: Berman and Berndtsson proved that there is a smooth convex function φ whose gradient transports the measure e^(−φ)dx exactly onto the uniform measure on the convex body K.
2. **Move to complex space**: view φ as a function of the absolute values of n nonzero complex numbers. Consider the space H_k of holomorphic functions that are square-integrable with weight e^(−kφ). A basis of it is given exactly by the monomials labelled by integer points in the interior of kK. So the condition "the origin is the only interior integer point" is exactly equivalent to "H₁ contains only constant functions".
3. **Build a family of functions**: fix the point p = (1, …, 1), sort functions by their order of vanishing at p, and use this to build a family of potentials ψₜ (t ≥ 0) starting from ψ₀ = φ.
4. **The slope of a convex function**: define L(t) as the negative logarithm of a partition function. By Berndtsson's positivity theorem, L(t) is convex.
5. **Squeeze the slope from both sides**:
   - counting the linear conditions that the vanishing orders impose gives a **lower bound** n·c_K/(n+1) on the slope of L at 0, where c_K = (n!·vol K)^(1/n);
   - a local Schwarz estimate gives an **upper bound** n on the same slope.

   Comparing the two gives c_K ≤ n + 1, that is, vol(K) ≤ (n+1)ⁿ/n!.

**In Lean**: under the main theorem `ehrhart_volume_inequality_for_sets` is `normalizedVolume_le_sharpConstant_of_momentBodyWeakProbability` (the volume is at most the sharp constant), which depends on `momentBodySharpJetScale_le_dimension_of_weakProbability`, the slope comparison of step 5. The many names in the file containing `Bergman`, `Jet`, `Plurisubharmonic` and `Torus` belong to the complex-geometry part, steps 2 to 4.

---

## 9. Multicolor Ramsey numbers

**The problem**: colour the edges of a complete graph with k colours. How many vertices are needed to guarantee a triangle in a single colour? Call this number R_k(3). It was known to be at most about e·k!, but the lower bound was only exponential (about 3.28^k). Does it grow exponentially or like a factorial? Erdős offered a prize for this question.

**The result**: R_k(3) ≥ (c·k^(1/3)/log k)^k. Together with the known upper bound, R_k(3) = k^Θ(k), so it grows at the same rate as a factorial. (As a corollary, graphs with independence number 2 can have unbounded Shannon capacity.)

**The idea of the proof**: to show R_k(3) is large, you have to **construct** a large colouring with no monochromatic triangle.

1. **A combinatorial tool**: a random argument (a union bound) produces a "saturated matrix", which yields two fixed maps f and g with a "coordinate cover" property: for any two words x and y, some coordinate d satisfies x_d = f(y)_d or y_d = g(x)_d.
2. **Recursive construction**: build the colouring stage by stage while maintaining a stronger invariant: at stage j, the graph of each colour can be properly coloured with j+1 "labels" (adjacent vertices get different labels).
3. **Blocks and palettes**: split the vertices into many blocks, each with a "palette" recording which colours are **missing** in that block. Inside a block, place the previous stage's colouring (with the colours renumbered). A maximal packing selects many palettes while guaranteeing any two palettes differ in enough colours.
4. **Colouring edges between blocks**: an edge between two blocks gets its colour from the coordinate cover maps, so that every such edge's colour is "active" in the block at one end and "missing" in the block at the other, and the label at the active end is determined by the other end.
5. **Why there is no monochromatic triangle**:
   - If a triangle spans two blocks, two edges of the same colour run from one outside vertex into the active block, which forces their other endpoints to have the same label; so the edge between those two endpoints cannot have that colour.
   - If a triangle spans three blocks, a single colour would have to lie in all three pairwise symmetric differences of the palettes, which is impossible for sets.
6. **Count**: multiplying the numbers of blocks across the stages gives the lower bound on R_k(3).

**In Lean**: the main theorem `erdos_problem_183_explicit` consists of `quantitativeLowerBound_explicit_all` (the explicit lower bound) and `divergentRamseyRoot` (the k-th root tends to infinity). Both depend on `allColourPaletteRamsey_exponential_bound_sharp`, the conclusion of the recursive construction. The names `palette`, `saturatedMatrix`, `recursiveCrossColour` and `PaletteBlockCertificate` in the file correspond to the palettes, saturated matrix, cross-block colouring and the "no triangle" proof above. The Chinese-labelled graph (`zh/svg/erdos_problem_183_explicit.zh.svg`) was translated by hand and can be read alongside.

---

## 10. Two conjectures in extremal graph theory

**The problem**: the extremal number ex(n, F) is the largest number of edges in an n-vertex graph that contains no copy of a given subgraph. Two conjectures are disproved here:

- **The compactness conjecture** (Erdős–Simonovits): forbidding a whole family of graphs that contain cycles lowers the extremal number by at most a constant factor compared with forbidding one of its members alone.
- **The degeneracy conjecture** (Erdős): every bipartite r-degenerate graph H has extremal number O(n^(2−1/r)). For r = 2 this is O(n^(3/2)).

### 10a. The compactness conjecture

**The result**: there is a family F of connected bipartite graphs such that forbidding any single member gives extremal number Ω(n^(4/3)), while forbidding them all together gives only O(n^(4/3 − 1/48)). The gap is not a constant factor but a polynomial factor.

**The idea of the proof**:

1. **Choose the family**: F consists of the 4-cycle, the 6-cycle, and certain "quotients" of two templates built from subdivided complete bipartite graphs.
2. **Upper bound**: counting short paths in a graph that avoids the whole family gives O(n^(21/16)) edges (21/16 = 4/3 − 1/48).
3. **Lower bound**: for each graph in the family, the incidence graph of a "generalized quadrangle" (a point-line structure built from symplectic geometry over a finite field) gives a graph avoiding it with Ω(n^(4/3)) edges. The key is that the characteristic of the finite field can be chosen depending on which graph is forbidden. Each member has its own good construction, but the upper bound in step 2 shows that no graph can avoid the whole family with that many edges.

**In Lean**: under the main theorem `quantitativeCompactnessCounterexample` is `checkedManuscriptCounterexample`, which collects `proposedFamily_familyExtremal_sixteenth_power_le` (the upper bound), `proposedFamily_not_compact` (the per-member lower bounds make compactness fail), `proposedFamily_member_connected` and `proposedFamily_member_isBipartite`.

### 10b. The degeneracy conjecture

**The result**: there is a connected bipartite 2-degenerate graph H whose extremal number is at least c·n^(3/2+ε), beyond the conjectured O(n^(3/2)).

**The idea of the proof**:

1. **Build H**: layer by layer. In each layer, for **every pair** of vertices in the previous layer, add a new vertex joined to those two. Every new vertex has only 2 neighbours, so H is 2-degenerate.
2. **Build a large graph without H**: start from a bipartite graph defined by Hamming distance and keep each vertex independently at random.
3. **Why it contains no H**: design a bounded "entropy potential". If H could be embedded, each additional layer embedded would raise this potential by a fixed amount; with enough layers it would exceed its bound, which is impossible. The leaf "12/7 < √3" from the first walkthrough is part of the parameter estimates here.
4. **Enough edges**: a second-moment argument shows the randomly thinned graph still has Ω(n^(3/2+ε)) edges; padding then extends the result to every sufficiently large n.

**In Lean**: under the main theorem `twoDegenerateExtremalCounterexample` you can see `pairGraphOverFin_isTwoDegenerate` and `pairGraphOverFin_isBipartite` (the properties of H), `eventually_manuscriptVertexCount_power_le_extremalNumber` (the extremal-number lower bound, via the expected number of edges kept after random thinning), and `hammingRetentionProbability_pos` (the probability that a vertex of the Hamming graph is kept).

---

## How to read on

1. Read the relevant section here first to learn the steps of the proof.
2. Open the corresponding dependency graph, start from the main theorem at the right-hand end, find the key theorems mentioned above, and see how much hangs under each one.
3. For the detailed arguments, read the corresponding chapter of the paper; to see how a step is written in Lean, search the Lean file for the theorem name.
4. To start with something easy to understand, begin with the [leaf theorem walkthrough](leaves.md).
