"""Enrich the fluorescent-protein optical atlas with 2024-2026 biosensors.

Starts from data/optical/curated/atlas_fp_optical_v2_2_curated.csv (180 rows)
and emits data/optical/curated/atlas_fp_optical_v3_curated.csv plus a mirror
in data/processed/.

Adds the following biosensors published after the v2.2 freeze:
- CaBLAM (bioluminescent Ca2+, Lambert et al., Nat Methods 2026)
- HaloDA1.0 (far-red chemigenetic DA, Zheng et al., Science 2025)
- iGluSnFR4f / iGluSnFR4s (Aggarwal et al., Nat Methods 2026)
- ASAP4.4-Kv (positively-tuned voltage GEVI, Zhang et al., Nat Commun 2025)
- PinkyCaMP (mScarlet-based Ca2+, Fink et al., bioRxiv 2024)
- OCaMP / O-GECO2 (orange Ca2+, Aggarwal et al., bioRxiv 2025)

No entries are removed; existing iGABASnFR2 (2021) and GRAB-NE2m (2021) are
kept. A provenance note is written in reports/FP_ENRICHMENT_v3_log.md.
"""

from __future__ import annotations

import io
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "data" / "optical" / "curated" / "atlas_fp_optical_v2_2_curated.csv"
OUT_CURATED = REPO / "data" / "optical" / "curated" / "atlas_fp_optical_v3_curated.csv"
OUT_PROCESSED = REPO / "data" / "processed" / "atlas_fp_optical_v3_curated.csv"
LOG_FILE = REPO / "reports" / "FP_ENRICHMENT_v3_log.md"


def new_entries(existing_max_id: int) -> list[dict]:
    i = existing_max_id
    rows: list[dict] = []

    def row(
        protein: str,
        family: str,
        contrast: float,
        contrast_unit: str,
        ex: float | None,
        em: float | None,
        doi: str,
        pmcid: str,
        license_: str,
        year: int,
        note: str,
        context: str = "in_vivo(neurons)",
        temperature_K: float = 310.0,
        pH: float = 7.4,
        tier: str = "A",
        evidence: str = "primary_paper",
        method: str = "fluorescence",
        assay: str = "imaging",
    ):
        nonlocal i
        i += 1
        return {
            "SystemID": f"FP_{i:04d}",
            "protein_name": protein,
            "family": family,
            "is_biosensor": 1.0,
            "contrast_value": contrast,
            "contrast_unit": contrast_unit,
            "contrast_normalized": contrast,
            "quality_tier": tier,
            "context": context,
            "temperature_K": temperature_K,
            "pH": pH,
            "doi": doi,
            "pmcid": pmcid,
            "license": license_,
            "source": "atlas_fp_v3_enrichment_2024_2026",
            "source_note": note,
            "canonical_name": protein.lower().replace(".", "").replace("-", ""),
            "normalized_name": protein.lower().replace(".", "").replace("-", ""),
            "tier": 1.0,
            "source_refs": doi,
            "license_source": "publisher_page",
            "sd": "",
            "sem": "",
            "ci_low": "",
            "ci_high": "",
            "condition_text": note,
            "evidence_type": evidence,
            "spread_type": "",
            "spread_value": "",
            "method": method,
            "assay": assay,
            "curator": "atlas_v3_release_2026",
            "contrast_quality_tier": tier,
            "excitation_nm": ex,
            "emission_nm": em,
            "stokes_shift_nm": (em - ex) if (ex is not None and em is not None) else "",
            "excitation_missing": ex is None,
            "emission_missing": em is None,
            "contrast_missing": False,
            "source_priority": 1.0,
            "source_name": "Atlas_v3.0_enrichment",
            "year": float(year),
            "name_normalized": protein.lower().replace(".", "").replace("-", ""),
        }

    rows.append(
        row(
            "CaBLAM",
            "Calcium",
            83.0,
            "fold (luminescence max/min, in vitro)",
            None,
            None,
            "10.1038/s41592-025-02972-0",
            "",
            "CC BY (Nature Methods OA)",
            2026,
            "Bioluminescent Ca2+ indicator from SSLuc (Oplophorus gracilirostris); ~83x in vitro, 15-20x in cells; tunable Kd ~50 nM-1 uM.",
            context="in_cellulo(neurons,zebrafish,awake mice)",
            method="bioluminescence",
            assay="BL_imaging",
        )
    )

    rows.append(
        row(
            "HaloDA1.0",
            "Dopamine",
            9.0,
            "deltaF/F (max)",
            646.0,
            670.0,
            "10.1126/science.adt7705",
            "",
            "Science subscription (green OA via bioRxiv 10.1101/2024.12.22.629999)",
            2025,
            "Chemigenetic far-red DA sensor: D1R-cpHaloTag-JF646; ~900 pct deltaF/F; sub-second kinetics; compatible with multiplex neuromodulator imaging.",
            context="in_vivo(mice,zebrafish)",
            method="chemigenetic_fluorescence",
        )
    )

    rows.append(
        row(
            "iGluSnFR4f",
            "Glutamate",
            8.0,
            "deltaF/F (synaptic glutamate, 2P)",
            488.0,
            510.0,
            "10.1038/s41592-025-02965-z",
            "",
            "CC BY (Nature Methods OA)",
            2026,
            "Fourth-generation iGluSnFR with fast deactivation (26 ms); activation <2 ms; 2P imaging in cortex L1-4 and CA1.",
            context="in_vivo(mouse_cortex,CA1)",
        )
    )

    rows.append(
        row(
            "iGluSnFR4s",
            "Glutamate",
            10.0,
            "deltaF/F (synaptic glutamate, 2P)",
            488.0,
            510.0,
            "10.1038/s41592-025-02965-z",
            "",
            "CC BY (Nature Methods OA)",
            2026,
            "Fourth-generation iGluSnFR with slow deactivation (153 ms) for recording from large synapse populations; same paper as iGluSnFR4f.",
            context="in_vivo(mouse_cortex,CA1)",
        )
    )

    rows.append(
        row(
            "ASAP4.4-Kv",
            "Voltage",
            1.8,
            "deltaF/F (per 100 mV depolarization)",
            488.0,
            512.0,
            "10.1038/s41467-025-61774-2",
            "",
            "CC BY-NC-ND (Nat Commun OA)",
            2025,
            "Positively-tuned soma-targeted GEVI (ASAP4.4 fused to Kv2.1); tracks spontaneous and evoked spikes plus subthreshold events in DRG neurons.",
            context="in_vivo(DRG_neurons)",
        )
    )

    rows.append(
        row(
            "PinkyCaMP",
            "Calcium",
            15.1,
            "deltaF/F (max, purified protein)",
            568.0,
            600.0,
            "10.1101/2024.12.16.628673",
            "",
            "CC-BY-NC-ND (bioRxiv preprint)",
            2024,
            "mScarlet-based red GECI; Kd~250 nM; pKa 6.83/4.24; no photoswitching; compatible with optogenetics and 2P imaging.",
            context="in_vivo(awake_mice,hippocampus)",
            tier="B",
        )
    )

    rows.append(
        row(
            "OCaMP",
            "Calcium",
            12.0,
            "deltaF/F (action potential, 2P 1030 nm)",
            545.0,
            565.0,
            "10.1101/2025.07.28.667269",
            "",
            "CC-BY-NC-ND (bioRxiv preprint)",
            2025,
            "Orange GECI from mOrange2 / O-GECO1 scaffold; Kd~130 nM; optimized for 1030 nm 2P excitation; single-AP detection in vivo.",
            context="in_vivo(zebrafish,mouse_cortex)",
            tier="B",
        )
    )

    return rows


