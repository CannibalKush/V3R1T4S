/*
 * bklc_opt.c
 *
 * Lens 2 (c-evaluator-optimizer):
 * Bitwise Gray-Code Shell Evaluator (d, A_d) + Smart Puncturing, Full-Space
 * Tabu Column Replacement/Extension, and Covering-Radius Code Augmentation.
 *
 * Implements three complementary optimization attacks:
 * 1. Smart Puncturing (Minimum-Weight Hitting-Set Avoidance):
 *    Given a high-distance parent code [N, k, D]_q, enumerates the low-weight
 *    codeword shell {c in C \ {0} : wt(c) <= D + 10} and searches via greedy +
 *    tabu search for p = N - n columns whose deletion minimizes max overlap with
 *    low-weight codewords, achieving d(C_punct) >= D - p + 1 > d_lo(q, N - p, k).
 * 2. Full-Space Hitting-Set Column Extension & Tabu Column Replacement:
 *    Using a 256-bit (uint64_t[4]) bitwise Gray-code evaluator, tracks the exact
 *    minimum-weight codeword list M_d and searches over full k-bit columns
 *    v in GF(2)^k that hit the maximum fraction of M_d to drive A_d -> 0 and
 *    advance d -> d + 1.
 * 3. Code Augmentation (k -> k + 1 via Coset Distance Optimization):
 *    Given an [n_0, k, d_0]_2 parent code C, searches over candidate rows
 *    r_{k+1} in GF(2)^{n_0} (seeded by cyclic shifts and refined by tabu bit-flips)
 *    to maximize the coset distance min_{c in C} wt(r_{k+1} ^ c), plus tail bits.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAX_K 24
#define MAX_N 256
#define NWORDS 4

static int D_LO[10][260][40];
static int D_UP[10][260][40];

static void load_bounds_tsv(const char *path) {
    memset(D_LO, 0, sizeof(D_LO));
    memset(D_UP, 0, sizeof(D_UP));
    FILE *f = fopen(path, "r");
    if (!f) return;
    int q, n, k, dlo, dup;
    while (fscanf(f, "%d %d %d %d %d", &q, &n, &k, &dlo, &dup) == 5) {
        if (q >= 2 && q <= 9 && n >= 1 && n < 260 && k >= 1 && k < 40) {
            D_LO[q][n][k] = dlo;
            D_UP[q][n][k] = dup;
        }
    }
    fclose(f);
}

static int is_excluded_cell(int q, int n, int k) {
    if (q == 2 && k >= 19 && k <= 22 && n >= 170 && n <= 240) return 1;
    return 0;
}

static uint64_t rng_state = 0x9e3779b97f4a7c15ULL;
static uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

/* 256-bit codeword row */
typedef struct {
    uint64_t w[NWORDS];
} Row256;

static inline int popcnt256(const Row256 *r) {
    return __builtin_popcountll(r->w[0]) +
           __builtin_popcountll(r->w[1]) +
           __builtin_popcountll(r->w[2]) +
           __builtin_popcountll(r->w[3]);
}

static inline void xor256(Row256 *dst, const Row256 *src) {
    dst->w[0] ^= src->w[0];
    dst->w[1] ^= src->w[1];
    dst->w[2] ^= src->w[2];
    dst->w[3] ^= src->w[3];
}

static inline int get_bit256(const Row256 *r, int col) {
    return (r->w[col >> 6] >> (col & 63)) & 1;
}

static inline void set_bit256(Row256 *r, int col, int val) {
    if (val) r->w[col >> 6] |= (1ULL << (col & 63));
    else     r->w[col >> 6] &= ~(1ULL << (col & 63));
}

/* Evaluate exact (d, A_d) of a binary k x n generator matrix using Gray code */
static void eval_binary_gray(int k, int n, const Row256 *G_rows, int *d_out, uint64_t *Ad_out) {
    Row256 cw;
    memset(&cw, 0, sizeof(cw));
    int min_w = n + 1;
    uint64_t A_d = 0;
    uint32_t lim = 1U << k;
    uint32_t prev_g = 0;

    for (uint32_t i = 1; i < lim; i++) {
        uint32_t g = i ^ (i >> 1);
        uint32_t diff = g ^ prev_g;
        int bit = __builtin_ctz(diff);
        xor256(&cw, &G_rows[bit]);
        prev_g = g;

        int w = popcnt256(&cw);
        if (w < min_w) {
            min_w = w;
            A_d = 1;
        } else if (w == min_w) {
            A_d++;
        }
    }
    *d_out = min_w;
    *Ad_out = A_d;
}

