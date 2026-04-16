"""
Discover, unify, and clean all quantum systems CSV files in this repository.
NO EMOJIS - Windows PowerShell compatibility
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
from pathlib import Path
import json
import re
from datetime import datetime
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "data" / "qubits"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DOI_REGEX = re.compile(r'(10\.\d{4,9}/[-._;()/:A-Z0-9]+)', re.IGNORECASE)


def extract_doi(text):
    """Extract DOI from text."""
    if pd.isna(text) or not isinstance(text, str):
        return ''
    m = DOI_REGEX.search(text)
    return m.group(1).lower() if m else ''


def normalize_doi(doi):
    """Normalize DOI for comparison."""
    if not doi:
        return ''
    doi = str(doi).strip().lower()
    # Remove common prefixes
    doi = doi.replace('doi:', '').replace('doi ', '')
    return doi


def discover_csv_files():
    """Discover all CSV files related to quantum systems."""
    
    print("\n" + "=" * 70)
    print("STEP 1: DISCOVERING CSV FILES")
    print("=" * 70)
    
    csv_files = {
        'qubits_unified': [
            OUTPUT_DIR / "quantum_systems_unified_v2.csv",
            OUTPUT_DIR / "quantum_systems_unified.csv",
        ],
        'qubits_biological': [
            OUTPUT_DIR / "biological_qubits.csv",
        ],
        'qubits_nonoptical': [
            OUTPUT_DIR / "nonoptical_qubits_consolidated.csv",
        ],
        'non_optical_staging': [
            REPO_ROOT / "data" / "non_optical" / "spin_qubits" / "staging" / "spin_qubit_candidates.csv",
            REPO_ROOT / "data" / "non_optical" / "radical_pairs" / "staging" / "radical_pair_candidates.csv",
            REPO_ROOT / "data" / "non_optical" / "nuclear_spins" / "staging" / "nuclear_spin_candidates.csv",
        ],
        'optical_atlas': [
            REPO_ROOT / "data" / "processed" / "atlas_fp_optical_v2_2_curated.csv",
            REPO_ROOT / "data" / "processed" / "atlas_fp_optical_v2_2.csv",
        ],
    }
    
    discovered = {}
    for category, paths in csv_files.items():
        for path in paths:
            if path.exists():
                try:
                    df = pd.read_csv(path, nrows=0)  # Just headers
                    discovered[str(path)] = {
                        'category': category,
                        'columns': list(df.columns),
                        'exists': True
                    }
                    print(f"[OK] {path.name}: {len(df.columns)} columns")
                except Exception as e:
                    print(f"[ERROR] {path.name}: {e}")
                    discovered[str(path)] = {
                        'category': category,
                        'exists': False,
                        'error': str(e)
                    }
            else:
                discovered[str(path)] = {
                    'category': category,
                    'exists': False
                }
    
    return discovered, csv_files


def load_and_normalize_dataframe(path, category):
    """Load CSV and normalize to standard schema."""
    
    if not path.exists():
        return None
    
    try:
        # Handle problematic CSV files with better error handling
        if 'radical_pair' in str(path):
            df = pd.read_csv(path, low_memory=False, on_bad_lines='skip', encoding='utf-8')
        else:
            df = pd.read_csv(path, low_memory=False, encoding='utf-8')
        print(f"  [LOAD] {path.name}: {len(df)} rows")
        
        # Map to standard schema
        standard_cols = {
            'Systeme': ['Systeme', 'system_name', 'protein_name', 'SystemID'],
            'Classe': ['Classe', 'family', 'modality', 'class'],
            'DOI': ['DOI', 'doi', 'source_doi'],
            'T1_s': ['T1_s', 'T1_microseconds', 'T1_milliseconds'],
            'T2_us': ['T2_us', 'T2_microseconds', 'T2_milliseconds', 'timescale_ns'],
            'Temperature_K': ['Temperature_K', 'temperature_K', 'temperature'],
            'Contraste_%': ['Contraste_%', 'contrast_ratio', 'contrast'],
            'Hote_contexte': ['Hote_contexte', 'host_material', 'organism', 'context'],
            'Methode_lecture': ['Methode_lecture', 'method', 'measurement_method'],
            'Qualite': ['Qualite', 'quality', 'evidence_level', 'evidence'],
            'Verification_statut': ['Verification_statut', 'verification_status', 'status'],
        }
        
        mapped = {}
        for std_col, variants in standard_cols.items():
            for variant in variants:
                if variant in df.columns:
                    mapped[std_col] = df[variant]
                    break
        
        # Create normalized dataframe
        result = pd.DataFrame()
        for std_col in standard_cols.keys():
            if std_col in mapped:
                result[std_col] = mapped[std_col]
            else:
                result[std_col] = None
        
        # Handle special conversions
        if 'T1_milliseconds' in df.columns and 'T1_s' not in mapped:
            result['T1_s'] = df['T1_milliseconds'] / 1000.0
        if 'T1_microseconds' in df.columns and 'T1_s' not in mapped:
            result['T1_s'] = df['T1_microseconds'] / 1_000_000.0
        
        if 'T2_milliseconds' in df.columns and 'T2_us' not in mapped:
            result['T2_us'] = df['T2_milliseconds'] * 1000.0
        if 'timescale_ns' in df.columns and 'T2_us' not in mapped:
            result['T2_us'] = df['timescale_ns'] / 1000.0
        
        # Add metadata
        result['_source_file'] = path.name
        result['_source_category'] = category
        
        # Copy other columns that might be useful
        for col in df.columns:
            if col not in result.columns and col not in [v for variants in standard_cols.values() for v in variants]:
                result[col] = df[col]
        
        return result
        
    except Exception as e:
        print(f"  [ERROR] Failed to load {path.name}: {e}")
        return None


def clean_decimal_precision(df):
    """Clean decimal precision for physical quantities."""
    
    print("\n" + "=" * 70)
    print("STEP 3: CLEANING DECIMAL PRECISION")
    print("=" * 70)
    
    # Define precision rules
    precision_rules = {
        'T1_s': 3,  # 2-3 decimals max
        'T2_us': 2,  # 1-2 decimals max
        'Contraste_%': 1,  # 1 decimal max
        'Temperature_K': 1,  # 1 decimal max
    }
    
    cleaned_count = 0
    for col, decimals in precision_rules.items():
        if col in df.columns:
            before = df[col].notna().sum()
            # Convert to numeric, round, then back
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].round(decimals)
            after = df[col].notna().sum()
            if before != after:
                print(f"  [CLEAN] {col}: {before} -> {after} valid values")
                cleaned_count += 1
    
    return df, cleaned_count


def validate_physical_values(df):
    """Validate physical values and flag suspicious entries."""
    
    print("\n" + "=" * 70)
    print("STEP 4: VALIDATING PHYSICAL VALUES")
    print("=" * 70)
    
    if 'flag_suspect' not in df.columns:
        df['flag_suspect'] = 0
    if 'flag_reason' not in df.columns:
        df['flag_reason'] = ''
    
    suspect_count = 0
    
    # Check T2_us
    if 'T2_us' in df.columns:
        invalid = (df['T2_us'] < 0) | (df['T2_us'] > 1e9)  # Reasonable upper bound
        if invalid.any():
            df.loc[invalid, 'flag_suspect'] = 1
            df.loc[invalid, 'flag_reason'] = df.loc[invalid, 'flag_reason'].astype(str) + '; T2_out_of_range'
            suspect_count += invalid.sum()
            print(f"  [FLAG] {invalid.sum()} rows with T2_us out of range")
    
    # Check T1_s
    if 'T1_s' in df.columns:
        invalid = (df['T1_s'] < 0) | (df['T1_s'] > 1e6)  # Reasonable upper bound
        if invalid.any():
            df.loc[invalid, 'flag_suspect'] = 1
            df.loc[invalid, 'flag_reason'] = df.loc[invalid, 'flag_reason'].astype(str) + '; T1_out_of_range'
            suspect_count += invalid.sum()
            print(f"  [FLAG] {invalid.sum()} rows with T1_s out of range")
    
    # Check Temperature_K
    if 'Temperature_K' in df.columns:
        invalid = (df['Temperature_K'] < 0) | (df['Temperature_K'] > 1000)
        if invalid.any():
            df.loc[invalid, 'flag_suspect'] = 1
            df.loc[invalid, 'flag_reason'] = df.loc[invalid, 'flag_reason'].astype(str) + '; Temp_out_of_range'
            suspect_count += invalid.sum()
            print(f"  [FLAG] {invalid.sum()} rows with Temperature_K out of range")
    
    print(f"  [SUMMARY] {suspect_count} rows flagged as suspect")
    
    return df


def assign_quality_score(df):
    """Assign Data_Quality_Atlas score."""
    
    print("\n" + "=" * 70)
    print("STEP 5: ASSIGNING QUALITY SCORES")
    print("=" * 70)
    
    def score_row(row):
        has_t1 = pd.notna(row.get('T1_s')) and row.get('T1_s', 0) > 0
        has_t2 = pd.notna(row.get('T2_us')) and row.get('T2_us', 0) > 0
        has_doi = pd.notna(row.get('DOI')) and str(row.get('DOI', '')).strip() != ''
        has_classe = pd.notna(row.get('Classe')) and str(row.get('Classe', '')).strip() != ''
        has_context = pd.notna(row.get('Hote_contexte')) and str(row.get('Hote_contexte', '')).strip() != ''
        
        qualite = row.get('Qualite', '')
        verification = str(row.get('Verification_statut', '')).lower()
        is_verified = 'verifie' in verification or 'verified' in verification
        
        # HIGH: T1 and T2 present, DOI present, clear experimental context, high quality/verified
        if has_t1 and has_t2 and has_doi and has_classe and has_context:
            if (qualite in ['3', 3] or is_verified):
                return 'HIGH'
            elif qualite in ['2', 2]:
                return 'HIGH'  # Still high if T1+T2+DOI present
            else:
                return 'MEDIUM'
        
        # MEDIUM: T1 or T2 missing, but system well described (DOI + context + classe OK)
        if (has_t1 or has_t2) and has_doi and has_classe and has_context:
            return 'MEDIUM'
        
        # LOW: Very partial data, but at least some useful info
        if has_doi or has_classe or has_context:
            return 'LOW'
        
        # INCOMPLETE: Almost nothing exploitable
        return 'INCOMPLETE'
    
    df['Data_Quality_Atlas'] = df.apply(score_row, axis=1)
    
    quality_counts = df['Data_Quality_Atlas'].value_counts()
    print("\n  [QUALITY DISTRIBUTION]")
    for quality, count in quality_counts.items():
        print(f"    {quality}: {count}")
    
    return df


def deduplicate_systems(df):
    """Deduplicate systems using Systeme/Classe/DOI combo."""
    
    print("\n" + "=" * 70)
    print("STEP 2: DEDUPLICATING SYSTEMS")
    print("=" * 70)
    
    print(f"  [BEFORE] {len(df)} rows")
    
    # Create unique key
    df['_unique_key'] = (
        df['Systeme'].fillna('').astype(str).str.lower().str.strip() + '|' +
        df['Classe'].fillna('').astype(str).str.lower().str.strip() + '|' +
        df['DOI'].fillna('').apply(normalize_doi)
    )
    
    # Group by unique key
    groups = df.groupby('_unique_key')
    
    merged_rows = []
    merge_notes = []
    
    for key, group in groups:
        if len(group) == 1:
            merged_rows.append(group.iloc[0])
        else:
            # Merge multiple rows
            print(f"  [MERGE] {len(group)} rows for key: {key[:60]}...")
            
            # Take the most complete row
            row = group.iloc[0].copy()
            
            # Fill missing values from other rows
            for idx, other_row in group.iloc[1:].iterrows():
                for col in df.columns:
                    if pd.isna(row[col]) or row[col] == '':
                        if pd.notna(other_row[col]) and other_row[col] != '':
                            row[col] = other_row[col]
            
            # Add merge note
            sources = group['_source_file'].unique().tolist()
            row['merge_note'] = f"Merged from {len(group)} rows: {', '.join(sources)}"
            merge_notes.append(len(group) - 1)
            
            merged_rows.append(row)
    
    df_merged = pd.DataFrame(merged_rows)
    
    # Drop temporary columns
    if '_unique_key' in df_merged.columns:
        df_merged = df_merged.drop(columns=['_unique_key'])
    
    print(f"  [AFTER] {len(df_merged)} rows")
    print(f"  [REMOVED] {len(df) - len(df_merged)} duplicates")
    if merge_notes:
        print(f"  [MERGED] {sum(merge_notes)} rows merged into existing entries")
    
    return df_merged


def generate_status_report(df, discovered_files):
    """Generate ATLAS_STATUS.md report."""
    
    print("\n" + "=" * 70)
    print("STEP 6: GENERATING STATUS REPORT")
    print("=" * 70)
    
    # Calculate statistics
    n_total = len(df)
    n_high = len(df[df['Data_Quality_Atlas'] == 'HIGH'])
    n_medium = len(df[df['Data_Quality_Atlas'] == 'MEDIUM'])
    n_low = len(df[df['Data_Quality_Atlas'] == 'LOW'])
    n_incomplete = len(df[df['Data_Quality_Atlas'] == 'INCOMPLETE'])
    
    # By class
    class_stats = df.groupby('Classe')['Data_Quality_Atlas'].value_counts().unstack(fill_value=0)
    
    # By quality metric availability
    has_t1 = df['T1_s'].notna().sum()
    has_t2 = df['T2_us'].notna().sum()
    has_both = (df['T1_s'].notna() & df['T2_us'].notna()).sum()
    has_doi = df['DOI'].notna().sum()
    has_classe = df['Classe'].notna().sum()
    
    # Generate markdown
    md_content = f"""# ATLAS STATUS - Quantum Systems Biological Atlas

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Repository:** QBitAtlas (Quantum-Sensors-Qubits-in-Biology)

