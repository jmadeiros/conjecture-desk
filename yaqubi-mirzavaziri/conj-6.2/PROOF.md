# CANDIDATE PROOF: Conjectures 6.1 and 6.2 of Yaqubi and Mirzavaziri (arXiv:2611.05623v1)

Status: CANDIDATE for Conjecture 6.2. Computer-assisted (finite Sturm-bound checks), two independently written programs.
Not reviewed by a human number theorist. Not formalised.

NOT NEW for Conjecture 6.1: a Lean proof of 6.1 was merged in the public the-omega-institute/trureturing repository on
23 Nov 2026 (PR #33580, preregistration issue #33469), by a different route (2-dissections). The 6.1 half below is an
independent reproduction by another method. No entry for Conjecture 6.2 was found there or in Davis's catalogue (searched 25 Nov 2026).

## Statements (as printed in the paper, Section 6)

F(q) = f_6/(f_1 f_2 f_3), P(q) = f_4 f_6^2/(f_1 f_3 f_12), f_m = prod_{n>=1} (1 - q^{mn}).
sum A_k(n) q^n = F^k, sum B_k(n) q^n = P^k. A_k(3) = k(k+1)(k+14)/6, B_k(3) = k(k+2)(k+7)/6.

- Conjecture 6.1. For every k>=1, the largest power of 2 dividing all A_k(4n+3) is 2^{v_2(A_k(3))} if k is not 2 mod 16,
  and exactly 2^3 if k = 2 mod 16.
- Conjecture 6.2. For every k>=1, the largest power of 2 dividing all B_k(4n+3) is 2^{v_2(B_k(3))}, except when k = 1 mod 8
  (exactly 2^2) or k = 6 mod 8 (exactly 2^3; this last case is the paper's Theorem 4.6).

Write T3(h) for the part of a power series h supported on exponents = 3 mod 4, and m(h) = min 2-adic valuation of the
coefficients of T3(h). The conjectures give the value of m(F^k) and m(P^k) for every k>=1.
The upper bound m <= v_2(coefficient of q^3) is trivial (take n=0), so in the non-exceptional classes only the lower bound needs proof.

## Step 1: reduction of "all k" to finitely many residue classes

Lemma 1. If h is in 1 + qZ[[q]] and e>=1 then h(q)^(2^e) = h(q^2)^(2^(e-1)) mod 2^e. Hence for e>=2,
h(q)^(2^e) = h(q^4)^(2^(e-2)) mod 2^(e-1). (Standard: h(q)^2 = h(q^2) mod 2, then induct using x = y mod 2^j => x^2 = y^2 mod 2^(j+1).)
The same holds for h^(2^e m) with any integer m (both sides are units).

Lemma 2. Let h be in 1 + qZ[[q]], k and m integers, e>=2, 1<=j<=e-1. Then
T3(h^(k + 2^e m)) = 0 mod 2^j if and only if T3(h^k) = 0 mod 2^j.
Proof: h^(k+2^e m) = h^k * U(q^4) mod 2^(e-1) with U a unit power series in q^4; multiplying by a series in q^4
commutes with T3 and U is invertible.

So "T3(h^k) = 0 mod 2^j" depends only on k mod 2^(j+1), and negative representatives are allowed.
Put G = 1/F = f_1 f_2 f_3/f_6 and Q = 1/P = f_1 f_3 f_12/(f_4 f_6^2).

Case analysis for A (target value t(k) = v_2(k) + v_2(k+1) + v_2(k+14) - 1):
- k = 0 mod 4, e = v_2(k): F^k is a series in q^2 mod 2^e by Lemma 1, so T3(F^k) = 0 mod 2^e, and t(k) = e + 1 - 1 = e.
- k odd, e = v_2(k+1): t(k) = e - 1. k = -1 + 2^e m, so by Lemma 2 (j = e-1) it suffices that T3(G) = 0 mod 2^(e-1) for all e,
  i.e. (A0) T3(G) = 0 identically.
- k = 6, 10, 14 mod 16: t(k) = 2, 3, 2. Representatives -10, -6, -2 mod 16, Lemma 2 with e=4:
  (A1) T3(G^10) = 0 mod 4, (A2) T3(G^6) = 0 mod 8, (A3) T3(G^2) = 0 mod 4.
- k = 2 mod 16: claim m = 3 exactly. Lower bound: representative -14, (A4) T3(G^14) = 0 mod 8.
  Exactness: Lemma 2 with e=5, j=4; k mod 32 is 2 or 18, representatives -30 and -14:
  (A5) T3(G^30) != 0 mod 16 and T3(G^14) != 0 mod 16.

Case analysis for B (t(k) = v_2(k) + v_2(k+2) + v_2(k+7) - 1):
- k = 0 mod 4: as above, t(k) = v_2(k).
- k = 3 mod 4: t(k) = 0, nothing to prove.
- k = 5 mod 8: t(k) = 1. Representative -3 mod 4, e=2: (B1) T3(Q^3) = 0 mod 2.
- k = 1 mod 8: claim exactly 2. Representative -7 mod 8, e=3: (B2) T3(Q^7) = 0 mod 4.
  Exactness, e=4, k mod 16 is 1 or 9, representatives -15, -7: (B3) T3(Q^15) != 0 mod 8 and T3(Q^7) != 0 mod 8.
- k = 2 mod 8: t(k) = 2. Representative -6: (B4) T3(Q^6) = 0 mod 4.
- k = 6 mod 8: claim exactly 3 (paper's Theorem 4.6; re-derived here). Representatives -10, -2 mod 16:
  (B5) T3(Q^10) = 0 mod 8, T3(Q^2) = 0 mod 8. Exactness, k mod 32 in {6,14,22,30}, representatives -26,-18,-10,-2:
  (B6) T3(Q^j) != 0 mod 16 for j = 2, 10, 18, 26.

## Step 2: each of (A0)-(A4), (B1), (B2), (B4), (B5) is a finite check

G^j = eta(t)^j eta(2t)^j eta(3t)^j / eta(6t)^j exactly (no q-shift). By Newman's criterion it is a weakly holomorphic
modular form of weight j on Gamma_0(N) with a quadratic character (N = 72 for j=1; 12 or 36 for the even j used), and by
Ligozat's formula its order at every cusp is >= 0, so it is in M_j(Gamma_0(N), chi).

Q^j has weight 0, with poles at some cusps. Multiply by Delta(4t)^c = q^(4c) prod (1-q^(4n))^(24c): this is q^(4c) times a
unit series in q^4, so T3(Delta(4t)^c Q^j) = Delta(4t)^c T3(Q^j) and the two vanish modulo the same powers of 2.
For suitable c (1 to 3 for the proof items) the product is a holomorphic form of weight 12c on Gamma_0(N), N | 144.

For f = sum a(n) q^n in M_w(Gamma_0(N), chi) with 4 | N: T3(f) = (1/2)(f tensor psi_0 - f tensor psi_1), psi_0 the principal
character mod 4 and psi_1 the odd character mod 4. Both twists lie in M_w(Gamma_0(16N), chi) (Ono, Web of Modularity, Prop. 2.8;
psi^2 is trivial). T3(f) has integer coefficients. Sturm's theorem (applied repeatedly after dividing by 2):
if a(n) = 0 mod 2^t for all n = 3 mod 4 with n <= B = floor(w [SL_2(Z):Gamma_0(16N)]/12), then T3(f) = 0 mod 2^t.
For (A0) the same bound with all coefficients equal to 0 gives T3(G) = 0.

Certificate table (both implementations agree on every row; logs in this folder):

| item | form | level N | weight | Sturm bound B | min v_2 for n<=B, n=3 mod 4 | needed |
|---|---|---|---|---|---|---|
| A0 | G | 72 | 1 | 192 | all coefficients 0 | 0 identically |
| A3 | G^2 | 36 | 2 | 192 | 2 | 2 |
| A2 | G^6 | 12 | 6 | 192 | 3 | 3 |
| A1 | G^10 | 36 | 10 | 960 | 2 | 2 |
| A4 | G^14 | 36 | 14 | 1344 | 3 | 3 |
| B1 | Delta(4t) Q^3 | 48 | 12 | 1536 | 1 | 1 |
| B2 | Delta(4t)^2 Q^7 | 144 | 24 | 9216 | 2 | 2 |
| B4 | Delta(4t)^2 Q^6 | 24 | 24 | 1536 | 2 | 2 |
| B5 | Delta(4t)^3 Q^10 | 72 | 36 | 6912 | 3 | 3 |
| B5 | Delta(4t) Q^2 | 72 | 12 | 2304 | 3 | 3 |

Witnesses for exactness (exact integers, coefficient of q^n in the series itself):
- A5: [q^7] G^14 = -12168 (v_2 = 3); [q^7] G^30 = 247080 (v_2 = 3).
- B3: [q^7] Q^7 = 188 (v_2 = 2); [q^3] Q^15 = -260 (v_2 = 2).
- B6: [q^7] Q^2 = -8; [q^3] Q^10 = -40; [q^7] Q^18 = -18072; [q^3] Q^26 = -1976 (all v_2 = 3).

## Verification done

1. `prove_2adic.py` (implementation 1): numpy uint64 arithmetic, series by pentagonal-number products. Log `prove_2adic_impl1.log`.
2. `prove_2adic_impl2.py` (implementation 2, written separately): exact Python integers, series by the logarithmic-derivative
   recurrence, levels/cusp orders/Sturm bounds recomputed. Log `prove_2adic_impl2.log`. Same bounds, same minima, "ALL OK".
3. `sanity2adic.py`: direct computation of F^k and P^k (no reduction, no modular forms) for 1<=k<=300 and 4n+3 < 1200:
   the observed minimum valuation equals the conjectured value for every k (0 mismatches). This is 3x the authors' k range.
4. Re-read against the paper: generating functions (Section 2 and Prop. for PDO), the q^3 coefficients (checked against the
   computed series for k<=300), the residue classes and the word "exactly" in both conjectures.

## What a referee should check

- Lemma 2 is the only new idea; it is two lines. The rest is the standard eta-quotient/Sturm routine.
- The level used after extracting the class 3 mod 4 is 16N (generous). A smaller level would only lower the bounds.
- The use of Sturm's bound modulo 2^t for forms with character in M_w(Gamma_0(16N), chi), and for weight 1 (item A0).
- Newman/Ligozat bookkeeping is done by code, not by hand (two separate codes agree).
- Conjecture 6.2's class k = 6 mod 8 is already a theorem in the paper; it is re-proved here only as a by-product.
