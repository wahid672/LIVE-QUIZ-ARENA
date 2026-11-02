import asyncio
import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


class AudioPlaylistManager:
    """
    Manajer playlist audio langsung (.mp3, .wav, .mov, .ogg, .m4a, dll.)
    untuk musik latar siaran kuis live.
    """

    SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".mov", ".ogg", ".m4a", ".aac", ".flac"}
    URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)

    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self._lock = asyncio.Lock()
        self._queue: list[dict[str, Any]] = []
        self._current_index = -1
        self._is_playing = False
        self._volume = 75
        self._loop = True
        self._play_generation = 0
        self._load()

    @classmethod
    def _sanitize_raw_input(cls, raw_value: str) -> str:
        value = (raw_value or "").strip()
        value = value.strip("<>()[]{}\"'`")
        value = value.rstrip(".,;")
        match = cls.URL_RE.search(value)
        if match:
            value = match.group(0)
        return value.strip()

    @classmethod
    def parse_url(cls, raw_url: str) -> dict[str, Any]:
        value = cls._sanitize_raw_input(raw_url)
        if not value:
            raise ValueError("URL audio tidak boleh kosong.")

        parsed = urlparse(value)
        if not parsed.scheme or not parsed.netloc:
            # Allow relative or local path
            path = parsed.path or value
        else:
            path = parsed.path

        # Ambil ekstensi file
        path_obj = Path(unquote(path))
        ext = path_obj.suffix.lower()

        if ext not in cls.SUPPORTED_EXTENSIONS:
            allowed = ", ".join(sorted(cls.SUPPORTED_EXTENSIONS))
            raise ValueError(f"URL harus berupa file audio berakhiran salah satu dari: {allowed}")

        # Buat judul bersih dari nama file
        raw_name = path_obj.stem
        clean_title = re.sub(r"[_\-+]+", " ", raw_name).strip()
        if not clean_title:
            clean_title = f"Audio Track ({ext})"
        else:
            clean_title = clean_title.title()

        # Buat track_key unik berbasis hash URL
        url_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
        track_key = f"audio:{url_hash}"

        return {
            "track_key": track_key,
            "kind": ext.lstrip("."),
            "url": value,
            "title": clean_title,
            "extension": ext,
        }

    def _load(self) -> None:
        if not self.storage_path.exists():
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            raw_queue = data.get("queue", [])
            # Filter hanya trek audio yang valid (singkirkan format lama YouTube)
            valid_queue = []
            for item in raw_queue:
                url = item.get("url") or ""
                path = urlparse(url).path
                ext = Path(unquote(path)).suffix.lower()
                if ext in self.SUPPORTED_EXTENSIONS:
                    valid_queue.append(item)

            self._queue = valid_queue
            self._volume = int(data.get("volume", 75))
            self._loop = bool(data.get("loop", True))
            idx = int(data.get("current_index", -1))
            self._current_index = idx if 0 <= idx < len(self._queue) else (0 if self._queue else -1)
            self._is_playing = False
        except Exception:
            self._queue = []
            self._current_index = -1

    def _save_locked(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "queue": self._queue,
                "current_index": self._current_index,
                "volume": self._volume,
                "loop": self._loop,
                "play_generation": self._play_generation,
            }
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    async def get_state(self) -> dict[str, Any]:
        async with self._lock:
            current = self._queue[self._current_index] if 0 <= self._current_index < len(self._queue) else None
            return {
                "queue": list(self._queue),
                "current_index": self._current_index,
                "current_track": current,
                "is_playing": self._is_playing,
                "volume": self._volume,
                "loop": self._loop,
                "track_count": len(self._queue),
                "play_generation": self._play_generation,
            }

    async def add_urls(self, urls: list[str]) -> dict[str, Any]:
        async with self._lock:
            added = 0
            invalid: list[dict[str, str]] = []
            existing_urls = {item["url"] for item in self._queue}

            for raw in urls:
                if not (raw or "").strip():
                    continue
                try:
                    track = self.parse_url(raw)
                    if track["url"] in existing_urls:
                        continue
                    existing_urls.add(track["url"])
                    self._queue.append(track)
                    added += 1
                except Exception as error:
                    invalid.append({"raw": raw, "error": str(error)})

            if self._current_index == -1 and self._queue:
                self._current_index = 0

            self._save_locked()
            current = self._queue[self._current_index] if 0 <= self._current_index < len(self._queue) else None
            return {
                "added_count": added,
                "invalid": invalid,
                "queue": list(self._queue),
                "current_index": self._current_index,
                "current_track": current,
                "is_playing": self._is_playing,
                "volume": self._volume,
                "loop": self._loop,
                "track_count": len(self._queue),
                "play_generation": self._play_generation,
            }

    async def remove_track(self, track_key: str) -> dict[str, Any]:
        async with self._lock:
            target_idx = -1
            for i, item in enumerate(self._queue):
                if item["track_key"] == track_key:
                    target_idx = i
                    break

            if target_idx != -1:
                del self._queue[target_idx]
                if not self._queue:
                    self._current_index = -1
                    self._is_playing = False
                elif self._current_index >= len(self._queue):
                    self._current_index = 0
                elif self._current_index > target_idx:
                    self._current_index -= 1

                self._play_generation += 1
                self._save_locked()

            current = self._queue[self._current_index] if 0 <= self._current_index < len(self._queue) else None
            return {
                "queue": list(self._queue),
                "current_index": self._current_index,
                "current_track": current,
                "is_playing": self._is_playing,
                "volume": self._volume,
                "loop": self._loop,
                "track_count": len(self._queue),
                "play_generation": self._play_generation,
            }

    async def control(self, action: str, **kwargs: Any) -> dict[str, Any]:
        async with self._lock:
            if action == "play":
                if self._queue:
                    if self._current_index < 0:
                        self._current_index = 0
                    self._is_playing = True
                    self._play_generation += 1
            elif action == "pause":
                self._is_playing = False
            elif action == "next":
                if self._queue:
                    self._current_index = (self._current_index + 1) % len(self._queue)
                    self._play_generation += 1
            elif action == "previous":
                if self._queue:
                    self._current_index = (self._current_index - 1) % len(self._queue)
                    self._play_generation += 1
            elif action == "ended":
                if self._queue:
                    if self._current_index + 1 < len(self._queue):
                        self._current_index += 1
                        self._play_generation += 1
                        self._is_playing = True
                    elif self._loop:
                        self._current_index = 0
                        self._play_generation += 1
                        self._is_playing = True
                    else:
                        self._is_playing = False
            elif action == "select":
                key = kwargs.get("track_key")
                for i, item in enumerate(self._queue):
                    if item["track_key"] == key:
                        self._current_index = i
                        self._is_playing = True
                        self._play_generation += 1
                        break
            elif action == "volume":
                vol = kwargs.get("volume")
                if vol is not None:
                    self._volume = max(0, min(100, int(vol)))
            elif action == "loop":
                loop_val = kwargs.get("loop")
                if loop_val is not None:
                    self._loop = bool(loop_val)

            self._save_locked()
            current = self._queue[self._current_index] if 0 <= self._current_index < len(self._queue) else None
            return {
                "queue": list(self._queue),
                "current_index": self._current_index,
                "current_track": current,
                "is_playing": self._is_playing,
                "volume": self._volume,
                "loop": self._loop,
                "track_count": len(self._queue),
                "play_generation": self._play_generation,
            }


# Alias untuk backwards compatibility
YouTubePlaylistManager = AudioPlaylistManager
