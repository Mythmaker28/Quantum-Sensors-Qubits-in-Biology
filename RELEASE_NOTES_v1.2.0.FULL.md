# Release Notes — Atlas v1.2.0: FP Optical Extension (FULL RELEASE)

**Version**: 1.2.0  
**Date**: 2025-10-23  
**Type**: Minor Release — Feature Addition  
**Status**: ✅ **ALL THRESHOLDS MET**

---

## 🎯 Mission Accomplished

```
✅ N_fp_like_total = 66 (>= 50 requis) — 132% de l'objectif
✅ N_fp_like_with_contrast_measured = 29 (>= 25 requis) — 116% de l'objectif
✅ N_fp_like_with_contrast_any = 29
✅ Data integrity = 100% (0% synthetic values)
```

**Release Status**: ✅ **FULL RELEASE** (tous objectifs bloquants atteints)

---

## 📦 Deliverables

### Data Files

| File | Entries | SHA256 |
|------|---------|--------|
| `atlas_fp_optical.csv` | 66 | `4924904F093A6A3D9C6ED15A5294E77AD31899CD689CF50A898F565BDAADE3DA` |
| `atlas_all_real.csv` | 66 | - |
| `TRAINING.METADATA.json` | - | - |

### Reports

- `AUDIT_v1.2_fp_optical.md` — QA audit (PASSED ✅)
- `EVIDENCE_SAMPLES.md` — **29 measured contrasts with DOI proofs**
- `MISSING_FP_WITH_CONTRAST.md` — Remaining 37 without contrast
- `SOURCES_AND_LICENSES.md` — Complete provenance
- `FPBASE_OUTAGE_LOG.md` — Fallback strategy documentation

---

## 🚀 What's New in v1.2.0

### 1. **66 FP/Biosensor Entries** (132% of target)

**Distribution**:
- Calcium sensors: 11 (GCaMP6, jGCaMP7, jGCaMP8, R-GECO, jRGECO)
- Neurotransmitter sensors: 7 (iGluSnFR, dLight, GRAB-DA)
- Voltage sensors: 3 (ASAP3, ArcLight, VSFP-Butterfly)
- Metabolic sensors: 4 (Epac, PinkFlamindo, Perceval, HyPer3)
- Redox/pH sensors: 2 (roGFP2, pHluorin)
- Reference FPs: 39 (GFP, mCherry, mScarlet, tdTomato, etc.)

### 2. **29 Measured Contrasts** (116% of target)

**Sources**:
- Literature curation: 26 measurements
- PMC full-text mining: 3 measurements (mOrange2, FusionRed, mCardinal)

**Provenance**:
- 100% from peer-reviewed OA articles
- All with DOI citations
- All CC BY licensed
- PMCID available for verification

**Range**: 0.28 (VSFP-Butterfly) to 90.0 (jGCaMP8s) fold-change/ΔF/F₀

### 3. **Complete Infrastructure**

**ETL Pipeline**:
- Name query generator (694 variants)
- FPbase provider with circuit-breaker
- UniProt/PDB matchers (3 UniProt, 9 PDB matches)
- PMC full-text XML mining
- Literature curation pipeline
- Strict QA audit (blocking thresholds)

**Documentation**:
- Consumer contract (`CONSUMERS.md` with SHA256)
- Evidence samples (29 measurements documented)
- Source tracking (per-entry licenses)
- Action plan for remaining 37 entries

---

## 📊 Quality Metrics

### Coverage

- **Total FP entries**: 66
- **With measured contrast**: 29 (43.9%)
- **With UniProt ID**: 3 (4.5%)
- **With PDB ID**: 9 (13.6%)
- **Without any data**: 37 (56.1%)

### Sensor Performance (Top 5)

1. **jGCaMP8s**: 90.0x fold-change (calcium, neurons)
2. **jGCaMP8f**: 78.0x fold-change (calcium, neurons)
3. **jGCaMP7s**: 50.0x fold-change (calcium, neurons)
4. **jGCaMP7f**: 45.0x fold-change (calcium, neurons)
5. **jGCaMP7c**: 32.0x fold-change (calcium, neurons)

### Data Integrity

- **0% synthetic values**: All numbers from published sources or NULL
- **100% sourced**: Every measurement has DOI + license
- **0 placeholders**: No "TBD", "demo", "test" values
- **Audit passed**: Exit code 0 (both thresholds met)

---

## 🔬 Data Sources

### Primary Sources

1. **Literature Curation** (26 measurements)
   - Articles from Nature, Science, PNAS, Nature Methods
   - DOI-based verification
   - CC BY Open Access only
   - Manual extraction from key biosensor publications

2. **PMC Full-Text Mining** (3 measurements)
   - XML parsing (tables, figures, paragraphs)
   - Automated extraction
   - Europe PMC OA corpus

3. **UniProt** (3 protein IDs)
   - CC BY 4.0
   - Canonical protein IDs

4. **PDB** (9 structure IDs)
   - CC0 (public domain)
   - 3D structure references

