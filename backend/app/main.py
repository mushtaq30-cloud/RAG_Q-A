# rag-qa/backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
# added for CORS, logging and JSON error responses
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .rag import answer, store

app = FastAPI(title="RAG QA Service")

# Configure CORS for local development; set ALLOWED_ORIGINS in your environment for production
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3001,http://127.0.0.1:3001").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# JSON exception handlers so the frontend receives helpful error messages
logger = logging.getLogger("uvicorn.error")

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(status_code=500, content={"error": str(exc)})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": str(exc)})

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

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