def main() -> int:
    df = pd.read_csv(SRC, encoding="utf-8")
    existing_dois = set(df["doi"].dropna().astype(str).str.lower())

    next_id = (
        df["SystemID"]
        .dropna()
        .astype(str)
        .str.extract(r"FP_(\d+)")[0]
        .dropna()
        .astype(int)
        .max()
    )

    rows = new_entries(int(next_id))
    added: list[dict] = []
    skipped: list[str] = []
    for r in rows:
        if r["doi"].lower() in existing_dois:
            skipped.append(r["protein_name"])
        else:
            added.append(r)

    new_df = pd.DataFrame(added, columns=df.columns)
    df_out = pd.concat([df, new_df], ignore_index=True)

    OUT_CURATED.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(OUT_CURATED, index=False, encoding="utf-8")
    df_out.to_csv(OUT_PROCESSED, index=False, encoding="utf-8")

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    log_lines = [
        f"# FP optical enrichment v3.0 log\n",
        f"Generated: {now}\n",
        f"Source: {SRC.relative_to(REPO)}\n",
        f"Target: {OUT_CURATED.relative_to(REPO)}\n\n",
        f"- Total rows (input):  {len(df)}\n",
        f"- Added:               {len(added)}\n",
        f"- Skipped (DOI match): {len(skipped)}\n",
        f"- Total rows (output): {len(df_out)}\n\n",
        "## Added biosensors\n",
    ]
    for r in added:
        log_lines.append(
            f"- `{r['protein_name']}` ({r['family']}, {int(r['year'])}) - DOI {r['doi']} - dF/F {r['contrast_value']}\n"
        )
    if skipped:
        log_lines.append("\n## Skipped (already present)\n")
        for name in skipped:
            log_lines.append(f"- {name}\n")

    with open(LOG_FILE, "w", encoding="utf-8") as fh:
        fh.writelines(log_lines)

    print(f"[OK] Added: {len(added)} / Skipped: {len(skipped)}")
    print(f"[OK] Total rows: {len(df)} -> {len(df_out)} (+{len(df_out) - len(df)})")
    print(f"[OK] Wrote {OUT_CURATED.relative_to(REPO)}")
    print(f"[OK] Wrote {OUT_PROCESSED.relative_to(REPO)}")
    print(f"[OK] Log:   {LOG_FILE.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
