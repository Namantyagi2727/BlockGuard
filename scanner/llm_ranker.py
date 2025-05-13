from dotenv import load_dotenv # type: ignore
load_dotenv()
from scanner.local_llm import explain
import os, json
from typing import Dict, Any, List

_PROMPT = """
You are a smart-contract security auditor. Given this Slither finding:

<<<{finding}>>>

Return JSON with keys:
  severity   (1-10, 10 = critical)
  explanation
  fix
"""
from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

@lru_cache(maxsize=1)
def get_summariser():
    model_id = "google/flan-t5-base"        # light (250 MB) + permissive licence
    tok = AutoTokenizer.from_pretrained(model_id)
    mod = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    return pipeline("summarization", model=mod, tokenizer=tok)

def explain(text: str) -> str:
    pipe = get_summariser()
    out = pipe(
        text, max_length=60, min_length=20,
        do_sample=False
    )[0]["summary_text"]
    return out

# ――― GPT helper ――― #
# def _ask_gpt(user_text: str) -> Dict[str, Any]:
#     resp = openai.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": user_text}],
#         temperature=0
#     )
#     return json.loads(resp.choices[0].message.content)


# ――― Main ranking entrypoint ――― #
def rank(slither_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    detectors = slither_json.get("results", {}).get("detectors", [])
    sev_map = {
    "High":   9,   # critical & high
    "Medium": 6,   # medium
    "Low":    3,   # informational
    "Optimization": 2,
    "Informational": 2,
    }   

    ranked: List[Dict[str, Any]] = []
    for det in detectors:
        item = {
            "id": det.get("check") or det.get("id"),
            "description": det.get("description", "").strip(),
        }

        # try GPT first
        try:
            gpt = {
        "severity": sev_map.get(det.get("impact","Medium"), 5),
        "explanation": explain(item["description"]),
        "fix": ""    
            }
        except Exception as _:
            gpt = {
        "severity": sev_map.get(det.get("impact","Medium"), 5),
        "explanation": item["description"].split(".")[0],
        "fix": ""
            }

        item.update(gpt)
        ranked.append(item)

    ranked.sort(key=lambda x: -x["severity"])
    return ranked