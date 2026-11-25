"""
Finite Sturm-bound certificate for the 2-adic conjectures (Conj. conj:A2adic, conj:B2adic) of
Yaqubi-Mirzavaziri, arXiv:2611.05623v1.  Implementation 1: numpy uint64 arithmetic (exact mod 2^64).

For an eta quotient g = prod eta(d tau)^{r_d} we
  * check Newman's conditions on Gamma_0(N) and compute the order at every cusp (Ligozat),
  * if needed multiply by Delta(4 tau)^c (a q^4-series times q^{4c}) to make it holomorphic,
  * the series T3(g) = sum_{n = 3 mod 4} a(n) q^n lies in M_k(Gamma_0(16 N), chi), integer coefficients,
  * Sturm bound B = floor(k * index(Gamma_0(16N)) / 12); check a(n) = 0 mod 2^t for all n<=B, n=3 mod 4.
"""
import numpy as np, sys, json
from math import gcd
from fractions import Fraction
M64=1<<64
def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def index_gamma0(N):
    r=N; p=2; n=N
    primes=set()
    while p*p<=n:
        if n%p==0:
            primes.add(p)
            while n%p==0: n//=p
        p+=1
    if n>1: primes.add(n)
    num=N; den=1
    for p in primes: num*=(p+1); den*=p
    assert num%den==0
    return num//den
def newman(r,N):
    s1=sum(d*e for d,e in r.items()); s2=sum((N//d)*e for d,e in r.items())
    w=Fraction(sum(r.values()),2)
    return s1%24==0 and s2%24==0 and all(N%d==0 for d in r), w
def cusp_orders(r,N):
    out={}
    for d in divisors(N):
        o=Fraction(N,24)*sum(Fraction(gcd(d,dl)**2*e, gcd(d,N//d)*d*dl) for dl,e in r.items())
        out[d]=o
    return out
def eta_series(r,L):
    """coefficients (mod 2^64) of prod_d prod_n (1-q^{dn})^{r_d}, times q^{sum d r_d/24}; returns (shift, array)"""
    a=np.zeros(L,dtype=np.uint64); a[0]=1
    for d,e in sorted(r.items()):
        # f_d = sum_k (-1)^k q^{d k(3k-1)/2}; multiply |e| times by f_d or 1/f_d
        fd=np.zeros(L,dtype=np.uint64); fd[0]=1
        k=1
        while True:
            p1=d*k*(3*k-1)//2; p2=d*k*(3*k+1)//2
            if p1>=L: break
            sgn=np.uint64(1) if k%2==0 else np.uint64(M64-1)
            fd[p1]=sgn
            if p2<L: fd[p2]=sgn
            k+=1
        if e<0:
            # inverse of fd by recurrence using its sparse support
            supp=[(int(i),int(fd[i])) for i in np.nonzero(fd)[0] if i>0]
            inv=[0]*L; inv[0]=1
            for n in range(1,L):
                s=0
                for i,c in supp:
                    if i>n: break
                    s+=c*inv[n-i]
                inv[n]=(-s)%M64
            fd=np.array(inv,dtype=np.uint64)
        for _ in range(abs(e)):
            a=np.convolve(a,fd)[:L]
    s=sum(d*e for d,e in r.items()); assert s%24==0
    return s//24, a
def v2(x):
    x=int(x)
    return 64 if x==0 else (x&-x).bit_length()-1
def check(name,r,t,witness_mod=None,log=None):
    """prove T3(prod eta^r) = 0 mod 2^t; optionally also report a witness n with v2 < log2(witness_mod)"""
    N=1
    for d in r: N=N*d//gcd(N,d)
    # find level satisfying Newman
    N0=N; mult=1
    while not newman(r,N0*mult)[0]: mult+=1
    N=N0*mult
    ok,w=newman(r,N); assert ok
    co=cusp_orders(r,N); c=0
    rr=dict(r)
    if min(co.values())<0 or w<=0 or w.denominator!=1:
        # multiply by Delta(4 tau)^c ; need 4 | N
        while N%4: N*=2
        while True:
            c+=1
            rr=dict(r); rr[4]=rr.get(4,0)+24*c
            assert newman(rr,N)[0]
            co=cusp_orders(rr,N)
            if min(co.values())>=0: break
        w=newman(rr,N)[1]
    assert w.denominator==1 and w>0 and min(co.values())>=0
    k=int(w); Np=16*N; idx=index_gamma0(Np); B=(k*idx)//12
    L=B+8
    shift,a=eta_series(rr,L)
    assert shift>=0
    # coefficient of q^n in the form = a[n-shift]; shift is a multiple of 4 when c>0 (shift=4c) or 0
    assert shift%4==0
    worst=64; nw=None; cnt=0; wit=None
    for n in range(3,B+1,4):
        if n-shift<0: continue
        v=v2(a[n-shift]); cnt+=1
        if v<worst: worst=v; nw=n
        if witness_mod is not None and wit is None and v<witness_mod: wit=(n-shift,v)
    res=dict(name=name,eta=dict(r),delta4_power=c,level_N=N,level_after_T3=Np,weight=k,index=idx,sturm_bound=B,
             coeffs_checked=cnt,min_v2_up_to_bound=worst,argmin=nw,claim_t=t,PROVED=bool(worst>=t),
             cusp_orders_min=str(min(co.values())))
    if witness_mod is not None: res['witness_v2_lt_%d'%witness_mod]=wit
    print(json.dumps(res)); sys.stdout.flush()
    return res
if __name__=="__main__":
    G={1:1,2:1,3:1,6:-1}            # G = 1/F,  F = sum PD-type series f6/(f1 f2 f3)
    Q={1:1,3:1,12:1,4:-1,6:-2}      # Q = 1/PDO, PDO = f4 f6^2/(f1 f3 f12)
    pw=lambda r,j:{d:e*j for d,e in r.items()}
    out=[]
    out.append(check("A: T3(G)=0 (identically; t=64 proxy handled separately)",G,64))
    for j,t in [(2,2),(6,3),(10,2),(14,3)]:
        out.append(check(f"A: T3(G^{j}) = 0 mod 2^{t}",pw(G,j),t,witness_mod=4))
    out.append(check("A: witness T3(G^30) != 0 mod 16",pw(G,30),3,witness_mod=4))
    for j,t in [(3,1),(7,2),(6,2),(10,3),(2,3)]:
        out.append(check(f"B: T3(Q^{j}) = 0 mod 2^{t}",pw(Q,j),t,witness_mod=t+1))
    for j,t in [(15,2),(18,3),(26,3)]:
        out.append(check(f"B: witness T3(Q^{j}) != 0 mod 2^{t+1}",pw(Q,j),t,witness_mod=t+1))
    json.dump(out,open("prove_2adic_impl1.json","w"),indent=1)
