/* vlrt2.c -- independent engine, revision 2: revision-1 engine vlrt.c + own segmented sieve to 2^32, own m=2 candidate closure at
 * large nodes (CC), own trial-division prefilter before Euler (TDB). Author lcrt5.c NOT read.
 * vlrt.c -- independent reimplementation of LCAP-1 / LCRT-1..4 from SPEC_LCAP1.md + SPEC_LCRT.md text only
 * (author's lcrt.c NOT read).  Exact GMP integers for every decision.  pthreads, tasks at depth D0.
 * usage: vlrt X SIEVE D0 THREADS SIGMA PMIN CRT KMAX FILT EULER outprefix
 */
#include <stdio.h>
#include <gmp.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <math.h>

#define MAXD 48
static uint32_t *PR; static int64_t NPR;
static mpz_t X; static long SIGMA, PMIN; static int CRT, KMAX, FILT, EULER, D0, NT; static uint64_t CC = 0, TDB = 0;
static pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
static FILE *fev, *ftask;

static uint64_t sm(uint64_t x){ x += 0x9E3779B97F4A7C15ULL; x = (x ^ (x>>30)) * 0xBF58476D1CE4E5B9ULL;
  x = (x ^ (x>>27)) * 0x94D049BB133111EBULL; return x ^ (x>>31); }

typedef struct {
  uint64_t nodes[MAXD], pruned[MAXD], live[MAXD], small[MAXD], eclosed[MAXD], epass[MAXD], kfa[MAXD], kfb[MAXD],
           c2p[MAXD], c2a[MAXD], c2i[MAXD], cand[MAXD], sqhit[MAXD], c2n[MAXD], c2c[MAXD], c2sq[MAXD], tdrej[MAXD], nev;
  uint64_t digest, digest_live, maxq; int big;
} Cnt;

typedef struct {
  Cnt c;
  uint64_t pre[MAXD];
  mpz_t P[MAXD], F[MAXD];
  mpz_t A, lo, XP, s, M, Q0, Q1, K, L, t1, t2, t3, t4, t5, t6, D, qb, qa, u, n, r, N, e;
  int top; /* top pass: record tasks at depth D0 */
  uint64_t (*tasks)[MAXD]; int64_t ntasks, cap;
} Ctx;

static void subsig(mpz_t r, mpz_t a){ if (SIGMA>=0) mpz_sub_ui(r,a,(unsigned long)SIGMA); else mpz_add_ui(r,a,(unsigned long)(-SIGMA)); }
static void die(const char *m){ fprintf(stderr, "ABORT: %s\n", m); exit(3); }

static uint64_t H(mpz_t P, int *big){
  mpz_t t; mpz_init(t);
  uint64_t lo64 = mpz_getlimbn(P,0);
  mpz_tdiv_q_2exp(t, P, 64);
  if (mpz_sizeinbase(t,2) > 64) *big = 1;
  uint64_t hi = mpz_getlimbn(t,0); if (mpz_sgn(t)==0) hi = 0;
  mpz_clear(t);
  return sm(lo64 ^ sm(hi));
}

static int64_t first_ge(uint64_t x){ /* first index with PR[i] >= x */
  int64_t a = 0, b = NPR; while (a < b){ int64_t m = (a+b)/2; if (PR[m] < x) a = m+1; else b = m; } return a; }

/* c3 && c4 at prime index j for node (P,F) */
static int okj(Ctx *c, int d, int64_t j){
  if (j + 40 >= NPR) die("sieve too small in child scan");
  uint64_t q = PR[j];
  mpz_mul_ui(c->t1, c->P[d], q);            /* running P q prod pi */
  mpz_set_ui(c->t2, 1);                     /* prod (pi-1) */
  int m = 0;
  for (;;){
    uint64_t nx = PR[j+m+1];
    mpz_mul_ui(c->t3, c->t1, nx);
    if (mpz_cmp(c->t3, X) > 0) break;
    mpz_set(c->t1, c->t3); mpz_mul_ui(c->t2, c->t2, nx-1); m++;
    if (j+m+2 >= NPR) die("sieve too small in c4");
  }
  if (m < 2) return 0;
  /* (2F(q-1) - [sigma=-1]) * prod(pi-1) */
  mpz_mul_ui(c->t3, c->F[d], q-1); mpz_mul_2exp(c->t3, c->t3, 1);
  if (SIGMA == -1) mpz_sub_ui(c->t3, c->t3, 1);
  mpz_mul(c->t3, c->t3, c->t2);
  return mpz_cmp(c->t1, c->t3) > 0;
}

