#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Family Coverage Check
=====================
Vérifie qu'au moins 6 familles ont ≥3 systèmes mesurés.
Évite la sur-concentration sur une seule famille (e.g., full-calcium).
"""

import sys
from pathlib import Path
import pandas as pd

ATLAS_FILE = Path("data/processed/atlas_fp_optical.csv")
MIN_FAMILIES = 6
MIN_PER_FAMILY = 3

def check_family_coverage():
    """Vérifie la couverture par famille."""
    if not ATLAS_FILE.exists():
        print(f"ERROR: {ATLAS_FILE} not found!")
        sys.exit(1)
    
    df = pd.read_csv(ATLAS_FILE)
    measured = df[df['contrast_source'] == 'measured']
    
    print("=" * 70)
    print("Family Coverage Analysis")
    print("=" * 70)
    
    coverage = measured.groupby('family').size().sort_values(ascending=False)
    
    print("\nCoverage par famille:")
    print(coverage.to_string())
    
    # Check threshold
    families_ok = (coverage >= MIN_PER_FAMILY).sum()
    
    print(f"\nFamilles avec >={MIN_PER_FAMILY} mesures: {families_ok}")
    
    if families_ok < MIN_FAMILIES:
        print(f"\nERROR FAIL: Only {families_ok} families (need {MIN_FAMILIES})")
        
        # List missing families
        print("\nPriority families needing more measurements:")
        under_threshold = coverage[coverage < MIN_PER_FAMILY]
        for family, count in under_threshold.items():
            needed = MIN_PER_FAMILY - count
            print(f"  {family}: {count} measured, need {needed} more")
        
        return False
    else:
        print(f"\nOK PASS: {families_ok} families with >={MIN_PER_FAMILY} measurements")
        
        # List top families
        print("\nTop families (>=3 measurements):")
        top = coverage[coverage >= MIN_PER_FAMILY]
        for family, count in top.items():
            print(f"  {family}: {count} measurements")
        
        return True

def main():
    """Point d'entrée."""
    passed = check_family_coverage()
    
    if not passed:
        sys.exit(1)
    else:
        print("\nOK Family coverage check passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()

