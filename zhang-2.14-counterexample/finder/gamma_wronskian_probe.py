"""Integer-only rational-point necessary-condition search for C2.14.

If Gamma_previous properly interlaces Delta, the Wronskian
Gamma_previous*Delta' - Gamma_previous'*Delta is nonnegative on R.
Evaluate the recurrence and its derivative using q^min(a,b) scaling
at s=-p/q. Only two rows are kept, so large dimensions are inexpensive.
"""
import argparse
import json
import time


def probe(n,p,q):
    # F_m=q^m f_m(-p/q), dF_m=q^m f'_m(-p/q).
    F=[1,q]
    dF=[0,0]
    for m in range(2,n):
        F.append(q*F[-1]+p*q*F[-2])
        dF.append(q*dF[-1]+p*q*dF[-2]-q*q*F[m-2])
    prev=[1]+[q-(b-1)*p for b in range(1,n+1)]
    dprev=[0]+[(b-1)*q for b in range(1,n+1)]
    for a in range(2,n+1):
        cur=[1,q-(a-1)*p]+[0]*(n-1)
        dcur=[0,(a-1)*q]+[0]*(n-1)
        for b in range(2,n+1):
            if a<b:
                cur[b]=q*prev[b]+cur[b-1]-(p+q)*prev[b-1]
                dcur[b]=q*dprev[b]+dcur[b-1]-(p+q)*dprev[b-1]+q*prev[b-1]
            elif a>b:
                cur[b]=prev[b]+q*cur[b-1]-(p+q)*prev[b-1]
                dcur[b]=dprev[b]+q*dcur[b-1]-(p+q)*dprev[b-1]+q*prev[b-1]
            else:
                cur[b]=q*(prev[b]+cur[b-1])-(p+q)*prev[b-1]+p*F[a-1]
                dcur[b]=q*(dprev[b]+dcur[b-1])-(p+q)*dprev[b-1]+q*prev[b-1]-q*F[a-1]+p*dF[a-1]
            W=cur[b-1]*dcur[b]-dcur[b-1]*cur[b]
            if W<0:
                return {'a':a,'b':b,'s_numerator':-p,'s_denominator':q,
                        'scaled_previous':cur[b-1],'scaled_previous_derivative':dcur[b-1],
                        'scaled_current':cur[b],'scaled_current_derivative':dcur[b],
                        'Wronskian_numerator':W}
        prev,dprev=cur,dcur
    return None


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--size',type=int,default=1000)
    args=ap.parse_args()
    start=time.monotonic()
    records=[]
    for p,q in [(1,1),(2,1),(10,1),(1,2),(1,10),(1,100),(100,1)]:
        result=probe(args.size,p,q)
        records.append({'p':p,'q':q,'size':args.size,'failure':result})
        with open('gamma_wronskian_results.json','w') as f:
            json.dump(records,f,indent=2)
        print(f's=-{p}/{q}: failure={result}, elapsed={time.monotonic()-start:.2f}s',flush=True)
        if result:
            break


if __name__=='__main__':
    main()
