"""Independent exact necessary-condition audit for Zhang Conjecture 2.14.

Diagonal polynomials come directly from the diagonal generating function (37),
not the two-dimensional recurrence used by gamma_search_agent.py.
The signed Taylor coefficients of Delta/Gamma_previous must be Stieltjes
moments if the conjectured negative-root interlacing holds.
"""
import argparse
from math import comb
import json
import time


def combine(*terms):
    out = [0] * max(len(t) for t in terms)
    for t in terms:
        for k, c in enumerate(t):
            out[k] += c
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def neg(t):
    return [-x for x in t]


def shift(t):
    return [0] + t


def determinant(a):
    a = [row[:] for row in a]
    n = len(a)
    prev = 1
    sign = 1
    for k in range(n-1):
        if a[k][k] == 0:
            i = next((i for i in range(k+1,n) if a[i][k]), None)
            if i is None:
                return 0
            a[k],a[i]=a[i],a[k]
            sign=-sign
        pivot = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num = a[i][j]*pivot-a[i][k]*a[k][j]
                assert num % prev == 0
                a[i][j]=num//prev
        for i in range(k+1,n):
            a[i][k]=0
        prev=pivot
    return sign*a[-1][-1]


def moments(p,q,count):
    assert p[0]==1 and q[0]==0
    h=[0]*(count+1)
    for k in range(1,count+1):
        h[k]=(q[k] if k<len(q) else 0)-sum(p[j]*h[k-j] for j in range(1,min(k+1,len(p))))
    return [(-1)**k*h[k+1] for k in range(count)]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--size',type=int,default=400)
    parser.add_argument('--order',type=int,default=10)
    parser.add_argument('--seconds',type=int,default=420)
    parser.add_argument('--reverse',action='store_true')
    parser.add_argument('--output',default='gamma_moment_results.json')
    args=parser.parse_args()
    start=time.monotonic()
    gm2,gm1=[1],[1]
    dm2,dm1=[1],[1,1]
    fm2,fm1=[1],[1]
    result={'method':'diagonal generating function and exact Stieltjes-moment necessary conditions',
            'reverse':args.reverse,'hankel_order':args.order,'tested_n':[],'failure':None}
    for n in range(2,args.size+1):
        if time.monotonic()-start>args.seconds:
            break
        d=[comb(n,k)**2 for k in range(n+1)]
        g=combine(gm1,neg(shift(gm2)),d,neg(dm1),neg(shift(dm1)),shift(dm2))
        twicep=combine(g,gm1,neg(shift(gm1)),shift(fm1))
        assert all(c%2==0 for c in twicep)
        p=[c//2 for c in twicep]
        q=combine(g,neg(p))
        if args.reverse:
            assert len(p)==len(q) and p[-1]==1
            assert q[-1]==(1 if n==2 else 2*n-2)
            lead=q[-1]
            p=p[::-1]
            q=[lead*u-v for u,v in zip(p,q[::-1])]
        m=moments(p,q,2*args.order+1)
        failure=None
        if min(q)<0:
            failure={'type':'negative coefficient','n':n,'p':p,'q':q}
        elif min(m)<0:
            failure={'type':'negative moment','n':n,'p':p,'q':q,'moments':m}
        else:
            for order in range(1,min(args.order,n-1)+1):
                for offset in (0,1):
                    mat=[[m[i+j+offset] for j in range(order)] for i in range(order)]
                    det=determinant(mat)
                    if det<0:
                        failure={'type':'negative Hankel determinant','n':n,'order':order,
                                 'offset':offset,'determinant':str(det),'p':p,'q':q}
                        break
                if failure:
                    break
        result['tested_n'].append(n)
        if failure:
            result['failure']=failure
            print(json.dumps(failure),flush=True)
            break
        f=combine(fm1,neg(shift(fm2)))
        gm2,gm1=gm1,g
        dm2,dm1=dm1,d
        fm2,fm1=fm1,f
        if n%25==0:
            print('n=',n,'elapsed=',time.monotonic()-start,flush=True)
    result['elapsed_seconds']=time.monotonic()-start
    with open(args.output,'w') as stream:
        json.dump(result,stream,indent=2)
    print(json.dumps({'checked':len(result['tested_n']),'last_n':result['tested_n'][-1],
                      'failure':result['failure'],'elapsed':result['elapsed_seconds']}),flush=True)


if __name__=='__main__':
    main()
