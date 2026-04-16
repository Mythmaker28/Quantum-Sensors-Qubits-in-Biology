#!/usr/bin/env python3
"""
Création dataset v2.3 avec corrections méthodologiques
- Correction recatégorisation NV bulk (ex_vivo -> bulk)
- Recatégorisation systèmes "unknown"
- Expansion N_bulk si possible
"""

import pandas as pd
import sys
from pathlib import Path

# Encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def load_v2():
    """Charge le dataset v2"""
    v2_path = Path("data/qubits/quantum_systems_unified_v2.csv")
    if not v2_path.exists():
        raise FileNotFoundError(f"Fichier {v2_path} non trouvé")
    
    df = pd.read_csv(v2_path)
    print(f"[LOAD] Dataset v2: {len(df)} systèmes")
    return df

def correct_nv_bulk(df):
    """Corrige la recatégorisation NV bulk: ex_vivo -> bulk"""
    mask = df['Systeme'].str.contains('NV bulk', case=False, na=False)
    n_corrected = mask.sum()
    
    if n_corrected > 0:
        print(f"\n[CORRECT] NV bulk: {n_corrected} système(s) à corriger")
        df.loc[mask, 'Hote_contexte'] = 'bulk'
        print(f"  Changé: 'Interface tissu neural (ex_vivo)' -> 'bulk'")
        print(f"  Système(s): {df.loc[mask, 'Systeme'].tolist()}")
    else:
        print("\n[WARN] Aucun système NV bulk trouvé")
    
    return df

def identify_unknown_systems(df):
    """Identifie les systèmes avec contexte 'unknown' ou non standardisé"""
    # Systèmes avec Hote_contexte non standardisé (pas in_vitro/in_cellulo/in_vivo/ex_vivo/bulk)
    standard_patterns = ['in_vitro', 'in_cellulo', 'in_vivo', 'ex_vivo', 'bulk']
    
    def is_standard(context):
        if pd.isna(context):
            return False
        context_str = str(context).lower()
        return any(pattern in context_str for pattern in standard_patterns)
    
    df['is_standard_context'] = df['Hote_contexte'].apply(is_standard)
    unknown_mask = ~df['is_standard_context']
    
    unknown_systems = df[unknown_mask].copy()
    print(f"\n[ANALYZE] Systèmes avec contexte non standardisé: {len(unknown_systems)}")
    
    return unknown_systems

def recategorize_unknown_systems(df, unknown_df):
    """Recatégorise les systèmes unknown basé sur métadonnées"""
    recategorizations = []
    
    for idx, row in unknown_df.iterrows():
        systeme = row['Systeme']
        contexte_actuel = row['Hote_contexte']
        classe = row['Classe']
        notes = str(row.get('Notes', ''))
        conditions = str(row.get('Conditions', ''))
        taille = str(row.get('Taille_objet_nm', ''))
        
        # Analyse pour déterminer nouveau contexte
        nouveau_contexte = None
        raison = ""
        
        # Règle 1: Systèmes bulk (diamant, SiC, etc.) sans contexte biologique
        if any(x in contexte_actuel.lower() for x in ['diamond', 'silicon', 'carbide', 'fullerene']):
            if 'bulk' in taille.lower() or 'bulk' in systeme.lower():
                nouveau_contexte = 'bulk'
                raison = "Système bulk matériau (diamant/SiC) sans interface biologique"
            elif '77K' in systeme or 'cryo' in conditions.lower():
                nouveau_contexte = 'in_vitro'  # Cryogénique = in vitro
                raison = "Système cryogénique, contexte in vitro"
            else:
                nouveau_contexte = 'bulk'
                raison = "Système matériau bulk par défaut"
        
        # Règle 2: Systèmes hyperpolarisés (classe C)
        elif 'hyperpolarized' in contexte_actuel.lower() or 'hyperpolarisé' in systeme.lower():
            if 'in_vivo' in notes.lower() or 'in_vivo' in conditions.lower():
                nouveau_contexte = 'in_vivo'
                raison = "Métabolite hyperpolarisé utilisé in vivo"
            else:
                nouveau_contexte = 'in_vitro'
                raison = "Métabolite hyperpolarisé, contexte in vitro par défaut"
        
        # Règle 3: Systèmes biologiques (classe D) avec organisme spécifique
        elif classe == 'D':
            if 'in_vivo' in notes.lower() or 'in_vivo' in conditions.lower():
                nouveau_contexte = 'in_vivo'
                raison = "Système biologique in vivo (classe D)"
            elif 'in_cellulo' in notes.lower() or 'cell' in notes.lower():
                nouveau_contexte = 'in_cellulo'
                raison = "Système biologique in cellulo (classe D)"
            else:
                nouveau_contexte = 'in_vitro'
                raison = "Système biologique, contexte in vitro par défaut"
        
        # Règle 4: Systèmes couplés à NV (classe C)
        elif 'coupled to NV' in contexte_actuel.lower() or 'NV center intrinsic' in contexte_actuel.lower():
            nouveau_contexte = 'bulk'
            raison = "Spin nucléaire couplé à NV dans diamant bulk"
        
        # Règle 5: Systèmes bulk explicites (silicon bulk, etc.)
        elif 'bulk' in contexte_actuel.lower() or 'bulk' in systeme.lower():
            nouveau_contexte = 'bulk'
            raison = "Système bulk explicite dans nom/contexte"
        
        # Règle 5b: Systèmes avec "(bulk)" dans le contexte
        elif '(bulk)' in contexte_actuel or 'silicon (bulk)' in contexte_actuel:
            nouveau_contexte = 'bulk'
            raison = "Système bulk explicite (silicon bulk)"
        
        # Règle 6: Systèmes hyperpolarisés - vérifier Notes pour in_vivo
        elif 'hyperpolarized' in contexte_actuel.lower() or 'hyperpolarisé' in systeme.lower():
            notes_lower = notes.lower()
            if 'in vivo' in notes_lower or 'fda' in notes_lower or 'clinical' in notes_lower:
                nouveau_contexte = 'in_vivo'
                raison = "Métabolite hyperpolarisé utilisé in vivo (FDA/clinical)"
            else:
                nouveau_contexte = 'in_vitro'
                raison = "Métabolite hyperpolarisé, contexte in vitro par défaut"
        
        # Règle 7: Par défaut, analyser Notes et Conditions
        else:
            if 'in_vivo' in notes.lower() or 'in_vivo' in conditions.lower():
                nouveau_contexte = 'in_vivo'
                raison = "Déduit de Notes/Conditions: in_vivo"
            elif 'in_cellulo' in notes.lower() or 'cell' in notes.lower():
                nouveau_contexte = 'in_cellulo'
                raison = "Déduit de Notes/Conditions: in_cellulo"
            elif 'ex_vivo' in notes.lower() or 'tissue' in notes.lower():
                nouveau_contexte = 'ex_vivo'
                raison = "Déduit de Notes/Conditions: ex_vivo"
            else:
                nouveau_contexte = 'in_vitro'
                raison = "Par défaut: in_vitro"
        
        if nouveau_contexte:
            recategorizations.append({
                'index': idx,
                'systeme': systeme,
                'ancien': contexte_actuel,
                'nouveau': nouveau_contexte,
                'raison': raison
            })
    
    return recategorizations

