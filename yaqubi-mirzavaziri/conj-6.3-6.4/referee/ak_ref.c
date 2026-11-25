/*
 * Referee's own computation of A_k(n) = [q^n] F^k mod 3^10, F = prod_{t>=1} (1 + q^t/(1-q^t)^2)
 * (the combinatorial product for partitions with designated summands, paper eq. before Def. 2.1).
 *
 * Route 1 (main): F from the combinatorial product, as (1 - q^t + q^{2t}) / (1 - q^t)^2 for each t.
 * Route 2 (cross-check of F only): F = f6/(f1 f2 f3) via Euler's pentagonal theorem.
 * Powers: dense truncated convolutions (no pentagonal tricks), F^2, F^3, F^4, F^6, F^7, F^8.
 *
 * Usage: ak_ref NMAX NSMALL   (F^4, F^8 only to NSMALL; others to NMAX)
 * Writes binary residues ak_k{K}.bin (uint32, NMAX+1 or NSMALL+1 entries) and prints checks.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define MOD 59049u /* 3^10 */

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static uint32_t *alloc(long n) { uint32_t *a = calloc(n + 1, sizeof(uint32_t)); if (!a) { perror("calloc"); exit(1); } return a; }

/* c = a*b truncated to degree n, inputs reduced mod MOD */
static void mul(const uint32_t *a, const uint32_t *b, uint32_t *c, long n) {
    uint64_t *acc = calloc(n + 1, sizeof(uint64_t));
    if (!acc) { perror("calloc"); exit(1); }
    for (long i = 0; i <= n; i++) {
        uint64_t ai = a[i];
        if (!ai) continue;
        uint64_t *dst = acc + i;
        long lim = n - i;
        for (long j = 0; j <= lim; j++) dst[j] += ai * (uint64_t)b[j];
        /* acc entries can reach (n+1)*MOD^2 ~ 3.9e14 < 2^63: no overflow, reduce once at the end */
    }
    for (long i = 0; i <= n; i++) c[i] = (uint32_t)(acc[i] % MOD);
    free(acc);
}

static int v3(uint32_t x) { if (x == 0) return 10; int v = 0; while (x % 3 == 0) { x /= 3; v++; } return v; }

static void dump(const char *name, const uint32_t *a, long n) {
    FILE *f = fopen(name, "wb"); fwrite(a, sizeof(uint32_t), n + 1, f); fclose(f);
}

