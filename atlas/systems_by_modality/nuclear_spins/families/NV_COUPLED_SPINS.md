# NV-Coupled Nuclear Spins (Diamond) — État de l'Art

## Systèmes Catalogués dans Atlas

| ID | Nucleus | Host | T2 | T1 | Temperature | Coupling Strength | Method | Evidence | DOI |
|----|---------|------|----|----|-------------|-------------------|--------|----------|-----|
| **NUC_13C_001** | ¹³C | Diamond (NV-coupled) | **1000 ms** | — | 298K | 130 kHz | Dynamical decoupling | A | [10.1103/PhysRevLett.109.137602](https://doi.org/10.1103/PhysRevLett.109.137602) |
| **NUC_14N_001** | ¹⁴N | Diamond (NV intrinsic) | **3 ms** | — | 298K | 2.2 MHz | ODMR | A | [10.1126/science.1231364](https://doi.org/10.1126/science.1231364) |
| **NUC_15N_001** | ¹⁵N | Diamond (NV substitutional) | — | Long (>1s) | 298K | 3.1 MHz | ODMR | A | [10.1103/PhysRevLett.110.167402](https://doi.org/10.1103/PhysRevLett.110.167402) |

**Top performer :** NUC_13C_001 — T2 = **1000 ms (1 s) @ RT**, dynamical decoupling

---

## Paramètres Critiques

| Parameter | ¹³C (bath) | ¹⁴N (intrinsic) | ¹⁵N (substitutional) | Unit |
|-----------|-----------|----------------|---------------------|------|
| **T2 (coherence)** | 1000 ms (1 s) | 3 ms | — | ms |
| **T1 (relaxation)** | — | — | >1 s | s |
| **Coupling strength** | 130 kHz | 2.2 MHz | 3.1 MHz | Hz |
| **Temperature** | 298K | 298K | 298K | K |
| **Control method** | DD via NV | ODMR via NV | ODMR via NV | — |
| **Nuclear spin** | I=1/2 | I=1 (quadrupole) | I=1/2 | — |

**Key advantage :** **Hybrid qubit** (NV electron spin + nuclear spin) → **quantum memory at RT**

---

## Top 3 Papers Clés

### 1. Maurer et al. (2012) — PRL
**DOI :** [10.1103/PhysRevLett.109.137602](https://doi.org/10.1103/PhysRevLett.109.137602)  
**Breakthrough :** ¹³C nuclear spin T2 = 1s @ RT using dynamical decoupling  
**Key result :** NV-¹³C hybrid qubit, quantum memory demonstrated  
**Status :** **[AVÉRÉ]** — Direct T2 measurement

### 2. Taminiau et al. (2012) — Science
**DOI :** [10.1126/science.1231364](https://doi.org/10.1126/science.1231364)  
**Breakthrough :** ¹⁴N nuclear spin control via NV ODMR  
**Key result :** T2 = 3ms, entanglement NV-¹⁴N demonstrated  
**Status :** **[AVÉRÉ]** — Quantum gates implemented

### 3. Dréau et al. (2013) — PRL
**DOI :** [10.1103/PhysRevLett.110.167402](https://doi.org/10.1103/PhysRevLett.110.167402)  
**Breakthrough :** ¹⁵N-NV center, long T1 (>1s) @ RT  
**Key result :** Isotope substitution improves coherence (I=1/2 vs I=1)  
**Status :** **[AVÉRÉ]** — Direct measurement

---

## Applications Démontrées

### ✅ In Vitro (Diamond)
- **Quantum memory** (¹³C, ¹⁴N, ¹⁵N) — ✅ **[AVÉRÉ]**
- **Quantum gates** (NV-¹⁴N CNOT, NV-¹³C controlled-phase) — ✅ **[AVÉRÉ]**
- **Entanglement** (NV-nuclear spin Bell states) — ✅ **[AVÉRÉ]**

### ⚠️ In Cellulo (Nanodiamonds)
- **Limited demonstrations** (NV-¹³C hybrid in cells not yet shown)
- **Challenge :** Maintain T2 in biological environment (¹H spin bath)
- **Potential :** Quantum sensing with enhanced sensitivity (nuclear spin readout)

### ❌ In Vivo
- **No demonstrations yet**
- **Potential :** Hyperpolarized ¹³C imaging + NV readout (hybrid modality)

---

## Limitations Connues

### Coherence Degradation
- ✅ **T2 (¹³C) = 1s @ RT in diamond** (record for solid-state @ ambient)
- ❌ **T2 in cellulo unknown** (likely <<1s due to ¹H bath)
- ⚠️ **Dynamical decoupling required** (not passive, needs control pulses)

### Coupling Strength Trade-off
- ✅ **Strong coupling** (130 kHz - 3 MHz) → fast quantum gates
- ⚠️ **Strong coupling** → faster decoherence from NV electron spin
- **Optimal :** ~100 kHz (balance gate speed vs coherence)

### Isotopic Purity
- ⚠️ **Natural ¹³C abundance 1.1%** → most diamond is ¹²C (I=0, no spin)
- ✅ **¹³C-enriched diamond available** (but expensive)
- ✅ **¹⁴N intrinsic to NV** (no isotope engineering needed)
- ✅ **¹⁵N substitution possible** (ion implantation)

### Biocompatibility
- ✅ **Diamond biocompatible**
- ⚠️ **Nanodiamond delivery same challenges as NV** (size, functionalization)

---

## Connexions Écosystème

### fp-qubit-design
**Opportunity :** Design NV-nuclear spin hybrid sensors
- Predict coupling strength vs ¹³C distance
- ML models : ¹³C lattice position → hyperfine coupling
- Engineer "optimal" ¹³C shell around NV (maximize T2, minimize coupling)

### ising-life-lab
**Metrics applicable :**
- **Robustness** : T2 vs spin bath density (¹³C concentration)
- **Stability** : NV-¹³C entanglement fidelity
- **Memory capacity** : Number of controllable ¹³C spins per NV

### arrest-molecules
**Hypothesis :** Molecular arrest modulates NV-¹³C coupling
- Do arrest molecules alter diamond lattice dynamics → change hyperfine coupling?
- Mechanism : Strain/pressure on diamond → shift coupling strength
- **Testable :** NV-¹³C spectroscopy under molecular arrest conditions (unlikely, but conceptual link)

---

## TODO / Extensions

- [ ] Add ¹³C bath spin clusters (multiple ¹³C coupled to single NV)
- [ ] Add ¹⁴N-¹⁵N comparison (I=1 vs I=1/2, coherence difference)
- [ ] Extract T2 vs ¹³C enrichment (1.1% vs 99% enriched diamond)
- [ ] Add dynamical decoupling protocols (XY-8, Uhrig, etc.)
- [ ] Validate T1 data (currently sparse for ¹³C)
- [ ] Add coupling strength vs distance curves (nearest-neighbor to 5th shell)

---

**Last updated :** 2025-11-13  
**Curator :** non_optical_v1  
**Systems in Atlas :** 3 (NUC_13C_001, NUC_14N_001, NUC_15N_001)  
**Evidence level :** A (all systems, direct T2/T1 measurements)  
**Advantage :** **Quantum memory @ RT** (1s coherence), hybrid qubit platform

