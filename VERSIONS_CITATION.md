# Version Citation Guide - Biological Qubits Atlas

**Last updated:** 2026-04-17  
**Purpose:** instructions for citing the correct atlas version based on your use case.

---

## Quick decision tree

```
                Which version should I cite?
                            |
      +---------------------+---------------------+
      |                                           |
      v                                           v
  Citing the Frontiers                  Using atlas data for
  manuscript?                           research, ML, or clinical
                                        context in 2026+?
      |                                           |
      v                                           v
   v1.2.1                                     v3.0.0
   (FROZEN)                                   (ACTIVE)
   66 systems                                 82 qubits + 195 FP biosensors
   DOI: 10.5281/zenodo.17420604               DOI: 10.5281/zenodo.19617435
```

---

## Version comparison

| Aspect | v1.2.1 (Frontiers) | v2.2.2 (deprecated) | v3.0.0 (current) |
|--------|--------------------|---------------------|------------------|
| Status | Frozen (immutable) | Deprecated | Active |
| Qubits | 66 legacy systems (mixed atlas) | 34 qubits | 82 qubits (classes A, A', B, C, D) |
| FP biosensors | n/a | 180 curated + 13 + 103 | 195 curated |
| Purpose | Manuscript publication | Superseded reference | Research, ML, clinical context |
| DOI | [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604) | n/a | [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435) (concept DOI [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603)) |
| Main files | `atlas_fp_optical_v1_2_1.csv` | `atlas_fp_optical_v2_2_curated.csv` | `biological_qubits_v3.csv`, `atlas_fp_optical_v3_curated.csv` |
| Release date | 2025-10-23 | 2025-10-26 | 2026-04-17 |
| Use case | Cite Frontiers manuscript | Historical compatibility | ML pipelines, computational design, clinical context |
| Modifications | Never modified (reproducibility) | n/a | May receive patches (v3.0.1, etc.) |

---

## When to Use v1.2.1 (Frontiers)

### ✅ Use v1.2.1 if:

- You are **citing the Frontiers manuscript** specifically
- You need a **frozen dataset** guaranteed never to change
- You are **replicating published results** from the manuscript
- You need a **citable DOI** immediately (Zenodo-archived)

### 📥 How to Download v1.2.1

```bash
# Direct download from GitHub release
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/releases/download/v1.2.1/atlas_fp_optical_v1_2_1.csv

# Or from Zenodo (permanent archive)
wget https://zenodo.org/record/17420604/files/atlas_fp_optical_v1_2_1.csv
```

### 📝 How to Cite v1.2.1

**BibTeX:**

```bibtex
@dataset{biological_qubits_atlas_v1_2_1,
  title  = {Biological Qubits \& Quantum Sensors Atlas v1.2.1 (Frontiers Submission)},
  author = {Lepesteur, Tommy},
  year   = {2025},
  month  = {October},
  version = {1.2.1},
  systems = {66},
  doi    = {10.5281/zenodo.17420604},
  url    = {https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology}
}
```

**Plain text:**

> Lepesteur, T. (2025). *Biological Qubits & Quantum Sensors Atlas v1.2.1* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17420604

**In-text:**

> Data were obtained from the Biological Qubits Atlas v1.2.1 (Lepesteur, 2025), a curated database of 66 quantum-compatible systems for biological applications.

---

## When to use v3.0.0 (current)

### Use v3.0.0 if:

- You need the **consolidated qubits dataset** (82 systems, class A, A', B, C, D).
- You train ML models or run analyses that benefit from the **2024-2026 literature** refresh.
- You need class A' (direct ODMR FP-qubits) or the new non-optical benchmarks (SiC alkene, hBN, FND, first-in-human HP 13C,15N2-urea).
- You build downstream tools such as `fp-qubit-design` or `ising-life-lab`.

### Important notes for v3.0.0

1. Canonical qubits file: `data/qubits/biological_qubits_v3.csv` (follows `data/qubits/SCHEMA_v3.md`).
2. Canonical FP atlas: `data/optical/curated/atlas_fp_optical_v3_curated.csv` (mirrored in `data/processed/`).
3. Zenodo DOI: [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435); concept DOI (all versions): [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603).
4. Legacy CSVs remain accessible under `data/qubits/archive/pre_v3/` for reproducibility.

### How to download v3.0.0

```bash
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/qubits/biological_qubits_v3.csv
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/optical/curated/atlas_fp_optical_v3_curated.csv
```

### How to cite v3.0.0

BibTeX:

```bibtex
@dataset{biological_qubits_atlas_v3_0_0,
  title   = {Biological Qubits and Quantum Sensors Atlas v3.0.0},
  author  = {Lepesteur, Tommy},
  year    = {2026},
  month   = {April},
  version = {3.0.0},
  systems = {82 qubits + 195 FP biosensors},
  doi     = {10.5281/zenodo.19617435},
  url     = {https://doi.org/10.5281/zenodo.19617435}
}
```

Plain text:

> Lepesteur, T. (2026). *Biological Qubits and Quantum Sensors Atlas v3.0.0* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19617435

In-text:

> We used the Biological Qubits Atlas v3.0.0 (Lepesteur, 2026), containing 82 qubits (classes A, A', B, C, D) and 195 curated FP biosensors with full provenance tracking.

For cross-version stability use the concept DOI `10.5281/zenodo.17420603`, which always resolves to the latest released version.

---

## Data tier explanation (v3.0.0, FP atlas)

| Tier | Count | Description | File | Modelling use |
|------|-------|-------------|------|---------------|
| Tier 1 (curated) | 195 | Known family + DOI + (spectra OR contrast > 1.5) | `atlas_fp_optical_v3_curated.csv` | Recommended |
| Tier 2 (candidates) | ~13 | Real systems, incomplete metadata | `atlas_fp_optical_v2_2_candidates.csv` | Manual curation queue |
| Tier 3 (unknown) | ~103 | Auto-harvested, placeholder data | `atlas_fp_optical_v2_2_unknown.csv` | Transparency only |

For downstream analysis (ML, computational design), use Tier 1 exclusively to avoid placeholder noise.

Full documentation: see [docs/DATA_TIERS.md](docs/DATA_TIERS.md).

---

## Migration guide: v2.2.2 -> v3.0.0

Breaking changes:
- Canonical qubit CSV moves from `data/qubits/biological_qubits.csv` to `data/qubits/biological_qubits_v3.csv`.
- `Classe` now accepts `A_prime` in addition to `A`, `B`, `C`, `D`.
- FP atlas exposes new required-ish columns (`year`, `name_normalized`) already present since v2.2.
- Temperature validator range widened to 1-400 K (previously 4-400 K) to accommodate 2 K silicon donor benchmarks.

Migration steps:

```python
import pandas as pd

qubits = pd.read_csv('data/qubits/biological_qubits_v3.csv')
fp = pd.read_csv('data/optical/curated/atlas_fp_optical_v3_curated.csv')
```

Full change log: [`RELEASE_NOTES_v3.0.md`](RELEASE_NOTES_v3.0.md).

---

## Dual versioning policy

Scientific reproducibility requires frozen datasets for publications, while active research benefits from growing databases. The atlas therefore maintains three coexisting references:
- v1.2.1 - frozen, cited in the Frontiers manuscript.
- v2.2.2 - deprecated but preserved under `archive/` and in the git history.
- v3.0.0 - active, growing, citable via [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435).

Precedent: similar to TCGA (cancer genomics), UniProt (proteins), PDB (structures), all of which maintain versioned releases alongside "current" data.

---

## Zenodo DOI status

### v1.2.1 (available)
- DOI: [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604).
- Status: archived, permanent, citable.
- Files: `atlas_fp_optical_v1_2_1.csv`, metadata, checksums.

### v3.0.0 (archived)
- DOI: [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435).
- Concept DOI (all versions): [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603).
- Files archived: source zip (`Quantum-Sensors-Qubits-in-Biology-v3.0.0.zip`, 3.1 MB) containing `biological_qubits_v3.csv`, `atlas_fp_optical_v3_curated.csv`, schema, release notes, metadata.

Track progress: see the citation section of [`README.md`](README.md).

---

## Frequently asked questions

Q: Can I use v3.0.0 without a DOI?  
A: Yes. GitHub releases are stable and citable; the DOI will be appended retroactively once the Zenodo deposit is complete.

Q: Should I use the "mixed" FP file?  
A: No. Use `atlas_fp_optical_v3_curated.csv` (Tier 1) for modelling. The mixed file still contains placeholder rows.

Q: What if I need more than 82 qubits?  
A: Class-specific staging pulls are welcome via pull request. See `scripts/etl/enrich_v3_literature_2024_2026.py` for the pattern.

Q: Will v1.2.1 ever be updated?  
A: No. v1.2.1 is frozen for reproducibility. Critical errors would trigger v1.2.2; the v1.2.1 file itself is immutable.

Q: How often will v3.0.x update?  
A: Minor patches (v3.0.1, v3.0.2) for bug fixes and late literature additions as needed. See [VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md).

---

## Contact and Support

**Questions about citation:** Open a [GitHub Issue](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues) with label `documentation`  
**Report data errors:** Use [Data Fix Template](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/issues/new?template=data_fix.yml)  
**General discussion:** [GitHub Discussions](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/discussions)

---

## Related Documentation

- **[README.md](README.md)** — Project overview
- **[DATA_TIERS.md](docs/DATA_TIERS.md)** — Tier system specification
- **[VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md)** — Future version plans
- **[CHANGELOG.md](CHANGELOG.md)** — Detailed version history
- **[NOBEL2025_CONTEXT.md](docs/NOBEL2025_CONTEXT.md)** — Scientific positioning

---

**Maintained by:** Independent researcher  
**License:** Data (CC BY 4.0), Code (MIT)  
**Contributions:** See [CONTRIBUTING.md](CONTRIBUTING.md)

