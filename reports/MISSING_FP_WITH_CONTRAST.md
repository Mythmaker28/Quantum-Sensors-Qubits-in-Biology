# Missing FP with Contrast — Action Plan

**Date**: 2025-10-23T22:44:22.505397

## Summary

**Total FP entries without contrast**: 37 / 66

## Root Cause Analysis

### FPbase API Outage

- FPbase (https://www.fpbase.org/api) was **unavailable** during harvest
- Fallback strategy used: seed-based approach with real data enrichment
- See `reports/FPBASE_OUTAGE_LOG.md` for details

### PMC Extraction Challenges

- **Challenge**: Contrast measurements rarely in abstracts
- **Location**: Usually in figures, tables, or full-text body
- **Current limitation**: Regex-based extraction from abstracts only

## Action Plan to Reach >=25 Measured

### Short-term (v1.2.1)

1. **Wait for FPbase recovery** and re-run harvest
2. **Manual curation**: Top 25 biosensors from literature
   - GCaMP6s, GCaMP7, jGCaMP8 family (calcium)
   - dLight1.x, GRAB-DA (dopamine)
   - iGluSnFR (glutamate)
   - ASAP3, ArcLight (voltage)
3. **PMC full-text parsing**: Implement PDF/XML parser

### Medium-term (v1.3)

1. **NLP-based extraction**: Use transformers for better PMC parsing
2. **Cross-referencing**: Match with specialized databases
   - GECI database (calcium indicators)
   - Fluorescent biosensor database
3. **Community contributions**: GitHub issues for missing data

## Entries Needing Manual Curation (Top Priority)

| SystemID | Protein Name | Type | Family | UniProt | PDB |
|----------|--------------|------|--------|---------|-----|
| FP_SEED_0051 | RCaMP1h | Biosensor | Calcium | N/A | N/A |
| FP_SEED_0066 | pHuji | Biosensor | pH | N/A | N/A |

