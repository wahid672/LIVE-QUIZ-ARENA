from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
THEMES_DIR = BASE_DIR / "frontend" / "overlay" / "themes"
TEMA1_CSS = (THEMES_DIR / "tema1" / "style.css").read_text(encoding="utf-8")


def generate_tema2(base: str) -> str:
    css = base
    css = css.replace(
        "LIVE QUIZ ARENA — NEO-BRUTALIST ARCADE POP LIVESTREAM OVERLAY",
        "LIVE QUIZ ARENA — TEMA 2: NEON SYNTHWAVE / CYBERPUNK ARCADE"
    )
    # Background and surfaces
    css = css.replace("background-color: #05040d !important;", "background-color: #070114 !important;")
    css = css.replace("background-color: #05040d;", "background-color: #070114;")
    css = css.replace("background: #0c0a22;", "background: #110326;")
    css = css.replace("--arcade-bg: #0c0a22;", "--arcade-bg: #110326;")
    css = css.replace("--arcade-surface: #14122d;", "--arcade-surface: #180536;")
    css = css.replace("--arcade-q-card: #1b1744;", "--arcade-q-card: #200747;")
    css = css.replace("--arcade-panel: #141138;", "--arcade-panel: #180536;")
    css = css.replace("--arcade-topbar: #171439;", "--arcade-topbar: #1d0742;")

    # Color palette
    css = css.replace("--arcade-yellow: #FFDE00;", "--arcade-yellow: #a855f7;")
    css = css.replace("--arcade-pink: #FF2E93;", "--arcade-pink: #ec4899;")
    css = css.replace("--arcade-cyan: #00F0FF;", "--arcade-cyan: #22d3ee;")
    css = css.replace("--shadow-yellow: 4px 4px 0px #FFDE00;", "--shadow-yellow: 4px 4px 0px #a855f7;")
    css = css.replace("--shadow-pink: 4px 4px 0px #FF2E93;", "--shadow-pink: 4px 4px 0px #ec4899;")
    css = css.replace("--shadow-cyan: 4px 4px 0px #00F0FF;", "--shadow-cyan: 4px 4px 0px #22d3ee;")

    return css


def generate_tema3(base: str) -> str:
    css = base
    css = css.replace(
        "LIVE QUIZ ARENA — NEO-BRUTALIST ARCADE POP LIVESTREAM OVERLAY",
        "LIVE QUIZ ARENA — TEMA 3: GOLDEN ROYAL / LUXURY OBSIDIAN & IMPERIAL GOLD"
    )
    # Background and surfaces
    css = css.replace("background-color: #05040d !important;", "background-color: #09090b !important;")
    css = css.replace("background-color: #05040d;", "background-color: #09090b;")
    css = css.replace("background: #0c0a22;", "background: #121214;")
    css = css.replace("--arcade-bg: #0c0a22;", "--arcade-bg: #121214;")
    css = css.replace("--arcade-surface: #14122d;", "--arcade-surface: #18181b;")
    css = css.replace("--arcade-q-card: #1b1744;", "--arcade-q-card: #22201d;")
    css = css.replace("--arcade-panel: #141138;", "--arcade-panel: #1c1b18;")
    css = css.replace("--arcade-topbar: #171439;", "--arcade-topbar: #1e1d1a;")

    # Color palette (Gold, Amber, Platinum, Emerald)
    css = css.replace("--arcade-yellow: #FFDE00;", "--arcade-yellow: #f59e0b;")
    css = css.replace("--arcade-pink: #FF2E93;", "--arcade-pink: #d97706;")
    css = css.replace("--arcade-cyan: #00F0FF;", "--arcade-cyan: #facc15;")
    css = css.replace("--shadow-yellow: 4px 4px 0px #FFDE00;", "--shadow-yellow: 4px 4px 0px #f59e0b;")
    css = css.replace("--shadow-pink: 4px 4px 0px #FF2E93;", "--shadow-pink: 4px 4px 0px #d97706;")
    css = css.replace("--shadow-cyan: 4px 4px 0px #00F0FF;", "--shadow-cyan: 4px 4px 0px #facc15;")

    return css


def generate_tema4(base: str) -> str:
    css = base
    css = css.replace(
        "LIVE QUIZ ARENA — NEO-BRUTALIST ARCADE POP LIVESTREAM OVERLAY",
        "LIVE QUIZ ARENA — TEMA 4: SUNSET CRIMSON / FIERY RED & MOLTEN MAGMA"
    )
    # Background and surfaces
    css = css.replace("background-color: #05040d !important;", "background-color: #0d0202 !important;")
    css = css.replace("background-color: #05040d;", "background-color: #0d0202;")
    css = css.replace("background: #0c0a22;", "background: #190505;")
    css = css.replace("--arcade-bg: #0c0a22;", "--arcade-bg: #190505;")
    css = css.replace("--arcade-surface: #14122d;", "--arcade-surface: #220808;")
    css = css.replace("--arcade-q-card: #1b1744;", "--arcade-q-card: #2e0b0b;")
    css = css.replace("--arcade-panel: #141138;", "--arcade-panel: #240808;")
    css = css.replace("--arcade-topbar: #171439;", "--arcade-topbar: #290909;")

    # Color palette (Fiery Red, Molten Orange, Amber Flame, Emerald)
    css = css.replace("--arcade-yellow: #FFDE00;", "--arcade-yellow: #f97316;")
    css = css.replace("--arcade-pink: #FF2E93;", "--arcade-pink: #ef4444;")
    css = css.replace("--arcade-cyan: #00F0FF;", "--arcade-cyan: #fbbf24;")
    css = css.replace("--shadow-yellow: 4px 4px 0px #FFDE00;", "--shadow-yellow: 4px 4px 0px #f97316;")
    css = css.replace("--shadow-pink: 4px 4px 0px #FF2E93;", "--shadow-pink: 4px 4px 0px #ef4444;")
    css = css.replace("--shadow-cyan: 4px 4px 0px #00F0FF;", "--shadow-cyan: 4px 4px 0px #fbbf24;")

    return css


def main():
    tema2 = generate_tema2(TEMA1_CSS)
    (THEMES_DIR / "tema2" / "style.css").write_text(tema2, encoding="utf-8")
    print(f"[OK] Tema 2: {len(tema2)} chars")

    tema3 = generate_tema3(TEMA1_CSS)
    (THEMES_DIR / "tema3" / "style.css").write_text(tema3, encoding="utf-8")
    print(f"[OK] Tema 3: {len(tema3)} chars")

    tema4 = generate_tema4(TEMA1_CSS)
    (THEMES_DIR / "tema4" / "style.css").write_text(tema4, encoding="utf-8")
    print(f"[OK] Tema 4: {len(tema4)} chars")


if __name__ == "__main__":
    main()
