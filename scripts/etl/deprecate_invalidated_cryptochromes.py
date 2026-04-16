"""Mark Cry1-based rows as deprecated based on 2025 literature.

The plan identifies ErCry1 and ErCry4b as superseded by 2025 publications
that show they are not involved in magnetoreception the way earlier papers
suggested:
- ErCry1 shown to be circadian-only (PMC12757563)
- ErCry4b shown to lack FAD binding (bioRxiv 2025.02.21.639466)

This script flags the matching rows in biological_qubits_v3.csv as
deprecated but keeps them in the dataset for traceability.
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

PATTERNS_TO_DEPRECATE = {
    "Cry1": "ErCry1 shown to be circadian-only; see PMC12757563 (2025). Not a magnetoreceptor.",
    "Cryptochrome 1a": "Early Cry1a assignment superseded; evidence now supports Cry4a as primary magnetoreceptor candidate.",
}


def main() -> int:
    df = pd.read_csv(TARGET, encoding="utf-8")
    now = datetime.now(timezone.utc).isoformat()
    n_total = 0

    for pattern, reason in PATTERNS_TO_DEPRECATE.items():
        mask = df["Systeme"].astype(str).str.contains(pattern, case=False, regex=False)
        mask = mask & (df["Classe"] == "D")
        mask = mask & (df["Verification_statut"] != "deprecated")
        n = int(mask.sum())
        if n == 0:
            print(f"[SKIP] No rows matched pattern '{pattern}'")
            continue
        df.loc[mask, "Verification_statut"] = "deprecated"
        df.loc[mask, "Notes"] = df.loc[mask, "Notes"].astype(str) + f" | DEPRECATED v3.0: {reason}"
        df.loc[mask, "last_updated"] = now
        n_total += n
        print(f"[OK] Deprecated {n} rows matching '{pattern}'")

    df.to_csv(TARGET, index=False, encoding="utf-8")
    print(f"[OK] Total deprecated: {n_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
