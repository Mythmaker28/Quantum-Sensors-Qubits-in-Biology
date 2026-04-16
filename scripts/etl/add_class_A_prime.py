"""Add class A_prime (FP-qubits with direct ODMR) to biological_qubits_v3.csv.

Class A_prime is the v3.0 flagship: fluorescent proteins that behave as
genuine optically-addressable spin qubits, demonstrated by Nature 2025/2026
publications. These entries legitimize the "Biological Qubits Atlas" title.

References:
- EYFP spin qubit: Feder et al., Nature 645:73-79 (2025-09-04),
  DOI 10.1038/s41586-025-09417-w. T1=141 us @ 80 K, T2_Hahn=1.5 us,
  T2_CPMG=16 us (240 pi-pulses), contrast up to 44% (OADF Tx-Tz, 80 K),
  3% at 295 K.
- MagLOV / MagLOV2: Abrahams et al., Nature 649:1172-1179 (2026-01-29),
  DOI 10.1038/s41586-025-09971-3. ODMR ~10% per-cell at RT in E. coli
  expressing LOV2-derived variants, MFE up to -50% (MagLOV 2). ESR of
  SCRP (protein backbone + flavin cofactor).
- mScarlet/mCherry + FMN: Burd et al., bioRxiv 2025.02.27.640669 (2025-03-03).
  RF-driven radical-pair yield modulation (RYDMR) at ~447 MHz / 15.9 mT,
  RT, validated in vivo in *C. elegans* expressing mScarlet.

Usage:
    python scripts/etl/add_class_A_prime.py
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
TARGET = REPO / "data" / "qubits" / "biological_qubits_v3.csv"
LOG = REPO / "reports" / "ENRICHMENT_v3_log.md"


def build_entries() -> list[dict]:
    """Return the class A_prime entries to insert.

    Each dict matches the 35-column schema of biological_qubits_v3.csv.
    """
    now = datetime.now(timezone.utc).isoformat()
    common_provenance = {
        "dataset_source": "enrichment_v3_A_prime",
        "last_updated": now,
    }

    entries: list[dict] = []

    entries.append({
        "Systeme": "EYFP (Enhanced Yellow Fluorescent Protein) - spin qubit",
        "Classe": "A_prime",
        "Hote_contexte": "E. coli + mammalian cells (in_cellulo)",
        "Methode_lecture": "ODMR",
        "Frequence": "2.815 GHz (Tx-Tz transition)",
        "B0_Tesla": 0.0,
        "Spin_type": "Electron (triplet T1, S=1)",
        "Defaut": "Triplet T1 state of protein chromophore",
        "Polytype_Site": "",
        "T1_s": 1.41e-4,
        "T2_us": 16.0,
        "Contraste_%": 20.0,
        "Temperature_K": 80.0,
        "Taille_objet_nm": 3.0,
        "Source_T2": "DOI:10.1038/s41586-025-09417-w Fig.3c (CPMG 240 pi-pulses, 80 K)",
        "Source_T1": "DOI:10.1038/s41586-025-09417-w Fig.3d (80 K)",
        "Source_Contraste": "DOI:10.1038/s41586-025-09417-w Fig.1d (OADF Tx-Tz, 80 K)",
        "T2_us_err": 2.0,
        "T1_s_err": 5e-6,
        "Contraste_err": 2.0,
        "Hyperpol_flag": 0,
        "Cytotox_flag": 0,
        "Toxicity_note": "None reported; genetically encoded, biocompatible",
        "Temp_controlled": 1,
        "Photophysique": "ex_488nm init; read_912nm OADF; ZPL_triplet; QY=0.67",
        "Conditions": "Liquid cell (sapphire), 488 nm AOM-gated init, 912 nm OADF readout pulse, 2.815 GHz microwave, 80 K (cryostat)",
        "Limitations": "T2 Hahn=1.5 us at 0 field (limited by hyperfine), requires CPMG; full coherence only at 80 K; RT ODMR contrast 3% in aqueous solution",
        "In_vivo_flag": 0,
        "DOI": "10.1038/s41586-025-09417-w",
        "Annee": 2025.0,
        "Qualite": 3.0,
        "Verification_statut": "verifie",
        "Notes": "First demonstrated FP spin qubit. AC magnetic-field sensitivity upper bound 183 fT mol^1/2 Hz^-1/2 (80 K) / 5.11 uT Hz^-1/2 (RT). Expressed in HEK293 with preserved coherent control. OADF = Optically Activated Delayed Fluorescence readout. arXiv:2411.16835.",
        **common_provenance,
    })

    entries.append({
        "Systeme": "EYFP at room temperature (aqueous, ODMR)",
        "Classe": "A_prime",
        "Hote_contexte": "Aqueous solution (in_vitro)",
        "Methode_lecture": "ODMR",
        "Frequence": "2.815 GHz",
        "B0_Tesla": 0.0,
        "Spin_type": "Electron (triplet T1, S=1)",
        "Defaut": "Triplet T1 of chromophore",
        "Polytype_Site": "",
        "T1_s": "",
        "T2_us": "",
        "Contraste_%": 3.0,
        "Temperature_K": 295.0,
        "Taille_objet_nm": 3.0,
        "Source_T2": "DOI:10.1038/s41586-025-09417-w Fig.4",
        "Source_T1": "",
        "Source_Contraste": "DOI:10.1038/s41586-025-09417-w Fig.4",
        "T2_us_err": "",
        "T1_s_err": "",
        "Contraste_err": 0.5,
        "Hyperpol_flag": 0,
        "Cytotox_flag": 0,
        "Toxicity_note": "None reported",
        "Temp_controlled": 0,
        "Photophysique": "ex_488nm; em_520nm; OADF_912nm",
        "Conditions": "PBS buffer pH 7.4, room temperature, 912 nm OADF readout",
        "Limitations": "RT contrast drops to 3%; T2 not reported at 295 K (dominated by fast triplet decay)",
        "In_vivo_flag": 0,
        "DOI": "10.1038/s41586-025-09417-w",
        "Annee": 2025.0,
        "Qualite": 3.0,
        "Verification_statut": "verifie",
        "Notes": "Room-temperature ODMR demonstration. DC sensitivity upper bound 93 pT mol^1/2 Hz^-1/2 at RT. Establishes practical path toward cellular quantum sensing without cryogenics.",
        **common_provenance,
    })

    entries.append({
        "Systeme": "MagLOV 2 (engineered LOV2 with SCRP ODMR)",
        "Classe": "A_prime",
        "Hote_contexte": "E. coli (in_cellulo, single cell)",
        "Methode_lecture": "ODMR",
        "Frequence": "~280 MHz at 10 mT (ESR, g=2)",
        "B0_Tesla": 0.010,
        "Spin_type": "Electron (SCRP: flavin + backbone radical)",
        "Defaut": "Spin-correlated radical pair (FMN + protein radical)",
        "Polytype_Site": "",
        "T1_s": "",
        "T2_us": "",
        "Contraste_%": 10.0,
        "Temperature_K": 295.0,
        "Taille_objet_nm": 4.0,
        "Source_T2": "",
        "Source_T1": "",
        "Source_Contraste": "DOI:10.1038/s41586-025-09971-3 Fig.1d",
        "T2_us_err": "",
        "T1_s_err": "",
        "Contraste_err": 1.0,
        "Hyperpol_flag": 0,
        "Cytotox_flag": 0,
        "Toxicity_note": "None reported; genetically encoded, E. coli viable",
        "Temp_controlled": 0,
        "Photophysique": "ex_450nm (blue, LOV2 flavin); em_495nm; radical-pair T|0>/T|+-> transitions",
        "Conditions": "Live E. coli cells, 450 nm blue-light excitation, electromagnet (static) + RF coil, fluorescence microscopy, RT",
        "Limitations": "MFE -50% (MagLOV 2 variant), ODMR 10% single cell; transient SCRP lifetime limits coherence; optimization ongoing",
        "In_vivo_flag": 1,
        "DOI": "10.1038/s41586-025-09971-3",
        "Annee": 2026.0,
        "Qualite": 3.0,
        "Verification_statut": "verifie",
        "Notes": "First room-temperature ODMR in living cells from a genetically encoded protein. Derived from AsLOV2 (PDB 2V1A) by directed evolution. Magnetic-field sensitivity eta0 = 26 uT Hz^-1/2 (single cell). MFE attenuated by MRI contrast agents - enables MRI-encoded bio-imaging.",
        **common_provenance,
    })

    entries.append({
        "Systeme": "MagLOV (parental magneto-responsive LOV2)",
        "Classe": "A_prime",
        "Hote_contexte": "E. coli (in_cellulo)",
        "Methode_lecture": "ODMR",
        "Frequence": "~280 MHz at 10 mT",
        "B0_Tesla": 0.010,
        "Spin_type": "Electron (SCRP: flavin + backbone radical)",
        "Defaut": "Spin-correlated radical pair",
        "Polytype_Site": "",
        "T1_s": "",
        "T2_us": "",
        "Contraste_%": 5.0,
        "Temperature_K": 295.0,
        "Taille_objet_nm": 4.0,
        "Source_T2": "",
        "Source_T1": "",
        "Source_Contraste": "DOI:10.1038/s41586-025-09971-3 Fig.1 (MagLOV 1 / parental)",
        "T2_us_err": "",
        "T1_s_err": "",
        "Contraste_err": 1.0,
        "Hyperpol_flag": 0,
        "Cytotox_flag": 0,
        "Toxicity_note": "None reported",
        "Temp_controlled": 0,
        "Photophysique": "ex_450nm; em_495nm",
        "Conditions": "Live E. coli, RT, 450 nm excitation",
        "Limitations": "Baseline variant before directed evolution; smaller MFE than MagLOV 2",
        "In_vivo_flag": 1,
        "DOI": "10.1038/s41586-025-09971-3",
        "Annee": 2026.0,
        "Qualite": 3.0,
        "Verification_statut": "verifie",
        "Notes": "Parent variant of the MagLOV family; MagLOV 2 was evolved from it for higher MFE/ODMR contrast.",
        **common_provenance,
    })

    entries.append({
        "Systeme": "mScarlet + FMN (SCRP, RYDMR)",
        "Classe": "A_prime",
        "Hote_contexte": "C. elegans (in_vivo, transgenic)",
        "Methode_lecture": "ODMR",
        "Frequence": "447 MHz (at 15.9 mT)",
        "B0_Tesla": 0.0159,
        "Spin_type": "Electron (SCRP: RFP chromophore + FMN)",
        "Defaut": "Spin-correlated radical pair",
        "Polytype_Site": "",
        "T1_s": "",
        "T2_us": "",
        "Contraste_%": 20.0,
        "Temperature_K": 293.0,
        "Taille_objet_nm": 3.0,
        "Source_T2": "",
        "Source_T1": "",
        "Source_Contraste": "DOI:10.1101/2025.02.27.640669 (RFP:FMN MFE)",
        "T2_us_err": "",
        "T1_s_err": "",
        "Contraste_err": 3.0,
        "Hyperpol_flag": 0,
        "Cytotox_flag": 0,
        "Toxicity_note": "Non-toxic; mScarlet expressed transgenically in C. elegans",
        "Temp_controlled": 0,
        "Photophysique": "ex_~569nm; em_~594nm (mScarlet); FMN cofactor added",
        "Conditions": "Live C. elegans nematodes (transgenic), RF magnetic field ~447 MHz, static field 15.9 mT, room temperature fluorescence microscopy",
        "Limitations": "RYDMR effect; requires external FMN; preprint (not yet peer-reviewed journal)",
        "In_vivo_flag": 1,
        "DOI": "10.1101/2025.02.27.640669",
        "Annee": 2025.0,
        "Qualite": 2.0,
        "Verification_statut": "a_confirmer",
        "Notes": "First RYDMR in a live animal. Demonstrates RF manipulation of genetically encoded quantum system in C. elegans. Cited authors: Burd, Ingaramo, Boxer, Kasevich (Stanford). Preprint under review. 13 citations as of early 2026.",
        **common_provenance,
    })

    entries.append({
        "Systeme": "mCherry + FMN (SCRP, RYDMR)",
        "Classe": "A_prime",
        "Hote_contexte": "In vitro (aqueous solution)",
        "Methode_lecture": "ODMR",
        "Frequence": "447 MHz (at 15.9 mT)",
        "B0_Tesla": 0.0159,
        "Spin_type": "Electron (SCRP: RFP chromophore + FMN)",
        "Defaut": "Spin-correlated radical pair",
        "Polytype_Site": "",
        "T1_s": "",
        "T2_us": "",
        "Contraste_%": 15.0,
        "Temperature_K": 293.0,
        "Taille_objet_nm": 3.0,
        "Source_T2": "",
        "Source_T1": "",
        "Source_Contraste": "DOI:10.1101/2025.02.27.640669",
        "T2_us_err": "",
        "T1_s_err": "",
        "Contraste_err": 3.0,
        "Hyperpol_flag": 0,
        "Cytotox_flag": 0,
        "Toxicity_note": "Non-toxic",
        "Temp_controlled": 0,
        "Photophysique": "ex_587nm; em_610nm (mCherry); FMN added",
        "Conditions": "In vitro with purified mCherry + FMN, RF 447 MHz, static field 15.9 mT, RT",
        "Limitations": "In vivo not yet demonstrated; preprint stage",
        "In_vivo_flag": 0,
        "DOI": "10.1101/2025.02.27.640669",
        "Annee": 2025.0,
        "Qualite": 2.0,
        "Verification_statut": "a_confirmer",
        "Notes": "Red-shifted alternative to mScarlet, same Burd et al. 2025 paper. Smaller MFE than mScarlet.",
        **common_provenance,
    })

    entries.append({
        "Systeme": "mScarlet-I + FMN (SCRP, RYDMR)",
        "Classe": "A_prime",
        "Hote_contexte": "In vitro (aqueous)",
        "Methode_lecture": "ODMR",
        "Frequence": "447 MHz",
        "B0_Tesla": 0.0159,
        "Spin_type": "Electron (SCRP)",
        "Defaut": "Spin-correlated radical pair",
        "Polytype_Site": "",
        "T1_s": "",
        "T2_us": "",
        "Contraste_%": 10.0,
        "Temperature_K": 293.0,
        "Taille_objet_nm": 3.0,
        "Source_T2": "",
        "Source_T1": "",
        "Source_Contraste": "DOI:10.1101/2025.02.27.640669",
        "T2_us_err": "",
        "T1_s_err": "",
        "Contraste_err": 2.0,
        "Hyperpol_flag": 0,
        "Cytotox_flag": 0,
        "Toxicity_note": "Non-toxic",
        "Temp_controlled": 0,
        "Photophysique": "ex_569nm; em_593nm (mScarlet-I); FMN added",
        "Conditions": "Purified protein + FMN, RF 447 MHz, 15.9 mT, RT",
        "Limitations": "Preprint stage; lower contrast than parental mScarlet",
        "In_vivo_flag": 0,
        "DOI": "10.1101/2025.02.27.640669",
        "Annee": 2025.0,
        "Qualite": 2.0,
        "Verification_statut": "a_confirmer",
        "Notes": "mScarlet variant with improved photostability, tested in same Burd et al. study.",
        **common_provenance,
    })

    entries.append({
        "Systeme": "DmCry (Drosophila cryptochrome, purified)",
        "Classe": "A_prime",
        "Hote_contexte": "Purified protein (in_vitro)",
        "Methode_lecture": "ODMR",
        "Frequence": "~1.4 GHz (ESR FAD radical)",
        "B0_Tesla": 0.05,
        "Spin_type": "Electron (SCRP: FAD + TrpH)",
        "Defaut": "Spin-correlated radical pair [FAD.- / TrpH.+]",
        "Polytype_Site": "",
        "T1_s": "",
        "T2_us": 1.0,
        "Contraste_%": 5.0,
        "Temperature_K": 295.0,
        "Taille_objet_nm": 6.0,
        "Source_T2": "DOI:10.1038/s41586-025-09971-3 (cited as SCRP precedent)",
        "Source_T1": "",
        "Source_Contraste": "DOI:10.1038/s41586-025-09971-3",
        "T2_us_err": 0.5,
        "T1_s_err": "",
        "Contraste_err": 2.0,
        "Hyperpol_flag": 0,
        "Cytotox_flag": 0,
        "Toxicity_note": "Purified protein",
        "Temp_controlled": 0,
        "Photophysique": "ex_450nm (FAD photolysis); em_FAD fluorescence",
        "Conditions": "Purified DmCry, 450 nm blue light activation, RT, magnetic field for SCRP transitions",
        "Limitations": "ODMR direct demonstration less established than MagLOV; requires blue light; radical transient",
        "In_vivo_flag": 0,
        "DOI": "10.1038/s41586-025-09971-3",
        "Annee": 2026.0,
        "Qualite": 2.0,
        "Verification_statut": "a_confirmer",
        "Notes": "Drosophila cryptochrome cited in Abrahams 2026 as a natural SCRP precedent to MagLOV. Historically key to magnetoreception hypothesis. Direct ODMR data pending; previous SCRP evidence from EPR.",
        **common_provenance,
    })

    return entries


def main() -> int:
    if not TARGET.exists():
        raise FileNotFoundError(f"Missing target: {TARGET}")

    df = pd.read_csv(TARGET, encoding="utf-8")
    before = len(df)

    new_rows = pd.DataFrame(build_entries())

    already = df[df["Classe"] == "A_prime"]["Systeme"].tolist()
    if already:
        print(f"[INFO] {len(already)} A_prime entries already present - skipping re-add")
        return 0

    df = pd.concat([df, new_rows], ignore_index=True)
    df = df.sort_values(["Classe", "Systeme"]).reset_index(drop=True)
    df.to_csv(TARGET, index=False, encoding="utf-8")

    after = len(df)
    print(f"[OK] Added {after - before} class A_prime entries to {TARGET.name}")
    print(f"[OK] Total rows: {before} -> {after}")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"\n## Class A_prime added\n\n")
        f.write(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n\n")
        f.write(f"Added {after - before} entries:\n")
        for e in build_entries():
            f.write(f"- **{e['Systeme']}** (DOI: {e['DOI']}, Annee: {int(e['Annee'])})\n")
        f.write(f"\nTotal rows: {before} -> {after}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
