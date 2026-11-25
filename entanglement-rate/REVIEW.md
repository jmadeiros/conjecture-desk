# N-3.c1 referee review: "Odd complete Bell networks have exact asymptotic GHZ cost k²/4"

Referee: pip (checker). 25 Nov 2026. Local work only. Nothing published.
Claim files: `swarm/work/_chain/MM-28491/` (ASTRA_RESULT.json, research/graph-tensor-chains.md).
Sources fetched to `swarm/work/N-3/src/` (OpenAI scope docs, Lean challenge and solution files, both Nov 24 PDFs; Zhou arXiv:2610.34273 v1, v2, v3 TeX; CVZ arXiv:1609.07476v2 TeX). Script: `swarm/work/N-3/check/verify.py`.

## Verdict

**Confirmed, conditional on one named OpenAI statement.** Every step holds. The result rests on the **lower-bound half of OpenAI's `rectangular_exponent` theorem**: lean/ComparatorChallenges/MatrixExponent.lean L121-131, stated in lean/docs/107.md and 379.md, with a claimed proof in lean/OAI/LinearAlgebra/SpectralBooks/ExactExponent.lean. It is used at the single point formalOmega_C(m², m, m) ≥ m² + m + 1/4. That statement is **not in the PDF**. The PDF's Corollaries 1.2 and 1.3 prove the claim only for odd k that are multiples of 3 (k = 9, 15, 21, ...). They do not prove it for k = 5, 7, 11, 13, ....

## Step-by-step check

### (i) Arithmetic and hypotheses of the rectangular formula
- The Lean statement is `formalOmega F w12 w23 w31`. It covers division-free straight-line programs that compute an ⌈N^{w31}⌉×⌈N^{w12}⌉ by ⌈N^{w12}⌉×⌈N^{w23}⌉ product as a formal polynomial identity. The cost counts add, sub and mul. The theorem sorts the weights itself (x = max, z = min), so the formula is applied to the sorted triple and the argument order does not matter.
- At (m², m, m): x = m², y = z = m, and x ≥ y ≥ z > 0 holds. Then (x+y)z − xy = m³ + m² − m³ = m² > 0. The correction term is m⁴/(4m⁴) = 1/4. So ω = m² + m + 1/4 = (2m+1)²/4 = k²/4. Correct.
- Cross-check: OpenAI's formula equals Zhou's Ψ(a,b,c) = (ab+ac+bc)²/(4abc), the known Uznański/ABZ upper curve. I verified the identity algebraically and in exact arithmetic for every three-block grouping, k ≤ 41. So OpenAI's new content is exactly the matching lower bound.

### (ii) Grouping gives a restriction in the right direction
- Grouping legs maps simple tensors to simple tensors, so the rank of the grouped tensor is at most R(G). Projecting the internal-edge labels to 0 is a restriction, and rank is monotone under restriction. Both operations commute with Kronecker powers, so R(B^{⊗N}) ≤ R(G^{⊗N}) and R̃(B) ≤ R̃(G). The direction is correct: the rectangular tensor gives a **lower** bound for G.
- With blocks of sizes m, m, 1 there are m·m = m² edges between the two big blocks and m edges from each big block to the singleton. Check: m² + 2m + 2·C(m,2) = 2m² + m = C(2m+1, 2). The weighted triangle with edge dimensions (2^{m²}, 2^m, 2^m) is ⟨2^{m²}, 2^m, 2^m⟩ up to permuting factors, and rank is invariant under that permutation.
- Zhou v3, Lemma "quadratic spectral constraint" (§5.1, HTML numbering Lemma 5.1), carries out exactly this construction. Its proof states log₂R̃(WT(Q_a)) ≤ log₂R̃(GT₂(K_A)) with (Q_a)_{ij} = 2^{a_i a_j}. Quoted correctly.

### (iii) From the circuit exponent to tensor rank (needed because the Lean theorem is about circuits)
- Direction needed: formalOmega ≤ log₂R̃(B). Take a rank-r decomposition of B^{⊗N} with formats p = 2^{Nm²} and q = s = 2^{Nm}. Recursive block algorithm: C(t) ≤ r·C(t−1) + c·D^{t−1}, where D = max of the pairwise products of p, q, s. Flattening gives r ≥ D, so C(t) = O(t·r^t). The circuits are division-free and use constants from F. Correctness is a formal identity, and zero-padding to the next power keeps it. So formalOmega_C(m², m, m) ≤ log₂ r / N for every N, hence ≤ log₂R̃(B).
- Combined with the Lean theorem: log₂R̃(B) ≥ k²/4, so log₂R̃(G) ≥ k²/4. Astra's step 3 says this. The literal Huang–Pan "O(M^t)" needs the extra factor t when r = D, and Astra notes this. Harmless.
- Zhou, Definition "rectangular matrix multiplication exponent", uses the rank-based ω_F(a,b,c) and states ω_F(a,b,c) = Γ_F(weighted triangle). This is a second route to the same transfer.

