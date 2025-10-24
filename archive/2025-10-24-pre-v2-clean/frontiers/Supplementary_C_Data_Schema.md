# Supplementary Material C — Data Schema and Column Descriptions

**Atlas Version**: 1.2.1  
**Date**: October 23, 2025  
**File**: `atlas_fp_optical.csv`

---

## Overview

This document defines the complete schema for the Biological Qubits Atlas v1.2.1 dataset, including column names, data types, units, and descriptions. The schema is guaranteed stable for v1.2.x releases (semantic versioning).

---

## File Format

- **Format**: CSV (Comma-Separated Values)
- **Encoding**: UTF-8
- **Delimiter**: `,` (comma)
- **Quote Character**: `"` (double quote)
- **Header**: First row contains column names
- **Rows**: 66 (data) + 1 (header)
- **File Size**: ~8 KB

---

## Column Schema

### Identification Columns

| Column Name | Type | Description | Nullable | Example |
|-------------|------|-------------|----------|---------|
| `SystemID` | string | Unique identifier (format: FP_EXT_XXXX) | No | FP_EXT_0001 |
| `protein_name` | string | Common protein name | No | jGCaMP8s |
| `variant` | string | Genetic variant or mutation (e.g., "A206K", "wild-type") | Yes | A206K |
| `family` | string | Protein family classification (e.g., "Calcium", "GFP-like", "Dopamine") | Yes | Calcium |
| `is_biosensor` | int | Binary flag: 1 = biosensor, 0 = standard FP | No | 1 |

**Notes**:
- `SystemID` is auto-generated and unique across all Atlas versions.
- `protein_name` follows FPbase naming conventions where possible.
- `family` groups proteins by functional class or spectral similarity.

---

### Cross-References

| Column Name | Type | Description | Nullable | Example |
|-------------|------|-------------|----------|---------|
| `uniprot_id` | string | UniProt accession number | Yes | P42212 |
| `pdb_id` | string | Protein Data Bank structure ID | Yes | 3WLD |

**Notes**:
- `uniprot_id` and `pdb_id` are NULL for many entries due to incomplete database coverage.
- Cross-references enable linking to external databases for sequence/structure data.

---

### Optical Properties

| Column Name | Type | Unit | Description | Nullable | Example |
|-------------|------|------|-------------|----------|---------|
| `excitation_nm` | float | nm | Peak excitation wavelength | Yes | 488.0 |
| `emission_nm` | float | nm | Peak emission wavelength | Yes | 510.0 |
| `quantum_yield` | float | dimensionless | Fluorescence quantum yield (0-1) | Yes | 0.60 |
| `extinction_coef` | float | M⁻¹cm⁻¹ | Molar extinction coefficient | Yes | 56000.0 |
| `brightness_relative` | float | dimensionless | Relative brightness (QY × ε / 1000) | Yes | 33.6 |

**Notes**:
- Wavelengths are for the major peak; some FPs have multiple peaks.
- `brightness_relative` = (quantum_yield × extinction_coef) / 1000.

---

### Contrast Measurements

| Column Name | Type | Unit | Description | Nullable | Example |
|-------------|------|------|-------------|----------|---------|
| `contrast_ratio` | float | varies | Measured or computed contrast value | Yes | 90.0 |
| `contrast_unit` | string | N/A | Unit of contrast_ratio: "fold", "deltaF_F0", or "percent" | Yes | fold |
| `contrast_normalized` | float | fold | Contrast normalized to fold-change | Yes | 90.0 |
| `contrast_ci_low` | float | varies | Lower bound of 95% confidence interval | Yes | 85.0 |
| `contrast_ci_high` | float | varies | Upper bound of 95% confidence interval | Yes | 95.0 |
| `contrast_source` | string | N/A | Source: "measured", "computed", or "none" | No | measured |
| `contrast_quality_tier` | string | N/A | Quality tier: "A" (with CI/n), "B" (measured), "C" (computed) | Yes | A |

**Notes**:
- **Normalization rules**:
  - `fold` → unchanged
  - `deltaF_F0` → fold = ΔF/F₀ + 1
  - `percent` → fold = 1 + (percent / 100)
- **Quality tiers**:
  - **A**: Measured with confidence intervals or n ≥ 3
  - **B**: Measured without statistical info
  - **C**: Computed (e.g., from QY × ε) or missing

---

### Experimental Context

| Column Name | Type | Unit | Description | Nullable | Example |
|-------------|------|------|-------------|----------|---------|
| `temperature_K` | float | Kelvin | Measurement temperature | Yes | 310.0 |
| `pH` | float | dimensionless | Measurement pH | Yes | 7.4 |
| `host_system` | string | N/A | Expression system (e.g., "HEK293", "E. coli") | Yes | HEK293 |
| `condition_text` | string | N/A | Free-text description of assay conditions | Yes | "Saturating Ca²⁺ (10 µM)" |

**Notes**:
- `temperature_K` commonly 310 K (37°C, physiological) or 298 K (25°C, room temp).
- `condition_text` captures details not easily structured (e.g., analyte concentration, buffer composition).

---

### Provenance and Licensing

