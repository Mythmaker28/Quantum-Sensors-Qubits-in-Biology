#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA Script: Audit FP Optical v1.2
=================================
Vérifie les seuils bloquants:
- N_fp_like_total >= 50
- N_fp_like_with_contrast_measured >= 25

Génère:
- reports/AUDIT_v1.2_fp_optical.md
- reports/MISSING_FP_WITH_CONTRAST.md
- patch/SCHEMA_MAP.yaml

Exit code ≠ 0 si seuils non atteints.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
import yaml

# Paths
FP_OPTICAL_FILE = Path("data/processed/atlas_fp_optical.csv")
METADATA_FILE = Path("data/processed/TRAINING.METADATA.json")
AUDIT_REPORT = Path("reports/AUDIT_v1.2_fp_optical.md")
MISSING_REPORT = Path("reports/MISSING_FP_WITH_CONTRAST.md")
SCHEMA_MAP = Path("patch/SCHEMA_MAP.yaml")

# Thresholds
MIN_TOTAL = 50
MIN_MEASURED = 25

def load_data() -> pd.DataFrame:
    """Charge les données FP optical."""
    if not FP_OPTICAL_FILE.exists():
        print(f"ERROR: {FP_OPTICAL_FILE} not found!", file=sys.stderr)
        sys.exit(1)
    
    df = pd.read_csv(FP_OPTICAL_FILE)
    print(f"Loaded {len(df)} FP optical entries")
    return df

def compute_metrics(df: pd.DataFrame) -> dict:
    """Calcule les métriques QA."""
    
    n_total = len(df)
    n_measured = (df['contrast_source'] == 'measured').sum()
    n_computed = (df['contrast_source'] == 'computed').sum()
    n_any_contrast = ((df['contrast_source'] == 'measured') | 
                      (df['contrast_source'] == 'computed')).sum()
    n_biosensor = (df['is_biosensor'] == 1).sum()
    
    # Check missing critical fields
    n_missing_ex = df['excitation_nm'].isna().sum()
    n_missing_em = df['emission_nm'].isna().sum()
    n_missing_uniprot = df['uniprot_id'].isna().sum()
    n_missing_pdb = df['pdb_id'].isna().sum()
    
    metrics = {
        'n_fp_like_total': int(n_total),
        'n_fp_like_with_contrast_measured': int(n_measured),
        'n_fp_like_with_contrast_computed': int(n_computed),
        'n_fp_like_with_contrast_any': int(n_any_contrast),
        'n_biosensors': int(n_biosensor),
        'n_missing_excitation': int(n_missing_ex),
        'n_missing_emission': int(n_missing_em),
        'n_missing_uniprot': int(n_missing_uniprot),
        'n_missing_pdb': int(n_missing_pdb),
    }
    
    return metrics

def check_thresholds(metrics: dict) -> bool:
    """Vérifie les seuils bloquants."""
    passed = True
    
    if metrics['n_fp_like_total'] < MIN_TOTAL:
        print(f"❌ FAIL: Total FP entries ({metrics['n_fp_like_total']}) < {MIN_TOTAL}", file=sys.stderr)
        passed = False
    else:
        print(f"✓ PASS: Total FP entries ({metrics['n_fp_like_total']}) >= {MIN_TOTAL}")
    
    if metrics['n_fp_like_with_contrast_measured'] < MIN_MEASURED:
        print(f"❌ FAIL: Measured contrast ({metrics['n_fp_like_with_contrast_measured']}) < {MIN_MEASURED}", file=sys.stderr)
        passed = False
    else:
        print(f"✓ PASS: Measured contrast ({metrics['n_fp_like_with_contrast_measured']}) >= {MIN_MEASURED}")
    
    return passed

