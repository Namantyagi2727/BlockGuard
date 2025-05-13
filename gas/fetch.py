import os, requests, pandas as pd # type: ignore

RPC = os.getenv("RPC_URL")          # loaded via dotenv in Streamlit

def fee_history(num_blocks: int = 120) -> pd.Series:
    """
    Get baseFeePerGas for the last `num_blocks` blocks (~30 min on Ethereum).
    Returns a Pandas Series indexed 0 … num_blocks-1 (oldest→newest).
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_feeHistory",
        "params": [hex(num_blocks), "latest", []]
    }
    r = requests.post(RPC, json=payload, timeout=10)
    r.raise_for_status()
    fees_hex = r.json()["result"]["baseFeePerGas"]
    fees_gwei = [int(x, 16) / 1e9 for x in fees_hex]
    return pd.Series(fees_gwei[::-1], dtype="float32")   # new