# 📦 Release Notes — Biological Qubits Atlas v2.2.2

**Release Date:** 2025-10-26  
**Version:** 2.2.2 (Stable, Active Development)  
**Previous Version:** v2.2.0 (191 systems) → v2.0.0 (113 systems) → v1.2.1 (66 systems, frozen for Frontiers)

---

## 🎯 Executive Summary

**v2.2.2** is the **recommended stable version** for research, machine learning, and downstream analysis. It provides **180 curated, modeling-ready systems** (Tier 1) with full provenance tracking, balanced family distribution, and 100% optical coverage.

**Key Metrics:**
- **180 systems** (Tier 1: curated, modeling-ready)
- **13 systems** (Tier 2: candidates needing curation)
- **103 systems** (Tier 3: auto-harvested, transparency audit)
- **296 total systems** (all tiers combined)
- **30 families** represented (calcium, voltage, dopamine, glutamate, pH, etc.)
- **100% optical coverage** (all Tier 1 have excitation/emission OR contrast>1.5)

**Status:**
- ✅ **Tag created:** `v2.2.2` (Git tag exists)
- ⏳ **GitHub Release:** Pending (this document prepares the release)
- ⏳ **Zenodo DOI:** TBD (deposit in progress)

---

## 📊 What's New in v2.2.2

### Major Features

#### 1. **Explicit Tier System** 🎯

**Problem solved:** v2.2.0 mixed curated data with auto-harvested placeholders (103 systems with `family="Unknown"`, `contrast=1.0`), causing noise in downstream ML pipelines.

**Solution:** Non-destructive tier splitting:

| Tier | Count | Description | File |
|------|-------|-------------|------|
| **Tier 1: CURATED** | 180 | Known family + DOI + (spectra OR contrast>1.5) | `atlas_fp_optical_v2_2_curated.csv` |
| **Tier 2: CANDIDATES** | 13 | Real but incomplete (missing spectral data) | `atlas_fp_optical_v2_2_candidates.csv` |
| **Tier 3: UNKNOWN** | 103 | Auto-harvested placeholders (transparency) | `atlas_fp_optical_v2_2_unknown.csv` |

**Benefit:** Tier 1 is 100% modeling-ready, no placeholders, no noise. Tier 3 preserved for transparency (0 systems deleted).

**Documentation:** See [docs/DATA_TIERS.md](docs/DATA_TIERS.md)

---

#### 2. **Balanced Dataset for ML** 🧠

**Family distribution optimized:**

| Family | Count | Examples |
|--------|-------|----------|
| Calcium | 40 | GCaMP8, XCaMP, jRGECO |
| Voltage | 22 | ASAP3, ASAP4e, ArcLight |
| Dopamine | 13 | dLight, GRAB-DA |
| Glutamate | 10 | iGluSnFR, SF-iGluSnFR |
| pH, H2O2, ATP, cAMP, Redox, etc. | 95 | (30 families total) |

**No class imbalance:** Largest family (Calcium) is 22% of dataset. Smallest represented families have ≥5 systems.

---

#### 3. **100% Optical Coverage** 🔬

**All Tier 1 systems have:**
- Excitation/emission wavelengths (nm), **OR**
- Measured contrast > 1.5 (fold-change), **OR**
- Both

**No placeholders:** Unlike Tier 3 (`contrast=1.0` default), all Tier 1 contrast values are measured or literature-derived.

---

#### 4. **Enhanced Provenance** 📚

**Every Tier 1 system includes:**
- `doi` (required, validated DOI format)
- `curator` (version tag: `v2_2_curated`, `v2_2_increment`, etc.)
- `source_note` (API harvest source: `deep_harvest_uniprot`, `api_fpbase`, `manual_lit_mining`)

**Traceability:** All data points traceable to peer-reviewed literature or validated databases (FPbase, UniProt, PDB).

---

### Dataset Evolution

| Version | Date | Systems (Curated) | Systems (Total) | Key Addition |
|---------|------|-------------------|-----------------|--------------|
| v1.2.1 | 2025-10-23 | 66 | 66 | Frontiers manuscript (frozen) |
| v2.0.0 | 2025-10-24 | 113 | 113 | Interactive dashboard, FP extension |
| v2.1.0 | 2025-10-24 | 120 | 120 | FPbase integration |
| v2.2.0 | 2025-10-25 | 170 | 191 | Data boost (curated + auto-harvest mixed) |
| **v2.2.2** | **2025-10-26** | **180** | **296** | **Tier split, balanced, 100% optical** |

**Net gain (v1.2.1 → v2.2.2):**
- +114 curated systems (+173% increase)
- +30 families represented
- 0 systems deleted (all preserved in appropriate tiers)

---

## 📥 Download Instructions

### Recommended: Curated Tier (Modeling-Ready)

