#!/usr/bin/env python3
"""Add the remaining 2024-2026 biosensors that were missing from the v3 release.

Targets (from plan phase 4):
    - FR-GECO1a / FR-GECO1c  (Dalangin et al., Nat Commun 2025)
    - NEMOf / NEMOc          (Jia Li et al., Nat Methods 2023)
    - LifeCamp               (Lodder et al., bioRxiv 2025)
    - ASAP6.1 / ASAP6b       (Lee et al., bioRxiv 2024)
    - GRAB-NE2h              (Feng et al., Neuron 2024)

Run:
    python scripts/etl/complete_missing_biosensors_v3.py
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


NEW_ROWS = [
    {
        "protein_name": "FR-GECO1a",
        "family": "Calcium",
        "is_biosensor": 1.0,
        "contrast_value": 6.0,
        "contrast_unit": "fold (deltaF/F0 in vitro)",
        "contrast_normalized": 6.0,
        "quality_tier": "A",
        "context": "in_vitro + in_cellulo (neurons)",
        "temperature_K": 310.0,
        "pH": 7.4,
        "doi": "10.1038/s41467-025-58485-z",
        "pmcid": "PMC11976869",
        "license": "CC BY (Nat Commun OA)",
        "source": "atlas_v3_post_release",
        "source_note": "Far-red GECI based on mKelly1; exc/em ~596/642 nm; Kd ~29 nM; ΔF/F0 ~6.",
        "excitation_nm": 596.0,
        "emission_nm": 642.0,
        "method": "fluorescence",
        "assay": "Ca_imaging",
        "year": 2025.0,
    },
    {
        "protein_name": "FR-GECO1c",
        "family": "Calcium",
        "is_biosensor": 1.0,
        "contrast_value": 18.0,
        "contrast_unit": "fold (deltaF/F0 in vitro)",
        "contrast_normalized": 18.0,
        "quality_tier": "A",
        "context": "in_vitro + in_cellulo (neurons)",
        "temperature_K": 310.0,
        "pH": 7.4,
        "doi": "10.1038/s41467-025-58485-z",
        "pmcid": "PMC11976869",
        "license": "CC BY (Nat Commun OA)",
        "source": "atlas_v3_post_release",
        "source_note": "Far-red GECI based on mKelly2; exc/em ~596/646 nm; Kd ~83 nM; ΔF/F0 ~18.",
        "excitation_nm": 596.0,
        "emission_nm": 646.0,
        "method": "fluorescence",
        "assay": "Ca_imaging",
        "year": 2025.0,
    },
    {
        "protein_name": "NEMOf",
        "family": "Calcium",
        "is_biosensor": 1.0,
        "contrast_value": 58.0,
        "contrast_unit": "fold (deltaF/F0)",
        "contrast_normalized": 58.0,
        "quality_tier": "A",
        "context": "in_cellulo + in_vivo (neurons, zebrafish, mice)",
        "temperature_K": 310.0,
        "pH": 7.4,
        "doi": "10.1038/s41592-023-01852-9",
        "pmcid": "PMC10172123",
        "license": "Springer Nature (publisher)",
        "source": "atlas_v3_post_release",
        "source_note": "NEMO family GECI with fast kinetics; >100-fold dynamic range reported; fast variant.",
        "excitation_nm": 488.0,
        "emission_nm": 515.0,
        "method": "fluorescence",
        "assay": "Ca_imaging",
        "year": 2023.0,
    },
    {
        "protein_name": "NEMOc",
        "family": "Calcium",
        "is_biosensor": 1.0,
        "contrast_value": 80.0,
        "contrast_unit": "fold (deltaF/F0)",
        "contrast_normalized": 80.0,
        "quality_tier": "A",
        "context": "in_cellulo + in_vivo (neurons)",
        "temperature_K": 310.0,
        "pH": 7.4,
        "doi": "10.1038/s41592-023-01852-9",
        "pmcid": "PMC10172123",
        "license": "Springer Nature (publisher)",
        "source": "atlas_v3_post_release",
        "source_note": "NEMO high-contrast variant; dynamic range >100x; large ΔF/F0 for subtle Ca transients.",
        "excitation_nm": 488.0,
        "emission_nm": 515.0,
        "method": "fluorescence",
        "assay": "Ca_imaging",
        "year": 2023.0,
    },
    {
        "protein_name": "LifeCamp",
        "family": "Calcium",
        "is_biosensor": 1.0,
        "contrast_value": 1.0,
        "contrast_unit": "delta_tau_ns (absolute lifetime shift)",
        "contrast_normalized": 1.0,
        "quality_tier": "B",
        "context": "in_cellulo + in_vivo (neurons)",
        "temperature_K": 310.0,
        "pH": 7.2,
        "doi": "10.64898/2025.12.23.696288",
        "pmcid": "",
        "license": "CC BY (bioRxiv preprint)",
        "source": "atlas_v3_post_release",
        "source_note": "High-speed fluorescence lifetime Ca sensor (GCaMP8m + BrUSLEE GFP); >1 ns substrate-dependent lifetime shift; preprint 2025.",
        "excitation_nm": 488.0,
        "emission_nm": 515.0,
        "method": "fluorescence_lifetime",
        "assay": "Ca_imaging_FLIM",
        "year": 2025.0,
    },
    {
        "protein_name": "ASAP6.1",
        "family": "Voltage",
        "is_biosensor": 1.0,
        "contrast_value": 0.50,
        "contrast_unit": "deltaF/F0 per 100 mV",
        "contrast_normalized": 1.50,
        "quality_tier": "B",
        "context": "in_cellulo + in_vivo (neurons)",
        "temperature_K": 310.0,
        "pH": 7.4,
        "doi": "10.1101/2024.06.21.599617",
        "pmcid": "",
        "license": "CC BY (bioRxiv preprint)",
        "source": "atlas_v3_post_release",
        "source_note": "Positively tuned GEVI (ASAP4 template); faster onset; AP response reaches 50% ΔF/F0 for 2 ms FWHM waveforms.",
        "excitation_nm": 488.0,
        "emission_nm": 510.0,
        "method": "fluorescence",
        "assay": "voltage_imaging",
        "year": 2024.0,
    },
    {
        "protein_name": "ASAP6b",
        "family": "Voltage",
        "is_biosensor": 1.0,
        "contrast_value": 0.33,
        "contrast_unit": "deltaF/F0 per 100 mV",
        "contrast_normalized": 1.33,
        "quality_tier": "B",
        "context": "in_cellulo + ex_vivo (retina)",
        "temperature_K": 310.0,
        "pH": 7.4,
        "doi": "10.1101/2024.06.21.599617",
        "pmcid": "",
        "license": "CC BY (bioRxiv preprint)",
        "source": "atlas_v3_post_release",
        "source_note": "Brighter ASAP6 variant (ASAP6.2 rebranded); operates at higher molecular brightness in physiological conditions.",
        "excitation_nm": 488.0,
        "emission_nm": 510.0,
        "method": "fluorescence",
        "assay": "voltage_imaging",
        "year": 2024.0,
    },
    {
        "protein_name": "GRAB-NE2h",
        "family": "Neurotransmitter (catecholamine)",
        "is_biosensor": 1.0,
        "contrast_value": 4.15,
        "contrast_unit": "fold (peak deltaF/F0)",
        "contrast_normalized": 4.15,
        "quality_tier": "A",
        "context": "in_vivo (mice, locus coeruleus + hypothalamus)",
        "temperature_K": 310.0,
        "pH": 7.4,
        "doi": "10.1016/j.neuron.2024.03.001",
        "pmcid": "PMC11364517",
        "license": "Elsevier (publisher)",
        "source": "atlas_v3_post_release",
        "source_note": "Second-generation GPCR-based NE sensor; high-affinity variant (nanomolar); 4x stronger response vs NE1h; published Neuron 2024.",
        "excitation_nm": 488.0,
        "emission_nm": 515.0,
        "method": "fluorescence",
        "assay": "neurotransmitter_imaging",
        "year": 2024.0,
    },
]


def main() -> int:
    path = Path("data/processed/atlas_fp_optical_v3_curated.csv")
    if not path.exists():
        print(f"[ERROR] Atlas CSV not found: {path}")
        return 1

    df = pd.read_csv(path)
    max_id = df["SystemID"].str.extract(r"FP_(\d+)")[0].astype(int).max()
    print(f"[*] Current rows: {len(df)} | max SystemID: FP_{max_id:04d}")

    existing_names_lower = set(df["protein_name"].astype(str).str.lower().str.strip())
    to_add = []
    next_id = max_id + 1
    for row in NEW_ROWS:
        if row["protein_name"].lower() in existing_names_lower:
            print(f"  - skip (already present): {row['protein_name']}")
            continue
        row["SystemID"] = f"FP_{next_id:04d}"
        row["curator"] = "atlas_v3_release_2026"
        row["canonical_name"] = row["protein_name"].lower()
        row["normalized_name"] = row["protein_name"].lower()
        row["name_normalized"] = row["protein_name"].lower().replace("-", "").replace(".", "")
        row["tier"] = 1.0 if row["quality_tier"] == "A" else 2.0
        row["source_refs"] = row["doi"]
        row["source_name"] = "Atlas_v3.0_post_release"
        row["source_priority"] = 1.0 if row["quality_tier"] == "A" else 2.0
        row["excitation_missing"] = pd.isna(row.get("excitation_nm"))
        row["emission_missing"] = pd.isna(row.get("emission_nm"))
        row["contrast_missing"] = False
        row["evidence_type"] = "primary_paper"
        if row.get("excitation_nm") and row.get("emission_nm"):
            row["stokes_shift_nm"] = row["emission_nm"] - row["excitation_nm"]
        row["contrast_quality_tier"] = row["quality_tier"]
        row["license_source"] = "publisher_page"
        to_add.append(row)
        next_id += 1
        print(f"  + add {row['SystemID']}: {row['protein_name']} ({row['year']:.0f})")

    if not to_add:
        print("[*] Nothing to add.")
        return 0

    new_df = pd.concat([df, pd.DataFrame(to_add)], ignore_index=True)
    new_df.to_csv(path, index=False)
    print(f"[OK] Wrote {len(new_df)} rows to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
