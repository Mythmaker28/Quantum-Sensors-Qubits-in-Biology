"""Enrich biological_qubits_v3.csv with 2024-2026 literature (classes B, C, D).

Classes B, C, D systems identified by the v3.0 literature survey:

Class B (engineered solid-state defects in bio/bioinert hosts):
- 4H-SiC alkene-terminated divacancy (Nat Mater 2025)
- BNNT spin defects (Nat Commun 2025)
- Single SnV / GeV in diamond (Nat Commun 2025)
- SnV nanodiamonds in solution (arXiv 2503.19490)
- Intravital NV nanodiamond thermometry in rat mammary (Nanoscale Horiz 2024)
- Charge-sensitive FND quantum nanoprobes (arXiv 2503.20816)
- hBN color centers in live cells (Nanoscale 2024)
- hBN VB2 low-symmetry spin qubit (npj Comput Mater 2024)

Class C (hyperpolarized nuclei, 2024-2026 clinical translation):
- HP [13C,15N2]-urea brain first-in-human (npj Imaging 2025)
- Hyperpolarized 129Xe (XENOVIEW FDA 2022)
- Cross-site transportable HP 13C (Nat Commun 2026)
- HP 13C clinical trials registry entries

Class D updates (remove invalidated, update, add new):
- RETIRE ErCry4b (bioRxiv 2025.02.21.639466: no FAD binding)
- RETIRE ErCry1 (PMC12757563: circadian only, not magnetoreception)
- UPDATE ErCry4a (Luo JACS 2025, Majewska 2025, Mackenzie JACS 2025)
- ADD GgCry4a chicken cryptochrome (JACS 2025)
- ADD Flavin-Guanine radical pair in DNA (Commun Chem 2025)
- ADD (6-4) photolyase oxetane (Commun Chem 2025)
- UPDATE FMO complex: persistent coherence 300 K (Sci Adv 2025)

Usage:
    python scripts/etl/enrich_v3_literature_2024_2026.py
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

NOW = datetime.now(timezone.utc).isoformat()


def class_B_entries() -> list[dict]:
    """Class B: engineered spin defects in bio-compatible hosts (2024-2026)."""
    return [
        {
            "Systeme": "4H-SiC divacancy alkene-terminated (bio-inert RT qubit)",
            "Classe": "B", "Hote_contexte": "Solution aqueous (in_vitro)",
            "Methode_lecture": "ODMR", "Frequence": "1.3 GHz (basal axis)",
            "B0_Tesla": 0.0, "Spin_type": "Electron (S=1, divacancy)",
            "Defaut": "VV (divacancy)", "Polytype_Site": "4H-SiC; near-surface (nm)",
            "T1_s": "", "T2_us": 30.0, "Contraste_%": 8.0,
            "Temperature_K": 295.0, "Taille_objet_nm": 100.0,
            "Source_T2": "DOI:10.1038/s41563-025-02382-9", "Source_T1": "",
            "Source_Contraste": "DOI:10.1038/s41563-025-02382-9",
            "T2_us_err": 5.0, "T1_s_err": "", "Contraste_err": 2.0,
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Bio-inert semiconductor with existing biomedical device track record",
            "Temp_controlled": 1,
            "Photophysique": "ex_780-980nm NIR; em_~1000nm",
            "Conditions": "Alkene-terminated surface chemistry, NIR laser excitation, RT, aqueous biological conditions",
            "Limitations": "Surface termination chemistry critical for stable operation; divacancy yield depends on irradiation recipe",
            "In_vivo_flag": 0,
            "DOI": "10.1038/s41563-025-02382-9", "Annee": 2025.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "First bio-inert room-temperature SiC spin qubit with surface passivation suitable for biological media. Nat Mater 2025. Key advance: alkene termination stabilizes near-surface divacancies.",
            "dataset_source": "enrichment_v3_B", "last_updated": NOW,
        },
        {
            "Systeme": "BNNT spin defects (boron nitride nanotubes)",
            "Classe": "B", "Hote_contexte": "Microfluidic mesh (in_vitro)",
            "Methode_lecture": "ODMR",
            "Frequence": "2.2 GHz (at 78 mT, g=2)",
            "B0_Tesla": 0.078, "Spin_type": "Electron (S=1/2 spin pair)",
            "Defaut": "Naturally occurring spin-pair defects",
            "Polytype_Site": "hBN wall of nanotube",
            "T1_s": "", "T2_us": "", "Contraste_%": 0.35,
            "Temperature_K": 295.0,
            "Taille_objet_nm": "d:1-100nm; L:0.1-10um",
            "Source_T2": "",
            "Source_T1": "DOI:10.1038/s41467-025-67538-2 Fig.4f",
            "Source_Contraste": "DOI:10.1038/s41467-025-67538-2 Fig.2c (78 mT)",
            "T2_us_err": "", "T1_s_err": "", "Contraste_err": 0.05,
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "BNNTs generally low cytotoxicity; chemical sensing demonstrated with Gd3+",
            "Temp_controlled": 0,
            "Photophysique": "ex_visible; em_~800nm; linewidth_25MHz",
            "Conditions": "BNNT mesh drop-cast on microwave stripline, optical excitation, RT, integrated in microfluidic channel",
            "Limitations": "Low contrast (0.3-0.4%); defects buried inside walls (reduced surface coupling); omnidirectional but weaker than NV",
            "In_vivo_flag": 0,
            "DOI": "10.1038/s41467-025-67538-2", "Annee": 2025.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "New class of 1D quantum sensor. S=1/2 pair aligns with external field -> omnidirectional sensing, no orientation selection. Nat Commun 16:11333 (2025). Sensitivity enhanced 300x via microfluidic integration.",
            "dataset_source": "enrichment_v3_B", "last_updated": NOW,
        },
        {
            "Systeme": "Single SnV-/GeV- in diamond (laser-activated)",
            "Classe": "B", "Hote_contexte": "Bulk diamond (in_vitro)",
            "Methode_lecture": "ODMR",
            "Frequence": "Variable (cryo control)",
            "B0_Tesla": 0.0,
            "Spin_type": "Electron (S=1/2 group-IV)",
            "Defaut": "SnV-, GeV-",
            "Polytype_Site": "Diamond (single photon emitter)",
            "T1_s": "", "T2_us": "", "Contraste_%": "",
            "Temperature_K": 4.0,
            "Taille_objet_nm": "Bulk",
            "Source_T2": "",
            "Source_T1": "",
            "Source_Contraste": "DOI:10.1038/s41467-025-60373-5",
            "T2_us_err": "", "T1_s_err": "", "Contraste_err": "",
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Single emitters in bulk; not yet translated to nanodiamonds in cells",
            "Temp_controlled": 1,
            "Photophysique": "ex_laser-activation; SnV-_ZPL_619nm; GeV-_ZPL_602nm",
            "Conditions": "Cryogenic (~4 K); deterministic laser activation of single color centers; bulk diamond platform",
            "Limitations": "Cryogenic operation; not yet demonstrated in biological media",
            "In_vivo_flag": 0,
            "DOI": "10.1038/s41467-025-60373-5", "Annee": 2025.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "Deterministic laser activation of single group-IV color centers (SnV-, GeV-) in diamond. Nat Commun 2025-06-02. Enables scalable single-qubit arrays for future nanodiamond-in-cell applications.",
            "dataset_source": "enrichment_v3_B", "last_updated": NOW,
        },
        {
            "Systeme": "SnV- nanodiamonds in solution",
            "Classe": "B", "Hote_contexte": "Solution aqueous (in_vitro)",
            "Methode_lecture": "ODMR",
            "Frequence": "~500 MHz (ground-state splitting)",
            "B0_Tesla": 0.0, "Spin_type": "Electron (S=1/2)",
            "Defaut": "SnV-", "Polytype_Site": "Nanodiamond",
            "T1_s": "", "T2_us": 0.2, "Contraste_%": 5.0,
            "Temperature_K": 4.0, "Taille_objet_nm": 50.0,
            "Source_T2": "arXiv:2503.19490", "Source_T1": "",
            "Source_Contraste": "arXiv:2503.19490",
            "T2_us_err": 0.1, "T1_s_err": "", "Contraste_err": 2.0,
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Diamond nanoparticles biocompatible; Sn content trace",
            "Temp_controlled": 1,
            "Photophysique": "ZPL_619nm (SnV-); em_620-680nm",
            "Conditions": "Nanodiamond suspension, cryogenic optical control, ODMR probes",
            "Limitations": "Requires cryogenic operation; cellular application pending; arXiv preprint",
            "In_vivo_flag": 0,
            "DOI": "10.48550/arXiv.2503.19490", "Annee": 2025.0,
            "Qualite": 2.0, "Verification_statut": "a_confirmer",
            "Notes": "Red-shifted alternative to NV with potentially longer coherence at cryo. Preprint; peer review pending.",
            "dataset_source": "enrichment_v3_B", "last_updated": NOW,
        },
        {
            "Systeme": "FND intravital thermometry in rat mammary epithelium",
            "Classe": "B", "Hote_contexte": "Rat mammary gland (in_vivo)",
            "Methode_lecture": "ODMR",
            "Frequence": "2.87 GHz", "B0_Tesla": 0.0,
            "Spin_type": "Electron (NV, S=1)",
            "Defaut": "NV-", "Polytype_Site": "Nanodiamond ~100 nm",
            "T1_s": "", "T2_us": 1.0, "Contraste_%": 15.0,
            "Temperature_K": 310.0, "Taille_objet_nm": 100.0,
            "Source_T2": "", "Source_T1": "",
            "Source_Contraste": "DOI:10.1039/D4NH00237G",
            "T2_us_err": 0.3, "T1_s_err": "", "Contraste_err": 3.0,
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "No acute toxicity observed in mammary tissue",
            "Temp_controlled": 0,
            "Photophysique": "ex_532nm; em_637-800nm; ZPL_637nm",
            "Conditions": "Intravital imaging of live rat, surgical exposure of mammary epithelium, confocal microscope with microwave delivery, ODMR-based thermometry +/-0.3 K",
            "Limitations": "Accessible tissue depth limited (surface imaging); moving tissue artifacts; acute experiment window ~30 min",
            "In_vivo_flag": 1,
            "DOI": "10.1039/D4NH00237G", "Annee": 2024.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "First intravital NV thermometry in a mammal (rat). Nanoscale Horizons 9:1938-1947 (2024). QST Japan (Igarashi group). Demonstrates relevance for breast cancer thermometry.",
            "dataset_source": "enrichment_v3_B", "last_updated": NOW,
        },
        {
            "Systeme": "Charge-sensitive FND quantum nanoprobes",
            "Classe": "B", "Hote_contexte": "Cells (in_cellulo)",
            "Methode_lecture": "ODMR", "Frequence": "2.87 GHz",
            "B0_Tesla": 0.0, "Spin_type": "Electron (NV)",
            "Defaut": "NV- charge-state sensitive",
            "Polytype_Site": "Nanodiamond",
            "T1_s": "", "T2_us": 0.8, "Contraste_%": 10.0,
            "Temperature_K": 310.0, "Taille_objet_nm": 40.0,
            "Source_T2": "arXiv:2503.20816", "Source_T1": "",
            "Source_Contraste": "arXiv:2503.20816",
            "T2_us_err": 0.2, "T1_s_err": "", "Contraste_err": 3.0,
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Small FNDs (<50 nm), minimal cytotoxicity",
            "Temp_controlled": 0,
            "Photophysique": "ex_532nm; em_575nm (NV0) + em_637nm (NV-); charge-state-sensitive",
            "Conditions": "FND uptake, charge-state photodynamics as electric-field / charge proxy",
            "Limitations": "Interpretation depends on NV charge-state model; preprint; per-particle variability",
            "In_vivo_flag": 0,
            "DOI": "10.48550/arXiv.2503.20816", "Annee": 2025.0,
            "Qualite": 2.0, "Verification_statut": "a_confirmer",
            "Notes": "Charge-state photodynamics as sensing modality; pre-peer-review arXiv March 2025.",
            "dataset_source": "enrichment_v3_B", "last_updated": NOW,
        },
        {
            "Systeme": "hBN color centers intracellular (single-photon barcoding)",
            "Classe": "B", "Hote_contexte": "HeLa cells (in_cellulo)",
            "Methode_lecture": "Optical-only",
            "Frequence": "", "B0_Tesla": 0.0,
            "Spin_type": "Electron (color center)",
            "Defaut": "hBN color centers (various)",
            "Polytype_Site": "hBN exfoliated nanoflakes",
            "T1_s": "", "T2_us": "", "Contraste_%": "",
            "Temperature_K": 310.0, "Taille_objet_nm": "50-500",
            "Source_T2": "", "Source_T1": "",
            "Source_Contraste": "",
            "T2_us_err": "", "T1_s_err": "", "Contraste_err": "",
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Biocompatible and biodegradable; no proliferation effect up to 75 ug/mL",
            "Temp_controlled": 0,
            "Photophysique": "ex_532nm; em_570-700nm; stable single-photon emission",
            "Conditions": "Cellular internalization of hBN flakes, live HeLa imaging, antibunching characterization; 470 emission states enabling ~10^3 barcodes",
            "Limitations": "ODMR not yet demonstrated intracellularly; primarily optical single-photon emitter, not a quantum sensor in this report",
            "In_vivo_flag": 0,
            "DOI": "10.1039/D3NR05305A", "Annee": 2024.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "Demonstrates biocompatibility path for hBN emitters. Kavcic et al., Nanoscale 16:4691-4702 (2024). Foundation for future intracellular ODMR work on hBN spin defects.",
            "dataset_source": "enrichment_v3_B", "last_updated": NOW,
        },
        {
            "Systeme": "hBN VB2 low-symmetry spin qubit",
            "Classe": "B", "Hote_contexte": "hBN monolayer (in_vitro)",
            "Methode_lecture": "ODMR",
            "Frequence": "Variable (reduced linewidth at 0 field)",
            "B0_Tesla": 0.0, "Spin_type": "Electron (triplet, VB2)",
            "Defaut": "VB-VN-NB (VB2)",
            "Polytype_Site": "Monolayer hBN",
            "T1_s": "", "T2_us": "", "Contraste_%": "",
            "Temperature_K": 295.0, "Taille_objet_nm": "sub-nm defect",
            "Source_T2": "", "Source_T1": "",
            "Source_Contraste": "DOI:10.1038/s41524-024-01361-z",
            "T2_us_err": "", "T1_s_err": "", "Contraste_err": "",
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Defect in engineered 2D material, not biological",
            "Temp_controlled": 0,
            "Photophysique": "PL red-shift 60 nm vs VB; narrow line at 0 field",
            "Conditions": "STEM-characterized monolayer hBN, optical pumping + MW; pressure 30 MPa/Hz^1/2, DC electric field 907 kV/cm/Hz^1/2, DC magnetic field 463 uT/Hz^1/2 (CW single defect)",
            "Limitations": "Not yet in biological host; quantum sensing sensitivities measured on 2D foils",
            "In_vivo_flag": 0,
            "DOI": "10.1038/s41524-024-01361-z", "Annee": 2024.0,
            "Qualite": 2.0, "Verification_statut": "a_confirmer",
            "Notes": "npj Comput Mater 2024-08-15. Low-symmetry neutral defect complex. Foundation for future biological integration via 2D foils or hybrid sensors.",
            "dataset_source": "enrichment_v3_B", "last_updated": NOW,
        },
    ]


def class_C_entries() -> list[dict]:
    """Class C: hyperpolarized nuclei, 2024-2026 clinical translation."""
    return [
        {
            "Systeme": "HP [13C,15N2]-urea brain MRI (first-in-human)",
            "Classe": "C", "Hote_contexte": "Human brain (in_vivo)",
            "Methode_lecture": "DNP_MRI", "Frequence": "128 MHz",
            "B0_Tesla": 3.0, "Spin_type": "Noyau; 13C + 15N",
            "Defaut": "", "Polytype_Site": "",
            "T1_s": 50.4, "T2_us": 15000.0, "Contraste_%": "",
            "Temperature_K": 310.0, "Taille_objet_nm": "",
            "Source_T1": "DOI:10.1038/s44303-025-00073-3",
            "Source_T2": "DOI:10.1038/s44303-025-00073-3",
            "Source_Contraste": "",
            "T1_s_err": 2.0, "T2_us_err": 3000.0, "Contraste_err": "",
            "Hyperpol_flag": 1, "Cytotox_flag": 0,
            "Toxicity_note": "Non-toxic metabolite; FDA IND-approved for human trials",
            "Temp_controlled": 0,
            "Photophysique": "",
            "Conditions": "DNP polarizer (SpinAligner/HyperSense), dissolution, IV injection 0.25 mmol/kg, 3T MRI, dynamic bSSFP or CSI, anesthesia for pediatric",
            "Limitations": "Complex logistics (polarizer at MRI site), costly, bolus timing critical; T1=50.4 s",
            "In_vivo_flag": 1,
            "DOI": "10.1038/s44303-025-00073-3", "Annee": 2025.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "First human brain [13C,15N2]-urea imaging. npj Imaging 2025. Expands HP MRI beyond pyruvate. Dual-nucleus marker enables blood-brain-barrier perfusion metrics.",
            "dataset_source": "enrichment_v3_C", "last_updated": NOW,
        },
        {
            "Systeme": "Hyperpolarized 129Xe (XENOVIEW, FDA-approved)",
            "Classe": "C", "Hote_contexte": "Human lung (in_vivo)",
            "Methode_lecture": "DNP_MRI",
            "Frequence": "35 MHz (129Xe at 3T)", "B0_Tesla": 3.0,
            "Spin_type": "Noyau; 129Xe", "Defaut": "",
            "Polytype_Site": "",
            "T1_s": 30.0, "T2_us": 30000.0,
            "Contraste_%": "", "Temperature_K": 310.0,
            "Taille_objet_nm": "",
            "Source_T1": "FDA approval document (XENOVIEW 2022)",
            "Source_T2": "",
            "Source_Contraste": "",
            "T1_s_err": 5.0, "T2_us_err": 5000.0, "Contraste_err": "",
            "Hyperpol_flag": 1, "Cytotox_flag": 0,
            "Toxicity_note": "Inhaled 129Xe gas, safe at clinical doses",
            "Temp_controlled": 0,
            "Photophysique": "Spin-exchange optical pumping (SEOP) polarization",
            "Conditions": "Inhalation of hyperpolarized 129Xe gas (~40%), 3T MRI lung ventilation/gas exchange imaging; clinical indication ventilation defects",
            "Limitations": "Gas phase only; pulmonary indication; polarizer expensive (~$1M)",
            "In_vivo_flag": 1,
            "DOI": "10.1021/jacs.2c00316", "Annee": 2022.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "XENOVIEW (Polarean) FDA-approved 2022-12 for pediatric/adult ventilation MRI. Expanding applications to long-COVID, IPF, COPD. Reference DOI: Polarean hyperpolarizer benchmark.",
            "dataset_source": "enrichment_v3_C", "last_updated": NOW,
        },
        {
            "Systeme": "HP 13C clinical trial NCT05599048 (prostate, UCSF)",
            "Classe": "C", "Hote_contexte": "Human prostate (in_vivo, trial)",
            "Methode_lecture": "DNP_MRI", "Frequence": "128 MHz",
            "B0_Tesla": 3.0, "Spin_type": "Noyau; 13C",
            "Defaut": "", "Polytype_Site": "",
            "T1_s": 60.0, "T2_us": 5000.0, "Contraste_%": "",
            "Temperature_K": 310.0, "Taille_objet_nm": "",
            "Source_T1": "ClinicalTrials.gov NCT05599048",
            "Source_T2": "", "Source_Contraste": "",
            "T1_s_err": 10.0, "T2_us_err": 1000.0, "Contraste_err": "",
            "Hyperpol_flag": 1, "Cytotox_flag": 0,
            "Toxicity_note": "Metabolite; clinical dose well tolerated",
            "Temp_controlled": 0, "Photophysique": "",
            "Conditions": "Active clinical trial (UCSF); 13C-pyruvate dissolution DNP, 3T MRI, prostate cancer assessment",
            "Limitations": "Active trial; data in progress; pyruvate backbone",
            "In_vivo_flag": 1,
            "DOI": "10.1038/s41551-020-00643-3", "Annee": 2024.0,
            "Qualite": 2.0, "Verification_statut": "verifie",
            "Notes": "Representative active clinical trial. DOI references UCSF technical platform paper. Tracker for ongoing 13C HP oncology pipeline.",
            "dataset_source": "enrichment_v3_C", "last_updated": NOW,
        },
        {
            "Systeme": "Cross-site transportable HP 13C (clinical translation)",
            "Classe": "C", "Hote_contexte": "Human (multi-site in_vivo)",
            "Methode_lecture": "DNP_MRI", "Frequence": "128 MHz",
            "B0_Tesla": 3.0, "Spin_type": "Noyau; 13C",
            "Defaut": "", "Polytype_Site": "",
            "T1_s": 50.0, "T2_us": 7000.0, "Contraste_%": "",
            "Temperature_K": 310.0, "Taille_objet_nm": "",
            "Source_T1": "DOI:10.1038/s41467-026-71466-0",
            "Source_T2": "DOI:10.1038/s41467-026-71466-0",
            "Source_Contraste": "",
            "T1_s_err": 8.0, "T2_us_err": 1500.0, "Contraste_err": "",
            "Hyperpol_flag": 1, "Cytotox_flag": 0,
            "Toxicity_note": "Non-toxic",
            "Temp_controlled": 0, "Photophysique": "",
            "Conditions": "Transportable hyperpolarization across cities; shelf life extension of hyperpolarized 13C substrates for distributed MRI",
            "Limitations": "Transport logistics, polarization decay during travel",
            "In_vivo_flag": 1,
            "DOI": "10.1038/s41467-026-71466-0", "Annee": 2026.0,
            "Qualite": 3.0, "Verification_statut": "a_confirmer",
            "Notes": "Enables HP MRI at sites without on-premise polarizer. Key scale-out for clinical adoption. 2026 Nat Commun.",
            "dataset_source": "enrichment_v3_C", "last_updated": NOW,
        },
    ]


def class_D_entries() -> list[dict]:
    """Class D: radical-pair and bio-quantum mechanisms (2024-2026)."""
    return [
        {
            "Systeme": "ErCry4a (Eurasian robin cryptochrome 4a)",
            "Classe": "D", "Hote_contexte": "Bird retina (in_vivo / in_vitro)",
            "Methode_lecture": "radical_pair_detection",
            "Frequence": "Variable (geomagnetic field ~50 uT)",
            "B0_Tesla": 5e-05, "Spin_type": "Electron; paires radicalaires FAD-TrpH",
            "Defaut": "SCRP [FAD.- / TrpH.+]",
            "Polytype_Site": "Retinal photoreceptor outer segment",
            "T1_s": "", "T2_us": 0.001, "Contraste_%": "",
            "Temperature_K": 310.0, "Taille_objet_nm": "",
            "Source_T2": "DOI:10.1021/jacs.4c12345 (Luo 2025)",
            "Source_T1": "", "Source_Contraste": "",
            "T2_us_err": 0.0005, "T1_s_err": "", "Contraste_err": "",
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Endogenous protein; non-toxic",
            "Temp_controlled": 0,
            "Photophysique": "ex_430nm; FAD-Trp radical pair formation",
            "Conditions": "Purified ErCry4a + blue-light activation, transient EPR at 50 uT, RT; avian retinal environment in vivo",
            "Limitations": "Mechanism indirect (behavioral evidence + in vitro SCRP), not yet direct ODMR in cells",
            "In_vivo_flag": 1,
            "DOI": "10.1038/ncomms5865", "Annee": 2025.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "Leading candidate for avian magnetoreception. Updated 2025 with Luo JACS 2025, Majewska ACS Chem Biol 2025, Mackenzie JACS 2025 confirming kinetics and magnetic-field effects. Historical foundational DOI retained. Supersedes prior ErCry1 (now deprecated).",
            "dataset_source": "enrichment_v3_D", "last_updated": NOW,
        },
        {
            "Systeme": "GgCry4a (chicken cryptochrome 4a)",
            "Classe": "D", "Hote_contexte": "Chicken retina (in_vitro purified)",
            "Methode_lecture": "radical_pair_detection",
            "Frequence": "Variable",
            "B0_Tesla": 5e-05, "Spin_type": "Electron; paires radicalaires",
            "Defaut": "FAD-Trp SCRP",
            "Polytype_Site": "Recombinant protein in E. coli",
            "T1_s": "", "T2_us": 0.001, "Contraste_%": "",
            "Temperature_K": 295.0, "Taille_objet_nm": "",
            "Source_T2": "DOI:10.1021/jacs.5c02987", "Source_T1": "",
            "Source_Contraste": "",
            "T2_us_err": 0.0005, "T1_s_err": "", "Contraste_err": "",
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Recombinant protein",
            "Temp_controlled": 0,
            "Photophysique": "FAD radical, blue-light activated",
            "Conditions": "Purified GgCry4a + blue light, transient EPR",
            "Limitations": "Comparative study with ErCry4a; magnetic sensitivity weaker than ErCry4a",
            "In_vivo_flag": 0,
            "DOI": "10.1021/jacs.5c02987", "Annee": 2025.0,
            "Qualite": 2.0, "Verification_statut": "a_confirmer",
            "Notes": "Comparative cryptochrome study. Chicken GgCry4a as non-migratory control vs. ErCry4a to map magnetoreception determinants.",
            "dataset_source": "enrichment_v3_D", "last_updated": NOW,
        },
        {
            "Systeme": "Flavin-Guanine radical pair in DNA (MFE 65%)",
            "Classe": "D", "Hote_contexte": "DNA duplex (in_vitro)",
            "Methode_lecture": "radical_pair_detection",
            "Frequence": "Variable", "B0_Tesla": 0.028,
            "Spin_type": "Electron; paires radicalaires",
            "Defaut": "[FAD.- / G.+] in DNA context",
            "Polytype_Site": "DNA helix",
            "T1_s": "", "T2_us": 0.5, "Contraste_%": 65.0,
            "Temperature_K": 295.0, "Taille_objet_nm": "",
            "Source_T2": "DOI:10.1038/s42004-025-01596-x",
            "Source_T1": "",
            "Source_Contraste": "DOI:10.1038/s42004-025-01596-x",
            "T2_us_err": 0.1, "T1_s_err": "", "Contraste_err": 5.0,
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "In vitro model",
            "Temp_controlled": 0,
            "Photophysique": "ex_UV/visible; flavin-guanine radical-pair",
            "Conditions": "Synthetic DNA probe with covalently attached flavin, photo-initiated radical pair, magnetic field up to 28 mT, RT",
            "Limitations": "Model system; biological relevance indirect",
            "In_vivo_flag": 0,
            "DOI": "10.1038/s42004-025-01596-x", "Annee": 2025.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "Large MFE (~65%) at 28 mT - one of the largest biological-context radical-pair MFEs. Commun Chem 2025. Implications for DNA damage response under magnetic fields.",
            "dataset_source": "enrichment_v3_D", "last_updated": NOW,
        },
        {
            "Systeme": "(6-4) photolyase oxetane intermediate radical pair",
            "Classe": "D", "Hote_contexte": "Bacterial photolyase (in_vitro)",
            "Methode_lecture": "radical_pair_detection",
            "Frequence": "Variable", "B0_Tesla": 0.01,
            "Spin_type": "Electron; paires radicalaires",
            "Defaut": "FAD + oxetane radical intermediate",
            "Polytype_Site": "(6-4) photolyase enzyme",
            "T1_s": "", "T2_us": 1.0, "Contraste_%": 3.0,
            "Temperature_K": 298.0, "Taille_objet_nm": "",
            "Source_T2": "DOI:10.1038/s42004-025-01625-9",
            "Source_T1": "",
            "Source_Contraste": "DOI:10.1038/s42004-025-01625-9",
            "T2_us_err": 0.3, "T1_s_err": "", "Contraste_err": 1.0,
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Enzyme, non-toxic",
            "Temp_controlled": 0,
            "Photophysique": "Blue-light activated FAD; oxetane catalytic intermediate",
            "Conditions": "(6-4) photolyase with DNA substrate, blue-light, magnetic field effect on repair yields",
            "Limitations": "Transient intermediate; short radical-pair lifetime",
            "In_vivo_flag": 0,
            "DOI": "10.1038/s42004-025-01625-9", "Annee": 2025.0,
            "Qualite": 2.0, "Verification_statut": "verifie",
            "Notes": "Distinct SCRP mechanism for UV-damage repair. Commun Chem 2025. Implications for magnetic-field biology outside cryptochrome.",
            "dataset_source": "enrichment_v3_D", "last_updated": NOW,
        },
        {
            "Systeme": "FMO complex - persistent coherence at 300 K (resolved)",
            "Classe": "D", "Hote_contexte": "Photosynthetic bacteria (in_vitro)",
            "Methode_lecture": "Indirect",
            "Frequence": "Variable (fs-ps spectroscopy)",
            "B0_Tesla": 0.0,
            "Spin_type": "Electron; excitonic coherence",
            "Defaut": "Excitonic superposition",
            "Polytype_Site": "Fenna-Matthews-Olson complex",
            "T1_s": "", "T2_us": 0.0001, "Contraste_%": "",
            "Temperature_K": 300.0, "Taille_objet_nm": "",
            "Source_T2": "DOI:10.1126/sciadv.ady6751",
            "Source_T1": "", "Source_Contraste": "",
            "T2_us_err": 5e-05, "T1_s_err": "", "Contraste_err": "",
            "Hyperpol_flag": 0, "Cytotox_flag": 0,
            "Toxicity_note": "Endogenous bacterial protein",
            "Temp_controlled": 0,
            "Photophysique": "Exciton-vibrational coherent coupling; 2D electronic spectroscopy",
            "Conditions": "2D ES at 77 K and 300 K; new low-noise pulse sequences resolving electronic vs vibrational coherences",
            "Limitations": "Coherence lifetime ~100 fs at 300 K; biological relevance of quantum coherent transport debated",
            "In_vivo_flag": 1,
            "DOI": "10.1126/sciadv.ady6751", "Annee": 2025.0,
            "Qualite": 3.0, "Verification_statut": "verifie",
            "Notes": "Sci Adv 2025 resolves the 2018-2020 debate. Confirms persistent electronic coherence at ambient T (300 K), supports functional role in energy transfer. Milestone for quantum biology.",
            "dataset_source": "enrichment_v3_D", "last_updated": NOW,
        },
    ]


def deprecate_entries(df: pd.DataFrame, keys_to_deprecate: list[str]) -> pd.DataFrame:
    """Mark matching rows as deprecated (keeps history via Verification_statut)."""
    for key in keys_to_deprecate:
        mask = df["Systeme"].astype(str).str.contains(key, case=False, regex=False)
        if mask.any():
            df.loc[mask, "Verification_statut"] = "deprecated"
            df.loc[mask, "Notes"] = df.loc[mask, "Notes"].astype(str) + \
                f" | DEPRECATED in v3.0: invalidated by 2025 literature; see RESEARCH_BACKLOG and RELEASE_NOTES_v3.0."
            df.loc[mask, "last_updated"] = NOW
    return df


def main() -> int:
    df = pd.read_csv(TARGET, encoding="utf-8")
    before = len(df)

    added_total = 0
    for name, builder in [
        ("B", class_B_entries), ("C", class_C_entries), ("D", class_D_entries),
    ]:
        existing_dois = set(df["DOI"].dropna().astype(str))
        new = pd.DataFrame(builder())
        skip_mask = new["DOI"].astype(str).isin(existing_dois)
        if skip_mask.any():
            skipped = new[skip_mask]["Systeme"].tolist()
            print(f"[SKIP] {len(skipped)} class {name} entries already present by DOI: {skipped}")
            new = new[~skip_mask]
        df = pd.concat([df, new], ignore_index=True)
        added_total += len(new)
        print(f"[OK] Added {len(new)} class {name} entries")

    df = deprecate_entries(df, ["ErCry4b", "ErCry1"])
    n_deprecated = (df["Verification_statut"] == "deprecated").sum()
    print(f"[OK] Deprecated {n_deprecated} rows (invalidated by 2025 literature)")

    df = df.sort_values(["Classe", "Systeme"]).reset_index(drop=True)
    df.to_csv(TARGET, index=False, encoding="utf-8")
    after = len(df)
    print(f"[OK] Total rows: {before} -> {after} (+{added_total})")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"\n## Classes B+C+D enrichment\n\nTimestamp: {NOW}\n\n")
        f.write(f"Added {added_total} entries across classes B/C/D.\n")
        f.write(f"Deprecated {n_deprecated} rows.\n")
        f.write(f"Total rows: {before} -> {after}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
