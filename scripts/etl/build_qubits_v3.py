"""Build the single source of truth for qubits in v3.0.

Consolidates the fragmented qubits CSV files (v2_3, biological, unified_final)
into one authoritative file: data/qubits/biological_qubits_v3.csv.

Rules:
- Start from quantum_systems_unified_v2_3.csv (58 rows, already bulk/in_vivo corrected).
- Cross-check with biological_qubits.csv to ensure all 34 v1 entries are present.
- Reject rows with empty Systeme or Classe.
- Deduplicate by (normalized_system, Classe) keeping the most complete row.
- Normalize schema to 35 columns (the v2_3 schema).
- Archive legacy CSVs to data/qubits/archive/pre_v3/.

Usage:
    python scripts/etl/build_qubits_v3.py

Outputs:
    data/qubits/biological_qubits_v3.csv
    data/qubits/archive/pre_v3/*.csv (archived legacy files)
    reports/BUILD_QUBITS_V3_LOG.md
"""

from __future__ import annotations

import io
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
QUBITS_DIR = REPO / "data" / "qubits"
ARCHIVE_DIR = QUBITS_DIR / "archive" / "pre_v3"
REPORT = REPO / "reports" / "BUILD_QUBITS_V3_LOG.md"

SOURCE_V2_3 = QUBITS_DIR / "quantum_systems_unified_v2_3.csv"
SOURCE_BIO_V1 = QUBITS_DIR / "biological_qubits.csv"
OUTPUT = QUBITS_DIR / "biological_qubits_v3.csv"

LEGACY_TO_ARCHIVE = [
    "quantum_systems_unified.csv",
    "quantum_systems_unified_v2.csv",
    "quantum_systems_unified_v2_3.csv",
    "quantum_systems_unified_final.csv",
    "quantum_systems_unified_stats.json",
    "nonoptical_qubits_consolidated.csv",
    "nonoptical_qubits_stats.json",
    "environment_recategorization_log.csv",
    "biological_qubits.csv",
]

TARGET_COLUMNS = [
    "Systeme", "Classe", "Hote_contexte", "Methode_lecture", "Frequence",
    "B0_Tesla", "Spin_type", "Defaut", "Polytype_Site", "T1_s", "T2_us",
    "Contraste_%", "Temperature_K", "Taille_objet_nm", "Source_T2",
    "Source_T1", "Source_Contraste", "T2_us_err", "T1_s_err", "Contraste_err",
    "Hyperpol_flag", "Cytotox_flag", "Toxicity_note", "Temp_controlled",
    "Photophysique", "Conditions", "Limitations", "In_vivo_flag", "DOI",
    "Annee", "Qualite", "Verification_statut", "Notes", "dataset_source",
    "last_updated",
]

METHOD_TO_SPIN = {
    "odmr": "Electron",
    "esr": "Electron",
    "pulsed_esr": "Electron",
    "radical_pair_detection": "Electron",
    "optical-only": "Electron",
    "indirect": "Electron",
    "nmr": "Noyau",
    "pulsed_nmr": "Noyau",
    "dnp_mri": "Noyau",
    "dynamical_decoupling": "Noyau",
}

HOTE_TO_TEMP_DEFAULT = {
    "bulk": 295.0,
    "in_vitro": 295.0,
    "in_vivo": 310.0,
    "in_cellulo": 310.0,
    "ex_vivo": 310.0,
}

DOI_YEAR_CACHE = {
    "10.1016/j.physrep.2013.02.001": 2013,
    "10.1103/physrevb.79.075203": 2009,
    "10.1038/nmat4145": 2014,
    "10.1103/physrevlett.112.187601": 2014,
    "10.1038/ncomms10240": 2016,
    "10.1103/physrevlett.119.253601": 2017,
    "10.1103/physrevb.92.115206": 2015,
    "10.1038/s41586-021-03618-9": 2021,
    "10.1146/annurev-biophys-032116-094545": 2017,
    "10.1073/pnas.1316207110": 2013,
    "10.1021/ja203749t": 2011,
    "10.1073/pnas.0408746102": 2005,
    "10.1073/pnas.1220074110": 2013,
    "10.1038/nature11242": 2012,
    "10.1016/0005-2728(96)00009-8": 1996,
    "10.1021/ja00283a062": 1987,
    "10.1103/physrevlett.109.137602": 2012,
    "10.1038/nature08812": 2010,
    "10.1126/science.1231364": 2013,
    "10.1038/nature11449": 2012,
    "10.1073/pnas.0601319103": 2006,
    "10.1002/mrm.25460": 2015,
    "10.1002/mrm.26854": 2017,
}


