# rag-qa/backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .rag import answer, store

app = FastAPI(title="RAG QA Service")

class AddDoc(BaseModel):
    id: str
    text: str
    meta: dict = {}

@app.post("/add")
async def add_document(doc: AddDoc):
    store.add([{"id": doc.id, "text": doc.text, "meta": doc.meta}])
    return {"ok": True, "count": store.count()}

@app.get("/qa")
async def qa(q: str):
    res = answer(q)
    return res

@app.get("/health")
async def health():
    return {"status":"ok", "doc_count": store.count()}