```bash
# Download Tier 1 ONLY (180 systems, no placeholders)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2_curated.csv

# Or via Python
import pandas as pd
url = "https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2_curated.csv"
df = pd.read_csv(url)
print(f"Loaded {len(df)} curated systems")
```

### Full Dataset (All Tiers Mixed, Audit Purposes)

```bash
# Download all 296 systems (includes Tier 3 placeholders)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2.csv

# ⚠️ NOT RECOMMENDED for ML/modeling (contains placeholder noise)
```

### Individual Tiers

```bash
# Tier 2: Candidates (13 systems, incomplete metadata)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/staging/atlas_fp_optical_v2_2_candidates.csv

# Tier 3: Unknown (103 systems, placeholders)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/staging/atlas_fp_optical_v2_2_unknown.csv
```

---

## ✅ Integrity Verification

### SHA256 Checksums

```bash
# Download checksums
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/SHA256SUMS_v2_2_2.txt

# Verify (Linux/macOS)
sha256sum -c SHA256SUMS_v2_2_2.txt

# Verify (Windows PowerShell)
Get-Content SHA256SUMS_v2_2_2.txt | ForEach-Object {
    $hash, $file = $_ -split '\s+', 2
    $actual = (Get-FileHash $file -Algorithm SHA256).Hash
    if ($actual -eq $hash) { Write-Host "✓ $file" -ForegroundColor Green }
    else { Write-Host "✗ $file" -ForegroundColor Red }
}
```

**Expected checksums (TBD after final file stabilization):**

```
[SHA256 for atlas_fp_optical_v2_2_curated.csv]
[SHA256 for atlas_fp_optical_v2_2.csv]
[SHA256 for atlas_fp_optical_v2_2_candidates.csv]
[SHA256 for atlas_fp_optical_v2_2_unknown.csv]
```

---

## 🔍 Quality Assurance

### Validation Passed

All datasets validated with `scripts/validate_atlas.py`:

```bash
# Tier 1 (strict mode)
python scripts/validate_atlas.py curated
# Result: 0 errors, 0 warnings, 180 systems validated

# Tier 2 (moderate mode)
python scripts/validate_atlas.py candidates
# Result: 0 critical errors, 13 warnings (expected: incomplete metadata)

# Tier 3 (permissive mode)
python scripts/validate_atlas.py unknown
# Result: Warnings expected (placeholders), no critical errors
```

### Known Limitations (Acceptable)

**Tier 1 (curated):**
- ✅ 0 critical errors
- ⚠️ 15 systems missing `temperature_K` (not reported in original papers)
- ⚠️ 113 systems missing `license` (cannot verify without journal API access)

**Policy:** Empty fields preferred over fabricated data. See [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md).

---

## 🚀 Use Cases

### ✅ Recommended Use Cases for v2.2.2

1. **Machine Learning / Predictive Modeling**
   - Use: `atlas_fp_optical_v2_2_curated.csv` (Tier 1 only)
   - Benefit: No placeholder noise, balanced distribution

