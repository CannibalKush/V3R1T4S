/* lcrt5.c (r2) -- lcrt.c (r1, sha 2eca0809...) + an exact segmented sieve beyond the main sieve (C2 ranges, children
 *   scans and lo beyond the sieve no longer abort); output adds the diagnostics seg_c2, seg_ch.  Otherwise unchanged.
 * lcrt.c -- spec LCRT-1 = LCAP-1 (10-06 SPEC_LCAP1.md) + the CRT prune.  C + GMP, exact for every X.
 *
 * Search: all C-sequences of primes PMIN <= p_1 < ... < p_w (w >= 2) with P = prod p <= X and
 *         P - 2*Phi = SIGMA (Phi = prod (p-1)).  SIGMA=+1 is the Lehmer case k=2 (the certificate);
 *         SIGMA=-1 is the companion N+1 = 2 phi(N) (regression, known solutions); other odd SIGMA = planted tests.
 *
 * Tree (exactly LCAP-1): node = prefix with A = 2 Phi - P > 0; lo = max(p_last+1, floor(2 Phi/A)+1);
 *   child q (prime, scanned upward from lo, scan STOPS at the first q failing (c3) or (c4)):
 *     (c1) q >= lo   (c2) gcd(q-1, P) = 1   (c3) P q pi1(q) pi2(q) <= X
 *     (c4) P q prod_{i<=m} pi_i(q) > (2 Phi (q-1) - [SIGMA<0]) prod_{i<=m} (pi_i(q)-1), m maximal with P q prod <= X
 *   C2 at every expanded node: primes q in [qa,qb] (q >= lo, h(q) = A q^2 - 4 Phi q + 2 Phi + SIGMA < 0,
 *     P q n(q) <= X u(q), q <= isqrt(X/P)), u = A q - 2 Phi, n = 2 Phi (q-1) - SIGMA; admissible gcd(q-1,P)=1;
 *     integral u | n  -> EVENT.
 * CRT prune (new): after the LCAP-1 shortcut "lo > isqrt(X/P) => return", a node is EXPANDED (C2 + children) only if
 *   some Q == SIGMA * P^{-1} (mod 8 Phi) lies in [lo (lo+2), floor(X/P)].  Otherwise it is counted as PRUNED.
 *   Soundness: a completion through an LCAP-1 node has m >= 2 further odd primes r_i, N = P Q, Q = prod r_i, and
 *   N - SIGMA = 2 Phi prod (r_i - 1) with 4 | prod (r_i - 1); gcd(P, 8 Phi) = 1 (C-sequence, P odd); Q <= X/P;
 *   r_1 >= lo (proper-prefix rule (c1)), r_2 >= r_1 + 2.
 *
 * Decisions are exact: mpz arithmetic; doubles only as filters that decide when the estimate is > 1e-9 relative away
 * from the threshold (accumulated relative error of <= 64 double ops is < 64 * 2^-52 < 1.5e-14), else exact mpz.
 *
 * Canonical output per task (JSON line): nodes[d] (visited nodes per depth), pruned[d], c2p[d], c2a[d], c2i[d],
 *   digest = sum H(P) mod 2^64 over visited nodes, H(P) = splitmix64(lo64(P) ^ splitmix64(bits 64..127 of P)),
 *   crt_tests, crt_skip, maxq, events.
 *
 * Build: clang -O3 -o lcrt lcrt.c -I/opt/homebrew/include -L/opt/homebrew/lib -lgmp
 * Usage: lcrt X_decimal SIEVE_LIMIT D0 WORKERS OUTDIR [SIGMA=1] [PMIN=5] [CRT=1] [KMAX=32] [FILT=1]
 * FILT = 1 (LCRT-3): at EVERY live node the candidates form the AP Q1 + k*8Phi (0 <= k < K); a child q is visited only
 *   if q divides one of them (k0 = -Q1/(8Phi) mod q < K), a necessary condition for the child to be live.
 * KMAX > 0 (LCRT-2): a live node with K <= KMAX candidates is closed by the candidate closure (m = 2 by a perfect-square
 *   test per candidate; m >= 3 via the LCAP-1 children that divide a candidate).  KMAX = 0: plain LCRT-1.
 *   The set of LIVE nodes (nodes passing the CRT test) and its digest are identical for every KMAX (canonical).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <time.h>
#include <dirent.h>
#include <gmp.h>

typedef uint64_t u64;
typedef uint32_t u32;
#define MAXD 64

static mpz_t X; static double Xd;
static long SIGMA = 1; static mpz_t SIG; static u64 PMIN = 5; static int CRT = 1;   /* SIG = sigma (exact); SIGMA = its sign */
static u32 *PR; static int64_t NPR;
static u64 pre[MAXD], lem[MAXD];

typedef struct {
    u64 nodes[MAXD], pruned[MAXD], c2p[MAXD], c2a[MAXD], c2i[MAXD];
    u64 live[MAXD], small[MAXD], cand[MAXD], sqhit[MAXD], kfilt[MAXD], eclosed[MAXD], epass[MAXD];
    u64 digest, digest_live, maxq, crt_tests, crt_skip;
    u64 tdrej[MAXD];               /* r2 LCRT-6: Euler-closure candidates rejected by trial division (prime < lo) */
    u64 c2k[MAXD];                 /* r2 LCRT-5: live large-regime nodes whose m = 2 part was done by the candidate
                                      closure instead of the C2 prime loop (their candidates/hits go to cand/sqhit) */
    u64 seg_c2, seg_ch;            /* r2 diagnostics: primes delivered by the segmented sieve (beyond the main sieve)
                                      to C2 ranges / to children scans */
} Stats;
#define KMAXMAX 64
static int KMAX = 32;              /* candidate-closure threshold; 0 = plain LCRT-1 (C2 + all children at live nodes) */
static int FILT = 1;               /* LCRT-3: filter the children of EVERY live node by the candidate AP (one mod test) */
static int EULER = 1;              /* LCRT-4: small-regime nodes first Euler-test their K candidates N = P Q:
                                      a genuine completion has N - sigma = 2 phi(N), so 2^((N-sigma)/2) == 1 (mod N);
                                      if every candidate fails, the node is closed (all m >= 2) */
static u64 C2CAND = 0;             /* r2 LCRT-5 (argv[13], 0 = off = LCRT-4): at a live large-regime node with K candidates
                                      and C2 interval [qa, qb], if K * C2CAND < qb - qa + 1 the m = 2 completions are found
                                      by the perfect-square test on the K candidates instead of the C2 prime loop */
static u64 TDIV = 0;               /* r2 LCRT-6 (argv[14], 0 = off): before the Euler test, a candidate Q divisible by a
                                      prime p < min(lo, TDIV) is rejected (every prime factor of a genuine cofactor
                                      Q = r_1 ... r_m is >= r_1 >= lo) */
