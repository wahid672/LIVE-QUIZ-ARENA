import asyncio
import math
import random
import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

from app.game.question_bank import Question, QuestionBank


class GamePhase(str, Enum):
    IDLE = "idle"
    QUESTION = "question"
    PAUSED = "paused"
    REVEAL = "reveal"
    FINISHED = "finished"
    WAITING_GIFT = "waiting_gift"


@dataclass
class Player:
    player_id: str
    username: str
    score: int = 0
    streak: int = 0
    correct_answers: int = 0
    total_answers: int = 0


class QuizEngine:
    """
    Mesin permainan kuis.
    Seluruh operasi state dilindungi asyncio.Lock agar event bersamaan
    tidak mengubah skor atau jawaban pemain secara tumpang tindih.
    """

    def __init__(self, question_bank: QuestionBank):
        self.question_bank = question_bank
        self._lock = asyncio.Lock()
        self._timer_task: asyncio.Task | None = None
        self._auto_advance_task: asyncio.Task | None = None
        self._round_token = 0

        self._phase = GamePhase.IDLE
        self._mode = "random"
        self._question_count = 10
        self._answer_duration = 15
        self._auto_play = False
        self._auto_advance_delay = 4
        self._question_number = 0

        self._current_question: Question | None = None
        self._players: dict[str, Player] = {}
        self._answers: dict[str, dict[str, Any]] = {}
        self._fastest_correct: dict[str, Any] | None = None
        self._used_question_ids: set[str] = set()
        self._last_random_question_id: str | None = None

        self._deadline: float | None = None
        self._advance_deadline: float | None = None
        self._paused_remaining = 0.0
        self._question_extension_total = 0

        self._endless = False
        self._gift_target_to_continue = 0
        self._gift_collected_for_continue = 0
        self._batch_round = 1
        self._continue_scheduled = False
        self._delayed_continue_task: asyncio.Task | None = None

    @staticmethod
    def parse_answer(raw_answer: str) -> str | None:
        """
        Format jawaban yang diterima:
        A, B, C, D, atau 'JAWAB A'.
        Komentar lain tidak dianggap sebagai jawaban.
        """
        match = re.fullmatch(
            r"\s*(?:JAWAB\s+)?([ABCD])\s*[.!]?\s*",
            raw_answer or "",
            flags=re.IGNORECASE,
        )
        return match.group(1).upper() if match else None

    async def start_game(
        self,
        mode: str = "random",
        question_id: str | None = None,
        question_count: int = 10,
        answer_duration: int = 15,
        auto_play: bool = False,
        auto_advance_delay: int = 4,
        endless: bool = False,
        gift_target_to_continue: int = 0,
    ) -> dict[str, Any]:
        if mode not in {"random", "manual"}:
            raise ValueError("Mode soal harus 'random' atau 'manual'.")
        if not endless and question_count < 1:
            raise ValueError("Jumlah pertanyaan minimal 1 (atau aktifkan mode endless).")
        if answer_duration < 1:
            raise ValueError("Durasi menjawab minimal 1 detik.")
        if not 1 <= auto_advance_delay <= 30:
            raise ValueError("Jeda auto play harus antara 1 sampai 30 detik.")

        async with self._lock:
            if self._phase not in {GamePhase.IDLE, GamePhase.FINISHED, GamePhase.WAITING_GIFT}:
                raise ValueError("Permainan sedang berjalan. Akhiri permainan sebelum memulai sesi baru.")

            self._cancel_timer_locked()
            self._cancel_advance_locked()
            if self._delayed_continue_task and not self._delayed_continue_task.done():
                self._delayed_continue_task.cancel()
            self._phase = GamePhase.IDLE
            self._players.clear()
            self._answers.clear()
            self._fastest_correct = None
            self._used_question_ids.clear()
            self._last_random_question_id = None

            self._mode = mode
            self._endless = bool(endless) or (question_count == 0)
            self._question_count = 0 if self._endless else question_count
            self._answer_duration = answer_duration
            self._auto_play = bool(auto_play)
            self._auto_advance_delay = auto_advance_delay
            self._question_number = 1
            self._gift_target_to_continue = max(0, int(gift_target_to_continue or 0))
            self._gift_collected_for_continue = 0
            self._batch_round = 1
            self._continue_scheduled = False

            question = self._select_question_locked(mode, question_id)
            self._start_question_locked(question)
            return self._state_locked()

    async def submit_answer(
        self,
        username: str,
        answer: str,
        user_id: str | None = None,
    ) -> dict[str, Any]:
        clean_username = username.strip()
        if not clean_username:
            raise ValueError("Username tidak boleh kosong.")

        normalized_answer = self.parse_answer(answer)
        if normalized_answer is None:
            raise ValueError("Jawaban harus A, B, C, D, atau 'JAWAB A'.")

        player_key = (user_id or clean_username).strip().casefold()
        if not player_key:
            raise ValueError("ID pemain tidak valid.")

        async with self._lock:
            if self._phase != GamePhase.QUESTION:
                return {
                    "accepted": False,
                    "reason": "question_not_open",
                    "message": "Pertanyaan sedang tidak menerima jawaban.",
                }

            now = time.monotonic()
            if self._deadline is None or now >= self._deadline:
                self._reveal_locked()
                return {
                    "accepted": False,
                    "reason": "time_expired",
                    "message": "Waktu menjawab sudah habis.",
                }

            if player_key in self._answers:
                return {
                    "accepted": False,
                    "reason": "already_answered",
                    "message": "Jawaban pertama pemain sudah tercatat.",
                }

            if self._current_question is None:
                raise RuntimeError("Tidak ada pertanyaan aktif.")

            player = self._players.get(player_key)
            if player is None:
                player = Player(player_id=player_key, username=clean_username)
                self._players[player_key] = player
            else:
                # Perbarui tampilan nama jika username berubah.
                player.username = clean_username

            remaining = max(0.0, self._deadline - now)
            is_correct = normalized_answer == self._current_question.correct_answer

            points_awarded = 0
            speed_bonus = 0
            streak_bonus = 0
            fastest_bonus = 0
            is_fastest = False

            if is_correct:
                speed_bonus = math.floor(
                    50 * min(1.0, remaining / self._answer_duration)
                )
                # Bonus streak mulai diberikan setelah satu jawaban benar beruntun.
                streak_bonus = min(player.streak * 10, 30)

                # Penjawab benar pertama pada setiap ronde mendapat bonus khusus.
                # asyncio.Lock memastikan hanya satu pemain yang bisa menjadi tercepat.
                if self._fastest_correct is None:
                    fastest_bonus = 50
                    is_fastest = True
                    self._fastest_correct = {
                        "username": player.username,
                        "bonus_points": fastest_bonus,
                        "answer": normalized_answer,
                    }

                points_awarded = 100 + speed_bonus + streak_bonus + fastest_bonus

                player.score += points_awarded
                player.streak += 1
                player.correct_answers += 1
            else:
                player.streak = 0

            player.total_answers += 1
            answer_record = {
                "username": player.username,
                "answer": normalized_answer,
                "is_correct": is_correct,
                "points_awarded": points_awarded,
            }
            self._answers[player_key] = answer_record

            return {
                "accepted": True,
                "username": player.username,
                "answer": normalized_answer,
                "is_correct": is_correct,
                "points_awarded": points_awarded,
                "score": player.score,
                "speed_bonus": speed_bonus,
                "streak_bonus": streak_bonus,
                "fastest_bonus": fastest_bonus,
                "is_fastest": is_fastest,
                "streak": player.streak,
                "message": "Jawaban berhasil dicatat.",
            }


    async def extend_time(self, seconds: int, max_bonus_per_question: int = 30) -> dict[str, Any]:
        """Tambahkan waktu pada soal aktif dengan batas bonus per ronde."""
        if seconds <= 0:
            return {"accepted": False, "reason": "invalid_seconds", "added_seconds": 0}

        async with self._lock:
            if self._phase != GamePhase.QUESTION or self._deadline is None:
                return {"accepted": False, "reason": "question_not_open", "added_seconds": 0}

            now = time.monotonic()
            if now >= self._deadline:
                self._reveal_locked()
                return {"accepted": False, "reason": "time_expired", "added_seconds": 0}

            remaining_cap = max(0, max_bonus_per_question - self._question_extension_total)
            added = min(int(seconds), remaining_cap)
            if added <= 0:
                return {"accepted": False, "reason": "bonus_cap_reached", "added_seconds": 0}

            self._question_extension_total += added
            self._deadline += added

            # Ganti timer lama agar reveal mengikuti deadline yang baru.
            self._cancel_timer_locked()
            self._round_token += 1
            token = self._round_token
            remaining = max(0.0, self._deadline - time.monotonic())
            self._timer_task = asyncio.create_task(
                self._auto_reveal_after(token, remaining)
            )
            return {
                "accepted": True,
                "reason": "time_extended",
                "added_seconds": added,
                "total_bonus_seconds": self._question_extension_total,
                "remaining_seconds": round(remaining, 1),
            }

    async def award_bonus_points(
        self,
        username: str,
        user_id: str | None,
        points: int,
        reason: str = "community_bonus",
    ) -> dict[str, Any]:
        """Berikan bonus komunitas tanpa mengonsumsi kesempatan menjawab."""
        clean_username = (username or "").strip()
        if not clean_username:
            clean_username = "TikTok Viewer"
        if points <= 0:
            return {"accepted": False, "reason": "invalid_points"}

        player_key = (user_id or clean_username).strip().casefold()
        async with self._lock:
            if self._phase not in {
                GamePhase.QUESTION, GamePhase.PAUSED, GamePhase.REVEAL
            }:
                return {"accepted": False, "reason": "no_active_session"}

            player = self._players.get(player_key)
            if player is None:
                player = Player(player_id=player_key, username=clean_username)
                self._players[player_key] = player
            else:
                player.username = clean_username

            player.score += int(points)
            return {
                "accepted": True,
                "username": player.username,
                "points_awarded": int(points),
                "score": player.score,
                "reason": reason,
            }

    async def next_question(
        self,
        mode: str | None = None,
        question_id: str | None = None,
    ) -> dict[str, Any]:
        async with self._lock:
            if self._phase != GamePhase.REVEAL:
                raise ValueError("Soal berikutnya hanya dapat dimulai setelah hasil ditampilkan.")

            self._cancel_advance_locked()

            if not self._endless and self._question_number >= self._question_count:
                if self._gift_target_to_continue > 0:
                    self._phase = GamePhase.WAITING_GIFT
                    self._deadline = None
                    self._advance_deadline = None
                    self._paused_remaining = 0.0
                    self._cancel_timer_locked()
                    self._gift_collected_for_continue = 0
                    self._continue_scheduled = False
                    return self._state_locked()
                else:
                    self._phase = GamePhase.FINISHED
                    self._deadline = None
                    self._advance_deadline = None
                    self._paused_remaining = 0.0
                    self._cancel_timer_locked()
                    return self._state_locked()

            next_mode = mode or self._mode
            if next_mode not in {"random", "manual"}:
                raise ValueError("Mode soal harus 'random' atau 'manual'.")

            question = self._select_question_locked(next_mode, question_id)
            self._mode = next_mode
            self._question_number += 1
            self._start_question_locked(question)
            return self._state_locked()

    async def pause_game(self) -> dict[str, Any]:
        async with self._lock:
            if self._phase != GamePhase.QUESTION:
                raise ValueError("Permainan hanya dapat dijeda saat pertanyaan aktif.")

            now = time.monotonic()
            self._paused_remaining = max(0.0, (self._deadline or now) - now)

            if self._paused_remaining <= 0:
                self._reveal_locked()
                return self._state_locked()

            self._cancel_timer_locked()
            self._deadline = None
            self._phase = GamePhase.PAUSED
            return self._state_locked()

    async def resume_game(self) -> dict[str, Any]:
        async with self._lock:
            if self._phase != GamePhase.PAUSED:
                raise ValueError("Tidak ada permainan yang sedang dijeda.")

            remaining = self._paused_remaining
            if remaining <= 0:
                self._reveal_locked()
                return self._state_locked()

            self._phase = GamePhase.QUESTION
            self._round_token += 1
            token = self._round_token
            self._deadline = time.monotonic() + remaining
            self._paused_remaining = 0.0
            self._timer_task = asyncio.create_task(
                self._auto_reveal_after(token, remaining)
            )
            return self._state_locked()

    async def continue_next_round(self, force: bool = False) -> dict[str, Any]:
        async with self._lock:
            if self._phase not in {GamePhase.WAITING_GIFT, GamePhase.FINISHED}:
                raise ValueError("Game tidak dalam status menunggu kelanjutan ronde.")
            if not force and self._gift_target_to_continue > 0:
                if self._gift_collected_for_continue < self._gift_target_to_continue:
                    raise ValueError(
                        f"Gift belum mencapai target ({self._gift_collected_for_continue}/{self._gift_target_to_continue})."
                    )

            self._cancel_timer_locked()
            self._cancel_advance_locked()
            if self._delayed_continue_task and not self._delayed_continue_task.done():
                self._delayed_continue_task.cancel()

            self._batch_round += 1
            self._question_number = 1
            self._gift_collected_for_continue = 0
            self._continue_scheduled = False
            self._answers.clear()
            self._fastest_correct = None

            if len(self._used_question_ids) >= len(self.question_bank.all()):
                self._used_question_ids.clear()

            if self._mode == "random":
                question = self._select_question_locked("random", None)
            else:
                question = self._select_next_manual_locked()

            self._start_question_locked(question)
            return self._state_locked()

    async def add_continue_gift(self, diamonds: int, username: str = "Viewer") -> dict[str, Any]:
        async with self._lock:
            if self._phase != GamePhase.WAITING_GIFT:
                return {"accepted": False, "reason": "not_waiting_gift"}

            self._gift_collected_for_continue += max(0, int(diamonds))
            reached = (
                self._gift_target_to_continue > 0
                and self._gift_collected_for_continue >= self._gift_target_to_continue
            )

            if reached and not self._continue_scheduled:
                self._continue_scheduled = True
                self._delayed_continue_task = asyncio.create_task(
                    self._delayed_continue(delay=2.5)
                )

            return {
                "accepted": True,
                "diamonds_added": diamonds,
                "collected": self._gift_collected_for_continue,
                "target": self._gift_target_to_continue,
                "reached": reached,
                "username": username,
            }

    async def _delayed_continue(self, delay: float = 2.5) -> None:
        try:
            await asyncio.sleep(delay)
            await self.continue_next_round(force=True)
        except asyncio.CancelledError:
            return
        except Exception:
            pass

    async def end_game(self) -> dict[str, Any]:
        async with self._lock:
            self._cancel_timer_locked()
            self._cancel_advance_locked()
            if self._delayed_continue_task and not self._delayed_continue_task.done():
                self._delayed_continue_task.cancel()
            self._deadline = None
            self._advance_deadline = None
            self._paused_remaining = 0.0
            self._gift_collected_for_continue = 0
            self._continue_scheduled = False
            self._phase = GamePhase.FINISHED
            return self._state_locked()

    async def get_state(self) -> dict[str, Any]:
        async with self._lock:
            # Pemeriksaan tambahan untuk menghindari state QUESTION tertinggal
            # jika timer dan request state tiba hampir bersamaan.
            if (
                self._phase == GamePhase.QUESTION
                and self._deadline is not None
                and time.monotonic() >= self._deadline
            ):
                self._reveal_locked()
            return self._state_locked()

    async def shutdown(self) -> None:
        async with self._lock:
            self._cancel_timer_locked()
            self._cancel_advance_locked()
            if self._delayed_continue_task and not self._delayed_continue_task.done():
                self._delayed_continue_task.cancel()

    def admin_questions(self) -> list[dict[str, Any]]:
        return self.question_bank.admin_list()

    def _select_question_locked(
        self,
        mode: str,
        question_id: str | None,
    ) -> Question:
        if mode == "manual":
            if not question_id:
                raise ValueError("Pilih question_id untuk mode manual.")
            return self.question_bank.get(question_id)

        if mode != "random":
            raise ValueError("Mode soal tidak dikenal.")

        available = [
            question
            for question in self.question_bank.all()
            if question.id not in self._used_question_ids
        ]

        if not available:
            self._used_question_ids.clear()
            available = self.question_bank.all()

        if len(available) > 1 and self._last_random_question_id:
            without_last = [
                question for question in available
                if question.id != self._last_random_question_id
            ]
            if without_last:
                available = without_last

        question = random.choice(available)
        self._used_question_ids.add(question.id)
        self._last_random_question_id = question.id
        return question

    def _start_question_locked(self, question: Question) -> None:
        self._current_question = question
        self._question_extension_total = 0
        self._answers = {}
        self._fastest_correct = None
        self._phase = GamePhase.QUESTION
        self._paused_remaining = 0.0

        self._round_token += 1
        token = self._round_token
        self._deadline = time.monotonic() + self._answer_duration
        self._timer_task = asyncio.create_task(
            self._auto_reveal_after(token, self._answer_duration)
        )

    async def _auto_reveal_after(self, token: int, duration: float) -> None:
        try:
            await asyncio.sleep(duration)
            async with self._lock:
                if token == self._round_token and self._phase == GamePhase.QUESTION:
                    self._reveal_locked()
        except asyncio.CancelledError:
            return

    async def _auto_advance_after(self, token: int, delay: int) -> None:
        try:
            await asyncio.sleep(delay)
            async with self._lock:
                if (
                    token != self._round_token
                    or self._phase != GamePhase.REVEAL
                    or not self._auto_play
                ):
                    return

                self._auto_advance_task = None
                self._advance_deadline = None

                if not self._endless and self._question_number >= self._question_count:
                    if self._gift_target_to_continue > 0:
                        self._phase = GamePhase.WAITING_GIFT
                        self._deadline = None
                        self._advance_deadline = None
                        self._paused_remaining = 0.0
                        self._gift_collected_for_continue = 0
                        self._continue_scheduled = False
                        return
                    else:
                        self._phase = GamePhase.FINISHED
                        self._deadline = None
                        self._paused_remaining = 0.0
                        return

                if self._mode == "random":
                    question = self._select_question_locked("random", None)
                else:
                    question = self._select_next_manual_locked()

                self._question_number += 1
                self._start_question_locked(question)
        except asyncio.CancelledError:
            return

    def _select_next_manual_locked(self) -> Question:
        """Auto-play manual mode follows the bank order from the selected question."""
        questions = self.question_bank.all()
        if not questions:
            raise ValueError("Bank soal kosong.")

        current_id = self._current_question.id if self._current_question else None
        current_index = next(
            (index for index, question in enumerate(questions) if question.id == current_id),
            -1,
        )
        next_index = (current_index + 1) % len(questions)
        return questions[next_index]

    def _reveal_locked(self) -> None:
        self._phase = GamePhase.REVEAL
        self._deadline = None
        self._paused_remaining = 0.0
        self._cancel_timer_locked()

        self._cancel_advance_locked()
        if self._auto_play:
            self._advance_deadline = time.monotonic() + self._auto_advance_delay
            token = self._round_token
            self._auto_advance_task = asyncio.create_task(
                self._auto_advance_after(token, self._auto_advance_delay)
            )

    def _cancel_advance_locked(self) -> None:
        task = self._auto_advance_task
        self._auto_advance_task = None
        self._advance_deadline = None
        if task is not None and task is not asyncio.current_task():
            task.cancel()

    def _cancel_timer_locked(self) -> None:
        task = self._timer_task
        self._timer_task = None
        if task is not None and task is not asyncio.current_task():
            task.cancel()

    def _leaderboard_locked(self) -> list[dict[str, Any]]:
        ranked = sorted(
            self._players.values(),
            key=lambda player: (
                -player.score,
                -player.correct_answers,
                -player.streak,
                player.username.casefold(),
            ),
        )
        return [
            {
                "rank": index,
                "username": player.username,
                "score": player.score,
                "streak": player.streak,
                "correct_answers": player.correct_answers,
                "total_answers": player.total_answers,
            }
            for index, player in enumerate(ranked, start=1)
        ]

    def _round_summary_locked(self) -> dict[str, Any]:
        correct_count = sum(
            1 for answer in self._answers.values() if answer.get("is_correct")
        )
        total_answers = len(self._answers)
        wrong_count = total_answers - correct_count
        return {
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "answered_count": total_answers,
            "fastest_answer": dict(self._fastest_correct) if self._fastest_correct else None,
        }

    def _state_locked(self) -> dict[str, Any]:
        if self._phase == GamePhase.QUESTION and self._deadline is not None:
            remaining = max(0.0, self._deadline - time.monotonic())
        elif self._phase == GamePhase.PAUSED:
            remaining = self._paused_remaining
        else:
            remaining = 0.0

        current = None
        if self._current_question is not None:
            current = {
                "id": self._current_question.id,
                "category": self._current_question.category,
                "question": self._current_question.question,
                "options": self._current_question.options,
            }
            # Kunci jawaban hanya dikirim setelah waktu menjawab berakhir.
            if self._phase in {GamePhase.REVEAL, GamePhase.FINISHED, GamePhase.WAITING_GIFT}:
                current["correct_answer"] = self._current_question.correct_answer
                current["explanation"] = self._current_question.explanation
            elif self._phase == GamePhase.PAUSED:
                current["hint"] = self._current_question.hint

        auto_advance_remaining = 0.0
        if self._phase == GamePhase.REVEAL and self._advance_deadline is not None:
            auto_advance_remaining = max(
                0.0, self._advance_deadline - time.monotonic()
            )

        waiting_gift_data = None
        if self._phase == GamePhase.WAITING_GIFT:
            target = self._gift_target_to_continue
            collected = self._gift_collected_for_continue
            remaining_diamonds = max(0, target - collected)
            pct = 100 if target <= 0 else min(100, int((collected / max(1, target)) * 100))
            waiting_gift_data = {
                "target": target,
                "collected": collected,
                "remaining": remaining_diamonds,
                "progress_percent": pct,
                "reached": target > 0 and collected >= target,
                "batch_round": self._batch_round,
                "batch_question_count": self._question_count,
            }

        return {
            "phase": self._phase.value,
            "mode": self._mode,
            "endless": self._endless,
            "batch_round": self._batch_round,
            "gift_target_to_continue": self._gift_target_to_continue,
            "gift_collected_for_continue": self._gift_collected_for_continue,
            "waiting_gift": waiting_gift_data,
            "auto_play": self._auto_play,
            "auto_advance_delay": self._auto_advance_delay,
            "auto_advance_remaining_seconds": round(auto_advance_remaining, 1),
            "question_number": self._question_number,
            "question_count": self._question_count,
            "answer_duration": self._answer_duration,
            "bonus_seconds_added": self._question_extension_total,
            "remaining_seconds": round(remaining, 1),
            "current_question": current,
            "players_count": len(self._players),
            "answered_count": len(self._answers),
            "fastest_answer": dict(self._fastest_correct) if self._fastest_correct else None,
            "round_summary": (
                self._round_summary_locked()
                if self._phase in {GamePhase.REVEAL, GamePhase.FINISHED, GamePhase.WAITING_GIFT}
                else None
            ),
            "leaderboard": self._leaderboard_locked(),
        }
