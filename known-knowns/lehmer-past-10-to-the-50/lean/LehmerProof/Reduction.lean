/-
  V3R1T4S — Lehmer's totient problem, formalization (2026-10-09).
  Part 1: the reduction used by the 10^50 search.

  Main result (`reduction`): a Lehmer number N ≤ 10^56 is odd, squarefree, not divisible by 3,
  all its prime factors are ≥ 5, and N = 2·φ(N) + 1 (index k = 2).
-/
import Mathlib

open Nat Finset

namespace LehmerOracle

/-- A Lehmer number: a composite `n > 1` with `φ n ∣ n - 1`. -/
def IsLehmer (n : ℕ) : Prop := 1 < n ∧ ¬ n.Prime ∧ n.totient ∣ n - 1

/-! ### Basic structure -/

theorem odd_of_lehmer {n : ℕ} (h : IsLehmer n) : Odd n := by
  obtain ⟨h1, hp, hd⟩ := h
  by_contra hodd
  rw [Nat.not_odd_iff_even] at hodd
  have h2 : 2 < n := by
    rcases Nat.lt_or_ge 2 n with h | h
    · exact h
    · exact absurd (show n = 2 by omega ▸ Nat.prime_two) (by intro h'; exact hp (by
        have : n = 2 := by omega
        subst this; exact Nat.prime_two))
  obtain ⟨m, hm⟩ := (Nat.totient_even h2).two_dvd.trans hd
  obtain ⟨a, ha⟩ := hodd
  omega

theorem dvd_one_of_dvd_and_dvd_pred {n p : ℕ} (hn : 1 ≤ n) (h1 : p ∣ n) (h2 : p ∣ n - 1) :
    p ∣ 1 := by
  have := Nat.dvd_sub h1 h2
  rwa [Nat.sub_sub_self hn] at this

theorem squarefree_of_lehmer {n : ℕ} (h : IsLehmer n) : Squarefree n := by
  obtain ⟨h1, -, hd⟩ := h
  rw [Nat.squarefree_iff_prime_squarefree]
  intro p hp hpp
  obtain ⟨m, rfl⟩ := hpp
  have hpm : p ∣ p * m := dvd_mul_right p m
  have htot : (p * (p * m)).totient = p * (p * m).totient :=
    Nat.totient_mul_of_prime_of_dvd hp hpm
  have hdvd : p ∣ (p * p * m).totient := by rw [mul_assoc, htot]; exact dvd_mul_right _ _
  have := dvd_one_of_dvd_and_dvd_pred (by omega)
    ((dvd_mul_right p p).mul_right m) (hdvd.trans hd)
  exact hp.one_lt.ne' (Nat.dvd_one.mp this)

/-- The C-set property: no prime factor `p` divides `q - 1` for a prime factor `q`. -/
theorem cset_of_lehmer {n p q : ℕ} (h : IsLehmer n) (hp : p.Prime) (hq : q.Prime)
    (hpn : p ∣ n) (hqn : q ∣ n) : ¬ p ∣ q - 1 := by
  intro hpq
  obtain ⟨h1, -, hd⟩ := h
  have hq1 : q - 1 ∣ n.totient := by
    rw [← Nat.totient_prime hq]; exact Nat.totient_dvd_of_dvd hqn
  have := dvd_one_of_dvd_and_dvd_pred (by omega) hpn ((hpq.trans hq1).trans hd)
  exact hp.one_lt.ne' (Nat.dvd_one.mp this)

/-- For squarefree `n`, `φ n = ∏ (p - 1)` over its prime factors. -/
theorem totient_eq_prod_of_squarefree {n : ℕ} (hn : Squarefree n) :
    n.totient = ∏ p ∈ n.primeFactors, (p - 1) := by
  have h := Nat.totient_mul_prod_primeFactors n
  rw [Nat.prod_primeFactors_of_squarefree hn] at h
  have hn0 : 0 < n := Nat.pos_of_ne_zero hn.ne_zero
  exact Nat.eq_of_mul_eq_mul_right hn0 (by rw [h, mul_comm])

