#!/usr/bin/env python3
import json
import os
from app.vector_store import FaissStore

SEED_FILE = "seed_data/sample_docs.json"
INDEX_PATH = "data/faiss.index"


def load_seed_data(path: str):
    """Load documents from JSON seed file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Seed file not found: {path}")

    with open(path, "r") as f:
        return json.load(f)


def ensure_directories():
    """Ensure index folder exists."""
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)


def seed_index():
    print(f"🚀 Starting FAISS index seeding...")
    print(f"📄 Reading seed data from: {SEED_FILE}")

    docs = load_seed_data(SEED_FILE)

    ensure_directories()

    print(f"📦 Initializing FAISS store at: {INDEX_PATH}")
    store = FaissStore(path=INDEX_PATH)

    print(f"➕ Adding {len(docs)} documents...")
    store.add(docs)

    print(f"✅ Done. FAISS index now contains {store.count()} vectors.")


if __name__ == "__main__":
    try:
        seed_index()
    except Exception as e:
        print(f"❌ Error seeding index: {e}")
        raise