static u64 TDG[256]; static int TDGN = 0; static u32 TDP[256][16]; static int TDPN[256];   /* prime groups, product < 2^64 */
static int CQMODE = 0;             /* cross-check mode: reimplementation of LCAP-CQ (1) / LCAP-CQ2 (2)
                                      from a separate formalization effort's spec; stats: pruned=DEAD, small=UNIQUE|MULTI, live=SCAN,
                                      cand=#candidates Euler-tested, sqhit=#Euler passes */

static mpz_t CAND[MAXD][KMAXMAX], PSI, WW, DISC, SQ, R1, R2, TPH;
static Stats S;
static char evbuf[1 << 20]; static size_t evlen = 0; static int nev = 0;

/* per-depth scratch */
static mpz_t LOZ_J[MAXD];
static mpz_t PP[MAXD], FF[MAXD], AA[MAXD], T1, T2, T3, T4, T5, T6, QLO, QHI, MM, Q0, TWOPHI, LOZ, QMZ;

typedef struct { int j; u64 pref[MAXD]; } Task;
static Task *tasks; static int64_t ntasks = 0, captasks = 0;
static int D0 = 1 << 30;

static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(2); }
static mpz_t CQ1[MAXD]; static u64 CK[MAXD];   /* live node's candidate AP: Q1 + k*8Phi, 0 <= k < K (K saturated) */
static inline u64 invmod_u64(u64 a, u64 m) {   /* a^{-1} mod m, gcd(a,m) = 1, m < 2^63 */
    int64_t t = 0, nt = 1; int64_t r = (int64_t)m, nr = (int64_t)(a % m);
    while (nr) { int64_t qq = r / nr, tmp; tmp = t - qq * nt; t = nt; nt = tmp; tmp = r - qq * nr; r = nr; nr = tmp; }
    if (r != 1) die("invmod: not invertible");
    if (t < 0) t += (int64_t)m;
    return (u64)t;
}
/* does the prime q divide some candidate Q1 + k*8Phi (0 <= k < K) of live node j?  (necessary for child q to be live) */
static int child_may_live(int j, u64 q) {
    if (CK[j] >= q) return 1;
    u64 r1 = mpz_fdiv_ui(CQ1[j], q);
    u64 m = (u64)(((unsigned __int128)8 * mpz_fdiv_ui(FF[j], q)) % q);
    if (r1 == 0) return 1;
    if (CK[j] <= 16) {
        u64 t = r1;
        for (u64 k = 1; k < CK[j]; k++) { t += m; if (t >= q) t -= q; if (t == 0) return 1; }
        return 0;
    }
    u64 k0 = (u64)(((unsigned __int128)(q - r1) * invmod_u64(m, q)) % q);
    return k0 < CK[j];
}

static inline u64 splitmix64(u64 x) {
    x += 0x9E3779B97F4A7C15ULL;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}
static u64 limb64(const mpz_t z, int k) {          /* bits 64k .. 64k+63 of z >= 0 */
    mpz_tdiv_q_2exp(T6, z, 64 * k);
    return (u64)mpz_getlimbn(T6, 0) | (sizeof(mp_limb_t) < 8 ? ((u64)mpz_getlimbn(T6, 1) << 32) : 0);
}
static inline u64 Hh(const mpz_t P) { return splitmix64(limb64(P, 0) ^ splitmix64(limb64(P, 1))); }

static int64_t lower_bound(u64 v) {
    int64_t a = 0, b = NPR;
    while (a < b) { int64_t m = (a + b) >> 1; if (PR[m] < v) a = m + 1; else b = m; }
    return a;
}
static inline int adm(u64 qm1, int j) {   /* no prefix prime divides q-1 (Lemire; q-1, p < 2^32) */
    for (int i = 0; i < j; i++) if (qm1 * lem[i] <= lem[i] - 1) return 0;
    return 1;
}
/* r2: same test for any q-1 < 2^64 (the Lemire test above is exact only for q-1 < 2^32; every prefix prime is < q) */
static inline int adm64(u64 qm1, int j) {
    if (qm1 < ((u64)1 << 32)) return adm(qm1, j);
    for (int i = 0; i < j; i++) if (qm1 % pre[i] == 0) return 0;
    return 1;
}

/* ---------------- r2: exact segmented sieve beyond the main sieve ----------------
 * Primes above PR[NPR-1] are produced on demand by sieving odd numbers in [a, b] with the base primes PR[i] <= isqrt(b)
 * (abort, never truncate, if isqrt(b) > PR[NPR-1]).  C2 ranges stream them; children scans use a per-depth stream with
 * a lookahead buffer (rules (c3)/(c4) at q need the next m primes after q). */
#define SEGW ((u64)1 << 20)                /* odd numbers per segment (2^21 integers) */
#define LOOK 128                           /* lookahead primes guaranteed to a children-scan test */
static unsigned char *SEGB;                /* segment scratch, used only inside seg_primes() */
static u64 *C2BUF;                         /* primes of one C2 segment */
static inline u64 isqrt_u64(u64 n) {
    long double s = sqrtl((long double)n);
    u64 r = (s >= 4294967295.0L) ? 4294967295ULL : (u64)s;
    while (r * r > n) r--;
    while (r < 4294967295ULL && (r + 1) * (r + 1) <= n) r++;
    return r;
}
/* all primes in [a, b] (a odd, a > PR[NPR-1], b - a < 2*SEGW, b < 2^63) written to out[] in increasing order */
static int64_t seg_primes(u64 a, u64 b, u64 *out) {
    if (!(a & 1) || a <= (u64)PR[NPR - 1] || b < a || b - a >= 2 * SEGW || b >= ((u64)1 << 63)) die("seg_primes: bad range");
    u64 nb = (b - a) / 2 + 1;              /* odd numbers a, a+2, ..., <= b */
    u64 rb = isqrt_u64(b);
    if (rb > (u64)PR[NPR - 1]) die("segmented sieve: base primes too small (main sieve must reach isqrt(q))");
    memset(SEGB, 0, nb);
    for (int64_t i = 0; i < NPR; i++) {     /* PR holds the primes >= 3 */
        u64 p = PR[i];
        if (p > rb) break;
        u64 s = p * p;
        if (s < a) { s = a + (p - a % p) % p; if (!(s & 1)) s += p; }
        for (u64 x = s; x <= b; x += 2 * p) SEGB[(x - a) >> 1] = 1;
    }
    int64_t c = 0;
    for (u64 k = 0; k < nb; k++) if (!SEGB[k]) out[c++] = a + 2 * k;
    return c;
}
/* increasing stream of ALL primes >= start: first from PR, then from the segmented sieve */
typedef struct { u64 *buf; int64_t n, pos, cap; u64 next, seg; } PStream;
static PStream PSJ[MAXD];
static void ps_init(PStream *s, u64 start) {
    if (!s->buf) { s->cap = (int64_t)SEGW + 70000; s->buf = malloc(s->cap * sizeof(u64)); if (!s->buf) die("malloc stream"); }
    s->n = s->pos = 0; s->next = start; s->seg = 4096;     /* segment length doubles per refill, up to SEGW odd numbers */
}
static void ps_refill(PStream *s) {
    if (s->pos > 0) { memmove(s->buf, s->buf + s->pos, (size_t)(s->n - s->pos) * sizeof(u64)); s->n -= s->pos; s->pos = 0; }
    u64 last = (u64)PR[NPR - 1];
    if (s->next <= last) {                 /* still inside the main sieve */
        int64_t i = lower_bound(s->next);
        int64_t cnt = NPR - i; if (cnt > 65536) cnt = 65536;
        for (int64_t k = 0; k < cnt; k++) s->buf[s->n++] = PR[i + k];
        s->next = (i + cnt < NPR) ? (u64)PR[i + cnt] : last + 1;
        return;
    }
    u64 a = s->next | 1;                   /* first odd number >= next (next > last >= 3) */
    u64 b = a + 2 * (s->seg - 1);
    s->n += seg_primes(a, b, s->buf + s->n);
    s->next = b + 1;
    if (s->seg < SEGW) s->seg <<= 1;
}
static inline void ps_ensure(PStream *s, int64_t look) { while (s->n - s->pos < look) ps_refill(s); }

