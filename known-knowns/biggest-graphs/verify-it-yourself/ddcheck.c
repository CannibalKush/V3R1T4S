/* ddcheck.c -- exhaustive all-pairs check that an edge list is a simple graph with maximum degree <= DELTA
 * and diameter <= D.  Written for strangers: no dependencies beyond a C99 compiler and pthreads.
 *
 * Build:   cc -O3 -o ddcheck ddcheck.c -lpthread
 *          (optional: -DW=32 to process 2048 sources per batch instead of 1024; memory per thread is 2*N*W*8 bytes)
 * Usage:   ./ddcheck EDGEFILE DELTA D [THREADS]
 *
 * Input:   one undirected edge "u v" per line, 0-based integer labels, no header; lines starting with '#' are ignored.
 *          Each edge should appear once (a repeated edge or a reversed duplicate is reported as a duplicate).
 *
 * Method:  bitset ball growth.  For a batch of up to 64*W source vertices, A[v] is a W-word bitmask whose bit i is
 *          set iff dist(v, s_i) <= r after r rounds; one round sets A'[v] = A[v] | OR_{u ~ v} A[u].  After D rounds the
 *          number of unset bits is the number of ordered pairs (v, s_i) at distance > D.  Every vertex is a source
 *          exactly once, so the count covers all N*N ordered pairs.
 *
 * Output:  N, edge count, loops, duplicates, min/max degree, degree histogram, ordered pairs at distance <= r for
 *          r = 0..D (summed over batches) and the number of ordered pairs at distance > D.
 *          Last line: VALID iff no loops, no duplicates, every label 0..N-1 occurs, max degree <= DELTA and 0 far pairs.
 * Exit code: 0 if VALID, 1 if INVALID, 2 on input/usage error.
 *
 * Controls: run with D-1 instead of D; a graph of diameter exactly D must then report far pairs > 0 and INVALID.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>

#ifndef W
#define W 16
#endif
#define SRC_PER_BATCH (64 * W)

static int N, D;
static long long M;
static int *off, *adj;
static long long far_total = 0;
static long long *within_total;      /* within_total[r] = ordered pairs at distance <= r */
static int next_batch = 0, nbatches = 0;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;

static int cmp_u64(const void *a, const void *b) {
    uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b;
    return x < y ? -1 : x > y;
}

static long long count_bits(const uint64_t *A, int ns) {
    long long c = 0;
    int full = ns / 64, rem = ns % 64;
    for (int v = 0; v < N; v++) {
        const uint64_t *row = A + (size_t)v * W;
        for (int k = 0; k < full; k++) c += __builtin_popcountll(row[k]);
        if (rem) c += __builtin_popcountll(row[full] & ((1ULL << rem) - 1));
    }
    return c;
}

