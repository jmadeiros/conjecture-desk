#!/usr/bin/env python3
"""Exact sanity checks for proof.md; the universal result is proved there.

No floating-point arithmetic is used. A monotonic clock is used only for
enforcing a seven-minute runtime ceiling, never to decide a mathematical claim.
"""

from fractions import Fraction
from math import comb
from time import monotonic
import json


def balanced_total(p, q, r):
    """Direct use of the star prefix count, grouped by arm length."""
    total = q ** (p - r) * (q + 1) ** r
    total += (p - r) * q ** (p - r - 1) * (q + 1) ** r
    if r:
        total += r * q ** (p - r) * (q + 1) ** (r - 1)
    return total


def check_threshold(p, q, r):
    assert p >= 5 and q >= 2 * p * p and 0 <= r < p
    total = balanced_total(p, q, r)
    lower = q ** p + (p + r) * q ** (p - 1)
    scale = p ** p
    upper_numerator = (p * q + p + r - 1) ** p
    assert total >= lower
    assert scale * lower > upper_numerator
    assert scale * total > upper_numerator
    # R has denominator dividing p^p. Reconstruct its numerator independently
    # by subtracting the first two binomial terms.
    remainder_numerator = upper_numerator - scale * (
        q ** p + (p + r - 1) * q ** (p - 1)
    )
    assert remainder_numerator >= 0
    assert remainder_numerator < scale * q ** (p - 1)
    # The proof's geometric-series envelope is compared by cross-multiplication.
    assert remainder_numerator * (q - 2 * p) < (
        scale * 2 * p * (p - 1) * q ** (p - 1)
    )
    assert 2 * p * (p - 1) <= q - 2 * p


def main():
    start = monotonic()
    cases = 0
    binomial_bounds = 0
    for p in range(5, 201):
        for j in range(2, p + 1):
            assert 2 * comb(p, j) <= p * (p - 1) * p ** (j - 2)
            binomial_bounds += 1
        for q in (2 * p * p, 2 * p * p + 1, 4 * p * p, 10 * p * p):
            for r in range(p):
                check_threshold(p, q, r)
                cases += 1
        if monotonic() - start > 420:
            raise RuntimeError("Seven-minute runtime ceiling exceeded")

    p, n = 5, 251
    q, r = divmod(n - 1, p)
    sample_total = balanced_total(p, q, r)
    sample_upper = Fraction(n + p - 2, p) ** p
    report = {
        "status": "passed",
        "arithmetic": "integers and fractions.Fraction only",
        "threshold_cases": cases,
        "binomial_bound_cases": binomial_bounds,
        "p_range": [5, 200],
        "q_values": ["2*p*p", "2*p*p+1", "4*p*p", "10*p*p"],
        "residues": "all r=0,...,p-1",
        "example": {
            "p": p,
            "n": n,
            "balanced_star_arm_lengths": [q] * p,
            "balanced_star_total": sample_total,
            "nonstar_total_upper_bound": str(sample_upper),
            "star_coefficient_at_x_to_p": p,
            "two_hub_arm_groups": [[n - p - 1, 1], [1] * (p - 2)],
            "two_hub_coefficient_at_x_to_p": 2 * (p - 2),
        },
        "scope": "Sanity checks; proof.md supplies the universal proof.",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
