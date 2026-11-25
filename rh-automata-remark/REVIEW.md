# N-1 review: "An explicit fourth-root correction to unary determinization"

Referee: max (checker), task N-1.c1, 25 Nov 2026. RH is taken as given (stipulated). Local files only.

## Verdict

**Confirmed. Every step holds.** The theorem is correct as stated, given RH. It is also new in the sense that I could not find it written down. But it is a routine two-line corollary: a known RH result about Landau's function, put into a known automata sandwich. It is a remark, not a theorem anyone would cite for its proof.

## 1. Sources checked word for word

Sources were downloaded and read in full text:
- Deléglise–Nicolas, arXiv:1907.07664v1 (60 pp.).
- Geffert, Information and Computation 205 (2007) 1652–1670, published PDF (19 pp.) at im.saske.sk.

**Deléglise–Nicolas (D–N)**
- Landau's g: (1.1) `g(n) = max_{ℓ(M) ≤ n} M`, where ℓ is the additive function with ℓ(p^α) = p^α. This is the largest product of prime powers with sum ≤ n. It is the same as the maximum order of an element of S_n.
- (1.9): `a_n = (√li⁻¹(n) − log g(n)) / (n log n)^{1/4}`, for n ≥ 2. Matches the claim.
- (1.11): `c = Σ_ρ 1/|ρ(ρ+1)| = 0.046 117 644 421 509…`. Matches.
- §2.2: li(x) is the principal value of ∫₀ˣ dt/log t, for x > 1. Matches. My program gives a_2 = 0.910235, the same as D–N's printed a_2 = 0.9102…. So the li convention and the natural log are confirmed.
- Theorem 1.1(v), under RH: `0.149… = (2−√2)/3 − c ≤ lim inf a_n ≤ lim sup a_n ≤ (2−√2)/3 + c = 0.241…`. Quoted correctly.
- (1.7): log g(n) ~ √(n log n) (Landau). Correct.
- Corollary 1.3: "Each of the six points of Theorem 1.1 is equivalent to the Riemann hypothesis." The proof uses Nicolas 1969: if RH fails, `log g(n) = √li⁻¹(n) + Ω±((n log n)^b)` for some b > 1/4.

**Geffert**
- Model (§2): the NFA is `M = (Q, Σ, δ, q_S, F)` with `δ : Q×Σ → 2^Q`. It has a single initial state and no ε-moves. A DFA has `|δ(q,s)| = 1`, so it is complete. Theorem 3.6 counts the empty-set (dead) state. This matches the claim's model.
- (1): `F(n) = max{lcm{ℓ₁,…,ℓ_m} : ℓ₁+…+ℓ_m = n}`. He calls it "Landau's function". The parts are positive integers that sum to exactly n. g is non-decreasing (you can pad with 1s), so the "= n" and "≤ n" conventions agree. **F = g exactly.**
- Theorem 3.7: "Let M be a unary nfa with **at most** n > 1 states. Then M can be replaced by an equivalent dfa M′ using at most d ≤ F(n−1) + (n²−2) ≤ e^{(1+o(1))√(n ln n)} states." Quoted correctly. The proof also covers the trivial n-cycle case (d = n).
- Theorem 5.2: "Gmax(n) = F(n−1) + k_n, for some k_n ∈ {0,…,n²−2}". Gmax(n) is the largest "muggle" number. A muggle number is a minimal-DFA size realised by a language whose **optimal NFA has exactly n states** (Definition 5.1). Quoted correctly, and Astra described the "exactly n" scope correctly.
- Lower witness for "at most n": in the proof of 5.2, L₀ = {1^u : u mod F(n−1) ≠ 0} has an NFA with ≤ 1 + Σ prime-power parts ≤ n states. Its minimal complete DFA has exactly F(n−1) states. Also Gmax(n) ≥ F(n−1).

So **g(n−1) ≤ D(n) ≤ g(n−1) + n² − 2 for n ≥ 2**. This is correct.

My own brute force checked every unary NFA with n ≤ 4 states (single initial state, all transition relations, all final sets) and computed the exact minimal complete DFA size:
- D(2) = 3, in the window [1, 3].
- D(3) = 6, in the window [2, 9].
- D(4) = 11, in the window [3, 17].

## 2. Transfer step

Put m = n−1 and N_m = (m log m)^{1/4}. Take n ≥ 3, so that m log m > 0. Then:

Q_n − a_m = −log(D(n)/g(m)) / N_m,  with  0 ≤ log(D(n)/g(m)) ≤ log(1 + (n²−2)/g(m)) ≤ (n²−2)/g(m).

g(m) = e^{(1+o(1))√(m log m)} is superpolynomial, so (n²−2)/g(m) → 0. Then Q_n = a_{n−1} − ε_n with 0 ≤ ε_n → 0. The shift is used the same way in li⁻¹ and in the normalising factor, as m = n−1 in both. So lim inf and lim sup of Q_n equal those of a_{n−1}, and the bounds transfer unchanged.

