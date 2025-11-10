#!/usr/bin/env python3
"""
Version Consistency Checker

Verifies that all version references are coherent across:
- CITATION.cff (latest stable)
- README.md (badges and citations)
- zenodo.json (Zenodo metadata)
- Git tags
- CITATION_v1.2.1.cff (frozen Frontiers version)

Exit code: 0 if consistent, 1 if inconsistencies found.
"""

import json
import re
import sys
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent
EXPECTED_LATEST = "2.2.2"
EXPECTED_FRONTIERS = "1.2.1"
EXPECTED_SYSTEMS_LATEST = 250
EXPECTED_SYSTEMS_FRONTIERS = 66

errors = []
warnings = []


def check_citation_cff():
    """Check CITATION.cff points to latest stable"""
    citation_path = REPO_ROOT / "CITATION.cff"
    if not citation_path.exists():
        errors.append("CITATION.cff not found")
        return
    
    content = citation_path.read_text()
    
    # Extract version
    version_match = re.search(r'version:\s*"([^"]+)"', content)
    if version_match:
        version = version_match.group(1)
        if version != EXPECTED_LATEST:
            errors.append(f"CITATION.cff version mismatch: {version} != {EXPECTED_LATEST}")
    else:
        errors.append("CITATION.cff version field not found")
    
    # Check message references Frontiers citation
    if "CITATION_v1.2.1.cff" not in content:
        warnings.append("CITATION.cff should mention CITATION_v1.2.1.cff in message")


def check_citation_v1_2_1_cff():
    """Check frozen Frontiers citation exists"""
    citation_path = REPO_ROOT / "CITATION_v1.2.1.cff"
    if not citation_path.exists():
        errors.append("CITATION_v1.2.1.cff not found (required for Frontiers)")
        return
    
    content = citation_path.read_text(encoding='utf-8')
    
    # Should be locked at v1.2.1
    if 'version: "1.2.1"' not in content:
        errors.append("CITATION_v1.2.1.cff must be locked at version 1.2.1")
    
    # Should reference Frontiers
    if "Frontiers" not in content:
        warnings.append("CITATION_v1.2.1.cff should explicitly mention Frontiers")
    
    # Should be frozen
    if "frozen" not in content.lower():
        warnings.append("CITATION_v1.2.1.cff should indicate it's frozen")


def check_readme():
    """Check README.md badges and citations"""
    readme_path = REPO_ROOT / "README.md"
    if not readme_path.exists():
        errors.append("README.md not found")
        return
    
    content = readme_path.read_text(encoding='utf-8')
    
    # Check version badge
    if f'version-v{EXPECTED_LATEST}' not in content:
        errors.append(f"README.md missing version badge for v{EXPECTED_LATEST}")
    
    # Check systems count badges
    if f'systems-{EXPECTED_SYSTEMS_LATEST}' not in content:
        warnings.append(f"README.md missing systems badge for {EXPECTED_SYSTEMS_LATEST}")
    
    if f'systems-{EXPECTED_SYSTEMS_FRONTIERS}' not in content:
        warnings.append(f"README.md missing systems badge for {EXPECTED_SYSTEMS_FRONTIERS}")
    
    # Check dual citation section
    if "Frontiers manuscript" not in content:
        errors.append("README.md missing Frontiers citation section")
    
    if "Latest stable for development" not in content:
        errors.append("README.md missing latest stable citation section")
    
    # Check link to VERSIONING_ROADMAP
    if "VERSIONING_ROADMAP.md" not in content:
        warnings.append("README.md should link to VERSIONING_ROADMAP.md")


def check_zenodo_json():
    """Check zenodo.json metadata"""
    zenodo_path = REPO_ROOT / "zenodo.json"
    if not zenodo_path.exists():
        errors.append("zenodo.json not found")
        return
    
    try:
        data = json.loads(zenodo_path.read_text(encoding='utf-8'))
        
        # Check version
        version = data.get("version", "")
        if version != EXPECTED_LATEST:
            errors.append(f"zenodo.json version mismatch: {version} != {EXPECTED_LATEST}")
        
        # Check title contains version
        title = data.get("title", "")
        if EXPECTED_LATEST not in title:
            warnings.append(f"zenodo.json title should mention version {EXPECTED_LATEST}")
        
        # Check related_identifiers has isVersionOf
        related = data.get("related_identifiers", [])
        has_version_of = any(
            r.get("relation") == "isVersionOf" for r in related
        )
        if not has_version_of:
            warnings.append("zenodo.json should have 'isVersionOf' relation to v1.2.1")
        
    except json.JSONDecodeError as e:
        errors.append(f"zenodo.json parse error: {e}")


def check_versioning_roadmap():
    """Check VERSIONING_ROADMAP.md exists"""
    roadmap_path = REPO_ROOT / "VERSIONING_ROADMAP.md"
    if not roadmap_path.exists():
        errors.append("VERSIONING_ROADMAP.md not found")
        return
    
    content = roadmap_path.read_text(encoding='utf-8')
    
    # Should document both versions
    if EXPECTED_LATEST not in content:
        errors.append(f"VERSIONING_ROADMAP.md missing v{EXPECTED_LATEST}")
    
    if EXPECTED_FRONTIERS not in content:
        errors.append(f"VERSIONING_ROADMAP.md missing v{EXPECTED_FRONTIERS}")
    
    # Should explain dual versioning
    if "dual versioning" not in content.lower():
        warnings.append("VERSIONING_ROADMAP.md should explain dual versioning policy")


def main():
    """Run all consistency checks"""
    print("Checking version consistency...\n")
    
    check_citation_cff()
    check_citation_v1_2_1_cff()
    check_readme()
    check_zenodo_json()
    check_versioning_roadmap()
    
    # Report results
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"   - {warning}")
        print()
    
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"   - {error}")
        print()
    
    if not errors and not warnings:
        print("All version consistency checks passed!\n")
        print(f"Latest stable: v{EXPECTED_LATEST} ({EXPECTED_SYSTEMS_LATEST} systems)")
        print(f"Frontiers frozen: v{EXPECTED_FRONTIERS} ({EXPECTED_SYSTEMS_FRONTIERS} systems)")
        return 0
    else:
        if errors:
            print(f"Found {len(errors)} error(s) and {len(warnings)} warning(s)")
            return 1
        else:
            print(f"Found {len(warnings)} warning(s) (no errors)")
            return 0


if __name__ == "__main__":
    sys.exit(main())
