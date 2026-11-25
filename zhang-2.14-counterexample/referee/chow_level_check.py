#!/usr/bin/env python3
"""ned / S-4: does the WEAKER Chow statement H_(a,b-1) <= H_(a,b) (paper Sec. 6 expectation,
Theorems 2.7-2.10 for min<=4) survive at the counterexample?  By Lemma 2.1 and the
t -> t/(1+t)^2 branch analysis, for deg Gamma_{a,b-1} = deg Gamma_{a,b} = d with n=a+b-2,
it is equivalent to the gamma root order alpha_1<beta_1<...<alpha_d<beta_d
(p = Gamma_{a,b-1} roots alpha, q = Gamma_{a,b} roots beta), i.e. root word 'pq'*d.
Exact certification as in exact_check.analyse (word letters: p, g=q)."""
import json, sys
import exact_check as ec
d = json.load(open(sys.argv[1])); a, b = int(sys.argv[2]), int(sys.argv[3])
p = [int(c) for c in d[f"{a},{b-1}"]]; q = [int(c) for c in d[f"{a},{b}"]]
ec.PREC[0] = 256
rep = ec.analyse(p, [x + y for x, y in zip(p, q)])[0]
w = rep["root_word_left_to_right"]
print({k: rep[k] for k in ("deg_p", "deg_g", "p_real_rooted_certified", "g_real_rooted_certified", "merged_order_certified")})
print("gamma root word (s from -inf to 0), p=Gamma_{a,b-1}, g=Gamma_{a,b}:")
print(w)
print("Chow interlacing H_(a,b-1) <= H_(a,b) holds (word == 'pg'*d):", w == "pg" * (len(p) - 1))
