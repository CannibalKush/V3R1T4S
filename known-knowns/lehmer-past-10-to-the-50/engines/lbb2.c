/* lbb2.c -- independent branch-and-bound for Lehmer numbers with k = 2 (independent engine 2), version 2.
 *
 * Written from the definition (composite n with phi(n) | n-1); see lemmas.py for 3 !| n and k = 2 below 10^50.
 * Search space: n = p1 ... pr, 5 <= p1 < ... < pr primes, r >= 2, n <= X, with  n - R = 2 phi(n)  (R = 1 is Lehmer;
 * R and a "fake prime" mode exist only for the planted completeness test).
 *
 * Node = prefix p1..ps, P = prod p, F = prod (p-1), admissible (p_i !| p_j - 1), P < 2F.  a = 2F, g = a - P > 0,
 * Qmax = floor(X/P).  Remaining Q = q1 < ... < qm (m >= 2 at every node, see below), primes > ps:
 *        P Q - R = 2 F phi(Q)                                                         (*)
 *  (L)  m >= 2  =>  q1 >= ceil(a/g)   [phi(Q)(a - g q1) < R (q1 - 1) and phi(Q) >= (q1-1)(q1+1)]
 *  (M2) m = 2: (g q1 - a)(g q2 - a) = D := a^2 - g (a + R), 0 < g q1 - a <= sqrt(D), q1 <= sqrt(Qmax).
 *        Closed EITHER by enumerating every admissible prime q1 in [L, U2] and testing (g q1 - a) | (a (q1-1) - R)
 *        OR by enumerating every Q == R P^{-1} (mod 8F) in [L(L+2), Qmax] (since 4 | phi(Q)), putting
 *        S = q1 + q2 = (g Q + a + R)/a and testing S^2 - 4Q for a perfect square.
 *  (M3) m >= 3: q1 <= cbrt(Qmax).  EITHER branch on every admissible prime q1 in [L, cbrt(Qmax)] (stopping at the first
 *        q1 failing a monotone necessary ratio/size bound) -> child node P q1 (whose remaining part has >= 2 primes),
 *        OR (when cheaper) enumerate every Q == R P^{-1} (mod 16F) in [L(L+2)(L+4), Qmax] (since 8 | phi(Q)) with no
 *        prime factor < L and test 2^((PQ-R)/2) == 1 (mod PQ), which every solution passes (phi(PQ) = (PQ-R)/2).
 *  (M1) redundant cross-check at every node with s >= 1: q = (a - R)/g  (this is the parent's m = 2 case).
 * The root P = 1 has m >= 2 automatically (n composite).
 */
#include <stdio.h>
#include <gmp.h>
#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;
#define MAXD 64

static mpz_t X;
static u64 SMAX = 100000000ULL;
static uint32_t *PR; static u64 NPR;
static long RR = 1;
static int FAKE = 0;
static u64 PMIN = 5;
static int D0 = 9, mode_gen = 0, VERB = 0;
static double K2 = 0.1;    /* m=2: AP+square if C <= K2 * (#q1 candidates) */
static double K3 = 0.5;    /* m>=3: Euler closure if C3 <= K3 * (#children estimate) */
static u64 T3 = 2;         /* m>=3: Euler closure if C3 <= T3 */
static u64 SIEVE_CAP = 1u << 18;

static mpz_t Pv[MAXD], Fv[MAXD], av[MAXD], gv[MAXD], Qv[MAXD];
static mpz_t t1, t2, t3, t4, t5, M_, c_, Q0_, N_, e_, two_;

/* stats */
static u64 st_nodes[MAXD], st_m2ap[MAXD], st_m2en[MAXD], st_m2apcand[MAXD], st_m2q1[MAXD], st_m3eul[MAXD], st_m3cand[MAXD], st_m3euler[MAXD], st_m3br[MAXD];
static u64 st_m1int = 0, st_m2int = 0, st_euler_pass = 0, st_solutions = 0, st_segq = 0, st_maxq1 = 0, st_ntask = 0, st_segchild = 0;
static FILE *OUT;
static int cur_s = 0; static u64 pr[MAXD];
static void die(const char *m) { fprintf(stderr, "FATAL %s\n", m); fprintf(OUT, "FATAL %s at depth %d prefix", m, cur_s); for (int i = 0; i < cur_s && i < MAXD; i++) fprintf(OUT, " %llu", (unsigned long long)pr[i]); fprintf(OUT, "\n"); fflush(OUT); exit(2); }

