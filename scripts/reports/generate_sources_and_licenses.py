#!/usr/bin/env python3
"""
Report Generator: Sources and Licenses
=======================================

Generate table of all data sources and their licenses.

Author: Biological Qubit Atlas Team
License: MIT
"""

import sys
from pathlib import Path
import pandas as pd

def generate_sources_and_licenses():
    """Generate SOURCES_AND_LICENSES.md."""
    # Load data
    data_path = Path("data/processed/atlas_fp_optical_v1_3.csv")
    if not data_path.exists():
        print(f"ERROR: {data_path} not found")
        return 1
    
    df = pd.read_csv(data_path)
    
    # Group by source and license
    source_license_counts = df.groupby(['source', 'license_source']).size().reset_index(name='count')
    source_license_counts = source_license_counts.sort_values(by='count', ascending=False)
    
    # Generate report
    report_lines = [
        "# Sources and Licenses — Atlas v1.3",
        "",
        f"**Total systems**: {len(df)}",
        "",
        "This document provides a complete breakdown of data sources and their licenses.",
        "",
        "## Data Sources Summary",
        "",
        "| Source | License | Count |",
        "|--------|---------|-------|"
    ]
    
    for idx, row in source_license_counts.iterrows():
        source = row['source']
        license_src = row['license_source']
        count = row['count']
        
        report_lines.append(f"| {source} | {license_src} | {count} |")
    
    report_lines.extend([
        "",
        "## License Details",
        "",
        "### FPbase",
        "- **License**: CC BY-SA 4.0",
        "- **Usage**: Pointer-only (no bulk text copying)",
        "- **Attribution**: Required",
        "- **URL**: https://fpbase.org/",
        "",
        "### UniProt",
        "- **License**: CC BY 4.0",
        "- **Usage**: Free to use, redistribute, modify",
        "- **Attribution**: Required",
        "- **URL**: https://www.uniprot.org/",
        "",
        "### PDB / PDBe",
        "- **License**: CC0 (Public Domain)",
        "- **Usage**: No restrictions",
        "- **Attribution**: Not required (but recommended)",
        "- **URL**: https://www.ebi.ac.uk/pdbe/",
        "",
        "### Europe PMC Open Access",
        "- **License**: CC BY / CC0 (article-specific)",
        "- **Usage**: Free to use, redistribute (per article license)",
        "- **Attribution**: Required (cite DOI/PMCID)",
        "- **URL**: https://europepmc.org/",
        "",
        "### Specialist Databases",
        "- **License**: Varies per entry",
        "- **Usage**: Pointer-only (DOI references)",
        "- **Attribution**: Required (cite original DOI)",
        "- **Sources**: GECI DB, voltage sensors, neurotransmitter sensors",
        "",
        "## Compliance",
        "",
        "All data in this Atlas is:",
        "1. **Traceable**: Each entry has `source_refs` with DOI/PMCID",
        "2. **Licensed**: Each entry has `license_source` indicating license type",
        "3. **Reusable**: Only CC-BY, CC0, or CC BY-SA data included",
        "4. **Attributed**: Sources cited in documentation and metadata",
        "",
        "## Citation",
        "",
        "If you use this Atlas, please cite:",
        "- The Atlas itself (see CITATION.cff)",
        "- The original data sources (see `source_refs` column)",
        "",
        "## Contact",
        "",
        "For licensing questions or data removal requests:",
        "- Open an issue on GitHub",
        "- Reference the specific SystemID",
        ""
    ])
    
    # Save report
    output_path = Path("reports/SOURCES_AND_LICENSES.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"OK Sources and licenses report generated: {output_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(generate_sources_and_licenses())

