# Data Tiering Specification

## Purpose

The Atlas contains systems from multiple sources with varying quality levels. This document defines explicit tiers to separate **curated, modeling-ready data** from **staging candidates** and **unusable placeholders**.

## Version

Applies to: **v4.0.0** (195 FP biosensors + 82 biological qubits, as of 2026-04-17).

The same three-tier philosophy is applied independently to each of the two datasets:

- `data/processed/atlas_fp_optical_v3_curated.csv` — **195 rows**, optical FP biosensors (this doc's primary scope).
- `data/qubits/biological_qubits_v3.csv` — **82 rows**, biological qubits (classes A, A', B, C, D). Quality is encoded in the `Qualite` column (Tier A1/A2/A3/B/C) as documented in `SCHEMA_v3.0.md`.

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

**Expected count (v4.0.0):** 195 systems (all currently in Tier 1 after the v3 enrichment pass).

**File:** `data/processed/atlas_fp_optical_v3_curated.csv`

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

**Expected count (v4.0.0):** 0 systems in the curated Tier 2 file. Legacy v2.2 Tier 2 candidates that could not be promoted were deprecated in `CHANGELOG.md` (v3.0.0, section "Deprecated").

**File (historical):** `data/staging/atlas_fp_optical_v2_2_candidates.csv`

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

**Source breakdown (historical):**
- 77 systems from `deep_harvest_uniprot_deep` (UniProt API)
- 26 systems from `api_harvest_fpbase_csv` (FPbase CSV)

**Purpose:**  
Isolation zone:
- NOT counted in official "N systems" for modeling
- Kept for transparency/auditability
- Reviewed during v3.0.0/v4.0.0 curation; remaining noise-only rows live under `data/staging/`.

**Expected count (historical v2.2 harvest):** ~103 systems

**File (historical):** `data/staging/atlas_fp_optical_v2_2_unknown.csv`

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

- **NO systems deleted arbitrarily** — v3.0.0 (and v4.0.0) explicitly logs deprecations in `CHANGELOG.md` when systems are removed (e.g., ErCry4b, ErCry1 when 2024-2025 replication studies invalidated the original claims).
- Historical v2.2 raw and tiered files remain available under `data/staging/` and in older Git tags (v2.2.x).
- All tiers programmatically reproducible via `scripts/qa/split_tiers.py`.

---

## Usage Recommendations

### For Downstream Analysis (e.g., fp-qubit-design)

**Recommended:**  
Use `data/processed/atlas_fp_optical_v3_curated.csv` (195 systems) for optical FP biosensors, and `data/qubits/biological_qubits_v3.csv` (82 systems) for biological qubits.

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

- **2026-04-17 (v4.0.0):** Clean re-release of v3.0.0 content on a pruned repository (historical archives, internal debate module, QA logs and binary submission bundles removed from tracking).
- **2026-04-17 (v3.0.0, RESTRICTED on Zenodo):** Refreshed for the v3 release.
  - Curated FP atlas promoted to 195 systems (all Tier 1) after the 2024-2026 literature enrichment pass.
  - Biological qubits dataset added (`biological_qubits_v3.csv`, 82 rows, classes A/A'/B/C/D).
  - Data Tiers doc retains the v2.2 three-tier philosophy for reproducibility; historical files are still available for audit under `data/staging/`.
- **2025-11-10:** Initial tier specification based on quality analysis
  - Tier 1: 180 systems (strict criteria)
  - Tier 2: 13 systems (incomplete)
  - Tier 3: 103 systems (unknown/placeholder)
  - Total: 296 systems (all preserved)

---

## Biological Qubits (v3 — separate dataset)

**Scope:** The Tier 1/2/3 scheme above applies ONLY to the **optical FP biosensor atlas** (`atlas_fp_optical_v3_curated.csv`, 195 rows).

**Biological qubits** (classes A, A', B, C, D) are curated in a separate dataset with its own quality annotations:

### Dataset

- File: `data/qubits/biological_qubits_v3.csv` (82 rows)
- Schema: `SCHEMA_v3.0.md`
- Quality encoded in the `Qualite` column (values: `A1`, `A2`, `A3`, `B`, `C`):
  - **A1**: Direct experimental values (T1/T2/contrast measured in the cited paper on the cited system)
  - **A2**: Values from a closely related system (same defect/host, minor composition differences)
  - **A3**: Values extrapolated from the literature with clear citation
  - **B**: Qualitative evidence only (e.g., ODMR observed but T1/T2 not reported)
  - **C**: Candidate / preliminary (preprint, unverified)

### Guarantee

- Biological qubits are NEVER mixed with optical FP tiers.
- Optical FP atlas counts (195 Tier 1 in v4.0.0) and qubit counts (82 across 5 classes) are reported separately.
- Both datasets require DOI + measurable evidence for Tier 1 / Qualite ∈ {A1, A2}.

---

**Contact:** via [GitHub Issues](https://github.com/Mythmaker28/quantum-sensors-qubits-in-biology/issues).  
**References:**
- `SCHEMA_v3.0.md` — Schema specification (qubits + FP systems, v3)
- `docs/ATLAS_SPEC.md` — Schema specification (optical systems, legacy)
- `docs/EXTENDED_QUBITS_SCHEMA.md` — Schema specification (non-optical systems, legacy)
- `docs/KNOWN_ISSUES.md` — Known data limitations
- `docs/STAGING_GUIDE.md` — Manual curation workflow

