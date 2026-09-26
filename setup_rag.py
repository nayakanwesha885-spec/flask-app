import os
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

import pickle
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# 1. Load free local embedding model (downloads automatically on first run ~90MB)
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./model_cache')

def load_and_chunk_pdfs(folder_path="knowledge_base"):
    chunks = []
    # Walk through main folder and subfolders (ayurvedic_guidelines, patent, etc.)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                print(f"Processing: {pdf_path}")
                try:
                    reader = PdfReader(pdf_path)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            for paragraph in text.split("\n\n"):
                                if len(paragraph.strip()) > 30:
                                    chunks.append(paragraph.strip())
                except Exception as e:
                    print(f"Error reading {pdf_path}: {e}")
    return chunks

print("Extracting text from knowledge_base...")
chunks = load_and_chunk_pdfs()

print(f"Extracted {len(chunks)} text chunks. Generating embeddings...")
embeddings = model.encode(chunks, show_progress_bar=True)

# 2. Save chunks and embeddings locally
with open("vector_store.pkl", "wb") as f:
    pickle.dump({"chunks": chunks, "embeddings": embeddings}, f)

print(f"Successfully saved vector store to vector_store.pkl!")