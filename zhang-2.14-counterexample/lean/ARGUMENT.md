# From the Lean facts to the failure of Conjecture 2.14

This note gives the human part of the proof. The Lean files check arithmetic facts about two explicit integer coefficient lists. Core Lean has no real numbers, so the last steps cannot be stated in it: from sign changes to real zeros, and from zero positions to "not interlacing". Those steps are written out here. Every Lean theorem this note uses is named. Every classical fact it uses is stated.

## 1. The statement being refuted

The definitions are those of Jiahao Zhang, arXiv:2610.33037v1, Section 2.

- `H_(a,b)(t)` is the characteristic Chow polynomial of the interval `[∅, (a,b)]` in generalized subword order, ranked by total size. It is palindromic of degree `a+b-1`.
- `Γ_{a,b}(s)` is its gamma polynomial: `H_(a,b)(t) = (1+t)^(a+b-1) · Γ_{a,b}(t/(1+t)^2)`.
- `Δ_{a,b} = Γ_{a,b} − Γ_{a,b−1}`, with `Γ_{a,0} = 1`.
- For real-rooted polynomials whose degrees differ by at most one, `f ≼ g` means that their zeros weakly interlace. The paper adds: "without choosing an orientation when the degrees are equal".

**Conjecture 2.14.** For all `a, b ≥ 1` with `(a,b) ≠ (1,1)`, the nonzero polynomial `Δ_{a,b}` has nonnegative coefficients and only nonpositive real zeros, and `Γ_{a,b−1} ≼ Δ_{a,b}`.

**Weak interlacing for equal degrees.** Let `f` and `g` be real-rooted of the same degree `d`. List their zeros with multiplicity, `α_1 ≤ … ≤ α_d` for `f` and `β_1 ≤ … ≤ β_d` for `g`. They weakly interlace if one of the following holds:

- (O1) `α_1 ≤ β_1 ≤ α_2 ≤ β_2 ≤ … ≤ α_d ≤ β_d`
- (O2) `β_1 ≤ α_1 ≤ β_2 ≤ α_2 ≤ … ≤ β_d ≤ α_d`

The argument below rules out both orientations.

We take `(a,b) = (165,165)`, with `p = Γ_{165,164}` and `Δ = Δ_{165,165} = Γ_{165,165} − Γ_{165,164}`.

## 2. Reading the Lean definitions

All of these are in `Certificate.lean`, namespace `Zhang214`.

| Lean | Meaning |
|---|---|
| `pCoeffs`, `deltaCoeffs` | the coefficient lists `[c_0, …, c_164]` of `p` and `Δ` (ascending powers of `s`) |
| `hCoeffs` | `deltaCoeffs` without its first entry, so `h(s) = Δ(s)/s` |
| `evalQ x c` | `c_0 + x·(c_1 + x·(c_2 + ⋯))`, the value of the polynomial at the rational `x`, in Lean's exact rationals `Rat` |
| `sgnQ v` | `1`, `-1` or `0`, the sign of `v` |
| `lead c` | the last list entry, i.e. the leading coefficient |
| `sampleQ` | the 328 sample points `t_0, …, t_327` |
| `signsQ c xs` | the list of signs of `c` at the points `xs` |
| `changes l` | for each pair of neighbouring entries of `l`: do they differ? |
| `rootWord sp sh` | one letter per gap `(t_k, t_{k+1})`, `k = 0, …, 326`: `p` if only the sign of `p` changes across the gap, `g` if only the sign of `h` changes, `none` if neither does, `both` if both do |
| `expectedWord` | `(p g)^140 p p g g (p g)^21 p` |
| `deriv c`, `wronskian p g x` | the formal derivative; `p(x)·g'(x) − p'(x)·g(x)` |

Gap `k` means the open interval `(t_k, t_{k+1})`. Letter `k` of the word belongs to gap `k`.

## 3. Facts checked by Lean

All the theorems in this table are proved by `decide +kernel`. The Lean kernel itself evaluates the computation, using exact integer and rational arithmetic.

