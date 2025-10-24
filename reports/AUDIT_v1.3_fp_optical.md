# Atlas FP Optical v1.3 - QA Audit Report

**Generated**: 2025-10-24 04:03:37

## Blocking Thresholds

- N_total ≥ 200
- N_measured ≥ 120
- families_with_ge_5 ≥ 10
- unique_doi_rate ≥ 0.85
- license_ok_rate ≥ 1.00

## Results

### Counts

- **N_total**: 80 [FAIL]
- **N_measured**: 65 [FAIL]
- N_with_ci: 0
- N_tier_A: 0
- N_tier_B: 80
- N_tier_C: 0

### Family Coverage

- **families_with_ge_5**: 5 [FAIL]

#### Family Breakdown (measured systems):

- Calcium: 12
- GFP-like: 8
- RFP: 6
- Dopamine: 5
- Far-red: 5
- Voltage: 4
- CFP-like: 3
- Glutamate: 3
- ATP/ADP: 2
- H2O2: 2
- NIR: 2
- Orange: 2
- cAMP: 2
- pH: 2
- BFP-like: 1
- Redox: 1
- Teal: 1

### DOI Uniqueness

- unique_dois: 20
- total_measured: 65
- **unique_doi_rate**: 0.308 [FAIL]

### License Compliance

- license_ok_count: 8
- license_uncertain_count: 72
- **license_ok_rate**: 0.100 [FAIL]

## Overall Status

**✗ SOME CHECKS FAILED** - Release blocked, see details above
