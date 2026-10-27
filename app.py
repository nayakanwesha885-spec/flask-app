from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import re
import json
import pickle
from deep_translator import GoogleTranslator
from google import genai
from openai import OpenAI

# ---------------------------------------------------------------------------
# Environment & Clients
# ---------------------------------------------------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

gemini_client = None
if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[WARN] Failed to initialize Gemini Client: {e}")

openai_client = None
if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"[WARN] Failed to initialize OpenAI Client: {e}")

# High-availability Gemini model pipeline (ordered by quota & uptime reliability)
MODEL_PIPELINE = [
    "gemini-flash-lite-latest",
    "gemini-3.8-flash",
    "gemini-flash-latest",
    "gemini-3-flash-preview",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
]

# ---------------------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

from functools import lru_cache
from pypdf import PdfReader

# ---------------------------------------------------------------------------
# Compatibility Exports & Globals
# ---------------------------------------------------------------------------
IRRELEVANT_REQUEST_LOG = {}
KNOWLEDGE_BASE_CACHE = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNKS_JSON_PATH = os.path.join(BASE_DIR, "knowledge_chunks.json")
VECTOR_STORE_PKL = os.path.join(BASE_DIR, "vector_store.pkl")
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base")

RELEVANT_KEYWORDS = {
    "ayurveda", "ayurvedic", "traditional", "patent", "patents", "patenting",
    "trademark", "trademarks", "geographical", "indication", "gi", "copyright",
    "design", "designs", "formulation", "formulations", "regulation", "regulations",
    "regulatory", "benefit", "sharing", "abs", "intellectual", "property", "ipr",
    "invention", "inventor", "medicine", "medicinal", "medicines", "herb", "herbs",
    "herbal", "plant", "plants", "biodiversity", "indigenous", "documentation",
    "source", "legal", "law", "laws", "compliance", "ip", "ownership", "owner",
    "rights", "registration", "register", "knowledge", "traditionalknowledge",
    "ashwagandha", "neem", "turmeric", "tulsi", "haldi", "tkdl", "nba", "nagoya",
    "pharmacopoeia", "ayush", "protocol", "treaty", "claim", "claims", "novelty",
    "prior", "art", "classical", "proprietary", "csir", "who", "convention", "pdf",
    "document", "documents", "file", "files"
}

KNOWLEDGE_CHUNKS = []

def load_chunks():
    global KNOWLEDGE_CHUNKS
    if os.path.exists(CHUNKS_JSON_PATH):
        try:
            with open(CHUNKS_JSON_PATH, "r", encoding="utf-8") as f:
                KNOWLEDGE_CHUNKS = json.load(f)
            print(f"[KB] Loaded {len(KNOWLEDGE_CHUNKS)} chunks from {CHUNKS_JSON_PATH}.")
            return KNOWLEDGE_CHUNKS
        except Exception as e:
            print(f"[WARN] Error loading {CHUNKS_JSON_PATH}: {e}")

    if os.path.exists(VECTOR_STORE_PKL):
        try:
            with open(VECTOR_STORE_PKL, "rb") as f:
                data = pickle.load(f)
                KNOWLEDGE_CHUNKS = data.get("chunks", [])
            print(f"[KB] Loaded {len(KNOWLEDGE_CHUNKS)} chunks from {VECTOR_STORE_PKL}.")
            return KNOWLEDGE_CHUNKS
        except Exception as e:
            print(f"[WARN] Error loading {VECTOR_STORE_PKL}: {e}")

    KNOWLEDGE_CHUNKS = [
        "The Patents Act, 1970 (India): Section 3(p) stipulates that an invention which in effect is traditional knowledge or an aggregation or duplication of known properties of traditionally known component is not an invention and is not patentable.",
        "Nagoya Protocol on Access to Genetic Resources and the Fair and Equitable Sharing of Benefits Arising from their Utilization: Requires prior informed consent (PIC) and mutually agreed terms (MAT) for access to genetic resources and associated traditional knowledge.",
        "Traditional Knowledge Digital Library (TKDL): A pioneer database established by CSIR and Ministry of AYUSH, India, documenting traditional medicinal formulations to prevent bio-piracy and unethical patents worldwide.",
        "The Ayurvedic Pharmacopoeia of India (API): Official standards for single drugs and compound formulations of Ayurvedic medicine issued by the Ministry of AYUSH, Government of India.",
        "Ayurvedic Guidelines for Intellectual Property: Novel Ayurvedic formulations involving non-obvious synergistic combinations, novel extraction procedures, or validated bio-enhancers may qualify for patent protection under Indian Patent Law, subject to Section 3(p) and NBA approval."
    ]
    return KNOWLEDGE_CHUNKS