| Theorem | Content |
|---|---|
| `p_degree` | `deg p = 164` |
| `delta_degree` | `deg Δ = 164` |
| `delta_eq_s_mul_h` | `Δ = s·h` and `h(0) = 164` |
| `h_degree` | `deg h = 163` |
| `delta_coeffs_nonneg` | every coefficient of `Δ` is `≥ 0` (clause 1 holds) |
| `samples_ok` | `t_0 < t_1 < … < t_327`, there are 328 points, and `t_327 = 0` |
| `samples_nonzero` | `p(t_k) ≠ 0` and `h(t_k) ≠ 0` for every `k` |
| `root_word` | the computed word equals `expectedWord` |
| `expectedWord_shape` | `expectedWord` has 327 letters: 164 `p`, 163 `g` (so no `none` and no `both`), and letters 280 to 283 are `p p g g` |
| `window_points` | `t_280 = −1/18`, `t_281 = −1/20`, `t_282 = −56/1131` |
| `p_window`, `h_window` | the signs of `p` and `h` at those three points, evaluated directly: `p` is `+ − +` and `h` is `− − −` |
| `wronskian_at_zero` | `W(0) = 164` (used only in Part B) |
| `wronskian_at_m5_101` | `−5621 < W(−5/101) < −5620` (used only in Part B) |

`certificate` bundles every fact that Part A uses into one statement.

`signs_at_samples'` gets the same 656 signs a second way, from integer-only scaled Horner evaluation. A proved lemma, `signsQ_eq_signsZ`, links that evaluation to `evalQ`.

## 4. Classical facts used (not formalised)

- **(IVT)** If `f` is a real polynomial, `u < v`, and `f(u)·f(v) < 0`, then `f` has a zero in `(u, v)`.
- **(ROOTS)** A nonzero complex polynomial of degree `n` has exactly `n` zeros in `ℂ`, counted with multiplicity.
- **Lemma W** (proved in Section 6; used only in Part B). If `f` and `g` are real-rooted, have the same degree `d ≥ 1`, and weakly interlace, then `f·g' − f'·g` is either `≥ 0` everywhere on `ℝ` or `≤ 0` everywhere on `ℝ`.

## 5. Part A: the zeros (main argument)

**A0. Signs at the sample points.** By `samples_nonzero`, `p` and `h` are nonzero at every sample point. So a letter `p` in gap `k` means `p(t_k)·p(t_{k+1}) < 0` and `h(t_k)·h(t_{k+1}) > 0`. A letter `g` means the reverse. By `root_word` and `expectedWord_shape`, there are 164 gaps with letter `p` and 163 gaps with letter `g`, and these make up all 327 gaps.

**A1. `p` is real-rooted and its zeros are located.** Gap `k` with letter `p` contains a zero of `p`, by IVT. The gaps are pairwise disjoint, so `p` has at least 164 distinct real zeros. By `p_degree` and ROOTS, `p` has exactly 164 zeros in `ℂ` with multiplicity. Therefore:

- every zero of `p` is real and simple;
- each `p`-gap contains exactly one zero of `p`;
- no other gap and no sample point contains a zero of `p`.

In particular all zeros lie in `(−40000, 0)`.

**A2. `Δ` is real-rooted and its zeros are located.** The same argument applies to `h`, using `h_degree`: `h` has 163 real simple zeros, exactly one in each `g`-gap, and none anywhere else. By `delta_eq_s_mul_h`, `Δ = s·h` and `h(0) ≠ 0`. So the zeros of `Δ` are the 163 zeros of `h` together with a simple zero at `0`.

Consequently clause 2 of the conjecture holds at `(165,165)`: `Δ` has only nonpositive real zeros. Clause 1 holds too, by `delta_coeffs_nonneg`. Both `p` and `Δ` are real-rooted of the same degree 164 (`p_degree`, `delta_degree`). So the pair lies inside the domain on which the paper defines `≼`, and no orientation is chosen.

**A3. The window.** By `window_points`, gap 280 is `(−1/18, −1/20)` and gap 281 is `(−1/20, −56/1131)`. By `expectedWord_shape` (equivalently `root_word_window`), both letters are `p`. By A1, `p` has exactly one zero `α` in gap 280 and exactly one zero `α'` in gap 281. It has no other zero in `[−1/18, −56/1131]`, because `p(−1/20) ≠ 0`. So `α < α'` are consecutive zeros of `p`.