static const char *EVVIA = "c2";    /* r2: which closure produced an event (reported only when C2CAND != 0) */
static void record_event_z(int j, const mpz_t qz, const mpz_t r, const mpz_t P) {
    const char *reason;
    if (mpz_cmp(r, qz) <= 0) reason = "r<=q";
    else {
        mpz_mul(T5, P, qz); mpz_mul(T5, T5, r);
        if (mpz_cmp(T5, X) > 0) reason = "cap";
        else {
            int ok = 1;
            mpz_sub_ui(T5, r, 1);
            for (int i = 0; i < j && ok; i++) if (mpz_divisible_ui_p(T5, pre[i])) ok = 0;
            if (ok && mpz_divisible_p(T5, qz)) ok = 0;
            if (!ok) reason = "C-violation";
            else reason = mpz_probab_prime_p(r, 50) ? "SOLUTION" : "r composite";
        }
    }
    char *rs = mpz_get_str(0, 10, r);
    if (evlen + 4096 + strlen(rs) > sizeof(evbuf)) die("event buffer full");
    evlen += sprintf(evbuf + evlen, "%s{\"prefix\":[", nev ? "," : "");
    for (int i = 0; i < j; i++) evlen += sprintf(evbuf + evlen, "%s%llu", i ? "," : "", (unsigned long long)pre[i]);
    char *qs = mpz_get_str(0, 10, qz);
    if (C2CAND) evlen += sprintf(evbuf + evlen, "],\"q\":%s,\"r\":%s,\"reason\":\"%s\",\"via\":\"%s\"}", qs, rs, reason, EVVIA);
    else evlen += sprintf(evbuf + evlen, "],\"q\":%s,\"r\":%s,\"reason\":\"%s\"}", qs, rs, reason);
    free(rs); free(qs); nev++;
}
static void record_event(int j, u64 q, const mpz_t r, const mpz_t P) {
    mpz_t qz; mpz_init_set_ui(qz, q); record_event_z(j, qz, r, P); mpz_clear(qz);
}
static int is_prime_z(const mpz_t z) {           /* exact below the sieve limit; above: MR (a 'no' is a proof) */
    if (mpz_cmp_ui(z, 3) < 0) return mpz_cmp_ui(z, 2) == 0;
    if (mpz_cmp_ui(z, (u64)PR[NPR - 1]) <= 0) {
        u64 v = mpz_get_ui(z);
        int64_t a = 0, b = NPR;
        while (a < b) { int64_t m = (a + b) >> 1; if (PR[m] < v) a = m + 1; else b = m; }
        return a < NPR && PR[a] == v;
    }
    return mpz_probab_prime_p(z, 50) > 0;
}

/* h(q) < 0 ? */
static int hneg(u64 q, const mpz_t A, const mpz_t Phi) {
    mpz_mul_ui(T1, A, q); mpz_mul_ui(T1, T1, q);              /* A q^2 */
    mpz_mul_2exp(T2, Phi, 1);                                  /* 2 Phi */
    mpz_add(T1, T1, T2);
    mpz_add(T1, T1, SIG);
    mpz_mul_2exp(T2, Phi, 2); mpz_mul_ui(T2, T2, q);           /* 4 Phi q */
    return mpz_cmp(T1, T2) < 0;
}
/* cap(q): P q n(q) <= X u(q) (requires u(q) > 0, i.e. q >= lo) */
static int capok(u64 q, const mpz_t P, const mpz_t A, const mpz_t Phi) {
    mpz_mul_2exp(T1, Phi, 1); mpz_mul_ui(T1, T1, q - 1);      /* 2 Phi (q-1) */
    mpz_sub(T1, T1, SIG);
    mpz_mul(T1, T1, P); mpz_mul_ui(T1, T1, q);                 /* P q n */
    mpz_mul_ui(T2, A, q); mpz_submul_ui(T2, Phi, 2);           /* u = A q - 2 Phi */
    mpz_mul(T2, T2, X);
    return mpz_cmp(T1, T2) <= 0;
}

/* one C2 prime q: admissible (gcd(q-1, P) = 1) and integral (u | n) test; integral -> event */
static inline void c2_one(int j, u64 q, const mpz_t P, const mpz_t Phi, const mpz_t A, u64 *na, u64 *ni) {
    if (!adm64(q - 1, j)) return;
    (*na)++;
    mpz_mul_ui(T1, A, q); mpz_submul_ui(T1, Phi, 2);          /* u */
    mpz_mul_2exp(T2, Phi, 1); mpz_mul_ui(T2, T2, q - 1);
    mpz_sub(T2, T2, SIG);                                      /* n */
    if (!mpz_divisible_p(T2, T1)) return;
    (*ni)++;
    mpz_t r; mpz_init(r); mpz_divexact(r, T2, T1);
    record_event(j, q, r, P);
    mpz_clear(r);
}

/* r2 LCRT-5: m = 2 completions of live node j through its K candidates Q = Q1 + k*8Phi (0 <= k < K).
 * A completion (q, r) (q prime >= lo, r > q, P q r <= X, P q r - 2 Phi (q-1)(r-1) = sigma; r is odd because
 * n = 2 Phi (q-1) - sigma is odd) has Q = q r == sigma P^{-1} (mod 8 Phi) (Lemma CRT, m = 2) and lo(lo+2) <= Q <= X/P,
 * so Q is a candidate; then Psi = (P Q - sigma)/(2 Phi) = (q-1)(r-1), q + r = Q - Psi + 1 and (q, r) are the roots of
 * t^2 - (Q - Psi + 1) t + Q.  Same events as the C2 prime loop over [qa, qb]. */
