import sys, mpmath as mp
sys.path.insert(0, sys.argv[1])
from check import landau_table, li_inv
g = landau_table(400)
bad = []
for n in range(2, 400):
    L = mp.sqrt(li_inv(n-1))
    if mp.log(g[n-1] + n*n - 2) >= L:
        bad.append(n)
print("li^-1(2)", mp.nstr(li_inv(2),6), "sqrt", mp.nstr(mp.sqrt(li_inv(2)),6), "log6", mp.nstr(mp.log(6),6))
print("li^-1(3)", mp.nstr(li_inv(3),6), "sqrt", mp.nstr(mp.sqrt(li_inv(3)),6), "log11", mp.nstr(mp.log(11),6))
print("n where upper-bound log(g(n-1)+n^2-2) >= sqrt(li^-1(n-1)):", bad)