def generate_audit_report(df: pd.DataFrame, metrics: dict, passed: bool):
    """Génère le rapport d'audit."""
    AUDIT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    
    with open(AUDIT_REPORT, 'w', encoding='utf-8') as f:
        f.write("# Atlas FP Optical v1.2 — Audit Report\n\n")
        f.write(f"**Date**: {datetime.now().isoformat()}\n")
        f.write(f"**Status**: {'✓ PASS' if passed else '❌ FAIL'}\n\n")
        
        f.write("## Quality Thresholds\n\n")
        f.write("| Metric | Value | Threshold | Status |\n")
        f.write("|--------|-------|-----------|--------|\n")
        
        total_status = "✓" if metrics['n_fp_like_total'] >= MIN_TOTAL else "❌"
        f.write(f"| Total FP entries | {metrics['n_fp_like_total']} | ≥ {MIN_TOTAL} | {total_status} |\n")
        
        measured_status = "✓" if metrics['n_fp_like_with_contrast_measured'] >= MIN_MEASURED else "❌"
        f.write(f"| Measured contrast | {metrics['n_fp_like_with_contrast_measured']} | ≥ {MIN_MEASURED} | {measured_status} |\n")
        
        f.write("\n## Summary Statistics\n\n")
        f.write(f"- **Total FP-like entries**: {metrics['n_fp_like_total']}\n")
        f.write(f"- **With measured contrast**: {metrics['n_fp_like_with_contrast_measured']} ({metrics['n_fp_like_with_contrast_measured']/max(metrics['n_fp_like_total'],1)*100:.1f}%)\n")
        f.write(f"- **With computed contrast**: {metrics['n_fp_like_with_contrast_computed']} ({metrics['n_fp_like_with_contrast_computed']/max(metrics['n_fp_like_total'],1)*100:.1f}%)\n")
        f.write(f"- **With any contrast**: {metrics['n_fp_like_with_contrast_any']} ({metrics['n_fp_like_with_contrast_any']/max(metrics['n_fp_like_total'],1)*100:.1f}%)\n")
        f.write(f"- **Biosensors**: {metrics['n_biosensors']}\n\n")
        
        f.write("## Data Completeness\n\n")
        f.write(f"- **Missing excitation wavelength**: {metrics['n_missing_excitation']}\n")
        f.write(f"- **Missing emission wavelength**: {metrics['n_missing_emission']}\n")
        f.write(f"- **Missing UniProt ID**: {metrics['n_missing_uniprot']}\n")
        f.write(f"- **Missing PDB ID**: {metrics['n_missing_pdb']}\n\n")
        
        # Histograms
        f.write("## Distributions\n\n")
        
        # Family distribution
        if 'family' in df.columns:
            family_counts = df['family'].value_counts().head(10)
            f.write("### Top 10 Families\n\n")
            f.write("| Family | Count |\n")
            f.write("|--------|-------|\n")
            for family, count in family_counts.items():
                f.write(f"| {family} | {count} |\n")
            f.write("\n")
        
        # Contrast distribution
        contrast_df = df[df['contrast_ratio'].notna()]
        if not contrast_df.empty:
            f.write("### Contrast Ratio Distribution\n\n")
            f.write(f"- **Mean**: {contrast_df['contrast_ratio'].mean():.2f}\n")
            f.write(f"- **Median**: {contrast_df['contrast_ratio'].median():.2f}\n")
            f.write(f"- **Min**: {contrast_df['contrast_ratio'].min():.2f}\n")
            f.write(f"- **Max**: {contrast_df['contrast_ratio'].max():.2f}\n\n")
    
    print(f"Audit report saved to {AUDIT_REPORT}")

