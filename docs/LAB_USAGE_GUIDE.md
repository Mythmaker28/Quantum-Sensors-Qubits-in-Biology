# Lab Usage Guide — Biological Qubits Atlas

**Date :** 2025-11-13  
**Audience :** Experimental labs using Atlas for experiment design  
**Purpose :** Practical workflows (optical + non-optical systems)

---

## Quick Start (30 Second Overview)

**Atlas contains :**
- **180 optical FP biosensors** (calcium, voltage, dopamine, etc.) — Tier 1 curated
- **23 non-optical quantum systems** (NV centers, cryptochrome, ¹³C spins, etc.) — Staging

**How to use :**
1. Identify your sensing goal (calcium? magnetic field? temperature?)
2. Filter Atlas by modality + family
3. Read family synthesis sheet (`atlas/systems_by_modality/.../families/`)
4. Select top 3 systems (contrast, temperature, in vivo compatibility)
5. Extract DOIs → Read original papers for protocols

---

## Scenario 1: Selecting a Calcium Sensor (Optical)

### Goal
Image calcium dynamics in mouse neurons in vivo

### Workflow

**Step 1: Filter Atlas**
```python
import pandas as pd

df = pd.read_csv('data/optical/curated/atlas_fp_optical_v2_2_curated.csv')
ca_sensors = df[df['family'] == 'Calcium']

print(f"Calcium sensors available: {len(ca_sensors)}")  # Output: 40
```

**Step 2: Read Family Sheet**
→ Open `atlas/systems_by_modality/optical/families/CALCIUM_SENSORS.md` (to be created)

**Step 3: Select Top 3 Based on Criteria**

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| **Contrast** | ≥10× | High SNR required for in vivo |
| **Temperature** | 298-310K | Mouse body temp = 310K |
| **In vivo flag** | 1 | Must be demonstrated in vivo |
| **Kinetics** | Rise time <50ms | Neural activity timescale |

**Top 3 :**
1. **jGCaMP8s** — 90× contrast, 298K, in vivo ✅
2. **jGCaMP8f** — 78× contrast, 298K, in vivo, faster kinetics
3. **jGCaMP7s** — 50× contrast, mature (2019), robust

**Step 4: Extract DOIs**
- jGCaMP8s : [10.xxxx/xxxxx] (from Atlas CSV)
- Read paper → Extract transfection protocol, imaging parameters

**Step 5: Implementation**
- Order plasmid (Addgene ID from paper)
- AAV packaging (if in vivo)
- Two-photon imaging (920nm excitation for depth)

---

## Scenario 2: NV Center Intracellular Thermometry (Spin Qubit)

### Goal
Measure temperature gradients in HeLa cells with mK precision

### Workflow

**Step 1: Filter Atlas**
```python
df_spin = pd.read_csv('data/non_optical/spin_qubits/staging/spin_qubit_candidates.csv')
nv_rt = df_spin[(df_spin['system_type'] == 'NV_center') & (df_spin['temperature_K'] >= 270)]

print(f"NV centers @ RT: {len(nv_rt)}")  # Output: 1 (SPIN_NV_001)
```

**Step 2: Read Family Sheet**
→ Open `atlas/systems_by_modality/spin_qubits/families/NV_CENTERS.md`

