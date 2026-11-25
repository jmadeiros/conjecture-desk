from fractions import Fraction as Fr
from itertools import combinations_with_replacement as cwr
def omega(a,b,c):            # OpenAI Lean-scope rectangular_exponent (positive weights)
    x,y,z=sorted([Fr(a),Fr(b),Fr(c)],reverse=True)
    if z==0: return x+y
    return x+y+max(Fr(0),(x+y)*z-x*y)**2/(4*x*y*z)
def psi(a,b,c):              # Zhou Prop (Uznanski/ABZ upper curve)
    a,b,c=sorted([Fr(a),Fr(b),Fr(c)],reverse=True)
    return a+b if c*(a+b)<=a*b else (a*b+a*c+b*c)**2/(4*a*b*c)
bad=[]
for k in range(3,42):
    K=Fr(k*k,4); floor=Fr(k*k//4)
    best_formula=Fr(0); best_pdf=Fr(0)
    for p in cwr(range(0,k+1),3):
        if sum(p)!=k: continue
        a,b,c=sorted(p,reverse=True)
        e=(a*b,a*c,b*c)
        if min(e)>0 and omega(*e)!=psi(*e): bad.append(('psi',k,p))
        f=omega(*e) if max(e)>0 else Fr(0)
        if f>K: bad.append(('exceeds Zhou',k,p,f))
        if c>0 and a<=b+c and f!=K: bad.append(('tri-identity',k,p,f))
        best_formula=max(best_formula,f)
        # PDF Cor 1.3: max{ab,bc,ca,(abc)^{3/4}} in log2 -> max(pairwise sums, 3/4 total)
        pdf=max(e[0]+e[1],e[0]+e[2],e[1]+e[2],Fr(3,4)*sum(e))
        best_pdf=max(best_pdf,pdf)
    if k%2==1:
        m=(k-1)//2
        assert omega(m*m,m,m)==K==m*m+m+Fr(1,4)
        print(f"k={k:2d} k^2/4={float(K):7.2f} floor={int(floor):4d} formula-best={float(best_formula):7.2f} PDF-Cor1.3-best={float(best_pdf):7.2f} PDF-closes-gap={best_pdf==K} (k%3={k%3})")
print("violations:",bad[:5],len(bad))