`Δ` has no zero in `[−1/18, −56/1131]`. By A2, a zero of `Δ` is either `0` or lies in a `g`-gap. The interval is negative. It is the union of two `p`-gaps and three sample points, and `h` does not vanish at sample points. The facts `p_window` and `h_window` confirm the signs at the three window points directly.

**A4. Contradiction.** Suppose `p ≼ Δ`. Let `α_1 < … < α_164` be the zeros of `p` (simple by A1) and `β_1 ≤ … ≤ β_164` the zeros of `Δ`. By A3, `α = α_i` and `α' = α_{i+1}` for some `i`.

- Under (O1), `α_i ≤ β_i ≤ α_{i+1}`.
- Under (O2), `α_i ≤ β_{i+1} ≤ α_{i+1}`.

Either way `Δ` has a zero in `[α, α'] ⊂ [−1/18, −56/1131]`, which contradicts A3.

Hence `Γ_{165,164} ⋠ Δ_{165,165}`: clause 3 of Conjecture 2.14 fails at `(a,b) = (165,165)`. This pair satisfies `a, b ≥ 1` and `(a,b) ≠ (1,1)`. So the conjecture is false. ∎

**What Part A needs.** The contradiction itself uses only the signs of `p` at `t_280, t_281, t_282` and the signs of `h` at all sample points. Without the other signs of `p`, A4 still goes through: `p ≼ Δ` assumes that `p` is real-rooted, IVT gives at least two zeros of `p` in the window, and any two consecutive ones among them serve as `α, α'`. The remaining signs of `p` (A1) add one thing. They show that `p` really is real-rooted, so the failure is a failure of interlacing proper, not of real-rootedness.

Letters 282–283 (`g g`, two zeros of `Δ` with no zero of `p` between them) give a second violation of the same kind.

## 6. Part B: the Wronskian (independent second argument)

Let `W = p·Δ' − p'·Δ`. By `wronskian_at_zero`, `W(0) = 164 > 0`. By `wronskian_at_m5_101`, `W(−5/101) < −5620 < 0`. Together with Lemma W, these two facts show that `p` and `Δ` do not weakly interlace in either orientation. (Real-rootedness and the equal degree 164 are part of the hypothesis `p ≼ Δ`. The degrees are also checked by `p_degree` and `delta_degree`.) Part B uses only these four Lean facts and Lemma W. It does not use the sample points.

**Proof of Lemma W.** Let `f` and `g` be real-rooted of degree `d ≥ 1` with weakly interlacing zeros, in orientation (O1) or (O2).

1. *Remove common zeros.* Merge the two zero lists into the chain (O1) or (O2). Neighbouring entries of the chain belong to different polynomials. Suppose `z` is a zero of both. All entries between an occurrence of `z` in one list and an occurrence in the other are equal to `z`, because the chain is non-decreasing. So there are two neighbouring entries, one from each list, both equal to `z`. Delete that pair. The chain still alternates between the two lists, keeps its starting list (hence its orientation), and stays non-decreasing. This divides `f` and `g` by `(x − z)`. Repeat until `f = r·f₁` and `g = r·g₁` with `f₁, g₁` having no common zero. Then `f₁, g₁` still weakly interlace in the same orientation, and both have the same degree `d₁`.

2. *The remaining chain is strict.* Suppose two neighbouring zeros of `f₁` were equal, `α_i = α_{i+1}`. The zero of `g₁` between them in the chain would be equal to them, a common zero. So all inequalities in the chain are strict: `f₁` and `g₁` have simple zeros that strictly alternate.

3. *Reduce to `f₁, g₁`.* Expanding the products gives `W[r·f₁, r·g₁] = r²·W[f₁, g₁]`. If `d₁ = 0`, then `f₁` and `g₁` are constants, so `W[f,g] ≡ 0`. Otherwise use partial fractions, valid because `f₁` has simple zeros `α_1 < … < α_{d₁}`:
   `g₁/f₁ = c + Σ_i ρ_i/(x − α_i)`, with `ρ_i = g₁(α_i)/f₁'(α_i)`.

