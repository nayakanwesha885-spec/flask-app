from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import re
import pickle
import threading
from functools import lru_cache
from openai import OpenAI
from google import genai
from deep_translator import GoogleTranslator
import numpy as np

# ---------------------------------------------------------------------------
# Network optimization: prefer IPv4 to prevent IPv6 DNS/connect timeouts
# ---------------------------------------------------------------------------
import socket
_original_getaddrinfo = socket.getaddrinfo
def _ipv4_first_getaddrinfo(*args, **kwargs):
    res = _original_getaddrinfo(*args, **kwargs)
    ipv4 = [r for r in res if r[0] == socket.AF_INET]
    return ipv4 if ipv4 else res
socket.getaddrinfo = _ipv4_first_getaddrinfo

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# ---------------------------------------------------------------------------
# Model pipeline
# ---------------------------------------------------------------------------
MODEL_PIPELINE = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-flash-latest",
]
EMBEDDING_MODEL = "gemini-embedding-001"   # Gemini embedding model
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_VECTOR_STORE_ID = os.getenv("OPENAI_VECTOR_STORE_ID")


def generate_response(prompt: str):
    import time
    primary = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    models_to_try = [primary] + [m for m in MODEL_PIPELINE if m != primary]
    last_err = None
    for model_id in models_to_try:
        for attempt in range(2):
            try:
                return client.models.generate_content(model=model_id, contents=prompt)
            except Exception as e:
                last_err = e
                err_str = str(e)
                print(f"[WARN] {model_id} (attempt {attempt+1}) failed: {e}")
                if "503" in err_str or "high demand" in err_str.lower():
                    time.sleep(1.5)
                    continue
                break
    raise RuntimeError(f"All Gemini model endpoints failed: {last_err}")


def embed_text(texts: list) -> np.ndarray:
    """Embed strings via Gemini API (768 dimensions). Falls back to zero-vectors on error."""
    vectors = []
    for text in texts:
        try:
            result = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text,
                config={"output_dimensionality": 768}
            )
            vectors.append(result.embeddings[0].values)
        except Exception as e:
            print(f"[WARN] embed_text failed: {e}")
            vectors.append([0.0] * 768)   # dim = 768
    return np.array(vectors, dtype=np.float32)


# ---------------------------------------------------------------------------
# Flask app — created BEFORE any startup work so gunicorn can import it
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# ---------------------------------------------------------------------------
# Vector store state
# ---------------------------------------------------------------------------
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store.pkl")
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")

_kb_chunks: list = []
_kb_embeddings: np.ndarray = np.empty((0, 768), dtype=np.float32)
_kb_ready = False          # True once the vector store is loaded/built
_kb_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Helpers: chunking and building
# ---------------------------------------------------------------------------

def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if len(c) > 30]


def _build_vector_store():
    """Read PDFs, chunk them, embed via Gemini. Called in a background thread."""
    global _kb_chunks, _kb_embeddings, _kb_ready

    raw_chunks = []
    for root, _, files in os.walk(KNOWLEDGE_BASE_DIR):
        for filename in sorted(files):
            if not filename.lower().endswith(".pdf"):
                continue
            path = os.path.join(root, filename)
            print(f"[RAG] Processing: {path}")
            try:
                reader = PdfReader(path)
                for page_num, page in enumerate(reader.pages, start=1):
                    text = (page.extract_text() or "").strip()
                    if not text:
                        continue
                    text = re.sub(r"\s+", " ", text)
                    for chunk in _chunk_text(text):
                        raw_chunks.append({
                            "text": chunk,
                            "filename": filename,
                            "page": page_num,
                        })
            except Exception as e:
                print(f"[WARN] Skipping {path}: {e}")

    if not raw_chunks:
        print("[RAG] No PDF chunks found.")
        with _kb_lock:
            _kb_ready = True
        return

    print(f"[RAG] Embedding {len(raw_chunks)} chunks …")
    texts = [c["text"] for c in raw_chunks]
    embeddings = embed_text(texts)

    with _kb_lock:
        _kb_chunks = raw_chunks
        _kb_embeddings = embeddings
        _kb_ready = True

    # Try to persist (may fail on read-only filesystems — that's OK)
    try:
        with open(VECTOR_STORE_PATH, "wb") as fh:
            pickle.dump({"chunks": raw_chunks, "embeddings": embeddings}, fh)
        print(f"[RAG] Saved vector store ({len(raw_chunks)} chunks)")
    except Exception as e:
        print(f"[WARN] Could not save vector store: {e}")


