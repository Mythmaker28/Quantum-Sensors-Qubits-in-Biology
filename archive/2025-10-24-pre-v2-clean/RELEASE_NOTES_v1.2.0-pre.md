# Release Notes — Atlas v1.2.0-pre (Pre-Release)

**Version**: 1.2.0-pre  
**Date**: 2025-10-23  
**Type**: Pre-Release (Quality Gate Not Fully Met)  
**Status**: ✅ Total Entries Met, ⚠️ Contrast Measurements Pending

---

## 🎯 Objectives Status

| Objective | Target | Achieved | Status |
|-----------|--------|----------|--------|
| **Total FP entries** | ≥ 50 | 66 | ✅ **MET** |
| **Measured contrast** | ≥ 25 | 0 | ⚠️ **PENDING** |

---

## 📊 What Was Delivered

### ✅ Achieved (66/50 entries)

1. **66 Real FP/Biosensor Entries**
   - All from seed file (`seed/seed_fp_names.csv`)
   - Real protein names (GFP, mCherry, GCaMP6s, etc.)
   - NULL for missing data (NO synthetic values)

2. **Real Data Enrichment**
   - 3 entries with UniProt IDs (CC BY 4.0)
   - 9 entries with PDB IDs (CC0)
   - All sources documented and licensed

3. **Complete Infrastructure**
   - Auto-research name query generator (694 variants)
   - FPbase provider with circuit-breaker
   - UniProt/PDB matchers
   - PMC OA contrast extractor
   - Strict QA audit

4. **Comprehensive Documentation**
   - `AUDIT_v1.2_fp_optical.md` (metrics + thresholds)
   - `MISSING_FP_WITH_CONTRAST.md` (action plan)
   - `SOURCES_AND_LICENSES.md` (provenance)
   - `FPBASE_OUTAGE_LOG.md` (fallback explanation)
   - `ALIAS_CHANGES.md` (query variants)

### ⚠️ Pending (0/25 measured contrast)

**Root Cause**: FPbase API unavailability + PMC extraction limitations

