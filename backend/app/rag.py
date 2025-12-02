# rag-qa/backend/app/rag.py
import os
import json
from typing import List, Dict, Any

try:
    import openai
except Exception:
    openai = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

from .vector_store import FaissStore

store = FaissStore(path="data/faiss.index")

def build_prompt(question: str, docs: List[Dict[str, Any]]) -> str:
    docs_text = "\n\n".join([f"[{i}] {d['text']}" for i, d in enumerate(docs)])
    prompt = f"""You are an assistant that answers user questions using the provided documents.
Do not hallucinate beyond the provided documents. If the answer is not contained, say "I don't know".

Documents:
{docs_text}

Question: {question}

Answer concisely and at the end list sources by index (e.g., [0], [2]).
"""
    return prompt

def answer(question: str):
    docs = store.search(question, k=3)
    prompt = build_prompt(question, docs)
    # If OpenAI key available, call LLM. Otherwise fallback to deterministic answer (top doc summary).
    if OPENAI_API_KEY and openai:
        openai.api_key = OPENAI_API_KEY
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0.2,
            )
            text = resp.choices[0].message["content"]
            return {"answer": text, "sources": docs}
        except Exception as e:
            return {"answer": f"[LLM error] {str(e)}", "sources": docs}
    else:
        # fallback: return the first doc's first 400 chars as "answer" and include sources
        if docs:
            summary = docs[0]["text"][:400]
            return {"answer": summary, "sources": docs}
        else:
            return {"answer": "No documents available to answer the question.", "sources": []}