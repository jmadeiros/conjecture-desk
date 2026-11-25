#!/usr/bin/env python3
"""Generate Certificate.lean from counterexample.json, the sample points and a template.

Usage: python3 gen_cert.py counterexample.json sample_points.json TEMPLATE OUT.lean

The coefficient lists are copied verbatim from counterexample.json. The expected signs
written into the Lean file are computed here with exact integer arithmetic; Lean then
re-checks every one of them independently (a wrong sign here would make Lean fail).
"""
import json
import sys
from fractions import Fraction

cj = json.load(open(sys.argv[1]))
pts = [tuple(map(int, xy)) for xy in json.load(open(sys.argv[2]))]
template = open(sys.argv[3]).read()
out = sys.argv[4]

P = [int(c) for c in cj["P_coefficients"]]
D = [int(c) for c in cj["Delta_coefficients"]]
H = D[1:]
assert len(P) == 165 and len(D) == 165 and D[0] == 0
assert len(pts) == 328 and all(y > 0 for _, y in pts)
fr = [Fraction(x, y) for x, y in pts]
assert all(a < b for a, b in zip(fr, fr[1:])) and fr[-1] == 0
# every pair must be in lowest terms so that the Rat literal and the pair agree visibly
assert all(Fraction(x, y).numerator == x and Fraction(x, y).denominator == y for x, y in pts)


def hom(c, X, Y):
    acc, xp = 0, 1
    for ci in c:
        acc, xp = acc * Y + ci * xp, xp * X
    return acc


def sgn(v):
    return (v > 0) - (v < 0)


PS = [sgn(hom(P, x, y)) for x, y in pts]
HS = [sgn(hom(H, x, y)) for x, y in pts]
assert 0 not in PS and 0 not in HS


def lean_coeffs(cs, indent="  "):
    lines = []
    for i, c in enumerate(cs):
        sep = "," if i + 1 < len(cs) else ""
        lines.append(f"{indent}{c}{sep}  -- s^{i}")
    return "[\n" + "\n".join(lines) + "\n]"


def rat_lit(x, y):
    return f"{x}" if y == 1 else f"{x}/{y}"


def ilist(vs):
    return "[" + ", ".join(str(v) for v in vs) + "]"


def wrap(items, per_line, indent="  "):
    lines = []
    for k in range(0, len(items), per_line):
        lines.append(indent + ", ".join(items[k:k + per_line]))
    return "[\n" + ",\n".join(lines) + "\n]"


K = 8
NB = len(pts) // K
assert NB * K == len(pts)
names = [f"{b:02d}" for b in range(NB)]

block_defs, iblock_defs, block_thms, iblock_thms = [], [], [], []
psb, hsb = [], []
for b, nm in enumerate(names):
    chunk = pts[b * K:(b + 1) * K]
    ps, hs = PS[b * K:(b + 1) * K], HS[b * K:(b + 1) * K]
    psb.append(ilist(ps))
    hsb.append(ilist(hs))
    first = b * K
    block_defs.append(
        f"/-- t{first} … t{first + K - 1} -/\n"
        f"def block{nm} : List Rat := [" + ", ".join(rat_lit(x, y) for x, y in chunk) + "]")
    iblock_defs.append(
        f"def iblock{nm} : List (Int × Int) := [" + ", ".join(f"({x}, {y})" for x, y in chunk) + "]")
    block_thms.append(
        f"theorem p_signs_block{nm} : signsQ pCoeffs block{nm} = {ilist(ps)} := by decide +kernel\n"
        f"theorem h_signs_block{nm} : signsQ hCoeffs block{nm} = {ilist(hs)} := by decide +kernel")
    iblock_thms.append(
        f"theorem p_signs_block{nm}_int : signsZ pCoeffs iblock{nm} = {ilist(ps)} := by decide +kernel\n"
        f"theorem h_signs_block{nm}_int : signsZ hCoeffs iblock{nm} = {ilist(hs)} := by decide +kernel")


def namelist(prefix):
    items = [f"{prefix}{nm}" for nm in names]
    return wrap(items, 8)


def rewrites(fmt):
    items = [fmt.format(nm) for nm in names]
    lines = []
    for k in range(0, len(items), 6):
        lines.append("    " + ", ".join(items[k:k + 6]))
    return "\n" + ",\n".join(lines)


text = (template
        .replace("@@P_COEFFS@@", lean_coeffs(P))
        .replace("@@DELTA_COEFFS@@", lean_coeffs(D))
        .replace("@@BLOCK_DEFS@@", "\n".join(block_defs))
        .replace("@@BLOCK_LIST@@", namelist("block"))
        .replace("@@IBLOCK_DEFS@@", "\n".join(iblock_defs))
        .replace("@@IBLOCK_LIST@@", namelist("iblock"))
        .replace("@@P_SIGN_BLOCKS@@", wrap(psb, 3))
        .replace("@@H_SIGN_BLOCKS@@", wrap(hsb, 3))
        .replace("@@BLOCK_THMS@@", "\n".join(block_thms))
        .replace("@@IBLOCK_THMS@@", "\n".join(iblock_thms))
        .replace("@@P_BLOCK_REWRITES@@", rewrites("p_signs_block{}"))
        .replace("@@H_BLOCK_REWRITES@@", rewrites("h_signs_block{}"))
        .replace("@@IP_BLOCK_REWRITES@@", rewrites("p_signs_block{}_int"))
        .replace("@@IH_BLOCK_REWRITES@@", rewrites("h_signs_block{}_int")))
assert "@@" not in text
open(out, "w").write(text)
print("wrote", out, len(text), "bytes;", NB, "blocks")
