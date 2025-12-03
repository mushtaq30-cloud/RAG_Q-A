# rag-qa/backend/app/utils.py
from .vector_store import FaissStore

# simple helper to expose the store for seeding from scripts/tests
_store = FaissStore(path="data/faiss.index")

def get_store():
    return _store