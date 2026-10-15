/*
 * maxdet_search.c
 * High-speed C optimizer for Hadamard excess maximization via Iterated Local Search
 * (greedy 1-flip + 2-flip polish + multi-radius Basin Hopping kicks) and bordered
 * Sherman-Morrison rank-1/rank-2 determinant local search.
 *
 * Compile: clang -O3 -march=native maxdet_search.c -o maxdet_search -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#define MAX_M 128

static uint64_t rng_state = 0x853c49e6748fea9bULL;

static inline uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

static int is_prime(int p) {
    if (p < 2) return 0;
    if (p % 2 == 0) return p == 2;
    for (int d = 3; d * d <= p; d += 2) {
        if (p % d == 0) return 0;
    }
    return 1;
}

/* Build Paley Class I Hadamard matrix of order m = p + 1 where p == 3 (mod 4) is prime */
static int build_paley1(int m, int H[MAX_M][MAX_M]) {
    int p = m - 1;
    if (p % 4 != 3 || !is_prime(p)) return 0;
    int *qr = (int *)calloc(p, sizeof(int));
    for (int x = 1; x < p; x++) {
        qr[(x * x) % p] = 1;
    }
    for (int j = 0; j < m; j++) {
        H[0][j] = 1;
        H[j][0] = 1;
    }
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < m; j++) {
            if (i == j) {
                H[i][j] = -1;
            } else {
                int diff = (j - i + p) % p;
                H[i][j] = qr[diff] ? 1 : -1;
            }
        }
    }
    free(qr);
    return 1;
}

/* Verify H * H^T == m * I_m */
static int verify_hadamard(int m, int H[MAX_M][MAX_M]) {
    for (int i = 0; i < m; i++) {
        for (int j = i; j < m; j++) {
            int dot = 0;
            for (int k = 0; k < m; k++) {
                dot += H[i][k] * H[j][k];
            }
            if (i == j && dot != m) return 0;
            if (i != j && dot != 0) return 0;
        }
    }
    return 1;
}

/* Load an m x m {-1, +1} Hadamard matrix from file */
static int load_hadamard(const char *path, int *m_out, int H[MAX_M][MAX_M]) {
    FILE *f = fopen(path, "r");
    if (!f) return 0;
    int vals[MAX_M * MAX_M];
    int count = 0;
    int v;
    while (count < MAX_M * MAX_M && fscanf(f, "%d", &v) == 1) {
        if (v != 1 && v != -1) {
            fclose(f);
            return 0;
        }
        vals[count++] = v;
    }
    fclose(f);
    int m = (int)round(sqrt((double)count));
    if (m * m != count || m <= 0 || m > MAX_M) return 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            H[i][j] = vals[i * m + j];
        }
    }
    *m_out = m;
    return verify_hadamard(m, H);
}

/* Full 1-flip + 2-flip steepest ascent polish on column signs c[0..m-1] */
static int polish_1_2_flip(int m, int H[MAX_M][MAX_M], int c[MAX_M], int r[MAX_M]) {
    int cur_E = 0;
    for (int i = 0; i < m; i++) {
        int s = 0;
        for (int j = 0; j < m; j++) s += H[i][j] * c[j];
        r[i] = s;
        cur_E += abs(s);
    }

    int improved = 1;
    while (improved) {
        improved = 0;
        /* 1-flip steepest ascent */
        while (1) {
            int best_j = -1;
            int best_E = cur_E;
            for (int j = 0; j < m; j++) {
                int c2 = 2 * c[j];
                int nE = 0;
                for (int i = 0; i < m; i++) {
                    nE += abs(r[i] - c2 * H[i][j]);
                }
                if (nE > best_E) {
                    best_E = nE;
                    best_j = j;
                }
            }
            if (best_j >= 0) {
                int c2 = 2 * c[best_j];
                for (int i = 0; i < m; i++) r[i] -= c2 * H[i][best_j];
                c[best_j] = -c[best_j];
                cur_E = best_E;
                improved = 1;
            } else {
                break;
            }
        }
        /* 2-flip first-improvement escape */
        int found_2 = 0;
        for (int j1 = 0; j1 < m && !found_2; j1++) {
            int c2_1 = 2 * c[j1];
            for (int j2 = j1 + 1; j2 < m; j2++) {
                int c2_2 = 2 * c[j2];
                int nE = 0;
                for (int i = 0; i < m; i++) {
                    nE += abs(r[i] - c2_1 * H[i][j1] - c2_2 * H[i][j2]);
                }
                if (nE > cur_E) {
                    for (int i = 0; i < m; i++) {
                        r[i] -= c2_1 * H[i][j1] + c2_2 * H[i][j2];
                    }
                    c[j1] = -c[j1];
                    c[j2] = -c[j2];
                    cur_E = nE;
                    found_2 = 1;
                    improved = 1;
                    break;
                }
            }
        }
    }
    return cur_E;
}

