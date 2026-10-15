/*
 * qcs.c - quasi-cyclic (1-generator, index p) binary code search, runner-codes 2026-10-14.
 *
 * Code: m odd, h | x^m - 1 with deg h = k (product of chosen irreducible factors), g = (x^m-1)/h.
 * Message a in M = GF(2)[x]/(h) (k-bit integer, coefficient of x^i at bit i).
 * Codeword c(a) = ( g*(a*f_0 mod h), g*(a*f_1 mod h), ..., g*(a*f_{p-1} mod h) ), f_0 = 1, each block m bits.
 * c(x*a) is the blockwise cyclic shift of c(a), so the weight is constant on x-orbits of M\{0};
 * d = min over orbit representatives, A_d = sum of orbit sizes of representatives of weight d.
 * Evaluation: codeword of a rep = XOR of 4 byte-chunk lookup tables built from the k generator rows.
 *
 * Modes:
 *   qcs factor m
 *       -> prints irreducible factors of x^m-1 of degree <= 26 (index, degree, hex)
 *   qcs search m facmask p seconds seed [dstop]
 *       facmask: hex bitmask over the factor list printed by 'factor' (h = product of those factors)
 *       random restarts + first-improvement hill climbing on (d, -A_d); prints JSON lines
 *   qcs emit m facmask p f1hex,f2hex,...
 *       -> prints JSON {"G": ...} for the code with multipliers f_1..f_{p-1} (f_0 = 1)
 *   qcs eval m facmask p f1hex,...      -> exact (d, A_d) by orbit enumeration
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;
typedef uint32_t u32;

static double now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

static u64 rs0 = 0x9E3779B97F4A7C15ULL, rs1 = 0xD1B54A32D192ED03ULL;
static u64 rnd(void) {
    u64 s1 = rs0;
    const u64 s0 = rs1;
    rs0 = s0;
    s1 ^= s1 << 23;
    rs1 = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26);
    return rs1 + s0;
}

/* ---------- small polynomials (degree < 64) ---------- */
static int sdeg(u64 a) { return a ? 63 - __builtin_clzll(a) : -1; }
static u64 smod(u64 a, u64 f) {
    int df = sdeg(f), da;
    while ((da = sdeg(a)) >= df) a ^= f << (da - df);
    return a;
}
static u64 smulmod(u64 a, u64 b, u64 f) { /* deg a, deg b < deg f <= 32 */
    u64 r = 0;
    int df = sdeg(f);
    a = smod(a, f);
    while (b) {
        if (b & 1) r ^= a;
        b >>= 1;
        a <<= 1;
        if ((a >> df) & 1) a ^= f;
    }
    return r;
}
static u64 xm_mod(int m, u64 f) {
    u64 r = smod(1, f), b = smod(2, f);
    int e = m;
    while (e) {
        if (e & 1) r = smulmod(r, b, f);
        b = smulmod(b, b, f);
        e >>= 1;
    }
    return r;
}

/* ---------- big polynomials (degree < 320) ---------- */
#define BW 5
typedef struct { u64 w[BW]; } BP;
static int bdeg(const BP *a) {
    for (int i = BW - 1; i >= 0; i--)
        if (a->w[i]) return i * 64 + 63 - __builtin_clzll(a->w[i]);
    return -1;
}
static int bget(const BP *a, int i) { return (a->w[i >> 6] >> (i & 63)) & 1; }
static void bflip(BP *a, int i) { a->w[i >> 6] ^= 1ULL << (i & 63); }
static void bxor_shift(BP *r, const BP *a, int s) { /* r ^= a << s */
    for (int i = 0; i < BW * 64; i++)
        if (bget(a, i) && i + s < BW * 64) bflip(r, i + s);
}
/* q = a / b (exact or not), r = remainder */
static void bdivmod(const BP *a, const BP *b, BP *q, BP *r) {
    BP rr = *a, qq;
    memset(&qq, 0, sizeof qq);
    int db = bdeg(b), dr;
    while ((dr = bdeg(&rr)) >= db) {
        bxor_shift(&rr, b, dr - db);
        bflip(&qq, dr - db);
    }
    if (q) *q = qq;
    if (r) *r = rr;
}

/* ---------- factorization of x^m - 1 (factors of degree <= 26) ---------- */
static int NF;
static u64 FAC[128];
static int FDEG[128];
static void factor_xm1(int m) {
    static int seen[1024];
    int need[64] = {0};
    memset(seen, 0, sizeof seen);
    for (int i = 0; i < m; i++)
        if (!seen[i]) {
            int s = 0, j = i;
            do { seen[j] = 1; j = (2 * j) % m; s++; } while (j != i);
            if (s < 64) need[s]++;
        }
    NF = 0;
    for (int e = 1; e <= 26; e++) {
        if (!need[e]) continue;
        int found = 0;
        for (u64 c = 0; c < (1ULL << (e - 1)); c++) {
            u64 f = (1ULL << e) | (c << 1) | 1ULL;
            if (xm_mod(m, f) != 1) continue;
            int irr = 1;
            for (int t = 0; t < NF; t++)
                if (smod(f, FAC[t]) == 0) { irr = 0; break; }
            if (!irr) continue;
            FAC[NF] = f;
            FDEG[NF] = e;
            NF++;
            if (++found == need[e]) break;
        }
    }
}

