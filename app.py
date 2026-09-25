from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import re
import time
from functools import lru_cache
from openai import OpenAI
from google import genai

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

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
    "the", "to", "what", "which", "with", "can", "does", "do", "from", "under"
}
KNOWLEDGE_BASE_CACHE = None
IRRELEVANT_REQUEST_LOG = {}
IRRELEVANT_REQUEST_LIMIT = 3
IRRELEVANT_REQUEST_WINDOW_SECONDS = 60
RELEVANCE_KEYWORDS = {
    "ayurveda", "ayurvedic", "traditional", "patent", "patents",
    "trademark", "trademarks", "geographical", "indication", "gi", "copyright",
    "design", "designs", "formulation", "formulations", "regulation", "regulatory",
    "benefit", "sharing", "abs", "intellectual", "property", "ipr", "invention",
    "inventor", "medicine", "medicinal", "herbal", "plant", "biodiversity",
    "indigenous", "documentation", "source", "legal", "compliance", "ip",
    "knowledge", "traditionalknowledge"
}


def extract_question_terms(question):
    terms = {
        term.lower() for term in re.findall(r"[a-zA-Z][a-zA-Z-]+", question)
        if term.lower() not in STOP_WORDS and len(term) > 2
    }
    return terms


def is_question_relevant(question, topic):
    if not isinstance(question, str):
        return False

    question_terms = extract_question_terms(question)
    if not question_terms:
        return False

    if topic != "General":
        topic_terms = {term.lower() for term in topic.split() if len(term) > 2}
        if question_terms & topic_terms:
            return True

    domain_hits = question_terms & RELEVANCE_KEYWORDS
    if not domain_hits:
        return False

    if "ayurveda" in domain_hits or "ayurvedic" in domain_hits:
        return True

    if len(domain_hits) >= 2:
        return True

    if "traditional" in domain_hits and "knowledge" in domain_hits:
        return True

    if "benefit" in domain_hits and "sharing" in domain_hits:
        return True

    return False


def get_client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown-client"