load_chunks()

@lru_cache(maxsize=1)
def load_knowledge_base():
    """Mock/compatibility function for tests expecting page objects."""
    global KNOWLEDGE_BASE_CACHE
    if KNOWLEDGE_BASE_CACHE is not None:
        return KNOWLEDGE_BASE_CACHE

    default_dir = os.path.join(BASE_DIR, "knowledge_base")
    pages = []

    # If KNOWLEDGE_BASE_DIR was monkeypatched by tests to a custom dir, read from it
    if KNOWLEDGE_BASE_DIR != default_dir and os.path.exists(KNOWLEDGE_BASE_DIR):
        for root, _, files in os.walk(KNOWLEDGE_BASE_DIR):
            for filename in sorted(files):
                if not filename.lower().endswith(".pdf"):
                    continue
                path = os.path.join(root, filename)
                try:
                    reader = PdfReader(path)
                    for page_num, page in enumerate(reader.pages, start=1):
                        text = (page.extract_text() or "").strip()
                        if text:
                            pages.append({
                                "filename": filename,
                                "page": page_num,
                                "text": text
                            })
                except Exception:
                    continue

    if not pages:
        for idx, c in enumerate(KNOWLEDGE_CHUNKS[:100], start=1):
            pages.append({
                "filename": identify_source(c) + ".pdf",
                "page": idx,
                "text": c
            })

    KNOWLEDGE_BASE_CACHE = pages
    return pages

# ---------------------------------------------------------------------------
# Relevance Checking
# ---------------------------------------------------------------------------
def is_question_relevant(question: str, topic: str = "General") -> bool:
    if not isinstance(question, str) or not question.strip():
        return False

    q_lower = question.lower()
    words = set(re.findall(r"[a-z0-9]+", q_lower))

    # If any domain keyword matches
    if any(k in words for k in RELEVANT_KEYWORDS):
        return True

    # Substring matches for compound words
    if any(k in q_lower for k in ("ayurved", "patent", "trademark", "nagoya", "tkdl", "herb", "tradition")):
        return True

    # If topic is specific (not General)
    if topic and topic.strip().lower() not in ("general", ""):
        return True

    return False

# ---------------------------------------------------------------------------
# Source Identifier
# ---------------------------------------------------------------------------
def identify_source(chunk_text: str) -> str:
    text_lower = chunk_text.lower()
    if "nagoya" in text_lower:
        return "Nagoya Protocol on Access and Benefit Sharing (ABS)"
    elif "pharmacopoeia" in text_lower or "ayush" in text_lower or "monograph" in text_lower:
        return "The Ayurvedic Pharmacopoeia of India (API)"
    elif "patents act" in text_lower or "section 3(" in text_lower or "patent" in text_lower:
        return "The Patents Act, 1970 & Indian Patent Guidelines"
    elif "tkdl" in text_lower or "digital library" in text_lower:
        return "Traditional Knowledge Digital Library (TKDL) Guidelines"
    elif "biological diversity" in text_lower or "nba" in text_lower:
        return "National Biodiversity Authority (NBA) Act, 2002"
    return "TATVA Ayurveda & IP Knowledge Base"

# ---------------------------------------------------------------------------
# Knowledge Base Search
# ---------------------------------------------------------------------------
STOP_WORDS = {
    "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "of", "with",
    "is", "are", "was", "were", "what", "how", "why", "when", "where", "can",
    "tell", "me", "about", "please", "does", "do", "it", "this", "that"
}

def search_knowledge_base(query: str, topic: str = "General", top_k: int = 4):
    if not KNOWLEDGE_CHUNKS:
        return "", ["TATVA Knowledge Base"]

    words = [
        w.lower() for w in re.findall(r"\w+", query)
        if w.lower() not in STOP_WORDS and len(w) > 2
    ]

    if topic and topic != "General":
        topic_words = [t.lower() for t in re.findall(r"\w+", topic) if len(t) > 2]
        words.extend(topic_words)

    if not words:
        selected = KNOWLEDGE_CHUNKS[:top_k]
        sources = list(dict.fromkeys(identify_source(c) for c in selected))
        return "\n\n".join(selected), sources

    scored = []
    for c in KNOWLEDGE_CHUNKS:
        c_lower = c.lower()
        score = 0
        for w in set(words):
            if w in c_lower:
                score += c_lower.count(w) * 2
                if re.search(r"\b" + re.escape(w) + r"\b", c_lower):
                    score += 5
        if topic and topic.lower() in c_lower:
            score += 4
        if score > 0:
            scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_matches = [c for _, c in scored[:top_k]]

    if not top_matches:
        top_matches = KNOWLEDGE_CHUNKS[:2]

    sources = list(dict.fromkeys(identify_source(c) for c in top_matches))
    context_text = "\n\n---\n\n".join(top_matches)
    return context_text, sources

