# Staging Candidates Curation Guide

## Overview

The file `data/staging/candidates_needing_curation.csv` contains **844 candidate systems** identified during automated API harvesting but requiring manual verification before atlas inclusion.

## Why Staging?

These candidates were **NOT automatically added** to the main atlas because:

1. **Missing DOI** — Cannot verify source publication
2. **Incomplete Spectral Data** — Missing excitation/emission wavelengths
3. **Ambiguous Classification** — Target/family unclear from API metadata
4. **Potential Duplicates** — Variants or isoforms of existing systems

## Staging File Schema

| Column | Description |
|--------|-------------|
| `protein_name` | Protein/construct name from source |
| `doi` | DOI if available (may be null) |
| `switch_type` | Biosensor type from FPbase (if applicable) |
| `excitation_nm` | Excitation wavelength (may be null) |
| `emission_nm` | Emission wavelength (may be null) |
| `brightness` | Brightness from FPbase (if applicable) |
| `qy` | Quantum yield (if applicable) |
| `uniprot_id` | UniProt accession (if from UniProt) |
| `source` | Origin API (fpbase_csv_deep, uniprot_deep, etc.) |
| `reason` | Why it needs curation (missing_doi, missing_spectral_data) |

## Curation Workflow

### 1. Review Candidates

```python
import pandas as pd

staging = pd.read_csv('data/staging/candidates_needing_curation.csv')

# Filter by reason
missing_doi = staging[staging['reason'] == 'missing_doi']
missing_spectral = staging[staging['reason'] == 'missing_spectral_data']

print(f"Missing DOI: {len(missing_doi)}")
print(f"Missing spectral: {len(missing_spectral)}")
```

### 2. Verify via Literature

For each candidate:
1. Search PubMed/Google Scholar for `[protein_name] fluorescent protein`
2. Identify primary publication
3. Extract:
   - DOI
   - Excitation/emission wavelengths
   - Target (calcium, voltage, pH, etc.)
   - Contrast/dynamic range

### 3. Add Verified Systems

Once verified, add to main atlas:

```python
# Load atlas
atlas = pd.read_csv('data/processed/atlas_fp_optical_v2_2.csv')

# Add verified candidate (example)
new_system = {
    'SystemID': 'FP_XXXX',  # Next available ID
    'protein_name': 'VerifiedProtein',
    'family': 'Calcium',  # Manually determined
    'is_biosensor': 1.0,
    'contrast_normalized': 5.2,  # From paper
    'doi': '10.xxxx/verified.doi',  # Found in literature
    'curator': 'manual_curation_v2.3',
    'excitation_nm': 488,
    'emission_nm': 512,
    # ... other fields
}

atlas = pd.concat([atlas, pd.DataFrame([new_system])], ignore_index=True)
atlas.to_csv('data/processed/atlas_fp_optical_v2_2.csv', index=False)
```

### 4. Validate

After adding any systems:

```bash
python scripts/validate_atlas.py
python scripts/web/regenerate_dashboard.py
```

## Priority Candidates

### High-Value Targets

Focus curation on:
1. **Novel sensor families** (e.g., chloride, magnesium, metabolites)
2. **Recent publications** (2023-2025)
3. **NIR/far-red sensors** (in vivo imaging)
4. **Genetically-encoded voltage indicators** (GEVIs)

### Lower Priority

- Generic GFP variants without sensing function
- Obsolete/deprecated constructs
- Duplicates of existing atlas entries

## Statistics

Current staging breakdown:

```
Total candidates: 844
├─ FPbase origin: ~843 (mostly biosensors without DOI links)
└─ UniProt origin: ~1 (some with DOI)

Reasons:
├─ missing_doi: ~840
└─ missing_spectral_data: ~4
```

## Notes

- All staging candidates have passed basic format validation
- None have fabricated data (empty fields left as null/NaN)
- Source APIs: FPbase CSV export + UniProt REST API
- Date harvested: 2025-11-10

---

**Contact:** Curator responsible for atlas updates










