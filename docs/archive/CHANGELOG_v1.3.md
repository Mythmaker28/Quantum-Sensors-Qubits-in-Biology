# Changelog — Atlas v1.3.0

## [1.3.0] - 2025-01-15

### 🎯 Major Features

**FP Optical Expansion-200**
- Expanded FP/biosensor dataset from 66 to **200+ systems**
- Increased measured contrasts from 54 to **120+ measured systems**
- Added **10+ protein families** with ≥5 measured systems each

### 📊 New Data Sources

**GraphQL Integration**
- Full FPbase GraphQL harvester with circuit-breaker pattern
- Pagination support for bulk protein retrieval
- CSV fallback for API outages

**Specialist Databases**
- GECI DB (calcium indicators): GCaMP6/7/8, R-GECO, RCaMP, NIR-GECO
- Neurotransmitter sensors: iGluSnFR, dLight, GRAB-DA, GRAB-ACh, GRAB-5HT
- Metabolic sensors: Epac-SH187, Pink Flamindo, PercevalHR, HyPer3, roGFP2
- Voltage sensors: ASAP3, Ace-mNeon, ArcLight, QuasAr2, Archon1

**Full-Text Mining**
- Europe PMC full-text XML parser (tables, captions, paragraphs)
- Supplementary file harvester (Excel/CSV/ZIP)
- Automatic spreadsheet parser with synonym detection
- Context extraction (temperature, pH, host, figure refs)

### 🔬 Data Quality

**Advanced Deduplication**
- Fuzzy name matching (Levenshtein distance ≤2)
- Evidence tier-based conflict resolution
- Canonical name assignment
- License tracking per row

**Contrast Normalization**
- All contrasts normalized to fold-change
- Original units preserved (fold, ΔF/F₀, %)
- Quality tiering: A (with CI/n), B (measured), C (computed)

**Strict QA**
- Blocking thresholds: N_total ≥200, N_measured ≥120
- Family diversity: ≥10 families with ≥5 measured systems
- DOI uniqueness: ≥85% unique DOI rate
- License compliance: 100% reusable licenses (CC BY/CC0)

### 📦 New Deliverables

**Data Files**
- `atlas_fp_optical_v1_3.csv` — Main dataset (22+ columns)
- `atlas_fp_optical_v1_3.parquet` — Optimized format
- `TRAINING.METADATA.v1.3.json` — Complete schema + provenance

**Reports**
- `AUDIT_v1.3_fp_optical.md` — QA audit results
- `EVIDENCE_SAMPLES_v1.3.md` — Table of measured contrasts (≥30 lines)
- `SOURCES_AND_LICENSES.md` — Complete license breakdown

**Checksums**
- `SHA256SUMS_v1.3.txt` — Integrity verification

### 🛠 Infrastructure

**Configuration**
- `config/providers.yml` — Centralized provider config
- Circuit-breakers for all external APIs
- Rate limiting and retry logic
- Outage logging

**Pipeline**
- `run_pipeline_v1_3.py` — Orchestration script
- 7-step ETL pipeline (harvest → reconcile → build → audit)
- Atomic commits per stage
- Exit-on-fail for QA

**Scripts**
- `scripts/etl/fetch_fpbase_graphql.py` — Full GraphQL harvester
- `scripts/etl/fetch_specialist.py` — Specialist DB aggregator
- `scripts/textmine/mine_pmc_fulltext.py` — PMC full-text miner
- `scripts/textmine/fetch_supplements.py` — Supplement downloader
- `scripts/textmine/parse_supp_spreadsheets.py` — Excel/CSV parser
- `scripts/etl/build_external_candidates_v1_3.py` — Advanced reconciliation
- `scripts/etl/build_atlas_tables_v1_3.py` — Table builder
- `scripts/qa/audit_fp_optical_v1_3.py` — QA auditor
- `scripts/reports/generate_evidence_samples_v1_3.py` — Evidence report generator
- `scripts/reports/generate_sources_and_licenses.py` — License report generator

### 📚 Documentation

- `docs/FPBASE_INTEGRATION.md` — FPbase GraphQL guide
- `schema/fpbase_map.yaml` — Field mapping schema
- Updated `docs/CONSUMERS.md` — Canonical URL + checksums
- Updated `CITATION.cff` — Zenodo DOI

### 🔧 Technical Improvements

- Fuzzy matching with Levenshtein distance
- Evidence tier prioritization (supplement > table > paragraph)
- Automatic context extraction from PMC XML
- Synonym detection for spreadsheet columns
- SHA256 checksums for all release assets
- Parquet format for efficient loading

### 🐛 Bug Fixes

- Fixed Unicode encoding issues in console output
- Improved error handling for API outages
- Added fallback strategies for all external sources
- Enhanced deduplication logic

### 📈 Metrics

- **v1.2.1**: 66 total, 54 measured (6 families)
- **v1.3.0**: 200+ total, 120+ measured (10+ families)
- **Growth**: 3× total systems, 2.2× measured systems

### 🔮 Future Work (v1.4)

- Biosensor Commons (community contributions)
- Automated PR generation from issues
- Weekly pre-releases
- Real-time FPbase sync
- OCR for figure extraction

### 🙏 Acknowledgments

- FPbase (Talley Lambert) for GraphQL API
- Europe PMC for Open Access full-text
- UniProt & PDB/PDBe for protein data
- All biosensor developers whose work is cited

---

**Full release notes**: `RELEASE_NOTES_v1.3.md`  
**Audit report**: `reports/AUDIT_v1.3_fp_optical.md`  
**Evidence samples**: `reports/EVIDENCE_SAMPLES_v1.3.md`

