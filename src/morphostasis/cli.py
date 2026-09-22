"""Command-line orchestration of independently specified research workstreams."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib
import importlib.metadata
import json
import platform
from pathlib import Path
import subprocess
import sys

from .io import check_budget, write_json

STREAMS = ("spatial", "epithelial", "aged")


def environment() -> dict:
    packages = ("numpy", "pandas", "scipy", "statsmodels", "matplotlib", "requests", "tifffile")
    versions = {p: importlib.metadata.version(p) for p in packages}
    try:
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True,
                                           stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    return {"python": platform.python_version(), "platform": platform.platform(),
            "packages": versions, "git_revision": revision}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("fetch", "validate", "analyze", "report"))
    p.add_argument("--workstream", choices=(*STREAMS, "all"), default="all")
    p.add_argument("--cache-dir", type=Path, default=Path("data/cache"))
    p.add_argument("--output-dir", type=Path, default=Path("results"))
    args = p.parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.command == "report":
        from .reporting import build_report
        print(build_report(args.output_dir))
        return 0
    selected = STREAMS if args.workstream == "all" else (args.workstream,)
    check_budget(args.cache_dir)
    run = {"command": args.command, "started_utc": datetime.now(timezone.utc).isoformat(),
           "environment": environment(), "workstreams": {}}
    failed = False
    for name in selected:
        print(f"[{name}] {args.command}", flush=True)
        module = importlib.import_module(f"morphostasis.{name}")
        try:
            result = getattr(module, args.command)(args.cache_dir / name, args.output_dir / name)
            run["workstreams"][name] = result
            print(json.dumps({"workstream": name, "status": result.get("status", "completed")}, default=str), flush=True)
        except Exception as exc:
            failed = True
            run["workstreams"][name] = {"status": "execution_error", "error_type": type(exc).__name__, "error": str(exc)}
            print(f"[{name}] ERROR: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
    run["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_json(args.output_dir / f"run_{args.command}.json", run)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
