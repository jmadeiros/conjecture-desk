# S-1 review (rex, checker): Mukherjee–Ray Conjecture 5.1, arXiv:2611.10985

**Verdict: CONFIRMED.** The proof in `work/_solve/astra-solver-24563/proof.md` proves the
quantified assertion of Conjecture 5.1 with N(p) = 2p³+1. I tried to break each step and could not.
Each lemma was tested by my own brute-force code, written from the paper's definitions (not from the
solver's scripts), and the threshold inequality was checked in exact integers.

My scripts are in `work/S-1/rex_scripts/`.

## Step 1. The paper's exact definitions, and whether the proof proves the stated claim

Source: the live arXiv HTML (v1, 7 Nov 2026). It is byte-identical to the solver's
`selected_paper.html`. arXiv lists only v1.

| Item | Paper's wording | Proof's usage | Match |
|---|---|---|---|
| Zero forcing rule | a colored vertex with exactly one uncolored neighbor forces that neighbor | same | yes |
| Connected ZFS | S is a zero forcing set and the induced subgraph Γ\|S is connected | same | yes |
| Polynomial | Z_C^Γ(x) = Σ_k a_k x^k, where a_k counts the connected ZFS of size k | F_T(x) = Σ c_k x^k | yes |
| 𝔗_{n,p} | "all trees with n vertices and p many pendant vertices"; pendant means d(v)=1 | trees with n vertices and p leaves | yes |
| Order T ≥ T′ | §4: "minimal or maximal … coefficientwise minimal or maximal"; the theorems state Z_C(T,i) ≥ Z_C(T′,i) for 1≤i≤n | c_k(T) ≥ c_k(T′) for every k | yes |
| Conj. 5.1 | "For p≥5, there exists a sufficiently large integer N (depending on p) such that, for every n≥N, there is no unique tree T∈𝔗_{n,p} satisfying T≥T′, for every T′∈𝔗_{n,p}." | no tree at all satisfies T ≥ T′ for every T′ when n ≥ 2p³+1 | stronger |

**How to read "unique".** There are three possible readings:
- (a) "it is not the case that exactly one tree dominates all";
- (b) "there is no unique maximal tree";
- (c) "there is no greatest element".

The proof shows that **zero** trees dominate all trees, which gives (a) and (c) directly. For (b):
the polynomials form a finite poset with no greatest element, so it has at least two maximal
polynomials, and therefore at least two maximal trees. The proof says this in §5 and the reasoning
is correct. The paper's own examples (two or three incomparable maximal trees) show that (b)/(c) is
the intended reading. So none of the readings leaves a gap.

**Robustness check.** Suppose ≥ meant pointwise Z^T(x) ≥ Z^{T′}(x) for x > 0 instead of
coefficientwise. The argument still works, because it uses only the total at x=1 and the lowest
coefficient (x→0⁺).

