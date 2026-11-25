/-
  Recompute.lean
  Recomputes the two coefficient lists of Certificate.lean from formulas in Zhang's paper
  (arXiv:2610.33037v1), so that the certificate does not rest on counterexample.json.

  Route 1, kernel-checked (`decide +kernel`):
    the diagonal generating function (Theorem 2.13), the diagonal defect identity (32) of
    Proposition 2.11, and the symmetry Γ_{a,b} = Γ_{b,a}. These are results proved in the
    paper; this file uses them, it does not re-prove them.

  Route 2, `native_decide` (trusts the Lean compiler and runtime, not only the kernel):
    the chain formulas (1) and (2) of the paper for the characteristic Chow polynomials
    H_(a,b)(t), summed over the interval [∅, (a,b)] (all one-part compositions (r) with
    r ≤ max(a,b) and all two-part compositions (i,j) with i ≤ a, j ≤ b), followed by the
    gamma expansion H_(a,b)(t) = (1+t)^(a+b-1) Γ_{a,b}(t/(1+t)^2).
    This route is closest to the paper's definition. It uses no generating function.

  Core Lean 4 only. No `sorry`, no `axiom`.
-/
import Certificate

set_option Elab.async false  -- see the note at the top of Certificate.lean

namespace Zhang214.Recompute
open Zhang214

/-! ## Polynomial arithmetic on coefficient lists (ascending powers of s) -/

def addP : Poly → Poly → Poly
  | [], q => q
  | p, [] => p
  | a :: p, b :: q => (a + b) :: addP p q

def negP (p : Poly) : Poly := p.map (fun a => -a)
def subP (p q : Poly) : Poly := addP p (negP q)
/-- multiplication by `s` -/
def mulS (p : Poly) : Poly := 0 :: p
/-- remove zero leading coefficients (trailing zeros of the list) -/
def trimP (p : Poly) : Poly := (p.reverse.dropWhile (· == 0)).reverse

/-! ## Consistency with three closed formulas printed in the paper (kernel-checked)

After Corollary 2.6 the paper gives, for `1 ≤ a ≤ b`: `γ₁ = a(b-1)`,
`γ₂ = C(a,2)·C(b-1,2) + C(a,3) + C(a-1,2)`, and `[s^a] Γ_{a,b} = C(b-1,a)`.
For `p = Γ_{164,165}` (= `Γ_{165,164}`) and for `Γ_{165,165} = p + Δ` these give the values
below. This is only a spot check of five coefficients; the full lists are recomputed by the
two routes that follow. -/

/-- `C(n,2)` and `C(n,3)`. -/
def choose2 (n : Int) : Int := n * (n - 1) / 2
def choose3 (n : Int) : Int := n * (n - 1) * (n - 2) / 6

theorem paper_closed_formulas :
    -- (a,b) = (164,165): γ₁ = 164·164, γ₂ = C(164,2)·C(164,2) + C(164,3) + C(163,2), [s^164] = C(164,164) = 1
    pCoeffs[1]? = some (164 * 164) ∧
    pCoeffs[2]? = some (choose2 164 * choose2 164 + choose3 164 + choose2 163) ∧
    pCoeffs[164]? = some 1 ∧
    -- (a,b) = (165,165): γ₁ = 165·164, γ₂ = C(165,2)·C(164,2) + C(165,3) + C(164,2)
    (addP pCoeffs deltaCoeffs)[1]? = some (165 * 164) ∧
    (addP pCoeffs deltaCoeffs)[2]? = some (choose2 165 * choose2 164 + choose3 165 + choose2 164) := by
  decide +kernel

/-! ## Route 1: the diagonal recurrences (kernel-checked)

Theorem 2.13: `Σ_n Γ_{n,n} Z^n = (1-Z)(1-sZ)/(1-Z+sZ²) · Σ_n D_n Z^n` with
`D_n(s) = Σ_k C(n,k)² s^k` and `Γ_{0,0} = 1`. Multiplying by `1 - Z + sZ²` and comparing
coefficients of `Z^n` gives, with `G_n = Γ_{n,n}`,
  `G_n = G_{n-1} - s·G_{n-2} + D_n - (1+s)·D_{n-1} + s·D_{n-2}`,   `G_0 = G_1 = 1`.
