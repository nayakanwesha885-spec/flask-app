from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import re
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


@lru_cache(maxsize=1)
def load_knowledge_base():
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
    return pages


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

    terms = {
        term.lower() for term in re.findall(r"[a-zA-Z][a-zA-Z-]+", question)
        if term.lower() not in STOP_WORDS and len(term) > 2
    }
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
    return [page for _, page in scored_pages[:3]]


class TranslationUnavailableError(RuntimeError):
    def __init__(self, message, code="translation_unavailable"):
        super().__init__(message)
        self.code = code


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
        unsafe_terms = {
            "diagnose", "diagnosis", "dosage", "dose", "cure", "emergency",
            "manufacture poison", "evade law", "bypass regulation", "fraud"
        }
        if any(term in question.lower() for term in unsafe_terms):
            return jsonify({
                "answer": "I cannot provide medical treatment, dosing, emergency, unsafe manufacturing, fraud, or regulation-evasion instructions. Please consult a qualified professional.",
                "sources": [],
                "citation_status": "not_applicable"
            })

        pages = retrieve_pages(question, topic)
        if not pages:
            return jsonify({
                "answer": "The local knowledge base does not contain enough information to answer this question. Please try an Ayurveda intellectual property or regulatory question.",
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

        answer = (
            "Based on the retrieved local knowledge-base documents, here are the most relevant findings:\n\n"
            + "\n\n".join(f"- {excerpt}" for excerpt in excerpts)
            + "\n\nThis is educational guidance only. Verify current legal or regulatory requirements with official sources or a qualified professional."
        )
        answer = translate_answer(answer, language)

        return jsonify({
            "answer": answer,
            "sources": sources,
            "citation_status": "cited"
        })

    except TranslationUnavailableError as error:
        print("TRANSLATION ERROR:", error)
        return jsonify({
            "answer": str(error),
            "error": error.code
        }), 503

    except Exception as e:

        print("LOCAL RAG ERROR:", e)
        return jsonify({
            "answer": "The local knowledge base could not be read. Please check the PDF files and try again.",
            "error": "local_knowledge_base_error"
        }), 503


if __name__ == "__main__":
    app.run(debug=True) 