# Known Issues — Biological Qubits Atlas

## Data Quality Structure (2025-11-10)

### Tier System Implemented

**Problem Identified:**  
After deep API harvesting (219 → 296 systems), downstream analysis (fp-qubit-design) revealed:
- ~193 systems usable for modeling
- ~103 systems with placeholder data (family="Unknown", contrast=1.0, no spectra)
- Mixing tiers introduced noise regularization (not signal)

**Solution:**  
Explicit non-destructive tier splitting:

| Tier | Count | Description | File |
|------|-------|-------------|------|
| **Tier 1: CURATED** | 180 | Known family + DOI + (spectra OR contrast>1.5) | `atlas_fp_optical_v2_2_curated.csv` |
| **Tier 2: CANDIDATES** | 13 | Real but incomplete (missing spectra) | `atlas_fp_optical_v2_2_candidates.csv` |
| **Tier 3: UNKNOWN** | 103 | Auto-harvested placeholders | `atlas_fp_optical_v2_2_unknown.csv` |

**Data Preservation:**  
- **0 systems deleted** — all 296 preserved
- Original `atlas_fp_optical_v2_2.csv` kept as "mixed" audit view
- Tier split programmatically reproducible via `scripts/qa/split_tiers.py`

**Tier 3 Composition (103 systems):**
- 77 from UniProt deep harvest (`deep_harvest_uniprot_deep`)
- 26 from FPbase API harvest (`api_harvest_fpbase_csv`)
- All have `family="Unknown"` and `contrast_normalized=1.0` (placeholder)
- All have DOI but insufficient metadata for modeling

**Recommended for Downstream:**  
Use **`atlas_fp_optical_v2_2_curated.csv`** (180 systems) for ML/modeling to avoid placeholder noise.

**Manual Curation Queue:**  
- Tier 2: 13 systems (high priority — real systems, just need spectral data)
- Tier 3: 103 systems (lower priority — need family classification + contrast measurement)
- Additional staging: 844 raw API candidates in `candidates_needing_curation.csv`

---

## Incomplete Metadata (Acceptable)

### Optional Fields with Missing Data

The following fields are **recommended but optional** (see `scripts/validate_atlas.py`):

| Field | Missing Count | Reason |
|-------|---------------|--------|
| `license` | 113 | Cannot verify without journal API access |
| `temperature_K` | 15 | Not reported in original papers |
| `method` | 15 | Implicit (inferred as "fluorescence") |
| `quality_tier` | 15 | Requires manual curation |

**Policy:**  
These fields are left empty rather than fabricated. This ensures data integrity and transparency.

**Validation:**  
`scripts/validate_atlas.py` treats these as **warnings** (not errors) when missing.

---

## Removed Systems (2025-11-10)

The following systems were **removed** due to missing required fields:

1. **GFP** (no DOI, no family) - FP_0015
2. **mClover** (no DOI) - FP_0063
3. **mOrange2** (no family, no is_biosensor) - FP_0220

**Reason:**  
Required fields (`doi`, `family`, `is_biosensor`) are essential for atlas integrity. Systems lacking these cannot be validated without fabricating data.

---

## Future Work

### Potential Enrichment Sources

1. **FPbase API** (when restored):
   - Target: Calcium, Voltage, Neurotransmitter sensors
   - Estimated: +20-30 systems

2. **UniProt API**:
   - Target: Genetically encoded biosensors
   - Estimated: +10-15 systems

3. **Literature Mining** (Europe PMC):
   - Target: Recent publications (2023-2025)
   - Estimated: +15-20 systems

### Manual Curation Queue

Systems identified but requiring manual verification:
- (None currently - will be added as discovered)

---

**Last Updated:** 2025-11-10  
**Validator Version:** scripts/validate_atlas.py (v2.2.2)

