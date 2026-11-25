# Lean certificate: Zhang's Conjecture 2.14 fails at (165, 165)

This folder holds a Lean 4 check of the arithmetic behind the counterexample to Conjecture 2.14 ("Gamma-difference Sturm property") of Jiahao Zhang, arXiv:2610.33037v1. It also holds the short human argument that turns that arithmetic into a disproof.

**What Lean proves.** Facts about two explicit integer polynomials of degree 164:

- `p = Γ_{165,164}`
- `Δ = Γ_{165,165} − Γ_{165,164}`

The facts are their degrees, the signs of their coefficients, their exact signs at 328 rational points, and two exact values of the Wronskian `p·Δ' − p'·Δ`. Lean also recomputes both coefficient lists from formulas in the paper.

**What Lean does not prove.** Lean does not prove the statement "Conjecture 2.14 is false". Core Lean has no real numbers, so it cannot express real zeros or interlacing. The step from the checked facts to the disproof uses the intermediate value theorem, the bound on the number of zeros of a polynomial, and the definition of weak interlacing. It is written out in `ARGUMENT.md`, which names every Lean theorem it uses.

No human mathematician has reviewed this. It was produced by an AI model (Claude) and should be read as a claim with its evidence attached.

## Files

| File | Contents |
|---|---|
| `Certificate.lean` | The two polynomials as integer literals. Exact evaluation, kernel-checked sign facts, Wronskian values, and an integer-only recomputation of every sign with a proved link to the rational one. |
| `Recompute.lean` | Recomputes both coefficient lists from the paper's formulas, by two independent routes. |
| `ARGUMENT.md` | The human argument from the Lean facts to the failure of the conjecture, plus a second argument via the Wronskian. |
| `lakefile.toml`, `lean-toolchain` | Build configuration. The toolchain is pinned to Lean 4.33.0. |
| `tools/gen_cert.py`, `tools/Certificate.template.lean`, `tools/sample_points.json` | How `Certificate.lean` was generated. They are not needed to check anything. `python3 tools/gen_cert.py ../finder/counterexample.json tools/sample_points.json tools/Certificate.template.lean Certificate.lean` regenerates it byte for byte. |

## Requirements

- Lean `4.33.0` (`Lean (version 4.33.0, arm64-apple-darwin24.6.0, commit d8b18978322de05a8f3dba51ef03cf5461676c17, Release)`), installed with `elan`.
- Nothing else: core Lean only, with no Mathlib, Std or Batteries, and no downloads of any library. If the 4.33.0 toolchain is not yet installed, `elan` downloads it the first time `lake` runs.

## How to reproduce

```sh
cd lean                      # this folder
rm -rf .lake                 # start from a clean state
lake build                   # builds Certificate, then Recompute
```

`lake build` must end with `Build completed successfully`. It prints the output of the `#print axioms` lines at the end of each file (see "Axioms" below).

You can also check a single file:

```sh
lake env lean Certificate.lean
lake env lean Recompute.lean      # needs Certificate built first
```

To confirm that no proof is missing:

```sh
grep -n -w sorry *.lean      # only match: the header comment of each file saying none is used
grep -n -w admit *.lean      # no matches
grep -n '^axiom' *.lean      # no matches
```

The authoritative check is the `#print axioms` output. A missing proof would show up there as `sorryAx`.

## Every theorem and how it is checked

"Kernel" means `decide +kernel`. The Lean kernel evaluates the decision procedure itself, with exact arithmetic, and the trusted base is the same as for plain `decide`. "Proof" means an ordinary proof (induction, `simp`, `grind`, rewriting) that holds for all inputs and involves no evaluation. "native" means `native_decide`, which trusts the Lean compiler and runtime in addition to the kernel.

### Certificate.lean (namespace `Zhang214`): kernel only, no `native_decide`

