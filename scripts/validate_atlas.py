#!/usr/bin/env python3
"""
Validation Script for Biological Qubits Atlas
==============================================

Vérifie l'intégrité et la cohérence du dataset atlas_fp_optical_v2_2.csv

Usage:
    python scripts/validate_atlas.py

Returns:
    Exit code 0 si validation OK, 1 si erreurs critiques
"""

import sys
from pathlib import Path
import pandas as pd
import re


def validate_atlas(csv_path: Path, tier_name: str = "MIXED") -> bool:
    """
    Valide le dataset principal de l'atlas.
    
    Args:
        csv_path: Path to CSV file
        tier_name: Tier name for reporting (CURATED, CANDIDATES, UNKNOWN, MIXED)
    
    Returns:
        True si validation complète réussie, False sinon
    """
    print(f"[*] Validation de l'atlas ({tier_name}): {csv_path}")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. Charger le fichier
    try:
        df = pd.read_csv(csv_path)
        print(f"[OK] {len(df)} systemes charges")
    except Exception as e:
        print(f"[ERREUR] Impossible de charger {csv_path}")
        print(f"   Detail: {e}")
        return False
    
    # 2. Vérifier les colonnes obligatoires
    # NOTE: license, temperature_K, method sont optionnels car souvent impossibles
    # a determiner sans fabrication de donnees (voir ATLAS_SPEC.md)
    required_cols = [
        'SystemID',
        'protein_name', 
        'family', 
        'is_biosensor',
        'contrast_normalized',
        'doi',
        'curator'
    ]
    
    # Colonnes fortement recommandees mais acceptees vides si donnees indisponibles
    recommended_cols = [
        'quality_tier',
        'temperature_K',
        'license',
        'method'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        errors.append(f"Colonnes obligatoires manquantes: {missing_cols}")
        print(f"[ERREUR] Colonnes obligatoires manquantes: {missing_cols}")
    else:
        print(f"[OK] Toutes les colonnes obligatoires presentes ({len(required_cols)})")
    
    # 3. Vérifier les valeurs manquantes critiques (colonnes OBLIGATOIRES)
    for col in required_cols:
        if col not in df.columns:
            continue
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            errors.append(f"Colonne '{col}': {missing_count} valeurs manquantes")
            print(f"[ERREUR] Colonne '{col}': {missing_count} valeurs manquantes")
    
    # 3b. Vérifier les colonnes recommandees (avertissements seulement)
    for col in recommended_cols:
        if col not in df.columns:
            continue
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            warnings.append(f"Colonne recommandee '{col}': {missing_count} valeurs manquantes")
            print(f"[INFO] Colonne recommandee '{col}': {missing_count} manquantes (acceptable si donnees indisponibles)")
    
    # 4. Vérifier les valeurs optionnelles
    optional_cols = ['pH', 'pmcid', 'excitation_nm', 'emission_nm']
    for col in optional_cols:
        if col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                warnings.append(f"Colonne '{col}': {missing_count} valeurs manquantes (non-bloquant)")
                print(f"[WARN] Colonne '{col}': {missing_count} valeurs manquantes (non-bloquant)")
    
    # 5. Vérifier la plausibilité des températures
    if 'temperature_K' in df.columns:
        temp_min = df['temperature_K'].min()
        temp_max = df['temperature_K'].max()
        out_of_range = df[(df['temperature_K'] < 270) | (df['temperature_K'] > 320)]
        
        if len(out_of_range) > 0:
            warnings.append(f"{len(out_of_range)} systemes hors plage bio (270-320K)")
            print(f"[WARN] {len(out_of_range)} systemes hors plage biologique (270-320K)")
            print(f"   Plage actuelle: {temp_min:.1f}K - {temp_max:.1f}K")
        else:
            print(f"[OK] Toutes les temperatures dans la plage biologique (270-320K)")
    
    # 6. Vérifier les contrastes
    if 'contrast_normalized' in df.columns:
        invalid_contrast = df[df['contrast_normalized'] <= 0]
        if len(invalid_contrast) > 0:
            errors.append(f"{len(invalid_contrast)} systemes avec contraste <= 0")
            print(f"[ERREUR] {len(invalid_contrast)} systemes avec contraste <= 0")
        
        # Stats descriptives
        contrast_min = df['contrast_normalized'].min()
        contrast_max = df['contrast_normalized'].max()
        contrast_mean = df['contrast_normalized'].mean()
        print(f"[STATS] Contraste: min={contrast_min:.2f}, max={contrast_max:.2f}, moyenne={contrast_mean:.2f}")
    
    # 7. Vérifier les DOI (format basique)
    if 'doi' in df.columns:
        doi_pattern = re.compile(r'^10\.\d{4,}/.+')
        invalid_doi = df[~df['doi'].apply(lambda x: bool(doi_pattern.match(str(x))) if pd.notna(x) else False)]
        if len(invalid_doi) > 0:
            warnings.append(f"{len(invalid_doi)} DOI avec format suspect")
            print(f"[WARN] {len(invalid_doi)} DOI avec format potentiellement invalide")
    
    # 8. Vérifier les familles
    if 'family' in df.columns:
        families = df['family'].value_counts()
        print(f"\n[STATS] Distribution par famille:")
        for family, count in families.head(10).items():
            print(f"   {family:20s}: {count:3d} systemes")
        if len(families) > 10:
            print(f"   ... et {len(families) - 10} autres familles")
    
    # 9. Vérifier les biosensors vs fluorophores
    if 'is_biosensor' in df.columns:
        biosensor_count = (df['is_biosensor'] == 1.0).sum()
        fluorophore_count = (df['is_biosensor'] == 0.0).sum()
        print(f"\n[STATS] Classification:")
        print(f"   Biosenseurs:  {biosensor_count:3d}")
        print(f"   Fluorophores: {fluorophore_count:3d}")
    
    # 10. Vérifier les quality tiers
    if 'quality_tier' in df.columns:
        tiers = df['quality_tier'].value_counts()
        print(f"\n[STATS] Qualite des donnees:")
        for tier, count in tiers.items():
            print(f"   Tier {tier}: {count:3d} systemes")
    
    # Résumé final
    print("\n" + "=" * 60)
    print("RESUME DE LA VALIDATION")
    print("=" * 60)
    
    if errors:
        print(f"[ERREUR] {len(errors)} erreur(s) critique(s):")
        for error in errors:
            print(f"   - {error}")
    else:
        print("[OK] Aucune erreur critique")
    
    if warnings:
        print(f"\n[WARN] {len(warnings)} avertissement(s):")
        for warning in warnings:
            print(f"   - {warning}")
    
    if not errors and not warnings:
        print("\n[SUCCESS] Dataset parfaitement valide!")
    elif not errors:
        print("\n[OK] Dataset valide (avec avertissements mineurs)")
    
    return len(errors) == 0


def main():
    """Point d'entrée principal."""
    import sys
    
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    # Parse arguments
    tier_arg = sys.argv[1] if len(sys.argv) > 1 else "mixed"
    
    # Map tier to file
    tier_files = {
        "curated": ("data/processed/atlas_fp_optical_v2_2_curated.csv", "CURATED"),
        "candidates": ("data/staging/atlas_fp_optical_v2_2_candidates.csv", "CANDIDATES"),
        "unknown": ("data/staging/atlas_fp_optical_v2_2_unknown.csv", "UNKNOWN"),
        "mixed": ("data/processed/atlas_fp_optical_v2_2.csv", "MIXED")
    }
    
    if tier_arg not in tier_files:
        print(f"[ERROR] Unknown tier: {tier_arg}")
        print(f"Usage: python scripts/validate_atlas.py [curated|candidates|unknown|mixed]")
        return 1
    
    csv_rel, tier_name = tier_files[tier_arg]
    csv_path = repo_root / csv_rel
    
    if not csv_path.exists():
        print(f"[ERREUR] Fichier introuvable: {csv_path}")
        print(f"   Tier: {tier_name}")
        return 1
    
    # Validation
    success = validate_atlas(csv_path, tier_name)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