static mpz_t QC, MC;
static void c2_cand(int j, const mpz_t P, const mpz_t Phi) {
    u64 K = CK[j];
    u64 plast = j ? pre[j - 1] : PMIN - 1;
    S.c2k[j]++;
    mpz_mul_2exp(TPH, Phi, 1);
    mpz_mul_2exp(MC, Phi, 3);
    mpz_set(QC, CQ1[j]);
    for (u64 k = 0; k < K; k++) {
        if (k) mpz_add(QC, QC, MC);
        S.cand[j]++;
        mpz_mul(PSI, P, QC); mpz_sub(PSI, PSI, SIG);
        if (!mpz_divisible_p(PSI, TPH)) die("candidate not congruent (c2_cand)");
        mpz_divexact(PSI, PSI, TPH);
        mpz_sub(WW, QC, PSI); mpz_add_ui(WW, WW, 1);              /* r1 + r2 */
        mpz_mul(DISC, WW, WW); mpz_submul_ui(DISC, QC, 4);        /* (r2 - r1)^2 */
        if (mpz_sgn(DISC) <= 0 || !mpz_perfect_square_p(DISC)) continue;
        mpz_sqrt(SQ, DISC);
        mpz_sub(R1, WW, SQ);
        if (mpz_odd_p(R1)) continue;
        mpz_tdiv_q_2exp(R1, R1, 1); mpz_add(R2, WW, SQ); mpz_tdiv_q_2exp(R2, R2, 1);
        S.sqhit[j]++;
        if (mpz_cmp(R1, LOZ_J[j]) < 0 || mpz_cmp_ui(R1, plast) <= 0) continue;
        if (!is_prime_z(R1)) continue;
        int ok = 1; mpz_sub_ui(T5, R1, 1);
        for (int i = 0; i < j && ok; i++) if (mpz_divisible_ui_p(T5, pre[i])) ok = 0;
        if (!ok) continue;
        S.c2i[j]++;
        EVVIA = "c2cand"; record_event_z(j, R1, R2, P); EVVIA = "c2";
    }
}

static void c2(int j, const mpz_t P, const mpz_t Phi, const mpz_t A, u64 lo, u64 qmax0) {
    if (!hneg(lo, A, Phi)) return;
    /* qb = largest q in [lo, qmax0] with h(q) < 0; estimate q+ = (2 Phi + sqrt(D))/A, D = 4 Phi^2 - A (2 Phi + SIGMA) */
    u64 qb;
    {
        mpz_mul(T3, Phi, Phi); mpz_mul_2exp(T3, T3, 2);
        mpz_mul_2exp(T4, Phi, 1);
        mpz_add(T4, T4, SIG);
        mpz_mul(T4, T4, A); mpz_sub(T3, T3, T4);              /* D */
        if (mpz_sgn(T3) <= 0) return;
        mpz_sqrt(T3, T3); mpz_mul_2exp(T4, Phi, 1); mpz_add(T3, T3, T4); mpz_fdiv_q(T3, T3, A);
        if (mpz_cmp_ui(T3, qmax0) >= 0) qb = qmax0;
        else { qb = mpz_get_ui(T3); if (qb < lo) qb = lo; }
        while (qb > lo && !hneg(qb, A, Phi)) qb--;
        while (qb < qmax0 && hneg(qb + 1, A, Phi)) qb++;
    }
    if (!capok(qb, P, A, Phi)) return;
    /* qa = least q in [lo, qb] with cap(q) (cap set is a final segment): galloping down + bisection */
    u64 qa;
    if (capok(lo, P, A, Phi)) qa = lo;
    else {
        u64 good = qb, bad = lo, step = 1;
        for (;;) {
            u64 t = (good - bad > step) ? good - step : bad;
            if (t == bad) break;
            if (capok(t, P, A, Phi)) { good = t; step <<= 1; } else { bad = t; break; }
        }
        while (good - bad > 1) { u64 m = bad + ((good - bad) >> 1); if (capok(m, P, A, Phi)) good = m; else bad = m; }
        qa = good;
    }
    if (qb > S.maxq) S.maxq = qb;
    if (C2CAND && CRT && FILT && !CQMODE && CK[j] < ((u64)1 << 62) &&
        (unsigned __int128)CK[j] * C2CAND < (unsigned __int128)(qb - qa) + 1) { c2_cand(j, P, Phi); return; }
    /* r2: primes of [qa, qb] inside the main sieve from PR, the rest (if any) from the exact segmented sieve */
    u64 last = (u64)PR[NPR - 1];
    u64 qbs = qb < last ? qb : last;
    int64_t i0 = lower_bound(qa), i1 = lower_bound(qbs + 1);
    if (i1 < i0) i1 = i0;
    u64 na = 0, ni = 0, nseg = 0;
    for (int64_t i = i0; i < i1; i++) c2_one(j, PR[i], P, Phi, A, &na, &ni);
    if (qb > last) {
        u64 a = (qa > last) ? qa : last + 1;
        if (!(a & 1)) a++;
        time_t ts = time(0);
        while (a <= qb) {
            u64 b = a + 2 * (SEGW - 1); if (b > qb) b = qb;
            int64_t c = seg_primes(a, b, C2BUF);
            for (int64_t t = 0; t < c; t++) c2_one(j, C2BUF[t], P, Phi, A, &na, &ni);
            nseg += (u64)c;
            if (b >= qb) break;
            a = b + 2;                                         /* b is odd here (b = a + 2(SEGW-1)) */
        }
        S.seg_c2 += nseg;
        if (qb - ((qa > last) ? qa : last) > 100000000ULL) {
            fprintf(stderr, "SEGC2 depth %d prefix", j); for (int i = 0; i < j; i++) fprintf(stderr, " %llu", (unsigned long long)pre[i]);
            fprintf(stderr, " qa %llu qb %llu segprimes %llu (%lds)\n", (unsigned long long)qa, (unsigned long long)qb,
                    (unsigned long long)nseg, (long)(time(0) - ts));
        }
    }
    S.c2p[j] += (u64)(i1 - i0) + nseg; S.c2a[j] += na; S.c2i[j] += ni;
}

/* exact a*b <= X with a mpz, b u64, double filter */
static int mul_le_X_d(double ed, const mpz_t a, u64 b) {
    if (ed > Xd * (1 + 1e-9)) return 0;
    if (ed < Xd * (1 - 1e-9)) return 1;
    mpz_mul_ui(T5, a, b); return mpz_cmp(T5, X) <= 0;
}

static void children(int j, u64 lo, int filterK);
static void node(int j);

/* small regime: K candidates Q (all Q == SIGMA P^{-1} mod 8 Phi in [lo(lo+2), X/P]) stored in CAND[j][0..K-1].
 * m = 2 completions: Q = r1 r2, Psi = (P Q - SIGMA)/(2 Phi) = (r1-1)(r2-1) => r1 + r2 = Q - Psi + 1 => perfect square.
 * m >= 3 completions: first remaining prime q is an LCAP-1 child dividing its candidate Q (push-down filter). */
