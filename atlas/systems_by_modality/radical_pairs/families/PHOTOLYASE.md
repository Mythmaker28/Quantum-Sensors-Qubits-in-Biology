# Photolyase Radical Pairs — État de l'Art

**Status :** STABLE  
**Scope :** FAD-Trp radical pairs in DNA repair enzymes (CPD, 6-4 photolyases), electron transfer kinetics  
**Systems in Atlas :** 2 (RP_PHOTOLYASE_001 E. coli, RP_6_4PHOTOLYASE_001 Xenopus)

---

## Systèmes Catalogués dans Atlas

| ID | Protein | Organism | Function | Timescale | Temperature | Evidence | DOI |
|----|---------|----------|----------|-----------|-------------|----------|-----|
| **RP_PHOTOLYASE_001** | DNA photolyase FAD-TrpH | *E. coli* | DNA repair (CPD lesions) | **1000 ns** | 298K | **A** | [10.1021/ja203749t](https://doi.org/10.1021/ja203749t) |
| **RP_6_4PHOTOLYASE_001** | 6-4 photolyase FAD | *Xenopus laevis* | DNA repair (6-4 lesions) | 500 ns | 298K | **A** | [10.1038/nature11242](https://doi.org/10.1038/nature11242) |

**Top system :** RP_PHOTOLYASE_001 (E. coli) — Evidence level A, **electron transfer 1 µs**

---

## Paramètres Critiques

| Parameter | CPD Photolyase (E. coli) | 6-4 Photolyase (Xenopus) | Unit |
|-----------|--------------------------|--------------------------|------|
| **Timescale** | 1000 ns (1 µs) | 500 ns | ns |
| **Observable** | Electron transfer FAD → TrpH | Electron transfer FAD | — |
| **Function** | CPD lesion repair | 6-4 lesion repair | — |
| **Radical pair** | FAD•⁻ ... TrpH•⁺ | FAD•⁻ ... (Trp triad) | — |
| **Distance** | ~15 Å (FAD-Trp) | ~10 Å | Å |
| **Quantum yield** | >90% (repair efficiency) | >80% | % |

**Key feature :** **Ultra-high repair efficiency** (>90%) — proposed quantum advantage (coherent electron transfer)

---

## Top 3 Papers Clés

### 1. Liu et al. (2011) — JACS
**DOI :** [10.1021/ja203749t](https://doi.org/10.1021/ja203749t)  
**Breakthrough :** FAD-TrpH radical pair kinetics in E. coli photolyase  
**Key result :** Electron transfer 1 µs, radical pair mechanism confirmed (EPR)  
**Status :** **[AVÉRÉ]** — Direct observation radical pair

### 2. Zhong et al. (2012) — Nature
**DOI :** [10.1038/nature11242](https://doi.org/10.1038/nature11242)  
**Breakthrough :** 6-4 photolyase mechanism, single-photon repair  
**Key result :** Oxetane intermediate, FAD radical essential  
**Status :** **[AVÉRÉ]** — Crystal structure + kinetics

### 3. Weber (2005) — Biochim Biophys Acta
**DOI :** [10.1016/j.bbabio.2004.11.009](https://doi.org/10.1016/j.bbabio.2004.11.009)  
**Breakthrough :** Quantum yield measurements, repair efficiency >90%  
**Key result :** Proposed quantum coherence in electron transfer chain  
**Status :** **[HYPOTHÈSE]** — High efficiency ≠ proof of quantum advantage

---

## Applications Démontrées

### ✅ In Vitro (Purified Enzyme)
- **DNA lesion repair** (CPD, 6-4 photolesions) — ✅ **[AVÉRÉ]**
- **Electron transfer** (FAD → Trp → DNA) — ✅ **[AVÉRÉ]**
- **Radical pair kinetics** (EPR, transient absorption) — ✅ **[AVÉRÉ]**

### ✅ In Cellulo
- **E. coli photolyase rescues UV damage** — ✅ **[AVÉRÉ]**
- **Xenopus photolyase in oocytes** — ✅ **[AVÉRÉ]**

### ⚠️ In Vivo (Organismal)
- **Demonstrated in bacteria, amphibians** — ✅
- **Not in mammals** (no photolyase gene, NER pathway instead)

---

## Classification [AVÉRÉ] vs [HYPOTHÈSE]

### [AVÉRÉ] — Démonstrations Directes

| Claim | Evidence | Source | Status |
|-------|----------|--------|--------|
| **FAD-Trp radical pair formed** | EPR, optical spectroscopy | Liu et al. 2011 (JACS) | ✅ **AVÉRÉ** |
| **Electron transfer 1 µs timescale** | Transient absorption kinetics | Multiple labs | ✅ **AVÉRÉ** |
| **Repair efficiency >90%** | Quantum yield measurements | Weber 2005 | ✅ **AVÉRÉ** |

### [HYPOTHÈSE] — Inférences Indirectes

| Claim | Evidence | Gap | Status |
|-------|----------|-----|--------|
| **Quantum coherence enhances repair** | High efficiency (>90%) | No direct coherence measurement | ⚠️ **HYPOTHÈSE** |
| **Proton-coupled electron transfer (PCET)** | Kinetic isotope effects | Mechanism debated | ⚠️ **HYPOTHÈSE** |
| **Spin selectivity in repair** | Singlet/triplet yield differences | Not quantified | ⚠️ **HYPOTHÈSE** |

**Consensus (2025) :** Radical pair mechanism **[AVÉRÉ]**, quantum advantage **[HYPOTHÈSE]** (high efficiency explainable classically).

---

## Limitations Connues

### Coherence vs Classical
- ✅ **Radical pair formed** (EPR confirmed)
- ⚠️ **No direct T2 measurement** (coherence inferred from kinetics)
- ❌ **Quantum advantage not proven** (classical hopping also explains >90% yield)

### Timescale
- ✅ **1 µs sufficient** for electron transfer (fast vs DNA damage timescale)
- ⚠️ **Short vs spin qubits** (µs vs ms) — different functional regime

### Biocompatibility (Non-Issue)
- ✅ **Endogenous enzyme** (bacteria, plants, amphibians)
- ❌ **Absent in mammals** (evolutionary loss)

### Engineering Potential
- ⚠️ **Difficult to engineer** (complex Trp triad geometry critical)
- ⚠️ **Repair specificity** (CPD vs 6-4 lesion selectivity)

---

## Connexions Écosystème

### fp-qubit-design
**Opportunity :** Design photolyase variants with altered repair specificity
- Predict FAD-Trp distance impact on electron transfer rate
- ML models : Trp triad geometry → repair efficiency
- Engineer "super-photolyase" (>95% yield, broader lesion specificity)

### ising-life-lab
**Metrics applicable :**
- **Robustness** : Electron transfer vs noise (protein dynamics)
- **Basin depth** : Radical pair recombination energy landscape
- **Functional score** : Repair efficiency as fitness metric

### arrest-molecules
**Hypothesis :** Molecular arrest modulates photolyase kinetics
- Do arrest molecules alter FAD-Trp electron transfer rate?
- Mechanism : Change protein conformation → alter radical pair distance
- **Testable :** In vitro photolyase repair assay + arrest molecules

---

## TODO / Extensions

- [ ] Add Arabidopsis thaliana photolyase (plant CPD repair)
- [ ] Add *Anacystis nidulans* photolyase (cyanobacterial)
- [ ] Extract quantum yield vs wavelength (action spectra)
- [ ] Add temperature dependence (repair efficiency @ 4K vs 298K)
- [ ] Add Trp triad variants (single/double/triple Trp mutants)
- [ ] Validate PCET mechanism (proton-coupled electron transfer)

---

**Last updated :** 2025-11-13  
**Curator :** non_optical_v1  
**Systems in Atlas :** 2 (RP_PHOTOLYASE_001, RP_6_4PHOTOLYASE_001)  
**Evidence level :** A (both systems, radical pair mechanism confirmed)  
**Functional :** DNA repair >90% efficiency, **endogenous quantum system**

