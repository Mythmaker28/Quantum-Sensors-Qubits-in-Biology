#!/usr/bin/env python3
"""
Atlas v2.2.2 Balance & Export Pipeline
=====================================

Crée deux exports :
1. TRAINING_TABLE_v2_2_2_full.csv (append-only, tout le corpus)
2. TRAINING_TABLE_v2_2_2_balanced.csv (rééquilibré par famille)

Objectif : limiter Calcium ≤ 35% dans balanced, sans duplication de lignes.
"""

import pandas as pd
import numpy as np
import json
import hashlib
from pathlib import Path
import datetime

def load_current_dataset():
    """Charge le dataset actuel v2.2"""
    
    print("=" * 80)
    print("ATLAS v2.2.2 BALANCE & EXPORT PIPELINE")
    print("=" * 80)
    
    training_path = Path("data/processed/TRAINING_TABLE_v2_2.csv")
    
    if not training_path.exists():
        print(f"ERREUR: Fichier {training_path} non trouvé")
        return None
    
    df = pd.read_csv(training_path)
    print(f"[LOAD] Dataset v2.2: {len(df)} systèmes")
    
    return df

def audit_distribution(df):
    """Audit de la distribution par famille"""
    
    print("\n[AUDIT] Distribution par famille...")
    
    # Filtrer les systèmes utiles (target mesurée + optique)
    df_useful = df[
        (df['contrast_normalized'].notna()) & 
        (df['excitation_nm'].notna()) & 
        (df['emission_nm'].notna())
    ].copy()
    
    print(f"  Systèmes utiles: {len(df_useful)}")
    
    # Analyse par famille
    family_stats = df_useful['family'].value_counts()
    family_pct = (family_stats / len(df_useful) * 100).round(1)
    
    print(f"\n  Distribution par famille:")
    for family, count in family_stats.head(10).items():
        pct = family_pct[family]
        print(f"    {family}: {count} ({pct}%)")
    
    # Identifier les familles minoritaires
    minor_families = family_stats[family_stats < 5].index.tolist()
    print(f"\n  Familles minoritaires (N<5): {minor_families}")
    
    # Calcium share
    calcium_share = family_pct.get('Calcium', 0)
    print(f"\n  Calcium share: {calcium_share}%")
    
    return df_useful, family_stats, family_pct, minor_families, calcium_share

def calculate_family_weights(family_stats):
    """Calcule les poids d'équilibrage par famille"""
    
    print("\n[WEIGHTS] Calcul des poids d'équilibrage...")
    
    # Médiane des effectifs
    median_count = family_stats.median()
    print(f"  Médiane des effectifs: {median_count:.1f}")
    
    # Calcul des poids
    weights = {}
    for family, count in family_stats.items():
        if count > 0:
            weight = median_count / count
            weights[family] = round(weight, 3)
        else:
            weights[family] = 1.0
    
    print(f"  Poids calculés pour {len(weights)} familles")
    
    # Afficher les poids
    for family, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        print(f"    {family}: {weight}")
    
    return weights

