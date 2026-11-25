#!/usr/bin/env python3
"""ned / S-4: certified scan of Conjecture 2.14 over pairs (a,b).

usage: scan.py OUT.jsonl K k MODE ARGS...
  MODE band N w     : pairs with a,b<=N and |a-b|<=w
  MODE sum  S0 S1   : pairs with S0 <= a+b <= S1, a,b>=1, (a,b)!=(1,1)
  MODE list a,b ... : explicit pairs
Job k of K takes the pairs with index % K == k (pairs sorted by (a+b, a)).
Each pair is tested exactly with exact_check.analyse (arb approximations only pick
rational test points; every verdict is by exact integer sign evaluation).
"""
import sys, json, time
import exact_check as ec
from gamma_kernel import rows


def verdict(rep):
    c1 = rep["g_nonzero"] and rep["clause1_nonneg_coeffs"]
    cert = rep.get("p_real_rooted_certified") and rep.get("g_real_rooted_certified") and rep.get("merged_order_certified")
    if not cert:
        return "uncertified", c1, None, None
    c2 = True  # h real-rooted (certified), roots negative; g = s^k h
    c3 = rep["clause3_strictly_alternating"]
    return ("pass" if (c1 and c2 and c3) else "FAIL"), c1, c2, c3


def main():
    out, K, k, mode = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    if mode == "band":
        N, w = int(sys.argv[5]), int(sys.argv[6])
        pairs = [(a, b) for a in range(1, N + 1) for b in range(1, N + 1) if abs(a - b) <= w and (a, b) != (1, 1)]
    elif mode == "sum":
        S0, S1 = int(sys.argv[5]), int(sys.argv[6])
        pairs = [(a, s - a) for s in range(S0, S1 + 1) for a in range(1, s) if (a, s - a) != (1, 1)]
    else:
        pairs = [tuple(map(int, x.split(","))) for x in sys.argv[5:]]
    pairs.sort(key=lambda t: (t[0] + t[1], t[0]))
    mine = set(pairs[i] for i in range(len(pairs)) if i % K == k)
    NA = max(a for a, _ in mine)
    NB = max(b for _, b in mine)
    f = open(out, "a")
    for a, row in rows(NA, NB):
        for b in range(1, NB + 1):
            if (a, b) not in mine:
                continue
            p = [int(c) for c in row[b - 1].coeffs()]
            G = [int(c) for c in row[b].coeffs()]
            t0 = time.time()
            for prec in (128, 1000, 4000):
                ec.PREC[0] = prec
                res = ec.analyse(p, G)
                rep = res[0]
                v = verdict(rep)
                if v[0] != "uncertified":
                    break
            rec = {"a": a, "b": b, "verdict": v[0], "clause1": v[1], "clause2": v[2], "clause3": v[3],
                   "deg_p": rep["deg_p"], "deg_g": rep["deg_g"], "nviol": rep.get("num_violations"),
                   "viol_interval": rep.get("first_violation_interval"), "prec": prec,
                   "secs": round(time.time() - t0, 2)}
            if v[0] != "pass":
                rec["rep"] = {kk: vv for kk, vv in rep.items() if kk != "root_word_left_to_right"}
                rec["word"] = rep.get("root_word_left_to_right")
            f.write(json.dumps(rec) + "\n")
            f.flush()


if __name__ == "__main__":
    main()
