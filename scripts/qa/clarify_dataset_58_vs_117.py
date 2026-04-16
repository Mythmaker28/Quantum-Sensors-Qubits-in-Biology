#!/usr/bin/env python3
"""
Clarification dataset 58 vs 117
Analyse tous les fichiers CSV pour comprendre la différence
"""

import pandas as pd
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def analyze_csv_files():
    """Analyse tous les fichiers CSV dans data/qubits et data/processed"""
    
    results = []
    
    # Fichiers dans data/qubits
    qubits_dir = Path("data/qubits")
    if qubits_dir.exists():
        for csv_file in qubits_dir.glob("*.csv"):
            try:
                df = pd.read_csv(csv_file)
                results.append({
                    'fichier': str(csv_file),
                    'categorie': 'qubits',
                    'n_systemes': len(df),
                    'colonnes': len(df.columns),
                    'colonnes_liste': list(df.columns)[:5]  # Premières 5 colonnes
                })
            except Exception as e:
                results.append({
                    'fichier': str(csv_file),
                    'categorie': 'qubits',
                    'n_systemes': f'ERROR: {e}',
                    'colonnes': 0,
                    'colonnes_liste': []
                })
    
    # Fichiers dans data/processed (atlas FP)
    processed_dir = Path("data/processed")
    if processed_dir.exists():
        for csv_file in processed_dir.glob("*.csv"):
            try:
                df = pd.read_csv(csv_file)
                results.append({
                    'fichier': str(csv_file),
                    'categorie': 'processed',
                    'n_systemes': len(df),
                    'colonnes': len(df.columns),
                    'colonnes_liste': list(df.columns)[:5]
                })
            except Exception as e:
                results.append({
                    'fichier': str(csv_file),
                    'categorie': 'processed',
                    'n_systemes': f'ERROR: {e}',
                    'colonnes': 0,
                    'colonnes_liste': []
                })
    
    return results

def check_deduplication():
    """Vérifie la déduplication entre fichiers"""
    print("\n" + "=" * 80)
    print("ANALYSE DÉDUPLICATION")
    print("=" * 80)
    
    # Charger fichiers principaux
    files_to_check = [
        ("quantum_systems_unified_v2_3.csv", "data/qubits/quantum_systems_unified_v2_3.csv"),
        ("quantum_systems_unified_v2.csv", "data/qubits/quantum_systems_unified_v2.csv"),
        ("quantum_systems_unified_final.csv", "data/qubits/quantum_systems_unified_final.csv"),
        ("biological_qubits.csv", "data/qubits/biological_qubits.csv"),
        ("atlas_fp_optical_v2_2_curated.csv", "data/processed/atlas_fp_optical_v2_2_curated.csv"),
    ]
    
    datasets = {}
    for name, path in files_to_check:
        p = Path(path)
        if p.exists():
            try:
                df = pd.read_csv(p)
                datasets[name] = df
                print(f"\n{name}: {len(df)} systèmes")
            except Exception as e:
                print(f"\n{name}: ERROR - {e}")
    
    # Vérifier chevauchements
    if 'quantum_systems_unified_v2_3.csv' in datasets and 'quantum_systems_unified_v2.csv' in datasets:
        df_v23 = datasets['quantum_systems_unified_v2_3.csv']
        df_v2 = datasets['quantum_systems_unified_v2.csv']
        
        if 'Systeme' in df_v23.columns and 'Systeme' in df_v2.columns:
            common = set(df_v23['Systeme']) & set(df_v2['Systeme'])
            print(f"\nSystèmes communs v2.3 et v2: {len(common)}")
            print(f"  v2.3 uniquement: {len(df_v23) - len(common)}")
            print(f"  v2 uniquement: {len(df_v2) - len(common)}")
    
    # Vérifier quantum_systems_unified_final
    if 'quantum_systems_unified_final.csv' in datasets:
        df_final = datasets['quantum_systems_unified_final.csv']
        print(f"\nquantum_systems_unified_final.csv: {len(df_final)} systèmes")
        if 'Systeme' in df_final.columns:
            print(f"  Systèmes uniques: {df_final['Systeme'].nunique()}")
            if 'dataset_source' in df_final.columns:
                print(f"\n  Sources:")
                print(df_final['dataset_source'].value_counts())

def main():
    """Fonction principale"""
    print("=" * 80)
    print("CLARIFICATION DATASET 58 vs 117")
    print("=" * 80)
    
    # Analyser tous les fichiers CSV
    results = analyze_csv_files()
    
    print("\n" + "=" * 80)
    print("RÉSUMÉ PAR FICHIER")
    print("=" * 80)
    
    for r in sorted(results, key=lambda x: (x['categorie'], x['fichier'])):
        print(f"\n{r['fichier']}")
        print(f"  Catégorie: {r['categorie']}")
        print(f"  Systèmes: {r['n_systemes']}")
        print(f"  Colonnes: {r['colonnes']}")
        if r['colonnes_liste']:
            print(f"  Colonnes (exemples): {', '.join(r['colonnes_liste'])}...")
    
    # Totaux par catégorie
    qubits_total = sum(r['n_systemes'] for r in results if r['categorie'] == 'qubits' and isinstance(r['n_systemes'], int))
    processed_total = sum(r['n_systemes'] for r in results if r['categorie'] == 'processed' and isinstance(r['n_systemes'], int))
    
    print("\n" + "=" * 80)
    print("TOTAUX PAR CATÉGORIE")
    print("=" * 80)
    print(f"data/qubits: {qubits_total} systèmes (total fichiers)")
    print(f"data/processed: {processed_total} systèmes (total fichiers)")
    print(f"\nTOTAL GLOBAL: {qubits_total + processed_total} systèmes")
    
    # Vérifier déduplication
    check_deduplication()
    
    # Créer document de clarification
    doc_path = Path("docs/DATASET_CLARIFICATION.md")
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write("# Clarification Dataset 58 vs 117\n\n")
        f.write(f"**Généré:** {pd.Timestamp.now()}\n\n")
        f.write("## Résumé\n\n")
        f.write(f"- **58 systèmes**: Dataset `quantum_systems_unified_v2_3.csv` (qubits quantiques)\n")
        f.write(f"- **117 systèmes**: Total dans `quantum_systems_unified_final.csv` (tous systèmes unifiés)\n")
        f.write(f"- **Différence**: 59 systèmes supplémentaires dans `final` (probablement protéines fluorescentes)\n\n")
        f.write("## Fichiers CSV Analysés\n\n")
        f.write("| Fichier | Catégorie | Systèmes | Colonnes |\n")
        f.write("|---------|-----------|----------|----------|\n")
        for r in sorted(results, key=lambda x: x['fichier']):
            f.write(f"| {Path(r['fichier']).name} | {r['categorie']} | {r['n_systemes']} | {r['colonnes']} |\n")
    
    print(f"\n[SAVE] Documentation créée: {doc_path}")

if __name__ == "__main__":
    main()

