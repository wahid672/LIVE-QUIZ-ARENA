from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
THEMES_DIR = BASE_DIR / "frontend" / "overlay" / "themes"
SETTINGS_FILE = BASE_DIR / "data" / "settings.json"

DEFAULT_THEMES = [
    {
        "id": "tema1",
        "name": "Tema 1: Cyber Arena",
        "tagline": "Esports Dark Navy & Cyan",
        "description": "Tema arena esports klasik dengan nuansa biru dongker gelap, cyan elektrik, dan aksen emas.",
        "accent": "#38bdf8",
        "bg": "#070e1c",
        "badge": "DEFAULT",
    },
    {
        "id": "tema2",
        "name": "Tema 2: Neon Synthwave",
        "tagline": "Cyberpunk Magenta & Electric Violet",
        "description": "Gaya retro arcade cyberpunk dengan warna neon magenta, ungu elektrik, dan cyan futuristik berenergi tinggi.",
        "accent": "#ec4899",
        "bg": "#120326",
        "badge": "ARCADE",
    },
    {
        "id": "tema3",
        "name": "Tema 3: Golden Royal",
        "tagline": "Luxury Obsidian & Imperial Gold",
        "description": "Tema mewah kejuaraan kerajaan dengan kombinasi hitam obsidian mengilap, emas murni, dan aksen zamrud.",
        "accent": "#f59e0b",
        "bg": "#0b0c0e",
        "badge": "CHAMPION",
    },
    {
        "id": "tema4",
        "name": "Tema 4: Sunset Crimson",
        "tagline": "Fiery Red & Molten Magma",
        "description": "Arena pertarungan berapi-api dengan warna merah delima membara, oranye lahar, dan arang vulkanik.",
        "accent": "#ef4444",
        "bg": "#140404",
        "badge": "BATTLE",
    },
]


def _load_settings() -> dict:
    if not SETTINGS_FILE.exists():
        return {"active_theme": "tema1"}
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"active_theme": "tema1"}


def _save_settings(settings: dict) -> None:
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")


def get_available_themes() -> list[dict]:
    themes = []
    if THEMES_DIR.exists():
        for theme_dir in sorted(THEMES_DIR.iterdir()):
            if theme_dir.is_dir() and (theme_dir / "style.css").exists():
                theme_json_path = theme_dir / "theme.json"
                if theme_json_path.exists():
                    try:
                        meta = json.loads(theme_json_path.read_text(encoding="utf-8"))
                        themes.append(meta)
                        continue
                    except Exception:
                        pass
                themes.append({
                    "id": theme_dir.name,
                    "name": theme_dir.name.capitalize(),
                    "tagline": "Custom Theme",
                    "description": f"Tema kustom dari folder {theme_dir.name}",
                    "accent": "#38bdf8",
                    "bg": "#0b0f19",
                    "badge": "CUSTOM",
                })
    if not themes:
        themes = DEFAULT_THEMES
    return themes


def get_active_theme() -> str:
    settings = _load_settings()
    theme = settings.get("active_theme", "tema1")
    available_ids = {t["id"] for t in get_available_themes()}
    if theme not in available_ids:
        return "tema1"
    return theme


def set_active_theme(theme_id: str) -> str:
    available_ids = {t["id"] for t in get_available_themes()}
    if theme_id not in available_ids:
        raise ValueError(f"Tema '{theme_id}' tidak ditemukan. Tersedia: {sorted(available_ids)}")
    settings = _load_settings()
    settings["active_theme"] = theme_id
    _save_settings(settings)
    return theme_id
