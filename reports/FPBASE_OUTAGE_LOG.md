# FPbase Outage Log

**Timestamp**: 2025-10-23T22:08:08.499626

## Status: UNAVAILABLE

FPbase API (https://www.fpbase.org/api/proteins/) is currently unreachable.

## Fallback Strategy Applied

1. Using seed file: `seed\seed_fp_names.csv` (66 real FP/biosensor names)
2. Harvesting REAL data from:
   - **UniProt**: protein IDs, sequences, annotations
   - **PDB/PDBe**: structures, experimental wavelengths
   - **PMC Open Access**: contrast measurements from literature

## Data Integrity Guarantee

- NO synthetic or demo values
- ALL numerical data from published sources
- Licenses tracked per entry
- Missing data left as NULL (not estimated)

