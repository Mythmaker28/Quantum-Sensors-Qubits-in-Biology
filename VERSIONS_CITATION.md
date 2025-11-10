# 📚 Version Citation Guide — Biological Qubits Atlas

**Last updated:** 2025-11-10  
**Purpose:** Clear instructions for citing the correct atlas version based on your use case

---

## Quick Decision Tree

```
┌─────────────────────────────────────────────────┐
│ Which version should I cite?                    │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    Are you citing           Are you using
    the Frontiers            atlas data for
    manuscript?              research/ML?
        │                     │
        ↓                     ↓
    v1.2.1                v2.2.2
    (FROZEN)              (ACTIVE)
    66 systems            180 curated
    DOI: 10.5281/         DOI: TBD
    zenodo.17420604       (pending)
```

---

## Version Comparison Table

| Aspect | **v1.2.1** (Frontiers) | **v2.2.2** (Development/ML) |
|--------|------------------------|----------------------------|
| **Status** | 🔒 **FROZEN** (immutable) | ✨ **ACTIVE** (current stable) |
| **Systems Count** | 66 | 180 curated + 13 candidates + 103 unknown |
| **Purpose** | Manuscript publication | Research, ML training, downstream analysis |
| **Data Quality** | Curated, peer-review ready | Tier 1 (180 curated), Tier 2 (13 incomplete), Tier 3 (103 placeholders) |
| **DOI** | ✅ [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604) | ⏳ **TBD** (Zenodo deposit in progress) |
| **Main File** | `atlas_fp_optical_v1_2_1.csv` | `atlas_fp_optical_v2_2_curated.csv` |
| **Release Date** | 2025-10-23 | 2025-10-26 (tag exists, release pending) |
| **Use Case** | Cite in publications referencing Frontiers manuscript | ML pipelines, computational design, research analysis |
| **Modifications** | ❌ Never modified (reproducibility) | ✅ May receive patches (v2.2.3, etc.) |

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

## When to Use v2.2.2 (Development/ML)

### ✅ Use v2.2.2 if:

- You are **training machine learning models** (180 curated systems, no placeholders)
- You need the **latest curated data** for research
- You are **building downstream tools** (e.g., fp-qubit-design)
- You want **balanced dataset** for computational analysis
- You need **100% optical coverage** (all systems have spectral data or measured contrast)

### ⚠️ Important Notes for v2.2.2

1. **Use Tier 1 (curated) ONLY** for modeling/ML:
   - File: `data/processed/atlas_fp_optical_v2_2_curated.csv` (180 systems)
   - **Avoid** `atlas_fp_optical_v2_2.csv` (mixed, includes 103 placeholders)

2. **DOI is TBD:** Zenodo deposit in progress. Check [README.md](README.md) for updates.

3. **May receive patches:** v2.2.3, v2.2.4 for bug fixes (backward compatible)

### 📥 How to Download v2.2.2

```bash
# Recommended: Curated tier ONLY (modeling-ready)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2_curated.csv

# Full dataset (all tiers mixed, audit purposes only)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/atlas_fp_optical_v2_2.csv

# Verify integrity (SHA256 checksums)
wget https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/raw/main/data/processed/SHA256SUMS_v2_2_2.txt
sha256sum -c SHA256SUMS_v2_2_2.txt
```

### 📝 How to Cite v2.2.2

**BibTeX (temporary, until DOI minted):**

```bibtex
@dataset{biological_qubits_atlas_v2_2_2,
  title  = {Biological Qubits \& Quantum Sensors Atlas v2.2.2 (Curated)},
  author = {Lepesteur, Tommy},
  year   = {2025},
  month  = {October},
  version = {2.2.2-curated},
  systems = {180},
  note   = {DOI pending Zenodo deposit},
  url    = {https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology}
}
```

**Plain text:**

> Lepesteur, T. (2025). *Biological Qubits & Quantum Sensors Atlas v2.2.2 (Curated)* [Data set]. GitHub. https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology (DOI: TBD)

**In-text:**

> We used the Biological Qubits Atlas v2.2.2 curated tier (Lepesteur, 2025), comprising 180 modeling-ready systems with full provenance tracking.

**⚠️ Once DOI is minted:** Update citations to include `doi = {10.5281/zenodo.XXXXXXX}` and replace GitHub URL with Zenodo permanent link.

---

## Data Tier Explanation (v2.2.2)

