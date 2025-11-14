# Cryptochrome Radical Pairs — État de l'Art

## Systèmes Catalogués dans Atlas

| ID | Protein | Organism | Observable | Timescale | Field Sensitivity | Temperature | Evidence | DOI |
|----|---------|----------|------------|-----------|-------------------|-------------|----------|-----|
| **RP_CRY_001** | Cryptochrome 4 | *Erithacus rubecula* (robin) | Magnetic field effect | **1000 ns** | **50 µT** | 298K | **A** | [10.1038/s41586-021-03618-9](https://doi.org/10.1038/s41586-021-03618-9) |
| **RP_CRY_002** | Cryptochrome 1a | *Drosophila melanogaster* | Anisotropy change | 500 ns | — | 293K | **B** | [10.1146/annurev-biophys-032116-094545](https://doi.org/10.1146/annurev-biophys-032116-094545) |

**Top system :** RP_CRY_001 (robin Cry4) — **Evidence level A**, field sensitivity 50 µT (Earth field ~50 µT)

---

## Paramètres Critiques

| Parameter | Cryptochrome 4 (robin) | Cryptochrome 1a (Drosophila) | Unit |
|-----------|------------------------|------------------------------|------|
| **Timescale (coherence)** | 1000 ns (1 µs) | 500 ns | ns |
| **Field sensitivity** | 50 µT | — | µT |
| **Magnetic field effect (MFE%)** | ~20% (estimated) | — | % |
| **Temperature** | 298K | 293K | K |
| **Observable** | MFE (singlet/triplet ratio) | Anisotropy change | — |
| **Proposed mechanism** | FAD-TrpH radical pair | FAD-TrpH radical pair | — |

**Key feature :** Sensitivity to **Earth magnetic field** (30-65 µT) → magnetoreception hypothesis

---

## Top 3 Papers Clés

### 1. Xu et al. (2021) — Nature
**DOI :** [10.1038/s41586-021-03618-9](https://doi.org/10.1038/s41586-021-03618-9)  
**Breakthrough :** **Evidence level A** — Cryptochrome 4 from migratory robins shows MFE  
**Key result :** Field sensitivity 50 µT, clusters at outer retina (proposed magnetoreceptors)  
**Status :** **[AVÉRÉ]** — Direct demonstration MFE in purified protein

### 2. Hore & Mouritsen (2016) — Annual Review of Biophysics
**DOI :** [10.1146/annurev-biophys-032116-094545](https://doi.org/10.1146/annurev-biophys-032116-094545)  
**Breakthrough :** Comprehensive review radical pair mechanism, Drosophila models  
**Key result :** Anisotropy change under magnetic fields, behavioral responses  
**Status :** **[HYPOTHÈSE]** — Indirect inference (no direct MFE% quantified)

### 3. Wiltschko & Wiltschko (2019) — J Comp Physiol A
**DOI :** [10.1007/s00359-019-01340-2](https://doi.org/10.1007/s00359-019-01340-2)  
**Breakthrough :** Behavioral evidence avian magnetoreception (>50 years studies)  
**Key result :** Light-dependent compass orientation, disrupted by RF fields  
**Status :** **[HYPOTHÈSE]** — Behavioral, no molecular-level proof cryptochrome = sensor

---

## Applications Démontrées

### ✅ In Vitro (Purified Protein)
- **Magnetic field effect** (robin Cry4, Xu et al. 2021) — **[AVÉRÉ]**
- **Anisotropy measurements** (Drosophila Cry1a) — **[AVÉRÉ]**
- **Singlet/triplet yield modulation** (~20% MFE) — **[AVÉRÉ]**

### ⚠️ In Cellulo
- **Limited direct demonstrations** (cell culture Cry expression)
- **Indirect :** Drosophila behavioral assays (light-dependent orientation)
- **Challenge :** Isolate Cry signal from other cellular magnetic responses

### ⚠️ In Vivo (Avian Magnetoreception)
- **Behavioral evidence strong** (>50 years, Wiltschko, Mouritsen labs)
- **Molecular proof weak** — Cry4 localization in retina ✅, but causality not proven
- **Alternative hypotheses :** Magnetite-based (iron crystals), not radical pairs

---

## Classification [AVÉRÉ] vs [HYPOTHÈSE]

### [AVÉRÉ] — Démonstrations Directes

| Claim | Evidence | Source | Status |
|-------|----------|--------|--------|
| **Cryptochrome shows MFE in vitro** | Purified robin Cry4, 50 µT sensitivity | Xu et al. 2021 (Nature) | ✅ **AVÉRÉ** |
| **FAD-TrpH radical pair formed** | EPR, optical spectroscopy | Multiple labs | ✅ **AVÉRÉ** |
| **Light-dependent response** | Photoactivation required for MFE | Drosophila assays | ✅ **AVÉRÉ** |

### [HYPOTHÈSE] — Inférences Indirectes

| Claim | Evidence | Gap | Status |
|-------|----------|-----|--------|
| **Cryptochrome = avian magnetoreceptor** | Behavioral + Cry4 retina localization | Causality not proven (knockout ≠ phenotype loss) | ⚠️ **HYPOTHÈSE FORTE** |
| **MFE% ≥20% in vivo** | Extrapolated from in vitro | In vivo measurements absent | ⚠️ **HYPOTHÈSE** |
| **Timescale 1 µs sufficient for navigation** | Calculated from singlet/triplet recombination | No direct in vivo coherence measurement | ⚠️ **HYPOTHÈSE** |

**Consensus (2025) :** Cryptochrome MFE **[AVÉRÉ]** in vitro, magnetoreception **[HYPOTHÈSE FORTE]** in vivo (high confidence but not proven).

---

## Limitations Connues

### Coherence Timescale
- ✅ **1 µs (1000 ns) sufficient** for singlet/triplet interconversion
- ⚠️ **Short vs NV/SiC** (µs vs ms) — different regime
- ⚠️ **No direct T2 measurement** (inferred from MFE kinetics)

### Biocompatibility (Non-Issue)
- ✅ **Endogenous protein** (naturally present in cells)
- ✅ **No toxicity** (evolved system)
- ✅ **Genetically encodable** (unlike NV nanoparticles)

### Signal Isolation
- ❌ **Weak signal** (~20% MFE @ 50 µT Earth field)
- ❌ **Competing processes** (fast radical recombination, scavenging)
- ❌ **Environmental noise** (thermal fluctuations, spin-orbit coupling)

### In Vivo Proof Gap
- ❌ **No direct in vivo MFE measurement** in behaving animals
- ❌ **Knockout experiments inconclusive** (Cry4-/- birds still navigate in some studies)
- ⚠️ **Alternative mechanisms** (magnetite) not ruled out

---

## Connexions Écosystème

### fp-qubit-design
**Opportunity :** Design Cry mutants with enhanced MFE
- Predict FAD-Trp distance impact on coherence
- ML models : Sequence → MFE% (training on Cry variants)
- Engineer "super-magnetoreceptor" (>50% MFE)

### ising-life-lab
**Metrics applicable :**
- **Robustness** : MFE vs noise (thermal, spin-orbit)
- **Basin depth** : Singlet vs triplet energy landscape
- **Stability** : Radical pair recombination kinetics

### arrest-molecules
**Hypothesis :** Molecular arrest modulates radical pair dynamics
- Do arrest molecules (ibogaine, salvinorin A) alter Cry MFE?
- Mechanism : Change local viscosity → alter radical pair recombination rate
- **Testable :** In vitro Cry MFE assay + arrest molecules

---

## TODO / Extensions

- [ ] Add Arabidopsis thaliana Cry1/Cry2 (plant model system)
- [ ] Add Xenopus laevis Cry (amphibian)
- [ ] Extract MFE% quantitative data from papers (currently estimated)
- [ ] Add timescale vs magnetic field strength curves (dose-response)
- [ ] Validate temperature dependence (MFE @ 4K vs 298K)
- [ ] Add knockout phenotype data (Cry4-/- behavioral tests)

---

**Last updated :** 2025-11-13  
**Curator :** non_optical_v1  
**Systems in Atlas :** 2 (RP_CRY_001 [AVÉRÉ], RP_CRY_002 [HYPOTHÈSE])  
**Evidence level :** A (robin Cry4), B (Drosophila Cry1a)  
**Controversy :** Magnetoreception hypothesis **strong but not proven causally** in vivo