/* ---------------- primes ---------------- */
static void sieve_table(u64 n) {
  if (FAKE) { NPR = 0; PR = malloc((n / 2 + 2) * sizeof(uint32_t)); for (u64 i = PMIN | 1; i <= n; i += 2) PR[NPR++] = (uint32_t)i; return; }
  /* odd-only byte sieve, segmented to keep memory small */
  u64 r = (u64)sqrt((double)n) + 2;
  uint8_t *small = calloc(r + 1, 1);
  for (u64 i = 2; i * i <= r; i++) if (!small[i]) for (u64 j = i * i; j <= r; j += i) small[j] = 1;
  u64 cap = (u64)(1.3 * n / log((double)n)) + 1000;
  PR = malloc(cap * sizeof(uint32_t)); NPR = 0;
  const u64 W = 1u << 24; uint8_t *seg = malloc(W);
  for (u64 lo = 0; lo <= n; lo += W) {
    u64 hi = lo + W - 1; if (hi > n) hi = n;
    memset(seg, 0, hi - lo + 1);
    for (u64 p = 2; p <= r && p * p <= hi; p++) if (!small[p]) {
      u64 st = (lo + p - 1) / p * p; if (st < p * p) st = p * p;
      for (u64 k = st; k <= hi; k += p) seg[k - lo] = 1;
    }
    for (u64 v = lo; v <= hi; v++) if (v >= 5 && !seg[v - lo]) { if (NPR >= cap) die("cap"); PR[NPR++] = (uint32_t)v; }
  }
  free(seg); free(small);
}
static u64 pidx(u64 v) { u64 lo = 0, hi = NPR; while (lo < hi) { u64 m = (lo + hi) / 2; if (PR[m] < v) lo = m + 1; else hi = m; } return lo; }
static inline int admissible(int s, u64 q) { for (int i = 0; i < s; i++) if (q % pr[i] == 1) return 0; return 1; }
static double mpz_log(const mpz_t z) { long e; double d = mpz_get_d_2exp(&e, z); return log(d) + (double)e * log(2.0); }

/* segmented prime source over [lo, hi], hi beyond table: calls cb for each prime; cb returns 0 to stop */
typedef int (*primecb)(int s, u64 q, void *ctx);
static void seg_primes(u64 lo, u64 hi, int s, primecb cb, void *ctx) {
  if (FAKE) die("fake: beyond table");
  if ((double)PR[NPR - 1] * (double)PR[NPR - 1] < (double)hi) die("table too small for segmented range");
  const u64 W = 1u << 21; uint8_t *seg = malloc(W);
  for (u64 base = lo; base <= hi; base += W) {
    u64 top = base + W - 1; if (top > hi) top = hi;
    memset(seg, 0, top - base + 1);
    for (u64 k = base + (base & 1); k <= top; k += 2) seg[k - base] = 1;   /* evens */
    { u64 st = (base + 2) / 3 * 3; for (u64 k = st; k <= top; k += 3) seg[k - base] = 1; }
    for (u64 j = 0; j < NPR; j++) {
      u64 r = PR[j]; if (r * r > top) break;
      u64 st = (base + r - 1) / r * r; if (st < r * r) st = r * r;
      for (u64 k = st; k <= top; k += r) seg[k - base] = 1;
    }
    for (u64 v = base; v <= top; v++) if (!seg[v - base] && v >= 5) { st_segq++; if (!cb(s, v, ctx)) { free(seg); return; } }
  }
  free(seg);
}

/* ---------------- reporting ---------------- */
static void emit_prefix(const char *tag, int s) { fprintf(OUT, "%s", tag); for (int i = 0; i < s; i++) fprintf(OUT, " %llu", (unsigned long long)pr[i]); }

static int is_prime_mpz(const mpz_t q) { return FAKE ? (mpz_odd_p(q) && mpz_cmp_ui(q, PMIN) >= 0) : mpz_probab_prime_p(q, 30) > 0; }
static int adm_mpz(int s, const mpz_t q) { for (int i = 0; i < s; i++) if (mpz_fdiv_ui(q, pr[i]) == 1) return 0; return 1; }