Numerics (program `N-1.c1/check.py`, exact g(m) for m ≤ 3000; g checked against OEIS A000793):
- ε_n ≤ 3.0e-10 for every n ≥ 201. It is 9.5e-6 at n = 101 and 0.0038 at n = 51. The additive n² term is negligible, as claimed.
- Endpoints, computed from D–N's printed c:
  - A = (2−√2)/3 = 0.195262145876.
  - A − c = 0.149144501454 and A + c = 0.241379790297. Both match the claim.
- Θ statement: A − c > 0 and A + c < ∞. Also (n log n)^{1/4} / ((n−1)log(n−1))^{1/4} → 1. So D(n) = exp(√li⁻¹(n−1) − Θ((n log n)^{1/4})) is correct.

The Q_n ≤ a_{n−1} side is exact, so D–N's effective bounds transfer too. Under RH, Q_n ≤ A + c + 1.02·log log(n−1)/log(n−1) for n ≥ 19426 (from (iii)). Q_n ≥ A − c − 0.43·log log(n−1)/log(n−1) − ε_n for n ≥ 3 (from (ii)).

Caution (not part of the claim): the all-n inequality of type (i) does not transfer at small n. Brute force gives log D(3) = log 6 = 1.792 > √li⁻¹(2) = 1.681, and log D(4) = log 11 = 2.398 > √li⁻¹(3) = 2.011. Geffert's upper bound gives log D(n) < √li⁻¹(n−1) only from n = 15 on. Under RH, D–N (iv) plus the ε_n bound then give it for all n ≥ 15.

## 3. Genuinely conditional on RH?

Yes. In fact the automata statement is **equivalent** to RH. If RH fails, Nicolas's Ω±((n log n)^b) oscillation with b > 1/4 passes through the o(1) perturbation. Then Q_n is unbounded in both directions. Unconditionally one only has Nicolas's error O(√n·exp(−a√log n)), which is far weaker than (n log n)^{1/4}. So this is not a known unconditional estimate in disguise.

## 4. Novelty: what I searched

- Web, extended and standard: "unary NFA to DFA Landau function Riemann hypothesis"; "Landau's function" with "inverse logarithmic integral", automata and state complexity; Chrobak, Landau, Riemann and Nicolas together; "state complexity" or "descriptional complexity" with "Riemann hypothesis", Landau and unary; "Landau's function" "Riemann hypothesis" "finite automata". No source links RH, or li⁻¹, to unary determinization.
- OpenAlex citation graph:
  - D–N is cited by 3 works, all number theory.
  - Works citing Geffert 2007 whose full text contains "Riemann hypothesis": 0.
  - Works citing Chrobak 1986 with "Riemann hypothesis": 2. Both are unrelated: a σ₁ remark in arXiv:2501.14725, and Miller–Rabin/ERH in arXiv:2610.27314. I checked both texts.
  - Works citing Nicolas 1969: 34. The automata ones (Holzer–König on syntactic monoid size, 2003/04; inverse semigroups, 2010) do not overlap with the "Riemann" full-text set.
- Petrov arXiv:2209.07362 (Landau–Okhotin function, from automata) has no RH content.

Finding: not found anywhere. The limit is that OpenAlex full-text coverage is partial, and a one-line remark in a talk or survey could be missed.

## 5. Significance

This is a direct substitution. Two points show how thin it is:
- **Geffert's refinement is not needed.** The classical Chrobak-level sandwich g(n−1) ≤ D(n) ≤ g(n) + O(n²) already gives the same lim inf/lim sup bounds. a_n and a_{n−1} are both eventually in the window, and √li⁻¹(n) − √li⁻¹(n−1) ~ ½√(log n / n) → 0. The model with several initial states (D ≈ g(n)) also gives the same constants. So the result does not depend on any fine automata fact. Only "D(n) is Landau's function up to an index shift and a polynomial" is used.
- **It has no practical reach.** At computable sizes a_m stays high: its minimum over 2 ≤ m ≤ 3000 is 0.396 (at m = 1709), and sampled values are 0.45–0.61. That is far above the asymptotic window [0.149, 0.241], and convergence is logarithmically slow. It says nothing new about which automata exist. It only restates the RH-sharp asymptotics of g(n−1).

Honest rating: **a nice remark**, at most a footnote in a survey. It could be phrased as "RH is equivalent to the unary determinization blow-up having a fourth-root correction". It is not a theorem anyone would cite for its proof. No logical gap.

## Files

- `N-1.c1/check.py`: g(m) by exact knapsack, brute-force D(n) for n ≤ 4, a_m and ε_n up to m = 3000, endpoints.
- `N-1.c1/check_out.txt`: the output of `check.py`.
- `N-1.c1/smalln.py`: the small-n check of the all-n inequality.