---

## SUMMARY

### Total Systems

- **n_total_systems**: {n_total}
- **n_high** (Data_Quality_Atlas = HIGH): {n_high}
- **n_medium** (Data_Quality_Atlas = MEDIUM): {n_medium}
- **n_low** (Data_Quality_Atlas = LOW): {n_low}
- **n_incomplete** (Data_Quality_Atlas = INCOMPLETE): {n_incomplete}

### Quality Breakdown

| Quality Level | Count | Percentage |
|---------------|-------|------------|
| HIGH | {n_high} | {n_high/n_total*100:.1f}% |
| MEDIUM | {n_medium} | {n_medium/n_total*100:.1f}% |
| LOW | {n_low} | {n_low/n_total*100:.1f}% |
| INCOMPLETE | {n_incomplete} | {n_incomplete/n_total*100:.1f}% |

### Data Completeness

- Systems with T1: {has_t1} ({has_t1/n_total*100:.1f}%)
- Systems with T2: {has_t2} ({has_t2/n_total*100:.1f}%)
- Systems with both T1 and T2: {has_both} ({has_both/n_total*100:.1f}%)
- Systems with DOI: {has_doi} ({has_doi/n_total*100:.1f}%)
- Systems with Classe: {has_classe} ({has_classe/n_total*100:.1f}%)