static int small_factor(const mpz_t Q, u64 lo) {       /* 1 iff some prime p < min(lo, TDIV) divides Q */
    for (int g = 0; g < TDGN; g++) {
        if (TDP[g][0] >= lo) return 0;
        u64 r = mpz_fdiv_ui(Q, TDG[g]);
        for (int i = 0; i < TDPN[g]; i++) { u64 p = TDP[g][i]; if (p >= lo) return 0; if (r % p == 0) return 1; }
    }
    return 0;
}
static void small_closure(int j, int K) {
    mpz_t *P = &PP[j], *Phi = &FF[j];
    u64 plast = j ? pre[j - 1] : PMIN - 1;
    if (EULER) {
        int pass = 0;
        u64 lo64 = TDIV ? mpz_get_ui(LOZ_J[j]) : 0;
        for (int k = 0; k < K; k++) {
            if (TDIV && small_factor(CAND[j][k], lo64)) { S.tdrej[j]++; continue; }
            mpz_mul(T3, *P, CAND[j][k]);                       /* N */
            mpz_sub(T4, T3, SIG); mpz_tdiv_q_2exp(T4, T4, 1);  /* (N - sigma)/2  (N - sigma even: N == sigma mod 8 Phi) */
            mpz_set_ui(T5, 2); mpz_powm(T5, T5, T4, T3);
            if (mpz_cmp_ui(T5, 1) == 0) { pass = 1; S.epass[j]++; }
        }
        if (!pass) { S.eclosed[j]++; return; }               /* no candidate can be a genuine completion */
    }
    mpz_mul_2exp(TPH, *Phi, 1);
    for (int k = 0; k < K; k++) {
        S.cand[j]++;
        mpz_mul(PSI, *P, CAND[j][k]); mpz_sub(PSI, PSI, SIG);
        if (!mpz_divisible_p(PSI, TPH)) die("candidate not congruent");
        mpz_divexact(PSI, PSI, TPH);
        mpz_sub(WW, CAND[j][k], PSI); mpz_add_ui(WW, WW, 1);          /* W + 1 = r1 + r2 */
        mpz_mul(DISC, WW, WW); mpz_submul_ui(DISC, CAND[j][k], 4);    /* (r2 - r1)^2 */
        if (mpz_sgn(DISC) <= 0 || !mpz_perfect_square_p(DISC)) continue;
        mpz_sqrt(SQ, DISC);
        mpz_sub(R1, WW, SQ);
        if (mpz_odd_p(R1)) continue;
        mpz_tdiv_q_2exp(R1, R1, 1); mpz_add(R2, WW, SQ); mpz_tdiv_q_2exp(R2, R2, 1);
        S.sqhit[j]++;
        if (mpz_cmp(R1, LOZ_J[j]) < 0 || mpz_cmp_ui(R1, plast) <= 0) continue;
        if (!is_prime_z(R1)) continue;
        int ok = 1; mpz_sub_ui(T5, R1, 1);
        for (int i = 0; i < j && ok; i++) if (mpz_divisible_ui_p(T5, pre[i])) ok = 0;
        if (!ok) continue;
        S.c2i[j]++;
        EVVIA = "small"; record_event_z(j, R1, R2, *P); EVVIA = "c2";
    }
    /* m >= 3 */
    mpz_add_ui(T1, LOZ_J[j], 2); mpz_mul(T1, T1, LOZ_J[j]); mpz_add_ui(T2, LOZ_J[j], 4); mpz_mul(T1, T1, T2); mpz_mul(T1, T1, *P);
    if (mpz_cmp(T1, X) > 0) return;
    if (!mpz_fits_ulong_p(LOZ_J[j]) || mpz_cmp_ui(LOZ_J[j], (u64)1 << 62) >= 0) die("lo >= 2^62 (small regime)");   /* r2: children() streams primes beyond the sieve */
    children(j, mpz_get_ui(LOZ_J[j]), K);
}

static void node(int j) {
    mpz_t *P = &PP[j], *Phi = &FF[j], *A = &AA[j];
    if (j >= D0) {
        if (ntasks == captasks) { captasks = captasks ? 2 * captasks : 4096; tasks = realloc(tasks, captasks * sizeof(Task)); }
        Task *t = &tasks[ntasks++]; t->j = j; memcpy(t->pref, pre, sizeof(u64) * j);
        return;
    }
    if (j >= MAXD - 3) die("depth");
    S.nodes[j]++;
    S.digest += Hh(*P);
    mpz_mul_2exp(TWOPHI, *Phi, 1);
    mpz_sub(*A, TWOPHI, *P);
    if (mpz_sgn(*A) <= 0) die("invariant P < 2 Phi violated");
    if (CQMODE) {                                   /* LCAP-CQ classification (before anything else) */
        mpz_mul_2exp(MM, *Phi, 3);
        if (!mpz_invert(Q0, *P, MM)) die("P not invertible mod 8 Phi");
        mpz_mul(Q0, Q0, SIG); mpz_mod(Q0, Q0, MM);
        if (mpz_sgn(Q0) == 0) mpz_set(Q0, MM);
        mpz_mul(T1, *P, Q0);
        if (mpz_cmp(T1, X) > 0) { S.pruned[j]++; return; }                 /* DEAD */
        long c = -1;
        if (CQMODE == 1) { mpz_mul(T2, MM, *P); if (mpz_cmp(T2, X) > 0) c = 1; }
        else {
            mpz_fdiv_q(T2, X, *P); mpz_sub(T2, T2, Q0); mpz_fdiv_q(T2, T2, MM);
            if (mpz_cmp_ui(T2, 15) <= 0) c = (long)mpz_get_ui(T2) + 1;
        }
        if (c > 0) {                                                        /* UNIQUE / MULTI */
            S.small[j]++;
            for (long t = 0; t < c; t++) {
                mpz_mul_ui(T3, MM, (u64)t); mpz_add(T3, T3, Q0); mpz_mul(T3, T3, *P);   /* N_t */
                mpz_sub(T4, T3, SIG); mpz_tdiv_q_2exp(T4, T4, 1);                     /* (N - sigma)/2 */
                mpz_set_ui(T5, 2); mpz_powm(T5, T5, T4, T3);
                S.cand[j]++;
                if (mpz_cmp_ui(T5, 1) == 0) {                                       /* Euler pass: report */
                    S.sqhit[j]++;
                    char *ns = mpz_get_str(0, 10, T3);
                    if (evlen + 4096 + strlen(ns) > sizeof(evbuf)) die("event buffer full");
                    evlen += sprintf(evbuf + evlen, "%s{\"euler_pass_N\":%s,\"prefix_depth\":%d}", nev ? "," : "", ns, j);
                    free(ns); nev++;
                }
            }
            return;
        }
        S.live[j]++; S.digest_live += Hh(*P);                               /* SCAN: plain LCAP-1 body */
    }
    u64 plast = j ? pre[j - 1] : PMIN - 1;
    mpz_fdiv_q(LOZ, TWOPHI, *A); mpz_add_ui(LOZ, LOZ, 1);
    if (mpz_cmp_ui(LOZ, plast + 1) < 0) mpz_set_ui(LOZ, plast + 1);
    mpz_set(LOZ_J[j], LOZ);
    mpz_fdiv_q(QHI, X, *P);                         /* floor(X/P) */
    mpz_sqrt(QMZ, QHI);                             /* qmax0 = isqrt(floor(X/P)) */
    if (mpz_cmp(LOZ, QMZ) > 0) return;
    if (CRT && !CQMODE) {
        mpz_add_ui(QLO, LOZ, 2); mpz_mul(QLO, QLO, LOZ);    /* lo (lo+2) */
        if (mpz_cmp(QHI, QLO) < 0) { S.pruned[j]++; return; }
        mpz_mul_2exp(MM, *Phi, 3);                          /* 8 Phi */
        mpz_sub(T1, QHI, QLO); mpz_add_ui(T1, T1, 1);
        mpz_mul_ui(T2, MM, (u64)KMAX + 1);
        if (!FILT && mpz_cmp(T1, T2) >= 0) S.crt_skip++;   /* >= KMAX+1 candidates surely: large regime */
        else {
            S.crt_tests++;
            if (!mpz_invert(Q0, *P, MM)) die("P not invertible mod 8 Phi");
            if (mpz_cmp_ui(SIG, 1) != 0) { mpz_mul(Q0, Q0, SIG); mpz_mod(Q0, Q0, MM); }
            /* least Q >= QLO with Q == Q0 (mod M):  Q1 = QLO + ((Q0 - QLO) mod M) */
            mpz_sub(T1, Q0, QLO); mpz_mod(T1, T1, MM); mpz_add(T1, T1, QLO);
            if (mpz_cmp(T1, QHI) > 0) { S.pruned[j]++; return; }
            mpz_sub(T2, QHI, T1); mpz_fdiv_q(T2, T2, MM);   /* K - 1 */
            mpz_set(CQ1[j], T1);
            CK[j] = (mpz_cmp_ui(T2, (1ULL << 62)) < 0) ? mpz_get_ui(T2) + 1 : (1ULL << 62);
            if (KMAX > 0 && mpz_cmp_ui(T2, (u64)KMAX) < 0) {
                int K = (int)mpz_get_ui(T2) + 1;
                S.live[j]++; S.digest_live += Hh(*P); S.small[j]++;
                for (int k = 0; k < K; k++) { if (k == 0) mpz_set(CAND[j][0], T1); else mpz_add(CAND[j][k], CAND[j][k - 1], MM); }
                small_closure(j, K);
                return;
            }
        }
    }
    if (!CQMODE) { S.live[j]++; S.digest_live += Hh(*P); }
    if (!mpz_fits_ulong_p(LOZ) || mpz_cmp_ui(LOZ, (u64)1 << 62) >= 0) die("lo >= 2^62");   /* r2: lo beyond the main sieve is handled by the segmented sieve */
    u64 lo = mpz_get_ui(LOZ);
    u64 qmax0 = mpz_fits_ulong_p(QMZ) ? mpz_get_ui(QMZ) : (u64)-1;
    c2(j, *P, *Phi, *A, lo, qmax0);
    children(j, lo, (CRT && FILT && !CQMODE) ? -1 : 0);
}

