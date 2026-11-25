#!/usr/local/bin/python3.12
"""Exact terminal-chain audit for Zhang, arXiv:2610.33037, Conjecture 2.14.

This constructs the actual composition principal intervals, counts terminal
chains using equations (1)--(2), then changes the Chow basis to the gamma basis.
It does not use the two-layer gamma recurrence in its object construction.
All coefficients and comparisons are Python integers.
"""
from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p or [0]


def add(p, q):
    r = [0] * max(len(p), len(q))
    for i, c in enumerate(p):
        r[i] += c
    for i, c in enumerate(q):
        r[i] += c
    return trim(r)


def multiply_q_integer(p, length, shift=0):
    """p(t) t^shift [length]_t, computed without division."""
    if length <= 0 or not any(p):
        return [0]
    r = [0] * (len(p) + length - 1 + shift)
    for i, c in enumerate(p):
        for j in range(length):
            r[i + j + shift] += c
    return trim(r)


def contained(alpha, beta):
    """Literal generalized-subword containment, not embedding multiplicity."""
    position = 0
    for value in alpha:
        while position < len(beta) and beta[position] < value:
            position += 1
        if position == len(beta):
            return False
        position += 1
    return True


def interval(beta):
    assert len(beta) in (1, 2) and min(beta) >= 1
    objects = [()]
    objects.extend((i,) for i in range(1, max(beta) + 1))
    if len(beta) == 2:
        objects.extend((i, j) for i in range(1, beta[0] + 1)
                       for j in range(1, beta[1] + 1))
    assert len(set(objects)) == len(objects)
    assert all(contained(a, beta) for a in objects)
    return sorted(objects, key=lambda a: (sum(a), a))


def terminal_chow(beta):
    objects = interval(beta)
    terminal = {}
    for alpha in objects[1:]:
        size = sum(alpha)
        # The chain with no nontrivial penultimate element.
        value = [1] * (size - 1) if size >= 2 else [0]
        for nu, rnu in terminal.items():
            if contained(nu, alpha):
                value = add(value, multiply_q_integer(
                    rnu, size - sum(nu) - 1, shift=1))
        terminal[alpha] = trim(value)
    result = [1]
    for value in terminal.values():
        result = add(result, [0] + value)
    degree = sum(beta) - 1
    result += [0] * (degree + 1 - len(result))
    assert result == result[::-1], (beta, result)
    assert result[0] == result[-1] == 1
    return result


def chow_to_gamma(chow):
    """Triangular integer elimination in t^k(1+t)^(degree-2k)."""
    remainder = list(chow)
    degree = len(chow) - 1
    gamma = []
    for k in range(degree // 2 + 1):
        value = remainder[k]
        gamma.append(value)
        for j in range(degree - 2*k + 1):
            remainder[k + j] -= value * comb(degree - 2*k, j)
    assert not any(remainder), remainder
    return trim(gamma)


def recurrence_table(limit):
    """Independent comparison only: equations (31)--(32)."""
    gamma = {(0, b): [1] for b in range(limit + 1)}
    gamma.update({(a, 0): [1] for a in range(limit + 1)})
    for n in range(1, limit + 1):
        gamma[1, n] = gamma[n, 1] = trim([1, n - 1])
    f = [[1], [1]]
    for k in range(2, limit + 1):
        f.append(add(f[-1], [0] + [-c for c in f[-2]]))
    for a in range(2, limit + 1):
        for b in range(2, limit + 1):
            previous = gamma[a - 1, b - 1]
            value = add(add(gamma[a - 1, b], gamma[a, b - 1]),
                        add([-c for c in previous], [0] + previous))
            if a == b:
                value = add(value, [0] + [-c for c in f[a - 1]])
            gamma[a, b] = value
    return gamma


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=8)
    parser.add_argument('--pair', type=int, nargs=2)
    parser.add_argument('--compare-agent', action='store_true')
    parser.add_argument('--output', default='gamma_terminal_audit.json')
    args = parser.parse_args()
    if args.pair:
        a, b = args.pair
        g = chow_to_gamma(terminal_chow((a, b)))
        p = chow_to_gamma(terminal_chow((a, b-1) if b > 1 else (a,)))
        delta = add(g, [-c for c in p])
        records = {'pair': [a, b], 'gamma': g, 'previous': p, 'delta': delta}
    else:
        reference = recurrence_table(args.limit)
        records = []
        for a in range(1, args.limit + 1):
            for b in range(1, args.limit + 1):
                chow = terminal_chow((a, b))
                gamma = chow_to_gamma(chow)
                assert gamma == reference[a, b], (a, b, gamma, reference[a, b])
                records.append({'a': a, 'b': b, 'chow': chow, 'gamma': gamma})
        print(f'{len(records)} direct principal intervals agree with equations (31)--(32).')
        if args.compare_agent:
            from gamma_search_agent import table
            agent_table = table(args.limit)
            for record in records:
                assert record['gamma'] == agent_table[record['a']][record['b']]
            print('All direct gamma polynomials also agree with gamma_search_agent.table.')
    Path(args.output).write_text(json.dumps(records, indent=2) + '\n')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
