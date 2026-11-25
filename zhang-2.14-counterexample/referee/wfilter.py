#!/usr/bin/env python3
"""ned / S-4: fast landscape FILTER (not a pass certificate).
For each (a,b): p = Gamma_{a,b-1}, g = Delta_{a,b}, W = p g' - p' g (exact integer poly).
If p, g are real-rooted and weakly interlace, W has one weak sign on R.  An exact sign change
of W at two rational points therefore certifies FAILURE of clause 3 (or of real-rootedness).
Same test for the weaker Chow-level pair (p, q = Gamma_{a,b}).
usage: wfilter.py N OUT.json [npts] [a0 a1]
"""
import sys, json
from flint import fmpz_poly, fmpq
from gamma_kernel import rows

N = int(sys.argv[1]); out = sys.argv[2]; npts = int(sys.argv[3]) if len(sys.argv) > 3 else 400
A0, A1 = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (1, N)
# log-spaced negative rationals from -10^-4 to -10^4, plus 0
pts = [fmpq(0)]
for k in range(npts + 1):
    e = -4 + 8 * k / npts
    x = 10 ** e
    pts.append(-fmpq(int(round(x * 10**6)) or 1, 10**6))


def signs(W):
    s = []
    for x in pts:
        v = W(x)
        s.append((v > 0) - (v < 0))
    return s


res = {"fail_delta": [], "fail_gamma": []}
for a, row in rows(A1, N):
    if a < A0:
        continue
    for b in range(1, N + 1):
        if (a, b) == (1, 1):
            continue
        p, q = row[b - 1], row[b]
        g = q - p
        for key, h in (("fail_delta", g), ("fail_gamma", q)):
            W = p * h.derivative() - p.derivative() * h
            sg = [v for v in signs(W) if v != 0]
            if sg and (min(sg) < 0 < max(sg)):
                res[key].append([a, b])
json.dump(res, open(out, "w"))
for k in res:
    L = sorted(res[k], key=lambda t: (t[0] + t[1], t[0]))
    print(k, len(L), "smallest by a+b:", L[:10])