Identity (32): for `a ≥ 2`, `Γ_{a,a} - 2Γ_{a-1,a} - (s-1)Γ_{a-1,a-1} = -s·f_{a-1}`, where
`f_0 = f_1 = 1`, `f_m = f_{m-1} - s·f_{m-2}`. Hence
  `Γ_{a-1,a} = (Γ_{a,a} - (s-1)·Γ_{a-1,a-1} + s·f_{a-1}) / 2`,
and `Γ_{a,a-1} = Γ_{a-1,a}` by symmetry. -/

/-- Pascal: binomial row `n` ↦ row `n+1`. -/
def nextRow (r : List Int) : List Int := addP (0 :: r) r

/-- State at index `n`: binomial row `n`, `D_n`, `D_{n-1}`, `G_n`, `G_{n-1}`, `f_n`, `f_{n-1}`. -/
structure Diag where
  row : List Int
  d0 : Poly
  d1 : Poly
  g0 : Poly
  g1 : Poly
  f0 : Poly
  f1 : Poly

/-- Index `n` ↦ index `n+1`. -/
def Diag.step (st : Diag) : Diag :=
  let row := nextRow st.row
  let D := row.map (fun c => c * c)
  -- G_{n+1} = G_n - s·G_{n-1} + D_{n+1} - (D_n + s·D_n) + s·D_{n-1}
  let G := addP (subP st.g0 (mulS st.g1)) (addP (subP D (addP st.d0 (mulS st.d0))) (mulS st.d1))
  -- f_{n+1} = f_n - s·f_{n-1}
  let f := subP st.f0 (mulS st.f1)
  { row := row, d0 := D, d1 := st.d0, g0 := G, g1 := st.g0, f0 := f, f1 := st.f0 }

/-- The state at index `n = 1`: row `[1,1]`, `D_1 = 1+s`, `D_0 = 1`, `G_1 = G_0 = 1`, `f_1 = f_0 = 1`. -/
def diagInit : Diag :=
  { row := [1, 1], d0 := [1, 1], d1 := [1], g0 := [1], g1 := [1], f0 := [1], f1 := [1] }

/-- `diagAt k` is the state at index `n = k + 1`. -/
def diagAt : Nat → Diag
  | 0 => diagInit
  | k + 1 => (diagAt k).step

/-- `Γ_{n,n}` for `n ≥ 1`. -/
def gammaDiag (n : Nat) : Poly := trimP (diagAt (n - 1)).g0

/-- `2·Γ_{n-1,n} = Γ_{n,n} - (s-1)·Γ_{n-1,n-1} + s·f_{n-1}`, for `n ≥ 2`. -/
def twiceGammaBelow (n : Nat) : Poly :=
  let st := diagAt (n - 1)
  addP (subP st.g0 (subP (mulS st.g1) st.g1)) (mulS st.f1)

def allEven (p : Poly) : Bool := p.all (fun a => a % 2 == 0)
def halve (p : Poly) : Poly := p.map (fun a => a / 2)

/-- Small cases against values printed in the paper: `Γ_{2,2} = 1 + 2s`
(that is, `H_(2,2) = 1 + 5t + 5t² + t³`), `Γ_{3,3} = 1 + 6s + 5s²`, `Γ_{1,2} = 1 + s`. -/
theorem diag_small_cases :
    gammaDiag 2 = [1, 2] ∧ gammaDiag 3 = [1, 6, 5] ∧
    trimP (halve (twiceGammaBelow 2)) = [1, 1] := by decide +kernel

/-- Route 1, diagonal: `Γ_{165,165} = p + Δ`, i.e. `Δ = Γ_{165,165} − Γ_{165,164}` once
`p = Γ_{165,164}` (next theorem). -/
theorem route1_gamma_165_165 : gammaDiag 165 = trimP (addP pCoeffs deltaCoeffs) := by
  decide +kernel

/-- Route 1, just below the diagonal: `Γ_{164,165} = p` (and `Γ_{165,164} = Γ_{164,165}` by
symmetry). The division by 2 is exact. -/
theorem route1_gamma_164_165 :
    allEven (twiceGammaBelow 165) = true ∧ trimP (halve (twiceGammaBelow 165)) = pCoeffs := by
  decide +kernel

/-! ## Route 2: the chain formulas (1), (2) of the paper (`native_decide`)

