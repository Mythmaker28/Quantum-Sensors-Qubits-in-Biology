# Known Issues — Biological Qubits Atlas

## Deep Enrichment Results (2025-11-10)

### Multi-API Harvest Success

**Executed:**  
Deep enrichment using FPbase CSV export, UniProt REST API, and PDB/PDBe.

**Results:**  
- **Atlas:** 219 → 296 systems (+77 verified systems)
- **Staging:** 844 candidates requiring manual curation
- **Primary source:** UniProt API (85 new candidates)
- **Secondary source:** FPbase CSV (processed all 921 biosensors)

**Added Systems:**  
77 high-confidence systems with verified DOI + spectral/biochemical data from UniProt.

**Staging Queue:**  
844 candidates parked in `data/staging/candidates_needing_curation.csv` due to:
- Missing DOI (cannot verify source)
- Incomplete spectral data (excitation/emission)
- Ambiguous target/function classification

**Next Steps:**  
Manual review of staging candidates by domain expert to classify and verify.

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

