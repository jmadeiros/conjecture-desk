"""
Referee's own modular-forms bookkeeping for B-T2 (written from scratch, exact arithmetic).

For a claim A_k(m n + r) = 0 mod 3^t, with F = f6/(f1 f2 f3) = eta(6z)/(eta(z)eta(2z)eta(3z)) (no q-shift):
  g = eta(m z)^(24c) * F^k.
Checks, all from first principles:
  * q-shift of g is exactly q^(m c): sum(delta * r_delta)/24 = m c.
  * Newman / Gordon-Hughes (Ono, Web of Modularity, Thm 1.64): delta | N for all delta, weight integer,
    sum delta r_delta = 0 mod 24, sum (N/delta) r_delta = 0 mod 24.
  * character chi(d) = ((-1)^w s / d), s = prod delta^{r_delta}; reported as the squarefree part of (-1)^w s.
  * holomorphy at every cusp: for gamma = [a b; c d] in SL2(Z), eta(delta gamma z) has leading exponent
    gcd(c,delta)^2/(24 delta) in q = e^{2 pi i z}. So g|gamma has leading q-exponent
    v(c) = sum_delta r_delta gcd(c,delta)^2 / (24 delta). Need v(c) >= 0 for every c (depends on gcd(c,N) only).
    This is checked for EVERY c = 0..N-1 (c=0 is the cusp infinity), not only for divisors.
  * Ligozat's normalised order at cusp 1/d is also printed for comparison.
  * level after U_p (p | N keeps level) and real-character extraction mod m' = m/p: N m'^2.
  * Sturm bound floor(w * [SL2(Z):Gamma0(L)] / 12); the index is computed both by formula and by
    counting points of P^1(Z/LZ) via CRT on prime powers (independent check).
"""
from fractions import Fraction as Fr
from math import gcd
import json, sys

def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def index_formula(L):
    out = Fr(L)
    for p in factor(L): out *= Fr(p + 1, p)
    assert out.denominator == 1
    return int(out)

def p1_count_prime_power(p, e):
    # count points of P^1(Z/p^e Z) by brute force: pairs (c,d) mod p^e with gcd(c,d,p)=1, divided by #units
    q = p ** e
    pairs = sum(1 for c in range(q) for d in range(q) if (c % p) or (d % p))
    units = sum(1 for u in range(q) if u % p)
    assert pairs % units == 0
    return pairs // units

def index_count(L):
    out = 1
    for p, e in factor(L).items(): out *= p1_count_prime_power(p, e)
    return out

def squarefree_part(x):
    # x a nonzero Fraction with x = +-(square) * sqfree ; return the signed squarefree kernel
    sign = -1 if x < 0 else 1
    num, den = abs(x.numerator), x.denominator
    n = num * den  # same square class as num/den
    k = 1
    for p, e in factor(n).items():
        if e % 2: k *= p
    return sign * k

def analyse(k, m, r, t, c, N=None):
    e = {1: -k, 2: -k, 3: -k, 6: k}
    e[m] = e.get(m, 0) + 24 * c
    e = {d: v for d, v in e.items() if v}
    shift = Fr(sum(d * v for d, v in e.items()), 24)
    wt = Fr(sum(e.values()), 2)
    lcm = 1
    for d in e: lcm = lcm * d // gcd(lcm, d)
    if N is None:
        N = lcm
        while sum(Fr(N, d) * v for d, v in e.items()) % 24: N += lcm
    newman = (all(N % d == 0 for d in e) and wt.denominator == 1
              and sum(d * v for d, v in e.items()) % 24 == 0
              and sum((N // d) * v for d, v in e.items()) % 24 == 0)
    vmin = min(sum(Fr(v * gcd(cc, d) ** 2, 24 * d) for d, v in e.items()) for cc in range(N))
    lig = {}
    for d in range(1, N + 1):
        if N % d == 0:
            lig[d] = Fr(N, 24 * d * gcd(d, N // d)) * sum(Fr(gcd(d, dl) ** 2 * v, dl) for dl, v in e.items())
    s = Fr(1)
    for d, v in e.items(): s *= Fr(d) ** v
    chi_kernel = squarefree_part(((-1) ** int(wt)) * s)
    p = gcd(r, m); mp = m // p; rp = r // p
    L = N * mp * mp
    idx = index_formula(L); idx2 = index_count(L)
    B = (int(wt) * idx) // 12
    # all Dirichlet characters mod mp real  <=>  exponent of (Z/mp)^* divides 2
    units = [u for u in range(1, mp + 1) if gcd(u, mp) == 1]
    real_chars = all((u * u) % mp == 1 % mp for u in units)
    return dict(k=k, m=m, r=r, t=t, c=c, eta=e, q_shift=str(shift), q_shift_ok=(shift == m * c),
                weight=str(wt), N=N, newman=newman, min_lead_exponent_all_cusps=str(vmin),
                holomorphic=(vmin >= 0), ligozat_orders={str(d): str(o) for d, o in lig.items()},
                chi_kernel=chi_kernel, chi_parity_ok=((chi_kernel < 0) == (int(wt) % 2 == 1)),
                U_p=p, p_divides_N=(N % p == 0), class_mod=mp, class_res=rp, coprime=(gcd(rp, mp) == 1),
                all_chars_mod_mprime_real=real_chars, level_after=L, index=idx, index_by_count=idx2,
                sturm_B=B, need_n_upto=p * B)

claims = [("6.3  A_6(12n+10) mod 3^5", 6, 12, 10, 5), ("6.4a A_3(12n+7) mod 3^4", 3, 12, 7, 4),
          ("6.4a A_3(12n+11) mod 3^4", 3, 12, 11, 4), ("6.4b A_4(6n+5) mod 3^3", 4, 6, 5, 3),
          ("6.4b A_7(12n+11) mod 3^3", 7, 12, 11, 3), ("6.4c A_8(18n+15) mod 3^5", 8, 18, 15, 5)]
out = []
for label, k, m, r, t in claims:
    c = 1
    while True:
        a = analyse(k, m, r, t, c)
        if a['newman'] and a['holomorphic'] and Fr(a['weight']) > 0: break
        c += 1
    a['label'] = label
    print(label, '| c =', c, '| eta exps', a['eta'], '| weight', a['weight'], '| N', a['N'],
          '| Newman', a['newman'], '| min lead exp', a['min_lead_exponent_all_cusps'],
          '| chi kernel', a['chi_kernel'], 'parity ok', a['chi_parity_ok'],
          '| U_p', a['U_p'], 'p|N', a['p_divides_N'], '| class', a['class_res'], 'mod', a['class_mod'],
          'real chars', a['all_chars_mod_mprime_real'], '| level', a['level_after'],
          '| index', a['index'], '=', a['index_by_count'], '| Sturm B', a['sturm_B'], '| need n <=', a['need_n_upto'])
    print('    Ligozat orders at cusps 1/d:', a['ligozat_orders'])
    assert a['q_shift_ok'] and a['coprime'] and a['p_divides_N'] and a['index'] == a['index_by_count']
    out.append(a)
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'bookkeeping.json', 'w'), indent=1, default=str)