int main(int argc, char **argv) {
    long N = atol(argv[1]), NS = atol(argv[2]);
    double t0 = now();
    /* Route 1: combinatorial product */
    uint32_t *F = alloc(N);
    F[0] = 1;
    for (long t = 1; t <= N; t++) {
        /* multiply by 1 - q^t + q^{2t} (descending so that old values are used) */
        for (long n = N; n >= t; n--) {
            uint32_t v = F[n] + MOD - F[n - t] + (n >= 2 * t ? F[n - 2 * t] : 0); /* in [1, 3 MOD) */
            if (v >= MOD) v -= MOD;
            if (v >= MOD) v -= MOD;
            F[n] = v;
        }
        /* divide by (1 - q^t) twice: running sums along stride t */
        for (int rep = 0; rep < 2; rep++)
            for (long n = t; n <= N; n++) { uint32_t v = F[n] + F[n - t]; if (v >= MOD) v -= MOD; F[n] = v; }
        if (t % 20000 == 0) { printf("  product factor t=%ld done (%.1fs)\n", t, now() - t0); fflush(stdout); }
    }
    printf("F (combinatorial product) first terms:"); for (int i = 0; i <= 12; i++) printf(" %u", F[i]); printf("  (%.1fs)\n", now() - t0);

    /* Route 2: f6/(f1 f2 f3) via pentagonal numbers, compared with route 1 */
    uint32_t *G = alloc(N);
    G[0] = 1;
    /* multiply by f6 = sum_j (-1)^j q^{6 j(3j-1)/2}, j in Z (descending in-place) */
    for (long n = N; n >= 0; n--) {
        int64_t s = G[n];
        for (long j = 1;; j++) {
            long p1 = 6 * (j * (3 * j - 1) / 2), p2 = 6 * (j * (3 * j + 1) / 2);
            if (p1 > n) break;
            int sg = (j & 1) ? -1 : 1;
            s += sg * (int64_t)G[n - p1];
            if (p2 <= n) s += sg * (int64_t)G[n - p2];
        }
        s %= MOD; if (s < 0) s += MOD; G[n] = (uint32_t)s;
    }
    /* divide by f_d for d = 1,2,3:  x = y / f_d  <=>  x[n] = y[n] - sum_{j!=0} (-1)^j x[n - d*pent(j)] */
    for (int d = 1; d <= 3; d++) {
        for (long n = 0; n <= N; n++) {
            int64_t s = G[n];
            for (long j = 1;; j++) {
                long p1 = d * (j * (3 * j - 1) / 2), p2 = d * (j * (3 * j + 1) / 2);
                if (p1 > n) break;
                int sg = (j & 1) ? -1 : 1;
                s -= sg * (int64_t)G[n - p1];
                if (p2 <= n) s -= sg * (int64_t)G[n - p2];
            }
            s %= MOD; if (s < 0) s += MOD; G[n] = (uint32_t)s;
        }
    }
    long mism = 0; for (long n = 0; n <= N; n++) if (F[n] != G[n]) mism++;
    printf("route 1 vs route 2 (eta quotient) for F mod 3^10, n<=%ld: mismatches = %ld  (%.1fs)\n", N, mism, now() - t0);
    fflush(stdout);
    if (mism) return 2;
    free(G);

    uint32_t *P[9] = {0};
    P[1] = F;
    P[2] = alloc(N); mul(F, F, P[2], N);       printf("F^2 done (%.1fs)\n", now() - t0); fflush(stdout);
    P[3] = alloc(N); mul(P[2], F, P[3], N);    printf("F^3 done (%.1fs)\n", now() - t0); fflush(stdout);
    P[6] = alloc(N); mul(P[3], P[3], P[6], N); printf("F^6 done (%.1fs)\n", now() - t0); fflush(stdout);
    P[7] = alloc(N); mul(P[6], F, P[7], N);    printf("F^7 done (%.1fs)\n", now() - t0); fflush(stdout);
    P[4] = alloc(NS); mul(P[2], P[2], P[4], NS); printf("F^4 done to %ld (%.1fs)\n", NS, now() - t0); fflush(stdout);
    P[8] = alloc(NS); mul(P[4], P[4], P[8], NS); printf("F^8 done to %ld (%.1fs)\n", NS, now() - t0); fflush(stdout);
    /* extra consistency: F^7 also as F^4*F^3 up to NS, F^8 also as F^7*F up to NS, F^6 as F^4*F^2 */
    {
        uint32_t *T = alloc(NS); long bad = 0;
        mul(P[4], P[3], T, NS); for (long n = 0; n <= NS; n++) bad += (T[n] != P[7][n]);
        mul(P[7], F, T, NS);   for (long n = 0; n <= NS; n++) bad += (T[n] != P[8][n]);
        mul(P[4], P[2], T, NS); for (long n = 0; n <= NS; n++) bad += (T[n] != P[6][n]);
        printf("associativity cross-checks to %ld: mismatches = %ld (%.1fs)\n", NS, bad, now() - t0);
        free(T); if (bad) return 3;
    }
    char nm[64];
    int ks[] = {3, 4, 6, 7, 8};
    for (int i = 0; i < 5; i++) { int k = ks[i]; sprintf(nm, "ak_k%d.bin", k); dump(nm, P[k], (k == 4 || k == 8) ? NS : N); }

    /* the six claims: k, m, r, t, bound (n <= bound) */
    struct { const char *lab; int k, m, r, t; long bound; } C[] = {
        {"6.3  A_6(12n+10) mod 3^5", 6, 12, 10, 5, 7776},
        {"6.4a A_3(12n+7)  mod 3^4", 3, 12, 7, 4, 19008},
        {"6.4a A_3(12n+11) mod 3^4", 3, 12, 11, 4, 19008},
        {"6.4b A_4(6n+5)   mod 3^3", 4, 6, 5, 3, 2160},
        {"6.4b A_7(12n+11) mod 3^3", 7, 12, 11, 3, 112320},
        {"6.4c A_8(18n+15) mod 3^5", 8, 18, 15, 5, 36288},
    };
    int allok = 1;
    for (int i = 0; i < 6; i++) {
        uint32_t *A = P[C[i].k]; long top = (C[i].k == 4 || C[i].k == 8) ? NS : N;
        long terms_b = 0, fail_b = -1, terms_all = 0, fail_all = -1; int minv_b = 99, minv_all = 99;
        long hist[11] = {0};
        for (long n = C[i].r; n <= top; n += C[i].m) {
            int v = v3(A[n]);
            terms_all++; if (v < minv_all) minv_all = v; if (v < C[i].t && fail_all < 0) fail_all = n; hist[v]++;
            if (n <= C[i].bound) { terms_b++; if (v < minv_b) minv_b = v; if (v < C[i].t && fail_b < 0) fail_b = n; }
        }
        int ok = (fail_b < 0) && (top >= C[i].bound);
        allok &= ok;
        printf("%s: n<=%ld (need %ld): %ld terms, min v3 = %d, first failure %ld -> %s | to n<=%ld: %ld terms, min v3 = %d, first failure %ld | v3 histogram 0..10(>=10):",
               C[i].lab, C[i].bound, C[i].bound, terms_b, minv_b, fail_b, ok ? "OK" : "FAIL", top, terms_all, minv_all, fail_all);
        for (int v = 0; v <= 10; v++) printf(" %ld", hist[v]);
        printf("\n");
    }
    /* exactness data for 6.3 */
    printf("A_6(10) mod 3^10 = %u (v3 = %d), A_6(22) mod 3^10 = %u (v3 = %d)\n", P[6][10], v3(P[6][10]), P[6][22], v3(P[6][22]));
    { long first6 = -1, cnt6 = 0, cnt5 = 0;
      for (long n = 10; n <= N; n += 12) { int v = v3(P[6][n]); if (v >= 6) { cnt6++; if (first6 < 0) first6 = n; } if (v == 5) cnt5++; }
      printf("6.3 exactness: among n=10 mod 12, n<=%ld: v3==5 for %ld terms, v3>=6 for %ld terms (first at n=%ld)\n", N, cnt5, cnt6, first6); }
    printf("%s (%.1fs)\n", allok ? "ALL SIX CLAIMS VERIFIED TO THEIR STURM RANGES" : "SOME CHECK FAILED", now() - t0);
    return allok ? 0 : 1;
}
