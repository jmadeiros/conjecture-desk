"""
Modular bookkeeping for a Sturm-bound proof of Conjectures 6.3 and 6.4 of arXiv:2611.05623v1 (3-adic).
F = f6/(f1 f2 f3) = eta(6t)/(eta(t)eta(2t)eta(3t)) (no q-shift).  For a claim  A_k(m n + r) = 0 mod 3^t :
  g = Delta(m t)^c * F^k ,  Delta(m t) = q^m prod (1-q^{mn})^24  (q^m times a unit power series in q^m).
  So (class r mod m of g) = Delta(m t)^c * (class r mod m of F^k): one vanishes mod 3^t iff the other does.
  Choose the least c making g holomorphic at all cusps of Gamma_0(N) (Newman + Ligozat); weight w = 12c - k.
  If p = gcd(r,m) > 1 (p | N): apply U_p, staying in M_w(Gamma_0(N),chi); then extract the class r/p mod m/p by twists with
  Dirichlet characters mod m' = m/p (all real since m' | 24), landing in M_w(Gamma_0(N m'^2), chi)  (Ono, Web of Modularity, Prop 2.8).
  Sturm bound B = floor(w * [SL2(Z):Gamma_0(N m'^2)] / 12).  Enough: A_k(n) = 0 mod 3^t for all n = r mod m, n <= p*B.
"""
from math import gcd
from fractions import Fraction as Fr
import json
def psi(N):
    out=Fr(N); n=N; p=2
    while p<=n:
        if n%p==0:
            out*=Fr(p+1,p)
            while n%p==0: n//=p
        p+=1
    return int(out)
def data(r):
    base=1
    for d in r: base=base*d//gcd(base,d)
    assert sum(d*e for d,e in r.items())%24==0
    N=base
    while sum((N//d)*e for d,e in r.items())%24: N+=base
    w=Fr(sum(r.values()),2)
    mo=min(Fr(N,24*d*gcd(d,N//d))*sum(Fr(gcd(d,dl)**2*e,dl) for dl,e in r.items()) for d in range(1,N+1) if N%d==0)
    return N,w,mo
claims=[("Conj 6.3  A_6(12n+10) = 0 mod 3^5",6,12,10,5),("Conj 6.4a A_3(12n+7)  = 0 mod 3^4",3,12,7,4),
 ("Conj 6.4a A_3(12n+11) = 0 mod 3^4",3,12,11,4),("Conj 6.4b A_4(6n+5)   = 0 mod 3^3",4,6,5,3),
 ("Conj 6.4b A_7(12n+11) = 0 mod 3^3",7,12,11,3),("Conj 6.4c A_8(18n+15) = 0 mod 3^5",8,18,15,5)]
plans=[]
for label,k,m,r,t in claims:
    c=0
    while True:
        c+=1
        e={6:k,1:-k,2:-k,3:-k}; e[m]=e.get(m,0)+24*c
        N,w,mo=data(e)
        if mo>=0 and w>0 and w.denominator==1: break
    p=gcd(r,m); mp=m//p; rp=r//p
    assert gcd(rp,mp)==1 and 24%mp==0 and N%p==0
    Np=N*mp*mp; B=int(w)*psi(Np)//12
    pl=dict(label=label,k=k,m=m,r=r,t=t,delta_power_c=c,eta={str(d):v for d,v in sorted(e.items())},N=N,weight=int(w),min_cusp_order=str(mo),
            U_p=p,class_mod=mp,class_res=rp,level_after=Np,index=psi(Np),sturm_bound=B,need_n_upto=p*B)
    plans.append(pl); print(json.dumps(pl))
json.dump(plans,open("plan_3adic.json","w"),indent=1)
