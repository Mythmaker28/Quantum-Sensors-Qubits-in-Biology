#!/usr/bin/env python3
"""Simple QA Audit for v1.3 (works with partial data)"""
import pandas as pd
from pathlib import Path

df = pd.read_csv('data/processed/atlas_fp_optical_v1_3.csv')

N_total = len(df)
N_measured = df['contrast_value'].notna().sum() if 'contrast_value' in df.columns else 0
N_tier_A = (df['contrast_quality_tier'] == 'A').sum() if 'contrast_quality_tier' in df.columns else 0
N_tier_B = (df['contrast_quality_tier'] == 'B').sum() if 'contrast_quality_tier' in df.columns else 0
N_tier_C = (df['contrast_quality_tier'] == 'C').sum() if 'contrast_quality_tier' in df.columns else 0

report = f"""# Atlas FP Optical v1.3 - QA Audit Report (BLOCKED)

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

- **N_total**: {N_total} FAIL (required: 200, gap: {200-N_total})
- **N_measured**: {N_measured} FAIL (required: 120, gap: {120-N_measured})
- N_tier_A: {N_tier_A}
- N_tier_B: {N_tier_B}
- N_tier_C: {N_tier_C}

### Root Cause

**FPbase API Outage**: Unable to harvest ~150+ systems from FPbase GraphQL/CSV.

**PMC Mining Skipped**: Rate limits and time constraints.

### Data Sources

- v1.2.1 base: 66 systems (54 measured)
- Specialist DBs: 43 biosensors (0 measured)
- Extended FPs: 50 variants (0 measured)
- Total (deduplicated): {N_total} systems

## Overall Status

**RELEASE BLOCKED**

See EXECUTION_SUMMARY_v1.3_BLOCKED.md for recovery options.
"""

Path('reports').mkdir(exist_ok=True)
with open('reports/AUDIT_v1.3_fp_optical.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(report)
print("\n" + "="*70)
print("QA AUDIT: FAILED")
print("="*70)
print(f"N_total:    {N_total} / 200 required")
print(f"N_measured: {N_measured} / 120 required")
print("\nRelease BLOCKED.")

