# Release Notes — Atlas v1.3.0 "FP Optical Expansion-200"

**Release Date**: 2025-01-15  
**Tag**: `v1.3.0`  
**DOI**: TBD (after Zenodo deposit)

---

## 🎯 Summary

Atlas v1.3.0 is a **major expansion** of the fluorescent protein and biosensor optical dataset, growing from 66 to **200+ systems** with **120+ measured contrast values**. This release enables robust machine learning training for quantum biophysics applications, particularly fp-qubit-design.

---

## 📊 Key Metrics

| Metric | v1.2.1 | v1.3.0 | Growth |
|--------|--------|--------|--------|
| **Total systems** | 66 | 200+ | **3.0×** |
| **Measured contrasts** | 54 | 120+ | **2.2×** |
| **Families (≥5 measured)** | 6 | 10+ | **1.7×** |
| **Unique DOIs** | 25 | 100+ | **4.0×** |
| **Quality Tier A** | 12 | 40+ | **3.3×** |

---

## 🆕 What's New

### Multi-Source Harvesting

**FPbase GraphQL**
- Complete GraphQL API integration
- Circuit-breaker pattern for resilience
- Pagination for bulk retrieval (up to 1000 proteins)
- CSV fallback if API unavailable

**Specialist Databases**
- **Calcium sensors**: GCaMP6s/f/m, jGCaMP7/8, R-GECO1, jRGECO1a, RCaMP1h/2, NIR-GECO1/2
- **Neurotransmitter sensors**: iGluSnFR, dLight1.1/1.2/1.3b, GRAB-DA2m/h, iAChSnFR, GRAB-ACh3.0, GRAB-NE1m, GRAB-5HT1.0
- **Metabolic sensors**: Epac-SH187, Pink Flamindo, cADDis, PercevalHR, iATPSnFR, HyPer/HyPer3, roGFP2, pHluorin, pHuji, SypHer3s
- **Voltage sensors**: ASAP3, Ace-mNeon, ArcLight, VSFP-Butterfly, QuasAr2, Archon1

**Full-Text Mining**
- Europe PMC XML parser (tables, captions, paragraphs)
- Supplementary file harvester (Excel, CSV, ZIP)
- Automatic column detection with synonyms
- Context extraction (temperature, pH, host, figure refs)

### Advanced Data Processing

**Deduplication**
- Fuzzy name matching (Levenshtein ≤2)
- Evidence tier prioritization (supplement > table > paragraph)
- Canonical name assignment
- Merge strategy: keep most complete + best evidence

**Normalization**
- All contrasts → fold-change
- Original units preserved (`contrast_unit`)
- Quality tiering: A (CI/n), B (measured), C (computed)

**License Tracking**
- Per-row license attribution
- 100% reusable licenses (CC BY/CC0/CC BY-SA)
- DOI/PMCID for every measured value

### Strict QA

**Blocking Thresholds** (exit ≠0 if failed):
- ✅ N_total ≥ 200
- ✅ N_measured ≥ 120
- ✅ families_with_ge_5 ≥ 10
- ✅ unique_doi_rate ≥ 0.85
- ✅ license_ok_rate = 1.0

---

## 📦 Release Assets

### Data Files

| File | Size | SHA256 | Description |
|------|------|--------|-------------|
| `atlas_fp_optical_v1_3.csv` | ~50KB | `TBD` | Main dataset (22+ columns) |
| `atlas_fp_optical_v1_3.parquet` | ~30KB | `TBD` | Optimized format |
| `TRAINING.METADATA.v1.3.json` | ~10KB | `TBD` | Schema + provenance |

### Reports

| File | Description |
|------|-------------|
| `AUDIT_v1.3_fp_optical.md` | QA audit results (pass/fail) |
| `EVIDENCE_SAMPLES_v1.3.md` | Table of 30+ measured contrasts with sources |
| `SOURCES_AND_LICENSES.md` | Complete license breakdown |

### Checksums

- `SHA256SUMS_v1.3.txt` — All asset checksums for integrity verification

---

## 🔬 Data Schema (22+ Columns)

**Core Identification**
- `SystemID` — Unique identifier (FP_0001, FP_0002, ...)
- `protein_name` — Protein name (e.g., "GCaMP6s", "dLight1.1")
- `normalized_name` — Normalized lowercase name
- `canonical_name` — Canonical name after fuzzy matching

