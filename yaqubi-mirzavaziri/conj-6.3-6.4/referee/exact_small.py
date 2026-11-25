"""
Referee's exact (big-integer) check for small n, by a third route: brute-force enumeration of partitions with
designated summands for n <= 20 (definition: one part of each distinct size is marked), the combinatorial product
for F to n <= NMAX, then F^k by schoolbook multiplication with exact integers.
Compares with the C program's residues (ak_k{k}.bin mod 3^10) and prints exact A_6(10), A_6(22) with v3.
"""
import sys, struct
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
MOD = 3 ** 10

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0:
        yield []; return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p):
            yield [p] + rest

def pd_brute(n):
    tot = 0
    for lam in partitions(n):
        mult = {}
        for p in lam: mult[p] = mult.get(p, 0) + 1
        ways = 1
        for v in mult.values(): ways *= v  # choose which copy of each size is designated
        tot += ways
    return tot

F = [0] * (NMAX + 1); F[0] = 1
for t in range(1, NMAX + 1):
    fac = [0] * (NMAX + 1); fac[0] = 1
    for m in range(1, NMAX // t + 1): fac[t * m] = m
    new = [0] * (NMAX + 1)
    for i, a in enumerate(F):
        if a:
            for j in range(0, NMAX - i + 1, t):
                if fac[j]: new[i + j] += a * fac[j]
    F = new
brute = [pd_brute(n) for n in range(21)]
assert brute == F[:21], (brute, F[:21])
print("brute-force PD(n), n<=20, equals product series:", brute)

def mul(a, b):
    c = [0] * (NMAX + 1)
    for i, x in enumerate(a):
        if x:
            for j in range(NMAX + 1 - i): c[i + j] += x * b[j]
    return c

P = {1: F}
for k in range(2, 9): P[k] = mul(P[k - 1], F)

def v3(x):
    if x == 0: return 99
    v = 0
    while x % 3 == 0: x //= 3; v += 1
    return v

print("A_6(10) =", P[6][10], "v3 =", v3(P[6][10]))
print("A_6(22) =", P[6][22], "v3 =", v3(P[6][22]))
print("v3 of A_6(12n+10), n=0..%d:" % ((NMAX - 10) // 12), [v3(P[6][n]) for n in range(10, NMAX + 1, 12)])
for k in (3, 4, 6, 7, 8):
    raw = open("ak_k%d.bin" % k, "rb").read()
    res = struct.unpack("<%dI" % (len(raw) // 4), raw)
    bad = sum(1 for n in range(NMAX + 1) if P[k][n] % MOD != res[n])
    print("k=%d: exact vs C residues mod 3^10, n<=%d: mismatches = %d" % (k, NMAX, bad))
claims = [(6, 12, 10, 5), (3, 12, 7, 4), (3, 12, 11, 4), (4, 6, 5, 3), (7, 12, 11, 3), (8, 18, 15, 5)]
for k, m, r, t in claims:
    vs = [v3(P[k][n]) for n in range(r, NMAX + 1, m)]
    print("exact: A_%d(%dn+%d), n<=%d: min v3 = %d (claim %d)" % (k, m, r, NMAX, min(vs), t))
