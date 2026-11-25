"""Exact certificate for Zhang, arXiv:2610.33037v1, Conjecture 2.14.

Uses only Python integers and the paper's equations (31)-(32), with
Gamma[a,0]=1 and Gamma[1,b]=Gamma[b,1]=1+(b-1)s.
Source: https://arxiv.org/html/2610.33037v1

At s=-u/v, V[a,b]=v**min(a,b)*Gamma[a,b](s), with the
same scaling for its derivative. Only two rows are stored.
The final pair is p=Gamma[165,164] and d=Gamma[165,165]-p.
Weak interlacing in either orientation forces p*d'-p'*d to have
constant sign; the two exact evaluations below have opposite signs.
"""


def wronskian(n, u, v):
    # F[m]=v**m*f_m(s), Fd[m]=v**m*f'_m(s),
    # where f_0=f_1=1 and f_m=f_(m-1)-s*f_(m-2).
    F, Fd = [1, v], [0, 0]
    for m in range(2, n):
        F.append(v * F[m-1] + u * v * F[m-2])
        Fd.append(v * Fd[m-1] + u * v * Fd[m-2] - v*v * F[m-2])

    old = [1] + [v - (b-1)*u for b in range(1, n+1)]
    oldd = [0] + [(b-1)*v for b in range(1, n+1)]
    for a in range(2, n+1):
        cur = [1, v - (a-1)*u] + [0]*(n-1)
        curd = [0, (a-1)*v] + [0]*(n-1)
        for b in range(2, n+1):
            left_scale = v if a > b else 1
            up_scale = v if a < b else 1
            if a == b:
                left_scale = up_scale = v
            cur[b] = (up_scale*old[b] + left_scale*cur[b-1]
                      - (u+v)*old[b-1])
            curd[b] = (up_scale*oldd[b] + left_scale*curd[b-1]
                       - (u+v)*oldd[b-1] + v*old[b-1])
            if a == b:
                cur[b] += u*F[a-1]
                curd[b] += -v*F[a-1] + u*Fd[a-1]
        old, oldd = cur, curd

    # p and p' have scale v**(n-1), G and G' scale v**n.
    # p*(G-p)' - p'*(G-p) = p*G' - p'*G.
    numerator = old[n-1]*oldd[n] - oldd[n-1]*old[n]
    denominator = v**(2*n-1)
    return numerator, denominator


if __name__ == "__main__":
    n = 165
    w0, d0 = wronskian(n, 0, 1)
    w1, d1 = wronskian(n, 5, 101)
    assert d0 == 1 and w0 == 164
    assert -5621*d1 < w1 < -5620*d1
    print("Composition: (165,165)")
    print("W(0) = 164 > 0")
    print("-5621 < W(-5/101) < -5620 < 0")
    print("Conjecture 2.14's interlacing clause is false.")
