"""Independent exact Dyck-walk check of Conjecture 3.14, arXiv:2609.38084.

Uses Corollary 3.13: [t^i] Pnest_n = H(n,2i-1)+H(n,2i),
where H(n,h) counts Dyck paths of semilength n and exact height h.
Dynamic programming is by individual up/down steps; no reflection formula.
All decisions use integers. Runs stop after a strict counterexample.
"""
from __future__ import annotations

import argparse
import json
import time


def bounded_dyck(n: int, cap: int) -> int:
    """Number of nonnegative +/-1 walks, 2*n steps, 0 to 0, height <= cap."""
    if cap < 0:
        return 0
    counts = [0] * (cap + 1)
    counts[0] = 1
    for step in range(2 * n):
        following = [0] * (cap + 1)
        # Only heights with parity step can occur. Discard heights that
        # cannot return to zero in the remaining number of steps.
        upper = min(cap, step, 2 * n - step)
        for height in range(step % 2, upper + 1, 2):
            count = counts[height]
            if height:
                following[height - 1] += count
            if height < cap:
                following[height + 1] += count
        counts = following
    return counts[0]


def verify_triplet(n: int, i: int) -> dict:
    degree = (n + 1) // 2
    caps = [2 * i - 4, 2 * i - 2, 2 * i, 2 * i + 2]
    cumulative = [bounded_dyck(n, cap) for cap in caps]
    coefficients = [cumulative[j + 1] - cumulative[j] for j in range(3)]
    left = coefficients[1] ** 2 * i * (degree - i)
    right = coefficients[0] * coefficients[2] * (i + 1) * (degree - i + 1)
    return {
        'n': n, 'i': i, 'degree': degree,
        'coefficients': coefficients,
        'left': left, 'right': right,
        'violation': left < right,
        'method': 'individual-step bounded Dyck walk dynamic programming',
    }


def search_n(n: int, max_i: int) -> dict | None:
    degree = (n + 1) // 2
    maximum = min(max_i, degree - 1)
    cumulative = [bounded_dyck(n, 2 * j) for j in range(maximum + 2)]
    coefficients = [0] + [cumulative[j] - cumulative[j - 1]
                            for j in range(1, maximum + 2)]
    for i in range(2, maximum + 1):
        left = coefficients[i] ** 2 * i * (degree - i)
        right = coefficients[i - 1] * coefficients[i + 1] * (i + 1) * (degree - i + 1)
        if left < right:
            return {'n': n, 'i': i, 'degree': degree,
                    'coefficients': coefficients[i - 1:i + 2],
                    'left': left, 'right': right, 'violation': True,
                    'method': 'individual-step bounded Dyck walk dynamic programming'}
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int)
    parser.add_argument('--i', type=int)
    parser.add_argument('--max-i', type=int, default=45)
    parser.add_argument('--output', default='peak_dp_certificate.json')
    args = parser.parse_args()
    started = time.monotonic()
    ns = [args.n] if args.n else [201, 250, 300, 400, 600, 800, 1000]
    for n in ns:
        result = verify_triplet(n, args.i) if args.i else search_n(n, args.max_i)
        print(f'n={n}, violation={bool(result and result["violation"])}, '
              f'elapsed={time.monotonic()-started:.2f}s', flush=True)
        if result and result['violation']:
            with open(args.output, 'w') as stream:
                json.dump(result, stream, indent=2)
                stream.write('\n')
            print(json.dumps(result), flush=True)
            return
    print('No violation in the stated finite search.', flush=True)


if __name__ == '__main__':
    main()
