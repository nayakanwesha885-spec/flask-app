from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import re
import time
from functools import lru_cache
from openai import OpenAI
from google import genai
from deep_translator import GoogleTranslator
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_PIPELINE = [
    'gemini-3.6-flash',
    'gemini-3.5-flash',
    'gemini-1.5-flash'
]

def generate_response(prompt):
    for model_id in MODEL_PIPELINE:
        try:
            return client.models.generate_content(
                model=model_id,
                contents=prompt
            )
        except Exception as e:
            print(f"Error on {model_id}, trying next model: {e}")
            continue
    raise Exception("All Gemini model endpoints failed to generate a response.")
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
# Initialize SentenceTransformer and load vector store
embedding_model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./model_cache')

with open("vector_store.pkl", "rb") as f:
    data = pickle.load(f)
    kb_chunks = data["chunks"]
    kb_embeddings = data["embeddings"]

def get_relevant_context(user_query, top_k=3):
    query_vector = embedding_model.encode([user_query])[0]
    norm_query = np.linalg.norm(query_vector)
    norm_kb = np.linalg.norm(kb_embeddings, axis=1)
    similarities = np.dot(kb_embeddings, query_vector) / (norm_kb * norm_query)
    
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    matched_chunks = []
    sources = []
    
    for i in top_indices:
        if similarities[i] > 0.15:
            chunk = kb_chunks[i]
            matched_chunks.append(chunk if isinstance(chunk, str) else chunk.get("text", ""))
            
            # Extract metadata if available, or build source object
            if isinstance(chunk, dict):
                sources.append({
                    "filename": chunk.get("filename", "Ayurvedic Document"),
                    "page": chunk.get("page", "N/A")
                })
            else:
                # If kb_chunks stores raw strings, look up page number
                page_num = find_source_page("knowledge_base.pdf", chunk)
                sources.append({
                    "filename": "Knowledge Base Document",
                    "page": page_num if page_num else "N/A"
                })
                
    context_text = "\n\n".join(matched_chunks)
    return context_text, sources

SUPPORTED_LANGUAGES = {
    "English",
    "Assamese",
    "Bengali",
    "Bodo",
    "Dogri",
    "Gujarati",
    "Hindi",
    "Kannada",
    "Kashmiri",
    "Konkani",
    "Maithili",
    "Malayalam",
    "Manipuri",
    "Marathi",
    "Nepali",
    "Odia",
    "Punjabi",
    "Sanskrit",
    "Santali",
    "Sindhi",
    "Tamil",
    "Telugu",
    "Urdu",
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
SUPPORTED_TOPICS = {
    "General",
    "Patents",
    "Trademarks",
    "Geographical Indications",
    "Copyright",
    "Designs",
    "Ayurveda Regulations",
    "Traditional Knowledge",
}
MAX_QUESTION_LENGTH = 2000
MAX_SOURCES = 8
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_VECTOR_STORE_ID = os.getenv("OPENAI_VECTOR_STORE_ID")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
GEMINI_FALLBACK_MODEL = "gemini-3.5-flash-lite"
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) if os.getenv("GEMINI_API_KEY") else None

KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
STOP_WORDS = {
    "a", "an", "and", "are", "about", "for", "how", "in", "is", "of", "on",
    "the", "to", "what", "which", "with", "can", "does", "do", "from", "under",
    "according", "based", "say", "says", "said", "pdf", "document", "documents",
    "file", "files", "uploaded", "upload"
}
KNOWLEDGE_BASE_CACHE = None
IRRELEVANT_REQUEST_LOG = {}
IRRELEVANT_REQUEST_LIMIT = 3
IRRELEVANT_REQUEST_WINDOW_SECONDS = 60
RELEVANCE_KEYWORDS = {
    "ayurveda", "ayurvedic", "traditional", "patent", "patents",
    "trademark", "trademarks", "geographical", "indication", "gi", "copyright",
    "design", "designs", "formulation", "formulations", "regulation", "regulations",
    "regulatory", "benefit", "sharing", "abs", "intellectual", "property", "ipr",
    "invention", "inventor", "medicine", "medicinal", "medicines", "herb", "herbs",
    "herbal", "plant", "plants", "biodiversity", "indigenous", "documentation",
    "source", "legal", "law", "laws", "compliance", "ip", "ownership", "owner",
    "rights", "registration", "register", "knowledge", "traditionalknowledge"
}
DOCUMENT_REFERENCE_KEYWORDS = {"pdf", "document", "documents", "file", "files", "uploaded"}


def extract_question_terms(question):
    terms = {
        term.lower() for term in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)?", question)
        if term.lower() not in STOP_WORDS and len(term) > 1
    }
    return terms


def is_question_relevant(question, topic):
    if not isinstance(question, str):
        return False

    normalized_question = " ".join(re.sub(r"[^a-z0-9\s]", " ", question.lower()).split())
    if not normalized_question:
        return False

    return True


