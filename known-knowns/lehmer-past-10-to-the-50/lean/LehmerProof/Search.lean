/-
  V3R1T4S — Lehmer's totient problem, formalization (2026-10-09).
  Part 2: every rule the LCAP-1 / LCRT-4 search uses to prune or close a node is a NECESSARY
  condition on a genuine Lehmer number N ≤ 10^56, so the exhaustive search cannot skip one.

  Setting: `F = N.primeFactors`, a "prefix" `T ⊆ F` and its rest `R = F \ T`;
  `P = ∏ T`, `Φ = ∏ (t - 1)` over `T`.
-/
import LehmerProof.Reduction

open Nat Finset

namespace LehmerOracle

variable {N : ℕ}

theorem prod_map_pred_le (l : List ℕ) : (l.map (· - 1)).prod ≤ l.prod := by
  induction l with
  | nil => simp
  | cons a l ih => simp only [List.map_cons, List.prod_cons]; exact Nat.mul_le_mul (Nat.sub_le a 1) ih

/-- Product and "totient product" of a finite set of numbers. -/
def Pr (s : Finset ℕ) : ℕ := ∏ x ∈ s, x
def Ph (s : Finset ℕ) : ℕ := ∏ x ∈ s, (x - 1)

section Setting

variable (h : IsLehmer N) (hN : N ≤ 10 ^ 56)
include h hN

theorem split {T : Finset ℕ} (hT : T ⊆ N.primeFactors) :
    N = Pr T * Pr (N.primeFactors \ T) ∧ N.totient = Ph T * Ph (N.primeFactors \ T) := by
  have hsq := squarefree_of_lehmer h
  constructor
  · rw [Pr, Pr, mul_comm, Finset.prod_sdiff hT, Nat.prod_primeFactors_of_squarefree hsq]
  · rw [Ph, Ph, mul_comm, Finset.prod_sdiff hT, totient_eq_prod_of_squarefree hsq]

theorem two_le_of_mem {p : ℕ} (hp : p ∈ N.primeFactors) : 2 ≤ p :=
  (Nat.prime_of_mem_primeFactors hp).two_le

/-- **(c1)** Every prefix with a nonempty rest satisfies `P < 2Φ` (the tree invariant `A > 0`). -/
theorem c1 {T : Finset ℕ} (hT : T ⊆ N.primeFactors) (hR : (N.primeFactors \ T).Nonempty) :
    Pr T < 2 * Ph T := by
  obtain ⟨hNe, hφe⟩ := split h hN hT
  obtain ⟨-, -, hN2⟩ := reduction h hN
  set R := N.primeFactors \ T
  have hRgt : Ph R < Pr R := by
    unfold Ph Pr
    apply Finset.prod_lt_prod_of_nonempty₀ _ _ hR
    · intro x hx
      have := two_le_of_mem h hN (Finset.mem_sdiff.mp hx).1; omega
    · intro x hx
      have := two_le_of_mem h hN (Finset.mem_sdiff.mp hx).1; omega
  have hΦ : 0 < Ph T := by
    unfold Ph; apply Finset.prod_pos; intro x hx
    have := two_le_of_mem h hN (hT hx); omega
  have hodd : Odd (Pr T) := by
    have hNodd := odd_of_lehmer h
    rw [hNe] at hNodd; exact (Nat.odd_mul.mp hNodd).1
  by_contra hcon
  push Not at hcon
  have hP : 2 * Ph T + 1 ≤ Pr T := by
    rcases hodd with ⟨a, ha⟩; omega
  have : (2 * Ph T + 1) * (Ph R + 1) ≤ Pr T * Pr R := Nat.mul_le_mul hP hRgt
  nlinarith