static uint64_t invmod(uint64_t a, uint64_t m){ /* a,m coprime, m < 2^32 */
  int64_t t = 0, nt = 1; int64_t r = (int64_t)m, nr = (int64_t)(a % m);
  while (nr){ int64_t qq = r / nr, tmp = t - qq*nt; t = nt; nt = tmp; tmp = r - qq*nr; r = nr; nr = tmp; }
  if (r != 1) die("noninvertible");
  if (t < 0) t += (int64_t)m; return (uint64_t)t;
}

static void event(Ctx *c, int d, const char *kind, mpz_t q, mpz_t r, const char *reason){
  pthread_mutex_lock(&mtx);
  fprintf(fev, "{\"kind\":\"%s\",\"prefix\":[", kind);
  for (int i = 0; i < d; i++) fprintf(fev, "%s%llu", i?",":"", (unsigned long long)c->pre[i]);
  gmp_fprintf(fev, "],\"q\":\"%Zd\",\"r\":\"%Zd\",\"reason\":\"%s\"}\n", q, r, reason);
  fflush(fev);
  pthread_mutex_unlock(&mtx);
  c->c.nev++;
}

/* classify a pair (q,r) completing prefix at depth d: integral already */
static const char *classify(Ctx *c, int d, mpz_t q, mpz_t r){
  if (mpz_cmp(r, q) <= 0) return "r<=q";
  mpz_mul(c->t5, c->P[d], q); mpz_mul(c->t5, c->t5, r);
  if (mpz_cmp(c->t5, X) > 0) return "cap";
  mpz_sub_ui(c->t6, r, 1); mpz_mul(c->t5, c->P[d], q); mpz_gcd(c->t6, c->t6, c->t5);
  if (mpz_cmp_ui(c->t6, 1) != 0) return "C-violation";
  if (mpz_probab_prime_p(r, 40) == 0) return "r composite";
  if (mpz_probab_prime_p(q, 40) == 0) return "q composite";
  /* exact identity recheck */
  mpz_mul(c->t5, c->P[d], q); mpz_mul(c->t5, c->t5, r);
  mpz_sub_ui(c->t6, q, 1); mpz_mul(c->t6, c->t6, c->F[d]); mpz_sub_ui(c->N, r, 1); mpz_mul(c->t6, c->t6, c->N);
  mpz_mul_2exp(c->t6, c->t6, 1); mpz_sub(c->t5, c->t5, c->t6);
  if (mpz_cmp_si(c->t5, SIGMA) != 0) return "identity-fail";
  return "SOLUTION";
}

static void visit(Ctx *c, int d);

static void children(Ctx *c, int d, int filt, int small){
  (void)small;
  /* shortcut: P lo (lo+2)(lo+4) > X -> none */
  mpz_add_ui(c->t1, c->lo, 2); mpz_mul(c->t1, c->t1, c->lo); mpz_add_ui(c->t2, c->lo, 4); mpz_mul(c->t1, c->t1, c->t2);
  mpz_mul(c->t1, c->t1, c->P[d]);
  if (mpz_cmp(c->t1, X) > 0) return;
  if (mpz_sizeinbase(c->lo, 2) > 40) die("lo too large for sieve");
  uint64_t lo = mpz_get_ui(c->lo);
  if (lo > PR[NPR-1]) die("lo beyond sieve");
  int64_t j0 = first_ge(lo);
  if (!okj(c, d, j0)) return;
  int64_t step = 1, good = j0, bad;
  for (;;){ int64_t j = j0 + step; if (j + 60 >= NPR) die("sieve too small (gallop)");
    if (okj(c, d, j)){ good = j; step *= 2; } else { bad = j; break; } }
  while (bad - good > 1){ int64_t mid = good + (bad-good)/2; if (okj(c, d, mid)) good = mid; else bad = mid; }
  /* need copies of node data: Q1, M, K live in ctx and get overwritten by recursion -> save */
  mpz_t Q1, M, K; mpz_init_set(Q1, c->Q1); mpz_init_set(M, c->M); mpz_init_set(K, c->K);
  int kbig = filt ? (mpz_sizeinbase(K,2) > 40) : 1;
  uint64_t Kv = kbig ? 0 : mpz_get_ui(K);
  for (int64_t j = j0; j <= good; j++){
    uint64_t q = PR[j];
    if (q > c->c.maxq) c->c.maxq = q;
    int adm = 1;
    for (int i = 0; i < d; i++) if (q % c->pre[i] == 1){ adm = 0; break; }
    int pass = 1;
    if (filt && !kbig && Kv < q){
      uint64_t a = mpz_fdiv_ui(Q1, q); uint64_t mq = mpz_fdiv_ui(M, q);
      uint64_t neg = (q - a) % q; uint64_t k0 = (unsigned __int128)neg * invmod(mq, q) % q;
      if (k0 >= Kv) pass = 0;
    }
    if (!pass){ c->c.kfa[d+1]++; if (adm) c->c.kfb[d+1]++; }
    if (!adm || !pass) continue;
    c->pre[d] = q; mpz_mul_ui(c->P[d+1], c->P[d], q); mpz_mul_ui(c->F[d+1], c->F[d], q-1);
    visit(c, d+1);
  }
  mpz_clear(Q1); mpz_clear(M); mpz_clear(K);
}

