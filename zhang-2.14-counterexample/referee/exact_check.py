#!/usr/bin/env python3
"""ned / S-4: exact test of the three clauses of Conjecture 2.14 at one (a,b).

p = Gamma_{a,b-1}, g = Delta_{a,b} = Gamma_{a,b} - Gamma_{a,b-1}.
Clause 1: coefficients of g >= 0 (and g != 0).
Clause 2: g has only nonpositive real zeros.
Clause 3: p <= g (weak interlacing, orientation free when degrees are equal).

Certification is EXACT: root approximations from flint/arb are only used to
choose rational test points; every claim is then checked by exact integer sign
evaluation (homogenised Horner) at those rationals.  If a polynomial of degree d
(with the zeros at s=0 split off) shows d sign changes on (-inf,0), all its zeros
are real, simple, negative and located in the certified intervals.
"""
import json, sys
from fractions import Fraction
from flint import fmpz_poly, arb, acb, ctx


def load(path, key):
    d = json.load(open(path))
    return [int(c) for c in d[key]]


def sign_at(c, x):
    """exact sign of sum c_i x^i at rational x (Fraction)"""
    p, q = x.numerator, x.denominator
    d = len(c) - 1
    acc = 0
    for i in range(d, -1, -1):          # homogenised Horner: sum c_i p^i q^(d-i)
        acc = acc * p + c[i] * q ** (d - i)
    return (acc > 0) - (acc < 0)


def strip_zero_roots(c):
    k = 0
    while c[k] == 0:
        k += 1
    return k, c[k:]


def arb_to_fraction(x):
    # exact dyadic midpoint -> Fraction
    man, exp = x.mid().man_exp()
    man, exp = int(man), int(exp)
    return Fraction(man) * (Fraction(2) ** exp)


PREC = [3000]


def isolate(c):
    """return (sorted list of Fraction approximations of real roots, #nonreal) via arb"""
    ctx.prec = PREC[0]
    f = fmpz_poly(c)
    real, nonreal = [], 0
    for z, m in f.complex_roots():
        if z.imag == 0:
            real += [arb_to_fraction(z.real)] * m
        else:
            nonreal += m
    real.sort()
    return real, nonreal


def separators(points):
    """rationals strictly between consecutive distinct sorted points, simple denominators"""
    seps = []
    for x, y in zip(points, points[1:]):
        assert x < y
        # pick a short rational in (x,y): continued-fraction style search
        seps.append(short_between(x, y))
    return seps


def short_between(x, y):
    """simplest-ish rational strictly between x<y (Stern-Brocot on the gap)"""
    lo, hi = x, y
    # move to positive by symmetry for simplicity
    if hi <= 0:
        r = short_between(-hi, -lo)
        return -r
    if lo < 0 < hi:
        return Fraction(0)
    # Stern-Brocot
    a, b, c, d = 0, 1, 1, 0  # a/b < target interval < c/d
    while True:
        m = Fraction(a + c, b + d)
        if m <= lo:
            a, b = a + c, b + d
            # accelerate
            k = 1
            while Fraction(a + k * c, b + k * d) <= lo:
                k *= 2
            # binary search largest j < k with (a+j c)/(b+j d) <= lo
            lo_j, hi_j = 0, k
            while hi_j - lo_j > 1:
                mid = (lo_j + hi_j) // 2
                if Fraction(a + mid * c, b + mid * d) <= lo:
                    lo_j = mid
                else:
                    hi_j = mid
            a, b = a + lo_j * c, b + lo_j * d
        elif m >= hi:
            c, d = a + c, b + d
            k = 1
            while Fraction(c + k * a, d + k * b) >= hi:
                k *= 2
            lo_j, hi_j = 0, k
            while hi_j - lo_j > 1:
                mid = (lo_j + hi_j) // 2
                if Fraction(c + mid * a, d + mid * b) >= hi:
                    lo_j = mid
                else:
                    hi_j = mid
            c, d = c + lo_j * a, d + lo_j * b
        else:
            return m


def wronskian_at(p, g, x):
    def ev(c, x):
        return sum(Fraction(ci) * x ** i for i, ci in enumerate(c))
    dp = [i * p[i] for i in range(1, len(p))] or [0]
    dg = [i * g[i] for i in range(1, len(g))] or [0]
    return ev(p, x) * ev(dg, x) - ev(dp, x) * ev(g, x)


