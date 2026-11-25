"""Truncated exact Gamma table and necessary moment checks for C2.14."""
import argparse
import json
import time
from gamma_moment_audit import determinant, moments


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--size',type=int,default=1000)
    ap.add_argument('--order',type=int,default=6)
    ap.add_argument('--all-until',type=int,default=120)
    ap.add_argument('--seconds',type=int,default=420)
    args=ap.parse_args()
    start=time.monotonic()
    n=args.size
    k=2*args.order+2
    zero=[0]*k
    one=[1]+[0]*(k-1)
    prev=[one[:]]+[[1,b-1]+[0]*(k-2) for b in range(1,n+1)]
    fs=[[1]+[0]*(k-1),[1]+[0]*(k-1)]
    for a in range(2,n):
        fs.append([fs[-1][0]]+[fs[-1][j]-fs[-2][j-1] for j in range(1,k)])
    offsets={0,1,-1,2,-2,3,-3,4,-4,5,-5,8,-8,10,-10,20,-20,50,-50,100,-100,200,-200,500,-500}
    result={'method':'truncated integer recurrence; signed Taylor coefficients and leading Hankel minors',
            'truncation':k,'hankel_order':args.order,'all_until':args.all_until,
            'offsets':sorted(offsets),'tested_count':0,'last_pair':None,'failure':None}
    for a in range(2,n+1):
        if time.monotonic()-start>args.seconds:
            break
        cur=[one[:],[1,a-1]+[0]*(k-2)]
        for b in range(2,n+1):
            v=[cur[-1][j]+prev[b][j]-prev[b-1][j] for j in range(k)]
            for j in range(1,k):
                v[j]+=prev[b-1][j-1]
                if a==b:
                    v[j]-=fs[a-1][j-1]
            cur.append(v)
            if not ((a<=args.all_until and b<=args.all_until) or b-a in offsets):
                continue
            p=cur[-2]
            q=[v[j]-p[j] for j in range(k)]
            failure=None
            m=moments(p,q,k-1)
            if min(q)<0:
                failure={'type':'negative coefficient','a':a,'b':b,'p':p,'q':q}
            elif min(m)<0:
                failure={'type':'negative moment','a':a,'b':b,'p':p,'q':q,'moments':m}
            else:
                degree=min(a,b-1,(a+b-2)//2)
                # Degree increase permits a nonnegative linear part in q/p;
                # shifting by one omits the possibly exceptional moment m0.
                for order in range(1,min(args.order,degree)+1):
                    for offset in (1,2):
                        mat=[[m[i+j+offset] for j in range(order)] for i in range(order)]
                        det=determinant(mat)
                        if det<0:
                            failure={'type':'negative Hankel determinant','a':a,'b':b,
                                     'order':order,'offset':offset,'determinant':str(det),'p':p,'q':q}
                            break
                    if failure:
                        break
            result['tested_count']+=1
            result['last_pair']=[a,b]
            if failure:
                result['failure']=failure
                print(json.dumps(failure),flush=True)
                break
        prev=cur
        if a%25==0:
            print('row',a,'pairs',result['tested_count'],'elapsed',time.monotonic()-start,flush=True)
        if result['failure']:
            break
    result['elapsed_seconds']=time.monotonic()-start
    with open('gamma_moment_grid_results.json','w') as stream:
        json.dump(result,stream,indent=2)
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