/* ---------- structure ---------- */
static int M, K, P, N, NWD;
static u64 H;        /* h(x), degree K */
static BP Gp;        /* g(x) = (x^m-1)/h(x) */
static void build_gs(void);
static u32 *REPS;    /* orbit representatives */
static uint16_t *RSZ;/* orbit sizes */
static u32 NREPS;
static u64 T[4][256][4];      /* chunk tables for current code */

static inline u32 mulx(u32 a) {
    a <<= 1;
    if ((a >> K) & 1) a ^= (u32)H;
    return a;
}

static int setup(int m, u64 facmask, int p) {
    M = m;
    P = p;
    N = m * p;
    if (N > 256) { fprintf(stderr, "n=%d > 256\n", N); return 0; }
    NWD = (N + 63) / 64;
    factor_xm1(m);
    H = 1;
    for (int i = 0; i < NF; i++)
        if ((facmask >> i) & 1) {
            /* multiply H by FAC[i] (degrees stay <= 26+26 temporarily fine in u64) */
            u64 r = 0, a = H, b = FAC[i];
            while (b) { if (b & 1) r ^= a; b >>= 1; a <<= 1; }
            H = r;
        }
    K = sdeg(H);
    if (K < 1 || K > 26) { fprintf(stderr, "k=%d out of range\n", K); return 0; }
    BP xm1;
    memset(&xm1, 0, sizeof xm1);
    bflip(&xm1, m);
    bflip(&xm1, 0);
    BP hb, rem;
    memset(&hb, 0, sizeof hb);
    hb.w[0] = H;
    bdivmod(&xm1, &hb, &Gp, &rem);
    if (bdeg(&rem) >= 0) { fprintf(stderr, "h does not divide x^m-1\n"); return 0; }
    build_gs();
    return 1;
}

/* GS[i] = g << i as big poly, i < K */
static BP GS[32];
static void build_gs(void) {
    for (int i = 0; i < K; i++) { memset(&GS[i], 0, sizeof(BP)); bxor_shift(&GS[i], &Gp, i); }
}
/* cw (4 words) ^= v << off, v a big poly of degree < m, off + m <= 256 */
static void xor_at(u64 *cw, const BP *v, int off) {
    int ws = off >> 6, bs = off & 63;
    for (int i = 0; i < BW; i++) {
        if (!v->w[i]) continue;
        int t = i + ws;
        if (t < 4) cw[t] ^= v->w[i] << bs;
        if (bs && t + 1 < 4) cw[t + 1] ^= v->w[i] >> (64 - bs);
    }
}
static void add_block(u64 *cw, u32 b, int off) {
    BP v;
    memset(&v, 0, sizeof v);
    for (int i = 0; i < K; i++)
        if ((b >> i) & 1)
            for (int w = 0; w < BW; w++) v.w[w] ^= GS[i].w[w];
    xor_at(cw, &v, off);
}

static u64 ROWS[32][4];
static void build_tables(const u32 *f) { /* f[0..P-1], f[0] = 1 */
    for (int i = 0; i < K; i++) {
        memset(ROWS[i], 0, sizeof ROWS[i]);
        for (int j = 0; j < P; j++) {
            u32 b = (u32)smulmod(1ULL << i, f[j], H);
            add_block(ROWS[i], b, j * M);
        }
    }
    for (int c = 0; c < 4; c++) {
        for (int w = 0; w < 4; w++) T[c][0][w] = 0;
        for (int byte = 1; byte < 256; byte++) {
            int t = __builtin_ctz(byte);
            int i = 8 * c + t;
            int prev = byte & (byte - 1);
            for (int w = 0; w < 4; w++) T[c][byte][w] = T[c][prev][w] ^ (i < K ? ROWS[i][w] : 0);
        }
    }
}

static inline int wt_of(u32 a) {
    const u64 *t0 = T[0][a & 255], *t1 = T[1][(a >> 8) & 255], *t2 = T[2][(a >> 16) & 255], *t3 = T[3][(a >> 24) & 255];
    return __builtin_popcountll(t0[0] ^ t1[0] ^ t2[0] ^ t3[0]) + __builtin_popcountll(t0[1] ^ t1[1] ^ t2[1] ^ t3[1]) +
           __builtin_popcountll(t0[2] ^ t1[2] ^ t2[2] ^ t3[2]) + __builtin_popcountll(t0[3] ^ t1[3] ^ t2[3] ^ t3[3]);
}