/*
 * Optimize E(c) = sum_{i=0}^{m-1} | (H c)_i | over c in {-1, +1}^m
 * using multi-start random initialization + Iterated Local Search (Basin Hopping) kicks.
 */
static int optimize_excess(int m, int H[MAX_M][MAX_M], int num_restarts, int kicks_per_restart,
                           int best_u[MAX_M], int best_c[MAX_M]) {
    int global_best_E = -1;
    int c[MAX_M], r[MAX_M], local_best_c[MAX_M];

    for (int restart = 0; restart < num_restarts; restart++) {
        for (int j = 0; j < m; j++) {
            c[j] = (xorshift64() & 1) ? 1 : -1;
        }
        int local_best_E = polish_1_2_flip(m, H, c, r);
        for (int j = 0; j < m; j++) local_best_c[j] = c[j];

        if (local_best_E > global_best_E) {
            global_best_E = local_best_E;
            for (int j = 0; j < m; j++) best_c[j] = c[j];
            for (int i = 0; i < m; i++) best_u[i] = (r[i] >= 0) ? 1 : -1;
        }

        /* Iterated Local Search: kick 3..6 random columns from local_best_c and re-polish */
        for (int kstep = 0; kstep < kicks_per_restart; kstep++) {
            for (int j = 0; j < m; j++) c[j] = local_best_c[j];
            int num_kicks = 3 + (int)(xorshift64() % 4ULL);
            for (int q = 0; q < num_kicks; q++) {
                int idx = (int)(xorshift64() % (uint64_t)m);
                c[idx] = -c[idx];
            }
            int cand_E = polish_1_2_flip(m, H, c, r);
            if (cand_E >= local_best_E) {
                local_best_E = cand_E;
                for (int j = 0; j < m; j++) local_best_c[j] = c[j];
                if (cand_E > global_best_E) {
                    global_best_E = cand_E;
                    for (int j = 0; j < m; j++) best_c[j] = c[j];
                    for (int i = 0; i < m; i++) best_u[i] = (r[i] >= 0) ? 1 : -1;
                }
            }
        }
    }
    return global_best_E;
}

/*
 * Check rank-1 and rank-2 Sherman-Morrison interior/border flips on the n x n bordered matrix R.
 */
