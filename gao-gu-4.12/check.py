from functools import cache
from math import comb

N = (2, 3, 19)

def difference(n, k, modulus=None):
    @cache
    def dyck(length, height):
        if length == 0:
            return 1
        total = (2*height+1)**(2*k) * sum(
            dyck(j, height+1) * dyck(length-1-j, height)
            for j in range(length)
        )
        return total if modulus is None else total % modulus

    result = dyck(n, 0) - comb(2*n, n)//(n+1)
    return result if modulus is None else result % modulus

def v2(x):
    assert x != 0
    return (x & -x).bit_length() - 1

exact = [difference(n, 2) for n in N]
assert exact == [80, 57344, 262020221225210556799916770024587452855383082581687788664501643846958138224055457924163584]
assert [v2(x)-n.bit_count() for n, x in zip(N, exact)] == [3, 11, 8]
table = [[difference(n, k, 2048) for k in range(4)] for n in N]
assert table == [[0, 8, 80, 728], [0, 320, 0, 64], [0, 384, 0, 896]]
for n, value, row in zip(N, exact, table):
    print(f"n={n}: k=2 difference = {value}; residues at k=0,1,2,3: {row}")