---

## BY CLASS

"""
    
    if not class_stats.empty:
        md_content += "| Classe | HIGH | MEDIUM | LOW | INCOMPLETE | Total |\n"
        md_content += "|--------|------|--------|-----|------------|-------|\n"
        for classe in class_stats.index:
            high = class_stats.loc[classe, 'HIGH'] if 'HIGH' in class_stats.columns else 0
            medium = class_stats.loc[classe, 'MEDIUM'] if 'MEDIUM' in class_stats.columns else 0
            low = class_stats.loc[classe, 'LOW'] if 'LOW' in class_stats.columns else 0
            incomplete = class_stats.loc[classe, 'INCOMPLETE'] if 'INCOMPLETE' in class_stats.columns else 0
            total = high + medium + low + incomplete
            md_content += f"| {classe} | {high} | {medium} | {low} | {incomplete} | {total} |\n"
    
    md_content += f"""

---

## DATA SOURCES

### CSV Files Discovered

"""
    
    for filepath, info in discovered_files.items():
        if info.get('exists'):
            md_content += f"- **{Path(filepath).name}**\n"
            md_content += f"  - Category: {info['category']}\n"
            md_content += f"  - Columns: {len(info.get('columns', []))}\n"
        else:
            md_content += f"- **{Path(filepath).name}** (not found)\n"
    
    md_content += f"""

