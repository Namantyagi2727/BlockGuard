"""
BlockGuard – unified security + gas-fee tool
Tab 1  Security Scan  (shows Slither+ranked findings)
Tab 2  Gas Forecast   (we’ll add next)
"""

# ---------- imports ----------
import sys, pathlib, os
ROOT = pathlib.Path(__file__).resolve().parents[1]   # …/blockguard
sys.path.insert(0, str(ROOT)) 
from dotenv import load_dotenv # type: ignore
load_dotenv()                 # pulls OPENAI_API_KEY and RPC_URL into os.environ
import json, pathlib, argparse
import streamlit as st                 # type: ignore # ← Streamlit import
st.set_page_config(page_title="BlockGuard", layout="wide") 
from typing import List, Dict
import pandas as pd, time # type: ignore
from streamlit_autorefresh import st_autorefresh # type: ignore
st_autorefresh(interval=20_000, limit=None, key="refresh")   # 20 s
from gas.predict import gru_predict, median_baseline
from gas.fetch import fee_history
from gas.predict import median_baseline


# ---------- helper ----------
def load_report(path: str) -> List[Dict]:
    with open(path) as f:
        return json.load(f)

# ---------- UI ----------
def security_tab(report_path: str):
    data = load_report(report_path)

    st.title("🛡️ BlockGuard — Security Scan")
    st.caption(f"Loaded **{len(data)}** findings from {pathlib.Path(report_path).name}")

    # Colour scale for severity
    def sev_color(score):
        if score >= 8: return "🟥 **"+str(score)+"**"
        if score >= 5: return "🟧 **"+str(score)+"**"
        return "🟨 **"+str(score)+"**"
        # Download full JSON
    st.download_button("⬇ Download report JSON",
                       data=json.dumps(data, indent=2),
                       file_name="blockguard_report.json")

    # Aggregate visuals
    sev_df = pd.DataFrame(data)
    sev_cat = sev_df["severity"].apply(lambda s: "High" if s>=8 else "Med" if s>=5 else "Low")
    st.subheader("Severity distribution")
    st.bar_chart(sev_cat.value_counts())

    import seaborn as sns, matplotlib.pyplot as plt, io # type: ignore
    heat = sev_df.pivot_table(index="id", values="severity")
    fig, ax = plt.subplots(figsize=(4, len(heat)*0.4+0.5))
    sns.heatmap(heat, cmap="YlOrRd", annot=True, ax=ax, cbar=False)
    st.pyplot(fig)

    for item in data:
        header = f"{sev_color(item['severity'])} — {item['id']}"
        with st.expander(header, expanded=False):
            st.markdown(f"**Explanation**: {item['explanation']}")
            st.markdown("**Original Slither finding:**")
            st.code(item["description"])
            if item["fix"]:
                st.markdown("**Suggested fix:**")
                st.code(item["fix"], language="solidity")

def main(report_path: str):
    tab1, tab2 = st.tabs(["🔍 Security Scan", "⛽ Gas Forecast"])

    with tab1:
        security_tab(report_path)

    with tab2:
        st.title("⛽ BlockGuard — Gas-Fee Forecast")

        try:
            fees = fee_history(240)                  # last ~1 h
            pred_gru  = gru_predict(fees)
            pred_med  = median_baseline(fees)

            c1, c2 = st.columns(2)
            c1.metric("GRU prediction (next block)",   f"{pred_gru:.1f} gwei")
            c2.metric("Median-12 baseline",            f"{pred_med:.1f} gwei")

            st.line_chart(fees.rename("baseFee gwei"))
            st.caption("Auto-refreshes every 20 s.")
        except Exception as e:
            st.error(f"RPC error → {e}")

# ---------- CLI ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to ranked JSON report")
    args = parser.parse_args()
    main(args.input)