/* orbit reps sorted by block-0 weight wt(g*a) ascending */
static void build_reps(void) {
    u64 size = 1ULL << K;
    uint8_t *vis = calloc(size / 8 + 1, 1);
    u32 cap = (u32)(size / 8 + 1024);
    u32 *reps = malloc(sizeof(u32) * cap);
    uint16_t *rsz = malloc(sizeof(uint16_t) * cap);
    u32 nr = 0;
    for (u32 a = 1; a < size; a++) {
        if ((vis[a >> 3] >> (a & 7)) & 1) continue;
        u32 b = a;
        int s = 0;
        do { vis[b >> 3] |= 1 << (b & 7); b = mulx(b); s++; } while (b != a);
        if (nr >= cap) { cap *= 2; reps = realloc(reps, sizeof(u32) * cap); rsz = realloc(rsz, sizeof(uint16_t) * cap); }
        reps[nr] = a;
        rsz[nr] = (uint16_t)s;
        nr++;
    }
    free(vis);
    /* block-0 weights: tables with f = (1,0,0,...) */
    u32 f0[8] = {1, 0, 0, 0, 0, 0, 0, 0};
    int saveP = P;
    P = 1;
    build_tables(f0);
    P = saveP;
    int cnt[300] = {0};
    uint8_t *w0 = malloc(nr);
    for (u32 r = 0; r < nr; r++) { w0[r] = (uint8_t)wt_of(reps[r]); cnt[w0[r]]++; }
    int start[300];
    int acc = 0;
    for (int w = 0; w < 300; w++) { start[w] = acc; acc += cnt[w]; }
    REPS = malloc(sizeof(u32) * nr);
    RSZ = malloc(sizeof(uint16_t) * nr);
    for (u32 r = 0; r < nr; r++) { int pos = start[w0[r]]++; REPS[pos] = reps[r]; RSZ[pos] = rsz[r]; }
    NREPS = nr;
    free(reps); free(rsz); free(w0);
}

/* evaluate current tables. Returns d; *A = count. Abort (return -1) if a weight < dmin is found, or
   weight == dmin with count > amax (strict-improvement thresholds). dmin=0 => full evaluation. */
static int TAILT = 0; /* Construction X with sub = (x+1): tail of TAILT ones on odd-parity messages */
#define NKILL 32
static u32 KILL[NKILL];
static int nkill = 0, kpos = 0;
static int evaluate(int dmin, u64 amax, u64 *A) {
    /* killer reps first (quick reject) */
    if (dmin > 0)
        for (int i = 0; i < nkill; i++) {
            int w = wt_of(KILL[i]) + (__builtin_parity(KILL[i]) ? TAILT : 0);
            if (w < dmin) return -1;
        }
    int d = 999;
    u64 cnt = 0;
    for (u32 r = 0; r < NREPS; r++) {
        u32 a = REPS[r];
        int w = wt_of(a) + (__builtin_parity(a) ? TAILT : 0);
        if (w <= d) {
            if (w < d) { d = w; cnt = 0; }
            cnt += RSZ[r];
            if (w < dmin || (w == dmin && cnt > amax)) {
                /* record killer */
                KILL[kpos] = a;
                kpos = (kpos + 1) % NKILL;
                if (nkill < NKILL) nkill++;
                return -1;
            }
        }
    }
    *A = cnt;
    return d;
}

static u32 rand_elem(void) {
    u32 a;
    do { a = (u32)(rnd() & ((1ULL << K) - 1)); } while (a == 0);
    return a;
}

static void print_code(const char *tag, int d, u64 A, const u32 *f, double t) {
    printf("{\"tag\":\"%s\",\"m\":%d,\"p\":%d,\"n\":%d,\"k\":%d,\"h\":\"%llx\",\"d\":%d,\"A\":%llu,\"f\":\"", tag, M, P, N, K,
           (unsigned long long)H, d, (unsigned long long)A);
    for (int j = 1; j < P; j++) printf("%s%x", j > 1 ? "," : "", f[j]);
    printf("\",\"t\":%.1f}\n", t);
    fflush(stdout);
}

static int parse_f(const char *s, u32 *f) {
    f[0] = 1;
    int j = 1;
    const char *c = s;
    while (*c && j < P) {
        f[j++] = (u32)strtoul(c, (char **)&c, 16);
        if (*c == ',') c++;
    }
    return j == P;
}


/* ================= Construction X mode =================
 * h = HC * HS (core * sub). C2 = messages a = 0 mod HS (dim KC). Residue r(a) = a mod HS (S bits).
 * Wmin[r] = min weight of the coset {a : a mod HS = r}; Wmin[0] = d2. For a subspace V = span(r_1..r_sp)
 * of residues and an sp x t tail T, the code {a : r(a) in V} + tail has length n+t, dim KC+sp and
 * D = min(d2, min_{lambda != 0} Wmin[r(lambda)] + wt(lambda T)).
 */
static u64 HC = 1, HS = 1;
static int KC, SS;
static u32 *RES;
static u32 *R0;
static u32 NR0;

static void x_setup(u64 coremask, u64 submask) {
    HC = 1; HS = 1;
    for (int i = 0; i < NF; i++) {
        u64 *t = NULL;
        if ((coremask >> i) & 1) t = &HC;
        else if ((submask >> i) & 1) t = &HS;
        if (!t) continue;
        u64 r = 0, a = *t, b = FAC[i];
        while (b) { if (b & 1) r ^= a; b >>= 1; a <<= 1; }
        *t = r;
    }
    KC = sdeg(HC);
    SS = sdeg(HS);
    RES = malloc(sizeof(u32) * NREPS);
    R0 = malloc(sizeof(u32) * NREPS);
    NR0 = 0;
    for (u32 i = 0; i < NREPS; i++) {
        RES[i] = (u32)smod(REPS[i], HS);
        if (RES[i] == 0) R0[NR0++] = i;
    }
}

static int evaluate_sub(int dmin, u64 amax, u64 *A) {
    int d = 999;
    u64 cnt = 0;
    for (u32 q = 0; q < NR0; q++) {
        u32 r = R0[q];
        int w = wt_of(REPS[r]);
        if (w <= d) {
            if (w < d) { d = w; cnt = 0; }
            cnt += RSZ[r];
            if (w < dmin || (w == dmin && cnt > amax)) return -1;
        }
    }
    *A = cnt;
    return d;
}

