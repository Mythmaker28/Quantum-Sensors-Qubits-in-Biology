# Changelog - Biological Qubits Catalog

All notable changes to the Biological Qubits Catalog will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-04-17

**Zenodo DOI:** [10.5281/zenodo.19617435](https://doi.org/10.5281/zenodo.19617435) - concept DOI [10.5281/zenodo.17420603](https://doi.org/10.5281/zenodo.17420603).

### Added
- **New class A' (A-prime): FP-qubits with direct ODMR readout.** 8 entries (EYFP at 80 K and 295 K, MagLOV, MagLOV 2, mScarlet-FMN, mCherry-FMN, mScarlet-I-FMN, DmCry) sourced from Nature 2025 and related preprints.
- **Class B refresh (+16 rows):** SiC alkene defects, BNNT spin probes, SnV / GeV nanodiamonds, FND in vivo thermometry, hBN colour centres.
- **Class C refresh (+11 rows):** first-in-human HP 13C,15N2-urea MRI, FDA 129Xe updates, HP 13C pyruvate clinical trials, 31P silicon donor benchmark.
- **Class D refresh (+13 rows):** Flavin-Guanine SCRP, 6-4 photolyase oxetane RP, room-temperature FMO coherence, GgCry4a, updated cryptochrome evidence.
- **FP biosensors atlas (+7 rows):** CaBLAM, HaloDA1.0, iGluSnFR4f, iGluSnFR4s, ASAP4.4-Kv, PinkyCaMP, OCaMP (all 2024 to 2026).
- Canonical schema documentation: `data/qubits/SCHEMA_v3.md` (35 columns).
- `docs/FP_QUBITS_ODMR_2025.md` explaining class A'.
- `RELEASE_NOTES_v3.0.md` with the complete changelog and reproducibility notes.

### Changed
- Canonical qubits CSV moved to `data/qubits/biological_qubits_v3.csv` (82 rows, single source of truth).
- Canonical FP atlas moved to `data/optical/curated/atlas_fp_optical_v3_curated.csv` (187 rows, mirrored in `data/processed/`).
- Validators updated: temperature range widened to 1-400 K, year range widened to 1980-2027, `A_prime` recognised as a valid class.
- `analysis/qubits_stats.py` accepts `--input` and `--version` and correctly reflects the dataset path in its Markdown output.
- Licences and PMCIDs enriched via Unpaywall and NCBI ID Converter: 63 licences and 60 PMCIDs automatically completed.
- README, DOCUMENTATION, VERSIONS_CITATION, VERSIONING_ROADMAP rewritten for v3.0.0.

### Deprecated
- Cry1-related rows (Cryptochrome (Cry1) - paires radicalaires, Cryptochrome 1a) flagged `deprecated` after 2025 evidence reassigned their biological role.

### Removed
- No removals. Legacy CSVs archived under `data/qubits/archive/pre_v3/` and `data/optical/curated/atlas_fp_optical_v2_2_curated.csv`.

### Fixed
- Consolidation script now fills required defaults (`Spin_type`, `Temperature_K`, `Annee`, `Qualite`, `Verification_statut`) using inference from `Methode_lecture`, `Hote_contexte`, and DOI metadata.

---

## [Unreleased]

### Planned for v3.1.0
- Promotion of Tier 2 FP biosensors to Tier 1 (manual curation).
- CI bounds for coherence times (class B) via bootstrap.
- Integration of 2026 H2 publications.

---

## [1.3.0-beta] - 2025-10-24

### Added
- **14 new systems** via hybrid curated strategy (total: 80 systems)
  - 8 from conservative literature extraction (priority DOIs)
  - 6 from specialist database cross-reference
- **New infrastructure**
  - `METHODOLOGY.md` documenting hybrid curation approach
  - `VERSIONS.md` defining version policy
  - `CHANGELOG.md` (this file) following Keep a Changelog standard
  - Evidence samples for 8 new extractions (`reports/EVIDENCE_SAMPLES_v1.3.md`)
- **Metadata improvements**
  - `TRAINING.METADATA.v1.3.json` with source breakdown
  - SHA256 checksums for all assets (`SHA256SUMS_v1.3.txt`)
- **Scripts**
  - `scripts/etl/convert_v121_to_v13.py` (schema migration)
  - `scripts/etl/extract_conservative_v13.py` (literature mining)
  - `scripts/reports/generate_metrics_v1_3.py` (automated reporting)

### Changed
- **Quality metrics**
  - N_total: 66 → 80 (+21%)
  - N_measured: 54 → 65 (+20%)
  - Quality tier B: 54 → 65 (+20%)
  - Provenance coverage: 88% (vs 90% in v1.2.1, target: >90% for stable)
- **Methodology**
  - Transitioned to hybrid approach (curated + conservative extraction)
  - Added no-merge protection for similar proteins (e.g., GCaMP6s ≠ GCaMP7s)
- **Documentation**
  - README.md: Added "Status & Versioning" section with disclaimer
  - Release notes: Clarified beta status and peer-review timeline

### Known Limitations (Beta)
- ⚠️ License audit incomplete for 8 specialist database entries
- ⚠️ No confidence intervals for 15 pre-2015 entries
- ⚠️ FPbase API outage during build (lost ~150 standard FP entries)
- ⚠️ Tier A measurements: 0 (all measurements are Tier B)

### Infrastructure
- Automated QA: `scripts/qa/audit_fp_optical_v1_3.py`
- Linter modes: Beta (warnings OK) vs Stable (warnings = errors)
- Assets: CSV, Parquet, JSON metadata, audit reports

### Fixed
- Column naming inconsistencies (`contrast_quality_tier` vs `quality_tier`)
- Unicode encoding errors in Windows (PowerShell compatibility)
- Deduplication logic (respects `config/alias.yaml` rules)

---

## [1.2.1] - 2025-10-23

### Added
- **Full provenance tracking** for all systems
  - `Source_T2`, `Source_T1`, `Source_Contraste` columns
  - Format: `DOI:10.xxxx/xxxxx Fig.X` or `PMCID:PMCxxxxxxx Table Y`
  - Coverage: 90% (60/66 systems with complete provenance)
- **Quantified uncertainties** for all measurements
  - `T2_us_err`, `T1_s_err`, `Contraste_err` columns
  - Extracted from original papers when available
  - Estimated (±20%) when not reported (flagged in notes)
- **Biological context flags**
  - `Hyperpol_flag` (hyperpolarization used: yes/no)
  - `Cytotox_flag` (cytotoxicity reported: yes/no/unknown)
  - `Temp_controlled` (temperature control: yes/no)
- **Quality control infrastructure**
  - `qubits_linter.py` — Automated linter (Python 3.8+)
  - `QC_REPORT.md` — Quality control report (regenerated on each run)
  - CI/CD integration (GitHub Actions)
- **Release assets**
  - `biological_qubits_v1.2.1.csv` (main dataset)
  - `SHA256SUMS` (integrity verification)
  - Evidence samples (20 key systems documented)
- **Documentation**
  - `CITATION.cff` (machine-readable citation metadata)
  - `zenodo.json` (Zenodo deposit metadata)
  - `RELEASE_NOTES_v1.2.0.md` (detailed release notes)

### Changed
- **Dataset expansion**
  - N_total: 21 → 66 systems (+214%)
  - N_measured: 18 → 54 (+200%)
  - Verification rate: 77% (50/66 systems verified by curator)
- **Quality distribution**
  - Tier ★★★ (Robust): 50% (33/66)
  - Tier ★★ (Solid): 31% (21/66)
  - Tier ★ (Exploratory): 19% (12/66)
- **Schema enhancements**
  - Added 8 new columns (see "Added" section)
  - Unified units (µs for T2, seconds for T1)
  - Standardized DOI format (always prefix "DOI:")
- **Interface improvements**
  - HTML interface: Sortable/filterable table
  - Responsive design (mobile-friendly)
  - Visual timeline of publications (figure)
  - T2 vs Temperature scatterplot (figure)

### Fixed
- **Version synchronization**
  - README.md, CITATION.cff, zenodo.json all show v1.2.1
  - Git tag matches release version exactly
- **Data corrections**
  - 5 T2 values corrected (unit conversion errors in v1.1)
  - 3 DOI links fixed (broken URLs)
  - 2 duplicate entries merged (NV 50nm vs NV-50nm)
- **Linter compliance**
  - 0 blocking errors (was 3 in v1.1)
  - 2 warnings (non-critical: missing Contraste for 2 systems)

### Deprecated
- Old schema (v1.0) is no longer supported
- CSV without provenance columns (upgrade to v1.2+ required)

---

## [1.2.0] - 2025-10-20

### Added
- Initial provenance tracking (Source_T2 column only)
- Basic uncertainty quantification (T2_us_err only)
- Linter prototype (`qubits_linter.py` v0.1)

### Changed
- Dataset: 66 systems (same as v1.2.1)
- Quality: Some missing metadata (incomplete provenance)

### Notes
- This version was quickly superseded by v1.2.1 (3 days later)
- v1.2.1 fixed critical metadata gaps
- **Recommendation**: Skip v1.2.0, use v1.2.1 instead

---

## [1.1.0] - 2025-10-15 (estimated)

### Added
- **Initial dataset**: 21 systems
  - 18 with T2 measurements
  - 12 Class B (bio-compatible internalized)
  - 5 Class C (NMR hyperpolarized)
  - 4 Class A+D (bio-intrinsic + mechanistic)
- **Basic provenance**: DOI column only (no Figure/Table reference)
- **HTML interface**: Basic sortable table
- **Documentation**: README.md with project description

### Changed
- First numbered release (no previous versions)

### Known Issues (Addressed in v1.2+)
- ❌ No uncertainty quantification (T2_err missing)
- ❌ No provenance beyond DOI (which figure/table?)
- ❌ No verification status tracking
- ❌ No quality control linter
- ❌ Manual CSV editing only (no automated pipeline)

---

## [1.0.0] - Never released

**Note**: Project started directly at v1.1.0 due to iterative development during research phase. No v1.0.0 exists.

---

## Version Naming Convention

- **Stable releases**: `vX.Y.Z` (e.g., v1.2.1)
  - Production-ready, recommended for citations
  - QA passed (0 blocking errors)
  - Zenodo DOI minted
  
- **Pre-releases**: `vX.Y.Z-beta` or `vX.Y.Z-alpha` (e.g., v1.3.0-beta)
  - Feature preview, community testing
  - May have warnings (non-blocking)
  - Not recommended for formal citations until stable
  
- **Git tags**: Match release numbers exactly (no "v" prefix in tag name: `1.2.1` not `v1.2.1`)

---

## How to Read This Changelog

### Section Meanings

- **Added**: New features, systems, columns, or documentation
- **Changed**: Modifications to existing functionality (backward-compatible)
- **Deprecated**: Features marked for removal in future versions
- **Removed**: Features removed in this version (breaking change → MAJOR version bump)
- **Fixed**: Bug fixes, data corrections
- **Security**: Vulnerability patches (if applicable)

### Emoji Legend

- 🟢 Stable release (production-ready)
- 🟡 Pre-release (beta testing)
- ⚠️ Known limitation or caveat
- ✅ Completed / verified
- ❌ Issue / not implemented
- 📝 Documentation change
- 🔧 Infrastructure / tooling

---

## Migration Guides

### Upgrading from v1.2.1 to v1.3.0-beta

**Schema changes**: None (backward-compatible)

**New columns** (optional, may be empty):
- `contrast_quality_tier` (A/B/C)
- `curator` (who added/verified this entry)

**Action required**: None (CSV from v1.2.1 will still work)

---

### Upgrading from v1.1.0 to v1.2.1

**Schema changes**: +8 new columns (see v1.2.1 release notes)

**Action required**:
1. Add new columns to import scripts
2. Re-validate provenance (now requires Figure/Table reference)
3. Update analysis pipelines to handle uncertainties

**Script example**:
```python
import pandas as pd

# Old schema (v1.1)
df_old = pd.read_csv('biological_qubits_v1.1.csv')

# New schema (v1.2+)
df_new = pd.read_csv('biological_qubits_v1.2.1.csv')

# Check for new columns
new_cols = set(df_new.columns) - set(df_old.columns)
print(f"New columns: {new_cols}")
# Output: {'Source_T2', 'Source_T1', 'Source_Contraste', ...}
```

---

## Questions or Feedback?

- **Bugs**: Open GitHub Issue with label `bug`
- **Feature requests**: Open GitHub Issue with label `enhancement`
- **General discussion**: GitHub Discussions (or email maintainer)

---

**Last updated**: 2025-10-24  
**Changelog format**: [Keep a Changelog v1.0.0](https://keepachangelog.com/en/1.0.0/)  
**Versioning scheme**: [Semantic Versioning v2.0.0](https://semver.org/spec/v2.0.0.html)