/-- **lo**: for every `q` in the rest with at least one more prime after it, `P·q < 2Φ·(q-1)`,
equivalently `2Φ < q·(2Φ - P)`, i.e. `q > 2Φ/A`. -/
theorem lo_bound {T : Finset ℕ} (hT : T ⊆ N.primeFactors) {q : ℕ}
    (hq : q ∈ N.primeFactors \ T) (hR : ((N.primeFactors \ T).erase q).Nonempty) :
    Pr T * q < 2 * Ph T * (q - 1) ∧ (2 * Ph T : ℤ) < q * (2 * Ph T - Pr T) := by
  have hqT : q ∉ T := (Finset.mem_sdiff.mp hq).2
  have hT' : insert q T ⊆ N.primeFactors :=
    Finset.insert_subset (Finset.mem_sdiff.mp hq).1 hT
  have hrest : N.primeFactors \ insert q T = (N.primeFactors \ T).erase q := by
    ext x; simp [Finset.mem_sdiff, Finset.mem_erase]; tauto
  have := c1 h hN hT' (hrest ▸ hR)
  rw [Pr, Ph, Finset.prod_insert hqT, Finset.prod_insert hqT] at this
  have h1 : Pr T * q < 2 * Ph T * (q - 1) := by unfold Pr Ph; linarith
  refine ⟨h1, ?_⟩
  have hq2 : 2 ≤ q := two_le_of_mem h hN (Finset.mem_sdiff.mp hq).1
  have h1' : (Pr T * q : ℤ) < 2 * Ph T * ((q : ℤ) - 1) := by
    have := h1; zify [show 1 ≤ q by omega] at this; exact this
  linarith

/-- **(c2)** C-sequence rule: for `q` in the rest, `gcd(q - 1, P) = 1`. -/
theorem c2 {T : Finset ℕ} (hT : T ⊆ N.primeFactors) {q : ℕ} (hq : q ∈ N.primeFactors \ T) :
    Nat.Coprime (q - 1) (Pr T) := by
  unfold Pr
  apply Nat.Coprime.prod_right
  intro t ht
  obtain ⟨htp, htn, -⟩ := Nat.mem_primeFactors.mp (hT ht)
  obtain ⟨hqp, hqn, -⟩ := Nat.mem_primeFactors.mp (Finset.mem_sdiff.mp hq).1
  exact (Nat.Coprime.symm ((Nat.Prime.coprime_iff_not_dvd htp).mpr
    (cset_of_lehmer h htp hqp htn hqn)))

/-- **(c3) / cap**: the prefix times any subset of the rest is at most `N` (hence at most the cap X). -/
theorem cap {T U : Finset ℕ} (hT : T ⊆ N.primeFactors) (hU : U ⊆ N.primeFactors \ T) :
    Pr T * Pr U ≤ N := by
  obtain ⟨hNe, -⟩ := split h hN hT
  have hpos : 0 < Pr (N.primeFactors \ T) := by
    unfold Pr; apply Finset.prod_pos; intro x hx
    have := two_le_of_mem h hN (Finset.mem_sdiff.mp hx).1; omega
  calc Pr T * Pr U ≤ Pr T * Pr (N.primeFactors \ T) :=
        Nat.mul_le_mul_left _ (Nat.le_of_dvd hpos (Finset.prod_dvd_prod_of_subset _ _ _ hU))
    _ = N := hNe.symm

