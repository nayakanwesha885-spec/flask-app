from app import app as flask_app, load_knowledge_base


def test_rag_knowledge_base_is_loaded():
    pages = load_knowledge_base()
    assert len(pages) > 0


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
