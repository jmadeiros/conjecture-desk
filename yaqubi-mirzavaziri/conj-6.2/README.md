# Conjecture 6.2: programs and commands

- `PROOF.md`: the prover's write-up. It also covers Conjecture 6.1. No referee checked the 6.1 half, and 6.1 is not claimed here.
- `REVIEW.md`: the referee's report (verdict: confirmed-proof).

The compiler flags first used were not recorded. `cc -O2` is a reasonable choice. Commands marked "reconstructed" were rebuilt from the program's usage line and the log it produced.

## Prover (`prover/`)

```
cd prover
python3 prove_2adic.py > prove_2adic_impl1.log             # implementation 1 (numpy, mod 2^64); also writes prove_2adic_impl1.json
nice python3 prove_2adic_impl2.py > prove_2adic_impl2.log  # implementation 2 (exact integers); about 10 s; last line "ALL OK"
python3 sanity2adic.py 1200 300                            # reconstructed: direct check, k <= 300, 4n+3 < 1200; no log was saved
```

The A items in these logs are for Conjecture 6.1. The B items are for 6.2.

## Referee (`referee/`)

```
cd referee
cc -O2 -o eta2 eta2.c
python3 referee.py                         # calls ./eta2; writes referee.log; last line "ALL B-ITEMS PASS"
./eta2 direct 4003 320 > direct_k320.log   # reconstructed: B_k(4n+3) directly for k <= 320, 4n+3 <= 4003
```

Each line of `direct_k320.log` gives the minimum 2-adic valuation of B_k(4n+3) for one k. All 320 lines equal the value Conjecture 6.2 predicts.
