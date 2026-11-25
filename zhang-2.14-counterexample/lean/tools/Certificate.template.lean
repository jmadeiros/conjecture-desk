/-
  Certificate.lean
  Arithmetic certificate: Conjecture 2.14 of Jiahao Zhang, arXiv:2610.33037v1
  ("Gamma-difference Sturm property") fails at (a, b) = (165, 165).

  Core Lean 4 only (no Mathlib, no Std, no Batteries). No `sorry`, no `axiom`.
  Every computational theorem in this file is proved by `decide +kernel`, so the computation
  is carried out by the Lean kernel itself. `native_decide` is NOT used in this file.

  WHAT THIS FILE PROVES. Facts about two explicit integer coefficient lists:
    p = Γ_{165,164}(s)                        (`pCoeffs`)
    Δ = Γ_{165,165}(s) − Γ_{165,164}(s)       (`deltaCoeffs`)
  namely their degrees, the signs of their coefficients, the exact signs of their values at
  328 explicit rational points, and two values of the Wronskian p·Δ' − p'·Δ.

  WHAT THIS FILE DOES NOT PROVE. Core Lean has no real numbers, so the steps
  "sign change ⇒ real zero" (intermediate value theorem), "degree n ⇒ at most n zeros", and
  "these zero positions contradict weak interlacing" are NOT formalised here. They are
  written out in ARGUMENT.md, which names the theorems of this file that it uses.
  That the lists really are Γ_{165,164} and Γ_{165,165} − Γ_{165,164} as defined in the
  paper is checked separately, in Recompute.lean.

  The coefficient lists were copied verbatim from counterexample.json (the finder's file).
  They agree exactly with the referee's independent recomputation by
  ../referee/chow_chain_fast.py (the paper's chain formulas).
-/

-- Elaborate one declaration at a time. With the default parallel elaboration, memory used by
-- the kernel computations is held until the end of the file (peak about 4 GB instead of
-- about 0.3 GB). This option does not change what is checked.
set_option Elab.async false

namespace Zhang214

/-! ## 1. Polynomials and exact evaluation -/

/-- A polynomial with integer coefficients, stored as `[c₀, c₁, …, c_d]` (ascending powers). -/
abbrev Poly := List Int

/-- `evalQ x c` is the value at the rational number `x` of the polynomial with coefficient
list `c`, by Horner's rule `c₀ + x·(c₁ + x·(c₂ + ⋯))`, in Lean's exact rationals `Rat`. -/
def evalQ (x : Rat) : Poly → Rat
  | [] => 0
  | a :: rest => (a : Rat) + x * evalQ x rest

/-- Sign of a rational number: `1`, `-1` or `0`. -/
def sgnQ (v : Rat) : Int := if 0 < v then 1 else if v < 0 then -1 else 0

/-- Formal derivative: `[c₀, c₁, c₂, …, c_d] ↦ [1·c₁, 2·c₂, …, d·c_d]`. -/
def derivAux : Nat → Poly → Poly
  | _, [] => []
  | k, a :: rest => ((k : Int) * a) :: derivAux (k + 1) rest

def deriv (c : Poly) : Poly := derivAux 1 c.tail

/-- The Wronskian `W(x) = p(x)·g'(x) − p'(x)·g(x)`. -/
def wronskian (p g : Poly) (x : Rat) : Rat :=
  evalQ x p * evalQ x (deriv g) - evalQ x (deriv p) * evalQ x g

/-- Leading coefficient (last list entry); `0` for the empty list. -/
def lead (c : Poly) : Int := c.getLastD 0

/-! ## 2. The two polynomials (exact coefficients from counterexample.json) -/

/-- `p(s) = Γ_{165,164}(s)`, coefficients of `s^0, …, s^164`. -/
def pCoeffs : Poly := @@P_COEFFS@@

/-- `Δ(s) = Γ_{165,165}(s) − Γ_{165,164}(s)`, coefficients of `s^0, …, s^164`. -/
def deltaCoeffs : Poly := @@DELTA_COEFFS@@

/-- `h(s) = Δ(s)/s` (the constant term of `Δ` is `0`, see `delta_eq_s_mul_h`). -/
def hCoeffs : Poly := deltaCoeffs.tail

/-! ## 3. Degrees and coefficient signs -/

/-- `p` has degree exactly 164. -/
theorem p_degree : pCoeffs.length = 165 ∧ lead pCoeffs ≠ 0 := by decide +kernel

/-- `Δ` has degree exactly 164 (so `p` and `Δ` have equal degree). -/
theorem delta_degree : deltaCoeffs.length = 165 ∧ lead deltaCoeffs ≠ 0 := by decide +kernel

/-- `Δ = s · h`, and `h(0) = 164 ≠ 0`, so `Δ` has a simple zero at `s = 0`. -/
theorem delta_eq_s_mul_h : deltaCoeffs = 0 :: hCoeffs ∧ hCoeffs.head? = some 164 := by
  decide +kernel

/-- `h` has degree exactly 163. -/
theorem h_degree : hCoeffs.length = 164 ∧ lead hCoeffs ≠ 0 := by decide +kernel

/-- Every coefficient of `p` is positive. -/
theorem p_coeffs_pos : ∀ c ∈ pCoeffs, 0 < c := by decide +kernel

/-- Clause 1 of the conjecture holds here: every coefficient of `Δ` is nonnegative. -/
theorem delta_coeffs_nonneg : ∀ c ∈ deltaCoeffs, 0 ≤ c := by decide +kernel

/-! ## 4. Sample points

328 rational sample points `t₀ < t₁ < ⋯ < t₃₂₇ = 0`. Apart from `t₀ = -40000`, they are the
referee's separating points (../referee/exact_check.py). They are stored in 41 blocks of 8 only so that
each kernel computation below stays small; `sampleQ` is the whole list. -/

@@BLOCK_DEFS@@

def sampleBlocks : List (List Rat) := @@BLOCK_LIST@@

/-- All 328 sample points, in increasing order. -/
def sampleQ : List Rat := sampleBlocks.flatten

/-- `true` iff the list is strictly increasing. -/
def strictlyIncreasing : List Rat → Bool
  | a :: b :: rest => decide (a < b) && strictlyIncreasing (b :: rest)
  | _ => true

/-- The sample points are strictly increasing, there are 328 of them, and the last is `0`. -/
theorem samples_ok :
    strictlyIncreasing sampleQ = true ∧ sampleQ.length = 328 ∧ sampleQ.getLast? = some 0 := by
  decide +kernel

/-! ## 5. Signs of `p` and `h` at all sample points (exact rational arithmetic) -/

/-- Signs of the polynomial `c` at the points `xs`. -/
def signsQ (c : Poly) (xs : List Rat) : List Int := xs.map (fun x => sgnQ (evalQ x c))

theorem signsQ_flatten (c : Poly) (bs : List (List Rat)) :
    signsQ c bs.flatten = (bs.map (signsQ c)).flatten := by
  induction bs with
  | nil => rfl
  | cons b bs ih => simp [signsQ] at ih ⊢; exact ih

/-- The expected sign of `p` at each sample point, block by block. -/
def pSignBlocks : List (List Int) := @@P_SIGN_BLOCKS@@

/-- The expected sign of `h` at each sample point, block by block. -/
def hSignBlocks : List (List Int) := @@H_SIGN_BLOCKS@@

def pSigns : List Int := pSignBlocks.flatten
def hSigns : List Int := hSignBlocks.flatten

/-! One kernel computation per block and polynomial (8 evaluations each). -/

@@BLOCK_THMS@@

theorem p_sign_blocks : sampleBlocks.map (signsQ pCoeffs) = pSignBlocks := by
  simp only [sampleBlocks, List.map_cons, List.map_nil, @@P_BLOCK_REWRITES@@]
  decide +kernel

theorem h_sign_blocks : sampleBlocks.map (signsQ hCoeffs) = hSignBlocks := by
  simp only [sampleBlocks, List.map_cons, List.map_nil, @@H_BLOCK_REWRITES@@]
  decide +kernel

/-- MAIN COMPUTATION. The exact signs of `p` and of `h` at all 328 sample points
(assembled from the 82 block computations above, each checked by the kernel). -/
theorem signs_at_samples : signsQ pCoeffs sampleQ = pSigns ∧ signsQ hCoeffs sampleQ = hSigns := by
  constructor
  · rw [sampleQ, signsQ_flatten, p_sign_blocks]; rfl
  · rw [sampleQ, signsQ_flatten, h_sign_blocks]; rfl

/-! ## 6. The root word -/

/-- For consecutive entries of a sign list: does the sign differ? -/
def changes : List Int → List Bool
  | a :: b :: rest => (a != b) :: changes (b :: rest)
  | _ => []

/-- One letter per gap `(tᵢ, tᵢ₊₁)`: `p` = only p changes sign, `g` = only h (equivalently
Δ = s·h, since 0 is not inside any gap) changes sign, `none` = neither, `both` = both. -/
inductive Mark | p | g | none | both
  deriving DecidableEq, Repr

def mark : Bool → Bool → Mark
  | true, false => .p
  | false, true => .g
  | false, false => .none
  | true, true => .both

/-- The word of letters, one per gap, from the sign lists of `p` and of `h`. -/
def rootWord (sp sh : List Int) : List Mark := List.zipWith mark (changes sp) (changes sh)

def rep : Nat → List Mark → List Mark
  | 0, _ => []
  | n + 1, w => w ++ rep n w

/-- The word read off by the referee: `(p g)^140 p p g g (p g)^21 p`, 327 letters. -/
def expectedWord : List Mark := rep 140 [.p, .g] ++ [.p, .p, .g, .g] ++ rep 21 [.p, .g] ++ [.p]

theorem expectedWord_shape :
    expectedWord.length = 327 ∧
    (expectedWord.filter (· == .p)).length = 164 ∧
    (expectedWord.filter (· == .g)).length = 163 ∧
    (expectedWord.drop 280).take 4 = [.p, .p, .g, .g] := by decide +kernel

/-- `p` and `h` are nonzero at every sample point. -/
theorem samples_nonzero :
    (∀ s ∈ signsQ pCoeffs sampleQ, s ≠ 0) ∧ (∀ s ∈ signsQ hCoeffs sampleQ, s ≠ 0) := by
  rw [signs_at_samples.1, signs_at_samples.2]; decide +kernel

/-- Across the 327 gaps between consecutive sample points, `p` and `h` never change sign in
the same gap, and the pattern of sign changes is `(p g)^140 p p g g (p g)^21 p`. -/
theorem root_word :
    rootWord (signsQ pCoeffs sampleQ) (signsQ hCoeffs sampleQ) = expectedWord := by
  rw [signs_at_samples.1, signs_at_samples.2]; decide +kernel

/-! ## 7. The violating window, stated explicitly

Gaps 280 and 281 are `(-1/18, -1/20)` and `(-1/20, -56/1131)`. `p` changes sign across each
of them and `h` changes sign across neither. These facts are contained in `root_word`;
here they are also checked on their own, by direct evaluation. -/

theorem window_points :
    sampleQ[280]? = some (-1/18 : Rat) ∧ sampleQ[281]? = some (-1/20 : Rat) ∧
    sampleQ[282]? = some (-56/1131 : Rat) := by decide +kernel

/-- `p(-1/18) > 0`, `p(-1/20) < 0`, `p(-56/1131) > 0`. -/
theorem p_window :
    0 < evalQ (-1/18) pCoeffs ∧ evalQ (-1/20) pCoeffs < 0 ∧ 0 < evalQ (-56/1131) pCoeffs := by
  decide +kernel

/-- `h(-1/18) < 0`, `h(-1/20) < 0`, `h(-56/1131) < 0`; so `Δ = s·h > 0` at all three points. -/
theorem h_window :
    evalQ (-1/18) hCoeffs < 0 ∧ evalQ (-1/20) hCoeffs < 0 ∧ evalQ (-56/1131) hCoeffs < 0 := by
  decide +kernel

/-- Letters 280–283 of the computed word are `p p g g`. -/
theorem root_word_window :
    ((rootWord (signsQ pCoeffs sampleQ) (signsQ hCoeffs sampleQ)).drop 280).take 4
      = [.p, .p, .g, .g] := by
  rw [root_word]; decide +kernel

/-! ## 8. Wronskian (an independent second obstruction)

`W = p·Δ' − p'·Δ`. Weakly interlacing real-rooted polynomials have a Wronskian of constant
weak sign on the real line (ARGUMENT.md, Lemma W). Here `W(0) > 0` and `W(-5/101) < 0`. -/

theorem wronskian_at_zero : wronskian pCoeffs deltaCoeffs 0 = 164 := by decide +kernel

theorem wronskian_at_m5_101 :
    -5621 < wronskian pCoeffs deltaCoeffs (-5/101) ∧
    wronskian pCoeffs deltaCoeffs (-5/101) < -5620 := by decide +kernel

/-! ## 9. Integer-only recomputation (scaled Horner) with a proved link to `evalQ`

`homEval c X Y = Σᵢ cᵢ·X^i·Y^(d-i)` (with `d + 1 = c.length`) uses integer arithmetic only.
For `Y > 0` it equals `Y^d · c(X/Y)`, so it has the sign of `c` at `X/Y`. That link is proved
below for all inputs (`sgn_evalQ`, `signsQ_eq_signsZ`, ordinary proofs, no computation).
All 656 signs are then recomputed with integers only (`signs_at_samples_int`). This is a
second evaluation, independent of Lean's `Rat` arithmetic. -/

/-- Scaled Horner, left to right, with state `(acc, X^i)`: `acc ← acc·Y + cᵢ·X^i`. -/
def homEval (c : Poly) (X Y : Int) : Int :=
  (c.foldl (fun (st : Int × Int) ci => (st.1 * Y + ci * st.2, st.2 * X)) (0, 1)).1

/-- Reference form: `hsum X Y [c₀, …, c_d] = c₀·Y^d + X·hsum X Y [c₁, …, c_d]`,
i.e. `Σᵢ cᵢ·X^i·Y^(d-i)`. -/
def hsum (X Y : Int) : Poly → Int
  | [] => 0
  | a :: rest => a * Y ^ rest.length + X * hsum X Y rest

theorem homEval_foldl (X Y : Int) (c : Poly) (acc xp : Int) :
    c.foldl (fun (st : Int × Int) ci => (st.1 * Y + ci * st.2, st.2 * X)) (acc, xp)
      = (acc * Y ^ c.length + xp * hsum X Y c, xp * X ^ c.length) := by
  induction c generalizing acc xp with
  | nil => simp [hsum]
  | cons a rest ih =>
    simp only [List.foldl_cons, ih, hsum, List.length_cons, Int.pow_succ]
    grind

/-- The scaled Horner loop computes the reference sum, for every input. -/
theorem homEval_eq_hsum (c : Poly) (X Y : Int) : homEval c X Y = hsum X Y c := by
  simp [homEval, homEval_foldl]

/-- `Y · hsum X Y c = Y^(d+1) · c(X/Y)` in `Rat`, for every `Y ≠ 0`. -/
theorem hsum_bridge (X Y : Int) (hY : Y ≠ 0) (c : Poly) :
    (Y : Rat) * (hsum X Y c : Rat) = (Y : Rat) ^ c.length * evalQ ((X : Rat) / (Y : Rat)) c := by
  have hY' : (Y : Rat) ≠ 0 := by exact_mod_cast hY
  induction c with
  | nil => simp [hsum, evalQ]
  | cons a rest ih =>
    simp only [hsum, evalQ, List.length_cons]
    push_cast
    grind

def sgnZ (v : Int) : Int := if 0 < v then 1 else if v < 0 then -1 else 0

/-- The rational number `num / den`. -/
def toQ (pt : Int × Int) : Rat := (pt.1 : Rat) / (pt.2 : Rat)

/-- For `Y > 0`, the integer `homEval c X Y` has the same sign as `c(X/Y)`. -/
theorem sgn_evalQ (c : Poly) (X Y : Int) (hY : 0 < Y) :
    sgnQ (evalQ (toQ (X, Y)) c) = sgnZ (homEval c X Y) := by
  rw [homEval_eq_hsum]
  have e := hsum_bridge X Y (by omega) c
  have hY' : (0 : Rat) < (Y : Rat) := by exact_mod_cast hY
  have hp : (0 : Rat) < (Y : Rat) ^ c.length := Rat.pow_pos hY'
  simp only [toQ]
  generalize evalQ ((X : Rat) / (Y : Rat)) c = v at e ⊢
  generalize hsum X Y c = h at e ⊢
  have k1 : 0 < h ↔ 0 < v := by
    rw [← Rat.mul_pos_iff_of_pos_left hp, ← e, Rat.mul_pos_iff_of_pos_left hY']
    exact_mod_cast Iff.rfl
  have k2 : h < 0 ↔ v < 0 := by
    rw [← Rat.mul_neg_iff_of_pos_left hp, ← e, Rat.mul_neg_iff_of_pos_left hY']
    exact_mod_cast Iff.rfl
  unfold sgnQ sgnZ
  by_cases a : 0 < h
  · simp [a, k1.mp a]
  · by_cases b : h < 0
    · have : ¬ 0 < v := fun hv => a (k1.mpr hv)
      simp [a, b, this, k2.mp b]
    · have : ¬ 0 < v := fun hv => a (k1.mpr hv)
      have : ¬ v < 0 := fun hv => b (k2.mpr hv)
      simp [*]

/-- Signs of `c` at the points `(num, den)`, computed with integers only. -/
def signsZ (c : Poly) (pts : List (Int × Int)) : List Int :=
  pts.map (fun pt => sgnZ (homEval c pt.1 pt.2))

theorem signsZ_flatten (c : Poly) (bs : List (List (Int × Int))) :
    signsZ c bs.flatten = (bs.map (signsZ c)).flatten := by
  induction bs with
  | nil => rfl
  | cons b bs ih => simp [signsZ] at ih ⊢; exact ih

/-- The integer and rational sign lists agree whenever all denominators are positive. -/
theorem signsQ_eq_signsZ (c : Poly) (pts : List (Int × Int)) (h : ∀ pt ∈ pts, 0 < pt.2) :
    signsQ c (pts.map toQ) = signsZ c pts := by
  unfold signsQ signsZ
  rw [List.map_map]
  apply List.map_congr_left
  intro pt hpt
  exact sgn_evalQ c pt.1 pt.2 (h pt hpt)

@@IBLOCK_DEFS@@

def samplePtBlocks : List (List (Int × Int)) := @@IBLOCK_LIST@@

/-- The sample points as (numerator, denominator) pairs. -/
def samplePts : List (Int × Int) := samplePtBlocks.flatten

/-- `samplePts` describes the same rationals as `sampleQ`, with positive denominators. -/
theorem samplePts_ok : samplePts.map toQ = sampleQ ∧ ∀ pt ∈ samplePts, 0 < pt.2 := by
  decide +kernel

@@IBLOCK_THMS@@

theorem p_sign_blocks_int : samplePtBlocks.map (signsZ pCoeffs) = pSignBlocks := by
  simp only [samplePtBlocks, List.map_cons, List.map_nil, @@IP_BLOCK_REWRITES@@]
  decide +kernel

theorem h_sign_blocks_int : samplePtBlocks.map (signsZ hCoeffs) = hSignBlocks := by
  simp only [samplePtBlocks, List.map_cons, List.map_nil, @@IH_BLOCK_REWRITES@@]
  decide +kernel

/-- The same 656 signs, computed with integer arithmetic only. -/
theorem signs_at_samples_int :
    signsZ pCoeffs samplePts = pSigns ∧ signsZ hCoeffs samplePts = hSigns := by
  constructor
  · rw [samplePts, signsZ_flatten, p_sign_blocks_int]; rfl
  · rw [samplePts, signsZ_flatten, h_sign_blocks_int]; rfl

/-- `signs_at_samples` again, now derived from the integer computation and the proved
link `signsQ_eq_signsZ` instead of from rational arithmetic. -/
theorem signs_at_samples' : signsQ pCoeffs sampleQ = pSigns ∧ signsQ hCoeffs sampleQ = hSigns := by
  rw [← samplePts_ok.1, signsQ_eq_signsZ _ _ samplePts_ok.2, signsQ_eq_signsZ _ _ samplePts_ok.2]
  exact signs_at_samples_int

/-! ## 10. Everything the human argument needs, in one statement -/

/-- The complete list of machine-checked facts used by Part A of ARGUMENT.md. -/
theorem certificate :
    -- degrees: deg p = deg Δ = 164, Δ = s·h with deg h = 163 and h(0) ≠ 0
    (pCoeffs.length = 165 ∧ lead pCoeffs ≠ 0) ∧
    (deltaCoeffs.length = 165 ∧ lead deltaCoeffs ≠ 0) ∧
    (deltaCoeffs = 0 :: hCoeffs ∧ hCoeffs.head? = some 164) ∧
    (hCoeffs.length = 164 ∧ lead hCoeffs ≠ 0) ∧
    -- sample points: strictly increasing, 328 of them, ending at 0
    (strictlyIncreasing sampleQ = true ∧ sampleQ.length = 328 ∧ sampleQ.getLast? = some 0) ∧
    -- p and h never vanish at a sample point
    ((∀ s ∈ signsQ pCoeffs sampleQ, s ≠ 0) ∧ (∀ s ∈ signsQ hCoeffs sampleQ, s ≠ 0)) ∧
    -- the sign-change pattern
    rootWord (signsQ pCoeffs sampleQ) (signsQ hCoeffs sampleQ) = expectedWord ∧
    -- the window
    (sampleQ[280]? = some (-1/18 : Rat) ∧ sampleQ[281]? = some (-1/20 : Rat) ∧
      sampleQ[282]? = some (-56/1131 : Rat)) :=
  ⟨p_degree, delta_degree, delta_eq_s_mul_h, h_degree, samples_ok, samples_nonzero, root_word,
    window_points⟩

/-! ## 11. Negative tests (kept commented out so that this file compiles)

Each of the next two theorems claims the wrong sign for `p(-1/20)` (the true value is
negative, see `p_window`). Uncommenting either one makes compilation FAIL. For the `Rat`
version Lean reports "Tactic `decide` failed ... did not reduce to `isTrue` or `isFalse`";
for the integer version the kernel itself reports "(kernel) application type mismatch",
i.e. `decide (0 < homEval pCoeffs (-1) 20)` does not evaluate to `true`. See README.md. -/

-- theorem p_wrong_sign : 0 < evalQ (-1/20) pCoeffs := by decide +kernel
-- theorem p_wrong_sign_int : 0 < homEval pCoeffs (-1) 20 := by decide +kernel

end Zhang214

#print axioms Zhang214.certificate
#print axioms Zhang214.signs_at_samples'
#print axioms Zhang214.p_window
#print axioms Zhang214.h_window
#print axioms Zhang214.delta_coeffs_nonneg
#print axioms Zhang214.p_coeffs_pos
#print axioms Zhang214.wronskian_at_zero
#print axioms Zhang214.wronskian_at_m5_101
#print axioms Zhang214.root_word_window
