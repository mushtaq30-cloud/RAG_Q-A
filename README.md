# RAG_Q-A
RAG Project for Q&amp;A

# 📘 RAG Q&A System — Complete Documentation

This project is a **Retrieval-Augmented Generation (RAG)** based Q&A System. It allows you to:
- Index documents using **FAISS**
- Retrieve the most relevant chunks using embeddings
- Feed retrieved context into an LLM (or fallback heuristic)
- Display answers + sources through a simple UI

This Readme explains:
1. Project structure
2. How FAISS indexing works
3. How to create documents
4. How to run locally
5. How to run with Docker
6. How to seed the FAISS index
7. How to test the API
8. UI usage guide
9. Troubleshooting

---

# 🔧 1. Project Structure
```
RAG_Q-A/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── rag.py
│   │   ├── vector_store.py
│   │   └── utils.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       └── test_vector_store.py
├── frontend/
│   ├── index.html
│   └── app.js
├── seed_data/
│   └── sample_docs.json
└── README.md
```

Backend → FastAPI server  
Frontend → Simple HTML+JS page  
FAISS → Vector index stored in `backend/data/faiss.index`

---

# 🧠 2. How RAG Works
RAG (Retrieval-Augmented Generation) improves answer quality by combining **retrieved documents** + **LLM reasoning**.

### Workflow:
1. User asks a question.
2. System generates an **embedding** vector for the query.
3. FAISS finds the **most similar document chunks**.
4. Backend builds a combined prompt containing the retrieved docs.
5. LLM receives the prompt and produces an answer.
6. Answer + sources returned to the UI.

If no OpenAI key is available, the system falls back to deterministic behavior (returns top doc).

---

# 🗂️ 3. Understanding Documents & FAISS Index

### What is a FAISS Index?
FAISS is a high‑performance vector search engine used for:
- Similarity search
- Nearest-neighbor lookup
- Embedding retrieval

Documents are converted into vectors using `sentence-transformers/all-MiniLM-L6-v2`, resulting in a `384-dim` embedding.

### How to Create Documents
Each document is a JSON object:
```json
{
  "id": "unique-id",
  "text": "Full text chunk to index",
  "meta": {"source": "filename or url"}
}
```

### Recommended Content
- Short factual paragraphs
- Technical explanations
- Guides or manuals
- FAQ snippets
- Clean, structured text

### Bad Content
- Raw HTML
- Very long paragraphs (>1500 chars)
- Noisy scraped text

### Chunking Strategy
If your docs are large, break them into chunks:
- Use 300–800 characters per chunk
- Add metadata: parent doc id, chunk index

Example chunk:
```json
{
  "id": "doc1_chunk_0",
  "text": "Python is a high‑level interpreted language...",
  "meta": {"parent": "doc1", "chunk": 0}
}
```

---

# ▶️ 4. Running the Project Locally (No Docker)

## Step 1 — Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 2 — Seed FAISS Index
```bash
python - <<'PY'
import json
from app.vector_store import FaissStore
with open("../seed_data/sample_docs.json") as f:
    docs = json.load(f)
s = FaissStore(path="data/faiss.index")
s.add(docs)
print("Seeded", s.count())
PY
```

## Step 3 — Start Backend
```bash
uvicorn app.main:app --reload --port 8001
```
Backend now available at:  
👉 `http://localhost:8001`

---

## Step 4 — Launch UI
```bash
cd ../frontend
python3 -m http.server 3001
```
Open in browser:  
👉 `http://localhost:3001`

Use the input box to ask questions.

---

# 🐳 5. Running with Docker

## Build image
```bash
cd backend
docker build -t rag-backend:local .
```

## Run container
```bash
docker run -p 8001:8001 rag-backend:local
```

FAISS index will live **inside container** unless you mount a volume.

---

# 🐙 6. Docker Compose (Recommended)
Create or use existing `docker-compose.yml`:
```yaml
version: "3.8"
services:
  rag:
    build: ./backend
    ports:
      - "8001:8001"
    volumes:
      - ./backend/data:/app/data
```
Start:
```bash
docker-compose up --build
```

---

# 📥 7. Testing the API

### Health Check
```bash
curl http://localhost:8001/health
```

### Add Document
```bash
curl -X POST http://localhost:8001/add \
  -H "Content-Type: application/json" \
  -d '{"id":"new1","text":"Python is a modern programming language."}'
```

### Ask a Question
```bash
curl "http://localhost:8001/qa?q=What+is+Python%3F"
```

---

# 🌐 8. UI Usage Guide
- Start backend → port **8001**
- Start frontend → port **3001**
- Type a question → click **Ask**
- UI fetches from:  
  `http://localhost:8001/qa?q=<question>`
- Answer + sources appear instantly

If LLM key missing → fallback answer shown.

---

# 🛠️ 9. Troubleshooting

### ❌ UI shows: *Error: TypeError: Failed to fetch*
Cause: CORS, wrong port, backend not running.
Fix:
1. Ensure backend running: `curl http://localhost:8001/health`
2. Ensure UI served using `python -m http.server`
3. Check CORS (already included in latest backend fixes)

### ❌ FAISS says index empty
You didn’t seed it.
Run:
```bash
python seed_data...
```

### ❌ Docker cannot access localhost backend
Inside containers use:  
`http://host.docker.internal:8001`

---

# 🎯 10. Summary
This RAG Implementation teaches:
- Building embeddings
- FAISS vector search
- RAG prompt building
- UI interaction
- Docker + local dev

You now have a working, production‑ready RAG foundation you can expand with:
- Better chunking
- Source ranking
- Reranker models
- Caching layer
- LLM function calling

---

Happy Building! 🚀