"""Verify the diagonal Gamma-difference counterexample using Theorem 2.13.

Independent of the two-dimensional coefficient/evaluation recurrences.
All construction, evaluation, and sign decisions use integers only.
"""
import argparse
import hashlib
import json
from math import comb


def combine(*terms):
    out = [0] * max(len(t) for t in terms)
    for term in terms:
        for k, coefficient in enumerate(term):
            out[k] += coefficient
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def neg(poly):
    return [-coefficient for coefficient in poly]


def shift(poly):
    return [0] + poly


def diagonal_pair(n):
    gm2,gm1=[1],[1]
    dm2,dm1=[1],[1,1]
    fm2,fm1=[1],[1]
    for k in range(2,n+1):
        d=[comb(k,j)**2 for j in range(k+1)]
        g=combine(gm1,neg(shift(gm2)),d,neg(dm1),neg(shift(dm1)),shift(dm2))
        if k==n:
            numerator=combine(g,gm1,neg(shift(gm1)),shift(fm1))
            assert all(c%2==0 for c in numerator)
            p=[c//2 for c in numerator]
            q=combine(g,neg(p))
            return p,q
        f=combine(fm1,neg(shift(fm2)))
        gm2,gm1=gm1,g
        dm2,dm1=dm1,d
        fm2,fm1=fm1,f
    raise ValueError('n must be at least 2')


def scaled_value(poly,num,den):
    # Return den^degree * poly(num/den).
    value=poly[-1]
    power=1
    for c in reversed(poly[:-1]):
        power*=den
        value=value*num+c*power
    return value


def evaluate(p,q,num,den):
    dp=[j*c for j,c in enumerate(p)][1:]
    dq=[j*c for j,c in enumerate(q)][1:]
    assert len(p)==len(q)
    pv=scaled_value(p,num,den)
    qv=scaled_value(q,num,den)
    pd=scaled_value(dp,num,den)
    qd=scaled_value(dq,num,den)
    w=pv*qd-pd*qv
    return {'P':pv,'Q':qv,'P_derivative':pd,'Q_derivative':qd,'W':w,
            'W_denominator_power':2*(len(p)-1)-1}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--n',type=int,default=165)
    ap.add_argument('--num',type=int,default=-5)
    ap.add_argument('--den',type=int,default=101)
    ap.add_argument('--output',default='counterexample.json')
    args=ap.parse_args()
    p,q=diagonal_pair(args.n)
    values=evaluate(p,q,args.num,args.den)
    denominator=args.den**values['W_denominator_power']
    floor=values['W']//denominator
    assert floor*denominator<=values['W']<(floor+1)*denominator
    assert p[0] == 1 and q[0] == 0
    assert min(p) > 0 and min(q) >= 0
    if (args.n,args.num,args.den) == (165,-5,101):
        assert len(p) == len(q) == 165
        assert q[1] == 164
        assert -5621*denominator < values['W'] < -5620*denominator
    record={'n':args.n,'s':[args.num,args.den],'degree':len(p)-1,
            'method':'Theorem 2.13 diagonal generating function, binomial-square coefficients',
            'P_coefficients':p,'Delta_coefficients':q,
            'scaled_values':{k:str(v) for k,v in values.items()},
            'W_at_zero':q[1],
            'W_rational_interval':[floor,floor+1],
            'P_all_coefficients_positive':all(c>0 for c in p),
            'Delta_all_coefficients_nonnegative':all(c>=0 for c in q),
            'W_negative':values['W']<0}
    with open(args.output,'w') as stream:
        json.dump(record,stream,indent=2)
    print(json.dumps({'n':args.n,'s':[args.num,args.den],'degree':len(p)-1,
                      'W_negative':values['W']<0,'W_digits':len(str(abs(values['W']))),
                      'W_at_zero':q[1],'W_rational_interval':[floor,floor+1],
                      'W_prefix':str(values['W'])[:70],
                      'coefficient_hash':hashlib.sha256(json.dumps([p,q]).encode()).hexdigest()}),flush=True)


if __name__=='__main__':
    main()