static void coset_minima(int *Wm) {
    int ns = 1 << SS;
    int raw[1 << 12];
    for (int r = 0; r < ns; r++) raw[r] = 999;
    for (u32 i = 0; i < NREPS; i++) {
        int w = wt_of(REPS[i]);
        if (w < raw[RES[i]]) raw[RES[i]] = w;
    }
    /* propagate over x-orbits of residues */
    static uint8_t seen[1 << 12];
    memset(seen, 0, ns);
    Wm[0] = raw[0];
    for (int r = 1; r < ns; r++) {
        if (seen[r]) continue;
        int mn = 999;
        u32 b = r;
        do { if (raw[b] < mn) mn = raw[b]; b = (u32)smod((u64)b << 1, HS); } while (b != (u32)r);
        b = r;
        do { Wm[b] = mn; seen[b] = 1; b = (u32)smod((u64)b << 1, HS); } while (b != (u32)r);
    }
}

/* tail feasibility: sp <= 3, requirement R[lambda] for lambda=1..2^sp-1, t columns. cols[] gets counts per type */
static int TSP, TNT, TR[8], TC[8], TCOLS[8];
static int dfs_tail(int c, int rem) {
    int done = 1;
    for (int l = 1; l <= TNT; l++) {
        int def = TR[l] - TC[l];
        if (def > rem) return 0;
        if (def > 0) done = 0;
    }
    if (done) { if (rem > 0) TCOLS[1] += rem; return 1; }
    if (c > TNT) return 0;
    for (int num = rem; num >= 0; num--) {
        for (int l = 1; l <= TNT; l++) if (__builtin_parity(l & c)) TC[l] += num;
        TCOLS[c] = num;
        if (dfs_tail(c + 1, rem - num)) {
            for (int l = 1; l <= TNT; l++) if (__builtin_parity(l & c)) TC[l] -= num;
            return 1;
        }
        TCOLS[c] = 0;
        for (int l = 1; l <= TNT; l++) if (__builtin_parity(l & c)) TC[l] -= num;
    }
    return 0;
}
static int tail_feasible(int sp, const int *Wl, int D, int t) { /* Wl[lambda] = coset minimum for lambda */
    TSP = sp;
    TNT = (1 << sp) - 1;
    memset(TC, 0, sizeof TC);
    memset(TCOLS, 0, sizeof TCOLS);
    for (int l = 1; l <= TNT; l++) { TR[l] = D - Wl[l]; if (TR[l] < 0) TR[l] = 0; if (TR[l] > t) return 0; }
    return dfs_tail(1, t);
}

#define XT 17
static int XBEST[4][XT];      /* best D per (sp, t) */
static void x_report(int sp, int t, int D, int d2, const u32 *f, const u32 *V) {
    printf("{\"tag\":\"x\",\"m\":%d,\"p\":%d,\"n\":%d,\"k\":%d,\"D\":%d,\"d2\":%d,\"sp\":%d,\"t\":%d,\"h\":\"%llx\",\"hc\":\"%llx\",\"hs\":\"%llx\",\"f\":\"",
           M, P, N + t, KC + sp, D, d2, sp, t, (unsigned long long)H, (unsigned long long)HC, (unsigned long long)HS);
    for (int j = 1; j < P; j++) printf("%s%x", j > 1 ? "," : "", f[j]);
    printf("\",\"V\":\"");
    for (int l = 0; l < sp; l++) printf("%s%x", l ? "," : "", V[l]);
    printf("\",\"T\":\"");
    for (int c = 1; c < (1 << sp); c++) printf("%s%d", c > 1 ? "," : "", TCOLS[c]);
    printf("\"}\n");
    fflush(stdout);
}

