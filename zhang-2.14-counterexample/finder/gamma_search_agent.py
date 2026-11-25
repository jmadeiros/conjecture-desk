"""Exact recurrence and joint root-isolation audit of arXiv:2610.33037 C2.14.

Equations (31),(32) construct Gamma; SymPy isolates roots using rationals.
No approximate root calculations or floating-point decisions are used.
"""
from __future__ import annotations
import argparse
import json
import time
import sympy as sp

s = sp.Symbol('s')


def trim(a):
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a


def add(*terms):
    out = [0] * max(map(len, terms))
    for term in terms:
        for j, value in enumerate(term):
            out[j] += value
    return trim(out)


def neg(a):
    return [-v for v in a]


def shift(a):
    return [0] + a


def table(n):
    f = [[1], [1]]
    for k in range(2, n):
        f.append(add(f[-1], neg(shift(f[-2]))))
    g = [[[1] for b in range(n + 1)] for a in range(n + 1)]
    for a in range(1, n + 1):
        g[a][1] = trim([1, a - 1])
        g[1][a] = trim([1, a - 1])
    for a in range(2, n + 1):
        for b in range(2, n + 1):
            g[a][b] = add(g[a-1][b], g[a][b-1],
                          shift(g[a-1][b-1]), neg(g[a-1][b-1]))
            if a == b:
                g[a][b] = add(g[a][b], neg(shift(f[a-1])))
    return g


def polynomial(coefficients):
    return sp.Poly.from_list(list(reversed(coefficients)), s, domain=sp.ZZ)


def check(g, a, b):
    p = g[a][b-1]
    q = add(g[a][b], neg(p))
    record = {'a': a, 'b': b, 'Gamma_previous': p, 'Delta': q}
    if min(q) < 0:
        return dict(record, failure='negative coefficient')
    if q == [0]:
        return None if (a,b)==(1,1) else dict(record, failure='zero Delta')
    pp, qq = polynomial(p), polynomial(q)
    roots = sp.intervals([pp.as_expr(), qq.as_expr()])
    totals = [sum(mult.get(j, 0) for _, mult in roots) for j in (0, 1)]
    degrees = [pp.degree(), qq.degree()]
    if totals != degrees:
        return dict(record, failure='nonreal roots', real_root_counts=totals,
                    degrees=degrees)
    if any(hi > 0 and hi != lo for (lo, hi), _ in roots):
        # Nonnegative coefficients already exclude positive roots; this
        # branch only refines an interval which straddles zero.
        roots = sp.intervals([pp.as_expr(), qq.as_expr()], eps=sp.Rational(1,10**12))
    # Weak proper-position relation. Alternating order is p,q,p,q,...
    # if equal degree, and q,p,q,p,... if q has one extra root. The largest
    # root is q's prescribed zero. At a common root, either ordering is OK.
    if degrees[1] not in (degrees[0], degrees[0]+1):
        return dict(record, failure='incompatible degrees', degrees=degrees)
    expected = 1 if degrees[1] == degrees[0]+1 else 0
    for interval, mult in roots:
        counts = [mult.get(0,0), mult.get(1,0)]
        while counts[0] or counts[1]:
            if not counts[expected]:
                return dict(record, failure='interlacing order',
                            offending_interval=[str(v) for v in interval],
                            root_records=[[[str(v) for v in iv], d] for iv,d in roots])
            counts[expected] -= 1
            expected = 1-expected
    return None


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--size',type=int,default=70)
    parser.add_argument('--seconds',type=int,default=420)
    parser.add_argument('--output',default='gamma_agent_results.json')
    args=parser.parse_args()
    start=time.monotonic()
    g=table(args.size)
    # Basic published coefficient checks independent of root computations.
    assert g[2][2]==[1,2]
    assert g[3][4]==[1,9,11,1]
    assert g[4][4]==[1,12,25,7]
    assert all(g[a][b]==g[b][a] for a in range(1,args.size+1) for b in range(1,args.size+1))
    pairs=[]
    for n in range(17,args.size+1):
        for offset in (0,1,-1,2,-2,3,-3,5,-5,10,-10):
            b=n+offset
            if 1<=b<=args.size:
                pairs.append((n,b))
    pairs += [(a,b) for a in range(1,args.size+1)
              for b in range(1,args.size+1) if a>16 or b>16]
    seen=set()
    results={'method':'Equations31/32 integer recurrence and joint rational root isolation',
             'tested':[], 'failure':None}
    for a,b in pairs:
        if (a,b) in seen:
            continue
        if time.monotonic()-start>args.seconds:
            break
        seen.add((a,b))
        failure=check(g,a,b)
        results['tested'].append([a,b])
        if len(seen)%10==0 or failure:
            print(f'{len(seen)} pairs, latest=({a},{b}), elapsed={time.monotonic()-start:.2f}s',flush=True)
        if failure:
            results['failure']=failure
            print(json.dumps(failure),flush=True)
            break
        with open(args.output,'w') as stream:
            json.dump(results,stream,indent=2)
    with open(args.output,'w') as stream:
        json.dump(results,stream,indent=2)
    print(json.dumps({'checked':len(seen),'failure':results['failure'],
                      'elapsed':time.monotonic()-start}),flush=True)


if __name__=='__main__':
    main()
