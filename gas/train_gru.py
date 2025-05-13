"""
Train a tiny 1-layer GRU to predict next-block baseFeePerGas.
Saves model weights to data/gru.pt for the Streamlit app to load.
"""

from dotenv import load_dotenv # type: ignore
load_dotenv()                       # pulls RPC_URL from .env

import numpy as np # type: ignore
import torch, torch.nn as nn # type: ignore
from gas.fetch import fee_history

# ---------------- hyper-params ----------------
N   = 1000   # how many recent blocks to fetch for training
SEQ = 24     # look-back window (24 blocks ≈ 6 min)
EPOCHS = 20
LR = 1e-2
# ----------------------------------------------

# 1. Fetch data  (fee_history returns N+1 values by spec)
series = fee_history(N + 1).values.astype("float32")

# 2. Build sliding-window dataset with consistent lengths
n_samples = len(series) - SEQ            # e.g. 1001-24 = 977
seqs    = np.stack([series[i:i+SEQ] for i in range(n_samples)]).astype("float32")
targets = series[SEQ:SEQ + n_samples].astype("float32")

X = torch.from_numpy(seqs).unsqueeze(-1)   # [n_samples, SEQ, 1], float32
y = torch.from_numpy(targets).unsqueeze(-1)

# 3. Define model
model = nn.GRU(1, 8, batch_first=True)
head  = nn.Linear(8, 1)

optim = torch.optim.Adam(list(model.parameters()) + list(head.parameters()), lr=LR)
lossf = nn.MSELoss()

# 4. Training loop
for epoch in range(EPOCHS):
    pred, _ = model(X)
    loss = lossf(head(pred[:, -1]), y)
    optim.zero_grad(); loss.backward(); optim.step()
    if epoch % 5 == 0:
        print(f"epoch {epoch:02d}  loss {loss.item():.4f}")

# 5. Save weights
torch.save({"model": model.state_dict(), "head": head.state_dict()}, "data/gru.pt")
print("✅ saved model to data/gru.pt")