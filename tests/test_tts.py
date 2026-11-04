import pytest
from app.core.tts import split_text_for_tts, generate_indonesian_tts
from app.core.themes import get_tts_mode, set_tts_mode


def test_split_text_for_tts():
    # Empty or whitespace
    assert split_text_for_tts("") == []
    assert split_text_for_tts("   ") == []

    # Short sentence
    text = "Siapakah presiden pertama Indonesia?"
    chunks = split_text_for_tts(text, max_chars=120)
    assert chunks == [text]

    # Multiple sentences
    long_text = "Pertanyaan nomor satu. Siapakah presiden pertama Indonesia? Beliau dikenal sebagai proklamator bangsa."
    chunks = split_text_for_tts(long_text, max_chars=40)
    assert len(chunks) >= 2
    for c in chunks:
        assert len(c) <= 40


def test_tts_settings_mode():
    original = get_tts_mode()

    # Valid mode switching
    assert set_tts_mode("browser") == "browser"
    assert get_tts_mode() == "browser"

    assert set_tts_mode("disabled") == "disabled"
    assert get_tts_mode() == "disabled"

    assert set_tts_mode("locked_id") == "locked_id"
    assert get_tts_mode() == "locked_id"

    # Invalid mode
    with pytest.raises(ValueError):
        set_tts_mode("unsupported_mode")

    # Restore
    set_tts_mode(original)


def test_tts_api_endpoints():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        # GET /api/settings/tts
        resp = client.get("/api/settings/tts")
        assert resp.status_code == 200
        assert "tts_mode" in resp.json()

        # POST /api/settings/tts
        resp = client.post("/api/settings/tts", json={"mode": "locked_id"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
        assert resp.json()["tts_mode"] == "locked_id"

        # Invalid mode
        resp_err = client.post("/api/settings/tts", json={"mode": "invalid_mode"})
        assert resp_err.status_code == 422  # Pydantic validation error

        # GET /api/tts with empty text
        resp_empty = client.get("/api/tts?text=")
        assert resp_empty.status_code == 204

        # GET /api/tts with valid text
        resp_audio = client.get("/api/tts?text=Halo%20dunia")
        assert resp_audio.status_code == 200
        assert resp_audio.headers.get("content-type") == "audio/mpeg"
        assert len(resp_audio.content) > 0
