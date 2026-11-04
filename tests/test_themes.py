from app.core.themes import get_available_themes, get_active_theme, set_active_theme


def test_get_available_themes():
    themes = get_available_themes()
    assert len(themes) >= 4
    theme_ids = [t["id"] for t in themes]
    assert "tema1" in theme_ids
    assert "tema2" in theme_ids
    assert "tema3" in theme_ids
    assert "tema4" in theme_ids

    # Pastikan setiap tema memiliki metadata lengkap
    for t in themes:
        assert "name" in t
        assert "tagline" in t
        assert "accent" in t
        assert "bg" in t


def test_theme_activation():
    # Ambil tema aktif saat ini
    original = get_active_theme()

    # Coba ganti ke tema2
    res = set_active_theme("tema2")
    assert res == "tema2"
    assert get_active_theme() == "tema2"

    # Kembalikan ke tema awal atau tema1
    set_active_theme(original if original in ["tema1", "tema2", "tema3", "tema4"] else "tema1")


def test_theme_api_endpoints():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        # GET /api/themes
        resp = client.get("/api/themes")
        assert resp.status_code == 200
        data = resp.json()
        assert "active_theme" in data
        assert "themes" in data
        assert len(data["themes"]) >= 4

        # POST /api/themes/active
        resp2 = client.post("/api/themes/active", json={"theme": "tema3"})
        assert resp2.status_code == 200
        assert resp2.json()["active_theme"] == "tema3"

        # Check theme changed
        resp3 = client.get("/api/themes")
        assert resp3.json()["active_theme"] == "tema3"

        # Invalid theme
        resp4 = client.post("/api/themes/active", json={"theme": "tema_tidak_ada"})
        assert resp4.status_code == 400

        # Friendly route /overlay/tema2
        resp5 = client.get("/overlay/tema2")
        assert resp5.status_code == 200

        # Reset back to tema1
        client.post("/api/themes/active", json={"theme": "tema1"})

