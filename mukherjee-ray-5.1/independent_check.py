"""Exact independent checks for arXiv:2611.10985 Conjecture 5.1.

The proof is in proof_check.md. These finite checks are consistency checks,
not substitutes for the proof. NetworkX is used only to enumerate unlabeled
trees and find graph paths. All mathematical decisions use integers.
"""

from itertools import product
from math import prod
import networkx as nx


def literal_polynomial(graph):
    """Enumerate vertex sets, test induced connectivity, run the forcing rule."""
    n = len(graph)
    neighbors = [sum(1 << v for v in graph[u]) for u in range(n)]
    full = (1 << n) - 1
    counts = [0] * (n + 1)
    successful = []
    for initial in range(1, full + 1):
        reached = initial & -initial
        while True:
            expanded = reached
            for u in range(n):
                if reached & (1 << u):
                    expanded |= neighbors[u] & initial
            if expanded == reached:
                break
            reached = expanded
        if reached != initial:
            continue
        blue = initial
        while True:
            old = blue
            for u in range(n):
                if blue & (1 << u):
                    white = neighbors[u] & (full ^ blue)
                    if white and white & (white - 1) == 0:
                        blue |= white
            if old == blue:
                break
        if blue == full:
            counts[initial.bit_count()] += 1
            successful.append(initial)
    return counts, successful


def structural_polynomial(graph):
    """Enumerate tail-prefix choices independently of the forcing procedure."""
    branch = [u for u in graph if graph.degree(u) >= 3]
    assert branch
    stem = {branch[0]}
    for u in branch[1:]:
        stem.update(nx.shortest_path(graph, branch[0], u))
    tails = []
    owners = []
    for u in sorted(stem):
        for first in graph[u]:
            if first in stem:
                continue
            path = [first]
            previous, current = u, first
            while graph.degree(current) != 1:
                onward = [v for v in graph[current] if v != previous]
                assert len(onward) == 1
                previous, current = current, onward[0]
                path.append(current)
            owners.append(u)
            tails.append(path)
    assert len(tails) == sum(graph.degree(u) == 1 for u in graph)
    assert len(stem) + sum(map(len, tails)) == len(graph)
    counts = [0] * (len(graph) + 1)
    masks = set()
    for lengths in product(*(range(len(tail) + 1) for tail in tails)):
        empty_owners = [owner for owner, k in zip(owners, lengths) if k == 0]
        if len(empty_owners) != len(set(empty_owners)):
            continue
        chosen = set(stem)
        for tail, k in zip(tails, lengths):
            chosen.update(tail[:k])
        counts[len(chosen)] += 1
        masks.add(sum(1 << v for v in chosen))
    return counts, masks, stem, [len(tail) for tail in tails]


def check_small_trees():
    checked = 0
    subset_count = 0
    for n in range(4, 11):
        at_n = 0
        for graph in nx.nonisomorphic_trees(n):
            graph = nx.convert_node_labels_to_integers(graph)
            p = sum(graph.degree(u) == 1 for u in graph)
            if p < 3:
                continue
            literal, literal_masks = literal_polynomial(graph)
            structural, structural_masks, stem, lengths = structural_polynomial(graph)
            assert literal == structural, (n, list(graph.edges()), literal, structural)
            assert set(literal_masks) == structural_masks
            stem_mask = sum(1 << v for v in stem)
            assert all(mask & stem_mask == stem_mask for mask in literal_masks)
            total = sum(literal)
            groups = [sum(v not in stem for v in graph[u]) for u in stem]
            groups = [a for a in groups if a]
            minimum_size = len(stem) + p - len(groups)
            assert all(value == 0 for value in literal[:minimum_size])
            assert literal[minimum_size] == prod(groups)
            assert total <= prod(d + 1 for d in lengths)
            assert total * p**p <= (n - len(stem) + p)**p
            if len(stem) == 1:
                assert literal[p] == p
                assert total == prod(lengths) + sum(
                    prod(lengths[:i] + lengths[i + 1:]) for i in range(p)
                )
            checked += 1
            at_n += 1
            subset_count += (1 << n) - 1
        print(f"n={n}: {at_n} non-path unlabeled trees checked")
    print(f"TOTAL: {checked} trees; {subset_count} vertex subsets considered")


def check_threshold_arithmetic():
    checked = 0
    for p in range(5, 101):
        q = 2 * p * p
        for r in range(p):
            arms = [q + 1] * r + [q] * (p - r)
            count = prod(arms) + sum(
                prod(arms[:i] + arms[i + 1:]) for i in range(p)
            )
            n = p * q + r + 1
            assert count * p**p > (n + p - 2)**p
            assert 2 * (p - 2) > p
            checked += 1
    print(f"THRESHOLD: {checked} exact (p,r) checks, p=5..100, q=2p^2")


def check_growth_products():
    checked = 0
    for p in range(6, 501):
        maxima = []
        for c in range(1, p // 3 + 1):
            quotient, remainder = divmod(p, c)
            maxima.append(quotient ** (c - remainder) * (quotient + 1) ** remainder)
        assert all(a < b for a, b in zip(maxima, maxima[1:]))
        checked += len(maxima) - 1
    print(f"GROWTH: {checked} exact M(p,c+1)>M(p,c) checks, p=6..500")


if __name__ == "__main__":
    check_small_trees()
    check_threshold_arithmetic()
    check_growth_products()
    print("PASS: every comparison used exact integer arithmetic")
