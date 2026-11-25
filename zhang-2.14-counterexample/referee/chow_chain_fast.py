#!/usr/bin/env python3
"""ned / S-4: H_{(a,b)}(t) for all a<=A, b<=B from the paper's chain formulas (1),(2),
evaluated with 2-D prefix sums (my own organisation; no kernel / generating function).

  R_alpha = [|alpha|-1]_t + t * sum_{empty<nu<alpha} R_nu [|alpha|-|nu|-1]_t        (2)
  H_beta  = 1 + t * sum_{empty<alpha<=beta} R_alpha                                   (1)

Below (a,b) the elements are: empty, (r) for r<=max(a,b), (i,j) for i<=a, j<=b
(verified against brute-force enumeration of the generalized subword order).
Trick: (1-t)[k]_t = 1 - t^k, so (1-t) sum_nu R_nu [m-|nu|-1] = sum R_nu - t^{-1} sum R_nu t^{m-|nu|}.
Exact integer polynomials via python-flint fmpz_poly.
"""
import sys, json
from flint import fmpz_poly

T = fmpz_poly([0, 1])
ONE = fmpz_poly([1])
ONE_MINUS_T = fmpz_poly([1, -1])


def qint(k):
    return fmpz_poly([1] * k) if k >= 1 else fmpz_poly([])


def exdiv(p, d):
    q, r = divmod(p, d)
    assert r == 0
    return q


def compute(A, B, want):
    M = max(A, B)
    # one-part compositions: R_(r) from (2) directly; nu ranges over (r') with r'<r
    R1 = [None] * (M + 1)
    for r in range(1, M + 1):
        acc = qint(r - 1)
        for rp in range(1, r):
            acc += T * R1[rp] * qint(r - rp - 1)
        R1[r] = acc
    # prefix data for one-part: P1[M'] = sum_{r<=M'} R_(r); V[M'] = sum_{r<=M'} R_(r) t^{M'-r}
    P1 = [fmpz_poly([])] * (M + 1)
    V = [fmpz_poly([])] * (M + 1)
    for r in range(1, M + 1):
        P1[r] = P1[r - 1] + R1[r]
        V[r] = T * V[r - 1] + R1[r]
    out = {}
    Sprev = [fmpz_poly([])] * (B + 1)   # S_{i-1, j}
    Uprev = [fmpz_poly([])] * (B + 1)   # U_{i-1, j}
    for i in range(1, A + 1):
        Scur = [fmpz_poly([])] * (B + 1)
        Ucur = [fmpz_poly([])] * (B + 1)
        for j in range(1, B + 1):
            m = i + j
            Mx, mn = max(i, j), min(i, j)
            # strict 2-D part
            Sstr = Sprev[j] + Scur[j - 1] - Sprev[j - 1]
            Ustr = T * Uprev[j] + T * Ucur[j - 1] - T * T * Uprev[j - 1]
            # (1-t)*two = Sstr - Ustr/t   (Ustr = sum_strict R_nu t^{m-|nu|}, divisible by t)
            two = exdiv(Sstr - exdiv(Ustr, T), ONE_MINUS_T)
            # one-part (r), r<=Mx : sum R_(r)[m-r-1] ; t^{m-r-1} part = V[Mx] t^{m-Mx-1}
            one_t = V[Mx] * T ** (mn - 1)
            one = exdiv(P1[Mx] - one_t, ONE_MINUS_T)
            R = qint(m - 1) + T * (one + two)
            Scur[j] = R + Sprev[j] + Scur[j - 1] - Sprev[j - 1]
            Ucur[j] = R + T * Uprev[j] + T * Ucur[j - 1] - T * T * Uprev[j - 1]
            if want == "all" or (i, j) in want:
                H = ONE + T * (P1[Mx] + Scur[j])
                out[(i, j)] = H
        Sprev, Uprev = Scur, Ucur
    return out, R1


def gamma_of(H, deg):
    from math import comb
    h = [int(c) for c in H.coeffs()]
    rem = h + [0] * (deg + 1 - len(h))
    g = []
    for i in range(deg // 2 + 1):
        gi = rem[i]
        g.append(gi)
        for k in range(deg - 2 * i + 1):
            rem[i + k] -= gi * comb(deg - 2 * i, k)
    assert all(v == 0 for v in rem), "not palindromic"
    while len(g) > 1 and g[-1] == 0:
        g.pop()
    return g


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "grid":
        N = int(sys.argv[2])
        out, R1 = compute(N, N, "all")
        # check (4): R_(s) = (1+t)^{s-2}, R_(1)=0
        for s in range(1, N + 1):
            assert R1[s] == ((1 + T) ** (s - 2) if s >= 2 else fmpz_poly([])), s
        res = {f"{a},{b}": gamma_of(H, a + b - 1) for (a, b), H in out.items()}
        json.dump(res, open(sys.argv[3], "w"))
        print("grid", N, "done;", len(res), "gamma polys; (4) verified")
    else:
        A, B = int(sys.argv[2]), int(sys.argv[3])
        want = {(A, B - 1), (A, B)}
        out, _ = compute(A, B, want)
        res = {f"{a},{b}": gamma_of(H, a + b - 1) for (a, b), H in out.items()}
        json.dump({k: [str(c) for c in v] for k, v in res.items()}, open(sys.argv[4], "w"))
        for k, v in res.items():
            print(k, "deg", len(v) - 1, "max coeff digits", max(len(str(abs(c))) for c in v))