def analyse(p, G, verbose=True):
    g = [ (G[i] if i < len(G) else 0) - (p[i] if i < len(p) else 0) for i in range(max(len(G), len(p)))]
    while len(g) > 1 and g[-1] == 0:
        g.pop()
    rep = {"deg_p": len(p) - 1, "deg_g": len(g) - 1}
    rep["g_nonzero"] = any(g)
    rep["clause1_nonneg_coeffs"] = all(x >= 0 for x in g)
    rep["min_coeff_g"] = min(g)
    kz, h = strip_zero_roots(g)
    rep["g_zero_mult_at_0"] = kz
    assert p[0] > 0
    # approximate real roots
    rp, nrp = isolate(p)
    rh, nrh = isolate(h) if len(h) > 1 else ([], 0)
    rep["p_nonreal_roots(arb)"] = nrp
    rep["g_nonreal_roots(arb)"] = nrh
    # exact certification of real-rootedness by sign changes
    merged = sorted([(x, 'p') for x in rp] + [(x, 'g') for x in rh])
    pts = [x for x, _ in merged]
    distinct = all(x < y for x, y in zip(pts, pts[1:]))
    rep["merged_roots_distinct"] = distinct
    if not distinct:
        rep["note"] = "coincident root approximations; need gcd handling"
        return rep, g, None, None, None, None, h
    seps = separators(pts)
    left = pts[0] * 2 - 1 if pts else Fraction(-1)
    test = [left] + seps + [Fraction(0)]   # all roots negative? last root < 0 checked below
    assert all(x < 0 for x in pts), "nonnegative root approx"
    # at s=0: p(0)>0, h(0)>0; use a point slightly left of 0 only if needed: s=0 is fine for p and h
    sp = [sign_at(p, x) for x in test]
    sh = [sign_at(h, x) for x in test]
    assert all(v != 0 for v in sp + sh), "test point hit a root exactly"
    chp = sum(1 for u, v in zip(sp, sp[1:]) if u != v)
    chh = sum(1 for u, v in zip(sh, sh[1:]) if u != v)
    rep["p_sign_changes_exact"] = chp
    rep["h_sign_changes_exact"] = chh
    rep["p_real_rooted_certified"] = (chp == len(p) - 1)
    rep["g_real_rooted_certified"] = (chh == len(h) - 1)
    # certified merged order: each test interval must hold exactly one sign change in total
    order = []
    ok_order = True
    for k in range(len(test) - 1):
        cp = sp[k] != sp[k + 1]
        ch = sh[k] != sh[k + 1]
        if cp and ch:
            ok_order = False
        order.append('p' if cp else ('g' if ch else '-'))
    if not pts:          # no negative roots at all: single root-free interval
        order = [] if order == ['-'] else order
    rep["merged_order_certified"] = ok_order and '-' not in order
    # add the zeros of g at s = 0 (to the right of every negative root)
    word = ''.join(order) + 'g' * kz
    rep["root_word_left_to_right"] = word
    # weak interlacing (generous): alternation of the merged word, either orientation
    alternating = all(word[i] != word[i + 1] for i in range(len(word) - 1))
    rep["clause3_strictly_alternating"] = alternating
    bad = [i for i in range(len(word) - 1) if word[i] == word[i + 1]]
    rep["violations_at_word_positions"] = bad[:20]
    rep["num_violations"] = len(bad)
    if bad:
        i = bad[0]
        rep["first_violation_interval"] = [str(test[i]), str(test[i + 2])] if i + 2 < len(test) else [str(test[i]), "0"]
    return rep, g, test, order, sp, sh, h


if __name__ == "__main__":
    path, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    d = json.load(open(path))
    p = [int(c) for c in d[f"{a},{b-1}"]]
    G = [int(c) for c in d[f"{a},{b}"]]
    out = analyse(p, G)
    rep = out[0]
    g = out[1]
    for x in [Fraction(0), Fraction(-5, 101)]:
        w = wronskian_at(p, g, x)
        rep[f"W({x})"] = float(w)
        rep[f"W({x})_exact_floor"] = str(w.numerator // w.denominator)
    print(json.dumps(rep, indent=1))