/* (c3) and (c4) at q = PR[i] (exact; monotone in q, so the children are an initial segment of the primes >= lo) */
static int child_pred(int j, int64_t i, double Pd, double Phid, u64 cmin) {
    mpz_t *P = &PP[j], *Phi = &FF[j];
    u64 q = PR[i];
    double curd = Pd * (double)q;
    if (!mul_le_X_d(curd, *P, q)) return 0;
    mpz_mul_ui(T3, *P, q);
    int m = 0; int64_t k = i + 1;
    double rhsd = 2.0 * Phid * (double)(q - 1) - (double)cmin;
    for (;; k++) {
        if (k + 1 >= NPR) die("sieve too small (m loop)");
        u64 pk = PR[k];
        double e = curd * (double)pk;
        int le;
        if (e > Xd * (1 + 1e-9)) le = 0;
        else if (e < Xd * (1 - 1e-9)) le = 1;
        else { mpz_mul_ui(T5, T3, pk); le = mpz_cmp(T5, X) <= 0; }
        if (!le) break;
        curd = e; mpz_mul_ui(T3, T3, pk); rhsd *= (double)(pk - 1); m++;
    }
    if (m < 2) return 0;
    if (curd > rhsd * (1 + 1e-9)) return 1;
    if (curd < rhsd * (1 - 1e-9)) return 0;
    mpz_mul_2exp(T4, *Phi, 1); mpz_mul_ui(T4, T4, q - 1); mpz_sub_ui(T4, T4, cmin);
    for (int64_t kk = i + 1; kk < i + 1 + m; kk++) mpz_mul_ui(T4, T4, (u64)PR[kk] - 1);
    return mpz_cmp(T3, T4) > 0;
}

/* r2: (c3)/(c4) at q = qp[0], reading the following primes from qp[1..avail-1] (same arithmetic as child_pred) */
static int child_pred_arr(int j, const u64 *qp, int64_t avail, double Pd, double Phid, u64 cmin) {
    mpz_t *P = &PP[j], *Phi = &FF[j];
    u64 q = qp[0];
    double curd = Pd * (double)q;
    if (!mul_le_X_d(curd, *P, q)) return 0;
    mpz_mul_ui(T3, *P, q);
    int m = 0; int64_t k = 1;
    double rhsd = 2.0 * Phid * (double)(q - 1) - (double)cmin;
    for (;; k++) {
        if (k + 1 >= avail) die("stream lookahead too small (m loop)");
        u64 pk = qp[k];
        double e = curd * (double)pk;
        int le;
        if (e > Xd * (1 + 1e-9)) le = 0;
        else if (e < Xd * (1 - 1e-9)) le = 1;
        else { mpz_mul_ui(T5, T3, pk); le = mpz_cmp(T5, X) <= 0; }
        if (!le) break;
        curd = e; mpz_mul_ui(T3, T3, pk); rhsd *= (double)(pk - 1); m++;
    }
    if (m < 2) return 0;
    if (curd > rhsd * (1 + 1e-9)) return 1;
    if (curd < rhsd * (1 - 1e-9)) return 0;
    mpz_mul_2exp(T4, *Phi, 1); mpz_mul_ui(T4, T4, q - 1); mpz_sub_ui(T4, T4, cmin);
    for (int64_t kk = 1; kk < 1 + m; kk++) mpz_mul_ui(T4, T4, qp[kk] - 1);
    return mpz_cmp(T3, T4) > 0;
}