/* final report of a 2-prime completion q1 < q2 (both mpz) at node s; verifies everything exactly */
static void report_m2(int s, const mpz_t q1, const mpz_t q2, const char *how) {
  st_m2int++;
  mpz_mul(t5, Pv[s], q1); mpz_mul(t5, t5, q2);
  int inX = mpz_cmp(t5, X) <= 0;
  emit_prefix("M2INT prefix", s); gmp_fprintf(OUT, " | %Zd %Zd inX %d via %s\n", q1, q2, inX, how);
  if (!inX) return;
  if (!is_prime_mpz(q1) || !is_prime_mpz(q2)) return;
  if (!adm_mpz(s, q1) || !adm_mpz(s, q2)) return;
  { mpz_t r; mpz_init(r); mpz_fdiv_r(r, q2, q1); int bad = mpz_cmp_ui(r, 1) == 0; mpz_clear(r); if (bad) return; }
  /* exact equation check */
  mpz_t ph; mpz_init(ph); mpz_sub_ui(ph, q1, 1); mpz_mul(ph, ph, Fv[s]); mpz_sub_ui(t4, q2, 1); mpz_mul(ph, ph, t4); mpz_mul_2exp(ph, ph, 1);
  mpz_sub_ui(t4, t5, RR); int ok = mpz_cmp(ph, t4) == 0; mpz_clear(ph);
  if (!ok) { fprintf(OUT, "WARN m2 equation mismatch\n"); return; }
  st_solutions++; emit_prefix("SOLUTION prefix", s); gmp_fprintf(OUT, " | %Zd %Zd N %Zd\n", q1, q2, t5); fflush(OUT);
}

/* ---------------- m = 2 by q1 enumeration ---------------- */
struct m2ctx { u128 a, g; int native; u64 U2; };
static int m2_q1(int s, u64 q, void *vctx) {
  struct m2ctx *c = vctx;
  if (q > c->U2) return 0;
  if (!admissible(s, q)) return 1;
  st_m2q1[s]++;
  if (q > st_maxq1) st_maxq1 = q;
  if (c->native) {
    u128 u = c->g * q - c->a;          /* > 0 since q >= L >= ceil(a/g) and g q = a impossible to give a solution */
    if (u == 0) return 1;
    u128 n = c->a * (q - 1) - (u128)RR;
    if (n % u) return 1;
  } else {
    mpz_mul_ui(t3, gv[s], q); mpz_sub(t3, t3, av[s]); if (mpz_sgn(t3) <= 0) return 1;
    mpz_mul_ui(t4, av[s], q - 1); mpz_sub_ui(t4, t4, RR);
    if (!mpz_divisible_p(t4, t3)) return 1;
  }
  /* integral: recompute exactly with mpz */
  mpz_mul_ui(t3, gv[s], q); mpz_sub(t3, t3, av[s]);
  mpz_mul_ui(t4, av[s], q - 1); mpz_sub_ui(t4, t4, RR);
  if (!mpz_divisible_p(t4, t3)) die("native/mpz disagree");
  mpz_divexact(t4, t4, t3);
  if (mpz_cmp_ui(t4, q) <= 0) return 1;
  mpz_t q1; mpz_init_set_ui(q1, q); mpz_t q2; mpz_init_set(q2, t4);
  report_m2(s, q1, q2, "enum"); mpz_clear(q1); mpz_clear(q2);
  return 1;
}

