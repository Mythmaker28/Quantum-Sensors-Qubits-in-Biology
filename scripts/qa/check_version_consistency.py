#!/usr/bin/env python3
"""Version Consistency Checker.

Verifies that all version references are coherent across:
- CITATION.cff (latest stable)
- README.md (badges and citations)
- zenodo.json (Zenodo metadata)
- VERSIONING_ROADMAP.md

Exit code: 0 if consistent, 1 if inconsistencies found.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXPECTED_LATEST = "4.0.0"
EXPECTED_FRONTIERS = "1.2.1"
EXPECTED_QUBITS = 82
EXPECTED_FP_BIOSENSORS = 195

errors: list[str] = []
warnings: list[str] = []


def check_citation_cff() -> None:
    path = REPO_ROOT / "CITATION.cff"
    if not path.exists():
        errors.append("CITATION.cff not found")
        return

    content = path.read_text(encoding="utf-8")
    match = re.search(r'^version:\s*"([^"]+)"', content, re.MULTILINE)
    if match:
        version = match.group(1)
        if version != EXPECTED_LATEST:
            errors.append(f"CITATION.cff version mismatch: {version} != {EXPECTED_LATEST}")
    else:
        errors.append("CITATION.cff version field not found")

    if EXPECTED_FRONTIERS not in content:
        warnings.append(
            f"CITATION.cff should reference the frozen Frontiers version "
            f"v{EXPECTED_FRONTIERS} in its references section"
        )


def check_readme() -> None:
    path = REPO_ROOT / "README.md"
    if not path.exists():
        errors.append("README.md not found")
        return

    content = path.read_text(encoding="utf-8")

    if f"version-v{EXPECTED_LATEST}" not in content:
        errors.append(f"README.md missing version badge for v{EXPECTED_LATEST}")

    if "Frontiers" not in content:
        warnings.append("README.md should mention the Frontiers frozen release")

    if "VERSIONING_ROADMAP.md" not in content:
        warnings.append("README.md should link to VERSIONING_ROADMAP.md")


def check_zenodo_json() -> None:
    path = REPO_ROOT / "zenodo.json"
    if not path.exists():
        errors.append("zenodo.json not found")
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"zenodo.json parse error: {exc}")
        return

    version = data.get("version", "")
    if version != EXPECTED_LATEST:
        errors.append(f"zenodo.json version mismatch: {version} != {EXPECTED_LATEST}")

    title = data.get("title", "")
    if EXPECTED_LATEST not in title:
        warnings.append(f"zenodo.json title should mention version {EXPECTED_LATEST}")

    related = data.get("related_identifiers", [])
    has_version_of = any(r.get("relation") == "isVersionOf" for r in related)
    if not has_version_of:
        warnings.append("zenodo.json should have 'isVersionOf' relation to the concept DOI")


def check_versioning_roadmap() -> None:
    path = REPO_ROOT / "VERSIONING_ROADMAP.md"
    if not path.exists():
        errors.append("VERSIONING_ROADMAP.md not found")
        return

    content = path.read_text(encoding="utf-8")

    if EXPECTED_LATEST not in content:
        errors.append(f"VERSIONING_ROADMAP.md missing v{EXPECTED_LATEST}")

    if EXPECTED_FRONTIERS not in content:
        errors.append(f"VERSIONING_ROADMAP.md missing v{EXPECTED_FRONTIERS}")


def main() -> int:
    print("Checking version consistency...\n")

    check_citation_cff()
    check_readme()
    check_zenodo_json()
    check_versioning_roadmap()

    if warnings:
        print("WARNINGS:")
        for msg in warnings:
            print(f"   - {msg}")
        print()

    if errors:
        print("ERRORS:")
        for msg in errors:
            print(f"   - {msg}")
        print()

    if not errors and not warnings:
        print("All version consistency checks passed!\n")
        print(f"Latest stable: v{EXPECTED_LATEST}")
        print(f"Frontiers frozen: v{EXPECTED_FRONTIERS}")
        return 0
    if errors:
        print(f"Found {len(errors)} error(s) and {len(warnings)} warning(s)")
        return 1
    print(f"Found {len(warnings)} warning(s) (no errors)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
