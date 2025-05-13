import torch, pandas as pd, functools # type: ignore

SEQ = 24

@functools.lru_cache(maxsize=1)
def _load():
    ck = torch.load("data/gru.pt", map_location="cpu")
    m  = torch.nn.GRU(1, 8, batch_first=True); m.load_state_dict(ck["model"]); m.eval()
    h  = torch.nn.Linear(8, 1);               h.load_state_dict(ck["head"]);  h.eval()
    return m, h

def gru_predict(series: pd.Series) -> float:
    """Predict next-block baseFee with the trained GRU."""
    m, h = _load()
    if len(series) < SEQ:
        return series.median()
    # cast to float32 before Tensor conversion
    x_np = series[-SEQ:].values.astype("float32")
    x = torch.from_numpy(x_np).unsqueeze(0).unsqueeze(-1)   # shape [1, 24, 1]
    with torch.no_grad():
        out, _ = m(x)
        return h(out[:, -1]).item()
    
def median_baseline(series: pd.Series, window: int = 12) -> float:
    """Simple baseline: median of the last `window` blocks."""
    if len(series) < window:
        window = len(series)
    return series.iloc[-window:].median()