`R_α = [|α|-1]_t + t · Σ_{∅<ν<α} R_ν · [|α|-|ν|-1]_t`              (2)
`H_β = 1 + t · Σ_{∅<α≤β} R_α`                                      (1)
with `[d]_t = 1 + t + ⋯ + t^(d-1)` for `d ≥ 1` and `[d]_t = 0` for `d ≤ 0`.
Below `(a,b)` the nonempty elements are `(r)`, `1 ≤ r ≤ max(a,b)`, and `(i,j)`, `i ≤ a`, `j ≤ b`.
The sums over `ν` are organised with prefix sums, using `(1-t)·[d]_t = 1 - t^d`. Every
division by `t` or by `1 - t` below is checked to be exact (flag `ok`). -/

abbrev APoly := Array Int

@[inline] def cf (p : APoly) (i : Nat) : Int := p.getD i 0

def padd (p q : APoly) : APoly := Id.run do
  let n := max p.size q.size
  let mut r : APoly := Array.mkEmpty n
  for i in [0:n] do
    r := r.push (cf p i + cf q i)
  return r

def psub (p q : APoly) : APoly := Id.run do
  let n := max p.size q.size
  let mut r : APoly := Array.mkEmpty n
  for i in [0:n] do
    r := r.push (cf p i - cf q i)
  return r

/-- multiplication by `t^k` -/
def pshift (k : Nat) (p : APoly) : APoly := (Array.replicate k (0 : Int)) ++ p

/-- `[k]_t` (the zero polynomial for `k = 0`) -/
def qint (k : Nat) : APoly := Array.replicate k 1

/-- Division by `1 - t`: quotient coefficients are the partial sums; the remainder is the
full sum, which must be `0`. -/
def divOneMinusT (p : APoly) : APoly × Bool := Id.run do
  let mut q : APoly := Array.mkEmpty p.size
  let mut acc : Int := 0
  for i in [0:p.size] do
    acc := acc + cf p i
    q := q.push acc
  return (q.pop, acc == 0)

/-- Division by `t`: the constant term must be `0`. -/
def divT (p : APoly) : APoly × Bool := (p.extract 1 p.size, cf p 0 == 0)

