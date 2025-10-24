#!/usr/bin/env python3
"""
Système automatisé de validation in vivo avec scoring
Licence: MIT
"""

import pandas as pd
import re
import os
from typing import Dict
from datetime import datetime

class InVivoValidator:
    """Validateur automatique contexte in vivo"""
    
    ORGANISM_PATTERNS = {
        'mouse': r'(mouse|mice|mus\s+musculus)',
        'rat': r'(rat|rattus\s+norvegicus)',
        'zebrafish': r'(zebrafish|danio\s+rerio)',
        'c.elegans': r'(c\.\s*elegans|caenorhabditis)',
        'drosophila': r'(drosophila|fruit\s+fly)',
        'human': r'(human|homo\s+sapiens|patient)',
    }
    
    def __init__(self, atlas_csv: str):
        self.df = pd.read_csv(atlas_csv)
        
    def score_in_vivo(self, row: pd.Series) -> Dict:
        """
        Score robustesse validation in vivo (0-100)
        
        Critères:
        - Organisme modèle standard: +30
        - Tissus multiples: +20
        - Méthode quantitative: +20
        - Reproductibilité (citations): +20
        - DOI multiple: +10
        """
        score = 0
        details = []
        
        context = str(row.get('context', '')).lower()
        notes = str(row.get('notes', '')).lower()
        doi = str(row.get('doi', ''))
        
        # Critère 1: Détection organisme
        organism_found = None
        for org, pattern in self.ORGANISM_PATTERNS.items():
            if re.search(pattern, context + ' ' + notes, re.IGNORECASE):
                organism_found = org
                score += 30
                details.append(f"Organisme: {org}")
                break
        
        # Critère 2: Context in vivo explicite
        if 'in_vivo' in context or 'in vivo' in notes:
            score += 20
            details.append("Context: in_vivo explicit")
        
        # Critère 3: Méthode quantitative
        method = str(row.get('method', '')).lower()
        if any(m in method for m in ['odmr', 'nmr', 'imaging', 'mri']):
            score += 20
            details.append(f"Method: {method}")
        
        # Critère 4: Publication majeure
        if doi and any(j in doi.lower() for j in ['nature', 'science', 'cell']):
            score += 20
            details.append("Journal: high-impact")
        
        # Critère 5: Contraste mesuré
        if pd.notna(row.get('contrast_value')):
            score += 10
            details.append("Measured contrast")
        
        return {
            'score': score,
            'organism': organism_found,
            'details': '; '.join(details),
            'validated': score >= 50
        }
    
    def generate_report(self, output_md: str = "reports/IN_VIVO_VALIDATION.md"):
        """Génère rapport validation in vivo"""
        
        results = []
        for idx, row in self.df.iterrows():
            validation = self.score_in_vivo(row)
            results.append({
                'SystemID': row.get('SystemID', idx),
                'protein_name': row.get('protein_name', 'Unknown'),
                'score': validation['score'],
                'organism': validation['organism'] or 'N/A',
                'validated': validation['validated'],
                'details': validation['details']
            })
        
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('score', ascending=False)
        
        # Export CSV
        os.makedirs(os.path.dirname(output_md), exist_ok=True)
        results_df.to_csv(output_md.replace('.md', '.csv'), index=False)
        
        # Rapport Markdown
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write("# 🔬 Rapport de Validation In Vivo\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            total = len(results_df)
            validated = results_df['validated'].sum()
            organisms = results_df['organism'].value_counts()
            
            f.write("## 📊 Statistiques Globales\n\n")
            f.write(f"- **Total systèmes**: {total}\n")
            f.write(f"- **Validés in vivo**: {validated} ({validated/total*100:.1f}%)\n")
            f.write(f"- **Organismes uniques**: {organisms.count()}\n\n")
            
            f.write("### Répartition Organismes\n\n")
            f.write("| Organisme | Nombre |\n")
            f.write("|-----------|--------|\n")
            for org, count in organisms.items():
                if org != 'N/A':
                    f.write(f"| {org.capitalize()} | {count} |\n")
            
            f.write("\n## 🏆 Top 10 Systèmes In Vivo (Score > 70)\n\n")
            f.write("| Système | Score | Organisme | Détails |\n")
            f.write("|---------|-------|-----------|---------|\\n")
            
            top10 = results_df.head(10)
            for _, row in top10.iterrows():
                if row['score'] >= 70:
                    f.write(f"| {row['protein_name']} | {row['score']} | {row['organism']} | {row['details']} |\n")
            
            low_score = results_df[results_df['score'] < 50]
            f.write(f"\n## ⚠️ Systèmes Nécessitant Validation ({len(low_score)})\n\n")
            f.write("| Système | Score | Raison |\n")
            f.write("|---------|-------|--------|\n")
            for _, row in low_score.head(20).iterrows():
                f.write(f"| {row['protein_name']} | {row['score']} | Manque données in vivo |\n")
        
        print(f"[OK] Rapport genere: {output_md}")
        print(f"   - Valides: {validated}/{total} ({validated/total*100:.1f}%)")

if __name__ == "__main__":
    validator = InVivoValidator("data/processed/atlas_fp_optical_v1_3.csv")
    validator.generate_report()


