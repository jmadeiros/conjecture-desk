# Conjecture desk: results

Results from a live desk of AI models: https://conjecture-desk.vercel.app

One model finds a target and produces a result. A model from a different company then tries to break it, reading the paper's definitions itself and writing its own programs. A result is listed here only if it survived that check.

**No human mathematician has reviewed anything in this repository.** Treat every item as a claim with its evidence attached. Corrections are welcome: open an issue.

## Results

| Folder | Claim | Depends on an unrefereed lab claim? |
|---|---|---|
| `zhang-2.14-counterexample/` | Conjecture 2.14 of Jiahao Zhang, arXiv:2610.33037v1 ("Gamma-difference Sturm property") is false: the interlacing clause fails at (a,b) = (165,165). The two-layer interlacing expectation in the paper's Section 6 fails at the same pair. | No |
| `yaqubi-mirzavaziri/` | Proofs of Conjectures 6.2, 6.3 and 6.4 of Yaqubi and Mirzavaziri, arXiv:2611.05623v1 (computer-assisted). | No |
| `mukherjee-ray-5.1/` | Proof of Conjecture 5.1 of Mukherjee and Ray (connected zero forcing on trees). | No |
| `rh-automata-remark/` | The Riemann hypothesis is equivalent to an explicit fourth-root correction in the worst-case cost of determinising a unary NFA (Deléglise–Nicolas 2019 combined with Geffert 2007 / Chrobak 1986). A short remark, not a deep result. | No (it is an equivalence) |
| `entanglement-rate/` | For odd k >= 5 the asymptotic GHZ cost of the complete Bell network on k parties is k^2/4 (for k = 5: 25/4, closing the interval [6, 25/4]). | **Yes.** It needs the exact rectangular matrix multiplication exponent stated in the Lean scope of OpenAI's November 2026 claim, which is not in their PDF. |

## The Zhang counterexample in one paragraph

With p = Gamma_{165,164} and Delta = Gamma_{165,165} - Gamma_{165,164} (both of degree 164, all zeros real and simple), two consecutive zeros of p lie in [-1/18, -56/1131] with no zero of Delta between them, followed by two consecutive zeros of Delta. So no weak interlacing is possible in either orientation. Equivalently the Wronskian W = p*Delta' - p'*Delta has W(0) = 164 > 0 and -5621 < W(-5/101) < -5620. The author checked a,b <= 16; an outside audit checked a,b <= 45 and near-diagonal pairs to 70. Among all 818 pairs with a,b <= 165 and |a-b| <= 2, (165,165) is the only failure; pairs further from the diagonal were not searched exhaustively, so it is the smallest counterexample found, not a proven minimum.

- `finder/`: the counterexample as found by GPT-6 Astra (twice, in two separate runs), with exact integer coefficients in `counterexample.json`.
- `referee/`: the independent check by Claude: `REVIEW.md`, three separate exact implementations (`chow_bruteforce.py` from the definition, `chow_chain_fast.py` from the paper's chain formulas, `gamma_kernel.py` from the rational kernel) and `exact_check.py`, which decides every sign by exact integer arithmetic.

A Lean certificate of the arithmetic is in preparation and is not included yet.

## Notes

- Review files are copied as written. Paths inside them refer to the folders where the work was first done.
- The catalogues https://github.com/1337isnot1337/solved-conjectures and https://github.com/the-omega-institute/trureturing were searched before each claim. The Zhang conjecture is issue 190 in the first, open at the time of writing.
