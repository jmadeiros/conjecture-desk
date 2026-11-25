"""
Implementation 2 for the 3-adic certificate (Conj. 6.3, 6.4 of arXiv:2611.05623v1), written separately from pdk.c / plan_3adic.py.
 - coefficients: F built factor by factor from prod_n (1-q^{6n}) / ((1-q^n)(1-q^{2n})(1-q^{3n})) with numpy (mod 3^7),
   powers by np.convolve (int64, exact before reduction);
 - modular data (level, weight, cusp orders, Sturm bound) recomputed here with its own code;
 - compares every coefficient with the dump of pdk.c, then checks the progressions up to the bound.
"""
import numpy as np, sys, json
from math import gcd
from fractions import Fraction as Fr
M=3**7; L=112400
def times_one_minus(a,n):   # a *= (1-q^n)
    a=a.copy(); a[n:]=(a[n:]-a[:-n])%M; return a
def over_one_minus(a,n):    # a /= (1-q^n)
    pad=(-len(a))%n
    b=np.concatenate([a,np.zeros(pad,dtype=np.int64)]).reshape(-1,n)
    return (np.cumsum(b,axis=0)%M).reshape(-1)[:len(a)]
F=np.zeros(L+1,dtype=np.int64); F[0]=1
for n in range(1,L+1):
    if 6*n<=L: F=times_one_minus(F,6*n)
    F=over_one_minus(F,n)
    if 2*n<=L: F=over_one_minus(F,2*n)
    if 3*n<=L: F=over_one_minus(F,3*n)
def mul(a,b): return np.convolve(a,b)[:L+1]%M
P={1:F}; P[2]=mul(F,F); P[3]=mul(P[2],F); P[4]=mul(P[2],P[2]); P[6]=mul(P[3],P[3]); P[7]=mul(P[6],F); P[8]=mul(P[4],P[4])
print("F coefficients 0..8:",F[:9].tolist()); sys.stdout.flush()
for k in (3,4,6,7,8):
    ref=np.fromfile(f"coef_k{k}.bin",dtype=np.uint32)[:L+1].astype(np.int64)
    print(f"k={k}: coefficients 0..{L} vs pdk.c dump: mismatches =",int((ref!=P[k]).sum()))
def index0(N):
    x=Fr(N); n=N; p=2
    while n>1:
        if n%p==0:
            x*=Fr(p+1,p)
            while n%p==0: n//=p
        p+=1
    return int(x)
def v3(x):
    if x==0: return 7
    v=0
    while x%3==0: x//=3; v+=1
    return v
allok=True
for label,k,m,r,t in [("6.3",6,12,10,5),("6.4a",3,12,7,4),("6.4a",3,12,11,4),("6.4b",4,6,5,3),("6.4b",7,12,11,3),("6.4c",8,18,15,5)]:
    c=1
    while True:
        e={1:-k,2:-k,3:-k,6:k}; e[m]=e.get(m,0)+24*c
        l=1
        for d in e: l=l*d//gcd(l,d)
        N=l
        while (sum(Fr(N,d)*x for d,x in e.items()))%24!=0: N+=l
        assert sum(d*x for d,x in e.items())%24==0
        orders=[sum(Fr(gcd(d,dl)**2*x,dl) for dl,x in e.items()) for d in range(1,N+1) if N%d==0]   # positive multiple of the cusp order
        w=sum(e.values())//2
        if min(orders)>=0 and w>0 and sum(e.values())%2==0: break
        c+=1
    p=gcd(m,r); mp=m//p
    assert N%p==0 and 24%mp==0
    B=w*index0(N*mp*mp)//12; top=p*B
    assert top<=L
    vals=[v3(int(P[k][n])) for n in range(r,top+1,m)]
    ok=min(vals)>=t; allok&=ok
    print(json.dumps(dict(conj=label,claim=f"A_{k}({m}n+{r}) = 0 mod 3^{t}",delta_power=c,level=N,weight=w,sturm=B,checked_n_upto=top,terms=len(vals),min_v3=min(vals),PROVED=ok)))
print("exactness for 6.3: v3(A_6(22)) =",v3(int(P[6][22]))," A_6(22) mod 3^7 =",int(P[6][22]),"  (6635911068 mod 3^7 =",6635911068%M,")")
print("ALL OK" if allok else "FAILED")