/* h(q) = A q^2 - 4F q + 2F + sigma < 0 ? */
static int hneg(Ctx *c, int d, mpz_t q){
  mpz_mul(c->t1, q, q); mpz_mul(c->t1, c->t1, c->A);
  mpz_mul(c->t2, c->F[d], q); mpz_mul_2exp(c->t2, c->t2, 2); mpz_sub(c->t1, c->t1, c->t2);
  mpz_mul_2exp(c->t2, c->F[d], 1); mpz_add(c->t1, c->t1, c->t2);
  if (SIGMA >= 0) mpz_add_ui(c->t1, c->t1, SIGMA); else mpz_sub_ui(c->t1, c->t1, -SIGMA);
  return mpz_sgn(c->t1) < 0;
}
/* cap(q): P q n(q) <= X u(q) */
static int capok(Ctx *c, int d, mpz_t q){
  mpz_sub_ui(c->t1, q, 1); mpz_mul(c->t1, c->t1, c->F[d]); mpz_mul_2exp(c->t1, c->t1, 1);
  if (SIGMA >= 0) mpz_sub_ui(c->t1, c->t1, SIGMA); else mpz_add_ui(c->t1, c->t1, -SIGMA); /* n */
  mpz_mul(c->t1, c->t1, q); mpz_mul(c->t1, c->t1, c->P[d]);
  mpz_mul(c->t2, c->A, q); mpz_mul_2exp(c->t3, c->F[d], 1); mpz_sub(c->t2, c->t2, c->t3); /* u */
  if (mpz_sgn(c->t2) <= 0) return 0;
  mpz_mul(c->t2, c->t2, X);
  return mpz_cmp(c->t1, c->t2) <= 0;
}

/* own m=2 candidate closure at a LIVE large node: every m=2 completion N = P q r has Q = q r among the K CRT candidates
   Q1 + i M (Lemma CRT), and q + r = Q - Psi + 1 with Psi = (P Q - sigma)/(2F) = (q-1)(r-1). */
static void candc2(Ctx *c, int d, uint64_t Kv){
  c->c.c2n[d]++;
  mpz_t Q, q, r; mpz_init(Q); mpz_init(q); mpz_init(r);
  for (uint64_t i = 0; i < Kv; i++){
    c->c.c2c[d]++;
    mpz_mul_ui(Q, c->M, i); mpz_add(Q, Q, c->Q1);
    mpz_mul(c->t1, c->P[d], Q); subsig(c->t1, c->t1);
    mpz_mul_2exp(c->t2, c->F[d], 1);
    if (!mpz_divisible_p(c->t1, c->t2)) die("Psi not integral (candc2)");
    mpz_divexact(c->t1, c->t1, c->t2);
    mpz_sub(c->t3, Q, c->t1); mpz_add_ui(c->t3, c->t3, 1);
    mpz_mul(c->t4, c->t3, c->t3); mpz_mul_2exp(c->t2, Q, 2); mpz_sub(c->t4, c->t4, c->t2);
    if (mpz_sgn(c->t4) > 0 && mpz_perfect_square_p(c->t4)){
      c->c.c2sq[d]++;
      mpz_sqrt(c->t4, c->t4); mpz_sub(q, c->t3, c->t4); mpz_fdiv_q_2exp(q, q, 1); mpz_add(r, c->t3, c->t4); mpz_fdiv_q_2exp(r, r, 1);
      const char *why = (mpz_cmp(q, c->lo) < 0) ? "q<lo" : (mpz_probab_prime_p(q,40)==0 ? "q composite" : classify(c, d, q, r));
      event(c, d, "C2K", q, r, why);
    }
  }
  mpz_clear(Q); mpz_clear(q); mpz_clear(r);
}

