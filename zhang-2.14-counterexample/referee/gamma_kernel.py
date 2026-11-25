#!/usr/bin/env python3
"""ned / S-4: Gamma_{a,b}(s) for the whole grid from the paper's Corollary 2.6 rational kernel,
expanded by its own denominator recurrence (G * D = Num coefficientwise).  Used for the scan;
validated against chow_chain_fast.py (chain formula) and chow_bruteforce.py (definition).

  G = XY(1-XY) N / [ (1-X)(1-Y)(1-XY+sX^2Y^2)(1-X-Y+(1-s)XY) ]
  N = 1-(1-s)(X+Y)+(1-3s)XY+sXY(X+Y)-s(1-s)X^2Y^2
"""
from flint import fmpz_poly

S = fmpz_poly([0, 1])
ONE = fmpz_poly([1])


def bmul(A, B):
    C = {}
    for (i, j), u in A.items():
        for (k, l), v in B.items():
            C[(i + k, j + l)] = C.get((i + k, j + l), fmpz_poly([])) + u * v
    return {k: v for k, v in C.items() if v != 0}


def kernel():
    N = {(0, 0): ONE, (1, 0): -(1 - S), (0, 1): -(1 - S), (1, 1): 1 - 3 * S,
         (2, 1): S, (1, 2): S, (2, 2): -S * (1 - S)}
    Num = bmul({(1, 1): ONE, (2, 2): -ONE}, N)
    D = {(0, 0): ONE}
    for f in ({(0, 0): ONE, (1, 0): -ONE},
              {(0, 0): ONE, (0, 1): -ONE},
              {(0, 0): ONE, (1, 1): -ONE, (2, 2): S},
              {(0, 0): ONE, (1, 0): -ONE, (0, 1): -ONE, (1, 1): 1 - S}):
        D = bmul(D, f)
    assert D[(0, 0)] == ONE
    return Num, D


def rows(N, M=None):
    """yield (a, row) with row[b] = Gamma_{a,b} for b = 0..M (row[0] = Gamma_{a,0} := 1)."""
    M = M or N
    Num, D = kernel()
    Dl = [(k, v) for k, v in D.items() if k != (0, 0)]
    maxi = max(i for i, _ in D)
    window = {}  # a -> list of polys over b (true G coefficients, G_{a,0}=0 in the series)
    for a in range(0, N + 1):
        row = [fmpz_poly([])] * (M + 1)
        for b in range(0, M + 1):
            acc = Num.get((a, b), fmpz_poly([]))
            for (i, j), v in Dl:
                if a - i >= 0 and b - j >= 0:
                    acc -= v * (row[b - j] if i == 0 else window[a - i][b - j])
            row[b] = acc
        window[a] = row
        window.pop(a - maxi - 1, None)
        if a >= 1:
            out = list(row)
            out[0] = ONE  # paper's boundary convention Gamma_{a,0} = 1
            yield a, out


if __name__ == "__main__":
    import json, sys
    cf = json.load(open(sys.argv[1]))
    n = 0
    for a, row in rows(40):
        for b in range(1, 41):
            assert [int(c) for c in row[b].coeffs()] == cf[f"{a},{b}"], (a, b)
            n += 1
    print("kernel == chain formula on", n, "pairs (a,b<=40)")
    big = json.load(open(sys.argv[2]))
    for a, row in rows(165):
        if a == 165:
            for b in (164, 165):
                assert [int(c) for c in row[b].coeffs()] == [int(c) for c in big[f"165,{b}"]], b
    print("kernel == chain formula at (165,164) and (165,165)")
