# REVIEW of card B-T2 (referee: checker-2, 25 Nov 2026)

Write-up under review: lane-b-sequences/t4_designated/CANDIDATE_PROOF_3adic.md (plan_3adic.py, prove_3adic_impl2.py).
Paper: Yaqubi and Mirzavaziri, "Partitions with designated summands: k-tuples and their congruences", arXiv:2611.05623v1 (3 Nov 2026; v1 is the only version).

**Verdict: confirmed-proof.** Every step holds, and the reasons are given below. I did not reuse the authors' code. My own bookkeeping and coefficient programs reproduce every number in their table. All six congruences hold to their Sturm ranges and beyond. This is still a computer-assisted argument that no human has refereed. It relies on four standard theorems, stated in step 3.

## Step 1. Statements and indexing (read from the PDF, paper_dl/paper.txt)
- Definition 2.1: sum_{n>=0} A_k(n) q^n = F^k, F = f6/(f1 f2 f3), f_d = prod (1-q^{dn}). F = 1 + q + 3q^2 + 5q^3 + 10q^4 + ...
  The write-up uses the same F, k and n>=0 indexing. I also checked F against the combinatorial definition, which marks one part of each size. I enumerated those partitions by brute force for n <= 20 and used the product prod_t (1 + q^t/(1-q^t)^2) for n <= 112,400. Both agree with f6/(f1 f2 f3).
- Conjecture 6.3 (quoted): "For all n >= 0, A6(12n + 10) ≡ 0 (mod 3^5), and 3^5 is the exact power of 3 dividing all of them."
- Conjecture 6.4 (quoted): "(a) A3(12n + 7) ≡ A3(12n + 11) ≡ 0 (mod 3^4). (b) A4(6n + 5) ≡ 0 (mod 3^3) and A7(12n + 11) ≡ 0 (mod 3^3). (c) A8(18n + 15) ≡ 0 (mod 3^5)."
  The six (k, m, r, t) in the write-up match these statements exactly.