def get_client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown-client"


def check_irrelevant_request_limit(question):
    return False


@lru_cache(maxsize=1)
def load_knowledge_base():
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
                except Exception as error:
                    print(f"SKIPPING unreadable page {page_number} in {filename}: {error}")
                    continue

                if text:
                    pages.append({
                        "filename": filename,
                        "page": page_number,
                        "text": re.sub(r"\s+", " ", text)
                    })

    KNOWLEDGE_BASE_CACHE = pages
    return KNOWLEDGE_BASE_CACHE


def ensure_knowledge_base_loaded():
    if KNOWLEDGE_BASE_CACHE is None:
        return load_knowledge_base()
    return KNOWLEDGE_BASE_CACHE


def find_source_page(filename, text):
    normalized_text = " ".join(text.lower().split())
    matching_pages = [
        page for page in ensure_knowledge_base_loaded()
        if page["filename"] == filename
    ]

    for page in matching_pages:
        if normalized_text and normalized_text in page["text"].lower():
            return page["page"]

    search_terms = {
        term for term in re.findall(r"[a-z0-9]+", normalized_text)
        if len(term) > 3 and term not in STOP_WORDS
    }
    if not search_terms:
        return None

    best_page = None
    best_score = 0
    for page in matching_pages:
        page_terms = set(re.findall(r"[a-z0-9]+", page["text"].lower()))
        score = len(search_terms & page_terms)
        if score > best_score:
            best_page = page
            best_score = score

    return best_page["page"] if best_page and best_score >= 3 else None


def retrieve_pages(question, topic):
    if openai_client is not None and OPENAI_VECTOR_STORE_ID:
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
                    content.text for content in result.content if content.type == "text"
                ).strip()
                if text:
                    # 1. Clean and resolve the real PDF filename
                    raw_fn = getattr(result, "filename", "") or ""
                    if not raw_fn or raw_fn == "Knowledge Base Document" or len(raw_fn) > 30:
                        clean_filename = "patent act.pdf"
                    else:
                        clean_filename = os.path.basename(raw_fn)

                    # 2. Extract page number
                    page_no = find_source_page(getattr(result, "filename", ""), text) or 1

                    vector_pages.append({
                        "filename": clean_filename,
                        "page": page_no,
                        "text": text,
                    })

            if vector_pages:
                return vector_pages

        except Exception as error:
            print("VECTOR STORE ERROR:", error)

    terms = extract_question_terms(question)
    if topic != "General":
        terms.update(term.lower() for term in topic.split() if len(term) > 2)

    scored_pages = []
    for page in ensure_knowledge_base_loaded():
        haystack = page["text"].lower()
        score = sum(haystack.count(term) for term in terms)
        if topic.lower() in page["filename"].lower():
            score += 3
        if score:
            scored_pages.append((score, page))

    scored_pages.sort(key=lambda item: item[0], reverse=True)
    pages = [page for _, page in scored_pages[:3]]
    if not pages:
        return []
    return pages


class TranslationUnavailableError(RuntimeError):
    def __init__(self, message, code="translation_unavailable"):
        super().__init__(message)
        self.code = code


def translate_with_openai(answer, language):
    if openai_client is None:
        return None

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"Translate the answer completely into {TRANSLATION_LANGUAGE_GUIDANCE[language]}. "
                    "Use the requested native script for every explanatory sentence. "
                    "Do not return English prose. "
                    "Preserve filenames, page numbers, bullet structure, "
                    "and the educational disclaimer. Return only the translation."
                ),
            },
            {"role": "user", "content": answer},
        ],
        temperature=0,
    )
    translated = response.choices[0].message.content
    if not translated or not translated.strip():
        return None
    return translated.strip()


def translate_answer(answer, language):
    # GUARDRAIL 1: Stop if input text is empty
    if not answer or not str(answer).strip():
        return answer

    # GUARDRAIL 2: Limit maximum text length to prevent timeouts
    if len(answer) > 3000:
        answer = answer[:3000]

    # Clean the language input
    clean_lang = str(language).strip().lower()

    # GUARDRAIL 3: Skip translation if language is English
    if clean_lang in ["english", "en"]:
        return answer

    # GUARDRAIL 4: Map language to code safely
    target_code = "hi"  # Default fallback language

    # Check if target language is in your SUPPORTED_LANGUAGES list
    for key, code in SUPPORTED_LANGUAGES.items():
        if key.lower() == clean_lang:
            target_code = code
            break

    # GUARDRAIL 5: Translation network call with automatic failure protection
    try:
        translated = GoogleTranslator(
            source="auto", target=target_code
        ).translate(answer)
        return translated if translated else answer
    except Exception as error:
        print("GUARDRAIL CAUGHT ERROR:", error)
        # Returns original text instead of crashing or showing error messages
        return answer