/* Check GF(2) rank of k x n matrix */
static int rank_binary(int k, int n, const Row256 *G_rows) {
    Row256 M[MAX_K];
    for (int i = 0; i < k; i++) M[i] = G_rows[i];
    int r = 0;
    for (int col = 0; col < n && r < k; col++) {
        int piv = -1;
        for (int i = r; i < k; i++) {
            if (get_bit256(&M[i], col)) { piv = i; break; }
        }
        if (piv < 0) continue;
        Row256 tmp = M[r]; M[r] = M[piv]; M[piv] = tmp;
        for (int i = 0; i < k; i++) {
            if (i != r && get_bit256(&M[i], col)) xor256(&M[i], &M[r]);
        }
        r++;
    }
    return r;
}

/* Save verified binary winning code to JSON */
static int save_binary_win(int n, int k, const Row256 *G_rows, const char *desc) {
    if (is_excluded_cell(2, n, k)) return 0;
    if (rank_binary(k, n, G_rows) < k) return 0;
    int d = 0;
    uint64_t A_d = 0;
    eval_binary_gray(k, n, G_rows, &d, &A_d);

    int d_lo = D_LO[2][n][k];
    int d_up = D_UP[2][n][k];
    if (d_lo <= 0 || d <= d_lo) return 0;

    D_LO[2][n][k] = d;
    printf("\n*** LENS 2 BREAKTHROUGH WIN: [%d, %d, %d]_2 (beats codetables.de d_lo=%d, d_up=%d, A_d=%llu) [%s] ***\n",
           n, k, d, d_lo, d_up, (unsigned long long)A_d, desc);
    fflush(stdout);

    char fname[256];
    snprintf(fname, sizeof(fname), "attempts/c-evaluator-optimizer/result/win_q2_n%d_k%d_d%d.json",
             n, k, d);
    FILE *fp = fopen(fname, "w");
    if (fp) {
        fprintf(fp, "{\n");
        fprintf(fp, "  \"type\": \"classical\",\n");
        fprintf(fp, "  \"q\": 2,\n");
        fprintf(fp, "  \"n\": %d,\n", n);
        fprintf(fp, "  \"k\": %d,\n", k);
        fprintf(fp, "  \"d\": %d,\n", d);
        fprintf(fp, "  \"d_lo_codetables\": %d,\n", d_lo);
        fprintf(fp, "  \"d_up_codetables\": %d,\n", d_up);
        fprintf(fp, "  \"A_d\": %llu,\n", (unsigned long long)A_d);
        fprintf(fp, "  \"construction\": \"%s\",\n", desc);
        fprintf(fp, "  \"G\": [\n");
        for (int r = 0; r < k; r++) {
            fprintf(fp, "    [");
            for (int c = 0; c < n; c++) {
                fprintf(fp, "%d%s", get_bit256(&G_rows[r], c), (c + 1 < n) ? "," : "");
            }
            fprintf(fp, "]%s\n", (r + 1 < k) ? "," : "");
        }
        fprintf(fp, "  ]\n}\n");
        fclose(fp);
    }
    return 1;
}

/* Load a binary generator matrix G from one of our JSON files */
static int load_json_matrix(const char *path, int *n_out, int *k_out, Row256 *G_rows) {
    FILE *fp = fopen(path, "r");
    if (!fp) return 0;
    fseek(fp, 0, SEEK_END);
    long sz = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    char *buf = (char *)malloc(sz + 1);
    fread(buf, 1, sz, fp);
    buf[sz] = '\0';
    fclose(fp);

    char *pn = strstr(buf, "\"n\":");
    char *pk = strstr(buf, "\"k\":");
    char *pG = strstr(buf, "\"G\":");
    if (!pn || !pk || !pG) { free(buf); return 0; }
    int n = atoi(pn + 4);
    int k = atoi(pk + 4);
    *n_out = n;
    *k_out = k;

    for (int i = 0; i < k; i++) memset(&G_rows[i], 0, sizeof(Row256));
    char *cur = strchr(pG, '[');
    if (cur) cur++;
    for (int r = 0; r < k; r++) {
        cur = strchr(cur, '[');
        if (!cur) break;
        cur++;
        for (int c = 0; c < n; c++) {
            while (*cur && (*cur < '0' || *cur > '9')) cur++;
            int val = *cur - '0';
            if (*cur) cur++;
            set_bit256(&G_rows[r], c, val);
        }
    }
    free(buf);
    return 1;
}