def _load_or_build_vector_store():
    """Try to load a pre-built pkl, otherwise build in background thread."""
    global _kb_chunks, _kb_embeddings, _kb_ready

    if os.path.exists(VECTOR_STORE_PATH):
        print(f"[RAG] Loading pre-built vector store …")
        try:
            with open(VECTOR_STORE_PATH, "rb") as fh:
                data = pickle.load(fh)
            with _kb_lock:
                _kb_chunks = data["chunks"]
                _kb_embeddings = np.array(data["embeddings"], dtype=np.float32)
                _kb_ready = True
            print(f"[RAG] Loaded {len(_kb_chunks)} chunks from disk.")
            return
        except Exception as e:
            print(f"[WARN] Could not load vector store: {e}. Rebuilding …")

    # Build in background so gunicorn binds the port immediately
    print("[RAG] Starting background vector store build …")
    t = threading.Thread(target=_build_vector_store, daemon=True)
    t.start()


# Start loading/building immediately when the module is imported
_load_or_build_vector_store()


# ---------------------------------------------------------------------------
# RAG: cosine similarity search
# ---------------------------------------------------------------------------

def get_relevant_context(user_query: str, top_k: int = 3):
    with _kb_lock:
        ready = _kb_ready
        chunks = _kb_chunks
        embeddings = _kb_embeddings

    if not ready or len(chunks) == 0 or embeddings.size == 0:
        return "", []

    try:
        q_vec = embed_text([user_query])[0]
        # Check for dimension mismatch (e.g. if pre-built vector store has different dim)
        if embeddings.ndim != 2 or embeddings.shape[1] != len(q_vec):
            print(f"[WARN] Vector dimension mismatch: kb has {embeddings.shape}, query has {len(q_vec)}. Using keyword search.")
            return "", []

        norm_q = np.linalg.norm(q_vec) + 1e-9
        norm_kb = np.linalg.norm(embeddings, axis=1) + 1e-9
        sims = embeddings @ q_vec / (norm_kb * norm_q)

        top_idx = np.argsort(sims)[::-1][:top_k]
        matched_chunks, sources = [], []

        for i in top_idx:
            if sims[i] < 0.15:
                continue
            chunk = chunks[i]
            if isinstance(chunk, dict):
                text = chunk.get("text", "")
                sources.append({
                    "filename": chunk.get("filename", "Ayurvedic Document"),
                    "page": chunk.get("page", "N/A"),
                })
            else:
                text = str(chunk)
                sources.append({
                    "filename": "Ayurvedic Document",
                    "page": "N/A",
                })
            matched_chunks.append(text)

        return "\n\n".join(matched_chunks), sources
    except Exception as e:
        print(f"[WARN] Error in get_relevant_context: {e}")
        return "", []


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SUPPORTED_LANGUAGES = {
    "English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi",
    "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri",
    "Marathi", "Nepali", "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi",
    "Tamil", "Telugu", "Urdu",
}
TRANSLATION_LANGUAGE_GUIDANCE = {
    "Assamese": "Assamese (অসমীয়া, Assamese script)",
    "Bengali": "Bengali (বাংলা, Bengali script)",
    "Bodo": "Bodo (बड़ो, Devanagari script)",
    "Dogri": "Dogri (डोगरी, Devanagari script)",
    "Gujarati": "Gujarati (ગુજરાતી, Gujarati script)",
    "Hindi": "Hindi (हिन्दी, Devanagari script)",
    "Kannada": "Kannada (ಕನ್ನಡ, Kannada script)",
    "Kashmiri": "Kashmiri (कॉशुर, native Kashmiri script)",
    "Konkani": "Konkani (कोंकणी, Devanagari script)",
    "Maithili": "Maithili (मैथिली, Devanagari script)",
    "Malayalam": "Malayalam (മലയാളം, Malayalam script)",
    "Manipuri": "Manipuri (মৈতৈলোন্, Meitei script)",
    "Marathi": "Marathi (मराठी, Devanagari script)",
    "Nepali": "Nepali (नेपाली, Devanagari script)",
    "Odia": "Odia (ଓଡ଼ିଆ, Odia script)",
    "Punjabi": "Punjabi (ਪੰਜਾਬੀ, Gurmukhi script)",
    "Sanskrit": "Sanskrit (संस्कृतम्, Devanagari script)",
    "Santali": "Santali (ᱥᱟᱱᱛᱟᱲᱤ, Ol Chiki script)",
    "Sindhi": "Sindhi (سنڌي, Sindhi script)",
    "Tamil": "Tamil (தமிழ், Tamil script)",
    "Telugu": "Telugu (తెలుగు, Telugu script)",
    "Urdu": "Urdu (اردو, Urdu script)",
}
STOP_WORDS = {
    "a", "an", "and", "are", "about", "for", "how", "in", "is", "of", "on",
    "the", "to", "what", "which", "with", "can", "does", "do", "from", "under",
    "according", "based", "say", "says", "said", "pdf", "document", "documents",
    "file", "files", "uploaded", "upload",
}
MAX_QUESTION_LENGTH = 2000
KNOWLEDGE_BASE_CACHE = None


