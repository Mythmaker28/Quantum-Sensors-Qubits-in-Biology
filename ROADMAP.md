# 🗺️ Roadmap — Next Steps

**State checked on 2026-10-24** against `main` at commit [`6759768`](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/commit/6759768) (merge of PR #16, 2025-11-14).
Each step names its evidence (a file, a PR or a commit) and a command that tells whether it is done.

Version history stays in [VERSIONING_ROADMAP.md](VERSIONING_ROADMAP.md) and data limitations in [KNOWN_ISSUES.md](KNOWN_ISSUES.md).
Steps marked **maintainer** change data, releases or repository settings and wait for the maintainer's decision.
The other steps only touch documentation, tests or CI.

---

## Current state

Commands run from the repository root, in an activated virtual environment (Python 3.11) with `requirements.txt` and `pytest` installed.

| Check | Command | Result on `6759768` |
|---|---|---|
| Unit tests | `python -m pytest tests/ -q -rs` | 34 passed, 5 skipped, 5 failed (steps 2 and 3) |
| Atlas validator | `python scripts/validate_atlas.py curated` (also `mixed`, `candidates`, `unknown`) | exit 0, warnings only |
| Non-optical validator | `python scripts/qa/validate_non_optical.py` | exit 0, 23 systems |
| Linter (the only check in CI) | `python qubits_linter.py` | exit 0, 0 errors, 6 warnings |
| Version consistency | `python scripts/qa/check_version_consistency.py` | exit 0, 1 warning (step 8) |
| Branches holding the latest release | `git fetch origin --tags && git branch -r --contains v4.0.0` | `origin/release/v3.0` only; GitHub release v4.0.0 dates from 2026-04-17 (step 1) |

---

## Steps

### 1. Bring the published v4.0.0 state into `main` — maintainer

- **Evidence**: the GitHub releases v3.0.0 (2026-04-16) and v4.0.0 (2026-04-17) were cut from branch `release/v3.0`, with tags on [`43cd38e`](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/commit/43cd38e) and [`0ca9c51`](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/commit/0ca9c51). That branch is 15 commits ahead of `main`.
  `main` still presents v2.2.2 with DOI "TBD" ([README.md](README.md) lines 69, 247 and 261, [CITATION.cff:5-7](CITATION.cff#L5-L7)).
  `release/v3.0` presents v4.0.0 (82 qubits in `data/qubits/biological_qubits_v3.csv`, 195 FP biosensors in `data/processed/atlas_fp_optical_v3_curated.csv`) with concept DOI 10.5281/zenodo.17420603.
- **Known**: the 4 commits of `main` that `release/v3.0` lacks are merge commits, `main`'s tree equals that of the merge base `88afdd8`, and `git merge-tree --write-tree origin/main origin/release/v3.0` reports no conflict.
  The merge changes 254 files (+12,130 / −35,800 lines), including the removal of `archive/` and `reports/` described in `0ca9c51`.
- **Blocker**: on `release/v3.0`, `python qubits_linter.py` exits 1 with `FileNotFoundError: ... 'biological_qubits.csv'`.
  Commit [`166c46e`](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/commit/166c46e) removed that file from the root, and `data/qubits/biological_qubits.csv` (added in [`7251d5b`](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/commit/7251d5b)) holds the same content, but [qubits_linter.py:49](qubits_linter.py#L49) and [:341](qubits_linter.py#L341), identical on both branches, still read the root path.
  CI runs this linter as a blocking step on pull requests to `main` ([ci.yml:3-7](.github/workflows/ci.yml#L3-L7)), so the path needs fixing before the merge. With the file copied back to the root, the linter exits 0 (0 errors, 6 warnings).
- **Done when**: `git fetch origin --tags && git merge-base --is-ancestor v4.0.0 origin/main && echo merged` prints `merged`.
- Steps 4 and 8 are already done on `release/v3.0`; steps 2, 3, 5, 6 and 7 apply to both branches (there, the linter part of step 7 only shows once the blocker above is fixed).

### 2. Fix the dashboard generation test

- **Evidence**: [tests/test_dashboard_generation.py:39](tests/test_dashboard_generation.py#L39) starts the script with `"python"`, which fails when the `python` on `PATH` has no pandas (`ModuleNotFoundError`).
  [Line 49](tests/test_dashboard_generation.py#L49) then expects `Dashboard généré` or `✅`, while the script prints `[OK] Dashboard genere:` ([scripts/web/generate_interactive_dashboard.py:426](scripts/web/generate_interactive_dashboard.py#L426)).
  `test_dashboard_generation_success` fails the same way on `release/v3.0`.
- **Proposed fix**: draft PR [#17](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/pull/17) uses `sys.executable` and checks for `[OK] Dashboard genere:`.
- **Done when**: `python -m pytest tests/test_dashboard_generation.py -q -rs` reports no failure.

### 3. Decide what the v2.1 schema gates mean — maintainer

- **Evidence**: 4 tests of [tests/test_optical_schema_v2_1.py](tests/test_optical_schema_v2_1.py) fail on `main` and on `release/v3.0`: `test_canonical_name_uniqueness` (line 101), `test_target_n_useful` (110), `test_coverage_minimal` (120) and `test_family_distribution` (138).
  PR [#18](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/pull/18) records the figures in KNOWN_ISSUES.md: 22 duplicate names in 113 rows, 113 rows for a target of 120, 66.4% excitation/emission coverage for a target of 90%, and 9 families with at least 5 entries for a target of 10.
- **Choice**: complete the v2.1 files from cited sources, or declare v2.1 a frozen snapshot and move the gates to the current tier. Editing values only to pass the gates is not an option.
- **Done when**: the choice is recorded in KNOWN_ISSUES.md and `python -m pytest tests/test_optical_schema_v2_1.py -q` reports no failure.

### 4. Point the installation tests at an existing atlas file — done on `release/v3.0`

- **Evidence**: [tests/test_v2_installation.py:47](tests/test_v2_installation.py#L47) and [:107](tests/test_v2_installation.py#L107) read `data/processed/atlas_fp_optical_v1_3.csv`, which does not exist, so both tests skip (lines 57 and 110).
  `release/v3.0` reads `data/processed/atlas_fp_optical_v2_2_curated.csv` instead.
- **Done when**: `python -m pytest tests/test_v2_installation.py -q -rs` no longer reports `Atlas CSV non trouvé`.

### 5. Run the validators and tests in CI

- **Evidence**: [.github/workflows/ci.yml:24-25](.github/workflows/ci.yml#L24-L25) and [:46-47](.github/workflows/ci.yml#L46-L47) only run `python qubits_linter.py`, and [requirements.txt](requirements.txt) does not list `pytest`.
  CI run 68 on `6759768` passed with the linter alone.
- **Now**: `validate_atlas.py curated`, `validate_non_optical.py` and `pytest tests/test_optical_schema_v2_2.py tests/test_v2_installation.py` already pass and can become a CI job. The full suite waits for steps 2 and 3.
- **Done when**: `grep -n -E 'pytest|validate_atlas|validate_non_optical' .github/workflows/ci.yml` lists these commands and the workflow is green.

### 6. Repair or retire the external FP pipeline — maintainer

- **Evidence**: [.github/workflows/atlas_external_fp.yml:15](.github/workflows/atlas_external_fp.yml#L15) (and lines 54, 94, 132, 166 and 213) checks out `release/v1.2-fp-optical`, a branch that does not exist on the remote.
  The last 5 of its 13 runs (2025-12-22 to 2026-01-19) failed in the "External Data Harvest" job. Their logs have expired, so the cause is not confirmed.
  GitHub has since disabled the workflow for inactivity. The file is identical on `release/v3.0`.
- **Choice**: point the checkouts at an existing branch and re-enable the workflow, or remove it.
- **Done when**: `grep -c 'release/v1.2-fp-optical' .github/workflows/atlas_external_fp.yml` prints 0 and a manual run succeeds, or the workflow is gone.

### 7. Keep local checks from modifying the working tree

- **Evidence**: each `python qubits_linter.py` run rewrites the date on line 3 of the tracked [QC_REPORT.md](QC_REPORT.md); CI already uploads that report as an artifact ([ci.yml:28-34](.github/workflows/ci.yml#L28-L34)).
  The dashboard test writes `index_v2_interactive.html` in the repository root ([generate_interactive_dashboard.py:12](scripts/web/generate_interactive_dashboard.py#L12)), and git does not ignore it.
- **Done when**: `python qubits_linter.py && python -m pytest tests/ -q; git status --short` prints no file.

### 8. Align the v2.2.2 system counts — done on `release/v3.0`

- **Evidence**: on `main`, VERSIONING_ROADMAP.md lines 11 and 25 and [scripts/qa/check_version_consistency.py:24](scripts/qa/check_version_consistency.py#L24) give v2.2.2 250 systems.
  The data files hold 180 curated rows (`data/processed/atlas_fp_optical_v2_2_curated.csv`), 296 rows in total (`data/processed/atlas_fp_optical_v2_2.csv`) and 221 rows in `data/processed/TRAINING_TABLE_v2_2_2_full.csv`; the README badges say 180 and 296.
  On `release/v3.0`, the script checks the v4.0.0 counts and passes.
- **Done when**: `python scripts/qa/check_version_consistency.py` prints no warning.

### 9. Close the superseded Zenodo PR — maintainer

- **Evidence**: PR [#3](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/pull/3) (2025-10-22) adds a `zenodo.json` for v1.2.0 (22 systems).
  `main` already has a v2.2.2 `zenodo.json` (commit [`d0da3f8`](https://github.com/Mythmaker28/Quantum-Sensors-Qubits-in-Biology/commit/d0da3f8)) and `release/v3.0` a v4.0.0 one.
- **Done when**: PR #3 is closed.

### 10. Re-date or drop the past milestones — maintainer

- **Evidence**: on `main`, VERSIONING_ROADMAP.md lines 89-114 still plan v2.3.0 (Q1 2026), v2.4.0 (Q2 2026) and v3.0.0 (Q3-Q4 2026).
  KNOWN_ISSUES.md lines 213-228 target v1.3.0 (Nov 2025), v1.4.0 (Q1 2026) and v2.0.0 (2026).
  On `release/v3.0`, VERSIONING_ROADMAP.md plans v4.1.0 for Q3 2026, now past, and v4.2.0 for Q4 2026.
- **Done when**: `grep -n -i -E 'planned|target' VERSIONING_ROADMAP.md KNOWN_ISSUES.md` shows no date before the current quarter.

---

## Updating this file

Re-run the commands of the [Current state](#current-state) table, update the commit and date at the top, and remove the steps whose **Done when** check passes.