Understanding the tier system is critical for proper usage:

| Tier | Count | Description | File | Modeling Use |
|------|-------|-------------|------|--------------|
| **Tier 1: CURATED** | 180 | Known family + DOI + (spectra OR contrast>1.5) | `atlas_fp_optical_v2_2_curated.csv` | ✅ **RECOMMENDED** |
| **Tier 2: CANDIDATES** | 13 | Real systems, incomplete metadata | `atlas_fp_optical_v2_2_candidates.csv` | ⚠️ Manual curation queue |
| **Tier 3: UNKNOWN** | 103 | Auto-harvested, placeholder data | `atlas_fp_optical_v2_2_unknown.csv` | ❌ **AVOID** (transparency only) |

**For downstream analysis (ML, computational design):** Use **Tier 1 exclusively** to avoid placeholder noise.

**Full documentation:** See [docs/DATA_TIERS.md](docs/DATA_TIERS.md)

---

## Migration Guide: v1.2.1 → v2.2.2

### Schema Compatibility

✅ **Backward compatible:** All columns from v1.2.1 present in v2.2.2  
✅ **No breaking changes:** Code written for v1.2.1 will work with v2.2.2  
⚠️ **New columns added:** v2.2.2 includes additional metadata (e.g., `quality_tier`, `curator`)

### What Changed

**Data expansion:**
- v1.2.1: 66 systems (all curated)
- v2.2.2: 180 curated + 116 staging (13 candidates + 103 unknown)

**New features:**
- Explicit tier classification (Tier 1/2/3)
- 100% optical coverage (excitation/emission or contrast>1.5 for all Tier 1)
- Balanced family distribution (30 families represented)
- Enhanced provenance tracking (curator field)

**Migration steps:**

```python
# Old code (v1.2.1)
import pandas as pd
df = pd.read_csv('atlas_fp_optical_v1_2_1.csv')

# New code (v2.2.2, Tier 1 only)
df = pd.read_csv('atlas_fp_optical_v2_2_curated.csv')

# No other changes needed (schema compatible)
```

---

## Dual Versioning Policy

### Why Two Versions Coexist?

**Scientific reproducibility** requires frozen datasets for publications, while **active research** benefits from growing databases.

**Solution:** Maintain both simultaneously:
- **v1.2.1:** Frozen forever (cited in Frontiers manuscript)
- **v2.2.2:** Active development (receives updates, patches)

**Precedent:** Similar to TCGA (cancer genomics), UniProt (protein database), PDB (protein structures) — all maintain versioned releases alongside "current" data.

---

## Zenodo DOI Status

### v1.2.1 (AVAILABLE)

✅ **DOI:** [10.5281/zenodo.17420604](https://doi.org/10.5281/zenodo.17420604)  
✅ **Status:** Archived, permanent, citable  
✅ **Files:** `atlas_fp_optical_v1_2_1.csv`, metadata, checksums

### v2.2.2 (IN PROGRESS)

⏳ **DOI:** TBD (Zenodo deposit being prepared)  
⏳ **Expected:** Q4 2025  
⏳ **Files planned:** `atlas_fp_optical_v2_2_curated.csv`, all tiers, training metadata, checksums

**Track progress:** Check [README.md](README.md) "Citation" section for updates.

---

## Frequently Asked Questions

### Q: Can I use v2.2.2 without a DOI?

**A:** Yes. GitHub releases are stable and citable. The DOI will be added retroactively once Zenodo deposit is complete. Your citation will remain valid (just update DOI field later).

### Q: Should I use the "mixed" file (296 systems) for ML?

**A:** **No.** Use `atlas_fp_optical_v2_2_curated.csv` (180 systems) only. The mixed file includes 103 placeholder systems (family="Unknown", contrast=1.0) that introduce noise.

### Q: What if I need more than 180 systems?

**A:** Consider Tier 2 candidates (13 systems) — real systems with incomplete metadata. Requires manual verification. See [docs/STAGING_GUIDE.md](docs/STAGING_GUIDE.md).

### Q: Will v1.2.1 ever be updated?

**A:** **No.** v1.2.1 is frozen for reproducibility. Critical errors (if discovered) would trigger v1.2.2, but v1.2.1 file itself never changes.

### Q: How often does v2.2.2 update?

**A:** Minor patches (v2.2.3, v2.2.4) for bug fixes as needed. Next minor version (v2.3.0) planned for 300+ systems. See [VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md).

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

