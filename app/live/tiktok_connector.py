import asyncio
import re
from typing import Any

from app.live.interaction_manager import LiveInteractionManager


class TikTokLiveBridge:
    """Adapter untuk TikTokLive 7.x. Tidak menyimpan password atau session cookie."""

    def __init__(self, interactions: LiveInteractionManager):
        self.interactions = interactions
        self.status = "disconnected"
        self.username: str | None = None
        self.room_id: str | None = None
        self.last_error: str | None = None
        self._client: Any = None
        self._task: asyncio.Task | None = None
        self._lock = asyncio.Lock()
        self._generation = 0

    @staticmethod
    def normalize_username(raw: str) -> str:
        value = (raw or "").strip()
        value = value.removeprefix("https://www.tiktok.com/").removeprefix("https://tiktok.com/")
        value = value.strip("/")
        value = value.removeprefix("@")
        if not re.fullmatch(r"[A-Za-z0-9._]{2,24}", value):
            raise ValueError("Masukkan username TikTok yang valid, misalnya @namakreator.")
        return value

    async def connect(self, raw_username: str) -> dict[str, Any]:
        username = self.normalize_username(raw_username)
        async with self._lock:
            if self._task is not None and not self._task.done():
                raise ValueError("Koneksi TikTok LIVE sedang berjalan atau masih aktif.")

            try:
                from TikTokLive import TikTokLiveClient
                from TikTokLive.events import (
                    CommentEvent,
                    ConnectEvent,
                    DisconnectEvent,
                    FollowEvent,
                    GiftEvent,
                    LikeEvent,
                )
            except ImportError as error:
                self.status = "dependency_missing"
                self.last_error = "TikTokLive belum terpasang. Jalankan pip install -r requirements.txt."
                raise RuntimeError(self.last_error) from error

            self._generation += 1
            generation = self._generation
            client = TikTokLiveClient(unique_id=f"@{username}")
            self._client = client
            self.username = username
            self.room_id = None
            self.last_error = None
            self.status = "connecting"

            @client.on(ConnectEvent)
            async def _on_connect(event):
                if generation != self._generation:
                    return
                self.status = "connected"
                self.room_id = str(getattr(client, "room_id", "") or "") or None
                self.last_error = None

            @client.on(DisconnectEvent)
            async def _on_disconnect(event):
                if generation == self._generation and self.status != "disconnecting":
                    self.status = "disconnected"

            @client.on(CommentEvent)
            async def _on_comment(event):
                user = getattr(event, "user", None)
                if user is None:
                    return
                user_id = getattr(user, "unique_id", None)
                nickname = getattr(user, "nickname", None) or user_id or "Viewer"
                comment = getattr(event, "comment", None) or getattr(event, "content", "")
                await self.interactions.process_comment(
                    username=str(nickname),
                    user_id=str(user_id) if user_id else None,
                    comment=str(comment),
                )

            @client.on(LikeEvent)
            async def _on_like(event):
                user = getattr(event, "user", None)
                user_id = getattr(user, "unique_id", None) if user else None
                nickname = getattr(user, "nickname", None) if user else None
                await self.interactions.process_like(
                    count=int(getattr(event, "count", 0) or 0),
                    total=getattr(event, "total", None),
                    username=str(nickname or user_id or "Community"),
                )

            @client.on(FollowEvent)
            async def _on_follow(event):
                user = getattr(event, "user", None)
                if user is None:
                    return
                user_id = getattr(user, "unique_id", None)
                nickname = getattr(user, "nickname", None) or user_id or "New follower"
                await self.interactions.process_follow(
                    username=str(nickname),
                    user_id=str(user_id) if user_id else None,
                )

            @client.on(GiftEvent)
            async def _on_gift(event):
                gift = getattr(event, "gift", None)
                user = getattr(event, "user", None)
                if gift is None or user is None:
                    return
                # Gift streak mengirim event intermediate; hanya proses event final.
                if bool(getattr(event, "streaking", False)):
                    return
                user_id = getattr(user, "unique_id", None)
                nickname = getattr(user, "nickname", None) or user_id or "Gift supporter"
                await self.interactions.process_gift(
                    username=str(nickname),
                    user_id=str(user_id) if user_id else None,
                    gift_name=str(getattr(gift, "name", None) or "Gift"),
                    diamonds=int(getattr(gift, "diamond_count", 0) or 0),
                    quantity=int(getattr(event, "repeat_count", 1) or 1),
                )

            self._task = asyncio.create_task(self._run_client(client, generation))
            return await self.get_status()

    @staticmethod
    def _safe_error(error: Exception) -> str:
        message = str(error)
        message = re.sub(r"https?://\\S+", "[URL disembunyikan]", message)
        message = re.sub(
            r"(?i)(token|signature|sessionid|session_id)=([^&\\s]+)",
            r"\\1=[redacted]",
            message,
        )
        return f"{type(error).__name__}: {message[:180]}"

    async def _run_client(self, client: Any, generation: int) -> None:
        try:
            await client.connect(fetch_gift_info=True)
            if generation == self._generation and self.status != "disconnecting":
                self.status = "disconnected"
        except asyncio.CancelledError:
            raise
        except Exception as error:
            if generation == self._generation:
                self.status = "error"
                # Batasi panjang pesan; jangan mengembalikan URL signed/token.
                self.last_error = self._safe_error(error)
        finally:
            if generation == self._generation and self._client is client:
                self._client = None

    async def disconnect(self) -> dict[str, Any]:
        async with self._lock:
            client = self._client
            task = self._task
            if client is None:
                self.status = "disconnected"
                self._task = None
                return await self.get_status()

            self.status = "disconnecting"
            try:
                await client.disconnect()
            except Exception as error:
                self.last_error = self._safe_error(error)

            if task is not None and not task.done():
                try:
                    await asyncio.wait_for(asyncio.shield(task), timeout=4)
                except asyncio.TimeoutError:
                    task.cancel()
                except Exception:
                    pass

            self._client = None
            self._task = None
            self.status = "disconnected"
            return await self.get_status()

    async def get_status(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "username": self.username,
            "room_id": self.room_id,
            "last_error": self.last_error,
            "connected": self.status == "connected",
        }