/-- `H_(i,j)(t)` for the pairs `(i,j)` in `want`, all `i ≤ A`, `j ≤ B`, from (1) and (2);
the flag is `true` iff every division was exact. -/
def chainH (A B : Nat) (want : List (Nat × Nat)) : Bool × Array (Nat × Nat × APoly) := Id.run do
  let M := max A B
  let mut ok := true
  -- one-part compositions: R1[r] = R_(r);  P1[r] = Σ_{r'≤r} R1[r'];  V[r] = Σ_{r'≤r} R1[r']·t^(r-r')
  let mut R1 : Array APoly := #[#[]]
  let mut P1 : Array APoly := #[#[]]
  let mut V : Array APoly := #[#[]]
  for r in [1:M+1] do
    -- (2) for α = (r):  Σ_{r'<r} R_(r')·[r-r'-1]_t = (P1[r-1] - V[r-1]) / (1-t)
    let (q, ok1) := divOneMinusT (psub P1[r-1]! V[r-1]!)
    ok := ok && ok1
    let R := padd (qint (r - 1)) (pshift 1 q)
    R1 := R1.push R
    P1 := P1.push (padd P1[r-1]! R)
    V := V.push (padd (pshift 1 V[r-1]!) R)
  -- two-part compositions, row by row:
  --   S[i][j] = Σ_{k≤i, l≤j} R_(k,l),   U[i][j] = Σ_{k≤i, l≤j} R_(k,l)·t^(i+j-k-l)
  let mut out : Array (Nat × Nat × APoly) := #[]
  let mut Sprev : Array APoly := Array.replicate (B + 1) #[]
  let mut Uprev : Array APoly := Array.replicate (B + 1) #[]
  for i in [1:A+1] do
    let mut Scur : Array APoly := Array.replicate (B + 1) #[]
    let mut Ucur : Array APoly := Array.replicate (B + 1) #[]
    for j in [1:B+1] do
      let m := i + j
      let Mx := max i j
      let mn := min i j
      -- the same sums over (k,l) ≤ (i,j) with (k,l) ≠ (i,j)
      let Sstr := psub (padd Sprev[j]! Scur[j-1]!) Sprev[j-1]!
      let Ustr := psub (padd (pshift 1 Uprev[j]!) (pshift 1 Ucur[j-1]!)) (pshift 2 Uprev[j-1]!)
      -- Σ_{(k,l)<(i,j)} R_(k,l)·[m-k-l-1]_t = (Sstr - Ustr/t) / (1-t)
      let (u, ok1) := divT Ustr
      let (two, ok2) := divOneMinusT (psub Sstr u)
      -- Σ_{r≤Mx} R_(r)·[m-r-1]_t = (P1[Mx] - t^(mn-1)·V[Mx]) / (1-t)
      let (one, ok3) := divOneMinusT (psub P1[Mx]! (pshift (mn - 1) V[Mx]!))
      ok := ok && ok1 && ok2 && ok3
      -- (2) for α = (i,j)
      let R := padd (qint (m - 1)) (pshift 1 (padd one two))
      Scur := Scur.set! j (padd R Sstr)
      Ucur := Ucur.set! j (padd R Ustr)
      -- (1) for β = (i,j)
      if want.contains (i, j) then
        out := out.push (i, j, padd #[1] (pshift 1 (padd P1[Mx]! Scur[j]!)))
    Sprev := Scur
    Uprev := Ucur
  return (ok, out)

/-- Binomial row `n`: `C(n,0), …, C(n,n)`. -/
def binomRow (n : Nat) : Array Int := Id.run do
  let mut r : Array Int := #[1]
  for k in [0:n] do
    r := r.push (r[k]! * ((n - k : Nat) : Int) / ((k + 1 : Nat) : Int))
  return r

/-- Gamma polynomial of `H` of degree `n`: peel off `γ_i·t^i·(1+t)^(n-2i)` for
`i = 0, …, ⌊n/2⌋`. The flag is `true` iff nothing is left over (so `H` is palindromic and
the expansion is exact). -/
def gammaOf (H : APoly) (n : Nat) : List Int × Bool := Id.run do
  let mut rem : Array Int := Array.ofFn (n := n + 1) (fun i => cf H i.val)
  let mut g : Array Int := #[]
  for i in [0:n/2+1] do
    let gi := rem[i]!
    g := g.push gi
    let row := binomRow (n - 2 * i)
    for k in [0:n-2*i+1] do
      rem := rem.set! (i + k) (rem[i + k]! - gi * row[k]!)
  return (trimP g.toList, H.size ≤ n + 1 && rem.all (· == 0))

/-- `(all divisions exact, [(a, b, Γ_{a,b})])` for the requested pairs. -/
def gammaChain (A B : Nat) (want : List (Nat × Nat)) : Bool × List (Nat × Nat × Poly) :=
  let (ok, hs) := chainH A B want
  hs.foldl (fun acc (a, b, H) =>
    let (g, ok') := gammaOf H (a + b - 1)
    (acc.1 && ok', acc.2 ++ [(a, b, g)])) (ok, [])

/-- Small cases against values in the paper: `H_(2,2) = 1 + 5t + 5t² + t³`;
`Γ_{2,3} = Γ_{3,2} = 1 + 4s + s²` and `Γ_{3,3} = 1 + 6s + 5s²` (from the coefficient
formulas after Corollary 2.6). -/
theorem chain_small_cases :
    (chainH 2 2 [(2, 2)]).2.toList.map (fun x => x.2.2.toList) = [[1, 5, 5, 1]] ∧
    gammaChain 3 3 [(2, 3), (3, 2), (3, 3)] =
      (true, [(2, 3, [1, 4, 1]), (3, 2, [1, 4, 1]), (3, 3, [1, 6, 5])]) := by
  native_decide

/-- Route 2: from the chain formulas, `Γ_{164,165} = Γ_{165,164} = p` and
`Γ_{165,165} = p + Δ`, with every division exact. -/
theorem route2_chain_formula :
    gammaChain 165 165 [(164, 165), (165, 164), (165, 165)] =
      (true, [(164, 165, pCoeffs), (165, 164, pCoeffs),
              (165, 165, trimP (addP pCoeffs deltaCoeffs))]) := by
  native_decide

end Zhang214.Recompute

#print axioms Zhang214.Recompute.paper_closed_formulas
#print axioms Zhang214.Recompute.diag_small_cases
#print axioms Zhang214.Recompute.route1_gamma_165_165
#print axioms Zhang214.Recompute.route1_gamma_164_165
#print axioms Zhang214.Recompute.chain_small_cases
#print axioms Zhang214.Recompute.route2_chain_formula