| Column Name | Type | Description | Nullable | Example |
|-------------|------|-------------|----------|---------|
| `source_refs` | string | DOI, PMCID, or database reference | Yes | DOI:10.1038/s41586-021-03362-w |
| `license_source` | string | License of source data (e.g., "CC-BY", "CC0") | Yes | CC-BY |
| `figure_ref` | string | Figure/table reference in original publication | Yes | Figure 2C |
| `evidence_type` | string | Evidence source: "xml", "pdf", "table", "supplement" | Yes | xml |

**Notes**:
- `source_refs` follows DOI format (e.g., `10.xxxx/xxxx`) or PMC format (e.g., `PMC:PMC12345678`).
- All entries with `contrast_ratio` non-NULL **must** have `source_refs` and `license_source`.
- Only CC-BY, CC0, or CC BY-SA licenses are included (Open Access only).

---

## Data Types and Constraints

### String Columns

- **Encoding**: UTF-8
- **Max Length**: 255 characters (practical limit)
- **NULL Representation**: Empty string `""` or `NULL` in Pandas

### Numeric Columns

- **Type**: `float64` (Pandas) or `REAL` (SQLite)
- **NULL Representation**: `NaN` (Pandas) or `NULL` (SQLite)
- **Range Constraints**:
  - `excitation_nm`, `emission_nm`: 300-800 nm (visible to NIR)
  - `quantum_yield`: 0.0-1.0
  - `extinction_coef`: 1000-200000 M⁻¹cm⁻¹
  - `contrast_ratio`: 0.0-100.0 (typical range; outliers >100 flagged in QA)
  - `temperature_K`: 273-323 K (-0°C to 50°C)
  - `pH`: 4.0-10.0 (physiological range)

### Boolean Columns

- `is_biosensor`: Integer (0 or 1, not TRUE/FALSE)

---

## Missing Data Policy

### NULL vs. Zero

- **NULL**: Data not available or not applicable
- **0.0**: Actual measurement of zero (rare; typically means "no contrast")

### Examples

| Case | `contrast_ratio` | `contrast_source` | Interpretation |
|------|------------------|-------------------|----------------|
| Measured value | 90.0 | "measured" | Real measurement from literature |
| Computed value | 2.5 | "computed" | Estimated from QY × ε |
| Unknown | NULL | "none" | No data available |
| No contrast | 1.0 | "measured" | Measured, no change (e.g., control FP) |

---

## Quality Assurance Rules

All data in v1.2.1 satisfy:

1. **No synthetic data**: All values are real or NULL
2. **License compliance**: Only OA-compatible licenses (CC-BY, CC0, CC BY-SA)
3. **Provenance**: All measured contrasts have DOI/PMCID
4. **No duplicates**: Unique `SystemID` per entry
5. **Type consistency**: All columns match declared types

---

## Example Row (jGCaMP8s)

```csv
SystemID,protein_name,variant,family,is_biosensor,uniprot_id,pdb_id,excitation_nm,emission_nm,temperature_K,pH,contrast_ratio,contrast_unit,contrast_normalized,contrast_ci_low,contrast_ci_high,contrast_source,contrast_quality_tier,condition_text,source_refs,license_source,figure_ref,evidence_type
FP_EXT_0012,jGCaMP8s,,Calcium,1,,,488.0,510.0,310.0,7.4,90.0,fold,90.0,85.0,95.0,measured,A,"Saturating Ca²⁺ (10 µM) vs. resting (100 nM), HEK293 cells",DOI:10.1038/s41586-021-03362-w,CC-BY,Figure 2C,xml
```

---

## Version History

### v1.2.1 (October 2025)

- **Columns**: 22
- **Entries**: 66
- **Schema**: Stable (guaranteed compatible with v1.2.0)

### v1.2.0 (October 2025)

- **Initial schema** with 22 columns
- **Breaking change** from v1.1.x (renamed columns, added quality tiers)

---

## Consumer Recipe

### Python (Pandas)

```python
import pandas as pd

# Load dataset
url = "https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases/download/v1.2.1/atlas_fp_optical.csv"
df = pd.read_csv(url)

# Enforce schema types
df['SystemID'] = df['SystemID'].astype(str)
df['is_biosensor'] = df['is_biosensor'].astype(int)
df['excitation_nm'] = pd.to_numeric(df['excitation_nm'], errors='coerce')
df['emission_nm'] = pd.to_numeric(df['emission_nm'], errors='coerce')
df['contrast_ratio'] = pd.to_numeric(df['contrast_ratio'], errors='coerce')

# Filter for measured contrasts only
measured = df[df['contrast_source'] == 'measured']

print(f"Loaded {len(df)} entries, {len(measured)} with measured contrast")
```

### R

```r
library(readr)

# Load dataset
url <- "https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases/download/v1.2.1/atlas_fp_optical.csv"
df <- read_csv(url)

# Filter for biosensors with measured contrast
biosensors <- df[df$is_biosensor == 1 & df$contrast_source == "measured", ]

cat(sprintf("Loaded %d entries, %d biosensors with measured contrast\n", nrow(df), nrow(biosensors)))
```

---

## Contact and Support

For schema questions or data issues, please contact:

- **GitHub Issues**: https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues
- **Email**: (to be provided)

---

**End of Schema Documentation**

