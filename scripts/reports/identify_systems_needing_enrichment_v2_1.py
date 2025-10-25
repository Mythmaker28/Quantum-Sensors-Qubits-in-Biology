#!/usr/bin/env python3
"""
Identification des systèmes v2.0 nécessitant un enrichissement
pour atteindre l'objectif v2.1 de 120 systèmes utiles mesurés
"""

import pandas as pd
import json
from pathlib import Path

def analyze_gaps():
    """Identifie les gaps dans le dataset v2.0"""
    
    csv_path = Path("data/processed/atlas_fp_optical_v2_0.csv")
    df = pd.read_csv(csv_path)
    
    print("=" * 80)
    print("ANALYSE DES GAPS - Atlas v2.0 -> v2.1")
    print("=" * 80)
    
    # Systèmes sans contrast_value
    no_contrast = df[df['contrast_value'].isna()]
    print(f"\n## SYSTEMES SANS CONTRAST_VALUE : {len(no_contrast)}")
    print("\nListe des systèmes prioritaires à enrichir :")
    for idx, row in no_contrast.iterrows():
        name = row['protein_name']
        family = str(row['family']) if pd.notna(row['family']) else 'N/A'
        doi = str(row.get('doi', 'N/A')) if pd.notna(row.get('doi')) else 'N/A'
        print(f"  - {name:25s} (Famille: {family:15s}) DOI: {doi}")
    
    # Familles sous-représentées
    print("\n## FAMILLES SOUS-REPRESENTEES (<5 systèmes mesurés)")
    measured = df[df['contrast_value'].notna()]
    family_counts = measured['family'].value_counts()
    under_5 = family_counts[family_counts < 5]
    
    for family, count in under_5.items():
        print(f"  - {family:20s}: {count} systèmes")
    
    # Systèmes avec metadata incomplète
    print("\n## SYSTEMES AVEC METADATA INCOMPLETE")
    
    # Vérifier quelles colonnes optiques existent
    has_ex = 'excitation_nm' in df.columns
    has_em = 'emission_nm' in df.columns
    
    if not has_ex and not has_em:
        print("  Note: Les colonnes excitation_nm/emission_nm n'existent pas encore dans v2.0")
        print("  -> Ces champs seront ajoutés lors de la création du schéma v2.1")
    else:
        if has_ex:
            no_ex = df[df['excitation_nm'].isna()]
            print(f"  Sans excitation_nm: {len(no_ex)} systèmes")
        if has_em:
            no_em = df[df['emission_nm'].isna()]
            print(f"  Sans emission_nm: {len(no_em)} systèmes")
    
    # Suggestions de systèmes à ajouter
    print("\n## SUGGESTIONS DE NOUVEAUX SYSTEMES (depuis priority_fp_list.csv)")
    
    priority_path = Path("data/priority_fp_list.csv")
    if priority_path.exists():
        priority = pd.read_csv(priority_path)
        
        # Comparer avec v2.0
        existing_names = set(df['protein_name'].str.lower().str.strip())
        
        missing = []
        for idx, row in priority.iterrows():
            pname = row['name'].lower().strip()
            if pname not in existing_names:
                missing.append(row)
        
        print(f"\n  Systèmes prioritaires ABSENTS de v2.0: {len(missing)}")
        if missing:
            for sys in missing[:15]:  # Top 15
                print(f"    - {sys['name']:25s} (Famille: {sys['family']:15s}, Priorité: {sys['priority']})")
        
        if len(missing) > 15:
            print(f"    ... et {len(missing) - 15} autres")
    
    # Plan d'action
    print("\n" + "=" * 80)
    print("PLAN D'ACTION POUR v2.1")
    print("=" * 80)
    
    target = 120
    current = len(measured)
    gap = target - current
    
    print(f"\n  Systèmes utiles actuels: {current}")
    print(f"  Objectif v2.1: {target}")
    print(f"  Gap: +{gap} systèmes requis")
    
    print("\n  STRATEGIE RECOMMANDEE:")
    print(f"  1. Enrichir systèmes existants sans contrast: {len(no_contrast)} candidats")
    print(f"     -> Si on enrichit TOUS: {current + len(no_contrast)} total ({current + len(no_contrast) - target:+d} vs objectif)")
    
    if len(missing) > 0:
        print(f"  2. Ajouter systèmes prioritaires manquants: {min(len(missing), 10)} systèmes")
        print(f"     -> Total projeté: {current + len(no_contrast) + min(len(missing), 10)} systèmes")
    
    print("\n  FAISABILITE:")
    if len(no_contrast) >= gap:
        print("  -> OK POSSIBLE en enrichissant uniquement systemes existants")
    elif len(no_contrast) + len(missing) >= gap:
        print("  -> OK POSSIBLE en enrichissant existants + ajoutant prioritaires")
    else:
        print("  -> DIFFICILE, mining litterature intensif requis")
    
    # Sauvegarder la liste
    output = {
        "date_analysis": pd.Timestamp.now().isoformat(),
        "current_useful": int(current),
        "target": target,
        "gap": int(gap),
        "systems_no_contrast": len(no_contrast),
        "priority_missing": len(missing) if priority_path.exists() else 0,
        "systems_to_enrich": no_contrast['protein_name'].tolist(),
        "priority_to_add": [s['name'] for s in missing[:10]] if missing else []
    }
    
    output_path = Path("reports/ENRICHMENT_PLAN_v2_1.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n  Plan sauvegardé: {output_path}")
    
    return output

if __name__ == "__main__":
    analyze_gaps()

