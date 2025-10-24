# Atlas FP Optical v1.3 - QA Audit Report (BLOCKED)

**Generated**: 2025-01-15
**Status**: FAILED - Thresholds NOT MET

## Blocking Thresholds

- N_total >= 200
- N_measured >= 120
- families_with_ge_5 >= 10
- unique_doi_rate >= 0.85
- license_ok_rate >= 1.0

## Results

### Counts

- **N_total**: 98 FAIL (required: 200, gap: 102)
- **N_measured**: 0 FAIL (required: 120, gap: 120)
- N_tier_A: 0
- N_tier_B: 54
- N_tier_C: 32

### Root Cause

**FPbase API Outage**: Unable to harvest ~150+ systems from FPbase GraphQL/CSV.

**PMC Mining Skipped**: Rate limits and time constraints.

### Data Sources

- v1.2.1 base: 66 systems (54 measured)
- Specialist DBs: 43 biosensors (0 measured)
- Extended FPs: 50 variants (0 measured)
- Total (deduplicated): 98 systems

## Overall Status

**RELEASE BLOCKED**

See EXECUTION_SUMMARY_v1.3_BLOCKED.md for recovery options.
