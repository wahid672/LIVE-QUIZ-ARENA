import asyncio

import pytest

from app.game.engine import GamePhase, QuizEngine
from app.game.question_bank import Question, QuestionBank


def make_bank() -> QuestionBank:
    questions = [
        Question(
            id="q1",
            category="Test",
            question="Berapakah 2 + 2?",
            options={"A": "3", "B": "4", "C": "5", "D": "6"},
            correct_answer="B",
            explanation="2 + 2 = 4.",
            hint="Hitung dua ditambah dua.",
        ),
        Question(
            id="q2",
            category="Test",
            question="Berapakah 3 + 3?",
            options={"A": "5", "B": "7", "C": "6", "D": "8"},
            correct_answer="C",
            explanation="3 + 3 = 6.",
            hint="Hitung tiga ditambah tiga.",
        ),
    ]
    return QuestionBank(questions)


@pytest.mark.asyncio
async def test_correct_answer_awards_points():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=1,
        answer_duration=10,
    )

    result = await engine.submit_answer("PemainSatu", "B")

    assert result["accepted"] is True
    assert result["is_correct"] is True
    assert result["points_awarded"] >= 100
    state = await engine.get_state()
    assert state["leaderboard"][0]["username"] == "PemainSatu"

    await engine.shutdown()


@pytest.mark.asyncio
async def test_player_can_only_answer_once_per_question():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=1,
        answer_duration=10,
    )

    first = await engine.submit_answer("PemainSatu", "A")
    second = await engine.submit_answer("PemainSatu", "B")

    assert first["accepted"] is True
    assert second["accepted"] is False
    assert second["reason"] == "already_answered"

    await engine.shutdown()


@pytest.mark.asyncio
async def test_timer_moves_game_to_reveal():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=1,
        answer_duration=1,
    )

    await asyncio.sleep(1.15)
    state = await engine.get_state()

    assert state["phase"] == GamePhase.REVEAL.value
    assert state["current_question"]["correct_answer"] == "B"

    await engine.shutdown()


@pytest.mark.asyncio
async def test_manual_next_question():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=2,
        answer_duration=5,
    )
    await engine.end_game()

    # Start a fresh session and let the first question reveal by ending its timer.
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=2,
        answer_duration=1,
    )
    await asyncio.sleep(1.1)
    state = await engine.next_question(mode="manual", question_id="q2")

    assert state["question_number"] == 2
    assert state["current_question"]["id"] == "q2"

    await engine.shutdown()


@pytest.mark.asyncio
async def test_auto_play_advances_to_next_question():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=2,
        answer_duration=1,
        auto_play=True,
        auto_advance_delay=1,
    )

    await asyncio.sleep(2.2)
    state = await engine.get_state()

    assert state["question_number"] == 2
    assert state["phase"] == GamePhase.QUESTION.value
    assert state["current_question"]["id"] == "q2"
    assert state["auto_play"] is True

    await engine.shutdown()


@pytest.mark.asyncio
async def test_auto_play_finishes_after_last_question():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=1,
        answer_duration=1,
        auto_play=True,
        auto_advance_delay=1,
    )

    await asyncio.sleep(2.2)
    state = await engine.get_state()

    assert state["phase"] == GamePhase.FINISHED.value
    assert state["question_number"] == 1

    await engine.shutdown()


@pytest.mark.asyncio
async def test_manual_next_cancels_pending_auto_advance():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=2,
        answer_duration=1,
        auto_play=True,
        auto_advance_delay=3,
    )

    await asyncio.sleep(1.1)
    state = await engine.next_question(mode="manual", question_id="q2")
    assert state["question_number"] == 2
    assert state["current_question"]["id"] == "q2"

    await asyncio.sleep(2.1)
    state = await engine.get_state()
    # The manually started question remains active; the previous round's
    # scheduled auto-advance must not fire a second time.
    assert state["question_number"] == 2
    assert state["current_question"]["id"] == "q2"

    await engine.shutdown()



@pytest.mark.asyncio
async def test_first_correct_viewer_gets_fastest_bonus_and_round_summary():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=1,
        answer_duration=20,
    )

    wrong = await engine.submit_answer("Penonton Salah", "A")
    fastest = await engine.submit_answer("Penonton Cepat", "B")
    later = await engine.submit_answer("Penonton Lain", "B")

    assert wrong["accepted"] is True
    assert wrong["is_correct"] is False
    assert wrong["fastest_bonus"] == 0

    assert fastest["accepted"] is True
    assert fastest["is_correct"] is True
    assert fastest["is_fastest"] is True
    assert fastest["fastest_bonus"] == 50
    assert fastest["points_awarded"] >= 150

    assert later["accepted"] is True
    assert later["is_fastest"] is False
    assert later["fastest_bonus"] == 0

    state = await engine.end_game()
    assert state["round_summary"]["correct_count"] == 2
    assert state["round_summary"]["wrong_count"] == 1
    assert state["round_summary"]["answered_count"] == 3
    assert state["fastest_answer"]["username"] == "Penonton Cepat"

    await engine.shutdown()


@pytest.mark.asyncio
async def test_large_question_count_and_endless_mode():
    engine = QuizEngine(make_bank())
    state = await engine.start_game(
        mode="random",
        question_count=200,
        answer_duration=10,
    )
    assert state["question_count"] == 200
    assert state["endless"] is False

    await engine.end_game()

    endless_state = await engine.start_game(
        mode="random",
        endless=True,
        answer_duration=10,
    )
    assert endless_state["endless"] is True
    assert endless_state["question_count"] == 0

    await engine.shutdown()


@pytest.mark.asyncio
async def test_round_ends_in_waiting_gift_and_continues_on_target_reached():
    engine = QuizEngine(make_bank())
    await engine.start_game(
        mode="manual",
        question_id="q1",
        question_count=1,
        answer_duration=1,
        auto_play=True,
        auto_advance_delay=1,
        gift_target_to_continue=5,
    )

    await asyncio.sleep(2.2)
    state = await engine.get_state()
    assert state["phase"] == GamePhase.WAITING_GIFT.value
    assert state["waiting_gift"] is not None
    assert state["waiting_gift"]["target"] == 5
    assert state["waiting_gift"]["collected"] == 0
    assert state["waiting_gift"]["reached"] is False

    res1 = await engine.add_continue_gift(diamonds=2, username="Budi")
    assert res1["accepted"] is True
    assert res1["collected"] == 2
    assert res1["reached"] is False

    res2 = await engine.add_continue_gift(diamonds=3, username="Siti")
    assert res2["accepted"] is True
    assert res2["collected"] == 5
    assert res2["reached"] is True

    # Tunggu auto-continue delay (2.5 detik)
    await asyncio.sleep(2.7)
    next_state = await engine.get_state()
    assert next_state["phase"] == GamePhase.QUESTION.value
    assert next_state["batch_round"] == 2
    assert next_state["question_number"] == 1

    # Akhiri game manual
    ended_state = await engine.end_game()
    assert ended_state["phase"] == GamePhase.FINISHED.value

    await engine.shutdown()
