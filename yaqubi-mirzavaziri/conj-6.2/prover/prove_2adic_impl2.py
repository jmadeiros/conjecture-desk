"""
Independent re-check (implementation 2) of the finite certificate for arXiv:2611.05623v1 Conj. A2adic/B2adic.
Differences from implementation 1: exact Python integers (no modulus), eta-quotient coefficients from the
logarithmic-derivative recurrence  n p(n) = sum_{m=1..n} c(m) p(n-m),  c(m) = -sum_{d | m} d * a_d
for P = prod_n (1-q^n)^{a_n};  cusp orders / Sturm bound recomputed from scratch;  witnesses taken on the
un-multiplied series (Q^j itself), computed mod nothing (exact).
"""
import sys, json
from math import gcd
from fractions import Fraction as Fr
def eta_exact(r, L):
    # a_n = sum_{d | n, d in r} r_d
    a=[0]*(L+1)
    for d,e in r.items():
        for n in range(d,L+1,d): a[n]+=e
    c=[0]*(L+1)
    for d in range(1,L+1):
        if a[d]:
            v=-d*a[d]
            for m in range(d,L+1,d): c[m]+=v
    p=[0]*(L+1); p[0]=1
    for n in range(1,L+1):
        s=0
        for m in range(1,n+1):
            cm=c[m]
            if cm: s+=cm*p[n-m]
        q,rem=divmod(s,n); assert rem==0
        p[n]=q
    return p
def psi(N):
    out=Fr(N); n=N; p=2
    while p<=n:
        if n%p==0:
            out*=Fr(p+1,p)
            while n%p==0: n//=p
        p+=1
    assert out.denominator==1; return int(out)
def v2(x):
    if x==0: return 10**9
    v=0
    while x%2==0: x//=2; v+=1
    return v
def modular_data(r):
    """smallest N (multiple of all deltas and of 4) with Newman conditions; weight; min cusp order"""
    base=4
    for d in r: base=base*d//gcd(base,d)
    N=base
    while True:
        if sum(d*e for d,e in r.items())%24==0 and sum((N//d)*e for d,e in r.items())%24==0: break
        N+=base
    k=Fr(sum(r.values()),2)
    orders=[]
    for d in range(1,N+1):
        if N%d: continue
        orders.append(Fr(N,24*d*gcd(d,N//d))*sum(Fr(gcd(d,dl)**2*e,dl) for dl,e in r.items()))
    return N,k,min(orders)
def prove(label, base, j, t):
    r={d:e*j for d,e in base.items()}
    c=0
    while True:
        rr=dict(r)
        if c: rr[4]=rr.get(4,0)+24*c
        N,k,mo=modular_data(rr)
        if mo>=0 and k>0 and k.denominator==1: break
        c+=1
    k=int(k); B=k*psi(16*N)//12
    shift=sum(d*e for d,e in rr.items())//24     # = 4c
    p=eta_exact(rr,B+4)
    worst=min((v2(p[n-shift]) for n in range(3,B+1,4) if n-shift>=0))
    ok = worst>=t
    print(json.dumps(dict(label=label,j=j,claim_mod=f"2^{t}" if t<100 else "identically 0",delta4_power=c,N=N,weight=k,sturm=B,min_v2=(worst if worst<10**9 else "all zero"),PROVED=ok))); sys.stdout.flush()
    return ok
def witness(label, base, j, s):
    """find n=3 mod 4 with v2([q^n] base^j) < s, on the series itself"""
    r={d:e*j for d,e in base.items()}
    p=eta_exact(r,400)
    for n in range(3,400,4):
        if v2(p[n])<s:
            print(json.dumps(dict(label=label,j=j,n=n,v2=v2(p[n]),coef=str(p[n]),need_lt=s,FOUND=True))); return True
    print(json.dumps(dict(label=label,j=j,FOUND=False))); return False
G={1:1,2:1,3:1,6:-1}; Q={1:1,3:1,12:1,4:-1,6:-2}
allok=True
allok&=prove("A T3(G)",G,1,10**6)
for j,t in [(2,2),(6,3),(10,2),(14,3)]: allok&=prove("A T3(G^j)",G,j,t)
for j in (14,30): allok&=witness("A exactness class 2 mod 16",G,j,4)
for j,t in [(3,1),(7,2),(6,2),(10,3),(2,3)]: allok&=prove("B T3(Q^j)",Q,j,t)
for j in (7,15): allok&=witness("B exactness class 1 mod 8",Q,j,3)
for j in (2,10,18,26): allok&=witness("B exactness class 6 mod 8",Q,j,4)
print("ALL OK" if allok else "SOMETHING FAILED")