1. **FPbase API Down**
   - Primary data source (https://www.fpbase.org/api) unreachable
   - Fallback to seed-based approach implemented
   - See `reports/FPBASE_OUTAGE_LOG.md`

2. **PMC Extraction Challenges**
   - Contrast measurements rarely in abstracts
   - Usually in figures/tables/full-text body
   - Current regex-based approach insufficient
   - 40 proteins searched, 0 measurements extracted

---

## 📁 Deliverables

### Data Files

- `data/processed/atlas_fp_optical.csv` (66 entries, 18 columns)
- `data/processed/atlas_all_real.csv` (66 entries, same content)
- `data/processed/TRAINING.METADATA.json` (schema + quality metrics)

### Reports

- `reports/AUDIT_v1.2_fp_optical.md` — QA audit results
- `reports/MISSING_FP_WITH_CONTRAST.md` — Action plan to reach ≥25
- `reports/SOURCES_AND_LICENSES.md` — Data provenance
- `reports/FPBASE_OUTAGE_LOG.md` — Fallback explanation
- `reports/EXTERNAL_HARVEST_LOG.md` — UniProt/PDB harvest logs
- `reports/ALIAS_CHANGES.md` — Query variants log

### Scripts

- `scripts/etl/build_name_queries.py` — 694 query variants
- `scripts/etl/harvest_from_seed.py` — Real data harvest
- `scripts/etl/extract_pmc_contrast_real.py` — PMC OA extractor
- `scripts/etl/build_atlas_from_seed_real_only.py` — Atlas builder
- `scripts/qa/audit_atlas_v1_2_strict.py` — Strict QA

---

## 🔐 Data Integrity Guarantee

### ✅ What We Did

- **NO synthetic/demo values**: Every numerical field is from real sources or NULL
- **NO placeholders**: No "TBD", "demo", "test" values
- **Source tracking**: Every non-NULL value has `source_refs` + `license_source`
- **License compliance**: CC BY 4.0 (UniProt), CC0 (PDB), CC BY (PMC OA)

### ❌ What We Did NOT Do

- **NO invented data**: Refused to fill contrast values without real measurements
- **NO estimated proxies**: Could have computed brightness-based proxies, chose not to without validation
- **NO relaxed QA**: Audit correctly fails (exit code 1) on threshold miss

---

## 🚀 Action Plan to Reach v1.2.0 (Full Release)

### Immediate Actions (v1.2.0 release)

1. **Wait for FPbase API Recovery**
   - Monitor https://www.fpbase.org/api/proteins/
   - Re-run harvest when available
   - Expected to provide contrast data for 30+ entries

2. **Manual Curation (Priority Biosensors)**
   - GCaMP6s, jGCaMP7, jGCaMP8 (calcium, n=8)
   - dLight1.x, GRAB-DA (dopamine, n=3)
   - iGluSnFR (glutamate, n=2)
   - ASAP3, ArcLight (voltage, n=2)
   - **Target**: 25+ manually curated with DOI citations

3. **PMC Full-Text Parsing**
   - Implement PDF/XML parser (not just abstracts)
   - Target figures/tables extraction
   - Use OpenAccess full-text when available

### Medium-term (v1.3)

4. **NLP-Based Extraction**
   - Use transformers (BioBERT, SciBERT)
   - Better entity recognition for measurements

5. **Cross-Database Matching**
   - GECI database (genetically-encoded calcium indicators)
   - Fluorescent biosensor database
   - FluoroFinder (commercial FPs)

6. **Community Contributions**
   - Open GitHub issues for each missing biosensor
   - Template for submitting contrast measurements + DOI

---

## 📦 Release Assets (v1.2.0-pre)

- `atlas_fp_optical.csv` (66 entries)
- `atlas_all_real.csv` (66 entries)
- `TRAINING.METADATA.json`
- `AUDIT_v1.2_fp_optical.md`
- `MISSING_FP_WITH_CONTRAST.md`
- `SOURCES_AND_LICENSES.md`
- `FPBASE_OUTAGE_LOG.md`

**NOT YET**: Zenodo DOI (will be issued for v1.2.0 full release)

---

## 🎓 Lessons Learned

### What Worked

1. **Seed-based fallback** successfully created 66 entries
2. **Strict data integrity** maintained (no synthetic values)
3. **Auto-research** generated 694 query variants for better matching
4. **Comprehensive reporting** documents gaps transparently

### What Needs Improvement

1. **FPbase dependency**: Need backup data source or cache
2. **PMC abstract-only** insufficient for contrast extraction
3. **Manual curation** still necessary for biosensors
4. **Full-text access** required for comprehensive data

---

## 🔗 Next Steps

### For Users

1. **Use v1.2.0-pre** if you only need protein names/families (66 entries)
2. **Wait for v1.2.0** if you need contrast measurements (target: ≥25)
3. **Contribute** via GitHub issues if you have biosensor data

### For Maintainers

1. Monitor FPbase API recovery
2. Prioritize manual curation of top 25 biosensors
3. Implement PDF/XML full-text parser
4. Prepare v1.2.0 release when ≥25 measured

---

## 📞 Support

- **GitHub Issues**: Report missing data, suggest biosensors
- **Discussions**: https://github.com/[OWNER]/[REPO]/discussions
- **Email**: research@example.org

---

## 🙏 Acknowledgments

- **FPbase**: (currently down) will be primary source when recovered
- **UniProt**: 3 real protein IDs
- **PDB**: 9 real structure IDs
- **PMC**: 40 proteins searched (OA only)

---

**This is a pre-release**. Full v1.2.0 will be issued when both thresholds are met (≥50 total ✓, ≥25 measured ⚠️).

---

**End of Pre-Release Notes**