/* one child q of node j that passed (c3)/(c4): rule (c2), the CRT child filters, then the child node */
static void child_visit(int j, u64 q, int filterK) {
    mpz_t *P = &PP[j], *Phi = &FF[j];
    if (!adm64(q - 1, j)) return;              /* (c2) */
    if (filterK < 0 || (filterK > 0 && FILT)) {   /* LCRT-3: q must divide a candidate of the AP */
        if (!child_may_live(j, q)) { S.kfilt[j + 1]++; return; }
    } else if (filterK > 0) {                  /* LCRT-2 push-down: q divides one of the K candidates */
        int hit = 0;
        for (int k = 0; k < filterK && !hit; k++) if (mpz_divisible_ui_p(CAND[j][k], q)) hit = 1;
        if (!hit) { S.kfilt[j + 1]++; return; }
    }
    pre[j] = q; lem[j] = UINT64_MAX / q + 1;
    mpz_mul_ui(PP[j + 1], *P, q); mpz_mul_ui(FF[j + 1], *Phi, q - 1);
    node(j + 1);
}

static void children(int j, u64 lo, int filterK) {
    mpz_t *P = &PP[j];
    double Pd = mpz_get_d(*P), Phid = mpz_get_d(FF[j]);
    {   /* (c3) shortcut: P lo (lo+2) (lo+4) > X => no child */
        mpz_mul_ui(T1, *P, lo); mpz_mul_ui(T1, T1, lo + 2); mpz_mul_ui(T1, T1, lo + 4);
        if (mpz_cmp(T1, X) > 0) return;
    }
    const u64 cmin = (SIGMA < 0) ? 1 : 0;
    const int64_t SAFE = NPR - 81;             /* child_pred(i) may read PR[i+1 .. i+80] */
    int64_t i0 = lower_bound(lo), iend;
    u64 stream_start = 0;                      /* r2: != 0 => the scan continues beyond index SAFE with the prime stream */
    /* stop index = first i >= i0 failing (c3)/(c4): galloping + bisection (exactly the linear scan's stop, by monotonicity) */
    if (i0 > SAFE) { iend = i0; stream_start = lo; }
    else if (!child_pred(j, i0, Pd, Phid, cmin)) iend = i0;
    else {
        int64_t good = i0, bad = -1, step = 1;
        for (;;) {
            int64_t t = good + step;
            if (t > SAFE) t = SAFE;
            if (t <= good) break;              /* (c3),(c4) hold at SAFE: the stop lies beyond; stream from SAFE+1 */
            if (child_pred(j, t, Pd, Phid, cmin)) { good = t; step <<= 1; } else { bad = t; break; }
        }
        if (bad < 0) { iend = SAFE + 1; stream_start = (u64)PR[SAFE + 1]; }
        else {
            while (bad - good > 1) { int64_t mid = good + ((bad - good) >> 1); if (child_pred(j, mid, Pd, Phid, cmin)) good = mid; else bad = mid; }
            iend = bad;
        }
    }
    if (!stream_start && (u64)PR[iend] > S.maxq) S.maxq = PR[iend];
    for (int64_t i = i0; i < iend; i++) child_visit(j, PR[i], filterK);
    if (stream_start) {                        /* linear scan over the stream; stops at the first q failing (c3)/(c4) */
        PStream *s = &PSJ[j];
        ps_init(s, stream_start);
        for (;;) {
            ps_ensure(s, LOOK);
            const u64 *qp = s->buf + s->pos;
            if (!child_pred_arr(j, qp, s->n - s->pos, Pd, Phid, cmin)) { if (qp[0] > S.maxq) S.maxq = qp[0]; break; }
            u64 q = qp[0]; s->pos++;
            if (q > (u64)PR[NPR - 1]) S.seg_ch++;
            child_visit(j, q, filterK);
        }
    }
}

static void sieve(u64 L) {
    if (L >= (1ULL << 32) - 1) die("sieve limit must be < 2^32");
    u64 n = (L - 1) / 2 + 1;
    unsigned char *s = calloc(n, 1); if (!s) die("calloc");
    for (u64 i = 1;; i++) { u64 p = 2 * i + 1; if (p * p > L) break; if (s[i]) continue; for (u64 k = (p * p - 1) / 2; k < n; k += p) s[k] = 1; }
    u64 cnt = 0; for (u64 i = 1; i < n; i++) if (!s[i] && 2 * i + 1 <= L) cnt++;
    PR = malloc(cnt * sizeof(u32)); NPR = 0;
    for (u64 i = 1; i < n; i++) if (!s[i] && 2 * i + 1 <= L) PR[NPR++] = (u32)(2 * i + 1);
    free(s);
}

static void arr(FILE *f, const char *name, u64 *a, int md) {
    fprintf(f, ",\"%s\":[", name);
    for (int d = 0; d < md; d++) fprintf(f, "%s%llu", d ? "," : "", (unsigned long long)a[d]);
    fprintf(f, "]");
}
static void write_stats(FILE *f, Stats *s, int64_t task, Task *t) {
    fprintf(f, "{\"task\":%lld", (long long)task);
    if (t) {
        fprintf(f, ",\"prefix\":[");
        for (int i = 0; i < t->j; i++) fprintf(f, "%s%llu", i ? "," : "", (unsigned long long)t->pref[i]);
        fprintf(f, "]");
    }
    int md = 0; for (int d = 0; d < MAXD; d++) if (s->nodes[d] || s->c2p[d] || s->pruned[d] || s->kfilt[d]) md = d + 1;
    arr(f, "nodes", s->nodes, md); arr(f, "pruned", s->pruned, md);
    arr(f, "c2p", s->c2p, md); arr(f, "c2a", s->c2a, md); arr(f, "c2i", s->c2i, md);
    arr(f, "live", s->live, md); arr(f, "small", s->small, md); arr(f, "cand", s->cand, md);
    arr(f, "sqhit", s->sqhit, md); arr(f, "kfilt", s->kfilt, md); arr(f, "eclosed", s->eclosed, md); arr(f, "epass", s->epass, md);
    if (C2CAND) arr(f, "c2k", s->c2k, md);
    if (TDIV) arr(f, "tdrej", s->tdrej, md);
    fprintf(f, ",\"digest\":\"%016llx\",\"digest_live\":\"%016llx\",\"crt_tests\":%llu,\"crt_skip\":%llu,\"maxq\":%llu,\"seg_c2\":%llu,\"seg_ch\":%llu,\"events\":[%.*s]}\n",
            (unsigned long long)s->digest, (unsigned long long)s->digest_live, (unsigned long long)s->crt_tests,
            (unsigned long long)s->crt_skip, (unsigned long long)s->maxq, (unsigned long long)s->seg_c2,
            (unsigned long long)s->seg_ch, (int)evlen, evbuf);
}

