#!/usr/bin/env python3
"""
Tests des validateurs de données
Lance les commandes de la section "Local Usage & Validation" du README
(scripts/validate_atlas.py sur chaque tier) et scripts/qa/validate_non_optical.py
Licence: MIT
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_script(script, *args):
    """Lance un script du dépôt avec l'interpréteur courant"""
    # Sortie en UTF-8 même si la console ne l'est pas (Windows)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / script), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


@pytest.mark.parametrize("tier", ["curated", "mixed", "candidates", "unknown"])
def test_validate_atlas(tier):
    """Aucune erreur critique dans le tier (les avertissements sont tolérés)"""
    result = run_script("scripts/validate_atlas.py", tier)
    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_non_optical():
    """Aucune erreur dans les jeux de données non optiques"""
    result = run_script("scripts/qa/validate_non_optical.py")
    assert result.returncode == 0, result.stdout + result.stderr