| Theorem | Statement | Checked by |
|---|---|---|
| `p_degree`, `delta_degree` | `deg p = deg Δ = 164` | kernel |
| `delta_eq_s_mul_h`, `h_degree` | `Δ = s·h`, `h(0) = 164`, `deg h = 163` | kernel |
| `p_coeffs_pos` | all coefficients of `p` are `> 0` | kernel |
| `delta_coeffs_nonneg` | all coefficients of `Δ` are `≥ 0` (clause 1 holds) | kernel |
| `samples_ok` | the 328 sample points are strictly increasing and the last is `0` | kernel |
| `p_signs_blockNN`, `h_signs_blockNN` (41 + 41 theorems) | signs of `p`, `h` at the 8 points of block `NN`, in `Rat` | kernel |
| `p_sign_blocks`, `h_sign_blocks`, `signs_at_samples` | the 656 signs at all 328 points (assembled from the blocks) | rewriting + kernel |
| `samples_nonzero` | `p`, `h` are nonzero at every sample point | kernel |
| `root_word` | the sign-change word is `(p g)^140 p p g g (p g)^21 p` | kernel |
| `expectedWord_shape` | that word has 164 `p`, 163 `g`, and letters 280–283 are `p p g g` | kernel |
| `window_points` | `t_280 = −1/18`, `t_281 = −1/20`, `t_282 = −56/1131` | kernel |
| `p_window`, `h_window` | `p(−1/18) > 0`, `p(−1/20) < 0`, `p(−56/1131) > 0`; `h < 0` at all three | kernel |
| `root_word_window` | letters 280–283 of the computed word are `p p g g` | kernel |
| `wronskian_at_zero` | `W(0) = 164` | kernel |
| `wronskian_at_m5_101` | `−5621 < W(−5/101) < −5620` | kernel |
| `homEval_foldl`, `homEval_eq_hsum` | the integer scaled-Horner loop computes `Σ cᵢ X^i Y^(d−i)`, for all inputs | proof |
| `hsum_bridge`, `sgn_evalQ`, `signsQ_eq_signsZ` | for `Y > 0` the integer value has the sign of `c(X/Y)`, for all inputs | proof |
| `signsQ_flatten`, `signsZ_flatten` | list bookkeeping | proof |
| `samplePts_ok` | the integer pairs are the same rationals, with positive denominators | kernel |
| `p_signs_blockNN_int`, `h_signs_blockNN_int` (82 theorems), `signs_at_samples_int` | the same 656 signs, integers only | kernel |
| `signs_at_samples'` | `signs_at_samples`, derived from the integer computation via the proved link | proof |
| `certificate` | conjunction of every fact Part A of `ARGUMENT.md` uses | assembled from the above |

### Recompute.lean (namespace `Zhang214.Recompute`)

| Theorem | Statement | Checked by |
|---|---|---|
| `paper_closed_formulas` | five coefficients match closed formulas printed after Corollary 2.6 (`γ₁ = a(b−1)`, `γ₂`, `[s^a]Γ_{a,b} = C(b−1,a)`) | kernel |
| `diag_small_cases` | Route 1 gives `Γ_{2,2} = 1+2s`, `Γ_{3,3} = 1+6s+5s²`, `Γ_{1,2} = 1+s` | kernel |
| `route1_gamma_165_165` | the recurrence equivalent to Theorem 2.13 gives `Γ_{165,165} = p + Δ` | kernel |
| `route1_gamma_164_165` | identity (32) gives `Γ_{164,165} = p`, and the division by 2 is exact | kernel |
| `chain_small_cases` | Route 2 gives `H_(2,2) = 1+5t+5t²+t³`, `Γ_{2,3} = Γ_{3,2} = 1+4s+s²`, `Γ_{3,3} = 1+6s+5s²` | native |
| `route2_chain_formula` | the chain formulas (1), (2) over the whole interval, then the gamma expansion, give `Γ_{164,165} = Γ_{165,164} = p` and `Γ_{165,165} = p + Δ`; every division is exact | native |

The two routes are independent of each other.

- **Route 1** relies on three results of the paper: Theorem 2.13 (the diagonal generating function), identity (32), and the symmetry `Γ_{a,b} = Γ_{b,a}`. It is fully kernel-checked.
- **Route 2** relies on the paper's chain formulas (1) and (2), which group the chain formula of Ferroni–Matherne–Stevens–Vecchi [7, Theorem 4.1], and on the description of the elements of `[∅,(a,b)]`. This route is closest to the definition. It uses `native_decide`, because it is far too large for kernel evaluation. It fills about 27,000 cells `(i,j)`, each with a dozen operations on integer polynomials of degree up to 329: of the order of 10^8 big-integer operations. Route 1 needs only about 10^5 to 10^6, and the kernel already takes about 40 s for it. We did not attempt Route 2 in the kernel. Under `native_decide` it runs in Lean's interpreter in about 65 s.