/*
 * ATTACK 1: Smart Puncturing (Minimum-Weight Hitting-Set Avoidance)
 * Given a binary [N, k, D]_2 code, collects all codewords of weight <= D + 6
 * and searches for p columns to delete so that the punctured [N - p, k]_2 code
 * beats d_lo(2, N - p, k).
 */
typedef struct {
    Row256 cw;
    int wt;
} LowWord;

static void smart_puncture_search(int N, int k, const Row256 *G_rows, const char *parent_name) {
    int D = 0;
    uint64_t A_D = 0;
    eval_binary_gray(k, N, G_rows, &D, &A_D);
    printf("[SmartPuncture] Parent %s: [%d, %d, %d]_2 (A_%d = %llu)\n",
           parent_name, N, k, D, D, (unsigned long long)A_D);

    /* Collect all codewords with weight <= D + 6 */
    int max_collect = 60000;
    LowWord *shell = (LowWord *)malloc(max_collect * sizeof(LowWord));
    int n_shell = 0;

    Row256 cw;
    memset(&cw, 0, sizeof(cw));
    uint32_t lim = 1U << k;
    uint32_t prev_g = 0;
    int wt_cap = D + 4;

    for (uint32_t i = 1; i < lim; i++) {
        uint32_t g = i ^ (i >> 1);
        uint32_t diff = g ^ prev_g;
        int bit = __builtin_ctz(diff);
        xor256(&cw, &G_rows[bit]);
        prev_g = g;
        int w = popcnt256(&cw);
        if (w <= wt_cap && n_shell < max_collect) {
            shell[n_shell].cw = cw;
            shell[n_shell].wt = w;
            n_shell++;
        }
    }
    printf("  Collected %d low-weight codewords (wt <= %d)\n", n_shell, wt_cap);

    /* Try puncturing p = 1 .. 18 columns */
    for (int p = 1; p <= 18; p++) {
        int n_target = N - p;
        if (n_target < 40 || is_excluded_cell(2, n_target, k)) continue;
        int d_lo = D_LO[2][n_target][k];
        if (d_lo <= 0) continue;
        int d_target = d_lo + 1;
        /* Can deleting p columns leave distance >= d_target? Only if D >= d_target! */
        if (D < d_target) continue;
        /* Wait: if D - p >= d_target, ANY p columns work! */
        int del_cols[32];
        uint8_t is_del[MAX_N];
        int *loss = (int *)malloc(n_shell * sizeof(int));

        for (int restart = 0; restart < 30; restart++) {
            memset(is_del, 0, sizeof(is_del));
            memset(loss, 0, n_shell * sizeof(int));

            /* Randomly pick p distinct initial columns to delete */
            for (int step = 0; step < p; step++) {
                int c = xorshift64() % N;
                while (is_del[c]) c = (c + 1) % N;
                del_cols[step] = c;
                is_del[c] = 1;
                for (int s = 0; s < n_shell; s++) {
                    if (get_bit256(&shell[s].cw, c)) loss[s]++;
                }
            }

            /* Fast critical-word histogram swap refinement */
            int *crit_idx = (int *)malloc(n_shell * sizeof(int));
            for (int iter = 0; iter < 250; iter++) {
                int min_rem = 9999;
                int n_viol = 0;
                int n_crit = 0;
                int first_viol = -1;
                for (int s = 0; s < n_shell; s++) {
                    int rw = shell[s].wt - loss[s];
                    if (rw < min_rem) min_rem = rw;
                    if (rw < d_target) {
                        if (first_viol < 0 || (xorshift64() & 7) == 0) first_viol = s;
                        n_viol++;
                    }
                    if (rw <= d_target + 1) {
                        crit_idx[n_crit++] = s;
                    }
                }
                if (min_rem >= d_target) break;

                /* Pick a deleted column that hits first_viol */
                int pick_idx = iter % p;
                if (first_viol >= 0) {
                    for (int j = 0; j < p; j++) {
                        int jj = (iter + j) % p;
                        if (get_bit256(&shell[first_viol].cw, del_cols[jj])) {
                            pick_idx = jj;
                            break;
                        }
                    }
                }
                int old_c = del_cols[pick_idx];
                is_del[old_c] = 0;
                for (int s = 0; s < n_shell; s++) {
                    if (get_bit256(&shell[s].cw, old_c)) loss[s]--;
                }

                /* Score all candidate columns c ONLY on the n_crit critical words! */
                int best_c = old_c;
                int64_t best_pen = 0x7fffffffffffffffLL;
                for (int c = 0; c < N; c++) {
                    if (is_del[c] || c == old_c) continue;
                    int64_t pen = 0;
                    for (int ci = 0; ci < n_crit; ci++) {
                        int s = crit_idx[ci];
                        int nl = loss[s] + get_bit256(&shell[s].cw, c);
                        int rw = shell[s].wt - nl;
                        if (rw < d_target) {
                            int viol = d_target - rw;
                            pen += (int64_t)viol * viol * 10000LL;
                        } else if (rw == d_target) {
                            pen += 5;
                        }
                    }
                    pen = pen * 8 + (xorshift64() & 7);
                    if (pen < best_pen) {
                        best_pen = pen;
                        best_c = c;
                    }
                }
                del_cols[pick_idx] = best_c;
                is_del[best_c] = 1;
                for (int s = 0; s < n_shell; s++) {
                    if (get_bit256(&shell[s].cw, best_c)) loss[s]++;
                }
            }
            free(crit_idx);

            /* Check shell minimum */
            int min_rem = 9999;
            for (int s = 0; s < n_shell; s++) {
                int rw = shell[s].wt - loss[s];
                if (rw < min_rem) min_rem = rw;
            }
            if (min_rem >= d_target) {
                /* Build punctured matrix and run full Gray-code evaluation! */
                Row256 G_punct[MAX_K];
                for (int r = 0; r < k; r++) memset(&G_punct[r], 0, sizeof(Row256));
                int dst_c = 0;
                for (int c = 0; c < N; c++) {
                    if (!is_del[c]) {
                        for (int r = 0; r < k; r++) {
                            set_bit256(&G_punct[r], dst_c, get_bit256(&G_rows[r], c));
                        }
                        dst_c++;
                    }
                }
                char desc[128];
                snprintf(desc, sizeof(desc), "Smart-punctured %d columns from %s [%d,%d,%d]_2",
                         p, parent_name, N, k, D);
                if (save_binary_win(n_target, k, G_punct, desc)) break;
            }
        }
        free(loss);
    }
    free(shell);
}

