#!/usr/bin/env python3
"""
Report Generator: Evidence Samples v1.3
========================================

Generate table of measured contrasts with evidence samples (≥30 lines).

Columns:
- SystemID
- Protein Name
- Family
- Contrast Value (normalized)
- Evidence Type
- Context Snippet
- DOI/PMCID
- Quality Tier

Author: Biological Qubit Atlas Team
License: MIT
"""

import sys
from pathlib import Path
import pandas as pd

def generate_evidence_samples():
    """Generate EVIDENCE_SAMPLES_v1.3.md."""
    # Load data
    data_path = Path("data/processed/atlas_fp_optical_v1_3.csv")
    if not data_path.exists():
        print(f"ERROR: {data_path} not found")
        return 1
    
    df = pd.read_csv(data_path)
    
    # Filter measured only
    measured_df = df[df['contrast_value'].notna()].copy()
    
    # Sort by quality tier and family
    measured_df = measured_df.sort_values(by=['contrast_quality_tier', 'family', 'protein_name'])
    
    # Generate report
    report_lines = [
        "# Evidence Samples — Atlas v1.3",
        "",
        f"**Total measured systems**: {len(measured_df)}",
        "",
        "This table shows measured contrast values with their evidence sources.",
        "",
        "| SystemID | Protein | Family | Contrast (fold) | Tier | Evidence | Context | DOI/PMCID |",
        "|----------|---------|--------|----------------|------|----------|---------|-----------|"
    ]
    
    for idx, row in measured_df.head(min(len(measured_df), 50)).iterrows():
        system_id = row.get('SystemID', 'N/A')
        protein = row.get('protein_name', 'N/A')
        family = row.get('family', 'N/A')
        contrast = f"{row.get('contrast_normalized', row.get('contrast_value', 'N/A')):.2f}" if pd.notna(row.get('contrast_normalized')) else 'N/A'
        tier = row.get('contrast_quality_tier', 'N/A')
        evidence = row.get('evidence_type', 'N/A')
        
        # Truncate context
        context = str(row.get('condition_text', ''))[:50]
        if len(str(row.get('condition_text', ''))) > 50:
            context += '...'
        if not context:
            context = 'N/A'
        
        # Extract first DOI/PMCID
        refs = str(row.get('source_refs', 'N/A'))
        ref_short = refs.split(';')[0][:30]
        if len(refs) > 30:
            ref_short += '...'
        
        report_lines.append(
            f"| {system_id} | {protein} | {family} | {contrast} | {tier} | {evidence} | {context} | {ref_short} |"
        )
    
    report_lines.extend([
        "",
        "## Notes",
        "",
        "- **Tier A**: Measured with confidence intervals or sample size",
        "- **Tier B**: Measured but without statistical info",
        "- **Evidence types**: supplement_table, main_table, caption, paragraph, xml",
        "",
        f"Full dataset: `data/processed/atlas_fp_optical_v1_3.csv`",
        ""
    ])
    
    # Save report
    output_path = Path("reports/EVIDENCE_SAMPLES_v1.3.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"OK Evidence samples report generated: {output_path}")
    print(f"   Total lines: {len(measured_df)} (showing {min(len(measured_df), 50)})")
    
    return 0

if __name__ == "__main__":
    sys.exit(generate_evidence_samples())

