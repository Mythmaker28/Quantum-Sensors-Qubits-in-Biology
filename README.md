# ⚛️ Biological Qubits & Quantum Sensors Atlas

[![Version (latest)](https://img.shields.io/badge/version-v2.2.2-blue.svg)](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases)
[![Stable (Frontiers)](https://img.shields.io/badge/frontiers-v1.2.1-lightgrey.svg)](#citation)
[![Systems (v2.2.2)](https://img.shields.io/badge/curated-180-green.svg)](#whats-inside)
[![Total](https://img.shields.io/badge/total-296-lightgrey.svg)](#data-tiers)
[![Systems (v1.2.1)](https://img.shields.io/badge/systems-66-lightgrey.svg)](#citation)

🔗 [**Live Dashboard**](https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/) | 📊 [Data](data/processed/atlas_fp_optical_v2_2_curated.csv) | 📖 [Full Documentation](DOCUMENTATION.md) | 🔀 [Version switch: v1.2.1 | v2.0 | v2.2.2](#citation)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17420604.svg)](https://doi.org/10.5281/zenodo.17420604)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![FAIR](https://img.shields.io/badge/FAIR-12/12-green?style=for-the-badge)](metadata/fair/)

> **Curated database of quantum systems (qubits, sensors, fluorescent proteins) used in biological contexts** — from ODMR-controlled NV centers to calcium biosensors with quantum optical properties.

---

## 🏆 Post-Nobel 2025 Context

The **2025 Nobel Prize in Physics** recognized pioneering work on Josephson junctions and superconducting quantum circuits—demonstrating that macroscopic engineered systems can exhibit genuine quantum behavior. This atlas extends that exploration to an orthogonal frontier: **room-temperature quantum platforms** compatible with biological contexts.

**Why this matters:** While superconducting qubits operate at ~10-50 mK, the systems catalogued here function at **270-320 K** (ambient/physiological temperatures), enabling in vivo sensing, biological imaging, and exploration of quantum effects in living systems.

📖 **[Read full context: Post-Josephson platforms and biological quantum systems →](docs/NOBEL2025_CONTEXT.md)**

---

## 🚀 Quick Start

### Explore the Data

```bash
# Interactive Dashboard (recommended)
https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/

# Download Dataset (RECOMMENDED: curated tier for modeling)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2_curated.csv

# Or full mixed dataset (includes 103 auto-harvested with placeholder data)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2.csv
```

### Use in Your Research

```python
import pandas as pd

# RECOMMENDED: Load curated tier (modeling-ready, 180 systems)
df = pd.read_csv('atlas_fp_optical_v2_2_curated.csv')

# Filter controlled qubits (ODMR)
qubits = df[df['method'].str.contains('ODMR', na=False)]

# Get calcium sensors
ca_sensors = df[df['family'] == 'Calcium']

# NOTE: Avoid 'atlas_fp_optical_v2_2.csv' (mixed, includes 103 placeholder systems)
```

---

## 🔀 Which Version Should I Use?

This atlas maintains **dual versioning** for different use cases:

| Version | Status | Systems | Use Case | DOI |
|---------|--------|---------|----------|-----|
| **v2.2.2** | ✨ **Active** | 180 curated | Research, ML, development | ⏳ TBD (pending Zenodo) |
| **v1.2.1** | 🔒 **Frozen** | 66 | Frontiers manuscript citation | ✅ [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604) |

**Quick guide:**
- 👉 **For ML/modeling:** Use v2.2.2 curated (`atlas_fp_optical_v2_2_curated.csv`)
- 👉 **For citing Frontiers manuscript:** Use v1.2.1
- 👉 **Confused?** See detailed guide: [VERSIONS_CITATION.md](VERSIONS_CITATION.md)

---

## 📊 What's Inside

**Tier 1: Curated Core (Modeling-Ready)**

| Category | Count | Examples |
|----------|-------|----------|
| **Calcium Sensors** | 40 | GCaMP8, XCaMP, jRGECO |
| **Voltage Sensors** | 22 | ASAP3, ASAP4e, ArcLight |
| **Dopamine Sensors** | 13 | dLight, GRAB-DA |
| **Glutamate Sensors** | 10 | iGluSnFR, SF-iGluSnFR |
| **Other Biosensors** | 95 | pH, ATP, GABA, cAMP, H2O2, etc. |

**180 curated systems** (Tier 1: modeling-ready) with full provenance  
+13 candidates (Tier 2: incomplete) + 103 staging/unknown (Tier 3: placeholder data)

See [Data Tiers](#data-tiers) for classification details.

---

## 🎯 Key Features

✅ **FAIR 12/12** — Findable, Accessible, Interoperable, Reusable  
✅ **Full Provenance** — Source DOI for every curated data point  
✅ **Interactive Dashboard** — D3.js visualizations with real-time filtering  
✅ **Normalized Data** — Temperature (K), contrast (fold-change), coherence (µs)  
✅ **Quality Tiers** — Explicit separation: curated vs candidates vs placeholder  
✅ **Bio-Relevant** — Systems tested at 270-320K

---

## Datasets Overview

This project contains **TWO DISTINCT datasets** for different applications:

### 1. Fluorescent Protein Atlas (Primary - 180 systems)

**File:** `data/processed/atlas_fp_optical_v2_2_curated.csv`

**Content:**
- 180 curated fluorescent protein systems (Tier 1 - modeling-ready)
- Families: Calcium (40), Voltage (22), Dopamine (13), Glutamate (10), Others (95)
- Properties: contrast (deltaF/F0), spectra, temperature, pH
- Applications: Neural imaging, biosensing, cell biology

**Quality tiers:**
- Tier 1 (180): Curated, full metadata [RECOMMENDED FOR ML/MODELING]
- Tier 2 (13): Candidates, incomplete (`data/staging/atlas_fp_optical_v2_2_candidates.csv`)
- Tier 3 (103): Staging, placeholder data (`data/staging/atlas_fp_optical_v2_2_unknown.csv`)

**Validation:** `python scripts/validate_atlas.py curated`

---

### 2. Biological Qubits Dataset (Secondary - 34 systems)

**File:** `data/qubits/biological_qubits.csv`

**Content:**
- 34 quantum systems (spin qubits, NMR, radical pairs)
- Classes: A (3 - FP with ODMR), B (15 - NV/VSi), C (12 - hyperpolarized nuclei), D (4 - radical pairs)
- Properties: T2 (coherence), T1 (relaxation), ODMR contrast
- Applications: Quantum magnetometry, thermometry, quantum sensing

**Reading methods:** ODMR, NMR, ESR

**Validation:** `python scripts/qa/validate_qubits_data.py`

**Documentation:** See `data/qubits/README.md` for detailed distinction

---

## Analysis & Reproducibility

All datasets have **functional analysis scripts** generating reproducible outputs:

```bash
# FP Atlas statistics
python analysis/descriptive_stats.py       # Overall stats (180 systems)
python analysis/class_comparisons.py       # Family comparisons (30 families)

# Qubits statistics  
python analysis/qubits_stats.py            # Qubit stats (34 systems)
python analysis/qubits_class_comparisons.py # Class A/B/C/D comparisons

# Outputs generated in analysis/output/ (JSON + Markdown)
```

---

## Repository Structure

```
Quantum-Sensors-Qubits-in-Biology
├── data/processed/
│   ├── atlas_fp_optical_v2_2.csv         # Full FP dataset (296 systems, mixed)
│   └── atlas_fp_optical_v2_2_curated.csv # [RECOMMENDED] Tier 1 (180 systems)
├── data/qubits/
│   ├── biological_qubits.csv             # Qubits dataset (34 systems)
│   └── README.md                         # Explains FP vs qubits distinction
├── data/staging/
│   ├── atlas_fp_optical_v2_2_candidates.csv  # Tier 2 (13 systems)
│   ├── atlas_fp_optical_v2_2_unknown.csv     # Tier 3 (103 systems)
│   └── candidates_needing_curation.csv       # API harvest queue (844)
├── analysis/
│   ├── qubits_stats.py, class_comparisons.py # Functional analysis scripts
│   └── output/                               # Reproducible JSON/Markdown outputs
├── docs/
│   ├── index.html                            # Interactive dashboard
│   ├── ATLAS_SPEC.md                         # Dataset schema & criteria
│   ├── DATA_TIERS.md                         # Quality tier definitions
│   ├── quantum_mechanisms.md                 # Quantum physics documentation
│   └── [photosynthesis, magnetoreception, nv_centers_qubits].md
├── scripts/
│   ├── validate_atlas.py                     # FP validation tool
│   ├── qa/validate_qubits_data.py            # Qubits validation tool
│   ├── qa/split_tiers.py                     # Reproducible tier splitting
│   └── web/regenerate_dashboard.py           # Dashboard generator
├── DOCUMENTATION.md                          # Full technical documentation
├── figures/                                  # Publication-quality plots
└── metadata/fair/                            # FAIR compliance metadata
```

---

## 📊 Data Tiers

The atlas uses **explicit quality tiers** to separate curated data from auto-harvested placeholders:

| Tier | Count | Description | File | Use Case |
|------|-------|-------------|------|----------|
| **Tier 1: CURATED** | 180 | Known family + DOI + (spectra OR contrast>1.5) | `atlas_fp_optical_v2_2_curated.csv` | ✅ **Modeling, analysis** |
| **Tier 2: CANDIDATES** | 13 | Real systems, incomplete metadata | `atlas_fp_optical_v2_2_candidates.csv` | Manual curation queue |
| **Tier 3: UNKNOWN** | 103 | Auto-harvested, placeholder data | `atlas_fp_optical_v2_2_unknown.csv` | Transparency only |

**For machine learning / quantitative analysis:** Use **Tier 1 (curated)** only.

**Why the split?**  
During API harvesting (UniProt, FPbase), 103 systems were auto-added with `family="Unknown"` and `contrast_normalized=1.0` (placeholder). These introduce noise in models and are now explicitly isolated.

See [docs/DATA_TIERS.md](docs/DATA_TIERS.md) for complete tier definitions.

---

## 🔗 Related Projects

This atlas is part of a broader ecosystem exploring quantum-inspired and quantum-compatible biological platforms:

### [fp-qubit-design](https://github.com/Mythmaker28/fp-qubit-design)
**Computational design of fluorescent protein mutants** — Uses atlas v2.2.2 curated data (180 systems) as training source for ML-guided protein engineering. Predicts spectral properties and dynamic range of novel biosensor variants.

### [arrest-molecules](https://github.com/Mythmaker28/arrest-molecules)
**Molecular arrest framework** — Theoretical framework for dampening compounds in biological regulation (10 compounds, 44 predictions, DOI: [10.5281/zenodo.17420685](https://doi.org/10.5281/zenodo.17420685)). Shares conceptual vocabulary with quantum metastability: energy landscapes, arrest kinetics, tunneling vs. activation barriers.

### [ising-life-lab](https://github.com/Mythmaker28/ising-life-lab)
**Computational sandbox for memory and energy landscapes** — Explores emergent properties in biological networks using Ising-inspired models. Principles of metastable states and network connectivity connect to quantum decoherence dynamics catalogued in this atlas.

**Conceptual bridge:** Superconducting circuits (Nobel 2025) → Artificial quantum systems (this atlas) → Quantum-inspired biological computation (ising-life-lab) → Molecular design (fp-qubit-design, arrest-molecules).

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Adding new systems
- Updating existing data
- Reporting errors

**Quick contribution:**
1. Fork this repo
2. Add your system to `atlas_fp_optical_v2_2_curated.csv` (Tier 1)
3. Run `python scripts/validate_atlas.py curated` to validate
4. Submit a Pull Request

---

## 🛠️ Local Usage & Validation

### Validate Dataset

```bash
# Validate curated tier (recommended, strict)
python scripts/validate_atlas.py curated

# Validate full mixed dataset
python scripts/validate_atlas.py mixed

# Validate individual tiers
python scripts/validate_atlas.py candidates
python scripts/validate_atlas.py unknown
```

**Tier splitting (reproducible):**
```bash
python scripts/qa/split_tiers.py
```

This checks for:
- Missing required columns
- Invalid data ranges (temperature 270-320K, contrast > 0)
- DOI format validation
- Data completeness report

### Run Static Site Locally

```bash
# Option 1: Python HTTP server
python -m http.server 8000

# Option 2: Node.js (if available)
npx http-server .

# Then open: http://localhost:8000/docs/index.html
```

### Enable GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Select source: **Deploy from a branch**
3. Branch: **`main`** / Folder: **`/ (root)`** or **`/docs`**
4. Save and wait ~2 minutes
5. Your site will be live at: `https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/`

**Note:** If using `/` as root, GitHub Pages will automatically redirect `/` to `/docs/index.html` if present.

---

## 📖 Citation

**Frontiers manuscript (fixed dataset):**
> **v1.2.1** — 66 systems (for manuscript submission)  
> DOI: 10.5281/zenodo.17420604  
> *This version is frozen for Frontiers publication.*

**Latest stable for development/ML:**
> **v2.2.2 (curated)** — 180 systems (modeling-ready, validated)  
> DOI: TBD (pending Zenodo deposit)  
> *Use this version for research, ML training, and development.*

**Full dataset (mixed tiers):**
> **v2.2.2 (mixed)** — 296 systems (includes 103 placeholder/staging)  
> For transparency and API harvest audit only. **Not recommended for modeling.**

```bibtex
@dataset{biological_qubits_atlas_v2_2_curated,
  title  = {Biological Qubits \& Quantum Sensors Atlas v2.2.2 (Curated)},
  author = {Mythmaker28},
  year   = {2025},
  version = {2.2.2-curated},
  systems = {180},
  doi    = {TBD},
  url    = {https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology}
}
```

For the Frontiers manuscript citation (v1.2.1), see [CITATION_v1.2.1.cff](CITATION_v1.2.1.cff).

---

## 📜 License

- **Data** (CSV files): [CC BY 4.0](LICENSE) — Free to use with attribution
- **Code** (scripts, dashboard): [MIT](LICENSE.CODE) — Free to use and modify

---

## 🔗 Links

- 🌐 **Live Dashboard**: https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/
- 📦 **Zenodo Archive**: https://doi.org/10.5281/zenodo.17420604
- 📖 **Data Tiers**: [docs/DATA_TIERS.md](docs/DATA_TIERS.md)
- 📖 **Full Documentation**: [DOCUMENTATION.md](DOCUMENTATION.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues)
- 📋 **Version Roadmap**: [VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md)

---

**⚛️ Built with scientific rigor | Maintained by an independent researcher | Contributions welcome**
