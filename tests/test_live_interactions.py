import asyncio

import pytest

from app.game.engine import QuizEngine
from app.game.question_bank import Question, QuestionBank
from app.live.interaction_manager import LiveInteractionManager


def make_bank():
    return QuestionBank([
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
    ])


@pytest.mark.asyncio
async def test_comment_answer_uses_existing_quiz_scoring():
    engine = QuizEngine(make_bank())
    interactions = LiveInteractionManager(engine)
    await engine.start_game(mode="manual", question_id="q1", question_count=1, answer_duration=20)

    result = await interactions.process_comment("Viewer", "viewer-1", "jawab b")

    assert result["accepted"] is True
    assert result["is_correct"] is True
    assert result["source"] == "tiktok"
    assert (await engine.get_state())["leaderboard"][0]["username"] == "Viewer"
    await engine.shutdown()


@pytest.mark.asyncio
async def test_non_answer_comment_is_ignored():
    engine = QuizEngine(make_bank())
    interactions = LiveInteractionManager(engine)
    result = await interactions.process_comment("Viewer", "viewer-1", "halo semua")
    assert result == {"accepted": False, "reason": "not_an_answer"}
    await engine.shutdown()


@pytest.mark.asyncio
async def test_one_follow_bonus_per_user_per_session():
    engine = QuizEngine(make_bank())
    interactions = LiveInteractionManager(engine)
    await engine.start_game(mode="manual", question_id="q1", question_count=1, answer_duration=20)

    first = await interactions.process_follow("Follower", "user-9")
    second = await interactions.process_follow("Follower", "user-9")

    assert first["accepted"] is True
    assert first["points_awarded"] == 25
    assert second["accepted"] is False
    state = await engine.get_state()
    assert state["leaderboard"][0]["score"] == 25
    assert (await interactions.get_state())["follow_bonus_count"] == 1
    await engine.shutdown()


@pytest.mark.asyncio
async def test_like_energy_extends_active_question_and_caps_at_30_seconds():
    engine = QuizEngine(make_bank())
    interactions = LiveInteractionManager(engine)
    await engine.start_game(mode="manual", question_id="q1", question_count=1, answer_duration=30)

    first = await interactions.process_like(100)
    second = await interactions.process_like(500)
    third = await interactions.process_like(100)

    assert first["applied_bonus_seconds"] == 5
    assert second["applied_bonus_seconds"] == 25
    assert third["applied_bonus_seconds"] == 0
    state = await engine.get_state()
    assert state["bonus_seconds_added"] == 30
    live = await interactions.get_state()
    assert live["likes_total"] == 700
    assert live["pending_time_seconds"] == 0
    await engine.shutdown()


@pytest.mark.asyncio
async def test_like_bonus_waits_until_next_question_is_open():
    engine = QuizEngine(make_bank())
    interactions = LiveInteractionManager(engine)
    await interactions.process_like(100)
    assert (await interactions.get_state())["pending_time_seconds"] == 5

    await engine.start_game(mode="manual", question_id="q1", question_count=1, answer_duration=20)
    applied = await interactions.flush_pending_time()
    assert applied == 5
    assert (await engine.get_state())["bonus_seconds_added"] == 5
    await engine.shutdown()


@pytest.mark.asyncio
async def test_gift_supporters_are_separate_from_quiz_scores():
    engine = QuizEngine(make_bank())
    interactions = LiveInteractionManager(engine)
    await engine.start_game(mode="manual", question_id="q1", question_count=1, answer_duration=20)

    await interactions.process_gift("GifterA", "g1", "Rose", 1, 5)
    await interactions.process_gift("GifterB", "g2", "Galaxy", 100, 1)

    live = await interactions.get_state()
    game = await engine.get_state()
    assert live["gift_total_diamonds"] == 105
    assert live["gift_leaderboard"][0]["username"] == "GifterB"
    assert live["gift_leaderboard"][0]["diamonds"] == 100
    assert game["players_count"] == 0
    assert live["gift_alert"]["gift_name"] == "Galaxy"
    await engine.shutdown()


@pytest.mark.asyncio
async def test_follow_bonus_resets_for_new_game_session():
    engine = QuizEngine(make_bank())
    interactions = LiveInteractionManager(engine)
    await engine.start_game(mode="manual", question_id="q1", question_count=1, answer_duration=20)
    assert (await interactions.process_follow("Follower", "user-9"))["accepted"] is True

    await engine.end_game()
    await engine.start_game(mode="manual", question_id="q1", question_count=1, answer_duration=20)
    await interactions.reset_session()
    result = await interactions.process_follow("Follower", "user-9")

    assert result["accepted"] is True
    await engine.shutdown()


@pytest.mark.asyncio
async def test_tiktok_username_normalization():
    from app.live.tiktok_connector import TikTokLiveBridge

    assert TikTokLiveBridge.normalize_username("@QuizMaster") == "QuizMaster"
    assert TikTokLiveBridge.normalize_username("https://www.tiktok.com/@QuizMaster/") == "QuizMaster"
    with pytest.raises(ValueError):
        TikTokLiveBridge.normalize_username("https://example.com/not-tiktok")


@pytest.mark.asyncio
async def test_like_event_batch_uses_count_without_double_counting_total():
    engine = QuizEngine(make_bank())
    interactions = LiveInteractionManager(engine)

    first = await interactions.process_like(count=25, total=25)
    second = await interactions.process_like(count=30, total=55)

    assert first["delta"] == 25
    assert second["delta"] == 30
    assert (await interactions.get_state())["likes_total"] == 55
    await engine.shutdown()
