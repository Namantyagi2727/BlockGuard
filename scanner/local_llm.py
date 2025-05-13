from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

@lru_cache(maxsize=1)
def _summariser():
    model_id = "google/flan-t5-base"      # 250 MB, open licence
    tok = AutoTokenizer.from_pretrained(model_id)
    mod = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    return pipeline("summarization", model=mod, tokenizer=tok)

def explain(text: str) -> str:
    pipe = _summariser()
    out = pipe(text, max_length=60, min_length=20, do_sample=False)[0]
    return out["summary_text"]