---

## DATA GAPS

### Missing T2 by Class

"""
    
    for classe in df['Classe'].dropna().unique():
        class_df = df[df['Classe'] == classe]
        missing_t2 = class_df['T2_us'].isna().sum()
        total_class = len(class_df)
        if missing_t2 > 0:
            md_content += f"- **Classe {classe}**: {missing_t2}/{total_class} systems missing T2 ({missing_t2/total_class*100:.1f}%)\n"
    
    md_content += f"""

### Missing T1 by Class

"""
    
    for classe in df['Classe'].dropna().unique():
        class_df = df[df['Classe'] == classe]
        missing_t1 = class_df['T1_s'].isna().sum()
        total_class = len(class_df)
        if missing_t1 > 0:
            md_content += f"- **Classe {classe}**: {missing_t1}/{total_class} systems missing T1 ({missing_t1/total_class*100:.1f}%)\n"
    
    md_content += f"""

---

## SUSPICIOUS ENTRIES

"""
    
    if 'flag_suspect' in df.columns:
        suspect_df = df[df['flag_suspect'] == 1]
        if len(suspect_df) > 0:
            md_content += f"**{len(suspect_df)} systems flagged as suspicious:**\n\n"
            for idx, row in suspect_df.iterrows():
                md_content += f"- {row.get('Systeme', 'Unknown')} (Classe: {row.get('Classe', 'N/A')}): {row.get('flag_reason', 'No reason')}\n"
        else:
            md_content += "No suspicious entries detected.\n"
    else:
        md_content += "Flag validation not performed.\n"
    
    md_content += f"""

