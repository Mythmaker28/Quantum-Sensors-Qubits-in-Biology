#!/usr/bin/env python3
"""
Nettoie fichiers obsolètes pour v2.0
Garde seulement docs nécessaires, supprime rapports intermédiaires anciens
Licence: Apache-2.0
"""

import os
from pathlib import Path

# Fichiers obsolètes à supprimer (rapports sessions anciennes, doublons)
OBSOLETE_FILES = [
    # Rapports sessions v1.2.x (obsolètes, info dans CHANGELOG)
    "BILAN_COMPLET_v1.2.1.md",
    "BILAN_FINAL_v1.2.0.txt",
    "CLOTURE_SESSION_v1.2.1.md",
    "SESSION_COMPLETE_RESUME.md",
    "HANDOFF_v1.2.1_FINAL.md",
    
    # Rapports release anciens (consolidés dans CHANGELOG_v2.0.md)
    "RAPPORT_FINAL_RELEASE.md",
    "RAPPORT_FINAL_v1.2.1.md",
    "RELEASE_v1.2.0_INSTRUCTIONS.md",
    "RELEASE_v1.2.0_RAPPORT_FINAL.md",
    "FINAL_DELIVERY_REPORT_v1.2.0.md",
    
    # Summaries intermédiaires (info dans PRD/CHANGELOG)
    "EXECUTION_SUMMARY_v1.2.0.md",
    "EXECUTION_SUMMARY_v1.3_BLOCKED.md",
    "EXECUTION_SUMMARY_v1.3_HYBRID.md",
    "v1.2_SUMMARY.md",
    
    # Extensions/découvertes (info dans RESEARCH_BACKLOG conservé)
    "DECOUVERTE_INTRIGANTE.md",
    "EXTENSION_COINS_INSOUPCONNES.md",
    "PARADOXE_TYROSYL_ANALYSE.md",
    
    # Feedback ancien (consolidé dans issues GitHub)
    "FEEDBACK_RESPONSE.md",
    
    # Warnings (info dans QC_REPORT actuel)
    "WARNINGS_EXPLANATION.md",
    
    # Print outputs anciens
    "PRINT_FINAL_CREDIBILITY.txt",
    "PRINT_FINAL_v1.3_beta.txt",
]

# Fichiers à GARDER (essentiels v2.0)
KEEP_FILES = [
    "README.md",
    "LICENSE",
    "LICENSE.CODE",
    "CONTRIBUTING.md",
    "CITATION.cff",
    "PRD_v2.0.md",
    "CHANGELOG_v2.0.md",
    "QC_REPORT.md",
    "RESEARCH_BACKLOG.md",  # Utile pour roadmap future
    "METHODOLOGY.md",
    "KNOWN_ISSUES.md",
]

def cleanup_obsolete():
    """Supprime fichiers obsolètes"""
    
    removed = []
    kept = []
    
    for file in OBSOLETE_FILES:
        if os.path.exists(file):
            print(f"[REMOVE] {file}")
            os.remove(file)
            removed.append(file)
        else:
            print(f"[SKIP] {file} (deja supprime)")
    
    print(f"\n[OK] {len(removed)} fichiers obsoletes supprimes")
    
    return removed

if __name__ == "__main__":
    removed = cleanup_obsolete()
    
    print("\nFichiers supprimes:")
    for f in removed:
        print(f"  - {f}")

