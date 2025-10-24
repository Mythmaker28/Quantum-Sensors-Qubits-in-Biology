README - Supplementary Data for Frontiers Submission

This supplementary data package contains the complete Biological Qubits Atlas v1.2.1 dataset and metadata files.

FILES INCLUDED:
- atlas_fp_optical.csv: Main dataset (66 FP/biosensor entries, 54 with measured contrast)
- atlas_all_real.csv: Extended dataset (all modalities, legacy compatibility)
- TRAINING.METADATA.json: Schema, provenance, and license information
- SHA256SUMS.txt: SHA-256 checksums for integrity verification

DATASET SCHEMA:
The atlas_fp_optical.csv contains 22 columns including protein identification (SystemID, protein_name, family), optical properties (excitation_nm, emission_nm), contrast measurements (contrast_ratio, contrast_unit, contrast_normalized), experimental context (temperature_K, pH, condition_text), and provenance (source_refs, license_source, figure_ref).

VERIFICATION:
To verify file integrity, run: sha256sum -c SHA256SUMS.txt
On Windows: certutil -hashfile filename SHA256

All data are sourced from Open Access literature (CC-BY/CC0) with full DOI/PMCID traceability.
No synthetic or placeholder values included.

For questions or issues, contact: GitHub Issues or email (to be provided).