static void c2(Ctx *c, int d, int crtlive){
  /* D = 4F^2 - A(2F+sigma) */
  mpz_mul(c->D, c->F[d], c->F[d]); mpz_mul_2exp(c->D, c->D, 2);
  mpz_mul_2exp(c->t4, c->F[d], 1); if (SIGMA>=0) mpz_add_ui(c->t4, c->t4, SIGMA); else mpz_sub_ui(c->t4, c->t4, -SIGMA);
  mpz_mul(c->t4, c->t4, c->A); mpz_sub(c->D, c->D, c->t4);
  if (mpz_sgn(c->D) <= 0) return;
  mpz_sqrt(c->t4, c->D); mpz_add_ui(c->t4, c->t4, 1); mpz_mul_2exp(c->t5, c->F[d], 1); mpz_add(c->t4, c->t4, c->t5);
  mpz_fdiv_q(c->qb, c->t4, c->A); mpz_add_ui(c->qb, c->qb, 1);
  while (mpz_cmp(c->qb, c->lo) >= 0 && !hneg(c, d, c->qb)) mpz_sub_ui(c->qb, c->qb, 1);
  if (mpz_cmp(c->qb, c->lo) < 0) return;
  if (mpz_cmp(c->qb, c->s) > 0) mpz_set(c->qb, c->s);
  if (mpz_cmp(c->qb, c->lo) < 0) return;
  if (!capok(c, d, c->qb)) return;
  /* smallest qa in [lo,qb] with cap */
  if (capok(c, d, c->lo)) mpz_set(c->qa, c->lo);
  else { mpz_set(c->t5, c->lo); mpz_set(c->t6, c->qb); /* t5 bad, t6 good */
    for (;;){ mpz_sub(c->e, c->t6, c->t5); if (mpz_cmp_ui(c->e, 1) <= 0) break;
      mpz_add(c->e, c->t5, c->t6); mpz_fdiv_q_2exp(c->e, c->e, 1);
      if (capok(c, d, c->e)) mpz_set(c->t6, c->e); else mpz_set(c->t5, c->e); }
    mpz_set(c->qa, c->t6); }
  if (mpz_cmp(c->qb, c->qa) < 0) die("qb < qa");
  if (crtlive && CC > 0 && mpz_sizeinbase(c->K, 2) <= 40){
    uint64_t Kv = mpz_get_ui(c->K);
    mpz_sub(c->e, c->qb, c->qa); mpz_add_ui(c->e, c->e, 1);
    int beyond = mpz_cmp_ui(c->qb, PR[NPR-1]) > 0;
    if (beyond || mpz_sizeinbase(c->e, 2) > 60 || Kv * CC < mpz_get_ui(c->e)){
      if (mpz_cmp_ui(c->qb, c->c.maxq) > 0 && mpz_sizeinbase(c->qb,2) <= 63) c->c.maxq = mpz_get_ui(c->qb);
      candc2(c, d, Kv); return; }
  }
  if (mpz_sizeinbase(c->qb, 2) > 40) die("C2 qb too large");
  uint64_t qa = mpz_get_ui(c->qa), qb = mpz_get_ui(c->qb);
  if (qb > PR[NPR-1]) die("C2 beyond sieve");
  mpz_t q; mpz_init(q);
  for (int64_t j = first_ge(qa); j < NPR && PR[j] <= qb; j++){
    uint64_t qq = PR[j]; if (qq > c->c.maxq) c->c.maxq = qq;
    c->c.c2p[d]++;
    int adm = 1; for (int i = 0; i < d; i++) if (qq % c->pre[i] == 1){ adm = 0; break; }
    if (!adm) continue;
    c->c.c2a[d]++;
    mpz_mul_ui(c->u, c->A, qq); mpz_mul_2exp(c->t1, c->F[d], 1); mpz_sub(c->u, c->u, c->t1);
    mpz_mul_ui(c->n, c->F[d], qq-1); mpz_mul_2exp(c->n, c->n, 1);
    if (SIGMA>=0) mpz_sub_ui(c->n, c->n, SIGMA); else mpz_add_ui(c->n, c->n, -SIGMA);
    if (mpz_divisible_p(c->n, c->u)){
      c->c.c2i[d]++; mpz_divexact(c->r, c->n, c->u); mpz_set_ui(q, qq);
      event(c, d, "C2", q, c->r, classify(c, d, q, c->r));
    }
  }
  mpz_clear(q);
}