4. *All residues have one sign.* The values `f₁'(α_i)` alternate in sign, since the zeros are simple and consecutive. Between `α_i` and `α_{i+1}` lies exactly one zero of `g₁`, and it is simple: `β_i` under (O1), `β_{i+1}` under (O2). So the values `g₁(α_i)` are nonzero and alternate in sign too. Hence every `ρ_i` is nonzero and they all have the same sign `σ`.

5. *Conclude.* Wherever `f₁ ≠ 0`, `W[f₁, g₁] = f₁²·(g₁/f₁)' = −f₁²·Σ_i ρ_i/(x − α_i)²` has sign `−σ`. By continuity `W[f₁, g₁]` has weak sign `−σ` everywhere, and so does `W[f, g] = r²·W[f₁, g₁]`. ∎

## 7. Where the two lists come from (Recompute.lean)

Part A and Part B are about the lists `pCoeffs` and `deltaCoeffs`. They show that the conjecture fails only once these lists are known to be `Γ_{165,164}` and `Γ_{165,165} − Γ_{165,164}`. `Recompute.lean` recomputes the lists from the paper's formulas, so the claim does not depend on trusting `counterexample.json`.

- **Route 1** (kernel-checked, `decide +kernel`): `route1_gamma_165_165` and `route1_gamma_164_165`. These compute `Γ_{n,n}` from the recurrence equivalent to Theorem 2.13. Multiplying (37) by `1 − Z + sZ²` gives `G_n = G_{n−1} − s·G_{n−2} + D_n − (1+s)·D_{n−1} + s·D_{n−2}`, with `D_n = Σ_k C(n,k)² s^k`. They then compute `Γ_{164,165} = (Γ_{165,165} − (s−1)·Γ_{164,164} + s·f_164)/2` from identity (32), and check that the division by 2 is exact. Route 1 relies on three results it does not prove:
  - Theorem 2.13 of the paper;
  - identity (32) of Proposition 2.11;
  - the symmetry `Γ_{165,164} = Γ_{164,165}`. Reversing compositions is a rank-preserving isomorphism `[∅,(a,b)] → [∅,(b,a)]` of generalized subword order. Corollary 2.6's kernel is also symmetric in `X, Y`.
- **Route 2** (`native_decide`, which trusts the Lean compiler): `route2_chain_formula`. It evaluates the chain formulas (1) and (2) of the paper over the interval `[∅,(a,b)]`, for every `a, b ≤ 165`, and then takes the gamma expansion. It returns `Γ_{164,165}`, `Γ_{165,164}` and `Γ_{165,165}`, which agree with the lists, and every division in the computation is checked to be exact. This route does not use Theorem 2.13, identity (32), or symmetry: it confirms `Γ_{164,165} = Γ_{165,164}` directly. It relies on two things it does not prove:
  - that formulas (1) and (2) compute the characteristic Chow polynomial `H = −χ̄^{−1}`. This is the paper's specialization of [7, Theorem 4.1]. The referee's `chow_bruteforce.py` checked it against the definition for all `a, b ≤ 9`.
  - the description of the elements below `(a,b)`: the empty composition, `(r)` for `r ≤ max(a,b)`, and `(i,j)` for `i ≤ a`, `j ≤ b`.
- `paper_closed_formulas` (kernel) spot-checks five coefficients against the closed formulas printed after Corollary 2.6. `diag_small_cases` and `chain_small_cases` check both routes against small values printed in the paper.

## 8. Summary of what is not formalised

1. IVT, ROOTS, the definition of weak interlacing, and the deduction in Part A (Sections 4–5).
2. Lemma W and the deduction in Part B (Section 6).
3. The step from Lean's definitions to their meaning: `evalQ` is polynomial evaluation, `rootWord` records sign changes, and so on. This is by reading short definitions; Section 2 lists them.
4. That the chain formulas (1), (2), or alternatively Theorem 2.13 with (32) and symmetry, really describe the paper's `Γ_{a,b}`. These are results of the paper and of [7]. Lean only evaluates them.
5. Route 2 rests on `native_decide`, so on the correctness of the Lean compiler and runtime as well as the kernel. Route 1 needs only the kernel.
