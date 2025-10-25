#!/usr/bin/env python3
"""
Analyse baseline du dataset v2.0 pour comprendre l'état actuel
avant la mise à jour v2.1
"""

import pandas as pd
import json
from pathlib import Path

def analyze_v2_0():
    """Analyse complète du dataset v2.0"""
    
    csv_path = Path("data/processed/atlas_fp_optical_v2_0.csv")
    
    if not csv_path.exists():
        print(f"Fichier non trouve: {csv_path}")
        return
    
    # Charger les données
    df = pd.read_csv(csv_path)
    
    print("=" * 80)
    print("ANALYSE BASELINE - Atlas v2.0")
    print("=" * 80)
    
    # Statistiques globales
    print("\n## STATISTIQUES GLOBALES")
    print(f"  Total lignes (avec header): {len(df) + 1}")
    print(f"  Total systèmes: {len(df)}")
    print(f"  Colonnes: {len(df.columns)}")
    
    # Systèmes mesurés
    has_contrast = df['contrast_value'].notna()
    n_measured = has_contrast.sum()
    print(f"\n  Systèmes avec contrast_value: {n_measured} ({n_measured/len(df)*100:.1f}%)")
    
    # Systèmes utiles (mesurés + features minimaux)
    has_excitation = df['excitation_nm'].notna() if 'excitation_nm' in df.columns else pd.Series([False]*len(df))
    has_emission = df['emission_nm'].notna() if 'emission_nm' in df.columns else pd.Series([False]*len(df))
    
    # Pour v2.0, on n'a pas de colonnes excitation_nm/emission_nm explicites
    # On va compter les systèmes mesurés comme utiles pour l'instant
    n_useful = n_measured
    print(f"  Systèmes utiles (mesurés): {n_useful}")
    
    # Noms uniques
    n_unique_names = df['protein_name'].nunique()
    print(f"  Noms de protéines uniques: {n_unique_names}")
    
    # Familles
    n_families = df['family'].nunique()
    print(f"  Familles: {n_families}")
    
    print("\n## DISTRIBUTION PAR FAMILLE (systèmes mesurés)")
    measured_df = df[has_contrast]
    family_counts = measured_df['family'].value_counts()
    
    for family, count in family_counts.head(15).items():
        print(f"  {family:20s}: {count:3d}")
    
    # Familles avec >=5 systèmes
    families_ge_5 = (family_counts >= 5).sum()
    print(f"\n  Familles avec >=5 systemes mesures: {families_ge_5}")
    
    # DOI uniqueness
    print("\n## PROVENANCE")
    dois = df[has_contrast]['doi'].dropna()
    n_unique_dois = dois.nunique()
    doi_rate = n_unique_dois / n_measured if n_measured > 0 else 0
    print(f"  DOIs uniques: {n_unique_dois}")
    print(f"  Taux de diversité DOI: {doi_rate:.2%}")
    
    # Licences
    print("\n## LICENCES")
    license_cc_by = df['license'].str.contains('CC BY', case=False, na=False).sum()
    license_uncertain = df['license'].str.contains('varies', case=False, na=False).sum()
    print(f"  Licence CC BY explicite: {license_cc_by}")
    print(f"  Licence incertaine ('varies'): {license_uncertain}")
    
    # Tiers de qualité
    print("\n## QUALITÉ")
    if 'quality_tier' in df.columns:
        tier_counts = df['quality_tier'].value_counts()
        for tier, count in sorted(tier_counts.items()):
            print(f"  Tier {tier}: {count}")
    
    # Sources
    print("\n## SOURCES")
    if 'source' in df.columns:
        source_counts = df['source'].value_counts()
        for source, count in source_counts.head(10).items():
            source_str = str(source)[:30]
            print(f"  {source_str:30s}: {count}")
    
    # Gap analysis vers objectif v2.1
    print("\n" + "=" * 80)
    print("GAP ANALYSIS - Objectif v2.1")
    print("=" * 80)
    
    target_useful = 120
    gap = target_useful - n_useful
    
    print(f"\n  Systèmes utiles actuels: {n_useful}")
    print(f"  Objectif v2.1: {target_useful}")
    print(f"  GAP: {gap} systèmes à ajouter")
    print(f"  % objectif atteint: {n_useful/target_useful*100:.1f}%")
    
    # Sauvegarder les métriques
    metrics = {
        "version": "2.0.0",
        "date_analysis": pd.Timestamp.now().isoformat(),
        "N_total": len(df),
        "N_measured": int(n_measured),
        "N_useful": int(n_useful),
        "N_unique_names": int(n_unique_names),
        "N_families": int(n_families),
        "N_families_ge_5": int(families_ge_5),
        "N_unique_dois": int(n_unique_dois),
        "doi_diversity_rate": float(doi_rate),
        "license_cc_by": int(license_cc_by),
        "license_uncertain": int(license_uncertain),
        "gap_to_v2_1": int(gap)
    }
    
    metrics_path = Path("reports/BASELINE_v2_0_metrics.json")
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    print(f"\nMetriques sauvegardees: {metrics_path}")
    
    return metrics

if __name__ == "__main__":
    analyze_v2_0()

