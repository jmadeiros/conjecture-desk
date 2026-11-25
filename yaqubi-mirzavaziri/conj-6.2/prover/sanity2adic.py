# Direct numeric test of Yaqubi-Mirzavaziri Conj (A2adic), (B2adic): arithmetic mod 2^64 (numpy uint64 wraps).
import numpy as np, sys
N=int(sys.argv[1]); K=int(sys.argv[2])
def fser(m):
    a=np.zeros(N,dtype=np.uint64); a[0]=1
    n=m
    while n<N:
        a[n:]=a[n:]-a[:-n].copy() if False else a[n:]  # placeholder
        n+=m
    return a
def eta_prod(exps):
    # prod_{d} f_d^{r_d} as integer series mod 2^64, via repeated multiply/divide by (1-q^{dn})
    a=[0]*N; a[0]=1; M=1<<64
    for d,r in exps.items():
        for _ in range(abs(r)):
            n=d
            while n<N:
                if r>0:
                    for i in range(N-1,n-1,-1): a[i]=(a[i]-a[i-n])%M
                else:
                    for i in range(n,N): a[i]=(a[i]+a[i-n])%M
                n+=d
    return np.array(a,dtype=np.uint64)
def mul(a,b):
    return np.convolve(a,b)[:N]
def v2(x):
    x=int(x)
    if x==0: return 64
    return (x&-x).bit_length()-1
def run(name,exps,poly,exc):
    F=eta_prod(exps); P=np.zeros(N,dtype=np.uint64); P[0]=1
    bad=0
    for k in range(1,K+1):
        P=mul(P,F)
        vals=[v2(P[n]) for n in range(3,N,4)]
        m=min(vals); a3=poly(k); va3=v2(a3)
        assert int(P[3])==a3%(1<<64),(k,int(P[3]),a3)
        pred=exc(k) if exc(k) is not None else va3
        if m!=pred:
            bad+=1; print(name,"MISMATCH k",k,"min v2",m,"pred",pred,"v2(coef3)",va3,"argmin n",vals.index(m))
    print(name,"done K",K,"N",N,"mismatches",bad)
run("A",{6:1,1:-1,2:-1,3:-1},lambda k:k*(k+1)*(k+14)//6,lambda k:3 if k%16==2 else None)
run("B",{4:1,6:2,1:-1,3:-1,12:-1},lambda k:k*(k+2)*(k+7)//6,lambda k:2 if k%8==1 else (3 if k%8==6 else None))
