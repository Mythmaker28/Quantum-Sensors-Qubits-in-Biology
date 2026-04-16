"""
Merge non-optical consolidated dataset into quantum_systems_unified.csv
- Deduplicate by DOI (robust extraction)
- Map only fields present in sources (no invention)
- Write quantum_systems_unified_v2.csv

Windows-safe UTF-8 stdout; no emojis.
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from datetime import datetime
import re
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
UNIFIED_PATH = REPO_ROOT / 'data' / 'qubits' / 'quantum_systems_unified.csv'
NONOPT_PATH = REPO_ROOT / 'data' / 'qubits' / 'nonoptical_qubits_consolidated.csv'
OUTPUT_PATH = REPO_ROOT / 'data' / 'qubits' / 'quantum_systems_unified_v2.csv'
REPORT_PATH = REPO_ROOT / 'analysis' / 'output' / 'merge_nonoptical_report.json'

DOI_REGEX = re.compile(r'(10\.\d{4,9}/[-._;()/:A-Z0-9]+)', re.IGNORECASE)


def extract_doi(text: str) -> str:
    if not isinstance(text, str) or not text:
        return ''
    m = DOI_REGEX.search(text)
    return m.group(1).lower() if m else text.strip().lower()


def load_datasets():
    df_u = pd.read_csv(UNIFIED_PATH)
    df_n = pd.read_csv(NONOPT_PATH)
    return df_u, df_n


def build_existing_doi_set(df_u: pd.DataFrame) -> set:
    dois = set()
    for v in df_u.get('DOI', []):
        doi = extract_doi(v)
        if doi:
            dois.add(doi)
    # Some sources store DOI-like references in Source_T1/Source_T2 too
    for col in ['Source_T1', 'Source_T2', 'Source_Contraste']:
        if col in df_u.columns:
            for v in df_u[col].fillna(''):
                doi = extract_doi(v)
                if doi:
                    dois.add(doi)
    return dois


def modality_to_classe(modality: str) -> str:
    # Keep consistent with existing dataset conventions
    # spin_qubit -> B, radical_pair -> D, nuclear_spin -> C
    m = (modality or '').lower()
    if m == 'spin_qubit':
        return 'B'
    if m == 'radical_pair':
        return 'D'
    if m == 'nuclear_spin':
        return 'C'
    return ''


def build_new_rows(df_n: pd.DataFrame, existing_dois: set) -> pd.DataFrame:
    # Target columns in unified
    target_cols = [
        'Systeme','Classe','Hote_contexte','Methode_lecture','Frequence','B0_Tesla','Spin_type',
        'Defaut','Polytype_Site','T1_s','T2_us','Contraste_%','Temperature_K','Taille_objet_nm',
        'Source_T2','Source_T1','Source_Contraste','T2_us_err','T1_s_err','Contraste_err',
        'Hyperpol_flag','Cytotox_flag','Toxicity_note','Temp_controlled','Photophysique',
        'Conditions','Limitations','In_vivo_flag','DOI','Annee','Qualite','Verification_statut',
        'Notes','dataset_source','last_updated'
    ]

    records = []
    for _, row in df_n.iterrows():
        doi_raw = row.get('source_doi', '')
        doi_norm = extract_doi(doi_raw)
        if not doi_norm:
            # Skip rows without DOI to avoid unverifiable entries
            continue
        if doi_norm in existing_dois:
            continue

        modality = row.get('modality', '')
        classe = modality_to_classe(modality)

        # Map fields; leave unknowns empty
        systeme = row.get('system_name', '')
        hote = row.get('host_material', '')
        methode = row.get('method', '')
        t1_us = row.get('T1_us', None)
        t2_us = row.get('T2_us', None)
        temp_k = row.get('temperature_K', None)
        notes = row.get('notes', '')

        # Convert T1_us (microseconds) to seconds for unified T1_s
        t1_s_val = ''
        if pd.notna(t1_us):
            try:
                t1_s_val = float(t1_us) / 1_000_000.0
            except Exception:
                t1_s_val = ''

        # Keep T2_us as-is when present
        t2_us_val = ''
        if pd.notna(t2_us):
            try:
                t2_us_val = float(t2_us)
            except Exception:
                t2_us_val = ''

        temp_val = ''
        if pd.notna(temp_k):
            try:
                temp_val = float(temp_k)
            except Exception:
                temp_val = ''

        record = {
            'Systeme': systeme,
            'Classe': classe,
            'Hote_contexte': hote,
            'Methode_lecture': methode,
            'Frequence': '',
            'B0_Tesla': '',
            'Spin_type': '',
            'Defaut': '',
            'Polytype_Site': '',
            'T1_s': t1_s_val,
            'T2_us': t2_us_val,
            'Contraste_%': '',
            'Temperature_K': temp_val,
            'Taille_objet_nm': '',
            'Source_T2': '',
            'Source_T1': '',
            'Source_Contraste': '',
            'T2_us_err': '',
            'T1_s_err': '',
            'Contraste_err': '',
            'Hyperpol_flag': '',
            'Cytotox_flag': '',
            'Toxicity_note': '',
            'Temp_controlled': '',
            'Photophysique': '',
            'Conditions': '',
            'Limitations': '',
            'In_vivo_flag': '',
            'DOI': doi_norm,
            'Annee': '',
            'Qualite': '',
            'Verification_statut': '',
            'Notes': notes,
            'dataset_source': 'nonoptical_merge_v2',
            'last_updated': datetime.now().isoformat(),
        }
        # Keep only target columns order
        records.append({k: record.get(k, '') for k in target_cols})

    return pd.DataFrame.from_records(records, columns=target_cols)


def main():
    print('=' * 60)
    print('MERGE nonoptical_qubits_consolidated -> quantum_systems_unified')
    print('=' * 60)

    df_u, df_n = load_datasets()
    print(f"[OK] Loaded unified: {len(df_u)} rows")
    print(f"[OK] Loaded nonoptical consolidated: {len(df_n)} rows")

    existing_dois = build_existing_doi_set(df_u)
    print(f"[INFO] Existing DOI set size: {len(existing_dois)}")

    df_new = build_new_rows(df_n, existing_dois)
    print(f"[RESULT] New rows to add: {len(df_new)}")

    df_out = pd.concat([df_u, df_new], ignore_index=True)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(OUTPUT_PATH, index=False)
    print(f"[OK] Wrote: {OUTPUT_PATH}")

    # Save report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = {
        'unified_rows_before': int(len(df_u)),
        'nonoptical_rows': int(len(df_n)),
        'new_rows_added': int(len(df_new)),
        'unified_rows_after': int(len(df_out)),
        'output_path': str(OUTPUT_PATH),
        'timestamp': datetime.now().isoformat(),
    }
    import json
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"[OK] Report: {REPORT_PATH}")


if __name__ == '__main__':
    main()