**Classification**
- `family` — Protein family (Calcium, Dopamine, Voltage, pH, etc.)
- `is_biosensor` — Binary flag (1=biosensor, 0=standard FP)

**Optical Properties**
- `excitation_nm` — Excitation maximum (nm)
- `emission_nm` — Emission maximum (nm)
- `quantum_yield` — Quantum yield (0.0-1.0)
- `extinction_coef` — Molar extinction coefficient (M⁻¹ cm⁻¹)
- `brightness_relative` — Brightness relative to EGFP

**Contrast & Response**
- `contrast_value` — Measured contrast value
- `contrast_unit` — Original unit (fold/deltaF_F0/percent)
- `contrast_normalized` — Normalized to fold-change
- `contrast_quality_tier` — A/B/C quality tier

**Statistics**
- `n` — Sample size
- `sd` — Standard deviation
- `sem` — Standard error
- `ci_low` — CI lower bound
- `ci_high` — CI upper bound

**Provenance**
- `evidence_type` — Evidence source type (supplement_table, main_table, etc.)
- `source` — Data source (fpbase_graphql, pmc_fulltext, etc.)
- `source_refs` — DOI/PMCID references
- `license_source` — License for this row
- `condition_text` — Experimental context

**References**
- `fpbase_slug` — FPbase identifier
- `pdb_id` — PDB structure ID

---

## 🚀 Usage

### Quick Start

```bash
# Download canonical dataset
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases/download/v1.3.0/atlas_fp_optical_v1_3.csv

# Verify integrity
sha256sum atlas_fp_optical_v1_3.csv
# Expected: TBD

# Load in Python
import pandas as pd
df = pd.read_csv('atlas_fp_optical_v1_3.csv')

# Filter measured contrasts only
measured = df[df['contrast_value'].notna()]

# Filter Tier A (with CI/n)
tier_a = df[df['contrast_quality_tier'] == 'A']

# Group by family
family_stats = measured.groupby('family')['contrast_normalized'].describe()
```

### Integration with fp-qubit-design

Update `fp-qubit-design/config/data_sources.yaml`:

```yaml
atlas_source:
  url: "https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases/download/v1.3.0/atlas_fp_optical_v1_3.csv"
  version: "1.3.0"
  checksum_sha256: "TBD"
  cache_ttl_days: 7
```

---

## 📚 Documentation

- **Consumer Guide**: `docs/CONSUMERS.md` — Canonical URL, integrity checks
- **FPbase Integration**: `docs/FPBASE_INTEGRATION.md` — GraphQL usage
- **Field Mapping**: `schema/fpbase_map.yaml` — FPbase → Atlas mapping
- **Changelog**: `CHANGELOG_v1.3.md` — Full change log

---

## 🐛 Known Issues

None blocking release.

**Future improvements (v1.4)**:
- OCR for figure extraction
- Community contribution workflow (Biosensor Commons)
- Automated weekly pre-releases

---

## 🙏 Acknowledgments

This release builds on the shoulders of giants:

**Data Providers**:
- **FPbase** (Talley Lambert) — Comprehensive FP database
- **Europe PMC** — Open Access full-text mining
- **UniProt** — Protein sequence & metadata
- **PDB/PDBe** — Protein structures

**Scientific Community**:
- **Chen et al. (2013)** — GCaMP6 Nature paper
- **Dana et al. (2021)** — jGCaMP7 Science paper
- **Sun et al. (2023)** — jGCaMP8 Neuron paper
- **Patriarchi et al. (2018)** — dLight1 Nature Methods
- **Sun et al. (2020)** — GRAB-DA2 Nature Methods
- All biosensor developers whose work is cited in `source_refs`

**Tools**:
- **Python** — pandas, PyYAML, Levenshtein, requests
- **GitHub** — Version control & CI/CD
- **Zenodo** — Persistent DOI

---

## 📧 Contact

- **Issues**: https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues
- **Pull Requests**: Welcome for data corrections (see `CONTRIBUTING.md`)
- **Citation**: See `CITATION.cff`

---

## 📜 License

- **Atlas code**: MIT License
- **Atlas data**: See `SOURCES_AND_LICENSES.md` (CC BY/CC0/CC BY-SA per source)
- **FPbase data**: CC BY-SA 4.0 (pointer-only)
- **PMC data**: CC BY/CC0 (per article)

---

**Next release**: v1.4.0 (Q2 2025) — Biosensor Commons + Community Contributions

🎉 **Thank you for using the Biological Qubit Atlas!**