/* ---------------- m >= 3 Euler closure ---------------- */
static uint8_t *mark = NULL; static u64 *sv_r = NULL, *sv_j = NULL; static u64 sv_cap = 0;
#define APBLK (1u << 18)
static u64 fk_list[64]; static int fk_n;
static int fk_adm(int s, u64 x) { for (int i = 0; i < s; i++) if (x % pr[i] == 1) return 0; for (int i = 0; i < fk_n; i++) if (x % fk_list[i] == 1) return 0; return 1; }
static int fk_rec(int s, u64 rem, u64 phi, u64 lo, int mmin) {
  int found = 0;
  if (fk_n + 1 >= mmin && rem >= lo && (rem & 1) && rem - 1 == phi && fk_adm(s, rem)) {
    found++; emit_prefix("SOLUTION fake prefix", s); fprintf(OUT, " |");
    for (int i = 0; i < fk_n; i++) fprintf(OUT, " %llu", (unsigned long long)fk_list[i]); fprintf(OUT, " %llu\n", (unsigned long long)rem);
  }
  for (u64 d = lo | 1; d * d < rem; d += 2) {
    if (rem % d || phi % (d - 1) || !fk_adm(s, d)) continue;
    fk_list[fk_n++] = d; found += fk_rec(s, rem / d, phi / (d - 1), d + 2, mmin); fk_n--;
  }
  return found;
}
static int fake_check(int s, const mpz_t Q, int mmin) {
  mpz_mul(t4, Pv[s], Q); mpz_sub_ui(t4, t4, RR); mpz_mul_2exp(t5, Fv[s], 1);
  if (!mpz_divisible_p(t4, t5)) die("fake: candidate not == R mod 2F");
  mpz_divexact(t4, t4, t5);
  if (!mpz_fits_ulong_p(Q) || !mpz_fits_ulong_p(t4)) die("fake: too big");
  fk_n = 0; return fk_rec(s, mpz_get_ui(Q), mpz_get_ui(t4), (s ? pr[s - 1] : PMIN - 2) + 2, mmin);
}
/* enumerate Q0 + k*M_, k < C; drop Q with a prime factor < min(L, B); Euler-test the rest */
static void euler_close(int s, u64 L, u64 C) {
  if (!mark) { mark = malloc(APBLK); if (!mark) die("oom"); }
  u64 B = SIEVE_CAP; if (8 * C + 1000 < B) B = 8 * C + 1000; if (L - 1 < B) B = L - 1; if (FAKE) B = 0;
  u64 ns = 0;
  for (u64 j = 0; j <= NPR && (j == 0 ? 3 : PR[j - 1]) <= B; j++) {
    u64 r = j == 0 ? 3 : PR[j - 1];
    u64 Mr = mpz_fdiv_ui(M_, r); if (Mr == 0) continue;
    u64 Q0r = mpz_fdiv_ui(Q0_, r);
    long long o_r = (long long)Mr, r_ = (long long)r, o_s = 1, s_ = 0;
    while (r_) { long long qq = o_r / r_, tmp = o_r - qq * r_; o_r = r_; r_ = tmp; tmp = o_s - qq * s_; o_s = s_; s_ = tmp; }
    long long x0 = o_s % (long long)r; if (x0 < 0) x0 += r;
    u64 j0 = (u64)(((u128)((r - Q0r) % r) * (u64)x0) % r);
    if (ns >= sv_cap) { sv_cap = sv_cap ? 2 * sv_cap : 4096; sv_r = realloc(sv_r, sv_cap * 8); sv_j = realloc(sv_j, sv_cap * 8); }
    sv_r[ns] = r; sv_j[ns] = j0; ns++;
  }
  mpz_set(t1, Q0_);
  for (u64 k0 = 0; k0 < C; k0 += APBLK) {
    u64 cb = C - k0 < APBLK ? C - k0 : APBLK;
    memset(mark, 0, cb);
    for (u64 i = 0; i < ns; i++) { u64 r = sv_r[i]; u64 st = (sv_j[i] + r - k0 % r) % r; for (u64 k = st; k < cb; k += r) mark[k] = 1; }
    for (u64 k = 0; k < cb; k++, mpz_add(t1, t1, M_)) {
      if (mark[k]) continue;
      st_m3euler[s]++;
      if (FAKE) { if (fake_check(s, t1, 3)) { st_euler_pass++; st_solutions++; } continue; }
      mpz_mul(N_, Pv[s], t1); mpz_sub_ui(e_, N_, RR); mpz_fdiv_q_2exp(e_, e_, 1);
      mpz_powm(t2, two_, e_, N_);
      if (mpz_cmp_ui(t2, 1) == 0) { st_euler_pass++; emit_prefix("EULERPASS prefix", s); gmp_fprintf(OUT, " | Q %Zd\n", t1); fflush(OUT); }
    }
  }
}

/* necessary bound for q1 as smallest prime of Q with >= mmin primes: monotone in q1.  double with one-sided margin. */
static int feasible(int s, u64 q1, u64 q1idx, double logQmax, double target, int mmin) {
  double lim = logQmax + 1e-9, ls = 0, lr = 0, tgt = target * (1 - 1e-11); int m = 0;
  if (q1idx < NPR) {
    for (u64 j = q1idx; j < NPR; j++) {
      u64 r = PR[j];
      if (j != q1idx && !admissible(s, r)) continue;
      double lg = log((double)r);
      if (ls + lg > lim) return 0;
      ls += lg; lr += -log1p(-1.0 / (double)r); m++;
      if (m >= mmin && lr >= tgt) return 1;
    }
    double rr = (double)SMAX, lg = log(rr), inc = -log1p(-1.0 / rr);
    while (ls + lg <= lim) { ls += lg; lr += inc; m++; if (m >= mmin && lr >= tgt) return 1; }
    return 0;
  }
  double lg = log((double)q1); int mm = (int)floor(lim / lg);
  if (mm < mmin) return 0;
  return mm * (-log1p(-1.0 / (double)q1)) >= tgt;
}

static void process(int s);
struct m3ctx { double logQmax, target; u64 cube; int stop; };
static int m3_child(int s, u64 q, void *vctx) {
  struct m3ctx *c = vctx;
  if (q > c->cube) { c->stop = 1; return 0; }
  if (!admissible(s, q)) return 1;
  if (!feasible(s, q, NPR, c->logQmax, c->target, 3)) { c->stop = 1; return 0; }
  st_segchild++;
  if (q > st_maxq1) st_maxq1 = q;
  pr[s] = q; mpz_mul_ui(Pv[s + 1], Pv[s], q); mpz_mul_ui(Fv[s + 1], Fv[s], q - 1); process(s + 1);
  return 1;
}

