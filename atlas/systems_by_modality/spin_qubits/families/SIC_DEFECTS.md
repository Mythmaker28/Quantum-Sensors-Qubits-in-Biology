# SiC Defects (Silicon Carbide Vacancies) — État de l'Art

## Systèmes Catalogués dans Atlas

| ID | Label | Defect Type | Polytype | Temperature | T2 | T1 | Method | Evidence | DOI |
|----|-------|-------------|----------|-------------|----|----|--------|----------|-----|
| **SPIN_SIC_001** | VSi 4H-SiC | Silicon vacancy | 4H | 298K | **160 µs** | — | ODMR | A | [10.1038/nmat4145](https://doi.org/10.1038/nmat4145) |
| **SPIN_SIC_002** | Divacancy 4H-SiC | Divacancy (neutral) | 4H | 20K | — | 1000 µs | pulsed ESR | A | [10.1103/PhysRevLett.112.187601](https://doi.org/10.1103/PhysRevLett.112.187601) |

**Top performer :** SPIN_SIC_001 (RT) — T2 = 160 µs @ 298K, **ODMR-controlled**

---

## Paramètres Critiques

| Parameter | VSi (4H) @ RT | Divacancy (4H) @ 20K | Unit |
|-----------|---------------|----------------------|------|
| **T2 (coherence)** | 160 µs | — | µs |
| **T1 (relaxation)** | — | 1000 µs (1 ms) | µs |
| **Measurement method** | ODMR | pulsed ESR | — |
| **Polytype** | 4H-SiC | 4H-SiC | — |
| **Defect charge** | VSi (silicon vacancy) | VV⁰ (neutral divacancy) | — |
| **Optical readout** | Yes (NIR ~900nm) | Limited | — |

**Key advantage over NV :** NIR emission (900-1000nm) → **better tissue penetration** than NV (637nm)

---

## Top 3 Papers Clés

### 1. Widmann et al. (2015) — Nature Materials
**DOI :** [10.1038/nmat4145](https://doi.org/10.1038/nmat4145)  
**Breakthrough :** Room-temperature ODMR control of VSi in 4H-SiC  
**Key result :** T2 = 160 µs @ 298K, optically active spin-3/2 ground state

### 2. Falk et al. (2013) — Nature Communications
**DOI :** [10.1038/ncomms2854](https://doi.org/10.1038/ncomms2854)  
**Breakthrough :** Polytype-dependent optical properties (4H vs 6H-SiC)  
**Key result :** V1/V2 site splitting in 4H, kk/hh in 6H

### 3. Fuchs et al. (2015) — Nature Communications
**DOI :** [10.1038/ncomms8578](https://doi.org/10.1038/ncomms7578)  
**Breakthrough :** Divacancy spin coherence, coupling to nuclear spins  
**Key result :** T2 > 1ms @ cryogenic, hybrid qubit potential

---

## Applications Démontrées

### ✅ In Vitro
- **Magnetic field sensing** (similar to NV, NIR advantage)
- **Temperature sensing** (>mK precision possible)
- **Electric field sensing** (Stark shift measurements)

### ⚠️ In Cellulo
- **Limited demonstrations** (SiC nanoparticles biocompatibility under study)
- **Advantage :** NIR emission → deeper tissue penetration vs NV
- **Challenge :** Surface functionalization protocols less mature than diamond

### ❌ In Vivo
- **No demonstrations yet** (as of 2025)
- **Potential :** Better than NV for deep-tissue imaging (NIR window)
- **Toxicity :** SiC biocompatible (FDA-approved for implants), but nanoparticle form under study

---

## Limitations Connues

### Coherence
- ✅ **T2 @ RT (160 µs) decent**, but 10× shorter than NV (1800 µs)
- ⚠️ **Mechanism :** Faster phonon decoherence in SiC vs diamond
- ⚠️ **Mitigation :** Isotopic purification (²⁸Si, ¹²C)

### Optical Properties
- ✅ **NIR emission (900-1000nm)** — biological window II (750-1350nm)
- ⚠️ **Quantum efficiency lower** than NV (~10% vs 70%)
- ⚠️ **Multiple polytype sites** (V1/V2 in 4H, kk/hh in 6H) → spectral complexity

### Biocompatibility (Unknown)
- ⚠️ **SiC nanoparticles cytotoxicity not fully characterized**
- ⚠️ **Surface chemistry immature** (vs well-developed diamond functionalization)
- ✅ **Bulk SiC biocompatible** (used in medical implants)

### Fabrication
- ✅ **Wafer-scale production** (vs diamond limited to HPHT/CVD)
- ✅ **CMOS-compatible** (integration with electronics easier than diamond)
- ⚠️ **Defect creation control** less mature than NV (implantation/annealing optimization ongoing)

---

## Polytype Comparison (Design Choice)

| Polytype | Sites | Optical Lines | Coherence | Status |
|----------|-------|---------------|-----------|--------|
| **4H-SiC** | V1, V2 | 862nm (V2), 917nm (V1) | T2~160µs (V2) | **Most studied** |
| **6H-SiC** | kk, hh | ~900nm (varies) | T2 data sparse | Research-grade |
| **3C-SiC** | — | ~700nm | T2 << 4H/6H | Less suitable |

**Recommendation :** Focus 4H-SiC V2 site for Atlas curation (best characterized).

---

## Connexions Écosystème

### fp-qubit-design
**Opportunity :** Design SiC nanoparticle surface chemistry
- Predict biocompatibility vs functionalization (PEG, peptides)
- ML models : Polytype (4H/6H) → optical properties

### ising-life-lab
**Metrics applicable :**
- **Robustness** : T2 vs polytype, isotopic purity
- **Stability** : Defect charge state metastability (VSi vs VSi⁻)
- **Coherence landscapes** : Compare 4H vs 6H vs 3C

### arrest-molecules
**Hypothesis :** SiC defects in biological "arrest" states
- Do molecular dampeners modulate SiC T2 via local electric fields?
- Comparative study : NV vs SiC sensitivity to arrest molecules

---

## TODO / Extensions

- [ ] Add 4H-SiC V1 site (complementary to V2, different optical line)
- [ ] Add 6H-SiC kk/hh sites (if T2 data available)
- [ ] Add 3C-SiC defects (for completeness, even if inferior)
- [ ] Extract T2 vs temperature for VSi (4K → 298K sweep)
- [ ] Add divacancy variants (charged states VV⁻, VV⁺)
- [ ] Validate nanoparticle biocompatibility (literature mining)

---

**Last updated :** 2025-11-13  
**Curator :** non_optical_v1  
**Systems in Atlas :** 2 (SPIN_SIC_001, SPIN_SIC_002)  
**Evidence level :** A (peer-reviewed, reproducible)  
**Advantage :** NIR emission → better tissue penetration than NV

