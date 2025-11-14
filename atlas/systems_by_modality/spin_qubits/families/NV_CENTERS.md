# NV Centers (Nitrogen-Vacancy in Diamond) — État de l'Art

## Systèmes Catalogués dans Atlas

| ID | Label | Temperature | T2 | T1 | Magnetic Sensitivity | Evidence | DOI |
|----|-------|-------------|----|----|---------------------|----------|-----|
| **SPIN_NV_001** | NV- RT | 298K | **1800 µs** | 6000 s | 130 nT/√Hz | A | [10.1016/j.physrep.2013.02.001](https://doi.org/10.1016/j.physrep.2013.02.001) |
| **SPIN_NV_002** | NV- 77K | 77K | **600 ms** | — | — | A | [10.1103/PhysRevB.79.075203](https://doi.org/10.1103/PhysRevB.79.075203) |

**Top performer :** SPIN_NV_002 (77K) — T2 = 600 ms (600,000 µs), 333× mieux que RT

---

## Paramètres Critiques

| Parameter | Room Temp (298K) | Cryogenic (77K) | Unit |
|-----------|------------------|-----------------|------|
| **T2 (coherence)** | 1800 µs (1.8 ms) | 600 ms | µs / ms |
| **T1 (relaxation)** | ~6000 s | — | s |
| **Magnetic sensitivity** | 130 nT/√Hz | — | nT/√Hz |
| **Measurement method** | ODMR | ODMR | — |
| **Defect charge state** | NV⁻ (negatively charged) | NV⁻ | — |
| **Host material** | Single-crystal diamond | Single-crystal diamond | — |

**Key insight :** T2 dégradation ×333 @ RT due to phonon coupling, spin bath interactions.

---

## Top 3 Papers Clés

### 1. Doherty et al. (2013) — Physics Reports
**DOI :** [10.1016/j.physrep.2013.02.001](https://doi.org/10.1016/j.physrep.2013.02.001)  
**Breakthrough :** Comprehensive review NV centers, ODMR control, biocompatibility  
**Citation count :** >2500 (foundational reference)

### 2. Balasubramanian et al. (2009) — Nature
**DOI :** [10.1038/nature08470](https://doi.org/10.1038/nature08470)  
**Breakthrough :** NV nanoscale thermometry in living cells  
**Key result :** Temperature sensing 1.8K accuracy, 200nm spatial resolution

### 3. Kucsko et al. (2013) — Nature
**DOI :** [10.1038/nature12373](https://doi.org/10.1038/nature12373)  
**Breakthrough :** Intracellular temperature mapping, nanodiamonds in HeLa cells  
**Key result :** 1mK thermal sensitivity, non-invasive

---

## Applications Démontrées

### ✅ In Vitro
- **Magnetic field sensing** (130 nT/√Hz @ RT)
- **Temperature sensing** (mK precision)
- **Pressure sensing** (GHz shifts under stress)
- **Electric field sensing** (kV/cm detection)

### ✅ In Cellulo
- **Intracellular thermometry** (HeLa, neurons)
- **Magnetic field mapping** (organelles, cytoskeleton)
- **pH sensing** (indirect, via surface chemistry)

### ⚠️ In Vivo
- **Limited demonstrations** (C. elegans, zebrafish embryos)
- **Challenge :** Nanoparticle delivery, long-term retention
- **Toxicity :** Low (biocompatible @ <100nm particles)

---

## Limitations Connues

### Biocompatibility
- ✅ **Diamond chemically inert**, non-toxic
- ⚠️ **Size-dependent uptake** : <50nm optimal, >100nm aggregation
- ⚠️ **Surface functionalization required** for targeting

### Coherence Degradation
- ❌ **T2 @ RT (1.8 ms) << T2 @ 77K (600 ms)** — phonon decoherence
- ❌ **In cellulo T2 further reduced** (~1-10 µs) — spin bath (¹H nuclei)
- ⚠️ **Mitigation :** Dynamical decoupling (DD), isotopic purification (¹²C diamond)

### Optical Readout
- ✅ **ODMR robust** (microwave + optical excitation)
- ⚠️ **Photobleaching minimal** (diamond stable)
- ❌ **Depth penetration limited** (~100 µm, scattering)

### Quantum Control
- ✅ **Single-spin control demonstrated**
- ✅ **Entanglement with ¹³C nuclear spins** (hybrid qubits)
- ⚠️ **Scalability challenge** (individual addressing difficult)

---

## Connexions Écosystème

### fp-qubit-design
**Opportunity :** Design NV-protein conjugates for targeted delivery
- Predict surface chemistry (carboxyl, amine, PEG) impact on uptake
- ML models : NV nanoparticle size → cellular localization

### ising-life-lab
**Metrics applicable :**
- **Robustness** : T2 degradation under noise (spin bath simulations)
- **Stability** : Metastable states (NV charge state switching NV⁰ ↔ NV⁻)
- **Basin depth** : Energy landscape NV triplet ground state

### arrest-molecules
**Shared vocabulary :**
- **Arrest kinetics** (molecular dampening) vs **T2 decoherence** (spin dampening)
- **Hypothesis :** Do arrest molecules (salvinorin A, ibogaine) modulate NV T2 via local field effects?

---

## TODO / Extensions

- [ ] Add NV⁰ (neutral charge state) systems (different optical properties)
- [ ] Add nanodiamond size variants (<10nm, 50nm, 100nm+)
- [ ] Extract T2 vs temperature sweep data (4K → 298K)
- [ ] Add coupling strength to ¹³C nuclear spin bath
- [ ] Validate biocompatibility data (LD50, cytotoxicity assays)

---

**Last updated :** 2025-11-13  
**Curator :** non_optical_v1  
**Systems in Atlas :** 2 (SPIN_NV_001, SPIN_NV_002)  
**Evidence level :** A (peer-reviewed, reproducible)

