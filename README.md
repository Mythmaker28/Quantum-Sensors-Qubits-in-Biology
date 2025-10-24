# ⚛️ Biological Qubits & Quantum Sensors Atlas

🔗 [**Live Dashboard**](https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/) | 📊 [Data](data/processed/atlas_fp_optical_v2_0.csv) | 📖 [Full Documentation](DOCUMENTATION.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17420604.svg)](https://doi.org/10.5281/zenodo.17420604)
[![Systems](https://img.shields.io/badge/Systems-113-blue?style=for-the-badge)](https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![FAIR](https://img.shields.io/badge/FAIR-12/12-green?style=for-the-badge)](metadata/fair/)

> **Curated database of quantum systems (qubits, sensors, fluorescent proteins) used in biological contexts** — from ODMR-controlled NV centers to calcium biosensors with quantum optical properties.

---

## 🚀 Quick Start

### Explore the Data

```bash
# Interactive Dashboard (recommended)
https://mythmaker28.github.io/Quantum-Sensors-Qubits-in-Biology/

# Download Dataset
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_0.csv
```

### Use in Your Research

```python
import pandas as pd

# Load atlas
df = pd.read_csv('atlas_fp_optical_v2_0.csv')

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
| **Calcium Sensors** | 28 | GCaMP8, jGCaMP8, XCaMP |
| **NV Centers** | 12 | Diamond nanoparticles (ODMR) |
| **Neurotransmitters** | 15 | iGABASnFR, GRAB-ACh, dLight |
| **Other Biosensors** | 23 | pH, ATP, glutamate, H2O2 |

**Total: 113 systems** with full provenance (DOI, temperature, contrast, coherence time when applicable)

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
├── 📊 data/processed/atlas_fp_optical_v2_0.csv  # Main dataset (113 systems)
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
2. Add your system to `atlas_fp_optical_v2_0.csv`
3. Run `python qubits_linter.py` to validate
4. Submit a Pull Request

---

## 📖 Citation

If you use this atlas in your research, please cite:

```bibtex
@dataset{biological_qubits_atlas_2025,
  title  = {Biological Qubits \& Quantum Sensors Atlas},
  author = {Mythmaker28},
  year   = {2025},
  doi    = {10.5281/zenodo.17420604},
  url    = {https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology}
}
```

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

---

**⚛️ Built with scientific rigor | Maintained by an independent researcher | Contributions welcome**

