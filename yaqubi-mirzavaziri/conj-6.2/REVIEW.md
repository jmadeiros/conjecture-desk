# REVIEW of card B-T1: Conjecture 6.2 of Yaqubi–Mirzavaziri (arXiv:2611.05623v1)

Referee: checker-1, 25 Nov 2026. Reviewed: `lane-b-sequences/t4_designated/CANDIDATE_PROOF_2adic.md` (the Conjecture 6.2 half only;
the 6.1 half is a different card and is already proved elsewhere, see step 5).

**Verdict: confirmed-proof.** Every step holds; reasons below. This is still a computer-assisted proof, checked by
three separate programs (two by the attacker, one by me), not peer reviewed and not formalised.

## Step 1. Statement, definitions, indexing (read from the arXiv TeX source of v1 myself)

- Paper, Definition in Sec. 2: sum B_k(n) q^n = G^k, G = f_4 f_6^2/(f_1 f_3 f_12) = 1+q+2q^2+4q^3+5q^4+...
  (the write-up calls this series P; its "Q" is 1/P. The paper's G and the write-up's G are different series, which
  is a notation trap but not an error.) I re-derived the product from the combinatorial definition:
  prod_{t odd}(1+q^t/(1-q^t)^2) = prod_{t odd}(1+q^{3t})/((1-q^t)(1-q^{2t})) = f_4 f_6^2/(f_1 f_3 f_12).
- Conjecture 6.2 (label conj:B2adic), verbatim: "For every k>=1, the largest power of 2 dividing all B_k(4n+3) is
  2^{v_2(B_k(3))}, except when k = 1 (mod 8) (where it is exactly 2^2) or k = 6 (mod 8) (where it is exactly 2^3, as
  established in Theorem 4.6)." The write-up quotes this correctly.
- B_k(3) = k(k+2)(k+7)/6: re-derived by hand (4k + 2k(k-1) + C(k,3)) and checked exactly for k = 1..60.
- Indexing: B_k(4n+3), n >= 0, is the coefficient of q^{4n+3}; the write-up's T3 extracts exponents = 3 mod 4. Same.
- Target t(k) = v_2(k)+v_2(k+2)+v_2(k+7)-1 equals v_2(B_k(3)) because v_2(6) = 1. Correct.
- Only arXiv version is v1 (abs page checked 25 Nov 2026).

## Step 2. Reduction from all k to finitely many classes: holds

- Lemma 1 (h in 1+qZ[[q]]: h^{2^e} = h(q^2)^{2^{e-1}} mod 2^e; for e>=2, h^{2^e} = h(q^4)^{2^{e-2}} mod 2^{e-1}).
  Proof checked: h^2 = h(q^2) mod 2 (a^2 = a mod 2 and cross terms are even); x = y mod 2^j gives x^2 = y^2 mod 2^{j+1};
  the second form is the first applied to h(q^2) with e-1. Negative exponents are fine because both sides are units.
- Lemma 2 (j <= e-1: T3(h^{k+2^e m}) = 0 mod 2^j iff T3(h^k) = 0 mod 2^j). Checked:
  h^{k+2^e m} = h^k U(q^4) mod 2^{e-1}, U in 1+q^4 Z[[q^4]]. Multiplying by a series in q^4 keeps exponents mod 4,
  so T3(h^k U(q^4)) = T3(h^k) U(q^4), and U is invertible. Both directions hold, so it gives lower bounds and
  exactness. So "T3(P^k) = 0 mod 2^j" depends only on k mod 2^{j+1}, negative representatives allowed.
