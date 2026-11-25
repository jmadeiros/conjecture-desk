#!/usr/bin/env python3
"""checker-1, card B-T1: independent re-check of the Sturm-bound proof of Conjecture 6.2 (arXiv:2611.05623v1).

Everything here is recomputed from the definitions with exact arithmetic (Fractions / Python ints / Z mod 2^64 in C).
  1. modular bookkeeping for each eta quotient: weight, order at infinity, smallest Newman level N, character,
     Ligozat order at every cusp of Gamma_0(N), Sturm bound for Gamma_0(16N) (level after the mod-4 twists);
  2. the coefficient check up to the Sturm bound (C program eta2, mod 2^64), both for f = Delta(4t)^c Q^j and for Q^j;
  3. exact big-integer witnesses for exactness;
  4. a cross-check that the C residues agree with exact big-integer expansions.
"""
import subprocess, sys, os
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
ETA = os.path.join(HERE, "eta2")

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def mu0(N):  # [SL2(Z) : Gamma_0(N)]
    m, n, p = N, N, 2
    res = Fraction(N)
    while p * p <= n:
        if n % p == 0:
            res *= Fraction(p + 1, p)
            while n % p == 0: n //= p
        p += 1
    if n > 1: res *= Fraction(n + 1, n)
    assert res.denominator == 1
    return int(res)

def kron(a, d):
    """Kronecker symbol (a/d) for odd d > 0 (Jacobi symbol), a any integer."""
    assert d > 0 and d % 2 == 1
    a %= d; res = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if d % 8 in (3, 5): res = -res
        a, d = d, a
        if a % 4 == 3 and d % 4 == 3: res = -res
        a %= d
    return res if d == 1 else 0

