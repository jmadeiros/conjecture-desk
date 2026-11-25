/* checker-1, card B-T1. Written from the definitions, independent of the attacker's code.
 *
 * Mode "eta": expand  q^shift * prod_delta prod_{m>=1} (1 - q^{delta m})^{r_delta}  mod 2^64 up to q^L,
 *   by multiplying (r>0) or dividing (r<0) by each single factor (1 - q^{delta m}) in turn.
 *   Arithmetic in Z/2^64 is a ring homomorphism, so every residue is exact.
 *   Reports min v_2 over n = 3 mod 4, n <= L (zero residue counts as v_2 >= 64),
 *   the first n attaining it, how many n = 3 mod 4 have v_2 < need, and the first 12 residues (for a big-int cross-check).
 *   usage: eta2 eta L shift need d1 r1 d2 r2 ...
 *
 * Mode "direct": B_k(n) = [q^n] P^k with P = f4 f6^2/(f1 f3 f12) built the same way, P^k by repeated plain
 *   convolution mod 2^64; prints for each k <= K the min v_2 of B_k(4n+3), 4n+3 <= L.
 *   usage: eta2 direct L K
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;

static int v2(u64 x) { if (x == 0) return 64; return __builtin_ctzll(x); }

static void apply_factor(u64 *F, long L, long step, int r) {
    /* multiply F by (1 - q^step)^r, r may be negative */
    if (step > L) return;
    if (r > 0) {
        for (int t = 0; t < r; t++)
            for (long n = L; n >= step; n--) F[n] -= F[n - step];
    } else {
        for (int t = 0; t < -r; t++)
            for (long n = step; n <= L; n++) F[n] += F[n - step];
    }
}

static void eta_prod(u64 *F, long L, int nd, const long *d, const int *r) {
    memset(F, 0, sizeof(u64) * (L + 1));
    F[0] = 1;
    for (int i = 0; i < nd; i++)
        for (long m = 1; d[i] * m <= L; m++) apply_factor(F, L, d[i] * m, r[i]);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage\n"); return 2; }
    if (!strcmp(argv[1], "eta")) {
        long L = atol(argv[2]); long shift = atol(argv[3]); int need = atoi(argv[4]);
        int nd = (argc - 5) / 2;
        long d[16]; int r[16];
        for (int i = 0; i < nd; i++) { d[i] = atol(argv[5 + 2 * i]); r[i] = atoi(argv[6 + 2 * i]); }
        u64 *F = calloc(L + 1, sizeof(u64));
        if (shift > L) { printf("shift beyond L\n"); return 1; }
        eta_prod(F, L - shift, nd, d, r);         /* F holds the unshifted product up to q^(L-shift) */
        int minv = 99; long argn = -1; long bad = 0, firstbad = -1, count = 0;
        for (long n = 3; n <= L; n += 4) {       /* coefficient of q^n in q^shift * product */
            long m = n - shift; u64 a = (m >= 0) ? F[m] : 0;
            int v = v2(a); count++;
            if (v < minv) { minv = v; argn = n; }
            if (v < need) { bad++; if (firstbad < 0) firstbad = n; }
        }
        printf("L=%ld shift=%ld need=%d checked_n=%ld min_v2=%d at_n=%ld below_need=%ld first_bad=%ld\n",
               L, shift, need, count, minv, argn, bad, firstbad);
        printf("first residues of product (unshifted):");
        for (long n = 0; n < 12 && n <= L - shift; n++) printf(" %llu", (unsigned long long)F[n]);
        printf("\n");
        free(F);
        return 0;
    }
    if (!strcmp(argv[1], "direct")) {
        long L = atol(argv[2]); int K = atoi(argv[3]);
        long d[5] = {4, 6, 1, 3, 12}; int r[5] = {1, 2, -1, -1, -1};
        u64 *P = calloc(L + 1, sizeof(u64)), *Pk = calloc(L + 1, sizeof(u64)), *T = calloc(L + 1, sizeof(u64));
        eta_prod(P, L, 5, d, r);
        memcpy(Pk, P, sizeof(u64) * (L + 1));
        for (int k = 1; k <= K; k++) {
            if (k > 1) {
                memset(T, 0, sizeof(u64) * (L + 1));
                for (long i = 0; i <= L; i++) { u64 a = Pk[i]; if (!a) continue; for (long j = 0; i + j <= L; j++) T[i + j] += a * P[j]; }
                memcpy(Pk, T, sizeof(u64) * (L + 1));
            }
            int minv = 99; long argn = -1;
            for (long n = 3; n <= L; n += 4) { int v = v2(Pk[n]); if (v < minv) { minv = v; argn = n; } }
            printf("k=%d minv2=%d at_n=%ld Bk3_mod2^64=%llu\n", k, minv, argn, (unsigned long long)Pk[3]);
            fflush(stdout);
        }
        return 0;
    }
    return 2;
}