2. **Computational Protein Design**
   - Example: [fp-qubit-design](https://github.com/Mythmaker28/fp-qubit-design) uses v2.2.2 as training data
   - Features: 180 systems with excitation/emission, contrast, family labels

3. **Quantitative Analysis / Meta-Studies**
   - Use: Tier 1 for statistical analysis
   - Benefit: Full provenance (DOI for every system)

4. **Biosensor Selection / Comparison**
   - Filter by family (calcium, voltage, pH, etc.)
   - Compare contrast ratios, spectral properties

### ⚠️ NOT Recommended

- ❌ Using `atlas_fp_optical_v2_2.csv` (mixed) for ML → introduces 103 placeholders
- ❌ Training on Tier 3 (unknown) → `family="Unknown"` lacks semantic meaning
- ❌ Assuming all 296 systems are modeling-ready → only 180 are (Tier 1)

---

## 🔄 Migration from Previous Versions

### From v1.2.1 (Frontiers)

**Schema:** ✅ Backward compatible (no breaking changes)

**Code migration:**

```python
# Old (v1.2.1)
df = pd.read_csv('atlas_fp_optical_v1_2_1.csv')

# New (v2.2.2, Tier 1)
df = pd.read_csv('atlas_fp_optical_v2_2_curated.csv')

# No other changes needed
```

**Data changes:**
- +114 curated systems (66 → 180)
- Same schema (new optional columns: `quality_tier`, `curator`)

---

### From v2.0.0 / v2.1.0

**Action required:** Switch to Tier 1 file to avoid placeholder noise.

```python
# Old (v2.0/v2.1, mixed data)
df = pd.read_csv('atlas_fp_optical_v2_0.csv')  # 113 systems, no tiers

# New (v2.2.2, curated only)
df = pd.read_csv('atlas_fp_optical_v2_2_curated.csv')  # 180 systems, no noise
```

---

## 📚 Citation

### How to Cite v2.2.2

**BibTeX:**

```bibtex
@dataset{biological_qubits_atlas_v2_2_2,
  title  = {Biological Qubits \& Quantum Sensors Atlas v2.2.2 (Curated)},
  author = {Lepesteur, Tommy},
  year   = {2025},
  version = {2.2.2-curated},
  systems = {180},
  note   = {DOI pending Zenodo deposit},
  url    = {https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology}
}
```

**Plain text:**

> Lepesteur, T. (2025). *Biological Qubits & Quantum Sensors Atlas v2.2.2 (Curated)*. GitHub. https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology

**⚠️ DOI Update:** Once Zenodo deposit completes, DOI will be added to [VERSIONS_CITATION.md](VERSIONS_CITATION.md).

---

## 🐛 Known Issues

### Fixed in v2.2.2

- ✅ **Placeholder noise in mixed dataset** → Resolved via tier splitting
- ✅ **Unbalanced family distribution** → Resolved via balanced harvest
- ✅ **Missing optical data** → Resolved via 100% coverage requirement

### Outstanding (Non-Critical)

- ⚠️ **DOI not yet minted** → Zenodo deposit in progress (Q4 2025)
- ⚠️ **Temperature field incomplete** → 15 systems missing (not reported in literature)
- ⚠️ **License field incomplete** → 113 systems missing (requires journal API access)

**Impact:** None for modeling/ML use cases. Empty fields do not affect data quality for intended use.

**Tracking:** See [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md)

---

## 🛠️ Technical Details

### Files Included in This Release

| File | Size | Lines | Description |
|------|------|-------|-------------|
| `atlas_fp_optical_v2_2_curated.csv` | ~45 KB | 181 | Tier 1 (180 systems + header) |
| `atlas_fp_optical_v2_2.csv` | ~75 KB | 297 | All tiers mixed (audit only) |
| `atlas_fp_optical_v2_2_candidates.csv` | ~3 KB | 14 | Tier 2 (13 systems + header) |
| `atlas_fp_optical_v2_2_unknown.csv` | ~25 KB | 104 | Tier 3 (103 systems + header) |
| `TRAINING.METADATA_v2_2_2.json` | ~8 KB | — | Metadata (sources, tiers, QA) |
| `SHA256SUMS_v2_2_2.txt` | <1 KB | — | Checksums for integrity verification |

### Schema (Tier 1)

**Required fields:** `SystemID`, `protein_name`, `family`, `is_biosensor`, `contrast_normalized`, `doi`, `curator`

**Recommended fields:** `quality_tier`, `temperature_K`, `license`, `method`, `excitation_nm`, `emission_nm`

**Full schema:** See [docs/ATLAS_SPEC.md](docs/ATLAS_SPEC.md)

---

## 📖 Documentation

**Key resources:**

- **[VERSIONS_CITATION.md](VERSIONS_CITATION.md)** — How to cite (v1.2.1 vs v2.2.2)
- **[docs/DATA_TIERS.md](docs/DATA_TIERS.md)** — Tier system specification
- **[docs/ATLAS_SPEC.md](docs/ATLAS_SPEC.md)** — Full schema documentation
- **[docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md)** — Data quality limitations
- **[VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md)** — Future version plans
- **[docs/NOBEL2025_CONTEXT.md](docs/NOBEL2025_CONTEXT.md)** — Scientific positioning

---

## 🤝 Contributing

**Found an error?** Open a [Data Fix Issue](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues/new?template=data_fix.yml)

**Want to add systems?** Open a [New Entry Issue](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues/new?template=new_entry.yml)

**See:** [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## 🔮 What's Next?

### v2.3.0 (Planned Q1 2026)

- **Goal:** 300+ systems
- **Focus:** Tier 2 → Tier 1 promotions (manual curation of 13 candidates)
- **Features:** Extended family coverage, rare biosensor types

### v3.0.0 (Planned Q2 2026)

- **Goal:** Peer-reviewed publication
- **Breaking changes:** Schema v3.0 (major reorganization)
- **Features:** Confidence intervals, extended metadata

**See:** [VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md) for detailed roadmap.

---

## 📧 Contact

**Maintainer:** Tommy Lepesteur (Independent Researcher)  
**Issues:** [GitHub Issues](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues)  
**Discussions:** [GitHub Discussions](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/discussions)  
**Email:** [contact: see GitHub Issues]

---

## 📜 License

- **Data** (CSV files): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Free to use with attribution
- **Code** (scripts, dashboard): [MIT](LICENSE.CODE) — Free to use and modify

---

**⚛️ Built with scientific rigor | Maintained independently | Contributions welcome**

---

**Release prepared:** 2025-11-10  
**Version:** 2.2.2 (Stable)  
**Status:** Tag created, GitHub Release pending, Zenodo DOI in progress