static void setup_task(Task *t) {
    mpz_set_ui(PP[0], 1); mpz_set_ui(FF[0], 1);
    for (int i = 0; i < t->j; i++) {
        pre[i] = t->pref[i]; lem[i] = UINT64_MAX / pre[i] + 1;
        mpz_mul_ui(PP[i + 1], PP[i], pre[i]); mpz_mul_ui(FF[i + 1], FF[i], pre[i] - 1);
    }
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: lcrt X SIEVE D0 WORKERS OUTDIR [SIGMA] [PMIN] [CRT]\n"); return 1; }
    mpz_init(X);
    if (mpz_set_str(X, argv[1], 10) != 0 || mpz_cmp_ui(X, 1000) < 0) die("bad X");
    Xd = mpz_get_d(X);
    u64 L = strtoull(argv[2], 0, 10);
    D0 = atoi(argv[3]); int W = atoi(argv[4]); const char *out = argv[5];
    mpz_init_set_si(SIG, 1);
    if (argc > 6 && mpz_set_str(SIG, argv[6], 10) != 0) die("bad SIGMA");
    SIGMA = mpz_sgn(SIG);
    if (argc > 7) PMIN = strtoull(argv[7], 0, 10);
    if (argc > 8) CRT = atoi(argv[8]);
    if (argc > 9) KMAX = atoi(argv[9]);
    if (argc > 10) FILT = atoi(argv[10]);
    if (argc > 11) CQMODE = atoi(argv[11]);
    if (argc > 12) EULER = atoi(argv[12]);
    if (argc > 13) C2CAND = strtoull(argv[13], 0, 10);
    if (argc > 14) TDIV = strtoull(argv[14], 0, 10);
    if (TDIV > 3000) die("TDIV must be <= 3000");
    if (!CRT || KMAX == 0) EULER = 0;
    if (KMAX < 0 || KMAX >= KMAXMAX) die("KMAX out of range");
    if (!CRT) { KMAX = 0; FILT = 0; }
    if (mpz_even_p(SIG)) die("SIGMA must be odd");
    if (PMIN != 3 && PMIN != 5 && PMIN != 7) die("PMIN must be 3, 5 or 7");
    for (int d = 0; d < MAXD; d++) { mpz_init(PP[d]); mpz_init(FF[d]); mpz_init(AA[d]); mpz_init(LOZ_J[d]); mpz_init(CQ1[d]);
        for (int k = 0; k < KMAXMAX; k++) mpz_init(CAND[d][k]); }
    mpz_inits(PSI, WW, DISC, SQ, R1, R2, TPH, QC, MC, NULL);
    mpz_inits(T1, T2, T3, T4, T5, T6, QLO, QHI, MM, Q0, TWOPHI, LOZ, QMZ, NULL);
    mkdir(out, 0755);
    SEGB = malloc(SEGW); C2BUF = malloc(SEGW * sizeof(u64));
    if (!SEGB || !C2BUF) die("malloc segment buffers");
    time_t t0 = time(0);
    sieve(L);
    fprintf(stderr, "X=%s sigma=%s pmin=%llu crt=%d sieve: %lld primes >= 3 up to %llu (%lds)\n", argv[1], argc > 6 ? argv[6] : "1",
            (unsigned long long)PMIN, CRT, (long long)NPR, (unsigned long long)L, (long)(time(0) - t0));
    if (TDIV) {                                     /* odd primes < TDIV in increasing order, grouped: product < 2^64 */
        u64 prodg = 1; TDGN = 0; TDPN[0] = 0;
        for (int64_t i = 0; i < NPR && PR[i] < TDIV; i++) {
            u64 p = PR[i];
            if (TDPN[TDGN] == 16 || prodg > UINT64_MAX / p) { TDG[TDGN++] = prodg; prodg = 1; TDPN[TDGN] = 0; }
            TDP[TDGN][TDPN[TDGN]++] = (u32)p; prodg *= p;
        }
        if (TDPN[TDGN]) TDG[TDGN++] = prodg;
    }
    memset(&S, 0, sizeof S);
    mpz_set_ui(PP[0], 1); mpz_set_ui(FF[0], 1);
    node(0);
    fprintf(stderr, "master: %lld tasks at depth %d (%lds)\n", (long long)ntasks, D0, (long)(time(0) - t0));
    char path[4096];
    snprintf(path, sizeof path, "%s/master.json", out);
    FILE *f = fopen(path, "w");
    fprintf(f, "{\"X\":\"%s\",\"sigma\":%s,\"pmin\":%llu,\"crt\":%d,\"kmax\":%d,\"filt\":%d,\"cqmode\":%d,\"euler\":%d,\"c2cand\":%llu,\"tdiv\":%llu,\"sieve\":%llu,\"D0\":%d,\"ntasks\":%lld,\"master\":",
            argv[1], argc > 6 ? argv[6] : "1", (unsigned long long)PMIN, CRT, KMAX, FILT, CQMODE, EULER, (unsigned long long)C2CAND, (unsigned long long)TDIV, (unsigned long long)L, D0, (long long)ntasks);
    write_stats(f, &S, -1, 0);
    fprintf(f, "}\n"); fclose(f);
    unsigned char *done = calloc(ntasks + 1, 1);
    DIR *dd = opendir(out); struct dirent *de;
    while ((de = readdir(dd))) {
        if (strncmp(de->d_name, "tasks_w", 7)) continue;
        snprintf(path, sizeof path, "%s/%s", out, de->d_name);
        FILE *g = fopen(path, "r"); if (!g) continue;
        char *line = 0; size_t cap = 0; ssize_t len;
        while ((len = getline(&line, &cap, g)) > 0) {
            if (line[len - 1] != '\n') continue;
            long long id; if (sscanf(line, "{\"task\":%lld", &id) == 1 && id >= 0 && id < ntasks) done[id] = 1;
        }
        free(line); fclose(g);
    }
    closedir(dd);
    int64_t ndone = 0; for (int64_t k = 0; k < ntasks; k++) ndone += done[k];
    fprintf(stderr, "resume: %lld/%lld tasks already done\n", (long long)ndone, (long long)ntasks);
    volatile int64_t *ctr = mmap(0, 4096, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANON, -1, 0);
    *ctr = 0;
    for (int w = 0; w < W; w++) {
        pid_t pid = fork();
        if (pid == 0) {
            snprintf(path, sizeof path, "%s/tasks_w%d_%d.jsonl", out, w, (int)getpid());
            FILE *g = fopen(path, "a");
            D0 = 1 << 30;
            for (;;) {
                int64_t k = __atomic_fetch_add(ctr, 1, __ATOMIC_SEQ_CST);
                if (k >= ntasks) break;
                if (done[k]) continue;
                Task *t = &tasks[k];
                memset(&S, 0, sizeof S); evlen = 0; nev = 0;
                setup_task(t);
                node(t->j);
                write_stats(g, &S, k, t);
                fflush(g);
#ifdef ORPHAN_EXIT
                if (getppid() == 1) _exit(0);      /* master was killed (job time cap): stop; resumable */
#endif
            }
            fclose(g);
            _exit(0);
        }
    }
    int st; while (wait(&st) > 0) { if (!WIFEXITED(st) || WEXITSTATUS(st)) { fprintf(stderr, "worker failed\n"); return 3; } }
    fprintf(stderr, "all done (%lds)\n", (long)(time(0) - t0));
    snprintf(path, sizeof path, "%s/DONE", out);
    f = fopen(path, "w"); fprintf(f, "ntasks %lld\n", (long long)ntasks); fclose(f);
    return 0;
}
