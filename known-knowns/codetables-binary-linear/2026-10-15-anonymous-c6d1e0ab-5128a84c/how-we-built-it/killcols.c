/*
 * killcols.c CODE.json tmax secs seed OUT.json  (runner-codes, 2026-10-14)
 *
 * Given an [n,k,d] code (k <= 26), find t <= tmax new columns v_1..v_t in GF(2)^k such that every
 * minimum-weight codeword uG gets at least one 1 in the new columns (<u, v_i> = 1 for some i), giving an
 * [n+t, k, d+1] code. Greedy with sampled + locally improved columns, restarts until secs.
 * Writes the extended generator matrix to OUT.json when a full cover is found (smallest t found).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;
typedef uint32_t u32;
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static u64 rs = 0x2545F4914F6CDD1DULL;
static u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }

static int N, K;
static int Gb[32][256];

static int load(const char *path) {
    FILE *fp = fopen(path, "rb");
    if (!fp) return 0;
    fseek(fp, 0, SEEK_END);
    long sz = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    char *b = malloc(sz + 1);
    if (fread(b, 1, sz, fp) != (size_t)sz) return 0;
    b[sz] = 0;
    fclose(fp);
    char *g = strstr(b, "\"G\"");
    if (!g) return 0;
    g = strchr(g, '[');
    int depth = 0, row = 0, col = 0;
    for (char *c = g; *c; c++) {
        if (*c == '[') { depth++; if (depth == 2) col = 0; }
        else if (*c == ']') { if (depth == 2) { N = col; row++; } depth--; if (depth == 0) break; }
        else if (depth == 2 && (*c == '0' || *c == '1')) { Gb[row][col++] = *c - '0'; }
    }
    K = row;
    free(b);
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 6 || !load(argv[1])) { fprintf(stderr, "usage: killcols CODE.json tmax secs seed OUT.json\n"); return 1; }
    int tmax = atoi(argv[2]);
    double secs = atof(argv[3]);
    rs ^= strtoull(argv[4], NULL, 10) * 0x9E3779B97F4A7C15ULL;
    for (int i = 0; i < 10; i++) rnd();
    /* rows as 4-word vectors */
    u64 R[32][4];
    memset(R, 0, sizeof R);
    for (int i = 0; i < K; i++) for (int j = 0; j < N; j++) if (Gb[i][j]) R[i][j >> 6] |= 1ULL << (j & 63);
    /* gray enumeration: collect min-weight messages */
    u64 cw[4] = {0, 0, 0, 0};
    int d = 9999;
    u32 cap = 1 << 20, ns = 0;
    u32 *S = malloc(sizeof(u32) * cap);
    u32 g = 0;
    for (u64 i = 1; i < (1ULL << K); i++) {
        int b = __builtin_ctzll(i);
        for (int w = 0; w < 4; w++) cw[w] ^= R[b][w];
        g ^= 1u << b;
        int wt = __builtin_popcountll(cw[0]) + __builtin_popcountll(cw[1]) + __builtin_popcountll(cw[2]) + __builtin_popcountll(cw[3]);
        if (wt < d) { d = wt; ns = 0; }
        if (wt == d) { if (ns < cap) S[ns] = g; ns++; }
    }
    if (ns > cap) { fprintf(stderr, "too many min words %u\n", ns); return 1; }
    fprintf(stderr, "code [%d,%d,%d] A_d=%u\n", N, K, d, ns);
    double t0 = now();
    int bestt = 999;
    u32 bestV[64];
    u32 *rem = malloc(sizeof(u32) * ns);
    long restarts = 0;
    while (now() - t0 < secs) {
        restarts++;
        u32 nr = ns;
        memcpy(rem, S, sizeof(u32) * ns);
        u32 V[64];
        int t = 0;
        while (nr > 0 && t < tmax && t < bestt - 1 + 1) {
            /* best column: sample candidates, then bit-flip local search */
            u32 bv = 0;
            int bc = -1;
            int samples = 64;
            for (int s = 0; s < samples; s++) {
                u32 v;
                if (s < 8 && nr > 0) v = rem[rnd() % nr] ^ (u32)(rnd() & ((1ULL << K) - 1)); else v = (u32)(rnd() & ((1ULL << K) - 1));
                if (!v) v = 1;
                int c = 0;
                for (u32 q = 0; q < nr; q++) c += __builtin_parity(rem[q] & v);
                /* local search */
                int improved = 1;
                while (improved) {
                    improved = 0;
                    for (int bit = 0; bit < K; bit++) {
                        u32 v2 = v ^ (1u << bit);
                        if (!v2) continue;
                        int c2 = 0;
                        for (u32 q = 0; q < nr; q++) c2 += __builtin_parity(rem[q] & v2);
                        if (c2 > c) { c = c2; v = v2; improved = 1; }
                    }
                }
                if (c > bc) { bc = c; bv = v; }
            }
            V[t++] = bv;
            u32 w = 0;
            for (u32 q = 0; q < nr; q++) if (!__builtin_parity(rem[q] & bv)) rem[w++] = rem[q];
            nr = w;
        }
        if (nr == 0 && t < bestt) {
            bestt = t;
            memcpy(bestV, V, sizeof(u32) * t);
            fprintf(stderr, "cover with t=%d after %ld restarts (%.1fs)\n", t, restarts, now() - t0);
            FILE *fo = fopen(argv[5], "w");
            fprintf(fo, "{\"n\":%d,\"k\":%d,\"construction\":\"%s extended by %d columns covering all %u weight-%d words\",\"G\":[\n", N + t, K, argv[1], t, ns, d);
            for (int i = 0; i < K; i++) {
                fprintf(fo, "[");
                for (int j = 0; j < N; j++) fprintf(fo, "%s%d", j ? "," : "", Gb[i][j]);
                for (int c = 0; c < t; c++) fprintf(fo, ",%d", (int)((bestV[c] >> i) & 1));
                fprintf(fo, "]%s\n", i + 1 < K ? "," : "");
            }
            fprintf(fo, "]}\n");
            fclose(fo);
            if (t <= 1) break;
        }
    }
    printf("{\"n\":%d,\"k\":%d,\"d\":%d,\"A\":%u,\"best_t\":%d,\"restarts\":%ld}\n", N, K, d, ns, bestt == 999 ? -1 : bestt, restarts);
    return 0;
}
