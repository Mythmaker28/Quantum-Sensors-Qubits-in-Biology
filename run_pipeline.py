#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Pipeline Runner — Atlas v1.2.0 FP Optical
=================================================
Exécute l'ensemble du pipeline ETL et QA pour l'Atlas FP Optical.

Usage:
    python run_pipeline.py --full          # Pipeline complet
    python run_pipeline.py --harvest       # Harvest uniquement
    python run_pipeline.py --build         # Build candidats uniquement
    python run_pipeline.py --qa            # QA uniquement
    python run_pipeline.py --quick         # Quick test (sample data)
"""

import sys
import subprocess
from pathlib import Path
import argparse
from datetime import datetime

# Scripts ETL
HARVEST_SCRIPTS = [
    "scripts/etl/fetch_fpbase_candidates.py",
    "scripts/etl/fetch_uniprot_bulk.py",
    "scripts/etl/fetch_pdb_pdbe_bulk.py",
]

BUILD_SCRIPTS = [
    "scripts/etl/build_external_candidates.py",
    "scripts/etl/classify_modality.py",
]

CONTRAST_SCRIPTS = [
    "scripts/etl/fetch_pmc_contrast.py",
    "scripts/etl/compute_proxies.py",
]

TABLE_SCRIPTS = [
    "scripts/etl/build_atlas_tables_v1_2.py",
]

QA_SCRIPTS = [
    "scripts/qa/audit_fp_optical_v1_2.py",
]

def run_script(script_path: str) -> int:
    """Exécute un script Python."""
    print("\n" + "=" * 70)
    print(f"Running: {script_path}")
    print("=" * 70)
    
    result = subprocess.run([sys.executable, script_path])
    
    if result.returncode != 0:
        print(f"\nERROR: {script_path} failed with code {result.returncode}", file=sys.stderr)
        return result.returncode
    
    print(f"\nOK {script_path} completed successfully")
    return 0

def run_stage(stage_name: str, scripts: list) -> int:
    """Exécute un stage du pipeline."""
    print("\n" + "#" * 70)
    print(f"# STAGE: {stage_name}")
    print("#" * 70)
    
    for script in scripts:
        ret = run_script(script)
        if ret != 0:
            print(f"\nERROR STAGE '{stage_name}' FAILED", file=sys.stderr)
            return ret
    
    print(f"\nOK STAGE '{stage_name}' COMPLETED")
    return 0

def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Atlas v1.2.0 FP Optical Pipeline Runner")
    parser.add_argument("--full", action="store_true", help="Run full pipeline")
    parser.add_argument("--harvest", action="store_true", help="Run harvest stage only")
    parser.add_argument("--build", action="store_true", help="Run build stage only")
    parser.add_argument("--contrast", action="store_true", help="Run contrast extraction only")
    parser.add_argument("--tables", action="store_true", help="Run table build only")
    parser.add_argument("--qa", action="store_true", help="Run QA audit only")
    parser.add_argument("--quick", action="store_true", help="Quick test mode (sample data)")
    
    args = parser.parse_args()
    
    start_time = datetime.now()
    
    print("=" * 70)
    print("Atlas v1.2.0 FP Optical — Pipeline Runner")
    print("=" * 70)
    print(f"Start time: {start_time.isoformat()}")
    print()
    
    # Determine what to run
    run_all = args.full or not any([args.harvest, args.build, args.contrast, args.tables, args.qa])
    
    ret = 0
    
    # Harvest
    if run_all or args.harvest:
        ret = run_stage("HARVEST", HARVEST_SCRIPTS)
        if ret != 0 and not args.full:
            sys.exit(ret)
    
    # Build
    if run_all or args.build:
        ret = run_stage("BUILD CANDIDATES", BUILD_SCRIPTS)
        if ret != 0 and not args.full:
            sys.exit(ret)
    
    # Contrast
    if run_all or args.contrast:
        ret = run_stage("CONTRAST EXTRACTION", CONTRAST_SCRIPTS)
        if ret != 0 and not args.full:
            sys.exit(ret)
    
    # Tables
    if run_all or args.tables:
        ret = run_stage("BUILD TABLES", TABLE_SCRIPTS)
        if ret != 0 and not args.full:
            sys.exit(ret)
    
    # QA
    if run_all or args.qa:
        ret = run_stage("QA AUDIT", QA_SCRIPTS)
        # Don't exit on QA failure, just report
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)
    print(f"Start time:  {start_time.isoformat()}")
    print(f"End time:    {end_time.isoformat()}")
    print(f"Duration:    {duration}")
    
    if ret == 0:
        print("\nOK PIPELINE COMPLETED SUCCESSFULLY!")
    else:
        print(f"\nERROR PIPELINE FAILED (exit code {ret})", file=sys.stderr)
    
    print("=" * 70)
    
    sys.exit(ret)

if __name__ == "__main__":
    main()

