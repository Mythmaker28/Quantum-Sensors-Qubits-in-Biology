# Extended Qubits Schema — Non-Optical Systems

## Purpose

This document defines data schemas for **non-optical qubit systems** used in biological contexts or quantum sensing applications. These systems are strictly separated from the optical fluorescent protein atlas (Tier1/Tier2/Tier3).

**Important:** Non-optical qubits live in separate CSV files and are NOT mixed with optical FP systems.

---

## Version

- **Created:** 2025-11-10
- **Schema version:** 1.0.0
- **Applies to:** Non-optical qubit candidates

---

## Design Principles

1. **Separation from optical atlas:**
   - Optical FP systems remain in `data/processed/atlas_fp_optical_v2_2*.csv`
   - Non-optical systems use distinct CSVs in `data/staging/`
   - No cross-contamination between modalities

2. **No fabrication policy:**
   - All entries require verifiable DOI
   - All entries require at least one quantitative observable (T2, coherence time, field sensitivity, reaction yield)
   - Unknown values remain empty (no guessing)

3. **Evidence levels:**
   - **A:** Peer-reviewed, reproducible, direct measurement
   - **B:** Peer-reviewed, indirect inference or theoretical model
   - **C:** Preprint, preliminary, or single-lab result

---

## Table 1: Spin Qubits (`spin_qubit_candidates.csv`)

### Scope

Solid-state defect qubits, molecular spin systems, and other spin-based quantum sensors relevant to biology or bio-compatible materials.

**Examples:**
- NV- centers in diamond
- Silicon vacancy (VSi) defects in SiC
- Molecular spin qubits (e.g., endohedral fullerenes)
- Electron spin resonance (ESR) active species

### Schema

| Column | Type | Unit | Description | Required |
|--------|------|------|-------------|----------|
| `id` | string | - | Unique identifier (e.g., SPIN_0001) | **Yes** |
| `label` | string | - | Human-readable name (e.g., "NV- in diamond") | **Yes** |
| `system_type` | string | - | Category: NV_center, SiC_defect, molecular_spin, endohedral_fullerene, etc. | **Yes** |
| `host_material` | string | - | Host matrix (diamond, SiC, protein, etc.) | **Yes** |
| `T2_microseconds` | float | µs | Coherence time T2 | Recommended* |
| `T2_star_microseconds` | float | µs | Dephasing time T2* (if reported separately) | Optional |
| `T1_microseconds` | float | µs | Relaxation time T1 | Optional |
| `temperature_K` | float | K | Measurement temperature | Recommended* |
| `measurement_method` | string | - | Technique: ODMR, EPR, pulsed_ESR, Ramsey, Hahn_echo, etc. | **Yes** |
| `magnetic_sensitivity_nT_rtHz` | float | nT/√Hz | Magnetic field sensitivity (if applicable) | Optional |
| `doi` | string | - | DOI of primary source | **Yes** |
| `evidence_level` | string | - | A, B, or C (see above) | **Yes** |
| `curator` | string | - | Curation source (e.g., "manual_v1.0", "auto_harvest_v1") | **Yes** |
| `notes` | string | - | Additional context or caveats | Optional |

**\*Recommended:** Strongly encouraged but may be empty if data unavailable in source.

### Validation Rules

- `system_type` must be from controlled vocabulary (extendable)
- `T2_microseconds` > 0 if present
- `temperature_K` in range [4, 400] K (cryogenic to physiological)
- `doi` must match DOI format (10.XXXX/...)
- `evidence_level` must be A, B, or C

---

## Table 2: Radical Pair Qubits (`radical_pair_candidates.csv`)

### Scope

Radical pair mechanisms in biological systems, including cryptochrome, photolyase, and other light-activated electron transfer systems with potential quantum coherence.

**Examples:**
- Cryptochrome radical pairs (avian magnetoreception)
- Photosystem II radical pairs
- Flavin-based radical pairs

### Schema