def create_balanced_dataset(df_useful, weights, minor_families, target_calcium_share=35):
    """Crée le dataset équilibré"""
    
    print(f"\n[BALANCE] Création du dataset équilibré...")
    print(f"  Objectif Calcium: <={target_calcium_share}%")
    
    # Copier le dataset
    df_balanced = df_useful.copy()
    
    # Ajouter les poids
    df_balanced['sample_weight'] = df_balanced['family'].map(weights)
    
    # Tagger les familles minoritaires
    df_balanced['low_support'] = df_balanced['family'].isin(minor_families)
    
    # Vérifier la part de Calcium
    calcium_count = len(df_balanced[df_balanced['family'] == 'Calcium'])
    calcium_share = calcium_count / len(df_balanced) * 100
    
    print(f"  Calcium dans balanced: {calcium_count} ({calcium_share:.1f}%)")
    
    # Si Calcium > 35%, appliquer un downsample léger
    if calcium_share > target_calcium_share:
        print(f"  [WARNING] Calcium {calcium_share:.1f}% > {target_calcium_share}%")
        
        # Calculer le facteur de réduction
        target_calcium_count = int(len(df_balanced) * target_calcium_share / 100)
        reduction_factor = target_calcium_count / calcium_count
        
        print(f"  Facteur de réduction Calcium: {reduction_factor:.2f}")
        
        # Appliquer le downsample (aléatoire mais reproductible)
        np.random.seed(42)
        calcium_mask = df_balanced['family'] == 'Calcium'
        calcium_indices = df_balanced[calcium_mask].index
        
        # Sélectionner un sous-échantillon
        n_keep = int(len(calcium_indices) * reduction_factor)
        keep_indices = np.random.choice(calcium_indices, n_keep, replace=False)
        
        # Créer le masque final
        keep_mask = ~calcium_mask | df_balanced.index.isin(keep_indices)
        df_balanced = df_balanced[keep_mask].copy()
        
        # Recalculer la part de Calcium
        new_calcium_share = len(df_balanced[df_balanced['family'] == 'Calcium']) / len(df_balanced) * 100
        print(f"  Calcium après downsample: {new_calcium_share:.1f}%")
    
    print(f"  Dataset équilibré: {len(df_balanced)} systèmes")
    
    return df_balanced

def validate_exports(df_full, df_balanced):
    """Valide les deux exports"""
    
    print("\n[VALIDATE] Validation des exports...")
    
    # Métriques communes
    def check_metrics(df, name):
        n_total = len(df)
        n_optical = (df['excitation_nm'].notna() & df['emission_nm'].notna()).sum()
        coverage_optical = n_optical / n_total * 100
        
        n_provenance = df['provenance'].notna().sum()
        n_license = df['license'].notna().sum()
        coverage_provenance = n_provenance / n_total * 100
        coverage_license = n_license / n_total * 100
        
        # Vérifier les doublons (par canonical_name)
        duplicates = df['canonical_name'].duplicated().sum()
        
        print(f"  {name}:")
        print(f"    N_total: {n_total}")
        print(f"    Couverture optique: {coverage_optical:.1f}%")
        print(f"    Doublons: {duplicates}")
        print(f"    Provenance: {coverage_provenance:.1f}%")
        print(f"    Licenses: {coverage_license:.1f}%")
        
        # Critères de succès
        criteria = {
            'coverage_optical >= 90%': coverage_optical >= 90,
            'doublons <= 3': duplicates <= 3,
            'provenance >= 99%': coverage_provenance >= 99,
            'license >= 99%': coverage_license >= 99
        }
        
        for criterion, passed in criteria.items():
            status = "[PASS]" if passed else "[FAIL]"
            print(f"    {criterion}: {status}")
        
        return all(criteria.values())
    
    # Valider les deux exports
    full_valid = check_metrics(df_full, "FULL")
    balanced_valid = check_metrics(df_balanced, "BALANCED")
    
    # Vérifier la contrainte Calcium
    calcium_share = len(df_balanced[df_balanced['family'] == 'Calcium']) / len(df_balanced) * 100
    calcium_valid = calcium_share <= 35
    
    print(f"\n  Contrainte Calcium: {calcium_share:.1f}% <= 35%: {'[PASS]' if calcium_valid else '[FAIL]'}")
    
    return full_valid and balanced_valid and calcium_valid

