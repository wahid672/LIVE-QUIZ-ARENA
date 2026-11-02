import asyncio
import time
from collections import deque
from typing import Any

from app.game.engine import GamePhase, QuizEngine


class LiveInteractionManager:
    """Menerjemahkan event LIVE menjadi aksi game yang terukur dan aman."""

    def __init__(
        self,
        engine: QuizEngine,
        likes_per_reward: int = 100,
        seconds_per_reward: int = 5,
        follow_bonus_points: int = 25,
    ):
        self.engine = engine
        self.likes_per_reward = likes_per_reward
        self.seconds_per_reward = seconds_per_reward
        self.follow_bonus_points = follow_bonus_points
        self._lock = asyncio.Lock()
        self._session_followers: set[str] = set()
        self._likes_total = 0
        self._last_reported_like_total: int | None = None
        self._like_energy = 0
        self._pending_time_seconds = 0
        self._follow_bonus_count = 0
        self._gift_total_diamonds = 0
        self._gift_count = 0
        self._gift_supporters: dict[str, dict[str, Any]] = {}
        self._recent_events: deque[dict[str, Any]] = deque(maxlen=20)
        self._event_sequence = 0
        self._gift_alert: dict[str, Any] | None = None

    async def reset_session(self) -> None:
        async with self._lock:
            self._session_followers.clear()
            self._likes_total = 0
            self._last_reported_like_total = None
            self._like_energy = 0
            self._pending_time_seconds = 0
            self._follow_bonus_count = 0
            self._gift_total_diamonds = 0
            self._gift_count = 0
            self._gift_supporters.clear()
            self._recent_events.clear()
            self._gift_alert = None

    def _record_locked(
        self,
        event_type: str,
        username: str,
        detail: str,
        status: str = "received",
    ) -> None:
        self._event_sequence += 1
        self._recent_events.appendleft({
            "id": self._event_sequence,
            "type": event_type,
            "username": username or "Viewer",
            "detail": detail,
            "status": status,
            "timestamp": time.time(),
        })

    async def process_comment(
        self,
        username: str,
        user_id: str | None,
        comment: str,
        source: str = "tiktok",
    ) -> dict[str, Any]:
        normalized = QuizEngine.parse_answer(comment)
        if normalized is None:
            return {"accepted": False, "reason": "not_an_answer"}

        result = await self.engine.submit_answer(
            username=username,
            user_id=user_id,
            answer=normalized,
        )
        async with self._lock:
            detail = f"Jawaban {normalized}"
            if result.get("accepted"):
                detail += " · benar" if result.get("is_correct") else " · salah"
                detail += f" · +{result.get('points_awarded', 0)} poin"
            else:
                detail += f" · {result.get('message', 'ditolak')}"
            self._record_locked("comment", username, detail, "accepted" if result.get("accepted") else "ignored")
        result["source"] = source
        return result

    async def process_like(
        self,
        count: int = 1,
        username: str = "Community",
        total: int | None = None,
        source: str = "tiktok",
    ) -> dict[str, Any]:
        delta = max(0, int(count or 0))
        if delta == 0 and total is not None:
            async with self._lock:
                # Gunakan perubahan total hanya sebagai fallback jika count kosong.
                previous = getattr(self, "_last_reported_like_total", None)
                if previous is not None:
                    delta = max(0, int(total) - previous)
                self._last_reported_like_total = max(int(total), previous or 0)

        async with self._lock:
            if delta <= 0:
                return {"accepted": False, "reason": "no_new_likes", "delta": 0}

            self._likes_total += delta
            self._like_energy += delta
            rewards = self._like_energy // self.likes_per_reward
            self._like_energy %= self.likes_per_reward
            queued_seconds = rewards * self.seconds_per_reward
            self._pending_time_seconds += queued_seconds

            applied = await self._apply_pending_time_locked()
            self._record_locked(
                "like",
                username or "Community",
                f"+{delta} likes · total {self._likes_total}",
                "reward" if queued_seconds else "received",
            )
            return {
                "accepted": True,
                "delta": delta,
                "likes_total": self._likes_total,
                "energy": self._like_energy,
                "queued_bonus_seconds": queued_seconds,
                "applied_bonus_seconds": applied,
            }

    async def _apply_pending_time_locked(self) -> int:
        if self._pending_time_seconds <= 0:
            return 0
        state = await self.engine.get_state()
        if state["phase"] != GamePhase.QUESTION.value:
            return 0

        result = await self.engine.extend_time(self._pending_time_seconds)
        added = int(result.get("added_seconds", 0))
        self._pending_time_seconds = max(0, self._pending_time_seconds - added)

        if result.get("reason") == "bonus_cap_reached":
            discarded = self._pending_time_seconds
            self._pending_time_seconds = 0
            self._record_locked(
                "system",
                "LIVE QUIZ ARENA",
                f"Batas bonus waktu per soal tercapai; {discarded} detik tidak diterapkan.",
                "notice",
            )
        elif added:
            self._record_locked(
                "system",
                "LIVE QUIZ ARENA",
                f"Community Energy membuka +{added} detik.",
                "reward",
            )
        return added

    async def flush_pending_time(self) -> int:
        async with self._lock:
            return await self._apply_pending_time_locked()

    async def process_follow(
        self,
        username: str,
        user_id: str | None,
        source: str = "tiktok",
    ) -> dict[str, Any]:
        clean_name = username or "New follower"
        key = (user_id or clean_name).strip().casefold()
        async with self._lock:
            if key in self._session_followers:
                return {"accepted": False, "reason": "already_rewarded"}

            result = await self.engine.award_bonus_points(
                username=clean_name,
                user_id=user_id,
                points=self.follow_bonus_points,
                reason="follow_bonus",
            )
            if result.get("accepted"):
                self._session_followers.add(key)
                self._follow_bonus_count += 1
                self._record_locked(
                    "follow",
                    clean_name,
                    f"Follow bonus +{self.follow_bonus_points} poin",
                    "reward",
                )
            else:
                self._record_locked("follow", clean_name, "Follow diterima; bonus menunggu sesi game aktif.", "received")
            result["source"] = source
            return result

    async def process_gift(
        self,
        username: str,
        user_id: str | None,
        gift_name: str,
        diamonds: int,
        quantity: int = 1,
        source: str = "tiktok",
    ) -> dict[str, Any]:
        clean_name = username or "Gift supporter"
        gift_name = gift_name or "Gift"
        quantity = max(1, int(quantity or 1))
        diamonds = max(0, int(diamonds or 0))
        total_diamonds = diamonds * quantity
        key = (user_id or clean_name).strip().casefold()

        async with self._lock:
            supporter = self._gift_supporters.setdefault(key, {
                "username": clean_name,
                "diamonds": 0,
                "gift_count": 0,
            })
            supporter["username"] = clean_name
            supporter["diamonds"] += total_diamonds
            supporter["gift_count"] += quantity
            self._gift_total_diamonds += total_diamonds
            self._gift_count += quantity
            self._gift_alert = {
                "id": self._event_sequence + 1,
                "username": clean_name,
                "gift_name": gift_name,
                "quantity": quantity,
                "diamonds": total_diamonds,
                "expires_at": time.time() + 8,
            }
            self._record_locked(
                "gift",
                clean_name,
                f"Mengirim {quantity}× {gift_name} · {total_diamonds} diamonds",
                "support",
            )
            continue_res = await self.engine.add_continue_gift(total_diamonds, clean_name)
            return {
                "accepted": True,
                "username": clean_name,
                "gift_name": gift_name,
                "quantity": quantity,
                "diamonds": total_diamonds,
                "source": source,
                "round_continue": continue_res,
            }

    async def get_state(self) -> dict[str, Any]:
        async with self._lock:
            supporters = sorted(
                self._gift_supporters.values(),
                key=lambda item: (-item["diamonds"], -item["gift_count"], item["username"].casefold()),
            )
            alert = dict(self._gift_alert) if self._gift_alert else None
            if alert and alert["expires_at"] <= time.time():
                alert = None
                self._gift_alert = None

            return {
                "likes_total": self._likes_total,
                "likes_per_reward": self.likes_per_reward,
                "like_energy": self._like_energy,
                "pending_time_seconds": self._pending_time_seconds,
                "seconds_per_reward": self.seconds_per_reward,
                "follow_bonus_points": self.follow_bonus_points,
                "follow_bonus_count": self._follow_bonus_count,
                "gift_total_diamonds": self._gift_total_diamonds,
                "gift_count": self._gift_count,
                "gift_leaderboard": [
                    {
                        "rank": index,
                        "username": item["username"],
                        "diamonds": item["diamonds"],
                        "gift_count": item["gift_count"],
                    }
                    for index, item in enumerate(supporters[:5], start=1)
                ],
                "recent_events": list(self._recent_events),
                "gift_alert": alert,
            }
