#!/usr/bin/env python3
"""
Orchestration Script: Atlas v1.3 Pipeline
==========================================

Execute full pipeline:
1. Harvest (FPbase + Specialist + PMC)
2. Reconcile & Deduplicate
3. Build Tables
4. QA Audit

Author: Biological Qubit Atlas Team
License: MIT
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_path: str, description: str) -> int:
    """Run a Python script and return exit code."""
    print("\n" + "=" * 70)
    print(f"{description}")
    print("=" * 70)
    
    result = subprocess.run([sys.executable, script_path])
    
    if result.returncode != 0:
        print(f"\nERROR: {script_path} failed with code {result.returncode}")
        return result.returncode
    
    print(f"\nOK {script_path} completed successfully")
    return 0

def main():
    """Main orchestrator."""
    print("=" * 70)
    print("Atlas v1.3 FP Optical Expansion-200 Pipeline")
    print("=" * 70)
    
    pipeline = [
        ("scripts/etl/fetch_fpbase_graphql.py", "Step 1/7: Harvest FPbase GraphQL"),
        ("scripts/etl/fetch_specialist.py", "Step 2/7: Harvest Specialist DBs"),
        ("scripts/textmine/mine_pmc_fulltext.py", "Step 3/7: Mine PMC Full-Text"),
        ("scripts/textmine/fetch_supplements.py", "Step 4/7: Fetch Supplements"),
        ("scripts/textmine/parse_supp_spreadsheets.py", "Step 5/7: Parse Spreadsheets"),
        ("scripts/etl/build_external_candidates_v1_3.py", "Step 6/7: Reconcile & Deduplicate"),
        ("scripts/etl/build_atlas_tables_v1_3.py", "Step 7/7: Build Final Tables"),
    ]
    
    for script_path, description in pipeline:
        if not Path(script_path).exists():
            print(f"\nERROR: Script not found: {script_path}")
            return 1
        
        exit_code = run_script(script_path, description)
        if exit_code != 0:
            print(f"\nPipeline FAILED at: {description}")
            return exit_code
    
    # Run QA audit
    print("\n" + "=" * 70)
    print("QA Audit")
    print("=" * 70)
    
    qa_exit_code = run_script("scripts/qa/audit_fp_optical_v1_3.py", "QA: Audit FP Optical v1.3")
    
    if qa_exit_code == 0:
        print("\n" + "=" * 70)
        print("✓ PIPELINE SUCCESS - All checks passed!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Review reports/AUDIT_v1.3_fp_optical.md")
        print("  2. Generate EVIDENCE_SAMPLES and SOURCES_AND_LICENSES reports")
        print("  3. Prepare release v1.3.0")
    else:
        print("\n" + "=" * 70)
        print("✗ PIPELINE COMPLETED WITH WARNINGS")
        print("=" * 70)
        print("\nQA audit failed. Review reports/AUDIT_v1.3_fp_optical.md for details.")
        print("Consider:")
        print("  - Adding more sources to meet thresholds")
        print("  - Releasing as v1.3.0-pre with action plan")
    
    return qa_exit_code

if __name__ == "__main__":
    sys.exit(main())

