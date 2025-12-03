# rag-qa/backend/app/vector_store.py
import os
import pickle
from typing import List, Dict, Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Small embedding model for demos
EMBED_MODEL = "all-MiniLM-L6-v2"
DIM = 384  # embedding dim for the model above

class FaissStore:
    def __init__(self, path: str = "data/faiss.index"):
        self.path = path
        self.meta_path = f"{path}.meta"
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.embedder = SentenceTransformer(EMBED_MODEL)
        # if index exists, load; else create new flat index (inner product)
        if os.path.exists(self.path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.path)
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatIP(DIM)  # inner product (use normalized vectors)
            self.metadata: List[Dict[str, Any]] = []

    def _encode(self, texts: List[str]) -> np.ndarray:
        embs = self.embedder.encode(texts, convert_to_numpy=True)
        # normalize for cosine similarity with inner product
        faiss.normalize_L2(embs)
        return embs.astype("float32")

    def add(self, docs: List[Dict[str, Any]]):
        """
        docs: list of {"id": str, "text": str, "meta": {...} (optional)}
        """
        texts = [d["text"] for d in docs]
        embs = self._encode(texts)
        self.index.add(embs)
        self.metadata.extend(docs)
        faiss.write_index(self.index, self.path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def search(self, query: str, k: int = 3):
        qemb = self._encode([query])
        dists, ids = self.index.search(qemb, k)
        results = []
        for idx in ids[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

    def count(self) -> int:
        return self.index.ntotal