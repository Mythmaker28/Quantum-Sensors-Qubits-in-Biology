# Biological Qubits and Quantum Sensors Atlas

[![Version (latest)](https://img.shields.io/badge/version-v4.0.0-blue.svg)](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases)
[![Stable (Frontiers)](https://img.shields.io/badge/frontiers-v1.2.1-lightgrey.svg)](#citation)
[![Qubits (v3.0)](https://img.shields.io/badge/qubits-82-green.svg)](#whats-inside)
[![FP biosensors (v3.0)](https://img.shields.io/badge/FP%20biosensors-195-green.svg)](#whats-inside)
[![Classes](https://img.shields.io/badge/classes-A%2FA%E2%80%B2%2FB%2FC%2FD-blueviolet.svg)](#data-tiers)

[Live Dashboard](https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/) | [Qubits dataset](data/qubits/biological_qubits_v3.csv) | [FP atlas](data/processed/atlas_fp_optical_v3_curated.csv) | [Full documentation](DOCUMENTATION.md) | [Release notes](RELEASE_NOTES_v4.0.md)

[![Concept DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17420603.svg)](https://doi.org/10.5281/zenodo.17420603)
[![DOI (v1.2.1, frozen)](https://zenodo.org/badge/DOI/10.5281/zenodo.17420604.svg)](https://doi.org/10.5281/zenodo.17420604)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![FAIR](https://img.shields.io/badge/FAIR-12/12-green?style=for-the-badge)](metadata/fair/)

> Curated databases of quantum systems and fluorescent biosensors used in biological contexts — from directly ODMR-controlled fluorescent proteins (Class A') and NV/SiC colour centres to calcium biosensors and radical-pair magnetoreceptors.

---

## What is new in v3.0

- **New class `A'` (A-prime): FP-qubits with direct ODMR readout.** Following the 2025 benchmarks on EYFP (Nature, DOI `10.1038/s41586-025-09417-w`) and on engineered LOV/flavin radical pairs (Nature, DOI `10.1038/s41586-025-09971-3`), fluorescent proteins are no longer only optical reporters: they have become a distinct class of biologically compatible spin qubits.
- **Single source of truth for qubits.** All legacy CSVs (v1.2.1, v2.x, v2.3 drafts) have been consolidated into `data/qubits/biological_qubits_v3.csv` (82 systems, 35 columns). Earlier files are archived under `data/qubits/archive/pre_v3/`.
- **2024 to 2026 literature refresh.** Classes B, C, D were updated with recent non-optical qubits: SiC alkene-functionalised defects, BNNT spin probes, SnV and GeV nanodiamonds, in vivo FND thermometry, hBN colour centres; first-in-human HP 13C, 15N2-urea MRI and additional FDA 129Xe trials; plus Flavin-Guanine SCRP (Comm Chem 2025) and room-temperature FMO coherence (Sci Adv 2025).
- **FP atlas extended.** Seven 2024 to 2026 biosensors added (CaBLAM, HaloDA1.0, iGluSnFR4f/s, ASAP4.4-Kv, PinkyCaMP, OCaMP). Missing licences and PMCIDs were enriched via Unpaywall and NCBI ID Converter.

See [`RELEASE_NOTES_v4.0.md`](RELEASE_NOTES_v4.0.md) for the full changelog.

---

## Post-Nobel 2025 Context

The 2025 Nobel Prize in Physics recognised pioneering work on Josephson junctions and superconducting quantum circuits, demonstrating that macroscopic engineered systems can exhibit genuine quantum behaviour. This atlas extends that exploration to an orthogonal frontier: room-temperature quantum platforms compatible with biological contexts.

Superconducting qubits operate at around 10 to 50 mK; the systems catalogued here function at 77 to 320 K (cryogenic benchmarks to physiological temperatures), enabling in vivo sensing, biological imaging and exploration of quantum effects in living systems.

[Read full context: post-Josephson platforms and biological quantum systems](docs/NOBEL2025_CONTEXT.md)

---

## Quick Start

### Explore the Data

```bash
# Interactive dashboard
https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/

# Qubits dataset (v3.0, 82 systems)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/qubits/biological_qubits_v3.csv

# FP biosensors atlas (v3.0 curated, 195 systems)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/optical/curated/atlas_fp_optical_v3_curated.csv
```

### Use in Your Research

```python
import pandas as pd

qubits = pd.read_csv('biological_qubits_v3.csv')
print(qubits['Classe'].value_counts())
# B: 31, C: 23, D: 17, A_prime: 8, A: 3

# Directly ODMR-controllable FP-qubits (new A' class)
fp_qubits = qubits[qubits['Classe'] == 'A_prime']

fp = pd.read_csv('atlas_fp_optical_v3_curated.csv')
calcium = fp[fp['family'] == 'Calcium']
```

---

## Which Version Should I Use?

This atlas maintains semantic versioning with long-lived references for legacy citations:

| Version | Status | Qubits | FP biosensors | Use case | DOI |
|---------|--------|--------|---------------|----------|-----|
| **v4.0.0** | Active | 82 | 195 curated | Research, ML, clinical context, 2024-2026 literature | [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603) (concept) |
| v3.0.0 | Restricted | 82 | 195 curated | Withdrawn on Zenodo (bundle issues); use v4.0.0 | [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435) |
| v2.2.2 | Deprecated | 34 | 180 curated | Superseded by v4.0.0 | n/a |
| v1.2.1 | Frozen | 66 | n/a | Frontiers manuscript citation | [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604) |

Quick guide:
- For current research and ML: use v4.0.0 (qubits + FP atlases).
- For citing the Frontiers manuscript: use v1.2.1.
- For a full discussion of versions and citation formats, see [`VERSIONS_CITATION.md`](VERSIONS_CITATION.md).

---

## What's Inside

### Qubits dataset (v3.0, 82 systems)

| Class | Count | Description |
|-------|-------|-------------|
| **A'** | 8 | FP-qubits with direct ODMR readout (EYFP, MagLOV/MagLOV2, mScarlet-FMN, DmCry...) |
| A | 3 | Original FP "quantum-like" biosensors |
| B | 31 | Solid-state colour centres in biocompatible hosts (NV, SiC, SnV, GeV, FND, hBN, BNNT...) |
| C | 23 | Hyperpolarised nuclei (13C, 15N, 129Xe, 31P) including first-in-human clinical trials |
| D | 17 | Radical-pair mechanisms and biological spin systems (cryptochromes, photolyases, FMO, ferredoxin...) |

### Fluorescent biosensors atlas (v3.0 curated, 195 systems)

| Category | Count | Examples |
|----------|-------|----------|
| Calcium sensors | 45+ | GCaMP8, XCaMP, jRGECO, CaBLAM, OCaMP, PinkyCaMP |
| Voltage sensors | 24+ | ASAP3, ASAP4e, ASAP4.4-Kv, Archon1, ArcLight |
| Glutamate sensors | 12+ | iGluSnFR3, iGluSnFR4f/s |
| Dopamine sensors | 14+ | dLight, GRAB-DA, HaloDA1.0 (far-red chemigenetic) |
| Other biosensors | 90+ | pH, ATP, GABA, cAMP, H2O2, serotonin, acetylcholine, bioluminescent |

---

## Key Features

- FAIR 12/12 compliance (Findable, Accessible, Interoperable, Reusable).
- Full provenance: DOI (and PMCID when available) for every curated data point.
- Interactive dashboard with real-time filtering.
- Normalised units: temperature in K, contrast in fold-change or deltaF/F, coherence in microseconds.
- Explicit quality tiers: curated (Tier 1), candidates (Tier 2), placeholder (Tier 3).
- Bio-relevant range: systems benchmarked from cryogenic controls (77-80 K) to physiological temperatures (295-320 K).

---

## Datasets Overview

This project contains two complementary datasets:

### 1. Fluorescent-biosensor atlas (v3.0 curated, 195 systems)

File: `data/optical/curated/atlas_fp_optical_v3_curated.csv` (mirrored in `data/processed/atlas_fp_optical_v3_curated.csv`).

Content:
- 195 curated biosensors (Tier 1, modelling-ready).
- Families: calcium, voltage, glutamate, dopamine, pH, ATP, GABA, cAMP, H2O2, serotonin, acetylcholine, bioluminescent, etc.
- Properties: contrast (deltaF/F0 or fold-change), excitation/emission spectra, temperature, pH.
- Applications: neural imaging, biosensing, cell biology.

New in v3.0: CaBLAM, HaloDA1.0, iGluSnFR4f, iGluSnFR4s, ASAP4.4-Kv, PinkyCaMP, OCaMP.

Validation: `python scripts/qa/analyze_atlas_quality.py --input data/optical/curated/atlas_fp_optical_v3_curated.csv`.

---

### 2. Biological qubits dataset (v3.0, 82 systems, single source of truth)

File: `data/qubits/biological_qubits_v3.csv`.

Content:
- 82 quantum systems with 35-column canonical schema (see [`data/qubits/SCHEMA_v3.md`](data/qubits/SCHEMA_v3.md)).
- Classes: A' (8, new), A (3), B (31), C (23), D (17).
- Properties: T2, T1, ODMR contrast, detection methods, hosts, references.
- Applications: quantum magnetometry, thermometry, clinical MRI, magnetoreception.

Reading methods: direct ODMR, ODMR-relay, pulsed ESR, pulsed NMR, DNP-MRI, radical-pair fluorescence.

Validation: `python scripts/qa/validate_qubits_data.py --input data/qubits/biological_qubits_v3.csv`.

Documentation: see [`data/qubits/README.md`](data/qubits/README.md) and [`data/qubits/SCHEMA_v3.md`](data/qubits/SCHEMA_v3.md).

---

## Analysis and Reproducibility

```bash
python analysis/descriptive_stats.py
python analysis/class_comparisons.py

python analysis/qubits_stats.py --input data/qubits/biological_qubits_v3.csv --version 3.0
python analysis/qubits_class_comparisons.py

# Outputs land in analysis/output/ (JSON + Markdown)
```

---

## Repository Structure (v3.0)

```
Quantum-Sensors-Qubits-in-Biology
├── data/
│   ├── qubits/
│   │   ├── biological_qubits_v3.csv          # Canonical qubits dataset (82)
│   │   ├── SCHEMA_v3.md                      # 35-column schema
│   │   ├── README.md                         # Dataset overview
│   │   └── archive/pre_v3/                   # Legacy CSVs (v1.2.1 to v2.3)
│   ├── optical/
│   │   └── curated/atlas_fp_optical_v3_curated.csv   # FP atlas (195)
│   ├── processed/
│   │   └── atlas_fp_optical_v3_curated.csv   # Mirror for tooling compatibility
│   └── staging/                              # Tier 2/3 candidates
├── analysis/
│   ├── qubits_stats.py
│   ├── qubits_class_comparisons.py
│   ├── descriptive_stats.py
│   └── output/                               # JSON + Markdown
├── docs/
│   ├── index.html                            # Interactive dashboard
│   ├── FP_QUBITS_ODMR_2025.md                # Class A' explanatory note (v3.0)
│   ├── ATLAS_SPEC.md                         # Dataset schema and criteria
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

## Data Tiers (FP atlas)

The atlas uses explicit quality tiers to separate curated data from auto-harvested placeholders:

| Tier | Count | Description | File | Use case |
|------|-------|-------------|------|----------|
| Tier 1 (curated) | 195 | Known family + DOI + (spectra OR contrast > 1.5) | `atlas_fp_optical_v3_curated.csv` | Modelling, analysis |
| Tier 2 (candidates) | ~13 | Real systems, incomplete metadata | `atlas_fp_optical_v2_2_candidates.csv` | Manual curation queue |
| Tier 3 (unknown) | ~103 | Auto-harvested, placeholder data | `atlas_fp_optical_v2_2_unknown.csv` | Transparency only |

For machine learning or quantitative analysis, use Tier 1 (curated) only.

Why the split? During API harvesting (UniProt, FPbase) about 103 systems were auto-added with `family="Unknown"` and `contrast_normalized=1.0`. They introduce noise in models and are kept isolated.

See [docs/DATA_TIERS.md](docs/DATA_TIERS.md) for complete tier definitions.

---

## 🔗 Related Projects

This atlas is part of a broader ecosystem exploring quantum-inspired and quantum-compatible biological platforms:

### [fp-qubit-design](https://github.com/Mythmaker28/fp-qubit-design)
Computational design of fluorescent protein mutants. Uses the atlas (v3.0 curated, 195 systems) as training source for ML-guided protein engineering. Predicts spectral properties, dynamic range, and ODMR contrast for the new A' class.

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

Quick contribution (v3.0 workflow):
1. Fork this repository.
2. For new FP biosensors: add the row to `data/optical/curated/atlas_fp_optical_v3_curated.csv` (Tier 1).
3. For new qubits (A, A', B, C or D): append to `data/qubits/biological_qubits_v3.csv` following [`data/qubits/SCHEMA_v3.md`](data/qubits/SCHEMA_v3.md).
4. Run the validators: `python scripts/validate_atlas.py curated` and `python scripts/qa/validate_qubits_data.py --input data/qubits/biological_qubits_v3.csv`.
5. Submit a pull request with the DOI of the primary reference.

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

Frontiers manuscript (frozen dataset):
> v1.2.1 — 66 systems (manuscript submission).  
> DOI: [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604).  
> This version is frozen for Frontiers publication.

Latest stable (research, ML, clinical context):
> v4.0.0 — 82 qubits + 195 FP biosensors (clean re-release of v3.0.0 content).  
> Concept DOI (always latest): [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603).  
> Use this version for current research, ML training, and development.  
> Note: v3.0.0 (DOI 10.5281/zenodo.19617435) is restricted on Zenodo because the bundle shipped internal artefacts and binary files with embedded author metadata; use v4.0.0 or the concept DOI instead.

```bibtex
@dataset{biological_qubits_atlas_v4_0_0,
  title   = {Biological Qubits and Quantum Sensors Atlas v4.0.0},
  author  = {Lepesteur, Tommy},
  year    = {2026},
  version = {4.0.0},
  note    = {82 qubits (classes A, A', B, C, D) + 195 curated FP biosensors},
  doi     = {10.5281/zenodo.17420603},
  url     = {https://doi.org/10.5281/zenodo.17420603}
}
```

For the frozen Frontiers manuscript citation (v1.2.1), see `CITATION.cff` (references section).

---

## 📜 License

- **Data** (CSV files): [CC BY 4.0](LICENSE) — Free to use with attribution
- **Code** (scripts, dashboard): [MIT](LICENSE.CODE) — Free to use and modify

---

## 🔗 Links

- 🌐 **Live Dashboard**: https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/
- 📦 **Zenodo (concept DOI, always latest)**: https://doi.org/10.5281/zenodo.17420603
- 📦 **Zenodo (v1.2.1, frozen Frontiers release)**: https://doi.org/10.5281/zenodo.17420604
- ⚠️ **Zenodo (v3.0.0, restricted)**: https://doi.org/10.5281/zenodo.19617435 — replaced by v4.0.0
- 📖 **Data Tiers**: [docs/DATA_TIERS.md](docs/DATA_TIERS.md)
- 📖 **Full Documentation**: [DOCUMENTATION.md](DOCUMENTATION.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues)
- 📋 **Version Roadmap**: [VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md)

---

**⚛️ Built with scientific rigor | Maintained by an independent researcher | Contributions welcome**