/* evaluate all tails for the current tables; Wm computed inside */
static void x_tails(const u32 *f, int tmax, int d2) {
    int ns = 1 << SS;
    int Wm[1 << 12];
    coset_minima(Wm);
    /* sp = 1 */
    int bestr = 1;
    for (int r = 1; r < ns; r++) if (Wm[r] > Wm[bestr]) bestr = r;
    for (int t = 0; t <= tmax && t < XT; t++) {
        int D = Wm[bestr] + t;
        if (D > d2) D = d2;
        if (D > XBEST[1][t]) {
            XBEST[1][t] = D;
            u32 V[1] = {(u32)bestr};
            memset(TCOLS, 0, sizeof TCOLS);
            TCOLS[1] = t;
            x_report(1, t, D, d2, f, V);
        }
    }
    if (SS < 2) return;
    /* sp = 2: all pairs r1 < r2 (closed form), keep top pairs for sp = 3 */
    int topn = 0;
    int topr1[24], topr2[24], tops[24];
    for (int r1 = 1; r1 < ns; r1++)
        for (int r2 = r1 + 1; r2 < ns; r2++) {
            int r3 = r1 ^ r2;
            int w1 = Wm[r1], w2 = Wm[r2], w3 = Wm[r3];
            int score = (w1 < w2 ? w1 : w2);
            if (w3 < score) score = w3;
            score = score * 4096 + w1 + w2 + w3;
            if (topn < 24) { topr1[topn] = r1; topr2[topn] = r2; tops[topn] = score; topn++; }
            else {
                int mi = 0;
                for (int q = 1; q < 24; q++) if (tops[q] < tops[mi]) mi = q;
                if (score > tops[mi]) { topr1[mi] = r1; topr2[mi] = r2; tops[mi] = score; }
            }
            for (int t = 0; t <= tmax && t < XT; t++) {
                /* max D <= d2 with max(R) <= t and R1+R2+R3 <= 2t */
                for (int D = d2; D > XBEST[2][t]; D--) {
                    int R1 = D - w1 > 0 ? D - w1 : 0, R2 = D - w2 > 0 ? D - w2 : 0, R3 = D - w3 > 0 ? D - w3 : 0;
                    int mx = R1 > R2 ? R1 : R2;
                    if (R3 > mx) mx = R3;
                    if (mx <= t && R1 + R2 + R3 <= 2 * t) {
                        XBEST[2][t] = D;
                        int Wl[4] = {0, w1, w2, w3};
                        tail_feasible(2, Wl, D, t);
                        u32 V[2] = {(u32)r1, (u32)r2};
                        x_report(2, t, D, d2, f, V);
                        break;
                    }
                }
            }
        }
    if (SS < 3) return;
    /* sp = 3: extend the top pairs */
    for (int q = 0; q < topn; q++) {
        int r1 = topr1[q], r2 = topr2[q];
        for (int r3 = 1; r3 < ns; r3++) {
            if (r3 == r1 || r3 == r2 || r3 == (r1 ^ r2)) continue;
            int Wl[8];
            for (int l = 1; l < 8; l++) {
                int r = ((l & 1) ? r1 : 0) ^ ((l & 2) ? r2 : 0) ^ ((l & 4) ? r3 : 0);
                Wl[l] = Wm[r];
            }
            for (int t = 0; t <= tmax && t < XT; t++) {
                for (int D = d2; D > XBEST[3][t]; D--) {
                    if (tail_feasible(3, Wl, D, t)) {
                        XBEST[3][t] = D;
                        u32 V[3] = {(u32)r1, (u32)r2, (u32)r3};
                        x_report(3, t, D, d2, f, V);
                        break;
                    }
                }
            }
        }
    }
}

static u64 clmul(u64 a, u64 b) { u64 r = 0; while (b) { if (b & 1) r ^= a; b >>= 1; a <<= 1; } return r; }

static void x_search(double secs, int tmax, int ncore, int nlift) {
    double t0 = now();
    for (int a = 0; a < 4; a++) for (int t = 0; t < XT; t++) XBEST[a][t] = 0;
    /* stage 1: hill-climb cores on (d2, -A2) for 60% of the time; keep the top ncore distinct cores */
    u32 cores[64][16];
    int cored[64];
    u64 coreA[64];
    int nc = 0;
    u32 f[16];
    double t1 = t0 + 0.6 * secs;
    long evals = 0;
    while (now() < t1) {
        f[0] = 1;
        for (int j = 1; j < P; j++) f[j] = (u32)smod(rand_elem(), HC);
        build_tables(f);
        u64 A;
        int dmin = nc ? cored[nc - 1] - 1 : 0;
        if (dmin < 0) dmin = 0;
        int d = evaluate_sub(dmin, ~0ULL, &A);
        evals++;
        if (d < 0) continue;
        int cd = d;
        u64 cA = A;
        int improved = 1;
        while (improved && now() < t1) {
            improved = 0;
            int order[512], nn = 0;
            for (int j = 1; j < P; j++) for (int i = 0; i < KC; i++) order[nn++] = j * 32 + i;
            for (int x = nn - 1; x > 0; x--) { int y = (int)(rnd() % (x + 1)); int tmp = order[x]; order[x] = order[y]; order[y] = tmp; }
            for (int x = 0; x < nn; x++) {
                int j = order[x] / 32, i = order[x] % 32;
                f[j] ^= 1u << i;
                if (f[j] == 0) { f[j] ^= 1u << i; continue; }
                build_tables(f);
                u64 A2;
                int d2 = evaluate_sub(cd, cA > 0 ? cA - 1 : 0, &A2);
                evals++;
                if (d2 > cd || (d2 == cd && A2 < cA)) { cd = d2; cA = A2; improved = 1; break; }
                f[j] ^= 1u << i;
            }
        }
        /* insert into sorted top list (by d desc, A asc), skip duplicates */
        int dup = 0;
        for (int q = 0; q < nc; q++) if (cored[q] == cd && coreA[q] == cA) { dup = 1; break; }
        if (dup) continue;
        if (nc < ncore || cd > cored[nc - 1] || (cd == cored[nc - 1] && cA < coreA[nc - 1])) {
            int pos = nc < ncore ? nc++ : nc - 1;
            while (pos > 0 && (cored[pos - 1] < cd || (cored[pos - 1] == cd && coreA[pos - 1] > cA))) {
                memcpy(cores[pos], cores[pos - 1], sizeof cores[0]); cored[pos] = cored[pos - 1]; coreA[pos] = coreA[pos - 1]; pos--;
            }
            memcpy(cores[pos], f, sizeof cores[0]); cored[pos] = cd; coreA[pos] = cA;
        }
    }
    fprintf(stderr, "stage1 evals=%ld cores=%d best d2=%d A2=%llu (KC=%d S=%d K=%d reps=%u sub-reps=%u)\n", evals, nc,
            nc ? cored[0] : -1, nc ? (unsigned long long)coreA[0] : 0ULL, KC, SS, K, NREPS, NR0);
    for (int q = 0; q < nc; q++) printf("{\"tag\":\"core\",\"d2\":%d,\"A2\":%llu}\n", cored[q], (unsigned long long)coreA[q]);
    fflush(stdout);
    /* stage 2: lifts */
    u64 total = 1;
    for (int j = 1; j < P; j++) { total <<= SS; if (total > (1ULL << 40)) break; }
    long lifts = 0;
    for (int q = 0; q < nc && now() - t0 < secs; q++) {
        u64 nl = total <= (u64)nlift ? total : (u64)nlift;
        for (u64 li = 0; li < nl && now() - t0 < secs; li++) {
            u64 code = total <= (u64)nlift ? li : rnd();
            f[0] = 1;
            for (int j = 1; j < P; j++) {
                u32 u = (u32)(code & ((1ULL << SS) - 1));
                code >>= SS;
                f[j] = (u32)(smod(cores[q][j], HC) ^ clmul(u, HC));
            }
            build_tables(f);
            x_tails(f, tmax, cored[q]);
            lifts++;
        }
    }
    fprintf(stderr, "stage2 lifts=%ld time=%.1f\n", lifts, now() - t0);
}

