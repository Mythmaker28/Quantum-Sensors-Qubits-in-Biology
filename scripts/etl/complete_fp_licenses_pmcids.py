"""Complete missing license + PMCID fields in atlas_fp_optical_v3_curated.csv.

Sources:
- Unpaywall (https://api.unpaywall.org/v2/<doi>) for open-access license
  and best_oa_location.license strings.
- NCBI ID Converter (https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/)
  for DOI -> PMCID mapping.

Behavior:
- Leaves non-empty license / pmcid cells unchanged.
- Falls back gracefully on transient HTTP errors and logs them in
  reports/FP_LICENSE_PMCID_log.md.

Usage:
    python scripts/etl/complete_fp_licenses_pmcids.py --email you@example.org
    python scripts/etl/complete_fp_licenses_pmcids.py --dry-run
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import parse, request
from urllib.error import HTTPError, URLError

import pandas as pd

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
TARGETS = [
    REPO / "data" / "optical" / "curated" / "atlas_fp_optical_v3_curated.csv",
    REPO / "data" / "processed" / "atlas_fp_optical_v3_curated.csv",
]
LOG = REPO / "reports" / "FP_LICENSE_PMCID_log.md"

UNPAYWALL = "https://api.unpaywall.org/v2/{doi}?email={email}"
IDCONV = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={doi}&format=json"

REQUEST_TIMEOUT = 15


def _http_json(url: str) -> dict | None:
    try:
        req = request.Request(url, headers={"User-Agent": "atlas-qubits-v3/1.0"})
        with request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def fetch_license(doi: str, email: str) -> tuple[str | None, str | None]:
    """Return (license_text, source_note)."""
    data = _http_json(UNPAYWALL.format(doi=parse.quote(doi), email=parse.quote(email)))
    if not data:
        return None, None
    loc = data.get("best_oa_location") or {}
    lic = loc.get("license") or data.get("oa_status")
    host = loc.get("host_type") or "publisher"
    if lic:
        return str(lic).upper().replace("-", " "), f"Unpaywall/{host}"
    return None, None


def fetch_pmcid(doi: str) -> str | None:
    data = _http_json(IDCONV.format(doi=parse.quote(doi)))
    if not data:
        return None
    records = data.get("records", [])
    if not records:
        return None
    pmcid = records[0].get("pmcid")
    return pmcid if pmcid else None


def enrich(df: pd.DataFrame, email: str, dry_run: bool) -> tuple[pd.DataFrame, list[str]]:
    log: list[str] = []
    n_license = 0
    n_pmcid = 0
    for idx, row in df.iterrows():
        doi = str(row.get("doi") or "").strip()
        if not doi or doi.lower() in {"nan", "none"}:
            continue

        need_license = pd.isna(row.get("license")) or str(row.get("license")).strip() == ""
        need_pmcid = pd.isna(row.get("pmcid")) or str(row.get("pmcid")).strip() == ""

        if not need_license and not need_pmcid:
            continue

        if need_license:
            lic, src = fetch_license(doi, email)
            if lic:
                if not dry_run:
                    df.at[idx, "license"] = lic
                    if pd.isna(row.get("license_source")) or not str(row.get("license_source")).strip():
                        df.at[idx, "license_source"] = src or "Unpaywall"
                log.append(f"- [{row.get('protein_name', '?')}] license <- {lic} (via {src})")
                n_license += 1
            time.sleep(0.2)

        if need_pmcid:
            pmcid = fetch_pmcid(doi)
            if pmcid:
                if not dry_run:
                    df.at[idx, "pmcid"] = pmcid
                log.append(f"- [{row.get('protein_name', '?')}] pmcid <- {pmcid}")
                n_pmcid += 1
            time.sleep(0.2)

    log.insert(0, f"Completed license: {n_license} rows")
    log.insert(1, f"Completed pmcid:   {n_pmcid} rows\n")
    return df, log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--email", default="atlas-qubits@example.org", help="Email for Unpaywall API")
    ap.add_argument("--dry-run", action="store_true", help="Do not write files")
    args = ap.parse_args()

    primary = TARGETS[0]
    df = pd.read_csv(primary, encoding="utf-8")
    print(f"[INFO] Loaded {len(df)} rows from {primary.relative_to(REPO)}")
    print(f"[INFO] Missing license: {df['license'].isna().sum()}")
    print(f"[INFO] Missing pmcid:   {df['pmcid'].isna().sum()}")

    df, log_lines = enrich(df, args.email, args.dry_run)

    if not args.dry_run:
        for target in TARGETS:
            df.to_csv(target, index=False, encoding="utf-8")
            print(f"[OK] Wrote {target.relative_to(REPO)}")
        LOG.parent.mkdir(parents=True, exist_ok=True)
        header = [
            "# FP license + PMCID completion log\n",
            f"\nGenerated: {datetime.now(timezone.utc).isoformat()}\n\n",
        ]
        with open(LOG, "w", encoding="utf-8") as fh:
            fh.writelines(header)
            fh.write("\n".join(log_lines) + "\n")
        print(f"[OK] Log: {LOG.relative_to(REPO)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