def generate_missing_report(df: pd.DataFrame):
    """Génère le rapport des FP manquants avec contraste."""
    MISSING_REPORT.parent.mkdir(parents=True, exist_ok=True)
    
    # FP sans contraste mesuré
    no_contrast_df = df[df['contrast_source'] != 'measured'].copy()
    
    with open(MISSING_REPORT, 'w', encoding='utf-8') as f:
        f.write("# Missing FP with Contrast — Action Plan\n\n")
        f.write(f"**Date**: {datetime.now().isoformat()}\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"Total FP entries without measured contrast: **{len(no_contrast_df)}**\n\n")
        
        if len(no_contrast_df) > 0:
            f.write("## Actionable Candidates\n\n")
            f.write("Ces protéines nécessitent une recherche manuelle de publications pour extraire les mesures de contraste.\n\n")
            
            f.write("| SystemID | Protein Name | Family | Source | Has Proxy |\n")
            f.write("|----------|--------------|--------|--------|----------|\n")
            
            for _, row in no_contrast_df.head(20).iterrows():  # Top 20
                has_proxy = "✓" if row.get('contrast_source') == 'computed' else "✗"
                f.write(f"| {row['SystemID']} | {row['protein_name']} | {row.get('family', 'N/A')} | {row.get('source_refs', 'N/A')} | {has_proxy} |\n")
            
            f.write("\n## Recommendations\n\n")
            f.write("1. **Littérature mining manuel**: Rechercher publications spécifiques pour chaque biosenseur\n")
            f.write("2. **Contact auteurs**: Pour biosenseurs récents, contacter directement les auteurs\n")
            f.write("3. **Experimental proxies**: Utiliser brightness/QY comme proxy temporaire\n")
            f.write("4. **Crowdsourcing**: Solliciter la communauté via GitHub issues\n\n")
    
    print(f"Missing report saved to {MISSING_REPORT}")

def generate_schema_map():
    """Génère le schema map avec aliases."""
    SCHEMA_MAP.parent.mkdir(parents=True, exist_ok=True)
    
    schema_map = {
        'version': '1.2.0',
        'description': 'Schema mapping and aliases for Atlas FP Optical',
        'column_aliases': {
            'SystemID': ['system_id', 'id', 'entry_id'],
            'protein_name': ['name', 'protein', 'fp_name'],
            'excitation_nm': ['ex_max', 'excitation', 'ex_wavelength'],
            'emission_nm': ['em_max', 'emission', 'em_wavelength'],
            'contrast_ratio': ['delta_f_f0', 'contrast', 'dynamic_range', 'on_off_ratio'],
            'quantum_yield': ['qy', 'φ'],
            'extinction_coef': ['epsilon', 'ε', 'ext_coeff']
        },
        'parsing_rules': {
            'wavelength_units': 'nanometers (nm)',
            'temperature_units': 'Kelvin (K)',
            'contrast_interpretation': 'ΔF/F₀, on/off ratio, or fold-change (dimensionless)',
            'ci_interpretation': '95% confidence interval'
        }
    }
    
    with open(SCHEMA_MAP, 'w', encoding='utf-8') as f:
        yaml.dump(schema_map, f, default_flow_style=False, allow_unicode=True)
    
    print(f"Schema map saved to {SCHEMA_MAP}")

def main():
    """Point d'entrée."""
    print("=" * 70)
    print("Audit FP Optical v1.2 Pipeline")
    print("=" * 70)
    
    # Load
    df = load_data()
    
    # Compute metrics
    metrics = compute_metrics(df)
    
    print("\nMetrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Check thresholds
    print("\nThreshold checks:")
    passed = check_thresholds(metrics)
    
    # Generate reports
    print("\nGenerating reports...")
    generate_audit_report(df, metrics, passed)
    generate_missing_report(df)
    generate_schema_map()
    
    # Print summary for user
    print("\n" + "=" * 70)
    print("AUDIT SUMMARY")
    print("=" * 70)
    print(f"N_fp_like_total = {metrics['n_fp_like_total']}")
    print(f"N_fp_like_with_contrast_measured = {metrics['n_fp_like_with_contrast_measured']}")
    print(f"N_fp_like_with_contrast_any = {metrics['n_fp_like_with_contrast_any']}")
    print()
    print(f"Paths:")
    print(f"  {FP_OPTICAL_FILE}")
    print(f"  {AUDIT_REPORT}")
    print(f"  {MISSING_REPORT}")
    print("=" * 70)
    
    if not passed:
        print("\n❌ AUDIT FAILED - Thresholds not met", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n✓ AUDIT PASSED - All thresholds met")
        sys.exit(0)

if __name__ == "__main__":
    main()