| Column | Type | Unit | Description | Required |
|--------|------|------|-------------|----------|
| `id` | string | - | Unique identifier (e.g., RP_0001) | **Yes** |
| `protein_or_complex` | string | - | Protein name or complex (e.g., "Cryptochrome-1a", "PSII") | **Yes** |
| `organism` | string | - | Source organism (if known) | Recommended* |
| `observable` | string | - | What was measured: reaction_yield, MFE, anisotropy, singlet_yield, etc. | **Yes** |
| `timescale_ns` | float | ns | Coherence or reaction timescale (if reported) | Recommended* |
| `field_sensitivity_uT` | float | µT | Magnetic field effect threshold (if reported) | Optional |
| `mfe_percent` | float | % | Magnetic field effect magnitude (if applicable) | Optional |
| `temperature_K` | float | K | Measurement temperature | Recommended* |
| `doi` | string | - | DOI of primary source | **Yes** |
| `evidence_level` | string | - | A, B, or C | **Yes** |
| `curator` | string | - | Curation source | **Yes** |
| `notes` | string | - | Additional context | Optional |

**\*Recommended:** Strongly encouraged but may be empty if data unavailable.

### Validation Rules

- `observable` must describe a measurable quantity
- `timescale_ns` > 0 if present
- `field_sensitivity_uT` > 0 if present
- `mfe_percent` typically in range [0, 100]
- `temperature_K` in range [4, 400] K
- `doi` must match DOI format

---

## Table 3: Nuclear Spin Qubits (`nuclear_spin_candidates.csv`)

### Scope

Nuclear spin systems used as qubits or quantum sensors in biological or bio-compatible contexts.

**Examples:**
- 13C nuclear spins in diamond (coupled to NV centers)
- 31P nuclear spins in phosphorus donors
- Endogenous nuclear spins in proteins (NMR-detected coherence)

### Schema

| Column | Type | Unit | Description | Required |
|--------|------|------|-------------|----------|
| `id` | string | - | Unique identifier (e.g., NUC_0001) | **Yes** |
| `nucleus` | string | - | Nuclear isotope (e.g., 13C, 15N, 31P, 1H) | **Yes** |
| `host` | string | - | Host material or protein | **Yes** |
| `system_type` | string | - | Context: diamond_NV_coupled, donor_spin, protein_NMR, etc. | **Yes** |
| `T2_milliseconds` | float | ms | Coherence time T2 | Recommended* |
| `T1_milliseconds` | float | ms | Relaxation time T1 | Optional |
| `temperature_K` | float | K | Measurement temperature | Recommended* |
| `measurement_method` | string | - | Technique: NMR, DNP, ENDOR, etc. | **Yes** |
| `coupling_strength_Hz` | float | Hz | Hyperfine coupling (if applicable) | Optional |
| `doi` | string | - | DOI of primary source | **Yes** |
| `evidence_level` | string | - | A, B, or C | **Yes** |
| `curator` | string | - | Curation source | **Yes** |
| `notes` | string | - | Additional context | Optional |

**\*Recommended:** Strongly encouraged but may be empty if data unavailable.

### Validation Rules

- `nucleus` must be valid isotope notation
- `T2_milliseconds` > 0 if present
- `temperature_K` in range [4, 400] K
- `doi` must match DOI format
- `evidence_level` must be A, B, or C

---

## Relationship to Optical Atlas

**Completely separate:**

- Optical fluorescent proteins (FPs) and biosensors → `data/processed/atlas_fp_optical_v2_2*.csv`
- Non-optical qubits → `data/staging/*_qubit_candidates.csv`

**No overlap:**
- A system is EITHER optical (uses fluorescence readout) OR non-optical (spin/magnetic/nuclear readout)
- If a system uses both modalities (e.g., NV center = optical readout of spin state), classify by PRIMARY readout mechanism in the biological context
- When in doubt, document separately in both schemas with clear cross-reference notes

---

## Data Quality Policy

### Entry Requirements (Minimum Bar)

To add a system to ANY non-optical qubit table, you MUST have:

1. ✅ Valid DOI to peer-reviewed or preprint source
2. ✅ At least ONE quantitative observable:
   - For spin qubits: T2, T1, T2*, or magnetic sensitivity
   - For radical pairs: timescale, magnetic field effect, or reaction yield change
   - For nuclear spins: T2, T1, or coupling strength
3. ✅ Clear system identification (host material, protein name, nucleus)
4. ✅ Measurement method documented

### Forbidden Practices

❌ **Never fabricate:**
- DOI or references
- Numerical values (T2, temperature, sensitivity)
- System classifications

❌ **Never guess:**
- If temperature not reported → leave empty
- If T2 not measured → leave empty
- If evidence level unclear → mark as C (preliminary) and note in `notes` field