static double est_primes(u64 lo, u64 hi) {
  if (hi < lo) return 0;
  if (hi <= SMAX) return (double)(pidx(hi + 1) - pidx(lo));
  double a = lo > SMAX ? (double)lo : (double)SMAX;
  return (lo <= SMAX ? (double)(NPR - pidx(lo)) : 0) + ((double)hi - a) / log((double)hi);
}

static void process(int s) {
  st_nodes[s]++; cur_s = s;
  if (s + 2 >= MAXD) die("depth");
  if (mode_gen && s == D0) { emit_prefix("TASK", s); fprintf(OUT, "\n"); st_ntask++; return; }
  u64 plast = s ? pr[s - 1] : PMIN - 2;
  mpz_mul_2exp(av[s], Fv[s], 1); mpz_sub(gv[s], av[s], Pv[s]);
  if (mpz_sgn(gv[s]) <= 0) die("node with P >= 2F");
  mpz_fdiv_q(Qv[s], X, Pv[s]);
  /* (M1) redundant cross-check */
  if (s >= 1) {
    mpz_sub_ui(t1, av[s], RR);
    if (mpz_divisible_p(t1, gv[s])) {
      mpz_divexact(t1, t1, gv[s]);
      if (mpz_cmp_ui(t1, plast) > 0 && mpz_cmp(t1, Qv[s]) <= 0) {
        st_m1int++; emit_prefix("M1INT prefix", s); gmp_fprintf(OUT, " | %Zd\n", t1);
        if (is_prime_mpz(t1) && adm_mpz(s, t1)) { st_solutions++; emit_prefix("SOLUTION m1 prefix", s); gmp_fprintf(OUT, " | %Zd\n", t1); fflush(OUT); }
      }
    }
  }
  /* L */
  mpz_cdiv_q(t1, av[s], gv[s]);
  if (mpz_cmp_ui(t1, plast + 2) < 0) mpz_set_ui(t1, plast + 2);
  mpz_add_ui(t2, t1, 2); mpz_mul(t2, t2, t1);
  if (mpz_cmp(t2, Qv[s]) > 0) return;          /* no m >= 2 */
  if (!mpz_fits_ulong_p(t1)) die("L too big");
  u64 L = mpz_get_ui(t1);

  /* ---------- m = 2 ---------- */
  {
    /* D = a^2 - g(a+R); U2 = min(floor((a + isqrt D)/g), isqrt(Qmax)) */
    mpz_mul(t3, av[s], av[s]); mpz_add_ui(t4, av[s], RR); mpz_mul(t4, t4, gv[s]); mpz_sub(t3, t3, t4);
    if (mpz_sgn(t3) > 0) {
      mpz_sqrt(t3, t3); mpz_add(t3, t3, av[s]); mpz_fdiv_q(t3, t3, gv[s]);
      mpz_sqrt(t4, Qv[s]); if (mpz_cmp(t4, t3) < 0) mpz_set(t3, t4);
      if (mpz_cmp_ui(t3, L) >= 0) {
        u64 U2 = mpz_fits_ulong_p(t3) ? mpz_get_ui(t3) : ~0ULL;
        /* AP count, modulus 8F, Q in [L(L+2), Qmax] */
        mpz_mul_2exp(M_, Fv[s], 3);
        int inv_ok = mpz_invert(c_, Pv[s], M_);
        if (!inv_ok) { if (FAKE) return; die("P not invertible mod 8F"); }
        mpz_mul_si(c_, c_, RR); mpz_fdiv_r(c_, c_, M_);
        mpz_set_ui(t1, L); mpz_mul_ui(t1, t1, L + 2);
        mpz_sub(t2, c_, t1); mpz_fdiv_r(t2, t2, M_); mpz_add(Q0_, t1, t2);
        u64 C = 0;
        if (mpz_cmp(Q0_, Qv[s]) <= 0) { mpz_sub(t2, Qv[s], Q0_); mpz_fdiv_q(t2, t2, M_); C = (mpz_fits_ulong_p(t2) && mpz_get_ui(t2) < (1ULL << 62)) ? mpz_get_ui(t2) + 1 : (1ULL << 62); }
        double nB = est_primes(L, U2);
        if ((double)C <= K2 * nB || U2 == ~0ULL) {
          if (U2 == ~0ULL && C > 100000000ULL) die("m2: both options huge");
          st_m2ap[s]++; st_m2apcand[s] += C;
          mpz_set(t1, Q0_);
          for (u64 k = 0; k < C; k++, mpz_add(t1, t1, M_)) {
            /* S = (g Q + a + R)/a */
            mpz_mul(t2, gv[s], t1); mpz_add(t2, t2, av[s]); mpz_add_ui(t2, t2, RR);
            if (!mpz_divisible_p(t2, av[s])) die("m2 AP: S not integral");
            mpz_divexact(t2, t2, av[s]);
            mpz_mul(t3, t2, t2); mpz_submul_ui(t3, t1, 4);
            if (mpz_sgn(t3) < 0 || !mpz_perfect_square_p(t3)) continue;
            mpz_sqrt(t3, t3);
            mpz_t q1, q2; mpz_inits(q1, q2, NULL);
            mpz_sub(q1, t2, t3); mpz_add(q2, t2, t3);
            if (mpz_odd_p(q1) || mpz_odd_p(q2)) { mpz_clears(q1, q2, NULL); continue; }
            mpz_fdiv_q_2exp(q1, q1, 1); mpz_fdiv_q_2exp(q2, q2, 1);
            if (mpz_cmp_ui(q1, plast) > 0 && mpz_cmp(q1, q2) < 0) report_m2(s, q1, q2, "apsq");
            mpz_clears(q1, q2, NULL);
          }
        } else {
          st_m2en[s]++;
          struct m2ctx c; c.U2 = U2;
          c.native = (mpz_sizeinbase(av[s], 2) + 64 - __builtin_clzll(U2 | 1) <= 125);
          if (c.native) {
            c.a = 0; c.g = 0;
            { size_t cnt; u64 w[4] = {0,0,0,0}; mpz_export(w, &cnt, -1, 8, 0, 0, av[s]); if (cnt > 2) die("a too big"); c.a = ((u128)w[1] << 64) | w[0]; }
            { size_t cnt; u64 w[4] = {0,0,0,0}; mpz_export(w, &cnt, -1, 8, 0, 0, gv[s]); if (cnt > 2) die("g too big"); c.g = ((u128)w[1] << 64) | w[0]; }
          }
          u64 j = pidx(L);
          for (; j < NPR; j++) if (!m2_q1(s, PR[j], &c)) break;
          if (j == NPR && U2 > SMAX) { u64 lo = L > SMAX ? L : SMAX + 1; seg_primes(lo, U2, s, m2_q1, &c); }
        }
      }
    }
  }

  /* ---------- m >= 3 ---------- */
  mpz_set_ui(t1, L); mpz_mul_ui(t1, t1, L + 2); mpz_mul_ui(t1, t1, L + 4);
  if (mpz_cmp(t1, Qv[s]) > 0) return;
  mpz_root(t2, Qv[s], 3); u64 cube = mpz_fits_ulong_p(t2) ? mpz_get_ui(t2) : ~0ULL;
  double logQmax = mpz_log(Qv[s]);
  double target = log1p(mpz_get_d(gv[s]) / mpz_get_d(Pv[s]));
  /* children estimate: U3 crude */
  double U3 = 0;
  for (int m = 3; m < 400; m++) {
    double sz = exp(logQmax / m) * (1 + 1e-9) + 2, rb = 1.0 / (-expm1(-target / m)) * (1 + 1e-9) + 2;
    double u = sz < rb ? sz : rb; if (u > U3) U3 = u; if (sz < 5) break;
  }
  if (U3 > (double)cube) U3 = (double)cube;
  double af = 1; for (int i = 0; i < s; i++) af *= 1.0 - 1.0 / (double)(pr[i] - 1);
  double n3 = est_primes(L, (u64)U3) * af;
  /* AP mod 16F count */
  mpz_mul_2exp(M_, Fv[s], 4);
  if (!mpz_invert(c_, Pv[s], M_)) { if (FAKE) return; die("P not invertible mod 16F"); }
  mpz_mul_si(c_, c_, RR); mpz_fdiv_r(c_, c_, M_);
  mpz_sub(t2, c_, t1); mpz_fdiv_r(t2, t2, M_); mpz_add(Q0_, t1, t2);
  u64 C3 = 0;
  if (mpz_cmp(Q0_, Qv[s]) <= 0) { mpz_sub(t2, Qv[s], Q0_); mpz_fdiv_q(t2, t2, M_); C3 = (mpz_fits_ulong_p(t2) && mpz_get_ui(t2) < (1ULL << 62)) ? mpz_get_ui(t2) + 1 : (1ULL << 62); }
  if (C3 == 0) return;
  if (C3 <= T3 || (double)C3 <= K3 * n3) { st_m3eul[s]++; st_m3cand[s] += C3; euler_close(s, L, C3); return; }
  st_m3br[s]++;
  u64 j = pidx(L);
  for (; j < NPR; j++) {
    u64 q = PR[j];
    if (q > cube) return;
    if (!admissible(s, q)) continue;
    if (!feasible(s, q, j, logQmax, target, 3)) return;
    if (q > st_maxq1) st_maxq1 = q;
    pr[s] = q; mpz_mul_ui(Pv[s + 1], Pv[s], q); mpz_mul_ui(Fv[s + 1], Fv[s], q - 1); process(s + 1);
  }
  if (cube > SMAX) {
    struct m3ctx c = { logQmax, target, cube, 0 };
    u64 lo = L > SMAX ? L : SMAX + 1;
    u64 hi = cube; if ((double)hi > U3 + 2) hi = (u64)(U3 + 2);
    if (VERB) { emit_prefix("SEGCHILD prefix", s); fprintf(OUT, " lo %llu hi %llu\n", (unsigned long long)lo, (unsigned long long)hi); }
    if (lo <= hi) seg_primes(lo, hi, s, m3_child, &c);
  }
}

