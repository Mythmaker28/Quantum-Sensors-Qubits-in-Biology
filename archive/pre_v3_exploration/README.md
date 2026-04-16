# Archive - Pre v3.0 exploration artefacts

This folder preserves exploration documents, session logs, agent reports, and one-off scripts that were generated during the pre-v3.0 exploration phase (Oct 2025 - Apr 2026).

They were moved out of the repository root during the v3.0.0 release cleanup to keep the active workspace focused on:

- the canonical v3.0 dataset (`data/qubits/biological_qubits_v3.csv`, `data/optical/curated/atlas_fp_optical_v3_curated.csv`);
- the official documentation set (`README.md`, `DOCUMENTATION.md`, `CHANGELOG.md`, `RELEASE_NOTES_v3.0.md`, `VERSIONS_CITATION.md`, `VERSIONING_ROADMAP.md`);
- the reusable scripts under `scripts/`, `analysis/`, and the top-level `run_pipeline.py`.

## Structure

- `scripts/` - ad-hoc scripts that are no longer part of the current ETL pipeline (e.g. Frontiers submission helpers, v1.3 quick builds, legacy repository inspection utilities).
- `release_notes/` - historical release notes (v1.3.0, v2.2.2). The current release notes live at the repo root (`RELEASE_NOTES_v3.0.md`).
- `*.md` / `*.txt` - older status reports, session summaries, agent reports, and French "entry-point" guides.
- `bioRxiv_submission_pack_BQA_v1_3_beta.zip` - the bioRxiv submission pack for v1.3.0-beta.

## Policy

Files in this folder are kept for provenance. They are not intended to be modified and should not be referenced by the active documentation or code. If you need content from one of these files, copy the relevant portions into a new, properly-versioned document under the active tree.