---

## Curation Workflow

### For New Entries

1. Identify candidate system from literature
2. Verify DOI is valid and accessible
3. Extract quantitative observables from paper
4. Fill required + recommended fields (leave unknowns empty)
5. Assign evidence level based on publication type and reproducibility
6. Add to appropriate staging CSV
7. Log entry in curation notes

### Promotion to "Curated" Status

Future work may define a promotion pathway similar to optical Tier1/Tier2/Tier3. For now:
- All non-optical systems remain in `staging/` until validation workflows established
- Each entry is individually traceable via DOI

**Tier1-ready candidates (conceptual, not yet promoted):**

Criteria for Tier1 (curated, modeling-ready):
1. Evidence level A (peer-reviewed, direct measurement)
2. At least ONE quantitative observable (T2, T1, timescale, field sensitivity)
3. Measurement method documented
4. Temperature specified OR system is temperature-independent

**Spin qubits meeting Tier1 criteria:** 7/7 systems
- SPIN_NV_001, SPIN_NV_002, SPIN_SIC_001, SPIN_SIC_002 (all have T2 or T1 + temp)
- SPIN_SIV_001, SPIN_P1_001, SPIN_FULLERENE_001 (all have quantitative data)

**Radical pairs meeting Tier1 criteria:** 3/5 systems
- RP_CRY_001 (A, timescale + field sensitivity + temp)
- RP_PHOTOLYASE_001 (A, timescale + temp)
- RP_BChl_001 (A, timescale + temp)
- Note: RP_CRY_002 (B, review), RP_PSII_001 (B, indirect) remain in staging

**Nuclear spins meeting Tier1 criteria:** 5/5 systems
- All have evidence level A, T2/T1 data, and temperature specified

**Total Tier1-ready:** 15/17 systems (88%)

**Action:** Keeping all in staging/ for now. Formal promotion requires:
- Written Tier1/Tier2/Tier3 criteria document
- Automated promotion script
- External validation/review

---

## Versioning

- **v1.2.0 (2025-11-10):** Extended curation with additional well-documented systems
  - 3 tables maintained: spin_qubits, radical_pair_qubits, nuclear_spin_qubits
  - **23 validated systems** (9 spin + 7 radical pairs + 7 nuclear)
  - All entries have DOI, measurement_method, evidence_level
  - Validation: `scripts/qa/validate_non_optical.py` passes with 0 errors, 0 warnings
  - New additions (v1.2): GeV/SnV centers, mitochondrial/photolyase radicals, 15N/1H nuclear spins
  - 20/23 systems (87%) meet conceptual Tier1 criteria (evidence_level A, quantitative data)

- **v1.1.0 (2025-11-10):** Extended curation with well-documented systems
  - 17 validated systems (7 spin + 5 radical pairs + 5 nuclear)
  - 15/17 systems (88%) meet conceptual Tier1 criteria
  
- **v1.0.0 (2025-11-10):** Initial schema definition + baseline curation
  - 10 systems (4 spin + 3 radical pairs + 3 nuclear)

---

## References

### Spin Qubits
- Doherty et al. (2013) "The nitrogen-vacancy colour centre in diamond" *Physics Reports* 528:1-45. DOI: 10.1016/j.physrep.2013.02.001
- Widmann et al. (2015) "Coherent control of single spins in silicon carbide" *Nature Materials* 14:164-168. DOI: 10.1038/nmat4145

### Radical Pairs
- Hore & Mouritsen (2016) "The Radical-Pair Mechanism of Magnetoreception" *Annual Review of Biophysics* 45:299-344. DOI: 10.1146/annurev-biophys-032116-094545
- Xu et al. (2021) "Magnetic sensitivity of cryptochrome 4 from a migratory songbird" *Nature* 594:535-540. DOI: 10.1038/s41586-021-03618-9

### Nuclear Spins
- Taminiau et al. (2012) "Detection and Control of Individual Nuclear Spins Using a Weakly Coupled Electron Spin" *Physical Review Letters* 109:137602. DOI: 10.1103/PhysRevLett.109.137602

---

**Curator:** atlas_maintainer_v1.0  
**Contact:** [GitHub Issues](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues)  
**See also:** `docs/DATA_TIERS.md` (optical systems), `docs/ATLAS_SPEC.md` (optical schema)