- Case split, k mod 8 (all eight classes are covered):
  - 0, 4: e = v_2(k) >= 2, t = e. P^k = P(q^2)^{2^{e-1} m} mod 2^e is a series in q^2, so all odd coefficients are
    = 0 mod 2^e. Upper bound is n = 0. Correct.
  - 3, 7: t = 0. Nothing to prove. Correct.
  - 5: t = 1. Class k mod 4 = 1 = -3: needs T3(Q^3) = 0 mod 2 (B1). Correct.
  - 1: claimed 2. Lower bound, k mod 8 = -7: T3(Q^7) = 0 mod 4 (B2). Exactness (j=3, depends on k mod 16; classes 1, 9
    = -15, -7): T3(Q^15), T3(Q^7) not = 0 mod 8 (B3). Correct.
  - 2: t = 2 (v_2(k+2) = 2). Class -6 mod 8: T3(Q^6) = 0 mod 4 (B4). Correct.
  - 6: claimed 3. Lower bound, k mod 16 in {6, 14} = {-10, -2}: (B5). Exactness, k mod 32 in {6,14,22,30} =
    {-26,-18,-10,-2}: (B6). All four classes are listed. Correct.
- Side remark (strengthens the result): B1, B2, B4 and the lower half of B5/B6 are already theorems in the paper
  (Thm 4.3(b),(c), Thm 4.5(a),(b), Thm 4.6; numbering from the v1 TeX counters). The only parts of 6.2 not in the paper are the k = 0 mod 4 classes
  (Lemma 1, elementary) and exactness for k = 1 mod 8 (Lemma 2 plus two exact integers). So those items have two
  independent proofs (the paper's dissections, and the Sturm checks below).

## Step 3. Modular-forms bookkeeping: holds

For f = Delta(4t)^c Q^j = eta(t)^j eta(3t)^j eta(4t)^{24c-j} eta(6t)^{-2j} eta(12t)^j (I derived this by hand and by code):
- Weight (sum r)/2 = 12c. Order at infinity (sum delta r)/24 = 4c, so f = q^{4c} x (unit series in q^4) x Q^j and
  T3(f) = Delta(4t)^c T3(Q^j): the two vanish mod the same powers of 2.
- Newman (Gordon–Hughes–Newman, Ono Web of Modularity Thm 1.64): sum delta r = 96c = 0 mod 24;
  sum (N/delta) r = N(5j/6 + 6c) = 0 mod 24 iff (N = 12M) jM = 0 mod 12. Smallest N: j=3: 48, j=7: 144, j=6: 24,
  j=10: 72, j=2: 72. Same as the write-up.
- Character: s = prod delta^r = 2^{48c-2j}, a square, weight even, so chi = (s/d) is trivial. (Write-up says "N | 144"
  but does not name the character; it is trivial.)
- Ligozat at cusp c/d: sign of S(d) = sum gcd(d,delta)^2 r_delta/delta. By hand: the binding cusps are
  gcd(d,4)=2 with 3|d, S = 24c - 6j, so holomorphic iff c >= j/4 (others need c >= j/36, j/72, or are always > 0).
  c = 1,2,2,3,1 for j = 3,7,6,10,2 all satisfy it, and each is the smallest such c. Code confirms over every d | N
  (smallest cusp order 1, at d = 6, in every item).
- Extracting 4n+3: I re-derived the level directly instead of relying on the twist proposition.
  T3(f)(t) = (1/4) sum_{r=0..3} i^{-3r} f(t + r/4). For gamma = [a b; c d] in Gamma_0(16N), with alpha = [1 r/4; 0 1],
  alpha gamma alpha^{-1} = [a+rc/4, b + r(d-a)/4 - r^2 c/16; c, d - rc/4]. Here 16 | c, ad = 1 mod 16 forces a, d odd
  and d = a^{-1} = a mod 8, so all entries are integers, the matrix is in Gamma_0(N) and its lower-right entry is
  d mod N. Hence f(t + r/4), and so T3(f), lies in M_w(Gamma_0(16N), chi), holomorphic at every cusp, integer
  coefficients. This agrees with the write-up's level 16N (Ono Prop. 2.8 gives the same).
- Sturm bound: B = floor(w [SL2(Z):Gamma_0(16N)]/12) = 1536, 9216, 1536, 6912, 2304 for B1, B2, B4, B5(j=10), B5(j=2).
  Same as the write-up.
- Theorem relied on: Sturm (1987, "On the congruence of modular forms", LNM 1240, Thm 1; also Stein, "Modular Forms:
  A Computational Approach", Thm 9.18): if Gamma has index mu in SL2(Z), f in M_k(Gamma) has q-expansion coefficients
  in O_K and lambda is a prime of O_K with ord_lambda(f) > k mu/12, then f = 0 mod lambda. No condition that lambda
  is prime to the level, so p = 2 with even level is allowed. Here the character is trivial, K = Q, lambda = 2.
  Prime powers: if T3(f) = 0 mod 2^s (s < t), then T3(f)/2^s is in the same space with integer coefficients and
  its first B coefficients are still = 0 mod 2, so Sturm mod 2 gives T3(f) = 0 mod 2^{s+1}. Induction gives mod 2^t.
  "n <= B" with B = k mu/12 an integer gives order >= B+1 > k mu/12, as required.

## Step 4. My own program: all items pass

Files: `eta2.c` (C; expands q^shift prod (1-q^{delta m})^{r_delta} by single-factor multiply/divide, arithmetic in
Z/2^64, which is exact for v_2 up to 64) and `referee.py` (exact Fractions for the bookkeeping, Python big integers for
witnesses, and a big-integer cross-check of the C residues). Neither uses the attacker's code. Log: `referee.log`.

| item | form | N | w | B | min v_2, n = 3 mod 4, n <= B (f) | same for Q^j | needed |
|---|---|---|---|---|---|---|---|
| B1 | Delta(4t) Q^3 | 48 | 12 | 1536 | 1 | 1 | 1 |
| B2 | Delta(4t)^2 Q^7 | 144 | 24 | 9216 | 2 | 2 | 2 |
| B4 | Delta(4t)^2 Q^6 | 24 | 24 | 1536 | 2 | 2 | 2 |
| B5 | Delta(4t)^3 Q^10 | 72 | 36 | 6912 | 3 | 3 | 3 |
| B5 | Delta(4t) Q^2 | 72 | 12 | 2304 | 3 | 3 | 3 |

Exactness witnesses, exact integers, all equal to the write-up's values:
[q^7]Q^7 = 188 (v_2 2), [q^3]Q^15 = -260 (v_2 2); [q^7]Q^2 = -8, [q^3]Q^10 = -40, [q^7]Q^18 = -18072,
[q^3]Q^26 = -1976 (all v_2 3).

Independent sanity check (no reduction, no modular forms): B_k(4n+3) computed directly from P^k for k = 1..320 and
4n+3 <= 4003 (`direct_k320.log`): the minimum v_2 equals the conjectured value for every k, 0 mismatches.
Total compute: about 4 seconds.

## Step 5. Prior proof search (25 Nov 2026)

- arXiv: only v1 of 2611.05623; arXiv API searches for "designated summands" (newest first) and author Yaqubi: later
  papers 2611.15164 (PDO_t mod 3) and 2611.28840 (Lin's PDO_t), neither about k-tuples or Conjecture 6.2.
  Semantic Scholar citations: rate-limited (429), not read.
- Web search (two queries): nothing beyond the paper itself and older PDO work.
- Davis catalogue `source/davis-CONTENTS.md`: no match for 2611.05623, Yaqubi, Mirzavaziri, designated summands.
- 1337isnot1337/solved-conjectures: issues and code, no match.
- the-omega-institute/trureturing: issues, PRs and code. Conjecture 6.1 proved (PR #33580, merged 23 Nov 2026; issues
  #33469, #33480). Conjecture 6.3 open (#26878, #26887, #30694). For 6.2: nothing; their 6.1 problem file says
  "Source scope. Conjecture 6.2 concerns B_k, the odd-parts model", that is, out of their scope.
- demonstrandum-research/artifacts: issues and code, no match.
No prior proof of Conjecture 6.2 found.

## How this could still be wrong (residual, none found)

- Reliance on standard theorems (Newman, Ligozat, Sturm at p = 2). Each is used within its stated hypotheses above.
- A shared misreading of the definition: excluded by deriving the product from the combinatorial definition and matching
  the paper's printed series and B_k(3) formula.
- Arithmetic bugs: three separate implementations agree; my C residues match exact big integers on the first terms;
  the direct check for k <= 320 matches.