def apply_recategorizations(df, recategorizations):
    """Applique les recatégorisations au DataFrame"""
    print(f"\n[RECATEGORIZE] Application de {len(recategorizations)} recatégorisations:")
    
    for recat in recategorizations:
        idx = recat['index']
        df.loc[idx, 'Hote_contexte'] = recat['nouveau']
        print(f"  - {recat['systeme'][:50]}")
        print(f"    {recat['ancien']} -> {recat['nouveau']} ({recat['raison']})")
    
    return df

def save_v2_3(df):
    """Sauvegarde le dataset v2.3"""
    output_path = Path("data/qubits/quantum_systems_unified_v2_3.csv")
    df = df.drop(columns=['is_standard_context'], errors='ignore')
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n[SAVE] Dataset v2.3 sauvegardé: {output_path}")
    print(f"  Total systèmes: {len(df)}")
    return output_path

def create_recategorization_log(recategorizations):
    """Crée le log de recatégorisation"""
    log_path = Path("data/qubits/environment_recategorization_log.csv")
    
    if recategorizations:
        log_df = pd.DataFrame(recategorizations)
        log_df['timestamp'] = pd.Timestamp.now()
        log_df.to_csv(log_path, index=False, encoding='utf-8')
        print(f"\n[LOG] Log de recatégorisation sauvegardé: {log_path}")
    else:
        print("\n[LOG] Aucune recatégorisation à logger")

def main():
    """Fonction principale"""
    print("=" * 80)
    print("CRÉATION DATASET v2.3 - Corrections Méthodologiques")
    print("=" * 80)
    
    # Charger v2
    df = load_v2()
    
    # Correction NV bulk (URGENT)
    df = correct_nv_bulk(df)
    
    # Identifier systèmes unknown
    unknown_df = identify_unknown_systems(df)
    
    # Recatégoriser
    recategorizations = recategorize_unknown_systems(df, unknown_df)
    
    # Appliquer recatégorisations
    df = apply_recategorizations(df, recategorizations)
    
    # Sauvegarder v2.3
    output_path = save_v2_3(df)
    
    # Créer log
    create_recategorization_log(recategorizations)
    
    # Statistiques finales
    print("\n" + "=" * 80)
    print("STATISTIQUES FINALES")
    print("=" * 80)
    print(f"Total systèmes: {len(df)}")
    print(f"\nDistribution Hote_contexte:")
    print(df['Hote_contexte'].value_counts())
    print(f"\nSystèmes bulk: {len(df[df['Hote_contexte'] == 'bulk'])}")
    print(f"Systèmes unknown restants: {len(df[~df['Hote_contexte'].str.contains('in_vitro|in_cellulo|in_vivo|ex_vivo|bulk', case=False, na=False)])}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

