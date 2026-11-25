# CANDIDATE PROOF: Conjectures 6.3 and 6.4 of Yaqubi and Mirzavaziri (arXiv:2611.05623v1)

Status: CANDIDATE. Computer-assisted (finite Sturm-bound checks), two independently written programs agree.
Not reviewed by a human. Not formalised. Conjecture 6.3 is listed as open and unresolved in the public
the-omega-institute/trureturing catalogue (issues #26878, #26887, #30694, read 25 Nov 2026); 6.4 has no entry there.

## Statements (Section 6 of the paper)
sum A_k(n) q^n = F^k, F = f_6/(f_1 f_2 f_3) = eta(6t)/(eta(t) eta(2t) eta(3t)).
- 6.3: for all n>=0, A_6(12n+10) = 0 mod 3^5, and 3^5 is the exact power of 3 dividing all of them.
- 6.4: (a) A_3(12n+7) = A_3(12n+11) = 0 mod 3^4. (b) A_4(6n+5) = 0 mod 3^3 and A_7(12n+11) = 0 mod 3^3. (c) A_8(18n+15) = 0 mod 3^5.

## Argument
For a claim A_k(mn+r) = 0 mod 3^t put g = Delta(m t)^c F^k, with Delta(m t) = q^m prod (1-q^{mn})^24.
Delta(m t)^c is q^{mc} times a unit power series in q^m, so the part of g on exponents r mod m equals Delta(m t)^c times the
part of F^k on exponents r mod m; one vanishes mod 3^t iff the other does.
For the least c in the table, g satisfies Newman's conditions on Gamma_0(N) and has non-negative order at every cusp (Ligozat),
so g is in M_w(Gamma_0(N), chi), w = 12c - k, integer coefficients.
If p = gcd(r,m) > 1 then p | N and U_p keeps g in the same space. The class r/p mod m' (m' = m/p, which is 6 or 12) is extracted
with the Dirichlet characters mod m', all real, so the result lies in M_w(Gamma_0(N m'^2), chi) (Ono, Web of Modularity, Prop. 2.8).
Sturm: if its coefficients vanish mod 3^t up to B = floor(w * index(Gamma_0(N m'^2))/12), it vanishes mod 3^t.
In terms of F^k this needs A_k(n) = 0 mod 3^t for n = r mod m, n <= p*B.

| claim | c | level N | weight | Sturm bound B | checked n up to | terms | min v_3 found |
|---|---|---|---|---|---|---|---|
| 6.3 A_6(12n+10), 3^5 | 5 | 12 | 54 | 3888 | 7776 | 648 | 5 |
| 6.4a A_3(12n+7), 3^4 | 3 | 24 | 33 | 19008 | 19008 | 1584 | 4 |
| 6.4a A_3(12n+11), 3^4 | 3 | 24 | 33 | 19008 | 19008 | 1584 | 4 |
| 6.4b A_4(6n+5), 3^3 | 2 | 18 | 20 | 2160 | 2160 | 360 | 3 |
| 6.4b A_7(12n+11), 3^3 | 6 | 72 | 65 | 112320 | 112320 | 9360 | 3 |
| 6.4c A_8(18n+15), 3^5 | 10 | 18 | 112 | 12096 | 36288 | 2016 | 5 |

Exactness in 6.3: v_3(A_6(22)) = 5 (A_6(22) = 6635911068; this witness is already recorded by others).
Beyond the bounds, implementation 1 checked all six progressions for every n <= 10^6 (83,333 to 166,666 terms each): no failure.

## Verification
1. `pdk.c` (C, pentagonal-number multiplication and division, mod 3^7) with `plan_3adic.py` (bookkeeping). Logs `run_3adic_1e6.log`, `plan_3adic.json`.
2. `prove_3adic_impl2.py`: series built factor by factor in numpy, powers by convolution, bookkeeping recomputed by separate code.
   Coefficients agree with pdk.c at all 112,401 indices for k = 3, 4, 6, 7, 8; same levels, weights and bounds; "ALL OK". Log `prove_3adic_impl2.log`.
3. Definitions re-read against the paper (generating function, progressions, moduli, the "exact power" clause).

## What a referee should check
- The twist/level statement used for extracting a residue class (level N m'^2), and U_p for p | N.
- Sturm's bound for odd weight with character (rows 2, 3, 5).
- Newman/Ligozat conditions were evaluated by code. Both codes give the same c, N, w.
- The two programs share the mathematical plan; they are independent only as implementations.
