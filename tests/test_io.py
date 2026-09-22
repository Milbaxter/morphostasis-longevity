from pathlib import Path
import json
from unittest.mock import patch

import pytest

from morphostasis.io import download, read_range, sha256, check_budget


class Response:
    def __init__(self, body=b"abc", status=200, headers=None):
        import io
        self.body, self.status_code = body, status
        self.headers = headers or {}
        self.raw = io.BytesIO(body)
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def raise_for_status(self): pass
    def iter_content(self, chunk_size): yield self.body


def test_range_refuses_full_archive_without_reading():
    r = Response(status=200)
    r.raw.read = lambda *a: pytest.fail("Should refuse before reading full body")
    with patch("morphostasis.io.requests.get", return_value=r):
        with pytest.raises(ValueError, match="refusing body"):
            read_range("https://example.org/archive", 0, 2)


@pytest.mark.parametrize("header", ["bytes 1-3/20", "bytes 0-2/21", "", "bytes */20"])
def test_range_requires_matching_extent(header):
    with patch("morphostasis.io.requests.get", return_value=Response(status=206, headers={"Content-Range": header})):
        with pytest.raises(ValueError):
            read_range("https://example.org/archive", 0, 2, total_size=20)


def test_range_exact_and_truncation():
    with patch("morphostasis.io.requests.get", return_value=Response(status=206, headers={"Content-Range": "bytes 0-2/20"})):
        assert read_range("https://example.org/archive", 0, 2, total_size=20) == b"abc"
    with patch("morphostasis.io.requests.get", return_value=Response(b"a", status=206, headers={"Content-Range": "bytes 0-2/20"})):
        with pytest.raises(ValueError, match="Truncated"):
            read_range("https://example.org/archive", 0, 2, total_size=20)


def test_download_provenance_tamper_and_stream_cap(tmp_path):
    dest = tmp_path / "x.txt"
    with patch("morphostasis.io.requests.get", return_value=Response()):
        result = download("https://example.org/x", dest, max_bytes=3)
    assert result["sha256"] == sha256(dest)
    dest.write_text("tampered")
    with pytest.raises(ValueError, match="provenance mismatch"):
        download("https://example.org/x", dest)
    other = tmp_path / "y.txt"
    with patch("morphostasis.io.requests.get", return_value=Response(b"too many")):
        with pytest.raises(ValueError, match="exceeds request budget"):
            download("https://example.org/y", other, max_bytes=3)
    assert not other.exists()
    assert not other.with_name("y.txt.part").exists()


def test_disk_floor_and_cache_cap(tmp_path):
    from collections import namedtuple
    Usage = namedtuple("Usage", "total used free")
    with patch("morphostasis.io.shutil.disk_usage", return_value=Usage(20, 15, 5)):
        with pytest.raises(RuntimeError, match="free"):
            check_budget(tmp_path)
    with patch("morphostasis.io.CACHE_LIMIT", 2):
        (tmp_path / "large").write_bytes(b"123")
        with pytest.raises(RuntimeError, match="cache budget"):
            check_budget(tmp_path)