# ---------------------------------------------------------------------------
# Knowledge base page lookup (for source citations)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_knowledge_base() -> list:
    global KNOWLEDGE_BASE_CACHE
    if KNOWLEDGE_BASE_CACHE is not None:
        return KNOWLEDGE_BASE_CACHE

    pages = []
    for root, _, files in os.walk(KNOWLEDGE_BASE_DIR):
        for filename in sorted(files):
            if not filename.lower().endswith(".pdf"):
                continue
            path = os.path.join(root, filename)
            try:
                reader = PdfReader(path)
            except Exception as error:
                print(f"SKIPPING unreadable PDF: {path} ({error})")
                continue
            for page_number, page in enumerate(reader.pages, start=1):
                try:
                    text = (page.extract_text() or "").strip()
                except Exception:
                    continue
                if text:
                    pages.append({
                        "filename": filename,
                        "page": page_number,
                        "text": re.sub(r"\s+", " ", text),
                    })

    KNOWLEDGE_BASE_CACHE = pages
    return KNOWLEDGE_BASE_CACHE


def ensure_knowledge_base_loaded():
    if KNOWLEDGE_BASE_CACHE is None:
        return load_knowledge_base()
    return KNOWLEDGE_BASE_CACHE


def find_source_page(filename: str, text: str):
    normalized = " ".join(text.lower().split())
    matching = [p for p in ensure_knowledge_base_loaded() if p["filename"] == filename]
    for p in matching:
        if normalized and normalized in p["text"].lower():
            return p["page"]

    search_terms = {
        t for t in re.findall(r"[a-z0-9]+", normalized)
        if len(t) > 3 and t not in STOP_WORDS
    }
    if not search_terms:
        return None

    best_page, best_score = None, 0
    for p in matching:
        page_terms = set(re.findall(r"[a-z0-9]+", p["text"].lower()))
        score = len(search_terms & page_terms)
        if score > best_score:
            best_page, best_score = p, score
    return best_page["page"] if best_page and best_score >= 3 else None


def extract_question_terms(question: str) -> set:
    return {
        term.lower() for term in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)?", question)
        if term.lower() not in STOP_WORDS and len(term) > 1
    }


def retrieve_pages(question: str, topic: str = "General") -> list:
    """OpenAI Vector Store → Gemini embedding search → keyword fallback."""
    # 1. OpenAI Vector Store (if configured)
    if openai_client and OPENAI_VECTOR_STORE_ID:
        try:
            query = question if topic == "General" else f"{topic}: {question}"
            results = openai_client.vector_stores.search(
                vector_store_id=OPENAI_VECTOR_STORE_ID,
                query=query,
                max_num_results=3,
                rewrite_query=True,
            )
            vector_pages = []
            for result in results.data:
                text = "".join(
                    c.text for c in result.content if c.type == "text"
                ).strip()
                if text:
                    raw_fn = getattr(result, "filename", "") or ""
                    clean_fn = os.path.basename(raw_fn) if raw_fn else "Ayurvedic Document"
                    page_no = find_source_page(raw_fn, text) or 1
                    vector_pages.append({
                        "filename": clean_fn,
                        "page": page_no,
                        "text": text,
                    })
            if vector_pages:
                return vector_pages
        except Exception as error:
            print("VECTOR STORE ERROR:", error)

    # 2. Local Gemini-embedding search
    context_text, sources = get_relevant_context(question)
    if context_text:
        pages = []
        for src in sources:
            pages.append({
                "filename": src.get("filename", "Ayurvedic Document"),
                "page": src.get("page", "N/A"),
                "text": context_text,
            })
        return pages

    # 3. Fast in-memory keyword search across pre-loaded chunks
    terms = extract_question_terms(question)
    if topic != "General":
        terms.update(t.lower() for t in topic.split() if len(t) > 2)

    with _kb_lock:
        chunks = list(_kb_chunks)

    scored = []
    for chunk in chunks:
        if isinstance(chunk, dict):
            text = chunk.get("text", "")
            filename = chunk.get("filename", "Ayurvedic Document")
            page_no = chunk.get("page", 1)
        else:
            text = str(chunk)
            filename = "Ayurvedic Document"
            page_no = 1

        haystack = text.lower()
        score = sum(haystack.count(t) for t in terms)
        if topic.lower() in filename.lower():
            score += 3
        if score > 0:
            scored.append((score, {
                "filename": filename,
                "page": page_no,
                "text": text,
            }))

    if scored:
        scored.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scored[:3]]

    return []


# ---------------------------------------------------------------------------
# Translation
# ---------------------------------------------------------------------------

