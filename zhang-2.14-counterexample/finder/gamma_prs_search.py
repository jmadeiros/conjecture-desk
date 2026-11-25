"""Exact integer PRS audit for Zhang, arXiv:2610.33037, Conjecture 2.14.

All polynomial arrays are in ascending coefficient order. Positive-leading
negative-remainder chains certify strict interlacing by Sturm's theorem.
No floating-point arithmetic is used for any mathematical comparison.
"""
import argparse
import json
import math
import time
from pathlib import Path


def trim(p):
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def add(*terms):
    out = [0] * max(map(len, terms))
    for p in terms:
        for k, x in enumerate(p):
            out[k] += x
    return trim(out)


def sub(p, q):
    return add(p, [-x for x in q])


def primitive(p):
    p = trim(p)
    d = math.gcd(*p)
    return [x // d for x in p] if d > 1 else p


def neg_remainder(p, q):
    """Negative rational remainder, scaled by a positive rational.

    q has positive leading coefficient. Each integer pseudo-division step
    scales by that positive coefficient; content removal is positive too.
    """
    p = p.copy()
    while len(p) >= len(q) and p != [0]:
        k, c, lead = len(p) - len(q), p[-1], q[-1]
        p = [lead * x for x in p]
        for j, x in enumerate(q):
            p[k+j] -= c*x
        p = primitive(p)
    return [-x for x in p]


def strict_interlacing(g, p):
    """Sufficient exact certificate for p interlacing g, whose last root is 0.

    If all nonzero members of the signed Euclidean chain g,p,-rem,... have
    positive leading coefficient and degrees drop by one (except the first
    equal-degree pair), Sturm variation forces all roots of g real and one
    root of p between every consecutive pair. Squarefree/coprime cases only;
    failures are candidates requiring an independent exact check.
    """
    if g[-1] <= 0 or p[-1] <= 0:
        return False, "leading coefficient"
    if len(g) - len(p) not in (0, 1):
        return False, "degree difference"
    a, b = primitive(g), primitive(p)
    while len(b) > 1:
        c = neg_remainder(a, b)
        if c == [0]:
            return False, "common factor"
        if len(c) != len(b)-1:
            return False, "degree drop"
        if c[-1] <= 0:
            return False, "negative leading remainder"
        a, b = b, c
    return b[0] > 0, "positive Sturm chain"


def table(N):
    f = [[1], [1]]
    for j in range(2, N+1):
        f.append(sub(f[-1], [0]+f[-2]))
    G = [[[1] for b in range(N+1)] for a in range(N+1)]
    for a in range(1, N+1):
        for b in range(1, N+1):
            if min(a,b) == 1:
                G[a][b] = trim([1, max(a,b)-1])
            else:
                z = G[a-1][b-1]
                G[a][b] = add(G[a-1][b], G[a][b-1], [0]+z,
                              [-x for x in z])
                if a == b:
                    G[a][b] = sub(G[a][b], [0]+f[a-1])
    return G


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=100)
    ap.add_argument('--seconds', type=int, default=420)
    ap.add_argument('--band', type=int, default=3)
    args = ap.parse_args()
    start = time.monotonic()
    G = table(args.limit)
    checks = []
    pairs = [(a,b) for a in range(1,args.limit+1)
             for b in range(1,args.limit+1)
             if (a,b)!=(1,1) and (abs(a-b)<=args.band or min(a,b)<=4)]
    pairs.sort(key=lambda x:(max(x), abs(x[0]-x[1]),x))
    for a,b in pairs:
        p = G[a][b-1]
        g = sub(G[a][b], p)
        nonnegative = all(x>=0 for x in g)
        ok, why = strict_interlacing(g,p) if nonnegative else (False,'negative coefficient')
        checks.append([a,b,ok])
        if not ok:
            result={'candidate':[a,b], 'reason':why, 'gamma_previous':p,
                    'delta':g, 'checks':len(checks)}
            Path('gamma_prs_candidate.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(result),flush=True)
            break
        if a==b and a%5==0:
            print('completed diagonal',a,'checks',len(checks),flush=True)
        if time.monotonic()-start > args.seconds:
            print('time limit',len(checks),flush=True)
            break
    Path('gamma_prs_results.json').write_text(json.dumps({'limit':args.limit,
        'band':args.band,'checks':checks,'elapsed_seconds':time.monotonic()-start},indent=2)+'\n')
    print('done',len(checks),'elapsed',time.monotonic()-start,flush=True)


if __name__=='__main__':
    main()