static u64 *stbuf; static u64 stn;
static int st_collect(int s, u64 q, void *ctx) { (void)s; (void)ctx; stbuf[stn++] = q; return 1; }
static int selftest(u64 lo2, u64 hi2) {
  /* 1) ranges inside the table must reproduce the table exactly */
  int bad = 0; stbuf = malloc(sizeof(u64) * 4000000);
  u64 los[] = {5, 6, 7, 100, 9973, 1000003, SMAX / 2 + 1, SMAX - 3000000};
  for (int t = 0; t < 8; t++) {
    u64 lo = los[t], hi = lo + 2999999; if (hi > SMAX) hi = SMAX;
    stn = 0; seg_primes(lo, hi, 0, st_collect, NULL);
    u64 a = pidx(lo), b = pidx(hi + 1);
    if (b - a != stn) bad = 1; else for (u64 i = 0; i < stn; i++) if (stbuf[i] != PR[a + i]) { bad = 1; break; }
    printf("SELFTEST in-table [%llu,%llu]: seg %llu table %llu %s\n", (unsigned long long)lo, (unsigned long long)hi, (unsigned long long)stn, (unsigned long long)(b - a), bad ? "BAD" : "ok");
  }
  /* 2) count in a range beyond the table (compare externally with sympy.primepi) */
  stn = 0; free(stbuf); stbuf = malloc(sizeof(u64) * ((hi2 - lo2) / 4 + 1000));
  seg_primes(lo2, hi2, 0, st_collect, NULL);
  u64 sum = 0; for (u64 i = 0; i < stn; i++) sum += stbuf[i] % 1000003;
  printf("SELFTEST beyond [%llu,%llu]: count %llu first %llu last %llu checksum %llu\n", (unsigned long long)lo2, (unsigned long long)hi2, (unsigned long long)stn,
         (unsigned long long)(stn ? stbuf[0] : 0), (unsigned long long)(stn ? stbuf[stn - 1] : 0), (unsigned long long)sum);
  return bad;
}