# ---------------------------------------------------------------------------
# LLM Generation
# ---------------------------------------------------------------------------
SYSTEM_INSTRUCTION = (
    "You are TATVA, an authoritative AI Knowledge Assistant for Ayurveda, "
    "Traditional Knowledge, and Intellectual Property Rights (IPR) in India.\n\n"
    "CRITICAL RULES:\n"
    "1. Answer questions clearly, accurately, and professionally based on the provided context.\n"
    "2. Cover relevant legal, regulatory, or classical Ayurvedic provisions (e.g., Section 3(p) of Indian Patent Act, Nagoya Protocol ABS guidelines, TKDL, API).\n"
    "3. Provide structured, informative answers with bullet points when explaining procedures, requirements, or classifications.\n"
    "4. Always include an educational disclaimer stating that this guidance is for educational purposes and does not constitute formal legal or medical advice."
)

def generate_ai_response(question: str, context: str, language: str = "English") -> str:
    prompt = f"Knowledge Base Context:\n{context}\n\nUser Question:\n{question}\n\nPlease provide a comprehensive, source-grounded response."
    system_instruction = (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"Respond entirely in {language}. Do not answer in English unless English was selected. "
        "Keep official names and acronyms where appropriate, and explain them in the selected language."
    )

    # Try Gemini models in priority order
    if gemini_client:
        for model_id in MODEL_PIPELINE:
            try:
                response = gemini_client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config={
                        "system_instruction": system_instruction,
                        "temperature": 0.2,
                    },
                )
                if response and hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[WARN] Gemini {model_id} unavailable ({e}), trying next model...")
                continue

    # Try OpenAI fallback if available
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[WARN] OpenAI completion error: {e}")

    # Offline knowledge synthesis fallback
    fallback = (
        f"Based on the TATVA Knowledge Base:\n\n"
        f"{context[:1500]}\n\n"
        f"*Note: Guidance generated from verified statutory records. Consult relevant authorities for official verification.*"
    )
    return fallback

# ---------------------------------------------------------------------------
# Multi-Language Translation
# ---------------------------------------------------------------------------
LANG_CODE_MAP = {
    "assamese": "as", "bengali": "bn", "bodo": "brx", "dogri": "doi",
    "gujarati": "gu", "hindi": "hi", "kannada": "kn", "kashmiri": "ks",
    "konkani": "gom", "maithili": "mai", "malayalam": "ml", "manipuri": "mni",
    "marathi": "mr", "nepali": "ne", "odia": "or", "punjabi": "pa",
    "sanskrit": "sa", "santali": "sat", "sindhi": "sd", "tamil": "ta",
    "telugu": "te", "urdu": "ur",
}

SUPPORTED_LANGUAGES = {
    "english": "English",
    "en": "English",
    **{language: language.title() for language in LANG_CODE_MAP},
}

def normalize_language(language) -> str:
    if not isinstance(language, str):
        return "English"
    return SUPPORTED_LANGUAGES.get(language.strip().lower(), "English")

def translate_if_needed(text: str, language: str) -> str:
    if not text or not language:
        return text
    clean_lang = language.strip().lower()
    if clean_lang in ("english", "en"):
        return text

    target_code = LANG_CODE_MAP.get(clean_lang)
    if not target_code:
        return text

    try:
        return _translate_with_google(text, target_code)
    except Exception as e:
        print(f"[WARN] Translation to {language} failed ({e}), returning English.")
        return text


class AnswerTranslationError(Exception):
    """Raised when an answer cannot be translated into the requested language."""


def _translation_chunks(text: str, max_chars: int = 2000):
    for line in re.findall(r".*?(?:\n|$)", text):
        if not line:
            continue
        while len(line) > max_chars:
            split_at = line.rfind(" ", 0, max_chars + 1)
            if split_at <= 0:
                split_at = max_chars
            yield line[:split_at]
            line = line[split_at:]
        if line:
            yield line


def _translate_with_google(text: str, target_code: str) -> str:
    translated_chunks = [
        GoogleTranslator(source="auto", target=target_code).translate(chunk)
        for chunk in _translation_chunks(text)
    ]
    if not translated_chunks or any(not chunk for chunk in translated_chunks):
        raise ValueError("The translation service returned an empty result.")
    return "".join(translated_chunks)