/-- **Lemma CRT** (cofactor congruence, the "live" test): with at least two primes left,
`N ≡ 1 (mod 8Φ)` and `P` is a unit mod `8Φ`; so the cofactor `Q` satisfies `P·Q ≡ 1 (mod 8Φ)`. -/
theorem crt {T : Finset ℕ} (hT : T ⊆ N.primeFactors) (hR : 2 ≤ #(N.primeFactors \ T)) :
    Pr T * Pr (N.primeFactors \ T) ≡ 1 [MOD 8 * Ph T] ∧ Nat.Coprime (Pr T) (8 * Ph T) := by
  obtain ⟨hNe, hφe⟩ := split h hN hT
  obtain ⟨-, -, hN2⟩ := reduction h hN
  set R := N.primeFactors \ T
  have hodd : ∀ x ∈ N.primeFactors, Odd x := by
    intro x hx
    obtain ⟨hp, hxn, -⟩ := Nat.mem_primeFactors.mp hx
    rcases hp.eq_two_or_odd' with rfl | ho
    · exact absurd (odd_of_lehmer h) (by rw [Nat.not_odd_iff_even]; exact even_iff_two_dvd.mpr hxn)
    · exact ho
  have h4 : 4 ∣ Ph R := by
    have h2pow : 2 ^ #R ∣ Ph R := by
      unfold Ph
      rw [← Finset.prod_const]
      apply Finset.prod_dvd_prod_of_dvd
      intro x hx
      obtain ⟨a, ha⟩ := hodd x (Finset.mem_sdiff.mp hx).1
      exact ⟨a, by omega⟩
    exact (pow_dvd_pow 2 hR).trans h2pow
  constructor
  · rw [← hNe]
    obtain ⟨c, hc⟩ := h4
    have : N = 8 * Ph T * c + 1 := by rw [hN2, hφe, hc]; ring
    rw [this]
    exact ((Nat.modEq_iff_dvd' (by omega)).mpr ⟨c, by omega⟩).symm
  · apply Nat.Coprime.mul_right
    · have hPodd : Odd (Pr T) := by
        have hNodd := odd_of_lehmer h
        rw [hNe] at hNodd; exact (Nat.odd_mul.mp hNodd).1
      have := Nat.Coprime.pow_right 3 (Nat.coprime_two_right.mpr hPodd)
      simpa using this
    · unfold Pr Ph
      apply Nat.Coprime.prod_left; intro t ht
      apply Nat.Coprime.prod_right; intro u hu
      obtain ⟨htp, htn, -⟩ := Nat.mem_primeFactors.mp (hT ht)
      obtain ⟨hup, hun, -⟩ := Nat.mem_primeFactors.mp (hT hu)
      exact (Nat.Prime.coprime_iff_not_dvd htp).mpr (cset_of_lehmer h htp hup htn hun)

/-- **Euler closure**: a genuine solution passes `2^((N-1)/2) ≡ 1 (mod N)`, so a node whose
candidates all fail this test has no completion. -/
theorem euler : 2 ^ ((N - 1) / 2) ≡ 1 [MOD N] := by
  obtain ⟨-, -, hN2⟩ := reduction h hN
  have : (N - 1) / 2 = N.totient := by omega
  rw [this]
  exact Nat.ModEq.pow_totient (Nat.coprime_two_left.mpr (odd_of_lehmer h))

/-- **AP child filter**: every prime of the rest divides the cofactor `Q`. -/
theorem child_dvd {T : Finset ℕ} {q : ℕ} (hq : q ∈ N.primeFactors \ T) :
    q ∣ Pr (N.primeFactors \ T) := Finset.dvd_prod_of_mem _ hq

/-- **(c4)** next-primes ratio bound. Let `q` be the smallest prime of the rest and `L` list the
consecutive primes after `q` (`Enumerates`), at least as many as the primes left after `q`. Then
`P·q·∏L > 2Φ·(q-1)·∏(L-1)`; and the cap gives `P·q·∏(first m' of L) ≤ N`. -/
theorem c4 {T : Finset ℕ} (hT : T ⊆ N.primeFactors) {q : ℕ} (hq : q ∈ N.primeFactors \ T)
    (hqmin : ∀ r ∈ N.primeFactors \ T, q ≤ r)
    {L : List ℕ} (hL : Enumerates (fun x => x.Prime ∧ q < x) L) (hL2 : ∀ x ∈ L, 2 ≤ x)
    (hlen : #((N.primeFactors \ T).erase q) ≤ L.length) :
    2 * Ph T * (q - 1) * (L.map (· - 1)).prod < Pr T * q * L.prod ∧
      Pr T * q * (L.take #((N.primeFactors \ T).erase q)).prod ≤ N := by
  set R' := (N.primeFactors \ T).erase q
  have hqT : q ∉ T := (Finset.mem_sdiff.mp hq).2
  have hqF := (Finset.mem_sdiff.mp hq).1
  have hT' : insert q T ⊆ N.primeFactors := Finset.insert_subset hqF hT
  have hrest : N.primeFactors \ insert q T = R' := by
    ext x; simp [R', Finset.mem_sdiff, Finset.mem_erase]; tauto
  obtain ⟨hNe, hφe⟩ := split h hN hT'
  obtain ⟨-, -, hN2⟩ := reduction h hN
  rw [hrest] at hNe hφe
  have hA : ∀ x ∈ R', x.Prime ∧ q < x := by
    intro x hx
    obtain ⟨hxq, hxR⟩ := Finset.mem_erase.mp hx
    exact ⟨Nat.prime_of_mem_primeFactors (Finset.mem_sdiff.mp hxR).1,
      lt_of_le_of_ne (hqmin x hxR) (Ne.symm hxq)⟩
  have hge : ∀ x ∈ R', 1 ≤ x := fun x hx => (hA x hx).1.one_lt.le
  obtain ⟨d1, d2⟩ := dominate hL (fun x hx => le_trans (by norm_num) (hL2 x hx)) R' hA hge hlen
  have hPq : Pr (insert q T) = Pr T * q := by unfold Pr; rw [Finset.prod_insert hqT, mul_comm]
  have hΦq : Ph (insert q T) = Ph T * (q - 1) := by unfold Ph; rw [Finset.prod_insert hqT, mul_comm]
  constructor
  · -- exact relation N = 2φ + 1 restricted to the split at `insert q T`
    set a := Pr T * q
    set b := Ph T * (q - 1)
    have hexact : 2 * b * Ph R' < a * Pr R' := by
      rw [← hPq, ← hΦq, mul_assoc, ← hφe, ← hNe]; omega
    have hPhpos : 0 < Ph R' := by
      unfold Ph; apply Finset.prod_pos; intro x hx; have := (hA x hx).1.two_le; omega
    -- ratio over the true rest ≤ ratio over the first #R' entries of L
    set t := (L.take #R').prod
    set tm := ((L.take #R').map (· - 1)).prod
    have hmain : 2 * b * tm < a * t := by
      have e1 : 2 * b * Ph R' * tm < a * Pr R' * tm := Nat.mul_lt_mul_of_pos_right hexact (by
        apply List.prod_pos; intro z hz; simp only [List.mem_map] at hz
        obtain ⟨w, hw, rfl⟩ := hz; have := hL2 w (List.mem_of_mem_take hw); omega)
      have e2 : a * (Pr R' * tm) ≤ a * (t * Ph R') := Nat.mul_le_mul_left a (by unfold Pr Ph; exact d2)
      have : 2 * b * tm * Ph R' < a * t * Ph R' := by nlinarith
      exact Nat.lt_of_mul_lt_mul_right this
    -- extend from the first #R' entries to all of L (extra factors x/(x-1) ≥ 1)
    have hsplit1 : L.prod = t * (L.drop #R').prod := (List.prod_take_mul_prod_drop L _).symm
    have hsplit2 : (L.map (· - 1)).prod = tm * ((L.drop #R').map (· - 1)).prod := by
      rw [← List.prod_take_mul_prod_drop (L.map (· - 1)) #R', ← List.map_take, ← List.map_drop]
    have hdrop : ((L.drop #R').map (· - 1)).prod ≤ (L.drop #R').prod := by
      exact prod_map_pred_le _
    rw [hsplit1, hsplit2, show 2 * Ph T * (q - 1) = 2 * b by simp only [b]; ring]
    calc 2 * b * (tm * ((L.drop #R').map (· - 1)).prod)
        = (2 * b * tm) * ((L.drop #R').map (· - 1)).prod := by ring
      _ ≤ (2 * b * tm) * (L.drop #R').prod := Nat.mul_le_mul_left _ hdrop
      _ < (a * t) * (L.drop #R').prod := Nat.mul_lt_mul_of_pos_right hmain (by
          apply List.prod_pos; intro z hz; have := hL2 z (List.mem_of_mem_drop hz); omega)
      _ = a * (t * (L.drop #R').prod) := by ring
  · calc Pr T * q * (L.take #R').prod ≤ Pr T * q * Pr R' := Nat.mul_le_mul_left _ (by
          unfold Pr; exact d1)
      _ = N := by rw [← hPq, hNe]

/-- **Two-prime closure C2**: if exactly two primes `q, r` remain, then with `A = 2Φ - P`,
`(A·q - 2Φ)·r = 2Φ(q-1) - 1` (so `r = n(q)/u(q)` is forced), and the candidate-closure identities
`r₁ + r₂ = Q - Ψ + 1`, `(Q - Ψ + 1)² - 4Q = (r₂ - r₁)²` hold with `Q = q·r`, `Ψ = (q-1)(r-1)`. -/
theorem c2_closure {T : Finset ℕ} (hT : T ⊆ N.primeFactors) {q r : ℕ} (hqr : q ≠ r)
    (hR : N.primeFactors \ T = {q, r}) :
    ((2 * Ph T - Pr T) * q - 2 * Ph T : ℤ) * r = 2 * Ph T * ((q : ℤ) - 1) - 1 ∧
    ((Pr T : ℤ) * (q * r) - 1 = 2 * Ph T * (((q : ℤ) - 1) * (r - 1))) ∧
    ((q : ℤ) * r - ((q : ℤ) - 1) * (r - 1) + 1 = q + r) ∧
    (((q : ℤ) * r - ((q : ℤ) - 1) * (r - 1) + 1) ^ 2 - 4 * (q * r) = ((r : ℤ) - q) ^ 2) := by
  obtain ⟨hNe, hφe⟩ := split h hN hT
  obtain ⟨-, -, hN2⟩ := reduction h hN
  rw [hR] at hNe hφe
  have hq1 : 1 ≤ q := (two_le_of_mem h hN (by
    have : q ∈ N.primeFactors \ T := by rw [hR]; simp
    exact (Finset.mem_sdiff.mp this).1)).trans' (by norm_num)
  have hr1 : 1 ≤ r := (two_le_of_mem h hN (by
    have : r ∈ N.primeFactors \ T := by rw [hR]; simp
    exact (Finset.mem_sdiff.mp this).1)).trans' (by norm_num)
  have hpr : Pr {q, r} = q * r := by unfold Pr; rw [Finset.prod_pair hqr]
  have hph : Ph {q, r} = (q - 1) * (r - 1) := by unfold Ph; rw [Finset.prod_pair hqr]
  rw [hpr] at hNe; rw [hph] at hφe
  have key : (Pr T : ℤ) * (q * r) = 2 * (Ph T * (((q : ℤ) - 1) * (r - 1))) + 1 := by
    have : Pr T * (q * r) = 2 * (Ph T * ((q - 1) * (r - 1))) + 1 := by rw [← hNe, ← hφe]; exact hN2
    zify [hq1, hr1] at this; exact this
  refine ⟨by linear_combination (-1 : ℤ) * key, by linear_combination key, by ring, by ring⟩

end Setting

/-! ### Summary: the conditions every node on the path to a genuine solution satisfies -/

/-- For any Lehmer number `N ≤ 10^56` and any prefix `T` of its prime factors with at least two
primes remaining, `T` passes every pruning test of the search: the invariant `P < 2Φ` (c1),
the live test `P·Q ≡ 1 (mod 8Φ)` with `P` a unit (Lemma CRT), `P·Q ≤ N` (cap), and every remaining
prime `q` passes the C-sequence test (c2) and the AP filter `q ∣ Q`. -/
theorem node_conditions {N : ℕ} (h : IsLehmer N) (hN : N ≤ 10 ^ 56) {T : Finset ℕ}
    (hT : T ⊆ N.primeFactors) (hR : 2 ≤ #(N.primeFactors \ T)) :
    Pr T < 2 * Ph T ∧
    Pr T * Pr (N.primeFactors \ T) ≡ 1 [MOD 8 * Ph T] ∧ Nat.Coprime (Pr T) (8 * Ph T) ∧
    Pr T * Pr (N.primeFactors \ T) ≤ N ∧
    ∀ q ∈ N.primeFactors \ T, Nat.Coprime (q - 1) (Pr T) ∧ q ∣ Pr (N.primeFactors \ T) := by
  have hne : (N.primeFactors \ T).Nonempty := Finset.card_pos.mp (by omega)
  obtain ⟨h1, h2⟩ := crt h hN hT hR
  exact ⟨c1 h hN hT hne, h1, h2, cap h hN hT subset_rfl,
    fun q hq => ⟨c2 h hN hT hq, child_dvd h hN hq⟩⟩

end LehmerOracle
