import importlib
import sys

import app as app_module
from app import app as flask_app, load_knowledge_base, IRRELEVANT_REQUEST_LOG


def test_import_does_not_preload_knowledge_base():
    sys.modules.pop("app", None)
    module = importlib.import_module("app")
    assert module.KNOWLEDGE_BASE_CACHE is None


def reset_irrelevant_request_log():
    IRRELEVANT_REQUEST_LOG.clear()


def test_rag_knowledge_base_is_loaded():
    pages = load_knowledge_base()
    assert len(pages) > 0


def test_load_knowledge_base_skips_corrupt_pdfs(monkeypatch, tmp_path):
    corrupt_pdf = tmp_path / "broken.pdf"
    corrupt_pdf.write_bytes(b"version https://example.com")
    valid_pdf = tmp_path / "good.pdf"
    valid_pdf.write_bytes(b"%PDF-1.4\n")

    class FakePage:
        def extract_text(self):
            return "Ayurveda knowledge for safe use"

    class FakeReader:
        def __init__(self, path):
            if "broken" in str(path).lower():
                raise ValueError("bad pdf")
            self.pages = [FakePage()]

    monkeypatch.setattr(app_module, "KNOWLEDGE_BASE_DIR", str(tmp_path))
    monkeypatch.setattr(app_module, "PdfReader", FakeReader)
    app_module.KNOWLEDGE_BASE_CACHE = None
    app_module.load_knowledge_base.cache_clear()

    pages = app_module.load_knowledge_base()

    assert any(page["filename"] == "good.pdf" and "Ayurveda knowledge" in page["text"] for page in pages)
    assert all(page["filename"] != "broken.pdf" for page in pages)


def test_relevant_herb_and_gi_questions_are_not_rejected():
    assert app_module.is_question_relevant("What are patent rights for herbs?", "General") is True
    assert app_module.is_question_relevant("How to file GI for an Indian traditional product?", "General") is True


def test_pdf_references_are_not_rejected():
    assert app_module.is_question_relevant(
        "According to my PDF, what does it say about Ashwagandha?", "General"
    ) is True
    assert app_module.is_question_relevant("What is the capital of France?", "General") is False


def test_answer_translation_failure_is_reported(monkeypatch):
    monkeypatch.setattr(app_module, "generate_ai_response", lambda question, context, language: "English answer")
    monkeypatch.setattr(app_module, "search_knowledge_base", lambda question, topic: ("Context", ["Source"]))

    def fail_translation(text, language):
        raise app_module.AnswerTranslationError("Translation service unavailable")

    monkeypatch.setattr(app_module, "translate_answer", fail_translation)
    response = flask_app.test_client().post(
        "/ask",
        json={"question": "What is Ayurveda traditional knowledge?", "language": "Odia"},
    )

    assert response.status_code == 503
    assert response.get_json()["error"] == "translation_unavailable"


def test_ask_instructs_ai_to_respond_in_selected_language(monkeypatch):
    captured = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            captured.update(kwargs)

            class Response:
                text = "Answer in English"

            return Response()

    class FakeGeminiClient:
        models = FakeModels()

    class FakeTranslator:
        def __init__(self, source, target):
            captured["translation_target"] = target

        def translate(self, text):
            return f"Hindi: {text}"

    monkeypatch.setattr(app_module, "gemini_client", FakeGeminiClient())
    monkeypatch.setattr(app_module, "MODEL_PIPELINE", ["test-model"])
    monkeypatch.setattr(app_module, "GoogleTranslator", FakeTranslator)
    monkeypatch.setattr(
        app_module,
        "search_knowledge_base",
        lambda question, topic: ("Relevant context", ["Test source"]),
    )

    response = flask_app.test_client().post(
        "/ask",
        json={
            "question": "What is Ayurveda traditional knowledge?",
            "language": "Hindi",
            "topic": "Traditional Knowledge",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["answer"] == "Hindi: Answer in English"
    assert "Respond entirely in Hindi" in captured["config"]["system_instruction"]
    assert captured["translation_target"] == "hi"


def test_answer_translation_processes_entire_long_response(monkeypatch):
    chunks = []

    class FakeTranslator:
        def __init__(self, source, target):
            pass

        def translate(self, text):
            chunks.append(text)
            return text

    monkeypatch.setattr(app_module, "GoogleTranslator", FakeTranslator)
    answer = "A" * 2500 + "\n" + "B" * 2500

    translated = app_module.translate_answer(answer, "Hindi")

    assert translated == answer
    assert len(chunks) > 2
    assert all(len(chunk) <= 2000 for chunk in chunks)


def test_google_rate_limit_falls_back_to_ai_translation(monkeypatch):
    class RateLimitedTranslator:
        def __init__(self, source, target):
            raise RuntimeError("TooManyRequests")

    monkeypatch.setattr(app_module, "GoogleTranslator", RateLimitedTranslator)
    monkeypatch.setattr(
        app_module,
        "_translate_with_ai",
        lambda text, language: f"{language} translation",
    )

    assert app_module.translate_answer("English answer", "Hindi") == "Hindi translation"


def test_ask_returns_localized_answer_when_google_translation_is_rate_limited(monkeypatch):
    class FakeModels:
        def generate_content(self, **kwargs):
            class Response:
                text = "Answer in English"

            return Response()

    class FakeGeminiClient:
        models = FakeModels()

    class RateLimitedTranslator:
        def __init__(self, source, target):
            raise RuntimeError("TooManyRequests")

    monkeypatch.setattr(app_module, "gemini_client", FakeGeminiClient())
    monkeypatch.setattr(app_module, "MODEL_PIPELINE", ["test-model"])
    monkeypatch.setattr(app_module, "GoogleTranslator", RateLimitedTranslator)
    monkeypatch.setattr(
        app_module,
        "search_knowledge_base",
        lambda question, topic: ("Relevant context", ["Test source"]),
    )
    monkeypatch.setattr(
        app_module,
        "_translate_with_ai",
        lambda text, language: "हिंदी में उत्तर",
    )

    response = flask_app.test_client().post(
        "/ask",
        json={
            "question": "What is Ayurveda traditional knowledge?",
            "language": "Hindi",
            "topic": "Traditional Knowledge",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["answer"] == "हिंदी में उत्तर"


def test_guardrails_removed_for_harmful_or_toxic_requests():
    reset_irrelevant_request_log()
    client = flask_app.test_client()
    response = client.post(
        "/ask",
        json={
            "question": "How can I make a toxic Ayurvedic poison to harm someone?",
            "language": "English",
            "topic": "General",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert "I cannot provide" not in payload["answer"]
    assert payload["citation_status"] in {"no_citation", "cited"}


def test_irrelevant_questions_are_not_rejected():
    reset_irrelevant_request_log()
    client = flask_app.test_client()
    response = client.post(
        "/ask",
        json={
            "question": "What is the capital of France?",
            "language": "English",
            "topic": "General",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert "local knowledge base" in payload["answer"] or "cannot answer" in payload["answer"].lower()
    assert payload["citation_status"] == "no_citation"


def test_repeated_irrelevant_questions_are_not_blocked():
    reset_irrelevant_request_log()
    client = flask_app.test_client()
    for _ in range(4):
        response = client.post(
            "/ask",
            json={
                "question": "What is the capital of France?",
                "language": "English",
                "topic": "General",
            },
        )
        assert response.status_code == 200
        assert response.get_json()["citation_status"] == "no_citation"
