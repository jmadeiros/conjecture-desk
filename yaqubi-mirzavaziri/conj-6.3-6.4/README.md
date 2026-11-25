# Conjectures 6.3 and 6.4: programs and commands

- `PROOF.md`: the prover's write-up.
- `REVIEW.md`: the referee's report (verdict: confirmed-proof).

The compiler flags first used were not recorded. `cc -O2` is a reasonable choice. Commands marked "reconstructed" were rebuilt from the program's usage line and the log it produced. The coefficient dumps (`*.bin`, about 20 MB from the prover and 1.7 MB from the referee) are not included. The commands below regenerate them.

## Prover (`prover/`)

```
cd prover
cc -O2 -o pdk pdk.c
for k in 3 4 6 7 8; do ./pdk $k 1000000 7 coef_k$k.bin; done > run_3adic_1e6.log   # reconstructed; usage: pdk k N E [dumpfile]
python3 plan_3adic.py                                        # writes plan_3adic.json (levels, weights, Sturm bounds)
nice python3 prove_3adic_impl2.py > prove_3adic_impl2.log    # reads coef_k*.bin; about 5 min; last line "ALL OK"
```

## Referee (`referee/`)

```
cd referee
python3 bookkeeping.py > bookkeeping.log       # also writes bookkeeping.json
cc -O2 -o ak_ref ak_ref.c
./ak_ref 112400 40000 > full_run.log           # reconstructed; usage: ak_ref NMAX NSMALL; writes ak_k*.bin; about 30 s
python3 exact_small.py 400 > exact_small.log   # reads ak_k*.bin; exact integers for n <= 400
```

`full_run.log` contains the line "ALL SIX CLAIMS VERIFIED TO THEIR STURM RANGES".

Note: `PROOF.md` says the prover's 10^6 run covered "83,333 to 166,666 terms each". `run_3adic_1e6.log` shows 55,555 terms for 18n+15. The referee did not re-run that check, and the proof does not need it.
