# Data Tiering Specification

## Purpose

The atlas contains systems from multiple sources with varying quality levels. This document defines explicit tiers to separate **curated, modeling-ready data** from **staging candidates** and **unusable placeholders**.

## Version

Applies to: Atlas v2.2.2+ (296 total systems as of 2025-11-10)

---

## Tier Definitions

### Tier 1: CURATED_CORE (Modeling-Ready)

**Criteria (ALL must be met):**
1. `family != "Unknown"` — Target/function is known
2. `doi` is present — Verifiable source
3. **AT LEAST ONE** of:
   - `excitation_nm` is present, OR
   - `emission_nm` is present, OR
   - `contrast_normalized > 1.5` (non-placeholder value)

**Purpose:**  
High-confidence systems suitable for:
- Machine learning / predictive modeling
- Quantitative analysis
- Direct experimental use

**Expected count:** ~180-193 systems

**File:** `data/processed/atlas_fp_optical_v2_2_curated.csv`

---

### Tier 2: CANDIDATES_STAGING (Incomplete but Real)

**Criteria:**
1. `doi` is present — Has verifiable source
2. `family != "Unknown"` — Target is known
3. **Does NOT meet Tier 1 criteria** (missing spectral + low/placeholder contrast)

**Characteristics:**
- Real systems from literature/databases
- Incomplete metadata (e.g., no reported excitation/emission wavelengths)
- May have `contrast_normalized = 1.0` if no dynamic range reported in source

**Purpose:**  
Manual curation queue:
- Requires literature review to fill missing fields
- Can be promoted to Tier 1 after verification
- NOT recommended for automated modeling

**Expected count:** ~13 systems

**File:** `data/staging/atlas_fp_optical_v2_2_candidates.csv`

---

### Tier 3: UNKNOWN/NOISY (Placeholder Systems)

**Criteria (ANY triggers inclusion):**
1. `family == "Unknown"` — Function/target unclear
2. `doi` is missing — No verifiable source
3. **Placeholder triple:**
   - `contrast_normalized == 1.0` (exactly) AND
   - `excitation_nm` is missing AND
   - `emission_nm` is missing

**Characteristics:**
- Auto-harvested from APIs (UniProt, FPbase)
- No usable metadata for modeling
- Often generic fluorescent proteins without sensing function
- Contrast set to 1.0 as conservative default (not measured)

**Source breakdown:**
- 77 systems from `deep_harvest_uniprot_deep` (UniProt API)
- 26 systems from `api_harvest_fpbase_csv` (FPbase CSV)

**Purpose:**  
Isolation zone:
- NOT counted in official "N systems" for modeling
- Kept for transparency/auditability
- May be reviewed manually later

**Expected count:** ~103 systems

**File:** `data/staging/atlas_fp_optical_v2_2_unknown.csv`

---

## Quality Assurance

### Validation Rules

**Tier 1 (strict):**
- 0 critical errors allowed
- All required fields present
- `scripts/validate_atlas.py --tier curated` must pass

**Tier 2 (moderate):**
- DOI + family required
- Spectral/contrast can be missing (documented)
- Warnings allowed

**Tier 3 (permissive):**
- Any structure accepted
- Reported separately for transparency

### Non-Destructive Guarantee

- **NO systems deleted** — all 296 systems preserved
- Original file `atlas_fp_optical_v2_2.csv` kept as "raw mixed" view
- All tiers programmatically reproducible via `scripts/qa/split_tiers.py`

---

## Usage Recommendations

### For Downstream Analysis (e.g., fp-qubit-design)

**Recommended:**  
Use `atlas_fp_optical_v2_2_curated.csv` (~180-193 systems)

**Rationale:**
- Clean, modeling-ready data
- No placeholder noise
- Full provenance chain

**Avoid:**  
Mixing curated + unknown tiers → introduces bias (Unknown systems act as noise regularization, not signal)

### For Atlas Curation

**Review pipeline:**
1. Start with Tier 2 (candidates) — easiest to promote
2. Manually curate: find missing spectra/contrast from papers
3. Promote to Tier 1 when complete

**Tier 3 systems:**
- Lower priority (generic FPs, unclear function)
- May require domain expert review

---

## Implementation

**Created by:** `scripts/qa/split_tiers.py` (reproducible)  
**Validated by:** `scripts/validate_atlas.py --tier [curated|candidates|unknown]`  
**Documented:** This file (`docs/DATA_TIERS.md`)

---

## Changelog

- **2025-11-10:** Initial tier specification based on quality analysis
  - Tier 1: 180 systems (strict criteria)
  - Tier 2: 13 systems (incomplete)
  - Tier 3: 103 systems (unknown/placeholder)
  - Total: 296 systems (all preserved)

---

## Non-Optical Qubit Systems (Separate Schema)

**Scope:** The tiering system above applies ONLY to **optical fluorescent protein systems**. 

**Non-optical quantum systems** (spin qubits, radical pairs, nuclear spins) are handled in a completely separate schema to avoid cross-contamination:

### Separate Files (Non-Optical)

| File | System Type | Status | Count |
|------|-------------|--------|-------|
| `data/staging/spin_qubit_candidates.csv` | Spin qubits (NV centers, SiC defects, etc.) | Staging | 0 (headers only) |
| `data/staging/radical_pair_candidates.csv` | Radical pairs (cryptochrome, etc.) | Staging | 0 (headers only) |
| `data/staging/nuclear_spin_candidates.csv` | Nuclear spin qubits | Staging | 0 (headers only) |

**Schema documentation:** See `docs/EXTENDED_QUBITS_SCHEMA.md`

**Guarantee:**
- Non-optical systems are NEVER mixed with optical FP tiers (Tier1/Tier2/Tier3)
- Optical counts (180+13+103=296) remain unchanged
- Non-optical candidates require same quality standards (DOI, measurements, no fabrication)

---

**Contact:** Atlas curator  
**References:**
- `docs/ATLAS_SPEC.md` — Schema specification (optical systems)
- `docs/EXTENDED_QUBITS_SCHEMA.md` — Schema specification (non-optical systems)
- `docs/KNOWN_ISSUES.md` — Known data limitations
- `docs/STAGING_GUIDE.md` — Manual curation workflow

