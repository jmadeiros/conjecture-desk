"""O(n) exact diagonal Wronskian probe from Theorem2.13, not the 2D recurrence."""
import argparse
import json
import time


def diagonal(n,p,q):
    # E_k=q^k D_k(s), with D_k=sum binomial(k,j)^2 s^j, s=-p/q.
    E=[1,q-p]
    Ed=[0,q]
    for k in range(1,n):
        num=(2*k+1)*(q-p)*E[k]-k*(q+p)**2*E[k-1]
        dnum=(2*k+1)*((q-p)*Ed[k]+q*E[k])-k*((q+p)**2*Ed[k-1]-2*q*(q+p)*E[k-1])
        assert num%(k+1)==0 and dnum%(k+1)==0
        E.append(num//(k+1)); Ed.append(dnum//(k+1))
    # C(z)=D(z)/(1-z+s*z^2), F(z)=1/(1-z+s*z^2).
    C=[]; Cd=[]; F=[]; Fd=[]; G=[]; Gd=[]
    for k in range(n+1):
        c1=C[k-1] if k else 0; c2=C[k-2] if k>1 else 0
        cd1=Cd[k-1] if k else 0; cd2=Cd[k-2] if k>1 else 0
        f1=F[k-1] if k else 0; f2=F[k-2] if k>1 else 0
        fd1=Fd[k-1] if k else 0; fd2=Fd[k-2] if k>1 else 0
        C.append(E[k]+q*c1+p*q*c2)
        Cd.append(Ed[k]+q*cd1+p*q*cd2-q*q*c2)
        F.append((1 if k==0 else 0)+q*f1+p*q*f2)
        Fd.append(q*fd1+p*q*fd2-q*q*f2)
        G.append(E[k]+p*c1)
        Gd.append(Ed[k]-q*c1+p*cd1)
        if k>=2:
            # P_k=Gamma_(k,k-1), scaled by q^k here.
            Pnum=G[k]+(q+p)*G[k-1]-p*F[k-1]
            Pdnum=Gd[k]+(q+p)*Gd[k-1]-q*G[k-1]+q*F[k-1]-p*Fd[k-1]
            assert Pnum%2==0 and Pdnum%2==0
            P=Pnum//2; Pd=Pdnum//2
            W=P*Gd[k]-Pd*G[k]
            if W<0:
                return {'a':k,'b':k,'s_numerator':-p,'s_denominator':q,
                        'scale_exponent':k,'previous':P,'previous_derivative':Pd,
                        'current':G[k],'current_derivative':Gd[k],
                        'Wronskian_numerator':W}
    return None


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--size',type=int,default=1000)
    ap.add_argument('--p',type=int)
    ap.add_argument('--q',type=int)
    args=ap.parse_args()
    start=time.monotonic()
    bound=args.size
    best=None
    points=[(args.p,args.q)] if args.p else [(1,q) for q in range(3,1001)]
    for p,q in points:
        hit=diagonal(bound,p,q)
        if hit:
            best=hit; bound=hit['a']
            print(f'found n={bound}, s=-{p}/{q}, elapsed={time.monotonic()-start:.2f}s',flush=True)
            with open('gamma_diagonal_certificate.json','w') as f:
                json.dump(best,f,indent=2)
    print('done', None if best is None else (best['a'],best['s_numerator'],best['s_denominator']),flush=True)


if __name__=='__main__':
    main()