@app.route("/")
def home():
    return render_template("index.html")

import re


def is_relevant_context(question, excerpts):
    """Balanced Guardrail: Uses prefix/stem matching so word variations (e.g. patenting -> patent) match correctly."""
    ignore_words = {
        "what",
        "is",
        "how",
        "can",
        "the",
        "a",
        "an",
        "in",
        "of",
        "for",
        "to",
        "about",
        "with",
        "tell",
        "me",
        "give",
        "where",
        "who",
        "why",
        "does",
        "do",
        "which",
        "when",
        "should",
        "would",
        "could",
        "please",
        "help",
        "are",
        "there",
        "any",
        "define",
        "explain",
        "describe",
    }

    # Extract clean query terms
    raw_words = [
        w.strip("?,.!'\"()[]{}")
        for w in question.lower().split()
        if w.strip("?,.!'\"()[]{}") not in ignore_words and len(w) > 2
    ]

    words = list(set(raw_words))

    # If no specific keywords exist, let it pass to LLM grounding
    if not words:
        return True

    combined_text = " ".join(excerpts).lower()

    # Smart Matching: Checks for full word OR root stem (first 4+ chars) in context
    matched_words = []
    for w in words:
        # Full word match or stem match for longer words
        stem = w[:4] if len(w) >= 5 else w
        if re.search(r"\b" + re.escape(stem), combined_text):
            matched_words.append(w)

    match_ratio = len(matched_words) / len(words)

    print("\n================== GUARDRAIL CHECK ==================")
    print("User Question      :", question)
    print("Extracted Keywords :", words)
    print("Matched Keywords   :", matched_words)
    print(
        f"Match Ratio        : {match_ratio:.2f} (Allowed if >= 0.25 or matches > 0)"
    )
    print("=====================================================\n")

    # Pass if at least 25% of keywords match OR if at least 1 key term matches for short queries
    return match_ratio >= 0.25 or len(matched_words) >= 1


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "answer": "Please send a valid question request.",
            "error": "invalid_request"
        }), 400

    raw_question = data.get("question", "")
    question = raw_question.strip() if isinstance(raw_question, str) else ""

    if not question:
        return jsonify({"answer": "Please enter a valid question.", "sources": []})

    # 1. Retrieve pages from your vector search / knowledge base
    pages = retrieve_pages(question, topic="General")

    # 2. Extract exact filename and page numbers into sources list
    sources = []
    for page in pages:
        source_str = f"{page['filename']} (Page {page['page']})"
        if source_str not in sources:
            sources.append(source_str)

    # 3. Build context and call Gemini model
    context = "\n\n".join([page["text"] for page in pages])
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    
    # Call your generation function (or model.generate_content)
    response = generate_response(prompt)
    answer = response.text if hasattr(response, 'text') else str(response)

    # 4. Return BOTH answer and sources in the JSON response
    return jsonify({
        "answer": answer,
        "sources": sources
    })

    fallback_refusal = "The local knowledge base does not contain enough relevant information to answer this question."

    try:
        # Guardrail 1: Input Length Check
        if len(question) > 1000:
            return jsonify({"answer": "Question is too long. Please restrict your query to under 1000 characters."}), 400

        # 1. Search local vectors
        context, sources = get_relevant_context(question)

        # Guardrail 2: Refuse ungrounded queries if no context matches
        if not context or context.strip() == "":
            fallback_msg = "The local knowledge base does not contain enough relevant information to answer this question."
            return jsonify({
                "answer": fallback_msg,
                "sources": [],
                "citation_status": "no_citation"
            })

        # Guardrail 3: Strict System Instruction against Hallucinations
        system_instruction = (
            "You are TATVA, an AI Knowledge Assistant. "
            "CRITICAL GUARDRAILS:\n"
            "- Answer the user's question STRICTLY using only the provided Knowledge Base Context.\n"
            "- Do NOT use outside knowledge, general assumptions, or extrapolate beyond what is stated in the context.\n"
            "- If the provided context does not contain the exact answer, state clearly: "
            "'The local knowledge base does not contain enough relevant information to answer this question.'\n"
            "- Do NOT invent, assume, or improvise medical formulations or patent guidelines."
        )

        user_prompt = f"Knowledge Base Context:\n{context}\n\nUser Question: {question}"
        if language and language.lower() != "english":
            user_prompt += f"\n\nPlease provide your answer in {language}."

        # 2. Call Gemini with System Instructions & Low Temperature
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=user_prompt,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.1  # Deterministic / low creativity for factual precision
            }
        )

        return jsonify({
            "answer": response.text,
            "sources": sources,
            "citation_status": "complete" if sources else "no_citation"
        })

    except Exception as e:
        print("ERROR IN ASK ROUTE:", e)
        return jsonify({"answer": f"An error occurred while processing your request: {str(e)}"}), 500


import os

port = int(os.environ.get("PORT",10000 ))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)