static void visit(Ctx *c, int d){
  if (d >= MAXD-2) die("depth");
  if (c->top && d == D0){
    if (c->ntasks == c->cap){ c->cap = c->cap ? 2*c->cap : 1024; c->tasks = realloc(c->tasks, c->cap * sizeof(*c->tasks)); }
    memcpy(c->tasks[c->ntasks], c->pre, sizeof(uint64_t)*MAXD); c->ntasks++; return;
  }
  Cnt *k = &c->c;
  k->nodes[d]++; k->digest += H(c->P[d], &k->big);
  uint64_t last = d ? c->pre[d-1] : (uint64_t)(PMIN - 1);
  mpz_mul_2exp(c->A, c->F[d], 1); mpz_sub(c->A, c->A, c->P[d]);
  if (mpz_sgn(c->A) <= 0) die("A <= 0 at a node");
  mpz_mul_2exp(c->t1, c->F[d], 1); mpz_fdiv_q(c->lo, c->t1, c->A); mpz_add_ui(c->lo, c->lo, 1);
  if (mpz_cmp_ui(c->lo, last+1) < 0) mpz_set_ui(c->lo, last+1);
  mpz_fdiv_q(c->XP, X, c->P[d]); mpz_sqrt(c->s, c->XP);
  if (mpz_cmp(c->lo, c->s) > 0){ if (CRT) k->pruned[d]++; return; }
  if (!CRT){ c2(c, d, 0); children(c, d, 0, 0); return; }
  mpz_mul_2exp(c->M, c->F[d], 3);
  if (!mpz_invert(c->Q0, c->P[d], c->M)) die("P not invertible mod 8F");
  mpz_mul_si(c->Q0, c->Q0, SIGMA); mpz_fdiv_r(c->Q0, c->Q0, c->M);
  mpz_add_ui(c->L, c->lo, 2); mpz_mul(c->L, c->L, c->lo);
  mpz_sub(c->t1, c->Q0, c->L); mpz_fdiv_r(c->t1, c->t1, c->M); mpz_add(c->Q1, c->L, c->t1);
  if (mpz_cmp(c->Q1, c->XP) > 0){ k->pruned[d]++; return; }
  mpz_sub(c->K, c->XP, c->Q1); mpz_fdiv_q(c->K, c->K, c->M); mpz_add_ui(c->K, c->K, 1);
  k->live[d]++; k->digest_live += H(c->P[d], &k->big);
  int small = (KMAX > 0 && mpz_cmp_ui(c->K, KMAX) <= 0);
  if (!small){ c2(c, d, 1); children(c, d, FILT, 0); return; }
  k->small[d]++;
  long Kv = mpz_get_si(c->K);
  if (EULER){
    int anypass = 0;
    for (long i = 0; i < Kv; i++){
      mpz_mul_ui(c->t1, c->M, i); mpz_add(c->t1, c->t1, c->Q1);
      if (TDB > 0){ /* genuine Q has every prime factor >= lo: reject Q with an odd prime factor < min(lo, TDB) */
        uint64_t lim = TDB; if (mpz_cmp_ui(c->lo, lim) < 0) lim = mpz_get_ui(c->lo);
        int rej = 0; for (int64_t j = 0; j < NPR && PR[j] < lim; j++) if (mpz_divisible_ui_p(c->t1, PR[j])){ rej = 1; break; }
        if (rej){ k->tdrej[d]++; continue; } }
      mpz_mul(c->N, c->t1, c->P[d]);
      subsig(c->e, c->N); mpz_fdiv_q_2exp(c->e, c->e, 1);
      mpz_set_ui(c->t2, 2); mpz_powm(c->t2, c->t2, c->e, c->N);
      if (mpz_cmp_ui(c->t2, 1) == 0){ anypass = 1; }
    }
    if (!anypass){ k->eclosed[d]++; return; }
    k->epass[d]++;
  }
  /* exact m=2 closure on every candidate */
  mpz_t q, r, Q; mpz_init(q); mpz_init(r); mpz_init(Q);
  for (long i = 0; i < Kv; i++){
    k->cand[d]++;
    mpz_mul_ui(Q, c->M, i); mpz_add(Q, Q, c->Q1);
    mpz_mul(c->t1, c->P[d], Q); subsig(c->t1, c->t1);
    mpz_mul_2exp(c->t2, c->F[d], 1);
    if (!mpz_divisible_p(c->t1, c->t2)) die("Psi not integral");
    mpz_divexact(c->t1, c->t1, c->t2);           /* Psi */
    mpz_sub(c->t3, Q, c->t1); mpz_add_ui(c->t3, c->t3, 1); /* sum */
    mpz_mul(c->t4, c->t3, c->t3); mpz_mul_2exp(c->t2, Q, 2); mpz_sub(c->t4, c->t4, c->t2);
    if (mpz_sgn(c->t4) > 0 && mpz_perfect_square_p(c->t4)){
      k->sqhit[d]++;
      mpz_sqrt(c->t4, c->t4); mpz_sub(q, c->t3, c->t4); mpz_fdiv_q_2exp(q, q, 1); mpz_add(r, c->t3, c->t4); mpz_fdiv_q_2exp(r, r, 1);
      const char *why = (mpz_cmp(q, c->lo) < 0) ? "q<lo" : (mpz_probab_prime_p(q,40)==0 ? "q composite" : classify(c, d, q, r));
      event(c, d, "SQ", q, r, why);
    }
  }
  mpz_clear(q); mpz_clear(r); mpz_clear(Q);
  children(c, d, 1, 1);
}