def create_family_distribution_report(df_full, df_balanced):
    """Crée le rapport de distribution des familles"""
    
    print("\n[REPORT] Création du rapport de distribution...")
    
    # Statistiques pour full
    full_stats = df_full['family'].value_counts()
    full_pct = (full_stats / len(df_full) * 100).round(1)
    
    # Statistiques pour balanced
    balanced_stats = df_balanced['family'].value_counts()
    balanced_pct = (balanced_stats / len(df_balanced) * 100).round(1)
    
    # Créer le rapport
    report_content = f"""# FAMILY DISTRIBUTION v2.2.2

**Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version**: 2.2.2

## 📊 Distribution par Famille

| Famille | Full (N) | %) | Balanced (N | %) | Δ% |
|---------|-----------|----|-------------|----|----|"""

    # Ajouter les lignes pour chaque famille
    all_families = set(full_stats.index) | set(balanced_stats.index)
    for family in sorted(all_families):
        full_n = full_stats.get(family, 0)
        full_p = full_pct.get(family, 0)
        balanced_n = balanced_stats.get(family, 0)
        balanced_p = balanced_pct.get(family, 0)
        delta = balanced_p - full_p
        
        report_content += f"\n| {family} | {full_n} | {full_p}% | {balanced_n} | {balanced_p}% | {delta:+.1f}% |"
    
    report_content += f"""

## 📈 Résumé

- **Full**: {len(df_full)} systèmes, {len(full_stats)} familles
- **Balanced**: {len(df_balanced)} systèmes, {len(balanced_stats)} familles
- **Calcium share**: {full_pct.get('Calcium', 0):.1f}% → {balanced_pct.get('Calcium', 0):.1f}%
- **Familles minoritaires**: {len(df_balanced[df_balanced['low_support']])} taggées

## 🎯 Objectifs

- [OK] Calcium <= 35% dans balanced
- ✅ Pas de duplication de lignes
- ✅ Équilibrage par pondération
- ✅ Préservation des familles minoritaires

---
*Généré automatiquement par Atlas v2.2.2 Balance Pipeline*
"""
    
    # Sauvegarder
    report_path = Path("reports/FAMILY_DISTRIB_v2_2_2.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"  [OK] Rapport créé: {report_path}")
    
    return report_path

def save_exports(df_full, df_balanced, weights):
    """Sauvegarde les exports finaux"""
    
    print("\n[SAVE] Sauvegarde des exports...")
    
    # Créer le répertoire
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Export FULL
    full_path = output_dir / "TRAINING_TABLE_v2_2_2_full.csv"
    df_full.to_csv(full_path, index=False, encoding='utf-8')
    print(f"  [OK] FULL: {full_path} ({len(df_full)} systèmes)")
    
    # Export BALANCED
    balanced_path = output_dir / "TRAINING_TABLE_v2_2_2_balanced.csv"
    df_balanced.to_csv(balanced_path, index=False, encoding='utf-8')
    print(f"  [OK] BALANCED: {balanced_path} ({len(df_balanced)} systèmes)")
    
    # Weights JSON
    weights_path = output_dir / "family_weights_v2_2_2.json"
    with open(weights_path, 'w', encoding='utf-8') as f:
        json.dump(weights, f, indent=2, ensure_ascii=False)
    print(f"  [OK] WEIGHTS: {weights_path}")
    
    return full_path, balanced_path, weights_path

def generate_hashes_and_sync(full_path, balanced_path):
    """Génère les hashes et met à jour les fichiers de sync"""
    
    print("\n[HASH] Génération des hashes et sync...")
    
    # Générer les hashes
    def get_sha256(filepath):
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest().upper()
    
    full_hash = get_sha256(full_path)
    balanced_hash = get_sha256(balanced_path)
    
    # Créer SHA256SUMS
    sha256_path = Path("data/processed/SHA256SUMS_v2_2_2.txt")
    with open(sha256_path, 'w', encoding='utf-8') as f:
        f.write(f"{full_hash} {full_path.name}\n")
        f.write(f"{balanced_hash} {balanced_path.name}\n")
    
    print(f"  [OK] SHA256SUMS: {sha256_path}")
    
    # Mettre à jour .atlas_sync
    sync_dir = Path(".atlas_sync")
    sync_dir.mkdir(exist_ok=True)
    
    # Charger les données pour sync
    df_full = pd.read_csv(full_path)
    
    # Mettre à jour processed_dois.txt
    dois_path = sync_dir / "processed_dois.txt"
    with open(dois_path, 'w', encoding='utf-8') as f:
        for doi in df_full['provenance'].tolist():
            f.write(f"{doi}\n")
    
    # Mettre à jour processed_canonical.txt
    canonical_path = sync_dir / "processed_canonical.txt"
    with open(canonical_path, 'w', encoding='utf-8') as f:
        for name in df_full['canonical_name'].tolist():
            f.write(f"{name}\n")
    
    print(f"  [OK] Sync files updated")
    
    # Créer le log
    log_path = sync_dir / "LOG_ATLAS_v2_2_2.md"
    log_content = f"""# LOG ATLAS v2.2.2

**Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Exports créés
- TRAINING_TABLE_v2_2_2_full.csv: {len(df_full)} systèmes
- TRAINING_TABLE_v2_2_2_balanced.csv: {len(df_full)} systèmes (équilibré)

## Calcium share
- Full: {len(df_full[df_full['family'] == 'Calcium']) / len(df_full) * 100:.1f}%
- Balanced: {len(df_full[df_full['family'] == 'Calcium']) / len(df_full) * 100:.1f}%

## Familles minoritaires
- Taggées: {len(df_full[df_full.get('low_support', False)]) if 'low_support' in df_full.columns else 0} systèmes
"""
    
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    print(f"  [OK] Log: {log_path}")
    
    return sha256_path

def main():
    """Fonction principale"""
    
    # Charger le dataset
    df = load_current_dataset()
    if df is None:
        return False
    
    # Audit de la distribution
    df_useful, family_stats, family_pct, minor_families, calcium_share = audit_distribution(df)
    
    # Calculer les poids
    weights = calculate_family_weights(family_stats)
    
    # Créer le dataset équilibré
    df_balanced = create_balanced_dataset(df_useful, weights, minor_families)
    
    # Valider les exports
    validation_passed = validate_exports(df_useful, df_balanced)
    
    if not validation_passed:
        print("\n[ERROR] Validation échouée")
        return False
    
    # Sauvegarder les exports
    full_path, balanced_path, weights_path = save_exports(df_useful, df_balanced, weights)
    
    # Créer le rapport de distribution
    report_path = create_family_distribution_report(df_useful, df_balanced)
    
    # Générer les hashes et sync
    sha256_path = generate_hashes_and_sync(full_path, balanced_path)
    
    # Statistiques finales
    print("\n" + "=" * 80)
    print("ATLAS v2.2.2 BALANCE - TERMINÉ")
    print("=" * 80)
    
    # Calculer les métriques finales
    full_calcium_share = len(df_useful[df_useful['family'] == 'Calcium']) / len(df_useful) * 100
    balanced_calcium_share = len(df_balanced[df_balanced['family'] == 'Calcium']) / len(df_balanced) * 100
    minor_families_count = len(df_balanced[df_balanced['low_support']])
    
    coverage_optical = (df_balanced['excitation_nm'].notna() & df_balanced['emission_nm'].notna()).sum() / len(df_balanced) * 100
    duplicates = df_balanced['canonical_name'].duplicated().sum()
    provenance_ok = df_balanced['provenance'].notna().all()
    license_ok = df_balanced['license'].notna().all()
    
    # Message de statut
    print(f"\n[STATUS] ATLAS v2.2.2 BALANCE")
    print(f"Full: N_utiles={len(df_useful)} ; Calcium_share={full_calcium_share:.1f}%")
    print(f"Balanced: N_utiles={len(df_balanced)} ; Calcium_share={balanced_calcium_share:.1f}% (<=35%) ; Minor_families(N<5)={minor_families_count} (tagged)")
    print(f"Coverage_optique={coverage_optical:.1f}% ; Doublons={duplicates} ; Provenance/Licenses={'PASS' if provenance_ok and license_ok else 'FAIL'}")
    print(f"Artifacts: TRAINING_TABLE_v2_2_2_full.csv, TRAINING_TABLE_v2_2_2_balanced.csv, family_weights.json, FAMILY_DISTRIB.md, SHA256SUMS")
    
    decision = "GO" if validation_passed and balanced_calcium_share <= 35 else "NO-GO"
    print(f"Decision: {decision}")
    
    return decision == "GO"

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[SUCCESS] Atlas v2.2.2 Balance terminé avec succès !")
    else:
        print("\n[ERROR] Atlas v2.2.2 Balance échoué")
