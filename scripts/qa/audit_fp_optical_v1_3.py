#!/usr/bin/env python3
"""
QA Script: Audit FP Optical v1.3
=================================

Strict QA audit with blocking thresholds:
- N_total ≥ 200
- N_measured ≥ 120
- families_with_ge_5 ≥ 10
- unique_doi_rate ≥ 0.85
- license_ok_rate = 1.0

Author: Biological Qubit Atlas Team
License: MIT
"""

import json
import sys
from pathlib import Path
import pandas as pd
import yaml

def load_config() -> dict:
    """Load configuration."""
    with open("config/providers.yml", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

CONFIG = load_config()
THRESHOLDS = CONFIG['thresholds']

def audit_counts(df: pd.DataFrame) -> dict:
    """Audit basic counts."""
    N_total = len(df)
    N_measured = df['contrast_value'].notna().sum()
    N_with_ci = df['ci_low'].notna().sum()
    N_tier_A = (df['contrast_quality_tier'] == 'A').sum()
    N_tier_B = (df['contrast_quality_tier'] == 'B').sum()
    N_tier_C = (df['contrast_quality_tier'] == 'C').sum()
    
    return {
        'N_total': N_total,
        'N_measured': N_measured,
        'N_with_ci': N_with_ci,
        'N_tier_A': N_tier_A,
        'N_tier_B': N_tier_B,
        'N_tier_C': N_tier_C,
        'pass_N_total': N_total >= THRESHOLDS['N_total_min'],
        'pass_N_measured': N_measured >= THRESHOLDS['N_measured_min']
    }

def audit_families(df: pd.DataFrame) -> dict:
    """Audit family coverage."""
    measured_df = df[df['contrast_value'].notna()]
    family_counts = measured_df.groupby('family').size()
    families_with_ge_5 = (family_counts >= 5).sum()
    
    return {
        'families_with_ge_5': families_with_ge_5,
        'family_counts': family_counts.to_dict(),
        'pass_families': families_with_ge_5 >= THRESHOLDS['families_with_ge_5_min']
    }

def audit_dois(df: pd.DataFrame) -> dict:
    """Audit DOI uniqueness."""
    measured_df = df[df['contrast_value'].notna()]
    
    # Extract DOIs from source_refs
    dois = []
    for refs in measured_df['source_refs']:
        if pd.notna(refs):
            # Extract DOI patterns
            import re
            doi_matches = re.findall(r'10\.\d{4,9}/[^\s;]+', str(refs))
            dois.extend(doi_matches)
    
    unique_dois = len(set(dois))
    total_measured = len(measured_df)
    
    if total_measured > 0:
        unique_doi_rate = unique_dois / total_measured
    else:
        unique_doi_rate = 0.0
    
    return {
        'unique_dois': unique_dois,
        'total_measured': total_measured,
        'unique_doi_rate': unique_doi_rate,
        'pass_doi_rate': unique_doi_rate >= THRESHOLDS['unique_doi_rate_min']
    }

def audit_licenses(df: pd.DataFrame) -> dict:
    """Audit license compliance."""
    allowed_licenses = CONFIG['validation']['license_check']['allowed']
    
    # Check if all licenses are OK
    license_ok_count = 0
    license_uncertain_count = 0
    
    for lic in df['license_source']:
        if pd.isna(lic):
            license_uncertain_count += 1
        else:
            lic_str = str(lic).upper()
            if any(allowed.upper() in lic_str for allowed in allowed_licenses):
                license_ok_count += 1
            else:
                license_uncertain_count += 1
    
    total = len(df)
    if total > 0:
        license_ok_rate = license_ok_count / total
    else:
        license_ok_rate = 0.0
    
    return {
        'license_ok_count': license_ok_count,
        'license_uncertain_count': license_uncertain_count,
        'license_ok_rate': license_ok_rate,
        'pass_license': license_ok_rate >= THRESHOLDS['license_ok_rate_min']
    }

def generate_report(audit_results: dict, output_path: Path):
    """Generate audit report in Markdown."""
    report_lines = [
        "# Atlas FP Optical v1.3 - QA Audit Report",
        "",
        f"**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Blocking Thresholds",
        "",
        f"- N_total ≥ {THRESHOLDS['N_total_min']}",
        f"- N_measured ≥ {THRESHOLDS['N_measured_min']}",
        f"- families_with_ge_5 ≥ {THRESHOLDS['families_with_ge_5_min']}",
        f"- unique_doi_rate ≥ {THRESHOLDS['unique_doi_rate_min']:.2f}",
        f"- license_ok_rate ≥ {THRESHOLDS['license_ok_rate_min']:.2f}",
        "",
        "## Results",
        "",
        "### Counts",
        "",
        f"- **N_total**: {audit_results['counts']['N_total']} {'[OK] PASS' if audit_results['counts']['pass_N_total'] else '[FAIL]'}",
        f"- **N_measured**: {audit_results['counts']['N_measured']} {'[OK] PASS' if audit_results['counts']['pass_N_measured'] else '[FAIL]'}",
        f"- N_with_ci: {audit_results['counts']['N_with_ci']}",
        f"- N_tier_A: {audit_results['counts']['N_tier_A']}",
        f"- N_tier_B: {audit_results['counts']['N_tier_B']}",
        f"- N_tier_C: {audit_results['counts']['N_tier_C']}",
        "",
        "### Family Coverage",
        "",
        f"- **families_with_ge_5**: {audit_results['families']['families_with_ge_5']} {'[OK] PASS' if audit_results['families']['pass_families'] else '[FAIL]'}",
        "",
        "#### Family Breakdown (measured systems):",
        ""
    ]
    
    # Add family table
    for family, count in sorted(audit_results['families']['family_counts'].items(), key=lambda x: -x[1]):
        report_lines.append(f"- {family}: {count}")
    
    report_lines.extend([
        "",
        "### DOI Uniqueness",
        "",
        f"- unique_dois: {audit_results['dois']['unique_dois']}",
        f"- total_measured: {audit_results['dois']['total_measured']}",
        f"- **unique_doi_rate**: {audit_results['dois']['unique_doi_rate']:.3f} {'[OK] PASS' if audit_results['dois']['pass_doi_rate'] else '[FAIL]'}",
        "",
        "### License Compliance",
        "",
        f"- license_ok_count: {audit_results['licenses']['license_ok_count']}",
        f"- license_uncertain_count: {audit_results['licenses']['license_uncertain_count']}",
        f"- **license_ok_rate**: {audit_results['licenses']['license_ok_rate']:.3f} {'[OK] PASS' if audit_results['licenses']['pass_license'] else '[FAIL]'}",
        "",
        "## Overall Status",
        ""
    ])
    
    all_pass = all([
        audit_results['counts']['pass_N_total'],
        audit_results['counts']['pass_N_measured'],
        audit_results['families']['pass_families'],
        audit_results['dois']['pass_doi_rate'],
        audit_results['licenses']['pass_license']
    ])
    
    if all_pass:
        report_lines.append("**[OK] ALL CHECKS PASSED** - Ready for release v1.3.0")
    else:
        report_lines.append("**✗ SOME CHECKS FAILED** - Release blocked, see details above")
    
    report_lines.append("")
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

def main():
    """Main audit."""
    print("=" * 70)
    print("QA Audit: FP Optical v1.3")
    print("=" * 70)
    
    # Load data
    data_path = Path("data/processed/atlas_fp_optical_v1_3.csv")
    if not data_path.exists():
        print(f"ERROR: {data_path} not found")
        print("Run scripts/etl/build_atlas_tables_v1_3.py first")
        return 1
    
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} systems\n")
    
    # Run audits
    print("Running audits...")
    
    audit_results = {
        'counts': audit_counts(df),
        'families': audit_families(df),
        'dois': audit_dois(df),
        'licenses': audit_licenses(df)
    }
    
    # Print results
    print("\nRESULTS:")
    print("--------")
    print(f"N_total:              {audit_results['counts']['N_total']} (min: {THRESHOLDS['N_total_min']}) {'PASS' if audit_results['counts']['pass_N_total'] else 'FAIL'}")
    print(f"N_measured:           {audit_results['counts']['N_measured']} (min: {THRESHOLDS['N_measured_min']}) {'PASS' if audit_results['counts']['pass_N_measured'] else 'FAIL'}")
    print(f"families_with_ge_5:   {audit_results['families']['families_with_ge_5']} (min: {THRESHOLDS['families_with_ge_5_min']}) {'PASS' if audit_results['families']['pass_families'] else 'FAIL'}")
    print(f"unique_doi_rate:      {audit_results['dois']['unique_doi_rate']:.3f} (min: {THRESHOLDS['unique_doi_rate_min']:.2f}) {'PASS' if audit_results['dois']['pass_doi_rate'] else 'FAIL'}")
    print(f"license_ok_rate:      {audit_results['licenses']['license_ok_rate']:.3f} (min: {THRESHOLDS['license_ok_rate_min']:.2f}) {'PASS' if audit_results['licenses']['pass_license'] else 'FAIL'}")
    
    # Generate report
    report_path = Path("reports/AUDIT_v1.3_fp_optical.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    generate_report(audit_results, report_path)
    print(f"\nOK Report saved: {report_path}")
    
    # Check overall pass/fail
    all_pass = all([
        audit_results['counts']['pass_N_total'],
        audit_results['counts']['pass_N_measured'],
        audit_results['families']['pass_families'],
        audit_results['dois']['pass_doi_rate'],
        audit_results['licenses']['pass_license']
    ])
    
    if all_pass:
        print("\n[OK] ALL CHECKS PASSED - Ready for release v1.3.0!")
        return 0
    else:
        print("\n[X] SOME CHECKS FAILED - Release blocked")
        return 1

if __name__ == "__main__":
    sys.exit(main())

