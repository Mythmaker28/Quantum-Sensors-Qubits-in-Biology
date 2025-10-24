#!/usr/bin/env python3
"""
Generate METRICS_v1.3.json - Machine-readable metrics report
==============================================================

Reads atlas_fp_optical_v1_3.csv and generates comprehensive metrics in JSON format.

Author: Biological Qubit Atlas Team
License: MIT
"""

import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

def load_atlas() -> pd.DataFrame:
    """Load atlas dataset."""
    atlas_path = Path("data/processed/atlas_fp_optical_v1_3.csv")
    
    if not atlas_path.exists():
        print(f"ERROR: {atlas_path} not found")
        sys.exit(1)
    
    return pd.read_csv(atlas_path)

def compute_metrics(df: pd.DataFrame) -> dict:
    """Compute all metrics."""
    
    # Basic counts
    N_total = int(len(df))
    N_measured = int(df['contrast_value'].notna().sum())
    
    # Quality tiers
    tier_counts = {}
    if 'contrast_quality_tier' in df.columns:
        tier_counts = df['contrast_quality_tier'].value_counts().to_dict()
        N_measured_A = int(tier_counts.get('A', 0))
        N_measured_B = int(tier_counts.get('B', 0))
        N_measured_C = int(tier_counts.get('C', 0))
    else:
        N_measured_A = 0
        N_measured_B = N_measured
        N_measured_C = 0
    
    # Family analysis
    family_measured = df[df['contrast_value'].notna()].groupby('family').size()
    families_with_ge_5 = int((family_measured >= 5).sum())
    family_breakdown = {str(k): int(v) for k, v in family_measured.to_dict().items()}
    
    # DOI uniqueness
    if 'source_refs' in df.columns:
        doi_list = []
        for refs in df[df['contrast_value'].notna()]['source_refs'].dropna():
            # Extract DOIs from refs string
            dois = [r.strip() for r in str(refs).split(';') if 'DOI:' in r or 'doi:' in r or '10.' in r]
            doi_list.extend(dois)
        
        unique_dois = int(len(set(doi_list)))
        total_dois = int(len(doi_list))
        unique_doi_rate = unique_dois / total_dois if total_dois > 0 else 0
    else:
        unique_dois = 0
        total_dois = 0
        unique_doi_rate = 0
    
    # License analysis
    if 'license_source' in df.columns:
        license_counts = {str(k): int(v) for k, v in df['license_source'].value_counts().to_dict().items()}
        
        # Check license_ok_rate (CC-BY, CC0, CC BY-SA)
        ok_licenses = ['CC BY', 'CC0', 'CC BY-SA', 'CC BY 4.0', 'CC BY-SA 4.0']
        license_ok = int(df['license_source'].apply(
            lambda x: any(ok in str(x) for ok in ok_licenses) if pd.notna(x) else False
        ).sum())
        license_ok_rate = license_ok / N_total if N_total > 0 else 0
    else:
        license_counts = {}
        license_ok_rate = 0
    
    # Source breakdown
    source_counts = {}
    if 'source' in df.columns:
        source_counts = {str(k): int(v) for k, v in df['source'].value_counts().to_dict().items()}
    
    # Biosensor vs FP
    biosensor_count = int(df['is_biosensor'].sum()) if 'is_biosensor' in df.columns else 0
    fp_count = int(N_total - biosensor_count)
    
    # Contrast statistics (for measured only)
    measured_df = df[df['contrast_value'].notna()]
    contrast_stats = {
        'mean': float(measured_df['contrast_value'].mean()) if len(measured_df) > 0 else None,
        'median': float(measured_df['contrast_value'].median()) if len(measured_df) > 0 else None,
        'min': float(measured_df['contrast_value'].min()) if len(measured_df) > 0 else None,
        'max': float(measured_df['contrast_value'].max()) if len(measured_df) > 0 else None,
        'std': float(measured_df['contrast_value'].std()) if len(measured_df) > 0 else None
    }
    
    # QA pass/fail
    thresholds = {
        'N_total_min': 200,
        'N_measured_min': 120,
        'families_with_ge_5_min': 10,
        'unique_doi_rate_min': 0.85,
        'license_ok_rate_min': 1.0
    }
    
    qa_results = {
        'N_total': {'value': N_total, 'threshold': thresholds['N_total_min'], 'pass': N_total >= thresholds['N_total_min']},
        'N_measured': {'value': N_measured, 'threshold': thresholds['N_measured_min'], 'pass': N_measured >= thresholds['N_measured_min']},
        'families_with_ge_5': {'value': families_with_ge_5, 'threshold': thresholds['families_with_ge_5_min'], 'pass': families_with_ge_5 >= thresholds['families_with_ge_5_min']},
        'unique_doi_rate': {'value': round(unique_doi_rate, 3), 'threshold': thresholds['unique_doi_rate_min'], 'pass': unique_doi_rate >= thresholds['unique_doi_rate_min']},
        'license_ok_rate': {'value': round(license_ok_rate, 3), 'threshold': thresholds['license_ok_rate_min'], 'pass': license_ok_rate >= thresholds['license_ok_rate_min']}
    }
    
    all_pass = all(qa_results[k]['pass'] for k in qa_results)
    
    return {
        'version': '1.3.0',
        'generated': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'dataset_path': 'data/processed/atlas_fp_optical_v1_3.csv',
        
        'counts': {
            'N_total': N_total,
            'N_measured': N_measured,
            'N_measured_A': N_measured_A,
            'N_measured_B': N_measured_B,
            'N_measured_C': N_measured_C,
            'N_biosensor': biosensor_count,
            'N_standard_fp': fp_count
        },
        
        'families': {
            'families_with_ge_5': families_with_ge_5,
            'family_breakdown': family_breakdown
        },
        
        'dois': {
            'unique_dois': unique_dois,
            'total_dois': total_dois,
            'unique_doi_rate': round(unique_doi_rate, 3)
        },
        
        'licenses': {
            'license_ok_rate': round(license_ok_rate, 3),
            'license_breakdown': license_counts
        },
        
        'sources': source_counts,
        
        'contrast_statistics': contrast_stats,
        
        'qa_results': qa_results,
        
        'overall_qa_status': 'PASS' if all_pass else 'FAIL',
        'blocking_issues': [k for k, v in qa_results.items() if not v['pass']]
    }

