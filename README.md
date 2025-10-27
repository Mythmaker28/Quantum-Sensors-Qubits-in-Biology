# ⚛️ Biological Qubits & Quantum Sensors Atlas

[![Version (latest)](https://img.shields.io/badge/version-v2.2.2-blue.svg)](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases)
[![Stable (Frontiers)](https://img.shields.io/badge/frontiers-v1.2.1-lightgrey.svg)](#citation)
[![Systems (v2.2.2)](https://img.shields.io/badge/systems-250-green.svg)](#whats-inside)
[![Systems (v1.2.1)](https://img.shields.io/badge/systems-66-lightgrey.svg)](#citation)

🔗 [**Live Dashboard**](https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/) | 📊 [Data](data/processed/atlas_fp_optical_v2_2.csv) | 📖 [Full Documentation](DOCUMENTATION.md) | 🔀 [Version switch: v1.2.1 | v2.0 | v2.2.2](#citation)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17420604.svg)](https://doi.org/10.5281/zenodo.17420604)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![FAIR](https://img.shields.io/badge/FAIR-12/12-green?style=for-the-badge)](metadata/fair/)

> **Curated database of quantum systems (qubits, sensors, fluorescent proteins) used in biological contexts** — from ODMR-controlled NV centers to calcium biosensors with quantum optical properties.

---

## 🚀 Quick Start

### Explore the Data

```bash
# Interactive Dashboard (recommended)
https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/

# Download Dataset (latest v2.2.2)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2.csv
```

### Use in Your Research

```python
import pandas as pd

# Load atlas (latest v2.2.2)
df = pd.read_csv('atlas_fp_optical_v2_2.csv')

# Filter controlled qubits (ODMR)
qubits = df[df['method'].str.contains('ODMR', na=False)]

# Get calcium sensors
ca_sensors = df[df['family'] == 'Calcium']
```

---

## 📊 What's Inside

| Category | Count | Examples |
|----------|-------|----------|
| **Voltage Sensors** | 35 | ASAP3, Archon1, ArcLight |
| **Calcium Sensors** | 38 | GCaMP8, XCaMP, jRGECO |
| **NV Centers** | 12 | Diamond nanoparticles (ODMR) |
| **Neurotransmitters** | 15 | iGABASnFR, GRAB-ACh, dLight |
| **Other Biosensors** | 23 | pH, ATP, glutamate, H2O2 |

**Total: 250 systems** (latest v2.2.2) with full provenance (DOI, temperature, contrast, coherence time when applicable)

---

## 🎯 Key Features

✅ **FAIR 12/12** — Findable, Accessible, Interoperable, Reusable  
✅ **Full Provenance** — Source DOI/PMCID for every data point  
✅ **Interactive Dashboard** — D3.js visualizations with real-time filtering  
✅ **Normalized Data** — Temperature (K), contrast (fold-change), coherence (µs)  
✅ **Quality Tiers** — A (peer-reviewed), B (measured but not audited)  
✅ **Bio-Relevant** — Only systems tested at 270-320K displayed by default

---

## 📁 Repository Structure

```
📦 Quantum-Sensors-Qubits-in-Biology
├── 📊 data/processed/atlas_fp_optical_v2_2.csv  # Main dataset (250 systems)
├── 🌐 docs/index.html                           # Interactive dashboard
├── 📜 DOCUMENTATION.md                          # Full technical documentation
├── 🧬 scripts/                                  # Data processing & QA
├── 📈 figures/                                  # Publication-quality plots
└── 📦 metadata/fair/                            # FAIR compliance metadata
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Adding new systems
- Updating existing data
- Reporting errors

**Quick contribution:**
1. Fork this repo
2. Add your system to `atlas_fp_optical_v2_2.csv`
3. Run `python qubits_linter.py` to validate
4. Submit a Pull Request

---

## 📖 Citation

**Frontiers manuscript (fixed dataset):**
> **v1.2.1** — 66 systems (for manuscript submission)  
> DOI: 10.5281/zenodo.17420604  
> *This version is frozen for Frontiers publication.*

**Latest stable for development/ML:**
> **v2.2.2** — 250 systems (current stable)  
> DOI: TBD (pending Zenodo deposit)  
> *Use this version for research, ML training, and development.*

```bibtex
@dataset{biological_qubits_atlas_v2_2,
  title  = {Biological Qubits \& Quantum Sensors Atlas v2.2.2},
  author = {Mythmaker28},
  year   = {2025},
  version = {2.2.2},
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
- 📖 **Full Documentation**: [DOCUMENTATION.md](DOCUMENTATION.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues)
- 📋 **Version Roadmap**: [VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md)

---

**⚛️ Built with scientific rigor | Maintained by an independent researcher | Contributions welcome**