/* emit the X code: f list, V list (residues), T counts per column type (sp<=3) */
static void x_emit(const u32 *f, int sp, const u32 *V, const int *tcnt) {
    build_tables(f);
    int t = 0;
    for (int c = 1; c < (1 << sp); c++) t += tcnt[c];
    int n = N + t, k = KC + sp;
    printf("{\"n\":%d,\"k\":%d,\"construction\":\"QC index %d m=%d h=%llx (core %llx, sub %llx) + Construction X tail t=%d\",\"G\":[\n",
           n, k, P, M, (unsigned long long)H, (unsigned long long)HC, (unsigned long long)HS, t);
    for (int r = 0; r < k; r++) {
        u32 a;
        int lam = 0;
        if (r < KC) a = (u32)clmul(1ULL << r, HS); /* HS * x^r, degree < K */
        else { a = V[r - KC]; lam = 1 << (r - KC); }
        u64 cw[4] = {0, 0, 0, 0};
        for (int i = 0; i < K; i++) if ((a >> i) & 1) for (int w = 0; w < 4; w++) cw[w] ^= ROWS[i][w];
        printf("[");
        for (int c = 0; c < N; c++) printf("%s%d", c ? "," : "", (int)((cw[c >> 6] >> (c & 63)) & 1));
        for (int ty = 1; ty < (1 << sp); ty++)
            for (int q = 0; q < tcnt[ty]; q++)
                printf(",%d", (r >= KC) ? __builtin_parity(lam & ty) : 0);
        printf("]%s\n", r + 1 < k ? "," : "");
    }
    printf("]}\n");
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: see header\n"); return 1; }
    const char *mode = argv[1];
    int m = atoi(argv[2]);
    if (!strcmp(mode, "factor")) {
        factor_xm1(m);
        printf("m=%d factors(deg<=26)=%d\n", m, NF);
        for (int i = 0; i < NF; i++) printf("%d %d %llx\n", i, FDEG[i], (unsigned long long)FAC[i]);
        return 0;
    }
    if (!strcmp(mode, "hlist")) {
        /* canonical factor subsets of total degree k up to the multiplier action x -> x^u, gcd(u,m)=1 */
        int k = atoi(argv[3]);
        factor_xm1(m);
        int perm[64][128];
        int nu = 0;
        for (int u = 1; u < m && nu < 64; u++) {
            int a = u, b = m;
            while (b) { int t = a % b; a = b; b = t; }
            if (a != 1) continue;
            /* skip u in <2> coset duplicates crudely: keep all, cheap */
            int uinv = 1;
            while ((uinv * u) % m != 1) uinv++;
            int ok = 1;
            for (int i = 0; i < NF; i++) {
                int img = -1;
                for (int t = 0; t < NF; t++) {
                    if (FDEG[t] != FDEG[i]) continue;
                    /* does FAC[t] divide FAC[i](x^uinv)? evaluate FAC[i] at y = x^uinv mod FAC[t] */
                    u64 y = xm_mod(uinv, FAC[t]);
                    u64 acc = 0;
                    for (int e = FDEG[i]; e >= 0; e--) {
                        acc = smulmod(acc, y, FAC[t]);
                        if ((FAC[i] >> e) & 1) acc ^= smod(1, FAC[t]);
                    }
                    if (acc == 0) { img = t; break; }
                }
                if (img < 0) { ok = 0; break; }
                perm[nu][i] = img;
            }
            if (ok) nu++;
        }
        if (NF > 40) { fprintf(stderr, "too many factors\n"); return 1; }
        /* enumerate subsets by recursion over factor indices with degree sum k */
        int cnt = 0;
        u64 maxmask = 1ULL << NF;
        for (u64 mask = 1; mask < maxmask; mask++) {
            int dsum = 0;
            for (int i = 0; i < NF; i++) if ((mask >> i) & 1) dsum += FDEG[i];
            if (dsum != k) continue;
            int canon = 1;
            for (int t = 0; t < nu && canon; t++) {
                u64 im = 0;
                for (int i = 0; i < NF; i++) if ((mask >> i) & 1) im |= 1ULL << perm[t][i];
                if (im < mask) canon = 0;
            }
            if (canon) { printf("%llx\n", (unsigned long long)mask); cnt++; }
        }
        fprintf(stderr, "m=%d k=%d canonical h: %d (multipliers used %d)\n", m, k, cnt, nu);
        return 0;
    }
    if (!strcmp(mode, "xs") || !strcmp(mode, "xemit")) {
        /* qcs xs m coremask submask p secs seed tmax ncore nlift
           qcs xemit m coremask submask p f1,f2.. V1,V2.. T1,T2,.. (T counts per column type 1..2^sp-1) */
        u64 cm = strtoull(argv[3], NULL, 16), sm = strtoull(argv[4], NULL, 16);
        int pp = atoi(argv[5]);
        if (!setup(m, cm | sm, pp)) return 1;
        build_reps();
        x_setup(cm, sm);
        if (!strcmp(mode, "xs")) {
            double secs = atof(argv[6]);
            u64 seed = strtoull(argv[7], NULL, 10);
            int tmax = atoi(argv[8]), ncore = atoi(argv[9]), nlift = atoi(argv[10]);
            rs0 ^= seed * 0x9E3779B97F4A7C15ULL;
            rs1 ^= seed * 0xBF58476D1CE4E5B9ULL + 1;
            for (int i = 0; i < 20; i++) rnd();
            if (ncore > 64) ncore = 64;
            x_search(secs, tmax, ncore, nlift);
            return 0;
        }
        u32 f[32];
        if (!parse_f(argv[6], f)) { fprintf(stderr, "bad f\n"); return 1; }
        u32 V[8];
        int sp = 0;
        const char *c = argv[7];
        while (*c) { V[sp++] = (u32)strtoul(c, (char **)&c, 16); if (*c == ',') c++; }
        int tc[8] = {0};
        c = argv[8];
        int ty = 1;
        while (*c && ty < 8) { tc[ty++] = (int)strtol(c, (char **)&c, 10); if (*c == ',') c++; }
        x_emit(f, sp, V, tc);
        return 0;
    }
    u64 facmask = strtoull(argv[3], NULL, 16);
    int p = atoi(argv[4]);
    if (!setup(m, facmask, p)) return 1;
    if (!strcmp(mode, "emit") || !strcmp(mode, "eval")) {
        u32 f[32];
        if (!parse_f(argv[5], f)) { fprintf(stderr, "bad f list\n"); return 1; }
        build_reps();
        build_tables(f);
        if (!strcmp(mode, "eval")) {
            if (getenv("TAILT")) TAILT = atoi(getenv("TAILT"));
            u64 A = 0;
            int d = evaluate(0, 0, &A);
            print_code("eval", d, A, f, 0.0);
            return 0;
        }
        int tt = getenv("TAILT") ? atoi(getenv("TAILT")) : 0;
        printf("{\"n\":%d,\"k\":%d,\"construction\":\"QC index %d, m=%d, h=%llx, f=", N + tt, K, P, M, (unsigned long long)H);
        for (int j = 1; j < P; j++) printf("%s%x", j > 1 ? "," : "", f[j]);
        printf(", tail of %d all-ones columns (Construction X on the x+1 component)\",\"G\":[\n", tt);
        for (int i = 0; i < K; i++) {
            printf("[");
            for (int c = 0; c < N; c++) printf("%d%s", (int)((ROWS[i][c >> 6] >> (c & 63)) & 1), c + 1 < N ? "," : "");
            for (int c = 0; c < tt; c++) printf(",1");
            printf("]%s\n", i + 1 < K ? "," : "");
        }
        printf("]}\n");
        return 0;
    }
    if (!strcmp(mode, "search2")) {
        /* iterated local search: qcs search2 m facmask p secs seed dtarget [startf]; env TAILT=t adds the X tail */
        if (getenv("TAILT")) TAILT = atoi(getenv("TAILT"));
        if (TAILT && __builtin_parityll(H)) { fprintf(stderr, "h(1) != 0: x+1 does not divide h\n"); return 1; }
        double secs = atof(argv[5]);
        u64 seed = strtoull(argv[6], NULL, 10);
        int dtarget = atoi(argv[7]);
        rs0 ^= seed * 0x9E3779B97F4A7C15ULL;
        rs1 ^= seed * 0xBF58476D1CE4E5B9ULL + 1;
        for (int i = 0; i < 20; i++) rnd();
        double t0 = now();
        build_reps();
        fprintf(stderr, "m=%d k=%d p=%d n=%d h=%llx reps=%u setup=%.2fs\n", M, K, P, N, (unsigned long long)H, NREPS, now() - t0);
        u32 f[32], bf[32], cf[32];
        int bd = 0, cdd = 0;
        u64 bA = ~0ULL, cAA = ~0ULL;
        long evals = 0, climbs = 0;
        int have = 0;
        if (argc > 8) { if (parse_f(argv[8], cf)) { build_tables(cf); u64 A; cdd = evaluate(0, 0, &A); cAA = A; memcpy(bf, cf, sizeof cf); bd = cdd; bA = cAA; have = 1; } }
        while (now() - t0 < secs) {
            climbs++;
            if (!have || rnd() % 16 == 0) {
                f[0] = 1;
                for (int j = 1; j < P; j++) f[j] = rand_elem();
            } else {
                memcpy(f, (rnd() % 4 == 0) ? bf : cf, sizeof f);
                int r = 1 + (int)(rnd() % 4);
                for (int q = 0; q < r; q++) {
                    int j = 1 + (int)(rnd() % (P - 1)), i = (int)(rnd() % K);
                    f[j] ^= 1u << i;
                    if (f[j] == 0) f[j] = 1;
                }
            }
            build_tables(f);
            u64 A;
            int dmin = bd > 3 ? bd - 3 : 0;
            int d = evaluate(dmin, ~0ULL, &A);
            evals++;
            if (d < 0) continue;
            int cd = d;
            u64 cA = A;
            int improved = 1;
            while (improved && now() - t0 < secs) {
                improved = 0;
                int order[32 * 16];
                int nn = 0;
                for (int j = 1; j < P; j++)
                    for (int i = 0; i < K; i++) order[nn++] = j * 32 + i;
                for (int x = nn - 1; x > 0; x--) { int y = (int)(rnd() % (x + 1)); int tmp = order[x]; order[x] = order[y]; order[y] = tmp; }
                for (int x = 0; x < nn; x++) {
                    int j = order[x] / 32, i = order[x] % 32;
                    f[j] ^= 1u << i;
                    if (f[j] == 0) { f[j] ^= 1u << i; continue; }
                    build_tables(f);
                    u64 A2;
                    int d2 = evaluate(cd, cA > 0 ? cA - 1 : 0, &A2);
                    evals++;
                    if (d2 > cd || (d2 == cd && A2 < cA)) { cd = d2; cA = A2; improved = 1; break; }
                    f[j] ^= 1u << i;
                }
            }
            /* accept as current if not worse than current (allows drift on plateaus) */
            if (!have || cd > cdd || (cd == cdd && cA <= cAA) || rnd() % 32 == 0) { memcpy(cf, f, sizeof f); cdd = cd; cAA = cA; have = 1; }
            if (cd > bd || (cd == bd && cA < bA)) {
                bd = cd; bA = cA;
                memcpy(bf, f, sizeof f);
                print_code(bd >= dtarget ? "TARGET" : "best", bd, bA, bf, now() - t0);
            }
        }
        fprintf(stderr, "done evals=%ld climbs=%ld best d=%d A=%llu time=%.1f\n", evals, climbs, bd, (unsigned long long)bA, now() - t0);
        print_code("final", bd, bA, bf, now() - t0);
        return 0;
    }
    if (!strcmp(mode, "search")) {
        double secs = atof(argv[5]);
        u64 seed = strtoull(argv[6], NULL, 10);
        int dstop = argc > 7 ? atoi(argv[7]) : 9999;
        rs0 ^= seed * 0x9E3779B97F4A7C15ULL;
        rs1 ^= seed * 0xBF58476D1CE4E5B9ULL + 1;
        for (int i = 0; i < 20; i++) rnd();
        double t0 = now();
        build_reps();
        fprintf(stderr, "m=%d k=%d p=%d n=%d h=%llx reps=%u setup=%.2fs\n", M, K, P, N, (unsigned long long)H, NREPS, now() - t0);
        u32 f[32], bf[32];
        int bd = 0;
        u64 bA = ~0ULL;
        long evals = 0, restarts = 0;
        while (now() - t0 < secs) {
            restarts++;
            f[0] = 1;
            for (int j = 1; j < P; j++) f[j] = rand_elem();
            build_tables(f);
            u64 A;
            /* only climb from starts that are within 2 of the best */
            int dmin = bd > 2 ? bd - 2 : 0;
            int d = evaluate(dmin, ~0ULL, &A);
            evals++;
            if (d < 0) continue;
            int cd = d;
            u64 cA = A;
            int improved = 1;
            while (improved && now() - t0 < secs) {
                improved = 0;
                int order[32 * 16];
                int nn = 0;
                for (int j = 1; j < P; j++)
                    for (int i = 0; i < K; i++) order[nn++] = j * 32 + i;
                for (int x = nn - 1; x > 0; x--) { int y = (int)(rnd() % (x + 1)); int tmp = order[x]; order[x] = order[y]; order[y] = tmp; }
                for (int x = 0; x < nn; x++) {
                    int j = order[x] / 32, i = order[x] % 32;
                    f[j] ^= 1u << i;
                    if (f[j] == 0) { f[j] ^= 1u << i; continue; }
                    build_tables(f);
                    u64 A2;
                    int d2 = evaluate(cd, cA - 1 < cA ? cA - 1 : 0, &A2);
                    evals++;
                    if (d2 > cd || (d2 == cd && A2 < cA)) {
                        cd = d2;
                        cA = A2;
                        improved = 1;
                        break;
                    }
                    f[j] ^= 1u << i;
                }
            }
            if (cd > bd || (cd == bd && cA < bA)) {
                bd = cd;
                bA = cA;
                memcpy(bf, f, sizeof f);
                print_code("best", bd, bA, bf, now() - t0);
                if (bd >= dstop) break;
            }
        }
        fprintf(stderr, "done evals=%ld restarts=%ld best d=%d A=%llu time=%.1f\n", evals, restarts, bd, (unsigned long long)bA, now() - t0);
        print_code("final", bd, bA, bf, now() - t0);
        return 0;
    }
    fprintf(stderr, "unknown mode\n");
    return 1;
}