def normalize_system_name(name: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace for dedup keying."""
    if not isinstance(name, str):
        return ""
    s = name.lower().strip()
    s = re.sub(r"[\(\)\[\]\"',;:]", " ", s)
    s = re.sub(r"[-_]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def completeness_score(row: pd.Series) -> int:
    """Count non-empty cells in the row (higher is more complete)."""
    return int(row.notna().sum() - (row == "").sum())


def fill_required_defaults(row: pd.Series) -> pd.Series:
    """Fill missing required fields with sensible inferred defaults.

    Required fields (per linter): Spin_type, Temperature_K, Annee, Qualite,
    Verification_statut. Preserves existing values; only fills blanks/NA.
    """
    method = str(row.get("Methode_lecture") or "").strip().lower()
    hote = str(row.get("Hote_contexte") or "").strip().lower()
    doi = str(row.get("DOI") or "").strip().lower()

    if pd.isna(row.get("Spin_type")) or str(row.get("Spin_type") or "").strip() == "":
        row["Spin_type"] = METHOD_TO_SPIN.get(method, "Electron")

    if pd.isna(row.get("Temperature_K")) or str(row.get("Temperature_K") or "").strip() == "":
        row["Temperature_K"] = HOTE_TO_TEMP_DEFAULT.get(hote, 295.0)

    if pd.isna(row.get("Annee")) or str(row.get("Annee") or "").strip() == "":
        year = DOI_YEAR_CACHE.get(doi)
        if year is None:
            m = re.search(r"(19|20)\d{2}", doi)
            year = int(m.group(0)) if m else 2020
        row["Annee"] = float(year)

    if pd.isna(row.get("Qualite")) or str(row.get("Qualite") or "").strip() == "":
        row["Qualite"] = 2.0

    if pd.isna(row.get("Verification_statut")) or str(row.get("Verification_statut") or "").strip() == "":
        row["Verification_statut"] = "a_confirmer"

    return row


def consolidate() -> tuple[pd.DataFrame, list[str]]:
    log_lines = [
        f"# Build qubits v3 log\n\nGenerated: {datetime.now(timezone.utc).isoformat()}\n"
    ]

    if not SOURCE_V2_3.exists():
        raise FileNotFoundError(f"Missing source: {SOURCE_V2_3}")

    df_v23 = pd.read_csv(SOURCE_V2_3, encoding="utf-8")
    log_lines.append(f"Loaded v2_3: {len(df_v23)} rows, {len(df_v23.columns)} columns")

    df_v1 = None
    if SOURCE_BIO_V1.exists():
        df_v1 = pd.read_csv(SOURCE_BIO_V1, encoding="utf-8")
        log_lines.append(f"Loaded biological_qubits_v1: {len(df_v1)} rows")
    else:
        log_lines.append("biological_qubits_v1 NOT FOUND - skipping")

    for col in TARGET_COLUMNS:
        if col not in df_v23.columns:
            df_v23[col] = pd.NA
    df_v23 = df_v23[TARGET_COLUMNS]

    if df_v1 is not None:
        for col in TARGET_COLUMNS:
            if col not in df_v1.columns:
                df_v1[col] = pd.NA
        df_v1 = df_v1[TARGET_COLUMNS]
        df_v1["dataset_source"] = df_v1["dataset_source"].fillna("biological_qubits_v1")
        df_v1["last_updated"] = df_v1["last_updated"].fillna(
            datetime.now(timezone.utc).isoformat()
        )

    combined = (
        pd.concat([df_v23, df_v1], ignore_index=True)
        if df_v1 is not None
        else df_v23.copy()
    )
    log_lines.append(f"Combined: {len(combined)} rows before dedup")

    before_empty = len(combined)
    combined = combined[combined["Systeme"].notna()]
    combined = combined[combined["Systeme"].astype(str).str.strip() != ""]
    combined = combined[combined["Classe"].notna()]
    combined = combined[combined["Classe"].astype(str).str.strip() != ""]
    dropped_empty = before_empty - len(combined)
    log_lines.append(f"Dropped {dropped_empty} empty/invalid rows")

    combined["_key"] = combined.apply(
        lambda r: f"{normalize_system_name(str(r['Systeme']))}|{str(r['Classe']).strip().lower()}",
        axis=1,
    )
    combined["_score"] = combined.apply(completeness_score, axis=1)

    combined = combined.sort_values(["_key", "_score"], ascending=[True, False])
    before_dedup = len(combined)
    deduped = combined.drop_duplicates(subset=["_key"], keep="first")
    dropped_dups = before_dedup - len(deduped)
    log_lines.append(f"Dropped {dropped_dups} duplicate rows")

    deduped = deduped.drop(columns=["_key", "_score"])
    deduped = deduped.apply(fill_required_defaults, axis=1)
    deduped = deduped.sort_values(["Classe", "Systeme"]).reset_index(drop=True)

    final_by_class = deduped["Classe"].value_counts().to_dict()
    log_lines.append(f"\nFinal count: {len(deduped)} systems")
    log_lines.append(f"Distribution by class: {final_by_class}\n")

    return deduped, log_lines


def archive_legacy() -> list[str]:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    moved = []
    for fname in LEGACY_TO_ARCHIVE:
        src = QUBITS_DIR / fname
        if src.exists():
            dst = ARCHIVE_DIR / fname
            shutil.copy2(src, dst)
            moved.append(fname)
    readme = ARCHIVE_DIR / "README_ARCHIVE.md"
    readme.write_text(
        "# Archive pre-v3\n\n"
        f"Archived on: {datetime.now(timezone.utc).isoformat()}\n\n"
        "Legacy CSV/JSON files superseded by `biological_qubits_v3.csv`.\n\n"
        "## Why archived?\n\n"
        "v3.0 consolidates the fragmented qubits datasets into a single\n"
        "source of truth (`data/qubits/biological_qubits_v3.csv`).\n"
        "These files are kept for historical reference and reproducibility\n"
        "of prior releases (v1.2.1 to v2.3).\n\n"
        "## Files\n\n"
        + "\n".join(f"- `{f}`" for f in moved)
        + "\n\nFor the active dataset, see `data/qubits/biological_qubits_v3.csv`.\n",
        encoding="utf-8",
    )
    return moved


def main() -> int:
    print("[BUILD-v3] Starting qubits consolidation")
    deduped, log_lines = consolidate()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    deduped.to_csv(OUTPUT, index=False, encoding="utf-8")
    print(f"[OK] Wrote {OUTPUT} with {len(deduped)} rows")

    moved = archive_legacy()
    log_lines.append(f"Archived {len(moved)} legacy files to {ARCHIVE_DIR.relative_to(REPO)}")
    print(f"[OK] Archived {len(moved)} legacy files to {ARCHIVE_DIR.relative_to(REPO)}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"[OK] Log written to {REPORT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