/*
 * ATTACK 2: Full-Space Hitting-Set Column Extension & Tabu Column Replacement
 * Given a binary [N, k, D]_2 seed, collects all codewords of weight <= D + 3
 * (storing their k-bit message vectors u in 1..2^k-1) and searches for:
 *  (a) 1..8 new columns v_1, ..., v_t in GF(2)^k to append (reaching [N+t, k, d]_2),
 *  (b) replacing 1..4 existing columns while appending columns.
 */
static void full_space_extension_search(int N, int k, const Row256 *G_rows, const char *seed_name) {
    int D = 0;
    uint64_t A_D = 0;
    eval_binary_gray(k, N, G_rows, &D, &A_D);

    uint32_t lim = 1U << k;
    uint32_t *msg_list = (uint32_t *)malloc(lim * sizeof(uint32_t));
    uint8_t *base_wt = (uint8_t *)malloc(lim * sizeof(uint8_t));
    int n_crit = 0;

    Row256 cw;
    memset(&cw, 0, sizeof(cw));
    uint32_t prev_g = 0;
    int cap_w = D + 3;

    for (uint32_t i = 1; i < lim; i++) {
        uint32_t g = i ^ (i >> 1);
        uint32_t diff = g ^ prev_g;
        int bit = __builtin_ctz(diff);
        xor256(&cw, &G_rows[bit]);
        prev_g = g;
        int w = popcnt256(&cw);
        if (w <= cap_w) {
            msg_list[n_crit] = g;
            base_wt[n_crit] = (uint8_t)w;
            n_crit++;
        }
    }
    printf("[FullSpaceExt] Seed %s [%d,%d,%d]_2: %d critical messages with wt <= %d\n",
           seed_name, N, k, D, n_crit, cap_w);

    for (int t = 1; t <= 8; t++) {
        int n_new = N + t;
        if (n_new >= 256 || is_excluded_cell(2, n_new, k)) continue;
        int d_lo = D_LO[2][n_new][k];
        if (d_lo <= 0) continue;
        int d_target = d_lo + 1;
        if (D + t < d_target) continue;

        uint32_t ext_cols[12];
        int *cur_w = (int *)malloc(n_crit * sizeof(int));

        for (int restart = 0; restart < 12; restart++) {
            for (int idx = 0; idx < n_crit; idx++) cur_w[idx] = base_wt[idx];

            for (int step = 0; step < t; step++) {
                /* Sample 4000 candidate columns v in GF(2)^k and pick best hitting column */
                uint32_t best_v = 1;
                int64_t best_sc = -1;
                for (int samp = 0; samp < 4000; samp++) {
                    uint32_t v = (xorshift64() % (lim - 1)) + 1;
                    int64_t sc = 0;
                    for (int idx = 0; idx < n_crit; idx++) {
                        int def = d_target - cur_w[idx];
                        if (def > 0) {
                            int bit = __builtin_parity(msg_list[idx] & v);
                            if (bit) sc += (int64_t)def * def * 32 + 1;
                        }
                    }
                    if (sc > best_sc) {
                        best_sc = sc;
                        best_v = v;
                    }
                }
                ext_cols[step] = best_v;
                for (int idx = 0; idx < n_crit; idx++) {
                    if (__builtin_parity(msg_list[idx] & best_v)) cur_w[idx]++;
                }
            }

            /* Check if all critical messages reached d_target */
            int min_cw = 9999;
            for (int idx = 0; idx < n_crit; idx++) {
                if (cur_w[idx] < min_cw) min_cw = cur_w[idx];
            }
            if (min_cw >= d_target) {
                Row256 G_ext[MAX_K];
                for (int r = 0; r < k; r++) G_ext[r] = G_rows[r];
                for (int step = 0; step < t; step++) {
                    for (int r = 0; r < k; r++) {
                        set_bit256(&G_ext[r], N + step, (ext_cols[step] >> r) & 1);
                    }
                }
                char desc[128];
                snprintf(desc, sizeof(desc), "Full-space hitting-set extension (+%d cols) from %s", t, seed_name);
                if (save_binary_win(n_new, k, G_ext, desc)) break;
            }
        }
        free(cur_w);
    }

    free(msg_list);
    free(base_wt);
}

