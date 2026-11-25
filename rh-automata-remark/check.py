"""Independent numeric checks for N-1 (unary determinization vs Landau g under RH).

1. Landau g(m) exactly (knapsack over prime powers), checked against OEIS A000793 head.
2. Brute-force D(n) for n <= 4 over all unary NFAs (single initial state, no eps),
   minimal complete DFA size, and check g(n-1) <= D(n) <= g(n-1) + n^2 - 2.
3. Endpoint numerics A -+ c from D-N's stated c.
4. a_m (D-N eq 1.9) and the window for Q_n for m up to M; size of the
   additive-term perturbation (n^2-2)/g(n-1) / ((n-1)log(n-1))^(1/4).
"""
import itertools, math, sys
import mpmath as mp

mp.mp.dps = 40

def primes_upto(N):
    s = bytearray([1]) * (N + 1); s[0] = s[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(N + 1) if s[i]]

def landau_table(N):
    # best[s] = max product of prime powers (distinct primes) with sum <= s
    best = [1] * (N + 1)
    for p in primes_upto(N):
        new = best[:]
        q = p
        while q <= N:
            for s in range(q, N + 1):
                v = best[s - q] * q
                if v > new[s]:
                    new[s] = v
            q *= p
        best = new
    return best

def min_dfa_size_unary(bits, t, p):
    """bits: membership of 1^k for k in [0, t+p) where sequence is eventually
    periodic with preperiod t and period p (as produced by subset construction).
    Returns minimal complete DFA size = minimal preperiod + minimal period."""
    L = t + p
    def val(k):
        return bits[k] if k < L else bits[t + (k - t) % p]
    # minimal period of the tail
    tail = [bits[t + i] for i in range(p)]
    pm = p
    for d in range(1, p + 1):
        if p % d == 0 and all(tail[i] == tail[i % d] for i in range(p)):
            pm = d; break
    # minimal preperiod: smallest s <= t with val(k) == val(k+pm) for all k >= s
    s = t
    while s > 0 and val(s - 1) == val(s - 1 + pm):
        s -= 1
    return s + pm

def brute_D(n):
    best = 0
    states = range(n)
    pairs = [(i, j) for i in states for j in states]
    for mask in range(1 << (n * n)):
        succ = [0] * n
        for b, (i, j) in enumerate(pairs):
            if mask >> b & 1:
                succ[i] |= 1 << j
        # subset sequence from {0}
        seen = {}
        seq = []
        S = 1
        while S not in seen:
            seen[S] = len(seq); seq.append(S)
            T = 0
            for i in states:
                if S >> i & 1:
                    T |= succ[i]
            S = T
        t = seen[S]; p = len(seq) - t
        for F in range(1 << n):
            bits = [1 if (X & F) else 0 for X in seq]
            d = min_dfa_size_unary(bits, t, p)
            if d > best:
                best = d
    return best

def li_inv(y):
    y = mp.mpf(y)
    x0 = y * mp.log(y) if y > 3 else mp.mpf(3)
    return mp.findroot(lambda x: mp.li(x) - y, x0)

def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    g = landau_table(M)
    oeis = [1, 1, 2, 3, 4, 6, 6, 12, 15, 20, 30, 30, 60, 60, 84, 105, 140, 210, 210, 420, 420]
    assert g[:len(oeis)] == oeis, g[:len(oeis)]
    print("g matches A000793 for n=0..20")

    for n in (2, 3, 4):
        D = brute_D(n)
        lo, hi = g[n - 1], g[n - 1] + n * n - 2
        print(f"n={n}: brute D(n)={D}, Geffert window [{lo}, {hi}] ok={lo <= D <= hi}")

    A = (2 - mp.sqrt(2)) / 3
    c = mp.mpf("0.046117644421509")
    print("A =", mp.nstr(A, 15), " A-c =", mp.nstr(A - c, 12), " A+c =", mp.nstr(A + c, 12))

    # a_m and the Q_n window
    amin = (None, 10); amax = (None, -10)
    worst_pert = 0
    rows = []
    for m in range(2, M + 1):
        L = mp.sqrt(li_inv(m))
        norm = (m * mp.log(m)) ** mp.mpf(0.25)
        a = (L - mp.log(g[m])) / norm
        n = m + 1
        pert = mp.log(1 + mp.mpf(n * n - 2) / g[m]) / norm  # Q_n in [a - pert, a]
        if m >= 200:
            worst_pert = max(worst_pert, pert)
        if a < amin[1]: amin = (m, a)
        if a > amax[1]: amax = (m, a)
        if m in (10, 50, 100, 200, 500, 1000, 1500, 2000, 3000, 5000, M):
            rows.append((m, a, pert))
    for m, a, pert in rows:
        print(f"m={m:5d}  a_m={mp.nstr(a, 8)}  Q_(m+1) in [a_m - {mp.nstr(pert, 3)}, a_m]")
    print("min a_m over 2..M:", amin[0], mp.nstr(amin[1], 8), "(D-N iv says > 0.11104)")
    print("max a_m over 2..M:", amax[0], mp.nstr(amax[1], 8), "(D-N iv says <= a_2 = 0.9102)")
    print("max perturbation for m>=200:", mp.nstr(worst_pert, 3))
    # shift check: sqrt(li^-1(m)) - sqrt(li^-1(m-1))
    for m in (100, 1000, M):
        print(f"shift sqrt(li^-1({m}))-sqrt(li^-1({m-1})) = {mp.nstr(mp.sqrt(li_inv(m)) - mp.sqrt(li_inv(m-1)), 5)}")

if __name__ == "__main__":
    main()
