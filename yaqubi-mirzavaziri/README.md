# Proofs of Conjectures 6.2, 6.3 and 6.4 of Yaqubi and Mirzavaziri (arXiv:2611.05623)


Paper: Daniel Yaqubi and Madjid Mirzavaziri, "Partitions with designated summands: k-tuples and their congruences", arXiv:2611.05623v1, 3 November 2026.

## What is claimed

- **Conjecture 6.2.** For every k >= 1, the largest power of 2 dividing all B_k(4n+3) is 2^{v_2(B_k(3))}. The exceptions are k = 1 (mod 8), where it is exactly 2^2, and k = 6 (mod 8), where it is exactly 2^3. Here sum B_k(n) q^n = (f_4 f_6^2/(f_1 f_3 f_12))^k.
- **Conjecture 6.3.** For all n >= 0, A_6(12n+10) = 0 (mod 3^5), and 3^5 is the largest power of 3 dividing all of these numbers. Here sum A_k(n) q^n = (f_6/(f_1 f_2 f_3))^k.
- **Conjecture 6.4.** (a) A_3(12n+7) = A_3(12n+11) = 0 (mod 3^4). (b) A_4(6n+5) = 0 (mod 3^3) and A_7(12n+11) = 0 (mod 3^3). (c) A_8(18n+15) = 0 (mod 3^5).

The proofs are computer-assisted. Each claim is reduced to congruences for eta quotients, and Sturm's theorem turns each congruence into a finite check, which programs carry out.

## Status

These proofs were found by an AI agent on 25 Nov 2026. A second, separate AI agent rechecked each proof: it re-derived every step and wrote its own programs. No human mathematician has reviewed them. They are not formalised in Lean or any other proof assistant. Conjecture 6.1 of the same paper was proved earlier by the-omega-institute/trureturing (pull request #33580, merged 23 Nov 2026, in Lean). It is not claimed here. No earlier proof of 6.2, 6.3 or 6.4 was found on arXiv or in the public catalogues searched (the-omega-institute/trureturing, 1337isnot1337/solved-conjectures, demonstrandum-research/artifacts).

## Points a reader should know

- For 6.2, the paper's Theorems 4.3, 4.5 and 4.6 already prove most classes of k. The parts the paper does not prove are k = 0 (mod 4) and exactness for k = 1 (mod 8). Both have short elementary proofs (Lemmas 1 and 2 in conj-6.2/PROOF.md). The Sturm checks in that folder prove the paper's classes a second time.
- For 6.3, "the exact power of 3 dividing all of them" is read as the largest common power. One term is enough: A_6(22) = 6635911068 = 3^5 x 27308276. The termwise reading, that every term has 3-adic valuation exactly 5, is false at n = 0: A_6(10) = 384183 = 3^6 x 527.
- In conj-6.2, the proof file writes P for the paper's G (the series for B_k) and G for 1/F.

## Layout

- `conj-6.2/`: PROOF.md (the prover's write-up, which also covers 6.1), REVIEW.md (the referee's report), `prover/` and `referee/` programs and logs. README.md there gives the commands.
- `conj-6.3-6.4/`: the same layout for the 3-adic conjectures.

The proof and review files are copied as written. Paths inside them refer to the folders where the work was first done: `lane-b-sequences/t4_designated/` is `prover/`, and `swarm/work/B-T1/` and `swarm/work/B-T2/` are the `referee/` folders.

Requirements: Python 3.12 with numpy, and a C compiler. Total run time is under 10 minutes on a laptop.