**Step 3: Select System**
- **SPIN_NV_001** — NV- center, T2 = 1800 µs @ 298K, magnetic sensitivity 130 nT/√Hz
- **DOI :** [10.1016/j.physrep.2013.02.001](https://doi.org/10.1016/j.physrep.2013.02.001) (Doherty et al. review)
- **Temperature sensing :** Demonstrated in Kucsko et al. 2013 (Nature, DOI: 10.1038/nature12373)

**Step 4: Extract Protocol**
- Read Kucsko 2013 → Extract:
  - Nanodiamond size : 50nm
  - Surface functionalization : Carboxyl groups (acid treatment)
  - Delivery : Incubation 24h, 50 µg/mL
  - ODMR setup : 532nm excitation, microwave sweep 2.8-2.9 GHz

**Step 5: Implementation**
- Order nanodiamonds (Adamas Nano, 50nm, <NV> ~10/particle)
- Functionalize surface (acid treatment, PEGylation)
- Incubate HeLa cells (24h)
- ODMR microscope (custom or commercial)
- Temperature calibration : ODMR peak shift = 74 kHz/K

**Expected result :** 1-5 mK temperature precision (single-NV level)

---

## Scenario 3: Cryptochrome Magnetoreception (Radical Pair)

### Goal
Test hypothesis: Cryptochrome 4 mediates avian magnetoreception

### Workflow

**Step 1: Filter Atlas**
```python
df_rp = pd.read_csv('data/non_optical/radical_pairs/staging/radical_pair_candidates.csv')
cry = df_rp[df_rp['protein_or_complex'].str.contains('Cryptochrome')]

print(f"Cryptochrome systems: {len(cry)}")  # Output: 2 (RP_CRY_001, RP_CRY_002)
```

**Step 2: Read Family Sheet + Evidence Grades**
→ Open `atlas/systems_by_modality/radical_pairs/families/CRYPTOCHROME.md`  
→ Open `atlas/systems_by_modality/radical_pairs/evidence_grades/RADICAL_PAIRS_AVERE_vs_HYPOTHESE.md`

**Step 3: Understand Evidence Status**
- **RP_CRY_001** (robin Cry4) : Evidence level **A** — MFE demonstrated in vitro ✅
- **In vivo magnetoreception :** **[HYPOTHÈSE FORTE]** — behavioral data strong, molecular proof incomplete

**Step 4: Extract Protocol (In Vitro MFE Assay)**
- **DOI :** [10.1038/s41586-021-03618-9](https://doi.org/10.1038/s41586-021-03618-9) (Xu et al. 2021)
- **Protein :** Purified robin Cry4 (express in E. coli, affinity purification)
- **Assay :** Flavin oxidation/reduction kinetics under 50 µT magnetic field
- **Observable :** MFE% = (Yield_50µT - Yield_0µT) / Yield_0µT × 100%
- **Expected :** MFE% ~ 20% (robin Cry4)

**Step 5: Implementation (In Vitro)**
- Clone robin Cry4 gene (GenBank from paper)
- Express in E. coli, purify (His-tag)
- Setup : LED illumination (450nm, blue light), Helmholtz coils (50 µT field)
- Measure FAD fluorescence or radical EPR signal
- Compare: 0 µT (control) vs 50 µT (test)

**Step 6: In Vivo Test (Advanced)**
- Knockout robin Cry4 (CRISPR, if ethical approval)
- Test migratory orientation behavior (autumn migration assays)
- Compare: Wild-type vs Cry4-/- birds
- **Expected :** If Cry4 = magnetoreceptor, Cry4-/- birds show disorientation

**Status :** In vivo test **not yet conclusive** (some Cry4-/- birds still navigate, alternative mechanisms possible)

---

## Scenario 4: ¹³C-NV Hybrid Qubit (Nuclear Spin)

### Goal
Implement quantum memory at room temperature using ¹³C nuclear spins coupled to NV electron spin

### Workflow

**Step 1: Filter Atlas**
```python
df_nuc = pd.read_csv('data/non_optical/nuclear_spins/staging/nuclear_spin_candidates.csv')
c13_nv = df_nuc[(df_nuc['nucleus'] == '13C') & (df_nuc['temperature_K'] >= 270)]

print(f"13C-NV @ RT: {len(c13_nv)}")  # Output: 1 (NUC_13C_001)
```

**Step 2: Read Family Sheet**
→ Open `atlas/systems_by_modality/nuclear_spins/families/NV_COUPLED_SPINS.md`

**Step 3: Extract Parameters**
- **NUC_13C_001** — T2 = 1000 ms (1 s) @ 298K, coupling = 130 kHz
- **DOI :** [10.1103/PhysRevLett.109.137602](https://doi.org/10.1103/PhysRevLett.109.137602) (Maurer et al. 2012)
- **Method :** Dynamical decoupling (XY-8 sequence)

**Step 4: Extract Protocol**
- Read Maurer 2012 → Extract:
  - Diamond : ¹³C-enriched (>1% natural abundance, or 99% enriched)
  - NV creation : Nitrogen implantation + annealing
  - ¹³C identification : ODMR spectroscopy (hyperfine splitting)
  - DD sequence : XY-8-N (N=128, τ=200µs)
  - Control : NV microwave pulses (π, π/2) + ¹³C selective RF pulses

**Step 5: Implementation**
- **Diamond sample :** Element Six, ¹³C-enriched (or natural ~1%)
- **NV creation :** Ion implantation (¹⁵N @10keV) + anneal 800°C
- **ODMR setup :** Confocal microscope, 532nm laser, microwave antenna
- **DD protocol :** Program XY-8 sequence, optimize τ (inter-pulse delay)
- **¹³C readout :** Measure NV fluorescence (¹³C state imprinted on NV)

**Expected result :** T2 = 1s @ RT (matches Atlas NUC_13C_001)

---

## Scenario 5: SiC Defect Biocompatibility Test (Spin Qubit)

### Goal
Validate VSi in 4H-SiC nanoparticles for in cellulo sensing (NIR advantage over NV)

### Workflow

**Step 1: Filter Atlas**
```python
df_spin = pd.read_csv('data/non_optical/spin_qubits/staging/spin_qubit_candidates.csv')
sic_rt = df_spin[(df_spin['system_type'] == 'SiC_defect') & (df_spin['temperature_K'] >= 270)]

print(f"SiC defects @ RT: {len(sic_rt)}")  # Output: 1 (SPIN_SIC_001)
```

**Step 2: Read Family Sheet**
→ Open `atlas/systems_by_modality/spin_qubits/families/SIC_DEFECTS.md`

**Step 3: Extract Parameters**
- **SPIN_SIC_001** — VSi in 4H-SiC, T2 = 160 µs @ 298K, ODMR-controlled
- **DOI :** [10.1038/nmat4145](https://doi.org/10.1038/nmat4145) (Widmann et al. 2015)
- **Advantage :** NIR emission (900nm) → better tissue penetration than NV (637nm)

**Step 4: Design Biocompatibility Experiment**
- **Nanoparticle prep :** Mill bulk 4H-SiC → <100nm particles (ball milling)
- **Surface chemistry :** Functionalize (PEG-silane, amine groups)
- **Cytotoxicity :** MTT assay (HeLa cells, 24h/48h/72h, dose 1-100 µg/mL)
- **Uptake :** Confocal imaging (SiC autofluorescence ~900nm)
- **ODMR in cellulo :** Measure VSi T2 inside cells (compare to in vitro baseline)

**Expected result :**
- Cytotoxicity : Low (<100nm particles, similar to NV)
- T2 degradation : 160 µs (in vitro) → 10-50 µs (in cellulo, estimated)

**Gap :** **Not demonstrated as of 2025** — SiC nanoparticles in cells = open research question

---

## Quick Reference — System Selection

| Goal | Modality | Recommended System | Atlas ID | DOI |
|------|----------|-------------------|----------|-----|
| **Calcium imaging (in vivo)** | Optical | jGCaMP8s | FP_xxxx | atlas_fp_optical_v2_2_curated.csv |
| **Magnetic field sensing** | Spin (NV) | NV- center @ RT | SPIN_NV_001 | 10.1016/j.physrep.2013.02.001 |
| **Temperature sensing (mK)** | Spin (NV) | NV- center @ RT | SPIN_NV_001 | 10.1038/nature12373 (Kucsko 2013) |
| **Magnetoreception test** | Radical pair | Cryptochrome 4 (robin) | RP_CRY_001 | 10.1038/s41586-021-03618-9 |
| **Quantum memory @ RT** | Nuclear (¹³C-NV) | ¹³C coupled to NV | NUC_13C_001 | 10.1103/PhysRevLett.109.137602 |
| **NIR imaging (deep tissue)** | Spin (SiC) | VSi in 4H-SiC | SPIN_SIC_001 | 10.1038/nmat4145 |

---

## Advanced Workflows

### Workflow A: Compare NV vs FP for Intracellular Sensing
**Decision tool :** Read `atlas/comparative_notes_cross_modality/NV_vs_FP_intracellular.md`

**Summary :**
- **FP dominates** : Genetic encoding, high contrast (90×), mature protocols
- **NV niche** : Magnetic field (no FP alternative), nanoscale resolution

### Workflow B: Validate Radical Pair Hypothesis
**Decision tool :** Read `atlas/systems_by_modality/radical_pairs/evidence_grades/RADICAL_PAIRS_AVERE_vs_HYPOTHESE.md`

**Summary :**
- **[AVÉRÉ]** : Cryptochrome MFE in vitro (robin Cry4)
- **[HYPOTHÈSE]** : Cryptochrome = in vivo magnetoreceptor (probable but not proven)

### Workflow C: Design Hybrid Qubit Experiment
**Decision tool :** Read `atlas/systems_by_modality/nuclear_spins/families/NV_COUPLED_SPINS.md`

**Summary :**
- **¹³C-NV** : T2 = 1s @ RT, quantum memory demonstrated
- **¹⁴N-NV** : T2 = 3ms @ RT, intrinsic (no isotope engineering)
- **Choice :** ¹³C for long memory, ¹⁴N for convenience

---

## Limitations & Disclaimers

### Non-Optical Systems (Early-Stage)

⚠️ **23 non-optical systems in staging** (not Tier 1 curated yet)  
⚠️ **Biocompatibility data sparse** (SiC nanoparticles not fully characterized)  
⚠️ **In vivo demonstrations limited** (NV : few, SiC : none, radical pairs : indirect)

**Recommendation :** Non-optical = research-grade, **not clinical-grade** (vs optical FP = mature)

### Evidence Levels

- **A** : Peer-reviewed, reproducible, direct measurement → **Trust high**
- **B** : Peer-reviewed, indirect inference → **Trust moderate, verify**
- **C** : Preprint, single-lab → **Trust low, replicate before use**

### Radical Pairs (Controversy)

⚠️ **Quantum biology field controversial** (magnetoreception, photosynthesis coherence)  
⚠️ **[AVÉRÉ] ≠ [HYPOTHÈSE]** : Read evidence grades document before citing

---

## Contact & Support

**Questions about protocols :**
- Open [GitHub Issue](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues) with label `lab-usage`
- Email : tommy.lepesteur@hotmail.fr

**Report experimental results :**
- Use [Data Fix template](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues/new?template=data_fix.yml) if Atlas data incorrect
- Use [New Entry template](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues/new?template=new_entry.yml) to add new systems

---

**Last updated :** 2025-11-13  
**Version :** 1.0 (MVP)  
**Feedback welcome** : Labs using this guide, please share successes/failures to improve documentation

