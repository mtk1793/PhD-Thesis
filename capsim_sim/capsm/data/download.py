"""Download and verify Open Power System Data (OPSD) time-series files.

Primary real-data source for the CAPSM Stage-1 offline validation.

Data package: OPSD "Time series", version 2020-10-06.
DOI: https://doi.org/10.25832/time_series/2020-10-06
Primary data: ENTSO-E Transparency Platform (real measured values).
Coverage: 2015 to mid-2020, hourly and 15-minute resolution.
"""

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "https://data.open-power-system-data.org/time_series/2020-10-06"

FILES = {
    "time_series_60min_singleindex.csv": {
        "url": f"{BASE_URL}/time_series_60min_singleindex.csv",
        "expected_bytes": 124_000_000,
    },
    "time_series_15min_singleindex.csv": {
        "url": f"{BASE_URL}/time_series_15min_singleindex.csv",
        "expected_bytes": 107_000_000,
    },
}

MANIFEST_NAME = "provenance_manifest.json"

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def sha256_of(path: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def download_file(name: str, dest_dir: Path = DATA_DIR, force: bool = False) -> Path:
    spec = FILES[name]
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / name
    if dest.exists() and not force:
        print(f"[download] {name} already exists ({dest.stat().st_size:,} bytes), skipping")
        return dest
    url = spec["url"]
    print(f"[download] {name}: fetching {url}")
    t0 = time.time()
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
                done += len(chunk)
                if total:
                    pct = 100 * done / total
                    print(f"\r[download] {name}: {done:,}/{total:,} bytes ({pct:.1f}%)", end="")
    dt = time.time() - t0
    print(f"\n[download] {name}: finished {dest.stat().st_size:,} bytes in {dt:.1f}s")
    return dest


def verify_and_manifest(dest_dir: Path = DATA_DIR) -> dict:
    manifest = {
        "dataset": "Open Power System Data - Time series",
        "version": "2020-10-06",
        "doi": "https://doi.org/10.25832/time_series/2020-10-06",
        "primary_source": "ENTSO-E Transparency Platform (measured values)",
        "attribution": (
            "Open Power System Data. 2020. Data Package Time series. "
            "Version 2020-10-06. https://doi.org/10.25832/time_series/2020-10-06. "
            "(Primary data from ENTSO-E Transparency.)"
        ),
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": {},
    }
    for name, spec in FILES.items():
        path = dest_dir / name
        if not path.exists():
            raise FileNotFoundError(f"{name} not downloaded yet")
        size = path.stat().st_size
        digest = sha256_of(path)
        size_ok = size >= spec["expected_bytes"] * 0.95
        manifest["files"][name] = {
            "url": spec["url"],
            "bytes": size,
            "expected_min_bytes": spec["expected_bytes"],
            "size_ok": bool(size_ok),
            "sha256": digest,
        }
        status = "OK" if size_ok else "SIZE MISMATCH"
        print(f"[verify] {name}: {size:,} bytes, sha256={digest[:16]}... -> {status}")
    out = dest_dir / MANIFEST_NAME
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"[verify] manifest written to {out}")
    return manifest


def run(force: bool = False) -> dict:
    for name in FILES:
        download_file(name, force=force)
    return verify_and_manifest()


if __name__ == "__main__":
    run()