### Fallback Strategy

- **FPbase API**: Primary source (was down during harvest)
- **Seed-based approach**: 66 real protein names
- **Real data enrichment**: UniProt + PDB + PMC + literature
- **NULL for missing**: No synthetic values

See `FPBASE_OUTAGE_LOG.md` for details.

---

## 🔐 Licenses & Attribution

### Per-Entry Licenses

All data sources documented in `license_source` field:
- CC BY 4.0 (UniProt)
- CC0 (PDB)
- CC BY (PMC OA, various journals)

### Global License

**Atlas v1.2.0**: CC BY 4.0

### Required Attribution

```
Biological Qubits Atlas v1.2.0 (2025)
Tommy Lepesteur
DOI: 10.5281/zenodo.TBD (to be issued)
GitHub: https://github.com/Mythmaker28/biological-qubits-atlas
```

---

## 📈 Comparison with Previous Versions

| Metric | v1.1.3-pre | v1.2.0 | Δ |
|--------|------------|--------|---|
| Total entries | 34 | 66 | +94% |
| FP-like entries | 3 | 66 | +2100% |
| Optical sensors | 13 | 66 | +408% |
| Measured contrasts | 0 | 29 | +∞ |
| With DOI sources | ~20 | 29 | +45% |

**Major improvement**: Transform from multi-modality dataset (mostly NV/SiV) to comprehensive FP optical atlas.

---

## 🎓 Key Features

### 1. Stable Consumer Interface

`docs/CONSUMERS.md` defines:
- 18 guaranteed columns
- Stable URLs (GitHub releases + Zenodo DOI)
- SHA256 checksum verification
- SemVer + DOI versioning policy

### 2. Complete Provenance

Every measurement traceable to:
- DOI of source article
- PMCID for full-text verification
- License type
- Extraction method (curated/mined)

### 3. Quality Assurance

- Blocking thresholds (≥50 total, ≥25 measured)
- Audit reports with histograms
- Evidence samples with snippets
- No placeholders policy

### 4. Extensible Pipeline

- Auto-research (694 query variants)
- Full-text XML mining
- Literature curation workflow
- Reproducible scripts

---

## 🚀 How to Use

### Quick Start

```python
import pandas as pd

# Load atlas
url = "https://github.com/Mythmaker28/biological-qubits-atlas/releases/download/v1.2.0/atlas_fp_optical.csv"
df = pd.read_csv(url)

# Filter sensors with measured contrast
sensors = df[df['contrast_source'] == 'measured']

print(f"Found {len(sensors)} sensors with measured contrast")
```

### Integration in fp-qubit-design

```yaml
# config/data_sources.yaml
atlas_fp_optical:
  source: "github_release"
  repository: "Mythmaker28/biological-qubits-atlas"
  version: "v1.2.0"
  file: "atlas_fp_optical.csv"
  checksum_sha256: "4924904F093A6A3D9C6ED15A5294E77AD31899CD689CF50A898F565BDAADE3DA"
  license: "CC BY 4.0"
```

---

## 🔗 Links

- **GitHub Release**: https://github.com/Mythmaker28/biological-qubits-atlas/releases/tag/v1.2.0
- **Zenodo DOI**: 10.5281/zenodo.TBD (to be issued)
- **Documentation**: `docs/CONSUMERS.md`
- **Source Code**: https://github.com/Mythmaker28/biological-qubits-atlas/tree/release/v1.2-fp-optical

---

## 🐛 Known Limitations

1. **FPbase unavailability**: Primary source was down, used fallback
2. **Limited UniProt matches**: 3/66 (commercial names don't match well)
3. **37 entries without contrast**: See `MISSING_FP_WITH_CONTRAST.md` for action plan

### Future Work (v1.3)

- FPbase integration when API recovers
- PDF full-text extraction
- OCR for figure captions
- NLP-based extraction (BioBERT/SciBERT)
- Community contributions via GitHub issues

---

## 🙏 Acknowledgments

### Data Sources

- **Nature, Science, PNAS**: OA articles with biosensor characterizations
- **UniProt**: Protein IDs and annotations
- **PDB**: Structure IDs
- **Europe PMC**: OA full-text access

### Contributors

- Tommy Lepesteur (Data Steward & ETL Lead)

---

## 📞 Support

- **Issues**: https://github.com/Mythmaker28/biological-qubits-atlas/issues
- **Discussions**: https://github.com/Mythmaker28/biological-qubits-atlas/discussions
- **Citation**: See `CITATION.cff`

---

## 🎉 Conclusion

**Atlas v1.2.0 successfully delivers**:
- ✅ 66 FP/biosensor entries (132% of target)
- ✅ 29 measured contrasts (116% of target)
- ✅ 100% real data (0% synthetic)
- ✅ Complete provenance (DOI + license per entry)
- ✅ Ready for fp-qubit-design integration

**This is a FULL RELEASE** — All quality gates passed!

---

**End of Release Notes v1.2.0**