static void *worker(void *arg) {
    (void)arg;
    uint64_t *A = calloc((size_t)N * W, 8), *B = calloc((size_t)N * W, 8);
    long long *within = calloc(D + 1, sizeof(long long));
    if (!A || !B || !within) { fprintf(stderr, "out of memory\n"); exit(2); }
    for (;;) {
        pthread_mutex_lock(&mu);
        int b = next_batch++;
        pthread_mutex_unlock(&mu);
        if (b >= nbatches) break;
        int s0 = b * SRC_PER_BATCH;
        int ns = (N - s0 < SRC_PER_BATCH) ? N - s0 : SRC_PER_BATCH;
        memset(A, 0, (size_t)N * W * 8);
        for (int i = 0; i < ns; i++) A[(size_t)(s0 + i) * W + i / 64] |= 1ULL << (i % 64);
        within[0] += count_bits(A, ns);
        for (int r = 1; r <= D; r++) {
            for (int v = 0; v < N; v++) {
                uint64_t t[W];
                memcpy(t, A + (size_t)v * W, W * 8);
                for (int e = off[v]; e < off[v + 1]; e++) {
                    const uint64_t *u = A + (size_t)adj[e] * W;
                    for (int k = 0; k < W; k++) t[k] |= u[k];
                }
                memcpy(B + (size_t)v * W, t, W * 8);
            }
            uint64_t *x = A; A = B; B = x;
            within[r] += count_bits(A, ns);
        }
        long long reached = within[D];
        (void)reached;
    }
    pthread_mutex_lock(&mu);
    for (int r = 0; r <= D; r++) within_total[r] += within[r];
    pthread_mutex_unlock(&mu);
    free(A); free(B); free(within);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s EDGEFILE DELTA D [THREADS]\n", argv[0]); return 2; }
    int Delta = atoi(argv[2]);
    D = atoi(argv[3]);
    int T = argc > 4 ? atoi(argv[4]) : 4;
    if (Delta <= 0 || D <= 0 || T <= 0 || T > 256) { fprintf(stderr, "bad DELTA/D/THREADS\n"); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[1]); return 2; }

    long long cap = 1 << 20, loops = 0, badlines = 0;
    uint64_t *E = malloc(cap * 8);
    long maxv = -1;
    char line[256];
    M = 0;
    while (fgets(line, sizeof line, f)) {
        char *p = line;
        while (*p == ' ' || *p == '\t') p++;
        if (*p == '#' || *p == '\n' || *p == '\r' || *p == 0) continue;
        char *q;
        long a = strtol(p, &q, 10);
        if (q == p) { badlines++; continue; }
        long b = strtol(q, &p, 10);
        if (p == q) { badlines++; continue; }
        while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
        if (*p != 0) { badlines++; continue; }
        if (a < 0 || b < 0 || a > 0x7fffffffL || b > 0x7fffffffL) { badlines++; continue; }
        if (a == b) { loops++; continue; }
        if (a > b) { long t = a; a = b; b = t; }
        if (M == cap) { cap *= 2; E = realloc(E, cap * 8); if (!E) { fprintf(stderr, "out of memory\n"); return 2; } }
        E[M++] = ((uint64_t)a << 32) | (uint64_t)b;
        if (b > maxv) maxv = b;
    }
    fclose(f);
    if (badlines) { fprintf(stderr, "%lld unparsable lines: INVALID\n", badlines); return 1; }
    if (maxv < 0) { fprintf(stderr, "no edges: INVALID\n"); return 1; }
    N = (int)maxv + 1;
    qsort(E, M, 8, cmp_u64);
    long long dup = 0;
    for (long long i = 1; i < M; i++) if (E[i] == E[i - 1]) dup++;

    int *deg = calloc(N, sizeof(int));
    for (long long i = 0; i < M; i++) { deg[E[i] >> 32]++; deg[E[i] & 0xffffffffULL]++; }
    int maxd = 0, mind = 1 << 30, missing = 0;
    for (int i = 0; i < N; i++) { if (deg[i] > maxd) maxd = deg[i]; if (deg[i] < mind) mind = deg[i]; if (deg[i] == 0) missing++; }
    off = malloc((size_t)(N + 1) * sizeof(int));
    off[0] = 0;
    for (int i = 0; i < N; i++) off[i + 1] = off[i] + deg[i];
    adj = malloc((size_t)off[N] * sizeof(int));
    int *pos = malloc((size_t)N * sizeof(int));
    memcpy(pos, off, (size_t)N * sizeof(int));
    for (long long i = 0; i < M; i++) {
        int x = (int)(E[i] >> 32), y = (int)(E[i] & 0xffffffffULL);
        adj[pos[x]++] = y; adj[pos[y]++] = x;
    }
    free(pos); free(E);

    printf("file=%s\nN=%d edges=%lld loops=%lld duplicates=%lld unused_labels=%d mindeg=%d maxdeg=%d (DELTA=%d, D=%d)\n",
           argv[1], N, M, loops, dup, missing, mind, maxd, Delta, D);
    printf("degree_histogram:");
    for (int d = 0; d <= maxd; d++) { long long c = 0; for (int i = 0; i < N; i++) if (deg[i] == d) c++; if (c) printf(" %d:%lld", d, c); }
    printf("\n");
    fflush(stdout);
    free(deg);

    nbatches = (N + SRC_PER_BATCH - 1) / SRC_PER_BATCH;
    within_total = calloc(D + 1, sizeof(long long));
    pthread_t th[256];
    for (int i = 0; i < T; i++) pthread_create(&th[i], NULL, worker, NULL);
    for (int i = 0; i < T; i++) pthread_join(th[i], NULL);
    far_total = (long long)N * (long long)N - within_total[D];

    printf("ordered_pairs_within_distance:");
    for (int r = 0; r <= D; r++) printf(" r=%d:%lld", r, within_total[r]);
    printf("\nordered_pairs_at_distance_gt_%d=%lld (of %lld)\n", D, far_total, (long long)N * (long long)N);
    int valid = (far_total == 0 && loops == 0 && dup == 0 && missing == 0 && maxd <= Delta);
    printf("%s\n", valid ? "VALID" : "INVALID");
    return valid ? 0 : 1;
}