/-- The index `k = (n-1)/φ(n)` of a Lehmer number is at least 2. -/
theorem index_ge_two {n k : ℕ} (h : IsLehmer n) (hk : n - 1 = k * n.totient) : 2 ≤ k := by
  obtain ⟨h1, hp, -⟩ := h
  rcases k with _ | _ | k
  · simp at hk; omega
  · simp at hk
    exact absurd ((Nat.totient_eq_iff_prime (by omega)).mp hk.symm) hp
  · omega

/-! ### If `3 ∣ n` then `k ≡ 1 (mod 3)` -/

theorem index_mod_three {n k : ℕ} (h : IsLehmer n) (hk : n - 1 = k * n.totient) (h3 : 3 ∣ n) :
    k % 3 = 1 := by
  have hsq := squarefree_of_lehmer h
  have hS : 3 ∈ n.primeFactors := by
    rw [Nat.mem_primeFactors]; exact ⟨Nat.prime_three, h3, hsq.ne_zero⟩
  -- every other prime factor is ≡ 2 (mod 3)
  have hother : ∀ p ∈ n.primeFactors.erase 3, (p - 1) % 3 = 1 := by
    intro p hpm
    obtain ⟨hp3, hpS⟩ := Finset.mem_erase.mp hpm
    obtain ⟨hp, hpn, -⟩ := Nat.mem_primeFactors.mp hpS
    have hc := cset_of_lehmer h Nat.prime_three hp h3 hpn
    have hnd : ¬ 3 ∣ p := fun hd =>
      hp3 ((Nat.prime_dvd_prime_iff_eq Nat.prime_three hp).mp hd).symm
    have h2 := hp.two_le
    omega
  have htot : n.totient % 3 = 2 := by
    rw [totient_eq_prod_of_squarefree hsq, ← Finset.mul_prod_erase _ _ hS, Nat.mul_mod,
      Finset.prod_nat_mod, Finset.prod_congr rfl hother]
    simp
  have h1 := h.1
  have : (n - 1) % 3 = 2 := by omega
  rw [hk, Nat.mul_mod, htot] at this
  have : k % 3 < 3 := Nat.mod_lt _ (by norm_num)
  interval_cases hk3 : k % 3 <;> simp_all

/-! ### Domination: a finite set of "allowed" numbers is dominated by the smallest allowed ones -/

/-- `L` lists the smallest elements of the allowed set `A`, in order: every allowed `x` below `L[j]`
already occurs among the first `j` entries. -/
def Enumerates (A : ℕ → Prop) (L : List ℕ) : Prop :=
  ∀ j (hj : j < L.length), ∀ x, A x → x < L[j] → x ∈ L.take j