---

## UNIFIED DATASET

**File:** `data/qubits/quantum_systems_unified_final.csv`

This file contains all systems from all discovered CSV files, deduplicated and cleaned.

**Key Features:**
- Deduplication by Systeme/Classe/DOI combination
- Decimal precision cleaned (T1_s: 3 decimals, T2_us: 2 decimals, etc.)
- Physical value validation (out-of-range values flagged)
- Quality scores assigned (HIGH/MEDIUM/LOW/INCOMPLETE)
- No invented values - all data from source CSVs only

---

**End of Report**
"""
    
    report_path = REPO_ROOT / "ATLAS_STATUS.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"  [OK] Report saved to: {report_path}")
    
    return report_path


def main():
    """Main execution."""
    
    print("=" * 70)
    print("QUANTUM SYSTEMS ATLAS - DISCOVERY & UNIFICATION")
    print("=" * 70)
    
    # Step 1: Discover files
    discovered, csv_files = discover_csv_files()
    
    # Step 2: Load and merge all data
    print("\n" + "=" * 70)
    print("STEP 2: LOADING AND MERGING DATA")
    print("=" * 70)
    
    all_dataframes = []
    
    # Load qubits unified (highest priority)
    for path in csv_files['qubits_unified']:
        if path.exists():
            df = load_and_normalize_dataframe(path, 'qubits_unified')
            if df is not None:
                all_dataframes.append(df)
    
    # Load biological qubits
    for path in csv_files['qubits_biological']:
        if path.exists():
            df = load_and_normalize_dataframe(path, 'qubits_biological')
            if df is not None:
                all_dataframes.append(df)
    
    # Load non-optical
    for path in csv_files['qubits_nonoptical']:
        if path.exists():
            df = load_and_normalize_dataframe(path, 'qubits_nonoptical')
            if df is not None:
                all_dataframes.append(df)
    
    # Load non-optical staging
    for path in csv_files['non_optical_staging']:
        if path.exists():
            df = load_and_normalize_dataframe(path, 'non_optical_staging')
            if df is not None:
                all_dataframes.append(df)
    
    # Note: Optical FP atlas is separate (180 systems), not merged here
    # as it's a different modality (optical vs non-optical quantum sensors)
    
    if not all_dataframes:
        print("[ERROR] No data loaded!")
        return
    
    # Concatenate all
    df_all = pd.concat(all_dataframes, ignore_index=True)
    print(f"\n[LOADED] Total rows from all sources: {len(df_all)}")
    
    # Deduplicate
    df_merged = deduplicate_systems(df_all)
    
    # Clean decimals
    df_cleaned, _ = clean_decimal_precision(df_merged)
    
    # Validate
    df_validated = validate_physical_values(df_cleaned)
    
    # Assign quality
    df_final = assign_quality_score(df_validated)
    
    # Save unified file
    output_path = OUTPUT_DIR / "quantum_systems_unified_final.csv"
    df_final.to_csv(output_path, index=False)
    print(f"\n[OK] Unified dataset saved to: {output_path}")
    
    # Generate report
    report_path = generate_status_report(df_final, discovered)
    
    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"\nUnified dataset: {output_path}")
    print(f"Status report: {report_path}")
    print(f"\nTotal systems: {len(df_final)}")
    print(f"High quality: {len(df_final[df_final['Data_Quality_Atlas'] == 'HIGH'])}")


if __name__ == "__main__":
    main()