### (iv) Upper bound k²/4 for odd k
- Zhou v3, Theorem 1.1 = Theorem 4.10 "complete-graph bound": for every field F and every n ≥ 2, ⌊n²/4⌋ ≤ log₂R̃_F(GT₂(K_n)) ≤ n²/4. The same statement is in v1 (25 Oct) and in v2. Zhou v3 also says: "For odd n, the upper bound exceeds the maximum cut lower bound by 1/4."
- Khoruzhii, Lemmata Repository 2610.00005, Theorem 3 (v1 21 Oct over C; v3 4 Nov, every field) independently proves d^{⌊k²/4⌋} ≤ R̃(G_k(d)) ≤ d^{k²/4}. It still leaves the odd gap (checked 25 Nov).
- **CVZ 2019 does NOT supply this upper bound.** CVZ prove only τ(K_k) ≤ log₇(9/2) ≈ 0.7729 per edge, which is 7.73 for K_5, and they ask whether τ < 2/3 is possible (Question 1.3.1). The brief's "Zhou and/or CVZ" is wrong for CVZ. Astra's derivation itself cites only Zhou for this step, which is correct.
- Consistency check (I tried to break it here): for every three-block grouping (a ≥ b ≥ c), OpenAI's formula evaluated on the edge counts (ab, ac, bc) gives exactly k²/4 when a ≤ b+c, and a(b+c) ≤ k²/4 when a > b+c. So it never exceeds Zhou's upper bound. The two stated theorems do not contradict each other (verify.py found 0 violations, k ≤ 41).

### (v) The quantum dictionary
- CVZ arXiv v2 (published as Comput. Complexity 28 (2019) 57–111) defines ω(φ,ψ) = lim (1/n) min{m : φ^{⊗m} ≥ ψ^{⊗n}} with ≥ meaning restriction. Its text says "if φ and ψ are pure quantum states, then φ ≥ ψ means precisely that ψ can be obtained from φ by SLOCC". The exponent is ω(ψ) := ω(GHZ₂, ψ). Proposition "limprop" (published numbering 1.19) proves ω(ψ) = lim (1/n) log₂ R(ψ^{⊗n}). The intro also states the K_k / EPR / GHZ reading and "⌈log₂ r⌉ copies".
- GHZ_k^{⊗h} is the rank-2^h unit tensor, so h_k(N) = ⌈log₂ R(Ψ_k^{⊗N})⌉ exactly. The limit exists by Fekete's lemma. Exact SLOCC with nonzero probability on pure states is restriction, and normalisation is irrelevant. Approximate conversion (degeneration) would give the same rate: CVZ Theorem "restrdegen". The claim's definition matches. Field: C, as CVZ require.

### (vi) Does the PDF's Corollary 1.3 suffice? No, except when k ≡ 0 mod 3
- At (m², m, m), the log₂ of (abc)^{3/4} is (3/4)(m² + 2m). This is below m² + m for m ≥ 2, since the gap is m(m−2)/4 ≥ 0. So Corollary 1.3 gives only max{m² + m, (3/4)(m² + 2m)} = m² + m = ⌊k²/4⌋, which is the already-known max-cut bound. For k = 5: 6 versus 6.25.
- Over every three-block grouping, the best bound Corollary 1.3 gives is (3/8)(k² − Σa_i²). For k ≢ 0 mod 3 this is exactly (k² − 1)/4 = ⌊k²/4⌋: no gain.
- For k = 3r, blocks r, r, r give the square tensor T_{2^{r²}}. Corollary 1.2 gives asymptotic rank 2^{9r²/4} = 2^{k²/4}. So **k = 9, 15, 21, ... follow from the PDF plus Zhou alone**. Astra's own research note states this fallback, but the final card does not.

## Novelty
- The exact rectangular formula first entered the OpenAI repo in commit 92b516ef8e (2026-11-25T00:04Z). The October version of lean/docs/107.md has only upper bounds. So this consequence could not have been derived from it more than about 18 hours ago.
- I found no statement of the result in: Zhou v1, v2, v3 (v1's Open Problem 1 asks exactly this, and v3 still records the 1/4 gap); Khoruzhii (last updated 4 Nov); the OpenAI 9/4 PDF or the "Euclidean geometry" companion (graph tensors appear there only as "wire prices", with no complete-graph rank); a GitHub code search of openai/math ("graph tensor", "complete graph", "GHZ", "asymptotic rank"); arXiv API searches (graph tensor(s), complete graph + asymptotic rank, GHZ + asymptotic rank, rectangular MM, sorted by date); and web searches.
- It is new as far as a search can tell. It is also immediate: Zhou's own lemma plus one substitution. Anyone reading OpenAI's scope document next to Zhou would see it.

## Significance (blunt)
- It answers Zhou's stated open problem (v1, Open Problem 1) in the "= n²/4" direction. Max-cut equality (CVZ Question 1.3.2) therefore fails for every odd complete graph, and the 1/4 gap is real. It also shows that the polynomial-method upper bound (Zhou, Khoruzhii) is tight on all complete graphs.
- The operational reading (exact GHZ cost of a complete EPR network) belongs to a small quantum-information / asymptotic-spectrum community (Christandl, Vrana, Zuiddam, Walter and others). These are real quantities that people asked about, but not central problems.
- All of its weight is inherited from OpenAI's unrefereed rectangular lower bound, which is stated only in the Lean scope. Zhou's and Khoruzhii's upper bounds are also unrefereed preprints. This is a corollary, not a theorem with its own idea.

## Weakest step
Step (i). It is the only place where the not-in-PDF statement enters. If `rectangular_exponent` were weakened to what the PDF proves, the result would survive only for k ≡ 0 mod 3, and k = 5 would stay open at [6, 25/4].