theorem dominate {A : ℕ → Prop} {L : List ℕ} (hL : Enumerates A L) (hpos : ∀ x ∈ L, 1 ≤ x) :
    ∀ S : Finset ℕ, (∀ x ∈ S, A x) → (∀ x ∈ S, 1 ≤ x) → #S ≤ L.length →
      (L.take #S).prod ≤ ∏ x ∈ S, x ∧
      (∏ x ∈ S, x) * ((L.take #S).map (· - 1)).prod ≤
        (L.take #S).prod * ∏ x ∈ S, (x - 1) := by
  intro S
  induction S using Finset.induction_on_max with
  | empty => intros; simp
  | insert m s hlt ih =>
    intro hA hge hcard
    have hms : m ∉ s := fun hm => lt_irrefl _ (hlt m hm)
    rw [Finset.card_insert_of_notMem hms] at hcard ⊢
    have hj : #s < L.length := by omega
    obtain ⟨ih1, ih2⟩ := ih (fun x hx => hA x (mem_insert_of_mem hx))
      (fun x hx => hge x (mem_insert_of_mem hx)) (by omega)
    -- the key comparison L[#s] ≤ m
    have hkey : L[#s] ≤ m := by
      by_contra hcon
      push Not at hcon
      have hsub : insert m s ⊆ (L.take #s).toFinset := by
        intro x hx
        rw [List.mem_toFinset]
        apply hL #s hj x (hA x hx)
        rcases mem_insert.mp hx with rfl | hx
        · exact hcon
        · exact (hlt x hx).trans hcon
      have := Finset.card_le_card hsub
      rw [Finset.card_insert_of_notMem hms] at this
      have hle : #(L.take #s).toFinset ≤ #s :=
        (List.toFinset_card_le _).trans (by simp)
      omega
    have hLpos : 1 ≤ L[#s] := hpos _ (List.getElem_mem hj)
    rw [Finset.prod_insert hms, Finset.prod_insert hms, List.prod_take_succ _ _ hj,
      List.map_take, List.prod_take_succ _ _ (by simpa using hj)]
    simp only [List.getElem_map]
    rw [← List.map_take] at *
    constructor
    · calc (L.take #s).prod * L[#s] ≤ (∏ x ∈ s, x) * m := Nat.mul_le_mul ih1 hkey
        _ = m * ∏ x ∈ s, x := mul_comm _ _
    · -- m * (L[j]-1) ≤ L[j] * (m-1)  ⇔  L[j] ≤ m
      have hm1 : m * (L[#s] - 1) ≤ L[#s] * (m - 1) := by
        have : 1 ≤ m := hge m (mem_insert_self m s)
        zify [hLpos, this]
        nlinarith
      calc m * (∏ x ∈ s, x) * (((L.take #s).map (· - 1)).prod * (L[#s] - 1))
          = ((∏ x ∈ s, x) * ((L.take #s).map (· - 1)).prod) * (m * (L[#s] - 1)) := by ring
        _ ≤ ((L.take #s).prod * ∏ x ∈ s, (x - 1)) * (L[#s] * (m - 1)) :=
            Nat.mul_le_mul ih2 hm1
        _ = (L.take #s).prod * L[#s] * ((m - 1) * ∏ x ∈ s, (x - 1)) := by ring

/-! ### The two exact product bounds below 10^56 -/

/-- The 33 smallest primes ≥ 5. -/
def L5 : List ℕ := [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
  83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]

/-- 3 followed by the 29 smallest primes ≡ 2 (mod 3), excluding 2. -/
def L3 : List ℕ := [3, 5, 11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89, 101, 107, 113, 131, 137, 149,
  167, 173, 179, 191, 197, 227, 233, 239, 251, 257, 263]

def A5 (x : ℕ) : Prop := x.Prime ∧ 5 ≤ x
def A3 (x : ℕ) : Prop := x = 3 ∨ (x.Prime ∧ x % 3 = 2 ∧ 3 ≤ x)

instance : DecidablePred A5 := fun x => by unfold A5; infer_instance
instance : DecidablePred A3 := fun x => by unfold A3; infer_instance

/-- A Boolean certificate: every `x ∈ [lo, B)` that lies below `L[j]` but is not among the first `j`
entries has an explicit proper divisor (so it is not prime). Checked by the kernel. -/
def chk (f : ℕ → Bool) (L : List ℕ) (lo B : ℕ) : Bool :=
  (List.range B).all fun x => (List.range L.length).all fun j =>
    !(f x && decide (lo ≤ x) && decide (x < L.getD j 0) && !((L.take j).contains x)) ||
      (List.range x).any fun d => decide (2 ≤ d) && x % d == 0

theorem chk_spec {f : ℕ → Bool} {L : List ℕ} {lo B : ℕ} (h : chk f L lo B = true) :
    ∀ x < B, ∀ j < L.length, f x = true → lo ≤ x → x < L.getD j 0 → x ∉ L.take j →
      ∃ d < x, 2 ≤ d ∧ x % d = 0 := by
  intro x hx j hj hf hlo hlt hnot
  unfold chk at h
  simp only [List.all_eq_true, List.mem_range] at h
  have := h x hx j hj
  simp only [Bool.or_eq_true, Bool.not_eq_true', Bool.and_eq_false_iff, decide_eq_false_iff_not,
    Bool.not_eq_false', List.contains_iff_mem, List.any_eq_true, List.mem_range, Bool.and_eq_true,
    decide_eq_true_eq, beq_iff_eq] at this
  rcases this with (((h1 | h1) | h1) | h1) | ⟨d, hd, h2, h3⟩
  · simp [hf] at h1
  · exact absurd hlo h1
  · exact absurd hlt h1
  · exact absurd h1 hnot
  · exact ⟨d, hd, h2, h3⟩

theorem chk5 : chk (fun _ => true) L5 5 150 = true := by decide +kernel
theorem chk3 : chk (fun x => x % 3 == 2) L3 5 264 = true := by decide +kernel

theorem not_prime_of_divisor {x d : ℕ} (hd : d < x) (h2 : 2 ≤ d) (hm : x % d = 0) : ¬ x.Prime :=
  fun hp => by
    rcases hp.eq_one_or_self_of_dvd d (Nat.dvd_of_mod_eq_zero hm) with h | h <;> omega

theorem enum5 : Enumerates A5 L5 := by
  intro j hj x hx hlt
  by_contra hnot
  have hg : L5.getD j 0 = L5[j] := by simp [List.getElem?_eq_getElem hj]
  have hb : ∀ i < 33, L5.getD i 0 ≤ 149 := by decide
  have := hb j hj
  obtain ⟨d, hd, h2, hm⟩ := chk_spec chk5 x (by omega) j hj rfl hx.2 (by omega) hnot
  exact not_prime_of_divisor hd h2 hm hx.1

theorem enum3 : Enumerates A3 L3 := by
  intro j hj x hx hlt
  by_contra hnot
  have hg : L3.getD j 0 = L3[j] := by simp [List.getElem?_eq_getElem hj]
  have hb : ∀ i < 30, L3.getD i 0 ≤ 263 := by decide
  have := hb j hj
  rcases hx with rfl | ⟨hp, hm3, h3⟩
  · -- 3 is L3[0], so it is in every nonempty prefix; j = 0 is impossible since x < L3[0] = 3
    have hj0 : j ≠ 0 := by rintro rfl; simp [L3] at hlt
    exact hnot (by
      obtain ⟨k, rfl⟩ : ∃ k, j = k + 1 := ⟨j - 1, by omega⟩
      simp [L3, List.take_succ_cons])
  · have h5 : 5 ≤ x := by
      have := hp.two_le
      rcases (show x = 2 ∨ x = 3 ∨ x = 4 ∨ 5 ≤ x by omega) with h | h | h | h
      · omega
      · subst h; norm_num at hm3
      · subst h; norm_num at hp
      · exact h
    obtain ⟨d, hd, h2, hm⟩ := chk_spec chk3 x (by omega) j hj (by simpa using hm3) h5 (by omega) hnot
    exact not_prime_of_divisor hd h2 hm hp

/-- Ratio bounds: every prefix of `L5` of length ≤ 32 has `∏ p < 3 ∏ (p-1)`; the full 33 exceed 10^56. -/
theorem L5_ratio : ∀ r ≤ 32, (L5.take r).prod < 3 * ((L5.take r).map (· - 1)).prod := by decide
theorem L5_big : 10 ^ 56 < L5.prod := by decide
theorem L3_ratio : ∀ r ≤ 29, (L3.take r).prod < 4 * ((L3.take r).map (· - 1)).prod := by decide
theorem L3_big : 10 ^ 56 < L3.prod := by decide

/-- Generic: a squarefree `n ≤ X` whose prime factors are allowed has `n < c · φ n`. -/
theorem ratio_bound {A : ℕ → Prop} {L : List ℕ} {c X : ℕ} (hL : Enumerates A L)
    (hpos : ∀ x ∈ L, 2 ≤ x) (hbig : X < L.prod)
    (hratio : ∀ r < L.length, (L.take r).prod < c * ((L.take r).map (· - 1)).prod)
    {n : ℕ} (hn : Squarefree n) (hX : n ≤ X) (hA : ∀ p ∈ n.primeFactors, A p) :
    n < c * n.totient := by
  set S := n.primeFactors
  have hge : ∀ x ∈ S, 1 ≤ x := fun x hx => (Nat.prime_of_mem_primeFactors hx).one_lt.le
  have hnS : ∏ x ∈ S, x = n := Nat.prod_primeFactors_of_squarefree hn
  have hcard : #S < L.length := by
    by_contra hc
    push Not at hc
    obtain ⟨T, hTS, hTc⟩ := Finset.exists_subset_card_eq hc
    have h1 := (dominate hL (fun x hx => le_trans (by norm_num) (hpos x hx)) T (fun x hx => hA x (hTS hx)) (fun x hx => hge x (hTS hx))
      (by omega)).1
    rw [hTc, List.take_length] at h1
    have h2 : ∏ x ∈ T, x ≤ n := hnS ▸ Nat.le_of_dvd (by
      rw [hnS]; exact Nat.pos_of_ne_zero hn.ne_zero) (Finset.prod_dvd_prod_of_subset _ _ _ hTS)
    omega
  obtain ⟨-, h2⟩ := dominate hL (fun x hx => le_trans (by norm_num) (hpos x hx)) S hA hge hcard.le
  rw [hnS, ← totient_eq_prod_of_squarefree hn] at h2
  have h3 := hratio #S hcard
  have hpos' : 0 < ((L.take #S).map (· - 1)).prod := by
    apply List.prod_pos
    intro a ha
    simp only [List.mem_map] at ha
    obtain ⟨b, hb, rfl⟩ := ha
    have := hpos b (List.mem_of_mem_take hb)
    omega
  have hφ : 0 < n.totient := Nat.totient_pos.mpr (Nat.pos_of_ne_zero hn.ne_zero)
  by_contra hcon
  push Not at hcon
  have e1 := Nat.mul_lt_mul_of_pos_right h3 hφ
  have e2 := Nat.mul_le_mul_right ((L.take #S).map (· - 1)).prod hcon
  nlinarith

/-! ### The reduction -/

theorem reduction {N : ℕ} (h : IsLehmer N) (hN : N ≤ 10 ^ 56) :
    ¬ 3 ∣ N ∧ (∀ p ∈ N.primeFactors, 5 ≤ p) ∧ N = 2 * N.totient + 1 := by
  have hsq := squarefree_of_lehmer h
  have hodd := odd_of_lehmer h
  obtain ⟨k, hk⟩ := h.2.2
  have hk' : N - 1 = k * N.totient := by rw [hk, mul_comm]
  have hk2 := index_ge_two h hk'
  have h1 := h.1
  have h3 : ¬ 3 ∣ N := by
    intro h3
    have hmod := index_mod_three h hk' h3
    have hk4 : 4 ≤ k := by omega
    have hlt : N < 4 * N.totient := by
      refine ratio_bound (X := 10 ^ 56) enum3 (by decide) L3_big ?_ hsq hN ?_
      · intro r hr; exact L3_ratio r (by simp [L3] at hr; omega)
      · intro p hp
        obtain ⟨hpp, hpn, -⟩ := Nat.mem_primeFactors.mp hp
        by_cases hp3 : p = 3
        · exact Or.inl hp3
        · right
          have hc := cset_of_lehmer h Nat.prime_three hpp h3 hpn
          have hnd : ¬ 3 ∣ p := fun hd =>
            hp3 ((Nat.prime_dvd_prime_iff_eq Nat.prime_three hpp).mp hd).symm
          have h2p : p ≠ 2 := by
            rintro rfl; obtain ⟨a, ha⟩ := hodd; omega
          have := hpp.two_le
          refine ⟨hpp, by omega, by omega⟩
    have : 4 * N.totient ≤ N - 1 := by rw [hk']; exact Nat.mul_le_mul_right _ hk4
    omega
  have h5 : ∀ p ∈ N.primeFactors, 5 ≤ p := by
    intro p hp
    obtain ⟨hpp, hpn, -⟩ := Nat.mem_primeFactors.mp hp
    have h2p : p ≠ 2 := by rintro rfl; obtain ⟨a, ha⟩ := hodd; omega
    have h3p : p ≠ 3 := by rintro rfl; exact h3 hpn
    have h4p : p ≠ 4 := by rintro rfl; exact absurd hpp (by decide)
    have := hpp.two_le
    omega
  refine ⟨h3, h5, ?_⟩
  have hlt : N < 3 * N.totient := by
    refine ratio_bound (X := 10 ^ 56) enum5 (by decide) L5_big ?_ hsq hN ?_
    · intro r hr; exact L5_ratio r (by simp [L5] at hr; omega)
    · intro p hp; exact ⟨Nat.prime_of_mem_primeFactors hp, h5 p hp⟩
  have hk3 : k = 2 := by
    by_contra hne
    have : 3 * N.totient ≤ N - 1 := by rw [hk']; exact Nat.mul_le_mul_right _ (by omega)
    omega
  subst hk3
  omega

end LehmerOracle