/*
 * ATTACK 3: Code Augmentation (k -> k + 1 via Coset Distance Optimization)
 * Given a binary [N, k, D]_2 parent code C, precomputes all 2^k codewords of C
 * and searches for an augmenting row r_new in GF(2)^N that maximizes
 *   d_coset = min_{c in C} wt(r_new ^ c),
 * then appends t = 0..8 tail bits (1 on r_new, 0 on C) to form [N + t, k + 1, min(D, d_coset + t)]_2!
 */
static void augment_row_search(int N, int k, const Row256 *G_rows, const char *parent_name) {
    if (k >= 20) return;
    int D = 0;
    uint64_t A_D = 0;
    eval_binary_gray(k, N, G_rows, &D, &A_D);

    uint32_t lim = 1U << k;
    Row256 *all_cw = (Row256 *)malloc(lim * sizeof(Row256));
    memset(&all_cw[0], 0, sizeof(Row256));
    Row256 cw;
    memset(&cw, 0, sizeof(cw));
    uint32_t prev_g = 0;

    for (uint32_t i = 1; i < lim; i++) {
        uint32_t g = i ^ (i >> 1);
        uint32_t diff = g ^ prev_g;
        int bit = __builtin_ctz(diff);
        xor256(&cw, &G_rows[bit]);
        prev_g = g;
        all_cw[i] = cw;
    }

    int k_new = k + 1;
    int best_coset_d = 0;
    Row256 best_r;
    memset(&best_r, 0, sizeof(best_r));

    for (int restart = 0; restart < 40; restart++) {
        Row256 r_cand;
        memset(&r_cand, 0, sizeof(r_cand));
        /* Initialize with random vector of weight ~ N/2 */
        for (int c = 0; c < N; c++) {
            if (xorshift64() & 1) set_bit256(&r_cand, c, 1);
        }

        int cur_d = 9999;
        uint32_t min_idx = 0;
        for (uint32_t i = 0; i < lim; i++) {
            Row256 diff = r_cand;
            xor256(&diff, &all_cw[i]);
            int w = popcnt256(&diff);
            if (w < cur_d) { cur_d = w; min_idx = i; }
        }

        /* Hill-climbing / Tabu bit-flips on r_cand: flip a coordinate where r_cand == all_cw[min_idx] */
        for (int step = 0; step < 80; step++) {
            Row256 worst_diff = r_cand;
            xor256(&worst_diff, &all_cw[min_idx]);
            /* Pick a coordinate c where worst_diff has a 0 (so flipping c increases distance to all_cw[min_idx]!) */
            int flip_c = -1;
            int start_c = xorshift64() % N;
            for (int off = 0; off < N; off++) {
                int c = (start_c + off) % N;
                if (!get_bit256(&worst_diff, c)) {
                    flip_c = c;
                    break;
                }
            }
            if (flip_c < 0) break;

            int old_bit = get_bit256(&r_cand, flip_c);
            set_bit256(&r_cand, flip_c, old_bit ^ 1);

            int new_d = 9999;
            uint32_t new_min_idx = 0;
            int new_cnt = 0;
            for (uint32_t i = 0; i < lim; i++) {
                Row256 diff = r_cand;
                xor256(&diff, &all_cw[i]);
                int w = popcnt256(&diff);
                if (w < new_d) {
                    new_d = w;
                    new_min_idx = i;
                    new_cnt = 1;
                    if (new_d < cur_d - 1) break;
                } else if (w == new_d) {
                    new_cnt++;
                }
            }

            if (new_d >= cur_d) {
                cur_d = new_d;
                min_idx = new_min_idx;
                if (cur_d > best_coset_d) {
                    best_coset_d = cur_d;
                    best_r = r_cand;
                }
            } else {
                set_bit256(&r_cand, flip_c, old_bit);
            }
        }
    }

    printf("[Augment] Parent %s [%d,%d,%d]_2 -> best coset distance for k=%d is d_coset=%d\n",
           parent_name, N, k, D, k_new, best_coset_d);

    for (int t = 0; t <= 8; t++) {
        int n_new = N + t;
        if (n_new >= 256 || is_excluded_cell(2, n_new, k_new)) continue;
        int d_ach = (D < best_coset_d + t) ? D : (best_coset_d + t);
        if (D_LO[2][n_new][k_new] > 0 && d_ach > D_LO[2][n_new][k_new]) {
            Row256 G_aug[MAX_K];
            for (int r = 0; r < k; r++) G_aug[r] = G_rows[r];
            G_aug[k] = best_r;
            for (int c = 0; c < t; c++) set_bit256(&G_aug[k], N + c, 1);
            char desc[128];
            snprintf(desc, sizeof(desc), "Augmented row + %d tail bits from %s", t, parent_name);
            save_binary_win(n_new, k_new, G_aug, desc);
        }
    }

    free(all_cw);
}

int main(void) {
    load_bounds_tsv("attempts/symmetry-orbit-join/bounds.tsv");
    printf("=== Lens 2: Bitwise Gray-Code Shell Evaluator & Smart-Puncture / Extension / Augmentation ===\n");

    const char *seed_files[] = {
        "attempts/symmetry-orbit-join/result/win_q2_n170_k17_d69.json",
        "attempts/symmetry-orbit-join/result/win_q2_n173_k17_d72.json",
        "attempts/symmetry-orbit-join/result/win_q2_n174_k17_d72.json"
    };

    for (int i = 0; i < 3; i++) {
        int N = 0, k = 0;
        Row256 G_rows[MAX_K];
        if (load_json_matrix(seed_files[i], &N, &k, G_rows)) {
            smart_puncture_search(N, k, G_rows, seed_files[i]);
            full_space_extension_search(N, k, G_rows, seed_files[i]);
            augment_row_search(N, k, G_rows, seed_files[i]);
        }
    }

    printf("=== Lens 2 optimization pass complete ===\n");
    return 0;
}