LANG_CODES = {
    "assamese": "as", "bengali": "bn", "bodo": "brx", "dogri": "doi",
    "gujarati": "gu", "hindi": "hi", "kannada": "kn", "kashmiri": "ks",
    "konkani": "gom", "maithili": "mai", "malayalam": "ml", "manipuri": "mni",
    "marathi": "mr", "nepali": "ne", "odia": "or", "punjabi": "pa",
    "sanskrit": "sa", "santali": "sat", "sindhi": "sd", "tamil": "ta",
    "telugu": "te", "urdu": "ur",
}


def translate_answer(answer: str, language: str) -> str:
    if not answer or not str(answer).strip():
        return answer
    if len(answer) > 3000:
        answer = answer[:3000]
    clean_lang = str(language).strip().lower()
    if clean_lang in ("english", "en"):
        return answer
    target_code = LANG_CODES.get(clean_lang, "hi")
    try:
        translated = GoogleTranslator(source="auto", target=target_code).translate(answer)
        return translated if translated else answer
    except Exception as error:
        print("TRANSLATION ERROR:", error)
        return answer


# ---------------------------------------------------------------------------
# Relevance guardrail
# ---------------------------------------------------------------------------

def is_relevant_context(question: str, excerpts: list) -> bool:
    ignore = {
        "what", "is", "how", "can", "the", "a", "an", "in", "of", "for",
        "to", "about", "with", "tell", "me", "give", "where", "who", "why",
        "does", "do", "which", "when", "should", "would", "could", "please",
        "help", "are", "there", "any", "define", "explain", "describe",
    }
    raw_words = [
        w.strip("?,.!'\"()[]{}")
        for w in question.lower().split()
        if w.strip("?,.!'\"()[]{}") not in ignore and len(w) > 2
    ]
    words = list(set(raw_words))
    if not words:
        return True

    combined = " ".join(excerpts).lower()
    matched = []
    for w in words:
        stem = w[:4] if len(w) >= 5 else w
        if re.search(r"\b" + re.escape(stem), combined):
            matched.append(w)

    ratio = len(matched) / len(words)
    return ratio >= 0.25 or len(matched) >= 1


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    """Health check — returns 200 immediately even while RAG is building."""
    return jsonify({"status": "ok", "rag_ready": _kb_ready})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"answer": "Please send a valid JSON request.", "error": "invalid_request"}), 400

    raw_question = data.get("question", "")
    question = raw_question.strip() if isinstance(raw_question, str) else ""
    language = data.get("language", "English")

    if not question:
        return jsonify({"answer": "Please enter a valid question.", "sources": []})

    if len(question) > MAX_QUESTION_LENGTH:
        return jsonify({"answer": "Question is too long. Please keep it under 2000 characters."}), 400

    # If RAG is still being built, warn but still try to answer via Gemini
    if not _kb_ready:
        print("[INFO] RAG not ready yet — answering without context.")

    topic = data.get("topic", "General")

    try:
        pages = retrieve_pages(question, topic=topic)

        sources = []
        for page in pages:
            src_str = f"{page['filename']} (Page {page['page']})"
            if src_str not in sources:
                sources.append(src_str)

        context = "\n\n".join(page["text"] for page in pages)

        system_instruction = (
            "You are TATVA, an evidence-led AI Knowledge Assistant specialising in Ayurveda, "
            "Traditional Knowledge, Nagoya Protocol / Access and Benefit Sharing (ABS), "
            "Patents, Trademarks, Geographical Indications, and Indian IPR Regulations. "
            "Provide helpful, accurate, well-structured and professional guidance. "
            "When the provided Knowledge Base Context contains relevant information, reference it directly. "
            "If the context is general or does not mention the specific topic, provide an accurate, authoritative answer "
            "based on established Ayurveda, biodiversity, and intellectual property frameworks."
        )
        user_prompt = (
            f"Topic: {topic}\n\n"
            f"Knowledge Base Context:\n{context if context.strip() else 'No direct context excerpt available.'}\n\n"
            f"User Question: {question}"
        )
        if language and language.lower() not in ("english", "en"):
            user_prompt += f"\n\nPlease provide your answer in {language}."

        full_prompt = f"{system_instruction}\n\n{user_prompt}"
        response = generate_response(full_prompt)
        answer = response.text if hasattr(response, "text") else str(response)

        if language and language.lower() not in ("english", "en"):
            answer = translate_answer(answer, language)

        return jsonify({
            "answer": answer,
            "sources": sources,
            "citation_status": "complete" if sources else "no_citation",
        })

    except Exception as e:
        print("ERROR IN /ask:", e)
        return jsonify({
            "answer": f"I encountered an issue processing your query: {str(e)}. Please try asking again in a moment.",
            "sources": [],
            "error": "server_error"
        }), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=False)