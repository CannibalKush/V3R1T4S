/* xchk.c: exact all-pairs diameter checker for (Delta,D) graphs, written from the definition (shares no code with
 * the other checkers used for this family).
 *
 * Input: edge list "u v" per line (0-based ids; lines starting with '#' or blank are skipped; extra columns ignored).
 * Checks: no loops, no repeated edges (either orientation), ids contiguous 0..N-1 (every id has degree >= 1),
 *         max degree <= Delta, and for EVERY source s: every vertex within distance D of s.
 * Method: sources in batches of 64*W (W=8 -> 512); per batch a bit-parallel BFS where bit b of vis[v] means
 *         d(src_b, v) <= current level. Level step: nxt[v] = (OR_{u in N(v)} fr[u]) & ~vis[v] (pull), or push from the
 *         active list when the frontier is small. After D levels, any zero bit in vis[v] (within the batch mask)
 *         is an ordered pair (s,v) with d(s,v) > D or unreachable. Threads: pthreads, batches distributed by an
 *         atomic counter, each thread owns its arrays.
 * Output: one RESULT line: N M maxdeg degree-histogram loops dups gaps bad_pairs bad_sources ecc-histogram (ecc<=D
 *         counted exactly via the level at which each source's batch row became complete) and VALID/INVALID.
 * usage: xchk GRAPH Delta D [threads]
 * Optional: environment variable XCHK_DUMP=FILE writes every far unordered pair 's v' (s < v; at most 200000) to
 *           FILE. With more than one thread the line ORDER depends on thread scheduling.
 * build:  cc -O3 -march=native -o xchk xchk.c -lpthread
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>

#define W 8
typedef uint64_t u64;
static int64_t N = 0, M = 0;
static int64_t *off, *adj;
static int Dmax;
static int64_t nbatch;
static atomic_long next_batch;
static atomic_long bad_pairs_total;
static atomic_long bad_sources_total;
static long ecc_hist_g[64];
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static atomic_long batches_done;
static FILE *dumpf = NULL;
static atomic_long dumped;

static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(2); }

static int cmp64(const void *a, const void *b) {
  int64_t x = *(const int64_t *)a, y = *(const int64_t *)b; return (x > y) - (x < y);
}

static void *worker(void *arg) {
  (void)arg;
  u64 *vis = malloc(sizeof(u64) * W * N), *fr = malloc(sizeof(u64) * W * N), *nx = malloc(sizeof(u64) * W * N);
  int64_t *act = malloc(sizeof(int64_t) * N), *act2 = malloc(sizeof(int64_t) * N);
  unsigned char *full = malloc(N), *inn = malloc(N);
  if (!vis || !fr || !nx || !act || !act2 || !full || !inn) die("oom");
  long ecc_hist[64]; memset(ecc_hist, 0, sizeof ecc_hist);
  for (;;) {
    long b = atomic_fetch_add(&next_batch, 1);
    if (b >= nbatch) break;
    int64_t s0 = b * 64 * W, s1 = s0 + 64 * W; if (s1 > N) s1 = N;
    u64 mask[W]; memset(mask, 0, sizeof mask);
    for (int64_t s = s0; s < s1; s++) mask[(s - s0) >> 6] |= (u64)1 << ((s - s0) & 63);
    memset(vis, 0, sizeof(u64) * W * N); memset(fr, 0, sizeof(u64) * W * N); memset(nx, 0, sizeof(u64) * W * N);
    memset(full, 0, N); memset(inn, 0, N);
    int64_t na = 0;
    for (int64_t s = s0; s < s1; s++) {
      int w = (s - s0) >> 6; u64 bit = (u64)1 << ((s - s0) & 63);
      vis[s * W + w] |= bit; fr[s * W + w] |= bit; act[na++] = s;
    }
    /* per-source completion level: done_level[k] = first level L with source k reaching all N */
    int nsrc = (int)(s1 - s0);
    /* count of vertices not yet full: track per-source reach counts would be expensive; instead after each level we
       compute, for the batch, the AND over all v of vis[v] -> bit set = source complete at this level. */
    int done_level[64 * W]; for (int k = 0; k < 64 * W; k++) done_level[k] = -1;
    {
      u64 andv[W]; for (int w = 0; w < W; w++) andv[w] = mask[w];
      for (int64_t v = 0; v < N; v++) for (int w = 0; w < W; w++) andv[w] &= vis[v * W + w];
      for (int k = 0; k < nsrc; k++) if ((andv[k >> 6] >> (k & 63)) & 1) done_level[k] = 0;
    }
    for (int L = 1; L <= Dmax; L++) {
      int64_t work = 0;
      for (int64_t i = 0; i < na; i++) work += off[act[i] + 1] - off[act[i]];
      int64_t na2 = 0;
      if (work < 2 * M / 16) {
        /* push */
        for (int64_t i = 0; i < na; i++) {
          int64_t u = act[i];
          u64 *fu = fr + u * W;
          for (int64_t j = off[u]; j < off[u + 1]; j++) {
            int64_t v = adj[j];
            if (full[v]) continue;
            u64 *xv = nx + v * W, *vv = vis + v * W; int any = 0;
            for (int w = 0; w < W; w++) { u64 t = fu[w] & ~vv[w]; xv[w] |= t; any |= (t != 0); }
            if (any && !inn[v]) { inn[v] = 1; act2[na2++] = v; }
          }
        }
        for (int64_t i = 0; i < na; i++) { int64_t u = act[i]; memset(fr + u * W, 0, sizeof(u64) * W); }
        for (int64_t i = 0; i < na2; i++) {
          int64_t v = act2[i]; inn[v] = 0;
          u64 *xv = nx + v * W, *vv = vis + v * W, *fv = fr + v * W; int f = 1;
          for (int w = 0; w < W; w++) { vv[w] |= xv[w]; fv[w] = xv[w]; xv[w] = 0; if ((vv[w] & mask[w]) != mask[w]) f = 0; }
          if (f) full[v] = 1;
        }
      } else {
        /* pull over all non-full vertices */
        for (int64_t v = 0; v < N; v++) {
          if (full[v]) continue;
          u64 acc[W]; memset(acc, 0, sizeof acc);
          for (int64_t j = off[v]; j < off[v + 1]; j++) { u64 *fu = fr + adj[j] * W; for (int w = 0; w < W; w++) acc[w] |= fu[w]; }
          u64 *xv = nx + v * W, *vv = vis + v * W; int any = 0;
          for (int w = 0; w < W; w++) { xv[w] = acc[w] & ~vv[w]; any |= (xv[w] != 0); }
          if (any) act2[na2++] = v;
        }
        for (int64_t i = 0; i < na; i++) { int64_t u = act[i]; memset(fr + u * W, 0, sizeof(u64) * W); }
        for (int64_t i = 0; i < na2; i++) {
          int64_t v = act2[i];
          u64 *xv = nx + v * W, *vv = vis + v * W, *fv = fr + v * W; int f = 1;
          for (int w = 0; w < W; w++) { vv[w] |= xv[w]; fv[w] = xv[w]; xv[w] = 0; if ((vv[w] & mask[w]) != mask[w]) f = 0; }
          if (f) full[v] = 1;
        }
      }
      int64_t *tmp = act; act = act2; act2 = tmp; na = na2;
      /* completion of sources at level L */
      u64 andv[W]; for (int w = 0; w < W; w++) andv[w] = mask[w];
      for (int64_t v = 0; v < N; v++) { if (full[v]) continue; for (int w = 0; w < W; w++) andv[w] &= vis[v * W + w]; }
      for (int k = 0; k < nsrc; k++) if (done_level[k] < 0 && ((andv[k >> 6] >> (k & 63)) & 1)) done_level[k] = L;
    }
    long bp = 0;
    for (int64_t v = 0; v < N; v++) {
      if (full[v]) continue;
      for (int w = 0; w < W; w++) {
        u64 miss = mask[w] & ~vis[v * W + w];
        bp += __builtin_popcountll(miss);
        if (dumpf && miss) {
          while (miss) {
            int bit = __builtin_ctzll(miss); miss &= miss - 1;
            int64_t s = s0 + w * 64 + bit;
            if (s < v && atomic_fetch_add(&dumped, 1) < 200000) {
              pthread_mutex_lock(&mu); fprintf(dumpf, "%lld %lld\n", (long long)s, (long long)v); pthread_mutex_unlock(&mu);
            }
          }
        }
      }
    }
    long bs = 0;
    for (int k = 0; k < nsrc; k++) { if (done_level[k] < 0) { bs++; ecc_hist[63]++; } else ecc_hist[done_level[k]]++; }
    atomic_fetch_add(&bad_pairs_total, bp); atomic_fetch_add(&bad_sources_total, bs);
    long d = atomic_fetch_add(&batches_done, 1) + 1;
    if (d % 200 == 0) { fprintf(stderr, "  batches %ld/%ld bad_pairs_so_far %ld\n", d, (long)nbatch, (long)atomic_load(&bad_pairs_total)); }
  }
  pthread_mutex_lock(&mu); for (int k = 0; k < 64; k++) ecc_hist_g[k] += ecc_hist[k]; pthread_mutex_unlock(&mu);
  free(vis); free(fr); free(nx); free(act); free(act2); free(full); free(inn);
  return NULL;
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: xchk GRAPH Delta D [threads]\n"); return 2; }
  int Delta = atoi(argv[2]); Dmax = atoi(argv[3]); int T = argc > 4 ? atoi(argv[4]) : 8;
  if (Dmax < 1 || Dmax > 60) die("bad D");
  FILE *f = fopen(argv[1], "r"); if (!f) die("open");
  int64_t cap = 1 << 20, ne = 0; int64_t *E = malloc(sizeof(int64_t) * 2 * cap);
  char line[4096]; int64_t maxid = -1; long loops = 0;
  while (fgets(line, sizeof line, f)) {
    char *p = line; while (*p == ' ' || *p == '\t') p++;
    if (*p == '#' || *p == '\n' || *p == 0) continue;
    char *e1; long long a = strtoll(p, &e1, 10); if (e1 == p) die("parse");
    char *e2; long long bb = strtoll(e1, &e2, 10); if (e2 == e1) die("parse2");
    if (a < 0 || bb < 0) die("negative id");
    if (ne == cap) { cap *= 2; E = realloc(E, sizeof(int64_t) * 2 * cap); if (!E) die("oom"); }
    E[2 * ne] = a; E[2 * ne + 1] = bb; ne++;
    if (a == bb) loops++;
    if (a > maxid) maxid = a; if (bb > maxid) maxid = bb;
  }
  fclose(f);
  N = maxid + 1; M = ne;
  int64_t *deg = calloc(N, sizeof(int64_t));
  for (int64_t i = 0; i < ne; i++) { if (E[2*i] != E[2*i+1]) { deg[E[2 * i]]++; deg[E[2 * i + 1]]++; } }
  off = malloc(sizeof(int64_t) * (N + 1)); off[0] = 0;
  for (int64_t v = 0; v < N; v++) off[v + 1] = off[v] + deg[v];
  adj = malloc(sizeof(int64_t) * off[N]);
  int64_t *pos = malloc(sizeof(int64_t) * N); memcpy(pos, off, sizeof(int64_t) * N);
  for (int64_t i = 0; i < ne; i++) { int64_t a = E[2 * i], bb = E[2 * i + 1]; if (a == bb) continue; adj[pos[a]++] = bb; adj[pos[bb]++] = a; }
  free(E); free(pos);
  long dups = 0, gaps = 0; int64_t maxdeg = 0; long hist[256]; memset(hist, 0, sizeof hist);
  for (int64_t v = 0; v < N; v++) {
    qsort(adj + off[v], off[v + 1] - off[v], sizeof(int64_t), cmp64);
    for (int64_t j = off[v] + 1; j < off[v + 1]; j++) if (adj[j] == adj[j - 1]) dups++;
    int64_t d = off[v + 1] - off[v]; if (d == 0) gaps++; if (d > maxdeg) maxdeg = d; if (d < 256) hist[d]++;
  }
  dups /= 2;
  fprintf(stderr, "parsed N=%lld M=%lld maxdeg=%lld loops=%ld dups=%ld gaps=%ld\n", (long long)N, (long long)M, (long long)maxdeg, loops, dups, gaps);
  nbatch = (N + 64 * W - 1) / (64 * W);
  if (getenv("XCHK_DUMP")) { dumpf = fopen(getenv("XCHK_DUMP"), "w"); if (!dumpf) die("dump open"); }
  atomic_store(&next_batch, 0); atomic_store(&bad_pairs_total, 0); atomic_store(&bad_sources_total, 0);
  struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
  pthread_t th[64]; if (T > 64) T = 64;
  for (int i = 0; i < T; i++) pthread_create(&th[i], NULL, worker, NULL);
  for (int i = 0; i < T; i++) pthread_join(th[i], NULL);
  clock_gettime(CLOCK_MONOTONIC, &t1);
  if (dumpf) fclose(dumpf);
  double secs = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
  long bp = atomic_load(&bad_pairs_total), bs = atomic_load(&bad_sources_total);
  int ok = (loops == 0 && dups == 0 && gaps == 0 && maxdeg <= Delta && bp == 0 && bs == 0);
  printf("RESULT N=%lld M=%lld maxdeg=%lld Delta=%d D=%d loops=%ld dups=%ld gaps=%ld bad_pairs=%ld bad_sources=%ld",
         (long long)N, (long long)M, (long long)maxdeg, Delta, Dmax, loops, dups, gaps, bp, bs);
  printf(" deghist={"); int first = 1; for (int d = 0; d < 256; d++) if (hist[d]) { printf("%s%d:%ld", first ? "" : ",", d, hist[d]); first = 0; } printf("}");
  printf(" ecchist={"); first = 1; for (int k = 0; k < 63; k++) if (ecc_hist_g[k]) { printf("%s%d:%ld", first ? "" : ",", k, ecc_hist_g[k]); first = 0; }
  if (ecc_hist_g[63]) printf("%s>%d:%ld", first ? "" : ",", Dmax, ecc_hist_g[63]);
  printf("} secs=%.1f %s\n", secs, ok ? "VALID" : "INVALID");
  return ok ? 0 : 1;
}