**The second sentence of the conjecture** ("the number of pairwise incomparable maximal elements
tends to increase") is informal. §5 proves a lower bound, max{2,⌊p/3⌋}, that tends to ∞. It does
not prove monotonicity, and the solver says so. The main claim is the quantified first sentence,
and that is what was proved.

## Step 2. Line-by-line check of proof.md, with each lemma tested by my code

My code is `czf.py`. It applies the literal coloring rule to every connected vertex subset. For
n ≤ 14 it also checks **all 2ⁿ subsets**. Trees come from networkx `nonisomorphic_trees`, and the
tree counts match OEIS A000055.

- **§1. Every connected ZFS contains every branch vertex, and so contains the stem K.**
  - Argument: true. If v ∉ S, then S lies in one component of T−v, and at least two other
    components are uncolored. Only v can enter either of them, and v always has ≥2 uncolored
    neighbors there. This is also the paper's Lemma 3.1.
  - Test: holds for every connected ZFS of every non-path tree with n ≤ 15.
- **§1. Components outside K are p paths, one per leaf, attached at one end; Σd_i = n−s; each ZFS
  meets each path in a prefix.**
  - Argument: true.
  - Test: holds for every tree with n ≤ 15.
- **§1, (1): F_T(1) ≤ ∏(d_i+1).** True. I also checked the exact description it rests on:
  connected ZFS = K ∪ (prefixes, with at most one empty prefix at each attachment vertex). The two
  sets are equal for every tree with n ≤ 15.
- **§2, (2): AM–GM, then s ≥ 2.** True. With d_i ≥ 1, the sum of the (d_i+1) is n−s+p.
- **§3, (3): star total = ∏b_i + Σ_i ∏_{j≠i} b_j.**
  - Argument: true. It matches the paper's Lemma 3.3 at x=1.
  - Test: matches the brute-force count on every subdivided star with n ≤ 15.
- **§3, (4): F_B(1) ≥ q^p + (p+r)q^{p−1}.** True: binomial lower bound plus p products, each
  ≥ q^{p−1}.
- **§3, the remainder bound R < q^{p−1}.** I re-derived it.
  - C(p,j)·a^j ≤ 2p(p−1)(2p)^{j−2} uses a < 2, and the inequality is strict because a ≤ (2p−2)/p.
  - The geometric series gives 2p(p−1)q^{p−1}/(q−2p).
  - This is ≤ q^{p−1} if and only if q ≥ 2p².
  - n ≥ 2p³+1 gives n−1 ≥ 2p³, so q ≥ 2p².
  - (q+a)^p equals ((n+p−2)/p)^p exactly.
- **§3, conclusion.** A dominant tree has total ≥ F_B(1) > every tree with s ≥ 2. Since p ≥ 3,
  there is at least one branch vertex, so the dominant tree has s = 1, which means it is a
  subdivided star. This is correct: coefficientwise dominance implies dominance of the sums.
- **§4, (6): c_p(star) = p.**
  - Argument: true.
  - Test: holds on all stars with n ≤ 15.
- **§4, (7): c_p(D) = 2(p−2) for D = two adjacent hubs carrying 2 and p−2 pendant paths.**
  - Argument: true. D has n vertices, p leaves, and both hubs have degree ≥ 3, for every
    n ≥ p+2.
  - It agrees with the paper's own Corollary 3.6: the lowest coefficient is ∏ d_st(v).
  - Test: holds on all D-type trees with n ≤ 15.
  - Since 2(p−2) > p if and only if p > 4, no star dominates D. **The theorem follows.**
- **§5, (8): minimum ZFS size = s+p−t, and c_p = ∏k_i if t = s, else 0.**
  - Argument: true.
  - Test: holds on all trees with n ≤ 15.
- **§5, (9)/(10): balanced products, and M(p,c+1) > M(p,c) for c < ⌊p/3⌋.**
  - Argument: true. In the replacement argument, a ≥ 5 gives 2(a−2) > a, and three 4s become four
    3s (64 becomes 81). f ≥ 3 follows from p ≥ 3c+3.
  - Test: (9) matches a brute-force maximum for p ≤ 18; (10) holds for p ≤ 500.
- **§5, the stem-size separation and the maximal-element argument.**
  - The separation works: s < c is excluded by c_p; s > c is excluded by the same F(1) estimate,
    with n−c ≥ 2p³ so q ≥ 2p².
  - The B_c construction is valid: every stem vertex has k_i ≥ 3, so the stem is exactly the path.
  - The chain "maximal, distinct, therefore incomparable" is correct.

**Lemma-test totals.** 0 failures over:
- all non-path trees with 4 ≤ n ≤ 15, 13,173 trees in total (the n=16 run was stopped at the
  10-minute limit before it finished);
- of these, all trees with n ≤ 14 were also checked by literal enumeration of all 2ⁿ subsets.

My closed form x^s·∏_v[∏P(b)+Σ∏_{≠}P(b)] equals the brute-force polynomial for every one of these
trees.

**Does a dominant tree exist? (my enumeration, all trees in 𝔗_{n,p})**
- Brute-force polynomials were used for n ≤ 14 and the validated closed form for 15 ≤ n ≤ 19.
- The table below gives, for each p, the values of n with 5 ≤ n ≤ 19 at which a greatest element
  exists. All figures are from my own runs (`dom_brute.log`, `dom_formula.log`); the solver's
  figures are not used.

| p | n with a greatest element (n ≤ 19) | first n with no greatest element | stays absent through n=19 |
|---|---|---|---|
| 5 | 6, 7, 8 | 9 | yes |
| 6 | 7, 8, 9, 10 | 11 | yes |
| 7 | 8 to 11 | 12 | yes |
| 8 | 9 to 12 | 13 | yes |
| 9 | 10 to 14 | 15 | yes |
| 10 | 11 to 15 | 16 | yes |

Every p shows the same pattern: a greatest element exists only for p+1 ≤ n ≤ about 1.5p, and then
never again within the range I could reach.

**Agreement with the paper.** These results agree with every number in the paper:
- p=5: H^n_{2,3} is the maximum at n=7 and n=8, and there is none for n ≥ 9.
- n=10: three pairwise incomparable maximal elements.
- p=8: a unique maximum for n=10–12, and none at n=13.
- The p=8 polynomials at n=13 are reproduced, with totals 144 and 147.

**Consistency.** None of this contradicts the claim. Every observed failure of dominance begins far
below 2p³+1.

**Note on the size of N.** Between those small n and the threshold, the star is *not* the
F(1)-maximiser. For example:
- p=7, n=17: a two-hub tree has 1360 sets, against 1200 for the best star.
- p=6, n=16: 784 against 756.

So the F(1) step really does need large n. It is a large-n argument and makes no claim about small n.

## Step 3. Exact check of the inequality behind N(p) = 2p³+1 (`exact_ineq.py`, integers and Fractions)

- **Main inequality.** For every p from 5 to 60, I checked every n in [2p³+1, 2p³+2p]. That covers
  every residue r of n−1 mod p twice, including the boundary n = 2p³+1, where q = 2p² and r = 0.
  The following all hold:
  - p^p·F_B(1) > (n+p−2)^p, exactly;
  - F_B(1) ≥ q^p+(p+r)q^{p−1};
  - R < q^{p−1}, with R computed exactly as a Fraction;
  - q ≥ 2p².

  There were 0 failures. The smallest case, p=5 and n=251, holds.
- **§5's inequality.** p^p·F_{B_c}(1) > (n+p−c−1)^p holds for all c ≤ ⌊p/3⌋ at
  n ∈ [2p³+m, 2p³+m+2p], for p ≤ 60.
- **How much slack the threshold has.** I replaced AM–GM by the integer-optimal bound
  max∏(d_i+1). The star then wins for all n > 38 (p=5), n > 70 (p=6), n > 121 (p=7), n > 187 (p=8)
  and n > 275 (p=9). So 2p³+1 is valid but about 6× larger than needed.
- **Bonus: p=5 at every n ≥ 9 (`p5_full.py`).** A dominant tree must maximise c_5, and 6 is
  attained only by the adjacent (2,3)-hub trees.
  - For 9 ≤ n ≤ 40, none of these trees dominates every subdivided star.
  - For 41 ≤ n ≤ 251, the star beats the integer prefix bound.
  - From 251 on, the proof applies.

  So for p=5 the true threshold is N=9, exactly as the paper reports.

## Step 4. Search for a prior resolution

- **arXiv.** The abstract page lists only v1 (7 Nov 2026). The arXiv API phrase search for
  "connected zero forcing polynomial" returns only this paper, so there are no later or citing
  arXiv papers.
- **`gh search issues/prs --repo the-omega-institute/trureturing`.** I searched for "2611.10985",
  "Mukherjee Ray", "connected zero forcing polynomial" and "connected forcing polynomial". The hits
  concern only **Problem 5.2** (issues #30379, #33479) and **Problem 5.3** (issues #31033, #31076;
  PRs #31101 and #32560, both merged, which refute 5.3). Issue #32504 registers path and star
  modules. None of them addresses Conjecture 5.1.
- **`--repo 1337isnot1337/solved-conjectures`.** No hits for 2611.10985, Mukherjee, or connected
  zero forcing. The only zero-forcing issue, #323, is the Boyer et al. path conjecture, which is
  unrelated.
- **Conclusion.** No prior resolution was found. The search is limited to these sources and is not
  exhaustive.

## How much the result matters

The result is correct, but small.
- **Half of it is already in the paper.** The x^p coefficient is the paper's own Corollary 3.6, and
  the paper prints 5x⁵ against 6x⁵ in Example 4.17. So "no star dominates H_{2,p−2}" is one line
  from the paper.
- **The only new ingredient** is that, for n ≫ p³, the balanced subdivided star has the largest
  total number of connected ZFS. That is a routine AM–GM plus binomial estimate.
- **Assessment.** It settles a three-week-old conjecture with an elementary two-page argument and a
  non-sharp cubic threshold. It is worth a short note or a comment to the authors, not a paper on
  its own. The growth sentence is only handled in a weak lower-bound form.
