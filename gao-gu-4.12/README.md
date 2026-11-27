# Three indices refute Gao–Gu Conjecture 4.12

Let D_n(k) be the weighted Catalan number with up-step weights (2h+1)^(2k) at height h, minus the ordinary Catalan number C_n. [Gao and Gu, Conjecture 4.12](https://arxiv.org/pdf/1908.03914#page=26) predicts that for each positive integer k, the adjusted value v₂(D_n(k)) − s₂(n) always equals c + v₂(n−α), with c nonnegative, α a 2-adic integer, and s₂ the binary digit sum.

For every positive k ≡ 2 (mod 4), the same three indices n = 2, 3, 19 contradict that prediction.

## Residues

For a Dyck path, let U be its weight at k=1. This is an odd square, so U−1 is a multiple of 8. Its weight at general k is U^k, which modulo 2048 is the sum of binom(k,j)(U−1)^j for j=0,1,2,3. Thus D_n(k) modulo 2048 has a Newton binomial expansion of degree at most 3, with coefficients given by forward differences at k=0.

For the recurrence, W(0,h)=1. By splitting at the first return to h, W(m,h)=(2h+1)^(2k) times the sum of W(j,h+1)W(m−1−j,h) for 0≤j<m. Then D_n(k)=W(n,0)−C_n. The table below gives residues modulo 2048 from [check.py](check.py).

| n | k=0 | k=1 | k=2 | k=3 |
|---|---:|---:|---:|---:|
| 2 | 0 | 8 | 80 | 728 |
| 3 | 0 | 320 | 0 | 64 |
| 19 | 0 | 384 | 0 | 896 |

Forward differences give D_3(k) ≡ 64k(3k+2) (mod 1024) and D_19(k) ≡ 128k(5k−2) (mod 2048). Separately, D_2(k)=9^k−1≡16 (mod 32) for k≡2 (mod 4), so its adjusted valuation is 4−1=3 and the conjecture forces c≤3.

## Contradiction

* If k≡2 (mod 8), D_3(k) is divisible by 1024 and D_19(k) by 2048. Since s₂(3)=2 and s₂(19)=3, both adjusted valuations are at least 8. With c≤3, both indices must be congruent to α modulo 32. Their difference is only 16.
* If k≡6 (mod 8), the two residues are 512 modulo 1024 and 1024 modulo 2048 respectively. Both adjusted valuations equal 7. The valuations v₂(3−α) and v₂(19−α) would therefore be equal to a common t≥4. After dividing by 2^t both are odd 2-adic integers, whose difference is even. Thus 32 divides 19−3, again impossible.

At k=2 the adjusted values are exactly 3, 11, 8. Run `python3 check.py` for the integer values and the residue table. This proof makes no claim about k outside 2 mod 4 or about priority.

The k=2 witness was supplied to the Desk; its original attribution is not established here. The arithmetic was reproduced by two different exact recurrences. This note has not been peer reviewed or formalized in Lean.
