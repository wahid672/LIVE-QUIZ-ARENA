import re
from typing import Final
import httpx

_TTS_CACHE: dict[str, bytes] = {}
_MAX_CACHE_SIZE: Final[int] = 500

GOOGLE_TTS_URL: Final[str] = "https://translate.google.com/translate_tts"
TTS_USER_AGENT: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def split_text_for_tts(text: str, max_chars: int = 120) -> list[str]:
    """Bagi teks menjadi potongan-potongan pendek yang tidak memotong kata di tengah."""
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return []
    if len(clean) <= max_chars:
        return [clean]

    # Pisahkan per tanda baca kalimat
    sentences = re.split(r"(?<=[.?!,;:])\s+", clean)
    chunks: list[str] = []
    current = ""

    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(current) + len(s) + 1 <= max_chars:
            current = f"{current} {s}".strip()
        else:
            if current:
                chunks.append(current)
            if len(s) <= max_chars:
                current = s
            else:
                # Jika 1 kalimat terlalu panjang, potong per kata
                words = s.split(" ")
                current = ""
                for w in words:
                    if len(current) + len(w) + 1 <= max_chars:
                        current = f"{current} {w}".strip()
                    else:
                        if current:
                            chunks.append(current)
                        current = w
    if current:
        chunks.append(current)
    return chunks


async def generate_indonesian_tts(text: str) -> bytes:
    """Hasilkan stream audio MP3 Bahasa Indonesia murni beraksen natural."""
    clean_text = re.sub(r"\s+", " ", text).strip()
    if not clean_text:
        return b""

    # Cek cache in-memory untuk efisiensi
    if clean_text in _TTS_CACHE:
        return _TTS_CACHE[clean_text]

    chunks = split_text_for_tts(clean_text, max_chars=120)
    if not chunks:
        return b""

    combined_audio = bytearray()
    headers = {"User-Agent": TTS_USER_AGENT}

    async with httpx.AsyncClient(timeout=10.0) as client:
        for chunk in chunks:
            params = {
                "ie": "UTF-8",
                "tl": "id",
                "client": "tw-ob",
                "q": chunk,
            }
            try:
                resp = await client.get(GOOGLE_TTS_URL, params=params, headers=headers)
                if resp.status_code == 200:
                    combined_audio.extend(resp.content)
            except Exception:
                pass

    result = bytes(combined_audio)
    if result:
        if len(_TTS_CACHE) >= _MAX_CACHE_SIZE:
            for k in list(_TTS_CACHE.keys())[:100]:
                _TTS_CACHE.pop(k, None)
        _TTS_CACHE[clean_text] = result

    return result