def check_irrelevant_request_limit(question):
    client_ip = get_client_ip()
    normalized = " ".join(re.sub(r"[^a-z0-9\s]", " ", question.lower()).split())
    now = time.time()
    history = IRRELEVANT_REQUEST_LOG.setdefault(client_ip, [])
    history[:] = [timestamp for timestamp in history if now - timestamp < IRRELEVANT_REQUEST_WINDOW_SECONDS]
    history.append(now)
    IRRELEVANT_REQUEST_LOG[client_ip] = history[-IRRELEVANT_REQUEST_LIMIT:]
    if len(history) > IRRELEVANT_REQUEST_LIMIT:
        return True
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
            reader = PdfReader(path)
            for page_number, page in enumerate(reader.pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    pages.append({
                        "filename": filename,
                        "page": page_number,
                        "text": re.sub(r"\s+", " ", text)
                    })

    KNOWLEDGE_BASE_CACHE = pages
    return KNOWLEDGE_BASE_CACHE


# Warm the local RAG index during app startup so the first browser request is fast.
load_knowledge_base()


def retrieve_pages(question, topic):
    if not is_question_relevant(question, topic):
        return []

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
                text = " ".join(
                    content.text for content in result.content if content.type == "text"
                ).strip()
                if text:
                    vector_pages.append({
                        "filename": result.filename,
                        "page": "vector store",
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
    for page in load_knowledge_base():
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


GUARDRAIL_MESSAGE = (
    "I cannot provide medical treatment, dosing, emergency, toxic, harmful, illegal manufacturing, "
    "fraud, or law-evasion instructions. I can help with lawful, educational information about "
    "Ayurveda intellectual property, traditional knowledge, and regulatory questions. Please consult "
    "a qualified professional or the relevant authority."
)


def detect_unsafe_request(question):
    if not isinstance(question, str):
        return False

    normalized = " ".join(re.sub(r"[^a-z0-9\s]", " ", question.lower()).split())
    if not normalized:
        return False

    unsafe_terms = (
        "diagnose", "diagnosis", "dosage", "dose", "prescription", "prescribe", "treatment plan",
        "emergency", "urgent care", "self medication", "cure disease",
        "poison", "poisoning", "toxic", "toxin", "weaponize", "harm someone", "kill someone",
        "make poison", "manufacture poison", "illegal drug", "self harm",
        "evade law", "evade customs", "bypass regulation", "bypass law", "avoid compliance",
        "counterfeit", "falsify", "fraud", "money laundering", "fake patent", "fake trademark",
    )

    return any(term in normalized for term in unsafe_terms)


def translate_answer(answer, language):
    if language == "English":
        return answer

    if gemini_client is None:
        raise TranslationUnavailableError(
            "Translation is unavailable because GEMINI_API_KEY is not configured."
        )

    try:
        prompt = (
            f"Translate the answer completely into {language}. "
            "Do not leave explanatory sentences in English. "
            "Preserve document filenames, page numbers, bullet structure, "
            "and the educational disclaimer. Return only the translation.\n\n"
            f"Answer:\n{answer}"
        )
        response = None
        last_error = None
        for model in (GEMINI_MODEL, GEMINI_FALLBACK_MODEL):
            try:
                response = gemini_client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={"temperature": 0},
                )
                break
            except Exception as error:
                last_error = error
                if getattr(error, "status_code", None) not in {429, 503}:
                    raise
        if response is None:
            raise last_error
        translated = response.text
        if not translated or not translated.strip():
            raise TranslationUnavailableError("The translation provider returned an empty answer.")
        return translated.strip()
    except Exception as error:
        print("TRANSLATION ERROR:", error)
        if isinstance(error, TranslationUnavailableError):
            raise
        if getattr(error, "status_code", None) == 429:
            raise TranslationUnavailableError(
                "The Gemini account has reached its API limit.",
                "quota_exceeded",
            ) from error
        raise TranslationUnavailableError("The translation provider could not translate the answer.") from error


@app.route("/")
def home():
    return render_template("index.html")


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
    language = data.get("language", "English")
    topic = data.get("topic", "General")

    if not question:
        return jsonify({
            "answer": "Please enter a question."
        })

    if len(question) > MAX_QUESTION_LENGTH:
        return jsonify({
            "answer": f"Please keep your question under {MAX_QUESTION_LENGTH} characters.",
            "error": "question_too_long"
        }), 400

    if not isinstance(language, str) or language not in SUPPORTED_LANGUAGES:
        language = "English"

    if not isinstance(topic, str) or topic not in SUPPORTED_TOPICS:
        topic = "General"

    try:
        if detect_unsafe_request(question):
            return jsonify({
                "answer": GUARDRAIL_MESSAGE,
                "sources": [],
                "citation_status": "not_applicable"
            })

        if not is_question_relevant(question, topic):
            if check_irrelevant_request_limit(question):
                return jsonify({
                    "answer": "Too many irrelevant requests in a short time. This service is limited to Ayurveda, traditional knowledge, intellectual property, and regulatory questions.",
                    "sources": [],
                    "citation_status": "no_citation"
                }), 429
            return jsonify({
                "answer": "The local knowledge base does not contain enough relevant information to answer this question. Please ask about Ayurveda, traditional knowledge, intellectual property, or regulatory matters.",
                "sources": [],
                "citation_status": "no_citation"
            })

        pages = retrieve_pages(question, topic)
        if not pages:
            return jsonify({
                "answer": "The local knowledge base does not contain enough relevant information to answer this question. Please try an Ayurveda intellectual property or regulatory question.",
                "sources": [],
                "citation_status": "no_citation"
            })

        excerpts = []
        sources = []
        for page in pages:
            excerpt = page["text"][:700].strip()
            excerpts.append(f"{excerpt} [{page['filename']}, page {page['page']}]")
            source = f"{page['filename']} (Page {page['page']})"
            if source not in sources:
                sources.append(source)

        base_answer = (
            "Based on the retrieved local knowledge-base documents, here are the most relevant findings:\n\n"
            + "\n\n".join(f"- {excerpt}" for excerpt in excerpts)
            + "\n\nThis is educational guidance only. Verify current legal or regulatory requirements with official sources or a qualified professional."
        )

        try:
            answer = translate_answer(base_answer, language)
        except TranslationUnavailableError as error:
            print("TRANSLATION ERROR:", error)
            # Keep the app functional even when live translation is temporarily unavailable.
            # Show the original English answer instead of failing the whole request.
            answer = base_answer

        return jsonify({
            "answer": answer,
            "sources": sources,
            "citation_status": "cited"
        })

    except Exception as e:

        print("LOCAL RAG ERROR:", e)
        return jsonify({
            "answer": "The local knowledge base could not be read. Please check the PDF files and try again.",
            "error": "local_knowledge_base_error"
        }), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)