The coefficient lists were also checked in Python. The finder's `counterexample.json` agrees exactly with the referee's independent recomputation by `../referee/chow_chain_fast.py` (the paper's chain formulas).

## Axioms

The `#print axioms` output from the build is:

- Most kernel-checked computational theorems report the three standard Lean axioms `propext`, `Classical.choice` and `Quot.sound`. They enter through core-library definitions and lemmas, for example the decidable order on `Rat`, and through the `simp`/`grind` proofs. Some report fewer. `delta_coeffs_nonneg`, `p_coeffs_pos`, `diag_small_cases`, `route1_gamma_165_165` and `route1_gamma_164_165` report none at all, and `paper_closed_formulas` reports only `propext`.
- `route2_chain_formula` reports `propext`, `Quot.sound` and `Zhang214.Recompute.route2_chain_formula._native.native_decide.ax_1`. The last one is the auxiliary axiom by which Lean 4.33's `native_decide` records that it trusted a compiled evaluation. No such axiom appears in `Certificate.lean`. `chain_small_cases` has the same form.
- No theorem depends on `sorryAx`. Neither file declares an `axiom`.

## What is not formalised

1. **The real-analytic step.** That a sign change gives a real zero (intermediate value theorem), that a degree-`n` polynomial has at most `n` zeros, and that the resulting zero positions contradict weak interlacing in both orientations. See `ARGUMENT.md`, Part A.
2. **The Wronskian lemma.** That weakly interlacing real-rooted polynomials of equal degree have a Wronskian of constant weak sign. It is used only for the second, independent argument (Part B). A proof is in `ARGUMENT.md`.
3. **The meaning of the Lean definitions.** For example, that `evalQ` is polynomial evaluation and `rootWord` records sign changes. These are short definitions to be read; `ARGUMENT.md` §2 lists them.
4. **The theory linking the computed lists to the paper's definition.** The paper defines `H = −χ̄^{−1}` in the incidence algebra. Lean evaluates either the paper's chain formulas (Route 2) or the paper's Theorem 2.13 with (32) and symmetry (Route 1). It does not prove that these formulas follow from the definition; that is the content of the paper and of [7]. The referee's `chow_bruteforce.py`, which computes from the definition, agrees with the chain formula for all `a, b ≤ 9`.
5. **Route 2 trusts the compiler.** Its correctness assumes the Lean compiler and runtime, not only the kernel, because it uses `native_decide`.

## Choices an expert may want to check

- **Rationals versus scaled integers.** The headline statements use Lean's core `Rat` (exact rationals), for example `0 < evalQ (-1/18) pCoeffs`, so they read directly. Every sign is computed a second time with integer arithmetic only, by scaled Horner `Σ cᵢ X^i Y^(d−i)`. The link between the two (`sgn_evalQ`) is proved for all inputs, not tested.
- **Sample points.** The sample points are the referee's separating rationals. Floating-point root approximations from `arb` were used to choose them, and `t_0` was replaced by `−40000`. Nothing depends on how they were found: Lean re-checks every sign exactly.
- **`decide +kernel` is not `native_decide`.** It skips the elaborator's own evaluation and goes straight to the kernel. For plain `decide` and for `decide +kernel` alike, the kernel is the trusted checker. Only `native_decide` adds the compiler to the trusted base.
- **`set_option Elab.async false`.** Both files set this option. With parallel elaboration, memory from the kernel computations was held until the end of the file, peaking at about 3.9 GB. Elaborating one declaration at a time brings the peak for `Certificate.lean` down to about 0.27 GB. `Recompute.lean` still peaks at about 2.2 GB. The option does not change what is checked.
- **Splitting into blocks.** The 41 blocks of 8 points exist only to keep each kernel check small. The block results are assembled into statements about the whole list by ordinary rewriting.
- **Scope of the counterexample.** No minimality is claimed for `(165,165)`. See `../referee/REVIEW.md` for the search that was done.

## Negative test

A negative test shows that the checker rejects a false sign claim. Section 11 of `Certificate.lean` contains two commented-out theorems that claim `p(−1/20) > 0`; the true value is negative:

```lean
-- theorem p_wrong_sign : 0 < evalQ (-1/20) pCoeffs := by decide +kernel
-- theorem p_wrong_sign_int : 0 < homEval pCoeffs (-1) 20 := by decide +kernel
```

Uncommenting either one makes compilation fail. We ran both as a separate file importing `Certificate`.

- The `Rat` version fails with `Tactic 'decide' failed for proposition 0 < evalQ (-1 / 20) pCoeffs because its 'Decidable' instance ... did not reduce to 'isTrue' or 'isFalse'`. After the kernel rejects the claim, `decide` reports what the elaborator's own reducer sees, and that reducer cannot unfold `Rat` arithmetic.
- The integer version fails with the kernel's own message: `(kernel) application type mismatch ... argument has type true = true but function has type decide (0 < homEval pCoeffs (-1) 20) = true → ...`. That is, the decision procedure evaluates to `false`, not `true`.
- The negation, `¬ (0 < evalQ (-1/20) pCoeffs)`, is accepted by `decide +kernel`.
- Two other false claims we tried also fail to compile: a wrong sign list for block 35 of `h`, and `0 < W(−5/101)`.

## Compile times

These were measured on an Apple Silicon Mac (arm64, macOS) with Lean 4.33.0. The machine was busy with unrelated work the whole time (load average between 5 and 37), so wall-clock times are inflated. CPU times are the better guide.

| Step | Wall clock | CPU (user) | Peak memory |
|---|---|---|---|
| `rm -rf .lake && lake build` (both files, from clean) | 2 min 34 s | 148 s | see below |
| `lean Certificate.lean` alone | 75 s | 74 s | 0.27 GB |
| `lean Recompute.lean` alone | 75 s | 73 s | 2.2 GB |

In `Recompute.lean`, the profiler attributes the time as follows:

- Route 1 (kernel): about 22 s for `route1_gamma_165_165` and 17 s for `route1_gamma_164_165`.
- Route 2 (`native_decide`): about 64 s of interpreted evaluation for `route2_chain_formula`.

The profiler figures are wall clock under load. In `Certificate.lean`, no single declaration takes more than about 12 s.

Each file compiles well inside the 10-minute limit. The build writes about 6 MB to `.lake/`.
