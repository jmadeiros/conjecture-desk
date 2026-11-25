# S-4.c1 referee review: Zhang, arXiv:2610.33037v1, Conjecture 2.14 (checker: ned)

**Verdict: CONFIRMED.** I computed everything myself from the paper's definitions, using exact arithmetic. Conjecture 2.14 fails at (a,b) = (165,165). Clause 3, the interlacing Γ_{165,164} ≼ Δ_{165,165}, is the clause that fails. Clauses 1 and 2 hold there. The same verdict applies to S-6.c1, which makes the identical claim.

## 1. Definitions, taken from the paper (v1 HTML, §2 and §2.6)
- **Γ_{a,b}.** H_{(a,b)}(t) is the characteristic Chow polynomial of P_{(a,b)} = [∅,(a,b)] in generalized subword order, ranked by total size. It is defined as H = −χ̄^{-1} in the incidence algebra, and the paper also gives the chain formulas (1) and (2). Γ_{a,b} is its gamma polynomial: H_{(a,b)}(t) = (1+t)^{a+b−1} Γ_{a,b}(t/(1+t)^2).
- **Δ_{a,b}.** Δ_{a,b} = Γ_{a,b} − Γ_{a,b−1}, with Γ_{a,0} = 1. The paper states this verbatim just before Proposition 2.12.
- **≼.** "For real-rooted polynomials of degrees differing by at most one, f ≼ g when their zeros weakly interlace." There is "no orientation when the degrees are equal". Common zeros are allowed, because the interlacing is weak.
- **Wording.** The conjecture's number and wording match the claim exactly: Conjecture 2.14, "Gamma-difference Sturm property".
- **Paper's own evidence.** "Exact coefficient generation followed by numerical root checks finds no failure … for 1≤a,b≤16". It also reports that the diagonal Γ_{n,n} is Sturm for n≤24. The pair (165,165) lies far outside both ranges, so there is no red flag here.

## 2. My own computation (scripts in this folder)
- `chow_bruteforce.py` computes H straight from the definition. It enumerates the poset, computes the Möbius function, and inverts −χ̄ in the incidence algebra. It reproduces the values printed in the paper: H_{(2,2)} = 1+5t+5t²+t³, formula (10), G_2 = Γ_{3,3}, and K_3 = Γ_{4,4}.
- `chow_chain_fast.py` uses chain formulas (1) and (2), organised as 2-D prefix sums (my own layout). It agrees with the brute force for every pair with a,b ≤ 9, and it confirms formula (4).
- `gamma_kernel.py` expands the Corollary 2.6 rational kernel through its own denominator recurrence. It agrees with the chain formula on all 1600 pairs with a,b ≤ 40, and at (165,164) and (165,165).
- After my independent computation, my coefficient vectors at (165,164) and (165,165) match Astra's `counterexample.json` exactly.
- **How `exact_check.py` certifies roots.** arb root approximations are used only to choose rational test points. Each verdict then comes from exact integer sign evaluation at those points.

**Results at (165,165)** (`check_165_165.json`):
- **Clause 1 holds.** Every coefficient of Δ is ≥ 0. The only zero coefficient is the constant term.
- **Clause 2 holds.** Δ = s·h, and h has 163 sign changes on (−∞,0). So h has 163 simple negative zeros, which is all of them. Γ_{165,164} likewise has 164 simple negative zeros.
- **Clause 3 fails.** I certified the left-to-right order of the merged roots exactly. It alternates except at one spot, where the pattern is `…g p p g g p…`. Inside [−1/18, −56/1131] there are two consecutive zeros of Γ_{165,164} with no zero of Δ between them, followed by two consecutive zeros of Δ. All the zeros are distinct, so no weak interlacing is possible in either orientation.
- **Wronskian check.** I independently reproduced Astra's Wronskian values: W(0) = 164 and −5621 < W(−5/101) < −5620. W is negative only on an interval narrower than 5·10⁻⁴.

**The paper's weaker expectation also fails** (`chow_level_165_165.txt`). Γ_{165,164} and Γ_{165,165} do not interlace either; the root word again contains `ggpp`. The map s ↦ t on (−1,0) is an increasing bijection, and H_{(165,164)} has no zero at −1. So H_{(165,164)} ⋠ H_{(165,165)}, which contradicts the §6 expectation "H_{(a,b−1)} ≼ H_{(a,b)} for all a,b". That expectation is the paper's motivating open question, though it is not a numbered conjecture. H_{(165,165)} itself is still real-rooted.

## 3. Search for a smaller counterexample
- **Exhaustive band check** (`scan/band2_*.jsonl`). I checked all 818 pairs with a,b ≤ 165, |a−b| ≤ 2 and (a,b) ≠ (1,1), exactly. **The only failure is (165,165).** Every pair with a+b ≤ 329 in that band passes.
- **Wronskian screen** (`wfilter.py`, a filter, not a certificate). Over all a,b ≤ 60 it finds no sign change.
- **What is not certified.** Pairs with |a−b| ≥ 3 and a+b < 330 were not checked exhaustively; the coordinator capped the compute. So (165,165) is the smallest counterexample found, not a proven minimum.
- **External audit.** The solved-conjectures issue #190 audit reports that all a,b ≤ 45 and near-diagonal pairs through 70 pass.

## 4. Earlier resolutions
- **arXiv.** The abstract page lists only v1 (15 Oct 2026).
- **solved-conjectures.** Issue #190 is open. It holds a research reservation and the bounded positive checks above, and records no counterexample.
- **trureturing.** No matching issue.
- **GitHub.** A global issue and code search for "2610.33037" found only arXiv RSS mirrors.
- **Web.** Searches found no resolution and no citing paper.
- **Not checked.** I did not query citation indexes such as Semantic Scholar or Google Scholar.
- **Conclusion.** As far as I can tell, the counterexample is new.

## 5. Significance
- **Area and author.** Algebraic combinatorics: real-rootedness and interlacing of characteristic Chow polynomials of posets, after Ferroni–Matherne–Stevens–Vecchi. The paper is a six-week-old single-author preprint by Jiahao Zhang (Tianjin Normal University). It discloses heavy ChatGPT/Codex assistance and has no citations.
- **Who is watching.** Mainly AI-driven conjecture catalogues. It is not a known community target.
- **Sibling results.** It is related in spirit to the known failure of real-rootedness for Cohen–Macaulay posets ([7, Remark 4.26] in the paper). It is not a sibling of a recently refuted conjecture.
- **Value.** It goes beyond the conjecture: the paper's §6 two-layer interlacing expectation also fails at (165,165). The failure is a delicate near-tie at large parameters, which explains why the audits up to 16, 45 and 70 missed it. Interest is modest.