static int sherman_morrison_polish(int n, int R[MAX_M][MAX_M], double *log_gain_out) {
    double B[MAX_M][MAX_M];
    double A[MAX_M][2 * MAX_M];

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            A[i][j] = (double)R[i][j];
            A[i][n + j] = (i == j) ? 1.0 : 0.0;
        }
    }
    for (int k = 0; k < n; k++) {
        int piv = k;
        double max_v = fabs(A[k][k]);
        for (int i = k + 1; i < n; i++) {
            if (fabs(A[i][k]) > max_v) {
                max_v = fabs(A[i][k]);
                piv = i;
            }
        }
        if (piv != k) {
            for (int j = 0; j < 2 * n; j++) {
                double tmp = A[k][j];
                A[k][j] = A[piv][j];
                A[piv][j] = tmp;
            }
        }
        double inv_p = 1.0 / A[k][k];
        for (int j = 0; j < 2 * n; j++) A[k][j] *= inv_p;
        for (int i = 0; i < n; i++) {
            if (i != k) {
                double f = A[i][k];
                for (int j = 0; j < 2 * n; j++) A[i][j] -= f * A[k][j];
            }
        }
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            B[i][j] = A[i][n + j];
        }
    }

    int total_flips = 0;
    double total_log_gain = 0.0;
    while (1) {
        double best_mult = 1.0 + 1e-11;
        int best_i = -1, best_j = -1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                double mult = fabs(1.0 - 2.0 * (double)R[i][j] * B[j][i]);
                if (mult > best_mult) {
                    best_mult = mult;
                    best_i = i;
                    best_j = j;
                }
            }
        }
        if (best_i >= 0) {
            int i = best_i, j = best_j;
            double denom = 1.0 - 2.0 * (double)R[i][j] * B[j][i];
            double factor = (2.0 * (double)R[i][j]) / denom;
            double col_i[MAX_M], row_j[MAX_M];
            for (int a = 0; a < n; a++) col_i[a] = B[a][i];
            for (int b = 0; b < n; b++) row_j[b] = B[j][b];
            for (int a = 0; a < n; a++) {
                for (int b = 0; b < n; b++) {
                    B[a][b] += factor * col_i[a] * row_j[b];
                }
            }
            R[i][j] = -R[i][j];
            total_flips++;
            total_log_gain += log(best_mult);
            continue;
        }
        break;
    }
    *log_gain_out = total_log_gain;
    return total_flips;
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s [n] <restarts> <kicks> [hadamard_file] [out_matrix_file]\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    int restarts = atoi(argv[2]);
    int kicks = atoi(argv[3]);
    const char *h_file = (argc >= 5 && strcmp(argv[4], "paley1") != 0) ? argv[4] : NULL;
    const char *out_file = (argc >= 6) ? argv[5] : NULL;

    int m = n - 1;
    int H[MAX_M][MAX_M];
    if (h_file) {
        int m_loaded = 0;
        if (!load_hadamard(h_file, &m_loaded, H) || m_loaded != m) {
            fprintf(stderr, "Error: Failed to load valid %dx%d Hadamard matrix from %s\n", m, m, h_file);
            return 1;
        }
    } else {
        if (!build_paley1(m, H) || !verify_hadamard(m, H)) {
            fprintf(stderr, "Error: Cannot build Paley Class I Hadamard matrix for m=%d\n", m);
            return 1;
        }
    }

    int best_u[MAX_M], best_c[MAX_M];
    int best_E = optimize_excess(m, H, restarts, kicks, best_u, best_c);
    int k = m / 4;
    int factor = k + best_E / 4;

    /* Construct bordered n x n matrix R */
    int R[MAX_M][MAX_M];
    R[0][0] = -1;
    for (int j = 0; j < m; j++) {
        R[0][j + 1] = 1;
        R[j + 1][0] = 1;
    }
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            R[i + 1][j + 1] = best_u[i] * best_c[j] * H[i][j];
        }
    }

    double log_gain = 0.0;
    int sm_flips = sherman_morrison_polish(n, R, &log_gain);

    printf("n=%d m=%d k=%d best_excess=%d factor=%d sm_flips=%d log_gain=%.8f\n",
           n, m, k, best_E, factor, sm_flips, log_gain);

    if (out_file) {
        FILE *f = fopen(out_file, "w");
        if (!f) {
            fprintf(stderr, "Error opening output file %s\n", out_file);
            return 1;
        }
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                fprintf(f, "%s%d", (j == 0 ? "" : " "), R[i][j]);
            }
            fprintf(f, "\n");
        }
        fclose(f);
    }
    return 0;
}
