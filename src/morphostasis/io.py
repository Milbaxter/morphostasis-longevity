"""Bounded public-data acquisition and provenance. No credentials are persisted."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
from datetime import datetime, timezone

import requests

GIB = 1024**3
CACHE_LIMIT = 10 * GIB
FREE_FLOOR = 10 * GIB


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024**2), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False, default=str) + "\n")


def check_budget(cache_root: Path, extra_bytes: int = 0) -> dict:
    root = Path(cache_root)
    root.mkdir(parents=True, exist_ok=True)
    used = sum(p.stat().st_size for p in root.rglob("*") if p.is_file())
    free = shutil.disk_usage(root).free
    if used + extra_bytes > CACHE_LIMIT:
        raise RuntimeError("10 GiB cache budget would be exceeded")
    if free - extra_bytes < FREE_FLOOR:
        raise RuntimeError("Download would leave less than 10 GiB free")
    return {"cache_bytes": used, "free_bytes": free}


def download(url: str, dest: Path, *, cache_root: Path | None = None,
             max_bytes: int = 256 * 1024**2, expected_sha256: str | None = None,
             source: str = "", license_note: str = "Source terms apply") -> dict:
    """Stream a bounded file, verify cached files, and write a provenance sidecar.

    max_bytes is checked against both headers and actual streamed bytes. The total
    cache budget is rechecked each chunk, including simultaneous sibling downloads.
    Cached content is trusted only if its sidecar URL and hash match.
    """
    dest = Path(dest)
    cache_root = Path(cache_root) if cache_root else dest.parent
    dest.parent.mkdir(parents=True, exist_ok=True)
    meta_path = dest.with_name(dest.name + ".provenance.json")
    if dest.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        actual = sha256(dest)
        if meta.get("url") != url or actual != meta.get("sha256"):
            raise ValueError(f"Cached provenance mismatch: {dest.name}")
        if expected_sha256 and actual != expected_sha256:
            raise ValueError(f"Pinned checksum mismatch: {dest.name}")
        check_budget(cache_root)
        return meta
    part = dest.with_name(dest.name + ".part")
    try:
        with requests.get(url, stream=True, timeout=(20, 60),
                          headers={"User-Agent": "morphostasis-longevity/0.1 (public research)"}) as r:
            r.raise_for_status()
            advertised = int(r.headers.get("Content-Length", 0))
            if advertised > max_bytes:
                raise ValueError(f"File exceeds {max_bytes} byte request budget")
            check_budget(cache_root, advertised)
            count = 0
            with part.open("wb") as f:
                for block in r.iter_content(chunk_size=1024**2):
                    count += len(block)
                    if count > max_bytes:
                        raise ValueError("Stream exceeds request budget")
                    check_budget(cache_root, len(block))
                    f.write(block)
            digest = sha256(part)
            if expected_sha256 and digest != expected_sha256:
                raise ValueError(f"Pinned checksum mismatch: {dest.name}")
            os.replace(part, dest)
            meta = {"url": url, "source": source, "license_note": license_note,
                    "sha256": digest, "bytes": count,
                    "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                    "etag": r.headers.get("ETag")}
            write_json(meta_path, meta)
            return meta
    finally:
        if part.exists():
            part.unlink()


def read_range(url: str, start: int, end: int, *, total_size: int | None = None,
               max_bytes: int = 8 * 1024**2) -> bytes:
    """Fetch exactly one inclusive HTTP range, rejecting full-body responses."""
    import re
    size = end - start + 1
    if start < 0 or size < 1 or size > max_bytes:
        raise ValueError("Invalid or oversized range")
    with requests.get(url, headers={"Range": f"bytes={start}-{end}",
                                   "Accept-Encoding": "identity"},
                      stream=True, timeout=(20, 60)) as r:
        if r.status_code != 206:
            raise ValueError(f"Range request returned {r.status_code}; refusing body")
        match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", r.headers.get("Content-Range", ""))
        if not match or tuple(map(int, match.groups()[:2])) != (start, end):
            raise ValueError("Server returned a different byte range")
        if total_size is not None and int(match.group(3)) != total_size:
            raise ValueError("Archive size changed")
        body = r.raw.read(size + 1)
        if len(body) != size:
            raise ValueError("Truncated or oversized range body")
        return body