def bookkeeping(r):
    """r: dict delta -> exponent. Returns dict of facts, all exact."""
    k2 = sum(r.values()); assert k2 % 2 == 0, "non-integral weight"; k = k2 // 2
    s24 = sum(d * e for d, e in r.items()); assert s24 % 24 == 0, "not an integer q-power"
    shift = s24 // 24
    L = 1
    for d in r: L = L * d // gcd(L, d)
    N = None
    for M in range(L, 100000, L):
        if sum(Fraction(M, d) * e for d, e in r.items()) % 24 == 0:
            N = M; break
    # character chi(d) = ((-1)^k s / d), s = prod delta^r ; test on odd d coprime to N up to 4N
    s = Fraction(1)
    for d, e in r.items(): s *= Fraction(d) ** e
    num = s.numerator * s.denominator  # same square class as s
    sgn = (-1) ** k
    chi_vals = {}
    for dd in range(1, 4 * N, 2):
        if gcd(dd, N) == 1: chi_vals[dd] = kron(sgn * num, dd)
    trivial = all(v == 1 for v in chi_vals.values())
    # Ligozat orders at cusps c/d, d | N
    orders = {}
    for d in divisors(N):
        o = Fraction(N, 24) * sum(Fraction(gcd(d, de) ** 2 * e, gcd(d, N // d) * d * de) for de, e in r.items())
        orders[d] = o
    holo = all(o >= 0 for o in orders.values())
    mu16 = mu0(16 * N)
    sturm = (k * mu16) // 12
    return dict(weight=k, shift=shift, N=N, char_trivial=trivial, char_sq_class=num, holomorphic=holo,
                min_cusp_order=min(orders.values()), worst_cusp=min(orders, key=orders.get), mu16N=mu16, sturm=sturm,
                orders=orders)

def run_eta(L, shift, need, r):
    args = [ETA, "eta", str(L), str(shift), str(need)]
    for d, e in sorted(r.items()):
        if e: args += [str(d), str(e)]
    out = subprocess.run(["nice", "-n", "10"] + args, capture_output=True, text=True, check=True).stdout
    return out.strip()

# ---------- exact big-integer series (for witnesses and for cross-checking the C residues) ----------
def eta_series_exact(r, L):
    F = [0] * (L + 1); F[0] = 1
    for d, e in r.items():
        for m in range(1, L // d + 1):
            st = d * m
            if e > 0:
                for _ in range(e):
                    for n in range(L, st - 1, -1): F[n] -= F[n - st]
            else:
                for _ in range(-e):
                    for n in range(st, L + 1): F[n] += F[n - st]
    return F

def main():
    log = []
    def P(*a):
        line = " ".join(str(x) for x in a); print(line, flush=True); log.append(line)

    # ---- definitions (paper, Def. after Sec. 2): G_paper = f4 f6^2/(f1 f3 f12) = sum PDO(n) q^n ; B_k = [q^n] G_paper^k
    Pdef = {4: 1, 6: 2, 1: -1, 3: -1, 12: -1}
    Qdef = {d: -e for d, e in Pdef.items()}  # Q = 1/P
    Pser = eta_series_exact(Pdef, 12)
    P("P = f4 f6^2/(f1 f3 f12) begins", Pser[:8], "(paper prints 1+q+2q^2+4q^3+5q^4)")
    # B_k(3) formula check, k <= 60, exact
    def power(S, k, L):
        R = [1] + [0] * L
        for _ in range(k):
            R = [sum(R[i] * S[n - i] for i in range(n + 1)) for n in range(L + 1)]
        return R
    ok = all(power(Pser, k, 3)[3] == k * (k + 2) * (k + 7) // 6 for k in range(1, 61))
    P("B_k(3) = k(k+2)(k+7)/6 for k=1..60:", ok)

    # ---- items of the proof for Conjecture 6.2 (j, c, needed min v2) ----
    items = [("B1", 3, 1, 1), ("B2", 7, 2, 2), ("B4", 6, 2, 2), ("B5a", 10, 3, 3), ("B5b", 2, 1, 3)]
    claimed = {"B1": (48, 12, 1536), "B2": (144, 24, 9216), "B4": (24, 24, 1536), "B5a": (72, 36, 6912), "B5b": (72, 12, 2304)}
    allok = True
    for name, j, c, need in items:
        r = {1: j, 3: j, 4: 24 * c - j, 6: -2 * j, 12: j}  # Delta(4t)^c * Q^j
        b = bookkeeping(r)
        P(f"\n[{name}] f = Delta(4t)^{c} Q^{j}: eta exponents {r}")
        P(f"  weight {b['weight']}, order at infinity {b['shift']} (expect 4c={4*c}), Newman level N={b['N']}, "
          f"character trivial={b['char_trivial']} (s square class {b['char_sq_class']})")
        P(f"  Ligozat: holomorphic at all {len(b['orders'])} cusps = {b['holomorphic']}; smallest cusp order {b['min_cusp_order']} at d={b['worst_cusp']}")
        P(f"  mu(16N) = {b['mu16N']}, Sturm bound floor(w*mu/12) = {b['sturm']};  write-up claims (N,w,B) = {claimed[name]}")
        same = (b['N'], b['weight'], b['sturm']) == claimed[name]
        # smallest c that makes Delta(4t)^c Q^j holomorphic (my own derivation: c >= j/4)
        cmin = next(cc for cc in range(0, 10) if bookkeeping({1: j, 3: j, 4: 24 * cc - j, 6: -2 * j, 12: j})['holomorphic'])
        P(f"  smallest holomorphic c = {cmin}; agrees with write-up table: {same}")
        assert b['shift'] == 4 * c and b['holomorphic']
        out1 = run_eta(b['sturm'], 4 * c, need, r)
        P("  f coefficients, n<=B, n=3 mod 4:", out1)
        rq = {1: j, 3: j, 4: -j, 6: -2 * j, 12: j}
        out2 = run_eta(b['sturm'], 0, need, rq)
        P("  Q^j coefficients, n<=B, n=3 mod 4:", out2)
        good = ("below_need=0 " in out1) and ("below_need=0 " in out2)
        # exact cross-check of the first residues
        ex = eta_series_exact(rq, 11)
        res = [int(x) for x in out2.split(":")[-1].split()]
        P("  C residues match exact big-int Q^j for n<=11:", [x % 2**64 for x in ex] == res)
        good = good and [x % 2**64 for x in ex] == res
        P(f"  RESULT {name}: {'PASS' if good else 'FAIL'}")
        allok &= good

    # ---- exactness witnesses (exact integers) ----
    P("\nExactness witnesses, exact big integers:")
    Q40 = eta_series_exact(Qdef, 40)
    def v2(x):
        if x == 0: return None
        v = 0
        while x % 2 == 0: x //= 2; v += 1
        return v
    wit = [("B3", 7, 7, 188), ("B3", 15, 3, -260), ("B6", 2, 7, -8), ("B6", 10, 3, -40), ("B6", 18, 7, -18072), ("B6", 26, 3, -1976)]
    for name, j, n, claim in wit:
        Qj = power(Q40, j, 11)
        val = Qj[n]
        P(f"  {name}: [q^{n}] Q^{j} = {val} (claimed {claim}), v2 = {v2(val)}")
        allok &= (val == claim)
    # smallest witnesses per class, my own scan (n = 3 mod 4, n <= 40)
    for name, j, bound in [("B3", 7, 3), ("B3", 15, 3), ("B6", 2, 4), ("B6", 10, 4), ("B6", 18, 4), ("B6", 26, 4)]:
        Qj = power(Q40, j, 39)
        hits = [(n, Qj[n]) for n in range(3, 40, 4) if v2(Qj[n]) is not None and v2(Qj[n]) < bound]
        P(f"  scan Q^{j}: n=3 mod 4, n<40 with v2 < {bound}: {hits[:3]}")
    P("\nALL B-ITEMS", "PASS" if allok else "FAIL")
    open(os.path.join(HERE, "referee.log"), "w").write("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