static Ctx *newctx(void){
  Ctx *c = calloc(1, sizeof(Ctx));
  for (int i = 0; i < MAXD; i++){ mpz_init(c->P[i]); mpz_init(c->F[i]); }
  mpz_t *v[] = {&c->A,&c->lo,&c->XP,&c->s,&c->M,&c->Q0,&c->Q1,&c->K,&c->L,&c->t1,&c->t2,&c->t3,&c->t4,&c->t5,&c->t6,&c->D,&c->qb,&c->qa,&c->u,&c->n,&c->r,&c->N,&c->e};
  for (size_t i = 0; i < sizeof(v)/sizeof(v[0]); i++) mpz_init(*v[i]);
  return c;
}

static uint64_t (*TASKS)[MAXD]; static int64_t NTASK; static int64_t NEXT = 0;
static Cnt TOT; static Cnt TOP; static int64_t *ORIG_G;

static void addcnt(Cnt *a, Cnt *b){
  for (int i = 0; i < MAXD; i++){ a->nodes[i]+=b->nodes[i]; a->pruned[i]+=b->pruned[i]; a->live[i]+=b->live[i];
    a->small[i]+=b->small[i]; a->eclosed[i]+=b->eclosed[i]; a->epass[i]+=b->epass[i]; a->kfa[i]+=b->kfa[i]; a->kfb[i]+=b->kfb[i];
    a->c2p[i]+=b->c2p[i]; a->c2a[i]+=b->c2a[i]; a->c2i[i]+=b->c2i[i]; a->cand[i]+=b->cand[i]; a->sqhit[i]+=b->sqhit[i]; a->c2n[i]+=b->c2n[i]; a->c2c[i]+=b->c2c[i]; a->c2sq[i]+=b->c2sq[i]; a->tdrej[i]+=b->tdrej[i]; }
  a->digest += b->digest; a->digest_live += b->digest_live; a->nev += b->nev; if (b->maxq > a->maxq) a->maxq = b->maxq; a->big |= b->big;
}

static void parr(FILE *f, const char *name, uint64_t *v, int comma){
  int hi = 0; for (int i = 0; i < MAXD; i++) if (v[i]) hi = i+1;
  fprintf(f, "\"%s\":[", name); for (int i = 0; i < hi; i++) fprintf(f, "%s%llu", i?",":"", (unsigned long long)v[i]); fprintf(f, "]%s", comma?",":"");
}
static void pcnt(FILE *f, Cnt *k){
  parr(f,"nodes",k->nodes,1); parr(f,"pruned",k->pruned,1); parr(f,"live",k->live,1); parr(f,"small",k->small,1);
  parr(f,"eclosed",k->eclosed,1); parr(f,"epass",k->epass,1); parr(f,"kfa",k->kfa,1); parr(f,"kfb",k->kfb,1);
  parr(f,"c2p",k->c2p,1); parr(f,"c2a",k->c2a,1); parr(f,"c2i",k->c2i,1); parr(f,"cand",k->cand,1); parr(f,"sqhit",k->sqhit,1); parr(f,"c2n",k->c2n,1); parr(f,"c2c",k->c2c,1); parr(f,"c2sq",k->c2sq,1); parr(f,"tdrej",k->tdrej,1);
  fprintf(f, "\"digest\":\"%016llx\",\"digest_live\":\"%016llx\",\"nev\":%llu,\"maxq\":%llu,\"big128\":%d",
    (unsigned long long)k->digest, (unsigned long long)k->digest_live, (unsigned long long)k->nev, (unsigned long long)k->maxq, k->big);
}