int main(int argc, char **argv) {
  mpz_inits(X, t1, t2, t3, t4, t5, M_, c_, Q0_, N_, e_, two_, NULL);
  for (int i = 0; i < MAXD; i++) mpz_inits(Pv[i], Fv[i], av[i], gv[i], Qv[i], NULL);
  mpz_set_ui(two_, 2);
  const char *Xs = "1e30", *taskfile = NULL; int widx = 0, nw = 1;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "-X")) Xs = argv[++i];
    else if (!strcmp(argv[i], "-S")) SMAX = strtoull(argv[++i], 0, 10);
    else if (!strcmp(argv[i], "-D")) D0 = atoi(argv[++i]);
    else if (!strcmp(argv[i], "-gen")) mode_gen = 1;
    else if (!strcmp(argv[i], "-tasks")) taskfile = argv[++i];
    else if (!strcmp(argv[i], "-w")) { widx = atoi(argv[++i]); nw = atoi(argv[++i]); }
    else if (!strcmp(argv[i], "-R")) RR = atol(argv[++i]);
    else if (!strcmp(argv[i], "-v")) VERB = 1;
    else if (!strcmp(argv[i], "-K2")) K2 = atof(argv[++i]);
    else if (!strcmp(argv[i], "-K3")) K3 = atof(argv[++i]);
    else if (!strcmp(argv[i], "-T3")) T3 = strtoull(argv[++i], 0, 10);
    else if (!strcmp(argv[i], "-fake")) FAKE = 1;
    else if (!strcmp(argv[i], "-pmin")) PMIN = strtoull(argv[++i], 0, 10);
    else if (!strcmp(argv[i], "-selftest")) { u64 a = strtoull(argv[++i], 0, 10), b = strtoull(argv[++i], 0, 10); mpz_set_ui(X, 1); sieve_table(SMAX); return selftest(a, b); }
    else { fprintf(stderr, "bad arg %s\n", argv[i]); return 2; }
  }
  OUT = stdout;
  if (Xs[0] == '1' && Xs[1] == 'e') mpz_ui_pow_ui(X, 10, atoi(Xs + 2)); else mpz_set_str(X, Xs, 10);
  struct timespec ts0, ts1; clock_gettime(CLOCK_MONOTONIC, &ts0);
  sieve_table(SMAX);
  gmp_fprintf(OUT, "START X %Zd R %ld fake %d pmin %llu SMAX %llu NPR %llu K2 %g K3 %g T3 %llu\n", X, RR, FAKE, (unsigned long long)PMIN, (unsigned long long)SMAX, (unsigned long long)NPR, K2, K3, (unsigned long long)T3);
  if (!taskfile) { mpz_set_ui(Pv[0], 1); mpz_set_ui(Fv[0], 1); process(0); }
  else {
    FILE *f = fopen(taskfile, "r"); if (!f) die("taskfile");
    char line[8192]; u64 ti = 0;
    while (fgets(line, sizeof line, f)) {
      if (strncmp(line, "TASK", 4)) continue;
      u64 my = ti++; if (my % nw != (u64)widx) continue;
      int s = 0; char *p = line + 4; mpz_set_ui(Pv[0], 1); mpz_set_ui(Fv[0], 1);
      while (*p) { while (*p == ' ') p++; if (*p < '0' || *p > '9') break; u64 v = strtoull(p, &p, 10); pr[s] = v; mpz_mul_ui(Pv[s + 1], Pv[s], v); mpz_mul_ui(Fv[s + 1], Fv[s], v - 1); s++; }
      u64 n0 = 0; for (int d = 0; d < MAXD; d++) n0 += st_nodes[d];
      struct timespec a0, a1; clock_gettime(CLOCK_MONOTONIC, &a0);
      process(s);
      clock_gettime(CLOCK_MONOTONIC, &a1);
      u64 n1 = 0; for (int d = 0; d < MAXD; d++) n1 += st_nodes[d];
      fprintf(OUT, "DONE %llu nodes %llu sec %.2f :", (unsigned long long)my, (unsigned long long)(n1 - n0), (a1.tv_sec - a0.tv_sec) + 1e-9 * (a1.tv_nsec - a0.tv_nsec));
      for (int i = 0; i < s; i++) fprintf(OUT, " %llu", (unsigned long long)pr[i]); fprintf(OUT, "\n"); fflush(OUT);
    }
    fclose(f);
  }
  clock_gettime(CLOCK_MONOTONIC, &ts1);
  u64 tn = 0;
  fprintf(OUT, "STATS d nodes m2ap m2apcand m2en m2q1 m3eul m3cand m3euler m3br\n");
  for (int d = 0; d < MAXD; d++) {
    if (!st_nodes[d]) continue; tn += st_nodes[d];
    fprintf(OUT, "D %d %llu %llu %llu %llu %llu %llu %llu %llu %llu\n", d, (unsigned long long)st_nodes[d], (unsigned long long)st_m2ap[d], (unsigned long long)st_m2apcand[d],
            (unsigned long long)st_m2en[d], (unsigned long long)st_m2q1[d], (unsigned long long)st_m3eul[d], (unsigned long long)st_m3cand[d], (unsigned long long)st_m3euler[d], (unsigned long long)st_m3br[d]);
  }
  u64 a1 = 0, a2 = 0, a3 = 0; for (int d = 0; d < MAXD; d++) { a1 += st_m2apcand[d]; a2 += st_m2q1[d]; a3 += st_m3euler[d]; }
  fprintf(OUT, "TOTAL nodes %llu m2apcand %llu m2q1 %llu m3euler %llu m1int %llu m2int %llu euler_pass %llu solutions %llu segq %llu segchild %llu maxq1 %llu ntask %llu wall %.1f\n",
          (unsigned long long)tn, (unsigned long long)a1, (unsigned long long)a2, (unsigned long long)a3, (unsigned long long)st_m1int, (unsigned long long)st_m2int,
          (unsigned long long)st_euler_pass, (unsigned long long)st_solutions, (unsigned long long)st_segq, (unsigned long long)st_segchild, (unsigned long long)st_maxq1,
          (unsigned long long)st_ntask, (ts1.tv_sec - ts0.tv_sec) + 1e-9 * (ts1.tv_nsec - ts0.tv_nsec));
  return 0;
}
