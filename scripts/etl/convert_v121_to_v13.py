#!/usr/bin/env python3
"""
Convert v1.2.1 curated contrasts to v1.3 schema
================================================
"""

import pandas as pd
import sys
from pathlib import Path

def convert_v121_to_v13():
    """Convert v1.2.1 schema to v1.3 schema."""
    
    # Read v1.2.1
    v121_path = Path("data/curated_contrasts.csv")
    if not v121_path.exists():
        print(f"ERROR: {v121_path} not found")
        return 1
    
    df_old = pd.read_csv(v121_path)
    print(f"Loaded {len(df_old)} entries from v1.2.1")
    
    # Map to new schema
    records = []
    for _, row in df_old.iterrows():
        # Determine quality tier
        # v1.2.1 has mostly tier B (measured but no explicit CI/n in CSV)
        quality_tier = 'B'
        
        # Determine is_biosensor from family
        biosensor_families = ['Calcium', 'Dopamine', 'Glutamate', 'Voltage', 'pH', 
                             'cAMP', 'H2O2', 'Redox', 'ATP/ADP', 'Serotonin', 
                             'Acetylcholine', 'Norepinephrine', 'ATP']
        is_biosensor = 1 if row.get('family_type') in biosensor_families else 0
        
        # Map measure_type to contrast_unit
        measure_type = str(row.get('measure_type', 'fold_change'))
        if 'fold' in measure_type.lower():
            contrast_unit = 'fold'
        elif 'delta' in measure_type.lower() or 'df' in measure_type.lower():
            contrast_unit = 'deltaF/F0'
        elif 'percent' in measure_type.lower():
            contrast_unit = 'percent'
        else:
            contrast_unit = 'fold'  # Default
        
        # Compute normalized value
        contrast_value = row.get('contrast_ratio')
        if pd.notna(contrast_value):
            if contrast_unit == 'fold':
                contrast_normalized = float(contrast_value)
            elif contrast_unit == 'deltaF/F0':
                contrast_normalized = 1.0 + float(contrast_value)
            elif contrast_unit == 'percent':
                contrast_normalized = 1.0 + float(contrast_value) / 100.0
            else:
                contrast_normalized = float(contrast_value)
        else:
            contrast_normalized = None
        
        # Extract context (simplified)
        condition_text = str(row.get('condition_text', ''))
        if 'HEK' in condition_text or 'HeLa' in condition_text:
            context = f"in_cellulo({condition_text.split()[0]})" if condition_text else "in_cellulo"
        elif 'neuron' in condition_text.lower() or 'brain' in condition_text.lower():
            context = "in_vivo(neurons)"
        else:
            context = "in_cellulo"
        
        new_record = {
            'protein_name': row.get('protein_name'),
            'family': row.get('family_type'),
            'is_biosensor': is_biosensor,
            'context': context,
            'temperature_K': 298,  # Assume room temp if not specified
            'pH': 7.4,  # Assume physiological if not specified
            'contrast_value': contrast_value,
            'contrast_unit': contrast_unit,
            'contrast_normalized': contrast_normalized,
            'quality_tier': quality_tier,
            'n': None,  # Not in v1.2.1
            'spread_type': 'none',
            'spread_value': None,
            'method': 'fluorescence',
            'assay': 'imaging',
            'doi': row.get('doi'),
            'pmcid': row.get('pmcid'),
            'license': row.get('license_source'),
            'source_note': row.get('notes'),
            'curator': 'v1.2.1_migration'
        }
        records.append(new_record)
    
    df_new = pd.DataFrame(records)
    
    # Save
    output_path = Path("data/curated_contrasts_v1_3.csv")
    df_new.to_csv(output_path, index=False)
    print(f"Converted {len(df_new)} entries to v1.3 schema")
    print(f"Saved to: {output_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(convert_v121_to_v13())

