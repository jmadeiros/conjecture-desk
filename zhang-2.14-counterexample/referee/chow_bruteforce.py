#!/usr/bin/env python3
"""ned / S-4: characteristic Chow polynomial H_beta(t) straight from the paper's DEFINITION.

Zhang, arXiv:2610.33037v1, Section 2:
  * composition poset, generalized subword order: alpha <= beta iff there are
    indices i_1<...<i_r with a_j <= b_{i_j};
  * P_beta = [empty, beta], ranked by total size;
  * chi_xy(t) = sum_{x<=u<=y} mu(x,u) t^{rho(y)-rho(u)};
    chibar_xy = chi_xy/(t-1) if x<y, and -1 if x=y;
  * H = -chibar^{-1} (incidence-algebra inverse); H_beta = H(empty, beta).
Nothing here uses the paper's chain formula, kernels or generating functions.
Polynomials are lists of Python ints, ascending powers.
"""
import itertools, sys


def leq(alpha, beta):
    """generalized subword order, greedy leftmost embedding"""
    j = 0
    for a in alpha:
        while j < len(beta) and beta[j] < a:
            j += 1
        if j == len(beta):
            return False
        j += 1
    return True


def interval(beta):
    """all compositions alpha <= beta (enumerate subsequences and part sizes)"""
    out = set()
    k = len(beta)
    for r in range(k + 1):
        for idx in itertools.combinations(range(k), r):
            for parts in itertools.product(*[range(1, beta[i] + 1) for i in idx]):
                out.add(tuple(parts))
    assert all(leq(a, beta) for a in out)
    return sorted(out, key=lambda c: (sum(c), c))


def padd(p, q):
    n = max(len(p), len(q))
    r = [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    return r


def pmul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        if x:
            for j, y in enumerate(q):
                r[i + j] += x * y
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    return r


def div_t_minus_1(p):
    """exact division by (t-1); asserts remainder 0"""
    # synthetic division by root 1, from the top
    n = len(p) - 1
    q = [0] * n
    carry = 0
    for i in range(n, 0, -1):
        carry = p[i] + carry
        q[i - 1] = carry
    assert p[0] + carry == 0, "not divisible by t-1"
    return q if q else [0]


def chow_H(beta):
    P = interval(beta)
    n = len(P)
    pos = {x: i for i, x in enumerate(P)}
    rank = [sum(x) for x in P]
    le = [[leq(P[i], P[j]) for j in range(n)] for i in range(n)]
    # Moebius function mu(i,j)
    mu = [[0] * n for _ in range(n)]
    for i in range(n):
        mu[i][i] = 1
        for j in range(n):  # P sorted by rank, so linear extension
            if j != i and le[i][j]:
                mu[i][j] = -sum(mu[i][k] for k in range(n) if le[i][k] and le[k][j] and k != j)
    # graded check: every cover raises rank by 1
    for i in range(n):
        for j in range(n):
            if i != j and le[i][j]:
                between = [k for k in range(n) if k not in (i, j) and le[i][k] and le[k][j]]
                if not between:
                    assert rank[j] == rank[i] + 1, ("not graded by size", P[i], P[j])
    top = pos[tuple(beta)]

    def chibar(x, y):
        if x == y:
            return [-1]
        chi = [0] * (rank[y] - rank[x] + 1)
        for u in range(n):
            if le[x][u] and le[u][y]:
                chi[rank[y] - rank[u]] += mu[x][u]
        return div_t_minus_1(chi)

    # H = -chibar^{-1}:  sum_{x<=u<=y} chibar(x,u) H(u,y) = -delta(x,y)
    # => H(y,y)=1, H(x,y) = sum_{x<u<=y} chibar(x,u) H(u,y)
    H = {top: [1]}
    for x in sorted([i for i in range(n) if le[i][top] and i != top], key=lambda i: -rank[i]):
        acc = [0]
        for u in range(n):
            if u != x and le[x][u] and le[u][top]:
                acc = padd(acc, pmul(chibar(x, u), H[u]))
        H[x] = acc
    return H[pos[()]]


def gamma_of(H, deg):
    """unique gamma expansion H = sum g_i t^i (1+t)^(deg-2i); asserts exactness"""
    from math import comb
    rem = list(H) + [0] * (deg + 1 - len(H))
    g = []
    for i in range(deg // 2 + 1):
        gi = rem[i]
        g.append(gi)
        for k in range(deg - 2 * i + 1):
            rem[i + k] -= gi * comb(deg - 2 * i, k)
    assert all(v == 0 for v in rem), "not palindromic / gamma expansion failed"
    while len(g) > 1 and g[-1] == 0:
        g.pop()
    return g


if __name__ == "__main__":
    import json
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    res = {}
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            H = chow_H((a, b))
            res[f"{a},{b}"] = {"H": H, "Gamma": gamma_of(H, a + b - 1)}
    for b in range(1, 2 * N + 1):
        H = chow_H((b,))
        res[f"{b},0"] = {"H": H, "Gamma": gamma_of(H, b - 1)}
    json.dump(res, open(sys.argv[2] if len(sys.argv) > 2 else "bruteforce_small.json", "w"))
    print("H(2,2) =", res["2,2"]["H"])
    print("H(1,3) =", res["1,3"]["H"], " Gamma(1,3) =", res["1,3"]["Gamma"])
    print("Gamma(3,3) =", res["3,3"]["Gamma"], "Gamma(4,4) =", res["4,4"]["Gamma"])
