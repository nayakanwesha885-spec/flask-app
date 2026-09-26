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


def test_rag_translation_falls_back_when_translation_fails():
    client = flask_app.test_client()
    response = client.post(
        "/ask",
        json={
            "question": "What is Ayurveda traditional knowledge?",
            "language": "Odia",
            "topic": "Traditional Knowledge",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert "answer" in payload
    assert payload["answer"]


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