- The "exact power" clause. The wording "the exact power of 3 dividing all of them" means the largest common power. One term with v3 = 5 is therefore enough. I computed exact big integers: A_6(22) = 6635911068 = 3^5 * 27308276, and 3 does not divide 27308276, so v3 = 5. The conjecture holds in this reading.
  Warning on the other reading: if the clause meant that each term has v3 exactly 5, it would be FALSE already at n = 0. A_6(10) = 384183 = 3^6 * 527. Up to n = 112,400, 3848 of the 9366 terms have v3 >= 6. The trureturing registrations (#26878, #30694) also adopt the common-power reading. The write-up proves the common-power reading, and that is the right one.

## Step 2. "Multiply by an eta-quotient ≡ 1 mod 3^t"
The final proof does not use this step. TARGETS.md mentions the plan F^k * (f_d^3/f_{3d})^{...} ≡ F^k only as an early idea. The write-up instead multiplies by Delta(mz)^c = eta(mz)^{24c} = q^{mc} prod(1-q^{mn})^{24c}. That is an exact identity with no congruence involved.
- Every exponent of Delta(mz)^c is ≡ 0 mod m, and its leading coefficient is 1. So class_r(g) = Delta(mz)^c * class_r(F^k) exactly, and class_r(F^k) = class_r(g) * q^{-mc} prod(1-q^{mn})^{-24c}, where the second factor is in Z[[q^m]]. One class vanishes mod 3^t if and only if the other does. Checked.
- Finite reduction: a_g(n) = sum_j delta_j A_k(n - mc - mj). Every argument is in the same class and is at most n. So checking A_k(n) ≡ 0 for n ≡ r (mod m), n <= pB, gives a_g(n) ≡ 0 in the same range. Checked.
- q-shift: F has none because (6-1-2-3)/24 = 0. The shift of g is exactly q^{mc}, and my code checks this.

## Step 3. Modular-forms bookkeeping
I recomputed everything in bookkeeping.py, written from scratch (log: bookkeeping.log).

| claim | c | eta exponents of g | weight | N | chi | min leading exp. over all cusps | U_p | class | level N m'^2 | index (formula = P^1 count) | Sturm B | need n <= |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6.3 A6(12n+10) 3^5 | 5 | 1:-6 2:-6 3:-6 6:6 12:120 | 54 | 12 | trivial | 0 | 2 | 5 mod 6 | 432 | 864 | 3888 | 7776 |
| 6.4a A3(12n+7) 3^4 | 3 | 1:-3 2:-3 3:-3 6:3 12:72 | 33 | 24 | (-1/d) | 1/24 | 1 | 7 mod 12 | 3456 | 6912 | 19008 | 19008 |
| 6.4a A3(12n+11) 3^4 | 3 | same | 33 | 24 | (-1/d) | 1/24 | 1 | 11 mod 12 | 3456 | 6912 | 19008 | 19008 |
| 6.4b A4(6n+5) 3^3 | 2 | 1:-4 2:-4 3:-4 6:52 | 20 | 18 | trivial | 1/18 | 1 | 5 mod 6 | 648 | 1296 | 2160 | 2160 |
| 6.4b A7(12n+11) 3^3 | 6 | 1:-7 2:-7 3:-7 6:7 12:144 | 65 | 72 | (-1/d) | 1/72 | 1 | 11 mod 12 | 10368 | 20736 | 112320 | 112320 |
| 6.4c A8(18n+15) 3^5 | 10 | 1:-8 2:-8 3:-8 6:8 18:240 | 112 | 18 | trivial | 0 | 3 | 5 mod 6 | 648 | 1296 | 12096 | 36288 |

All of these match plan_3adic.json.

(a) **Modularity of g.** I used Gordon–Hughes–Newman (Ono, *Web of Modularity*, Thm 1.64). Every delta divides N, the weight is an integer, sum delta*r_delta ≡ 0 (mod 24) and sum (N/delta)*r_delta ≡ 0 (mod 24). Under these conditions g ∈ weight-w forms for Gamma_0(N) with chi(d) = ((-1)^w s / d), where s = prod delta^{r_delta}. Here s is a perfect square times 1, so chi is trivial for even w and (-1/·) for odd w. The parity is consistent, so the spaces are not forced to be zero.

(b) **Holomorphy at every cusp.** I used my own formula: for gamma = [a b; c d] in SL2(Z), the slash g|gamma starts at q^{v(c)} with v(c) = sum r_delta gcd(c,delta)^2/(24 delta). I checked v(c) >= 0 for every c = 0..N-1. Ligozat's normalised orders are also printed (Ono Thm 1.65), and the minimum is >= 0 in all six cases. The order is 0 at the cusp 0 for 6.3 and 6.4c, which is holomorphic but not cuspidal, and that is enough. So g ∈ M_w(Gamma_0(N), chi) with integer coefficients.

(c) **U_p (6.3: p=2 | 12; 6.4c: p=3 | 18).** For p | N, U_p = T_p preserves M_w(Gamma_0(N), chi) (Diamond–Shurman §5.2–5.3: T_p acts on M_k(Gamma_1(N)), commutes with the diamond operators, and chi(p) = 0). Holomorphy at the cusps is preserved because g|U_p is a sum of g|[1 j; 0 p]. Coefficients: b(n) = a_g(pn), so class r' mod m' of g|U_p is class r mod m of g. Checked.

(d) **Residue-class extraction to level N m'^2.** The write-up cites Ono Prop 2.8 for twists. I did not check that proposition number, so I re-proved the step directly. It needs no characters.
Let G ∈ M_w(Gamma_0(N), chi) and h = (1/m') sum_j zeta^{-r'j} G|T_j, with T_j = [1 j/m'; 0 1]. Then h is the part of G on exponents ≡ r' mod m'. Take gamma = [a b; c d] ∈ Gamma_0(N m'^2) and put j' ≡ j d^2 (mod m'). Then T_j gamma T_{j'}^{-1} is an integer matrix in Gamma_0(N) with lower-right entry ≡ d (mod N m'). This uses c ≡ 0 mod N m'^2 and ad ≡ 1 mod m'. Hence G|T_j|gamma = chi(d) G|T_{jd^2}, and h|gamma = chi(d) * (class r' d^{-2} of G).
When m' | 24, every unit satisfies d^2 ≡ 1 mod m', so h|gamma = chi(d) h. Here m' ∈ {6, 12}, which divides 24. Holomorphy at the cusps carries over from G, because T_j gamma is in SL2(Z) times an upper-triangular matrix.
So h ∈ M_w(Gamma_0(N m'^2), chi). Its coefficients are a subset of G's, so they are integers. The level is right, and the coprimality gcd(r', m') = 1 is not even needed.

(e) **Sturm for a prime power with a quadratic character.** The theorem relied on is Sturm (1987), Thm 1: if f ∈ M_k(Gamma_0(L)) has integer coefficients and ord_3(f) > k[SL2(Z):Gamma_0(L)]/12, then f ≡ 0 mod 3.
  - Character: chi is quadratic. If h ≢ 0 mod 3 with ord_3(h) = n0 > w*i/12, then h^2 ∈ M_{2w}(Gamma_0(L)) has trivial character and ord_3(h^2) = 2 n0 > 2w*i/12, because F_3[[q]] is an integral domain. Sturm then gives h^2 ≡ 0, a contradiction.
  - Prime power, by induction: if h ≡ 0 mod 3^s entirely and s < t, then h/3^s is in the same space with integer coefficients and vanishes mod 3 up to B. So it vanishes mod 3 entirely, and h ≡ 0 mod 3^{s+1}.
  - Hence: vanishing mod 3^t for all n <= B = floor(w*i/12) implies vanishing mod 3^t for every n.

  The write-up uses exactly this B, the index of the final level, and checks n <= pB in terms of A_k. Checked.

## Step 4. My own recomputation (ak_ref.c, full_run.log; exact_small.py, exact_small.log)
- Route 1: F mod 3^10 from the combinatorial product prod_t (1 - q^t + q^{2t})/(1 - q^t)^2.
- Route 2: F from f6/(f1 f2 f3) with Euler's pentagonal theorem. The two routes agree at all 112,401 indices.
- Powers by dense truncated convolution: F^2, F^3, F^6, F^7 to n = 112,400, and F^4, F^8 to n = 40,000. These are cross-checked by different associations (F^4*F^3 = F^7, F^7*F = F^8, F^4*F^2 = F^6), with 0 mismatches.
- Exact big-integer series (Python) for n <= 400 agree with the C residues for k = 3, 4, 6, 7, 8.
- Results (n ≡ r mod m):

| claim | bound | terms to bound | min v3 to bound | further range | min v3 there |
|---|---|---|---|---|---|
| 6.3 A6(12n+10), 3^5 | 7776 | 648 | 5 | n <= 112400 (9366 terms) | 5 |
| 6.4a A3(12n+7), 3^4 | 19008 | 1584 | 4 | n <= 112400 | 4 |
| 6.4a A3(12n+11), 3^4 | 19008 | 1584 | 4 | n <= 112400 | 4 |
| 6.4b A4(6n+5), 3^3 | 2160 | 360 | 3 | n <= 40000 | 3 |
| 6.4b A7(12n+11), 3^3 | 112320 | 9360 | 3 | n <= 112400 | 3 |
| 6.4c A8(18n+15), 3^5 | 36288 | 2016 | 5 | n <= 40000 | 5 |

There are no failures. The run took 29 s and 4.5 MB.

## Step 5. Prior-proof search (25 Nov 2026)
- arXiv: 2611.05623 has only v1. An arXiv API search for "designated summands" by date found two later papers, 2611.15164v2 and 2611.28840. Both are about PDO_t (odd parts, tagged-part totals), not the k-tuples A_k, and neither treats Conj. 6.3 or 6.4. Semantic Scholar returned rate-limited (429).
- Web search (two queries) found only the paper itself, with no proof.
- Davis catalogue (source/davis-CONTENTS.md): no hit for 2611.05623, Yaqubi, Mirzavaziri or designated.
- 1337isnot1337/solved-conjectures and demonstrandum-research/artifacts: no issues for 2611.05623, "designated summands" or Yaqubi.
- the-omega-institute/trureturing:
  - #26878 is OPEN (last update 9 Nov), #26887 is OPEN (5 Nov) and #30694 is OPEN (15 Nov, carrier failure). None claims a proof of the universal clause. #26878 records that rainwangphy/aftd-platform has Lean proofs of single instances only: 3^5 | A_6(10), 3^5 | A_6(22) and 3^6 ∤ A_6(22). Those are prior art for the sharpness witness, which the write-up already says is "recorded by others".
  - No issue or blueprint covers Conjecture 6.4.
  - Code search: Blueprint/.../DesignatedSummandCongruence.md marks Conjecture **6.1** (the 2-adic one) as **proved** ("Resolves ... conjecture-6-1 (proved)"). Issues #33469 and #33480 are open preregistrations on 6.1. This is relevant to the 2-adic card, not to this one.
- Conclusion: there is no prior proof of 6.3 or 6.4 that I could find. The proof is new as far as this search reaches.

## Remaining caveats (none is a gap in the argument)
1. The argument cites four standard theorems and does not re-prove them: Gordon–Hughes–Newman, Ligozat, U_p for p | N, and Sturm. The extraction step is re-proved above, and the steps from Sturm to prime powers and to a character are given.
2. The "exact power" clause is proved in the common-power reading. The termwise reading is false at n = 0, so if anyone means that reading, say so explicitly.
3. The write-up's extra check of all six progressions to n <= 10^6 was not re-run. It is not needed for the proof.