static void *worker(void *arg){
  (void)arg; Ctx *c = newctx();
  for (;;){
    pthread_mutex_lock(&mtx); int64_t t = NEXT++; pthread_mutex_unlock(&mtx);
    if (t >= NTASK) break;
    memset(&c->c, 0, sizeof(Cnt));
    memcpy(c->pre, TASKS[t], sizeof(uint64_t)*MAXD);
    mpz_set_ui(c->P[0], 1); mpz_set_ui(c->F[0], 1);
    for (int i = 0; i < D0; i++){ mpz_mul_ui(c->P[i+1], c->P[i], c->pre[i]); mpz_mul_ui(c->F[i+1], c->F[i], c->pre[i]-1); }
    visit(c, D0);
    pthread_mutex_lock(&mtx);
    fprintf(ftask, "{\"task\":%lld,\"prefix\":[", (long long)ORIG_G[t]); for (int i = 0; i < D0; i++) fprintf(ftask, "%s%llu", i?",":"", (unsigned long long)c->pre[i]);
    fprintf(ftask, "],"); pcnt(ftask, &c->c); fprintf(ftask, "}\n"); fflush(ftask);
    addcnt(&TOT, &c->c);
    pthread_mutex_unlock(&mtx);
  }
  return NULL;
}

int main(int argc, char **argv){
  if (argc < 12){ fprintf(stderr, "usage: vlrt X SIEVE D0 THREADS SIGMA PMIN CRT KMAX FILT EULER out\n"); return 1; }
  mpz_init_set_str(X, argv[1], 10);
  uint64_t LIM = strtoull(argv[2],0,10); D0 = atoi(argv[3]); NT = atoi(argv[4]); SIGMA = atol(argv[5]); PMIN = atol(argv[6]);
  CRT = atoi(argv[7]); KMAX = atoi(argv[8]); FILT = atoi(argv[9]); EULER = atoi(argv[10]);
  if (argc > 12) CC = strtoull(argv[12],0,10); if (argc > 13) TDB = strtoull(argv[13],0,10);
  char fn[1024];
  snprintf(fn, sizeof fn, "%s.events.jsonl", argv[11]); fev = fopen(fn, "w");
  snprintf(fn, sizeof fn, "%s.tasks.jsonl", argv[11]); ftask = fopen(fn, "w");
  /* own segmented odd sieve (revision 2): base primes <= isqrt(LIM), segments of 2^21 integers */
  if (LIM > 4294967295ULL) die("LIM > 2^32-1");
  { uint64_t rt = 1; while ((rt+1)*(rt+1) <= LIM) rt++;
    uint8_t *bs = calloc(rt+2, 1); uint32_t *base = malloc(sizeof(uint32_t)*(rt+2)); int64_t nbase = 0;
    for (uint64_t i = 2; i <= rt; i++) if (!bs[i]){ if (i > 2) base[nbase++] = (uint32_t)i; for (uint64_t j = i*i; j <= rt; j += i) bs[j] = 1; }
    int64_t capP = (int64_t)(LIM / 15) + 100000; if (LIM > 100000) capP = (int64_t)(1.3 * (double)LIM / (log((double)LIM) - 1.1)) + 100000;
    PR = malloc(capP * sizeof(uint32_t)); NPR = 0;
    const uint64_t SEG = 1ULL << 21; uint8_t *seg = malloc(SEG/2 + 8);
    for (uint64_t lo0 = 0; lo0 <= LIM; lo0 += SEG){
      uint64_t hi0 = lo0 + SEG; if (hi0 > LIM + 1) hi0 = LIM + 1;
      uint64_t cnt = (hi0 - lo0) / 2; memset(seg, 0, cnt);
      for (int64_t b = 0; b < nbase; b++){
        uint64_t p = base[b]; if (p*p >= hi0) break;
        uint64_t st = p*p;
        if (st < lo0 + 1){ st = ((lo0 + 1 + p - 1) / p) * p; if (!(st & 1)) st += p; }
        for (uint64_t n = st; n < hi0; n += 2*p) seg[(n - lo0 - 1) >> 1] = 1;
      }
      for (uint64_t kk = 0; kk < cnt; kk++) if (!seg[kk]){ uint64_t n = lo0 + 1 + 2*kk; if (n >= 3 && n <= LIM){
        if (NPR >= capP) die("PR capacity"); PR[NPR++] = (uint32_t)n; } }
    }
    free(seg); free(bs); free(base);
  }
  fprintf(stderr, "sieve: %lld odd primes <= %llu, largest %u\n", (long long)NPR, (unsigned long long)LIM, PR[NPR-1]);
  if (getenv("VSIEVEONLY")) return 0;
  if ((uint64_t)PR[NPR-1] >= (1ULL<<32)) die("sieve >= 2^32");
  /* top pass */
  Ctx *c = newctx(); c->top = 1;
  mpz_set_ui(c->P[0], 1); mpz_set_ui(c->F[0], 1);
  visit(c, 0);
  TOP = c->c; TASKS = c->tasks; NTASK = c->ntasks;
  /* optional task subset: VSTRIDE=s VOFF=o keeps task indices i with i % s == o; VSEL=file adds listed prefixes
     (one comma-separated prefix of length D0 per line). Kept tasks are logged with their ORIGINAL index. */
  { int64_t *ORIG = malloc(sizeof(int64_t) * (NTASK + 1));
    int64_t s = getenv("VSTRIDE") ? atoll(getenv("VSTRIDE")) : 0, o = getenv("VOFF") ? atoll(getenv("VOFF")) : 0;
    const char *sel = getenv("VSEL"); uint64_t (*SL)[MAXD] = 0; int64_t nsl = 0;
    if (sel){ FILE *fsel = fopen(sel, "r"); char line[4096]; SL = malloc(sizeof(*SL) * 100000);
      while (fsel && fgets(line, sizeof line, fsel)){ int i = 0; char *p = line; memset(SL[nsl], 0, sizeof(SL[nsl]));
        while (*p && i < MAXD){ while (*p == ' ' || *p == ',') p++; if (*p < '0' || *p > '9') break; SL[nsl][i++] = strtoull(p, &p, 10); }
        if (i == D0) nsl++; }
      if (fsel) fclose(fsel); fprintf(stderr, "VSEL: %lld prefixes\n", (long long)nsl); }
    int64_t w = 0;
    for (int64_t t = 0; t < NTASK; t++){
      int keep = 1;
      if (s > 0 && t % s != o) keep = 0;
      if (sel){ int hit = 0; for (int64_t z = 0; z < nsl && !hit; z++) if (!memcmp(SL[z], TASKS[t], sizeof(uint64_t)*D0)) hit = 1;
        if (s > 0) keep = keep || hit; else keep = hit; }
      if (keep){ if (w != t) memcpy(TASKS[w], TASKS[t], sizeof(uint64_t)*MAXD); ORIG[w] = t; w++; }
    }
    if (w != NTASK) fprintf(stderr, "task subset: %lld of %lld\n", (long long)w, (long long)NTASK);
    NTASK = w; ORIG_G = ORIG; }
  fprintf(stderr, "top done: %lld tasks at depth %d\n", (long long)NTASK, D0);
  pthread_t th[256]; for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, worker, 0);
  for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
  addcnt(&TOT, &TOP);
  snprintf(fn, sizeof fn, "%s.summary.json", argv[11]); FILE *fs = fopen(fn, "w");
  gmp_fprintf(fs, "{\"X\":\"%Zd\",\"cc\":%llu,\"tdb\":%llu,\"sigma\":%ld,\"pmin\":%ld,\"crt\":%d,\"kmax\":%d,\"filt\":%d,\"euler\":%d,\"sieve\":%llu,\"D0\":%d,\"ntasks\":%lld,\"complete\":true,",
    X, (unsigned long long)CC, (unsigned long long)TDB, SIGMA, PMIN, CRT, KMAX, FILT, EULER, (unsigned long long)LIM, D0, (long long)NTASK);
  fprintf(fs, "\"top\":{"); pcnt(fs, &TOP); fprintf(fs, "},"); pcnt(fs, &TOT); fprintf(fs, "}\n"); fclose(fs);
  fclose(fev); fclose(ftask);
  fprintf(stderr, "DONE\n");
  return 0;
}
