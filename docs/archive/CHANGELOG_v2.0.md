# Changelog — Atlas v2.0.0

**Release Date**: 2025-10-24  
**Tag**: `v2.0.0`  
**Branch**: `release/v2.0`

---

## 🎯 Summary

Atlas v2.0.0 introduces **interactive dashboard**, **FAIR 12/12 compliance**, and **systematic in vivo validation** while maintaining the 80-system curated dataset from v1.3.0-beta.

---

## ✨ What's New

### Interactive Dashboard (D3.js)
- ✅ Scatter plot T2 vs Temperature (interactive tooltips)
- ✅ Barplot families by count
- ✅ Real-time statistics cards
- ✅ Responsive design (mobile/tablet)
- ✅ Export-ready visualizations

**File**: `index_v2_interactive.html`

### FAIR 12/12 Compliance
- ✅ Schema.org JSON-LD (Google Dataset Search indexing)
- ✅ DataCite XML (DOI minting ready)
- ✅ CODEMETA JSON (software metadata) **NEW**
- ✅ Complete provenance tracking

**Files**: `metadata/fair/*.json`, `*.xml`

### In Vivo Validation
- ✅ Automated scoring (0-100)
- ✅ Organism detection (mouse, rat, zebrafish, etc.)
- ✅ Validation report with gaps analysis

**Files**: `reports/IN_VIVO_VALIDATION.md`, `.csv`

---

## 📊 Metrics

| Metric | v1.3.0-beta | v2.0.0 | Change |
|--------|-------------|--------|--------|
| **Total systems** | 80 | 80 | = |
| **Measured contrasts** | 65 | 65 | = |
| **Families** | 17 | 20 | +3 |
| **FAIR Score** | 8/12 | 12/12 | **+4** |
| **Dashboard** | Static HTML | Interactive D3.js | ✨ |
| **Validation** | Manual | Automated (scoring) | ✨ |
| **Duplicates** | Unknown | 0 (verified) | ✅ |

---

## 🔧 Technical Changes

### New Scripts
- `scripts/web/generate_interactive_dashboard.py`
- `scripts/fair/generate_fair_metadata.py` (extended)
- `scripts/qa/in_vivo_validator.py`
- `scripts/qa/deduplicate_atlas_v2.py`
- `scripts/reports/generate_metrics_v2.py`

### New Tests
- `tests/test_dashboard_generation.py` (10 test cases)

### New Documentation
- `PRD_v2.0.md` (Product Requirements Document)
- `docs/DASHBOARD_USER_GUIDE.md`
- `START_HERE.md`

### Infrastructure
- `EXECUTE_V2_PHASE1.sh` (bash automation)
- `EXECUTE_V2_PHASE1.ps1` (PowerShell automation)
- `.gitignore` (secrets protection)
- `LICENSE.CODE` (Apache 2.0)

---

## 🐛 Bug Fixes

- Fixed Unicode encoding errors (emojis → ASCII) for Windows compatibility
- Fixed escape sequence warnings in validation script

---

## ⚠️ Breaking Changes

None. Backward compatible with v1.3.0-beta.

---

## 📚 Migration Guide

No migration required. v2.0.0 extends v1.3.0-beta with new features.

**New Users**: Start with `index_v2_interactive.html` (interactive dashboard)

**Developers**: See `PRD_v2.0.md` for roadmap and specs

---

## 🙏 Contributors

- Tommy Lepesteur (@Mythmaker28)
- Community contributors via GitHub Issues/PRs

---

## 📦 Assets

- `atlas_fp_optical_v2_0.csv` (main dataset, 80 systems)
- `index_v2_interactive.html` (interactive dashboard)
- `metadata/fair/*.json`, `*.xml` (FAIR metadata)
- `reports/METRICS_v2.0.json` (machine-readable metrics)
- `reports/IN_VIVO_VALIDATION.md` (validation report)

---

**END OF CHANGELOG v2.0.0**