def main():
    """Main function."""
    print("=" * 70)
    print("Generate METRICS v1.3 - Machine-Readable Report")
    print("=" * 70)
    
    # Load atlas
    df = load_atlas()
    print(f"Loaded {len(df)} systems from atlas")
    
    # Compute metrics
    metrics = compute_metrics(df)
    
    # Save JSON
    output_path = Path("reports/METRICS_v1.3.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    print(f"\nOK Metrics saved to: {output_path}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"N_total:              {metrics['counts']['N_total']} (threshold: 200)")
    print(f"N_measured (A+B):     {metrics['counts']['N_measured']} (threshold: 120)")
    print(f"  - Tier A:           {metrics['counts']['N_measured_A']}")
    print(f"  - Tier B:           {metrics['counts']['N_measured_B']}")
    print(f"  - Tier C:           {metrics['counts']['N_measured_C']}")
    print(f"Families (>=5 meas):   {metrics['families']['families_with_ge_5']} (threshold: 10)")
    print(f"Unique DOI rate:      {metrics['dois']['unique_doi_rate']:.3f} (threshold: 0.850)")
    print(f"License OK rate:      {metrics['licenses']['license_ok_rate']:.3f} (threshold: 1.000)")
    print(f"\nOverall QA: {metrics['overall_qa_status']}")
    
    if metrics['blocking_issues']:
        print(f"\nBlocking issues: {', '.join(metrics['blocking_issues'])}")
    
    return 0 if metrics['overall_qa_status'] == 'PASS' else 1

if __name__ == "__main__":
    sys.exit(main())

