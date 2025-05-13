#!/usr/bin/env python
import argparse, json, subprocess, tempfile, pathlib, uuid
from scanner import llm_ranker

from dotenv import load_dotenv # type: ignore
load_dotenv()
import os, subprocess, json, pathlib, uuid, argparse, tempfile, requests # type: ignore
from urllib.parse import urlparse
import json, os, subprocess, uuid, pathlib
from scanner import llm_ranker

def _is_git_url(s):
    return s.endswith(".git") or s.startswith("git@") or "/blob/" not in s

def _download_http_file(url) -> str:
    """Return local path to a temp-downloaded Solidity file."""
    fn = tempfile.mktemp(suffix=".sol")
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    open(fn, "wb").write(r.content)
    return fn

def _clone_git_repo(url) -> str:
    """Clone repo to /tmp and return path."""
    dest = tempfile.mkdtemp()
    subprocess.run(["git", "clone", "--depth", "1", url, dest], check=True)
    return dest

def _run_slither(src: str) -> dict:
    """Run Slither, parse JSON, ignore non-zero exit code (vulns found)."""
    out_path = pathlib.Path("data") / f"slither_{uuid.uuid4().hex[:6]}.json"
    cmd = ["slither", src, "--json", str(out_path)]
    # We DON'T set check=True; we accept any exit code
    subprocess.run(cmd, text=True)
    if not out_path.exists():
        raise RuntimeError("Slither did not produce JSON output")
    with open(out_path) as f:
        data = json.load(f)
    os.remove(out_path)
    return data

from urllib.parse import urlparse

def _is_remote(path: str) -> bool:
    """
    Return True only if path is:
      • http/https URL
      • git clone URL ending in .git
      • git@… SSH URL
    Anything else (absolute or relative filesystem path) is LOCAL.
    """
    if path.startswith(("http://", "https://")):
        return True
    if path.endswith(".git") or path.startswith("git@"):
        return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Solidity file or folder")
    ap.add_argument("--out", default=f"data/report_{uuid.uuid4().hex[:6]}.json")
    args = ap.parse_args()
    src = args.src

    # ---- 1. If it's an existing local path, leave it alone
    if os.path.exists(src):
        pass                          # nothing to do — already local

# ---- 2. If it's remote, fetch or clone
    elif _is_remote(src):
        if src.endswith(".git") or src.startswith("git@"):
            src = _clone_git_repo(src)
        else:                         # http/https raw file
            src = _download_http_file(src)

# ---- 3. Otherwise, treat as relative local path (may raise error later)
    else:
        pass    
    pathlib.Path("data").mkdir(exist_ok=True)
    raw = _run_slither(args.src)
    ranked = llm_ranker.rank(raw)

    with open(args.out, "w") as f:
        json.dump(ranked, f, indent=2)
    print(f"[✓] Ranked report saved to {args.out}")

if __name__ == "__main__":
    main()
