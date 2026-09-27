"""
setup_rag.py — Pre-build the vector store from local PDFs.

Run this locally to generate vector_store.pkl.
The pkl is loaded by app.py at startup (skips the slow embedding step on cold starts).

Usage:
    python setup_rag.py

Requirements:
    GEMINI_API_KEY must be set in .env or as an environment variable.
"""
import os
import re
import pickle
import numpy as np
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Please add it to your .env file.")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
EMBEDDING_MODEL = "text-embedding-004"


def embed_text(texts: list[str]) -> np.ndarray:
    """Embed a list of strings using the Gemini Embedding API."""
    vectors = []
    for i, text in enumerate(texts):
        try:
            result = gemini_client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text,
            )
            vectors.append(result.embeddings[0].values)
        except Exception as e:
            print(f"  [WARN] Failed to embed chunk {i}: {e}")
            vectors.append([0.0] * 768)
        if (i + 1) % 50 == 0:
            print(f"  Embedded {i + 1}/{len(texts)} chunks …")
    return np.array(vectors, dtype=np.float32)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if len(c) > 30]


def load_and_chunk_pdfs(folder_path: str = "knowledge_base") -> list[dict]:
    all_chunks = []
    for root, _, files in os.walk(folder_path):
        for filename in sorted(files):
            if not filename.lower().endswith(".pdf"):
                continue
            path = os.path.join(root, filename)
            print(f"Processing: {path}")
            try:
                reader = PdfReader(path)
                for page_num, page in enumerate(reader.pages, start=1):
                    text = (page.extract_text() or "").strip()
                    if not text:
                        continue
                    text = re.sub(r"\s+", " ", text)
                    for chunk in chunk_text(text):
                        all_chunks.append({
                            "text": chunk,
                            "filename": filename,
                            "page": page_num,
                        })
            except Exception as e:
                print(f"  [ERROR] Skipping {path}: {e}")
    return all_chunks


if __name__ == "__main__":
    print("=== TATVA RAG Vector Store Builder ===")
    print("Extracting text from knowledge_base/ …")
    chunks = load_and_chunk_pdfs()
    print(f"Extracted {len(chunks)} chunks.")

    print("Generating embeddings via Gemini API …")
    texts = [c["text"] for c in chunks]
    embeddings = embed_text(texts)

    output_path = "vector_store.pkl"
    with open(output_path, "wb") as fh:
        pickle.dump({"chunks": chunks, "embeddings": embeddings}, fh)

    print(f"\n✅ Saved {len(chunks)} chunks to {output_path}  ({os.path.getsize(output_path) / 1024 / 1024:.1f} MB)")
    print("\nNOTE: vector_store.pkl is in .gitignore.")
    print("Do NOT commit it to git — it will be rebuilt on Render at cold start.")