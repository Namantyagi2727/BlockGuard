#!/usr/bin/env python
"""
Fetch verified source code from Etherscan and run BlockGuard scan.
Usage: python utils/scan_etherscan.py 0xContractAddress
"""
import os, requests, tempfile, subprocess, json, sys, pathlib # type: ignore
from dotenv import load_dotenv; load_dotenv() # type: ignore

KEY = os.getenv("ETHERSCAN_KEY")
if not KEY:
    sys.exit(" ETHERSCAN_KEY missing in .env")

ADDR = sys.argv[1]
url  = (
    "https://api.etherscan.io/api"
    "?module=contract&action=getsourcecode"
    f"&address={ADDR}&apikey={KEY}"
)
data = requests.get(url, timeout=15).json()["result"][0]
src_str = data["SourceCode"]
if not src_str.strip():
    sys.exit(" Contract source not verified on Etherscan.")

if src_str.strip().startswith("{"):
    src_str = "// Flattened multi-file JSON removed for demo\n"

tmp = tempfile.mktemp(suffix=".sol")
open(tmp, "w").write(src_str)

tmp = tempfile.mktemp(suffix=".sol")
open(tmp, "w").write(data["SourceCode"])
out = pathlib.Path("data")/f"ethscan_{ADDR[:6]}.json"
subprocess.run([sys.executable, "scan.py", "--src", tmp, "--out", str(out)], check=True)
print(f" report saved to {out}")