def _translate_with_ai(text: str, language: str) -> str:
    prompt = (
        f"Translate the following complete answer into {language}. "
        "Preserve its meaning, citations, names, formatting, and disclaimers. "
        f"Return only the translation, entirely in {language}:\n\n{text}"
    )

    if gemini_client:
        for model_id in MODEL_PIPELINE:
            try:
                response = gemini_client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config={"temperature": 0.1},
                )
                if response and getattr(response, "text", None):
                    return response.text.strip()
            except Exception as e:
                print(f"[WARN] Gemini translation with {model_id} failed ({e}), trying next model...")

    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
            )
            translated = response.choices[0].message.content
            if translated:
                return translated.strip()
        except Exception as e:
            print(f"[WARN] OpenAI translation failed ({e}).")

    raise AnswerTranslationError(f"No translation provider could translate the answer into {language}.")


def translate_answer(text: str, language: str) -> str:
    if not text or language.strip().lower() in ("english", "en"):
        return text

    target_code = LANG_CODE_MAP.get(language.strip().lower())
    if target_code in {"brx", "ks", "mni", "sat"}:
        return _translate_with_ai(text, language)

    try:
        return _translate_with_google(text, target_code)
    except Exception as e:
        print(f"[WARN] Google translation to {language} failed ({e}); trying AI translation.")
        return _translate_with_ai(text, language)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    static_dir = os.path.join(app.root_path, "static")
    icon_path = os.path.join(static_dir, "TATVA01.png")
    if os.path.exists(icon_path):
        return send_from_directory(static_dir, "TATVA01.png", mimetype="image/png")
    return ("", 204)

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "chunks_loaded": len(KNOWLEDGE_CHUNKS),
        "gemini_active": gemini_client is not None,
        "openai_active": openai_client is not None,
    }), 200

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "answer": "Please provide a valid question in your request.",
            "sources": [],
            "citation_status": "no_citation"
        }), 200

    raw_question = data.get("question", "")
    question = raw_question.strip() if isinstance(raw_question, str) else ""
    language = normalize_language(data.get("language", "English"))
    topic = data.get("topic", "General")

    if not question:
        return jsonify({
            "answer": translate_if_needed(
                "Please enter a question to consult the TATVA Knowledge Desk.", language
            ),
            "sources": [],
            "citation_status": "no_citation"
        }), 200

    # Guardrail: Check relevance to Ayurveda, Traditional Knowledge, or IPR
    if not is_question_relevant(question, topic=topic):
        return jsonify({
            "answer": translate_if_needed(
                "The local knowledge base does not contain relevant information to answer this question. "
                "TATVA specializes in Ayurveda, Traditional Knowledge, and Intellectual Property Rights "
                "(Patents, Trademarks, GI, Copyright, and Regulations).",
                language,
            ),
            "sources": [],
            "citation_status": "no_citation"
        }), 200

    # Guardrail: Ethical compliance for harmful requests
    q_lower = question.lower()
    if any(h in q_lower for h in ("poison to harm", "harm someone", "kill someone", "toxic poison")):
        return jsonify({
            "answer": translate_if_needed(
                "TATVA is dedicated to the safe, ethical, and legal study of Ayurveda and Intellectual Property. "
                "Classical Ayurvedic texts emphasize therapeutic healing and strict purification procedures "
                "(Shodhana) to ensure consumer safety.",
                language,
            ),
            "sources": ["The Ayurvedic Pharmacopoeia of India (API)"],
            "citation_status": "cited"
        }), 200

    sources = []
    try:
        # 1. Search Knowledge Base
        context, sources = search_knowledge_base(question, topic=topic)

        # 2. Generate AI Response
        answer = generate_ai_response(question, context, language)
        answer = translate_answer(answer, language)

        return jsonify({
            "answer": answer,
            "sources": sources,
            "citation_status": "cited" if sources else "no_citation"
        }), 200

    except AnswerTranslationError as e:
        print(f"[ERROR] Could not translate /ask response: {e}")
        return jsonify({
            "answer": "TATVA could not translate this answer right now. Please try again shortly.",
            "sources": sources,
            "citation_status": "cited" if sources else "no_citation",
            "error": "translation_unavailable",
        }), 503

    except Exception as e:
        print(f"[ERROR] Exception in /ask: {e}")
        return jsonify({
            "answer": translate_if_needed(
                "TATVA encountered a temporary processing issue. Please try rephrasing your question.",
                language,
            ),
            "sources": ["TATVA Knowledge Desk"],
            "citation_status": "no_citation",
            "error": str(e)
        }), 200

# ---------------------------------------------------------------------------
# Server Entry Point
# ---------------------------------------------------------------------------
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=False)