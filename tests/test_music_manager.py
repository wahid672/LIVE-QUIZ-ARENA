import pytest
from app.live.music_manager import AudioPlaylistManager


TRACK_ONE = "https://example.com/audio/song_one.mp3"
TRACK_TWO = "https://example.com/music/epic_quiz.wav"
TRACK_THREE = "https://example.com/stream/ambience.mov"


def test_parse_direct_audio_links():
    first = AudioPlaylistManager.parse_url(TRACK_ONE)
    second = AudioPlaylistManager.parse_url(TRACK_TWO)
    third = AudioPlaylistManager.parse_url(TRACK_THREE)

    assert first["kind"] == "mp3"
    assert first["extension"] == ".mp3"
    assert first["title"] == "Song One"

    assert second["kind"] == "wav"
    assert second["extension"] == ".wav"
    assert second["title"] == "Epic Quiz"

    assert third["kind"] == "mov"
    assert third["extension"] == ".mov"
    assert third["title"] == "Ambience"


def test_reject_invalid_audio_extensions():
    with pytest.raises(ValueError):
        AudioPlaylistManager.parse_url("https://example.com/page.html")
    with pytest.raises(ValueError):
        AudioPlaylistManager.parse_url("https://youtube.com/watch?v=dQw4w9WgXcQ")
    with pytest.raises(ValueError):
        AudioPlaylistManager.parse_url("")


@pytest.mark.asyncio
async def test_add_multiple_audio_links_skip_duplicates_and_persist(tmp_path):
    storage = tmp_path / "music_playlist.json"
    manager = AudioPlaylistManager(storage)

    result = await manager.add_urls([TRACK_ONE, TRACK_TWO, TRACK_ONE, "https://example.com/bad.txt"])
    assert result["added_count"] == 2
    assert len(result["queue"]) == 2
    assert len(result["invalid"]) == 1
    assert result["current_index"] == 0

    restored = AudioPlaylistManager(storage)
    state = await restored.get_state()
    assert len(state["queue"]) == 2
    assert state["current_track"]["url"] == TRACK_ONE
    assert state["is_playing"] is False


@pytest.mark.asyncio
async def test_audio_controls_next_previous_loop_and_volume(tmp_path):
    manager = AudioPlaylistManager(tmp_path / "music_playlist.json")
    await manager.add_urls([TRACK_ONE, TRACK_TWO])

    state = await manager.control("play")
    assert state["is_playing"] is True

    state = await manager.control("next")
    assert state["current_index"] == 1
    assert state["current_track"]["url"] == TRACK_TWO

    await manager.control("loop", loop=True)
    state = await manager.control("ended")
    assert state["current_index"] == 0
    assert state["is_playing"] is True

    state = await manager.control("volume", volume=40)
    assert state["volume"] == 40

    state = await manager.control("previous")
    assert state["current_index"] == 1


@pytest.mark.asyncio
async def test_remove_current_track_selects_next_and_stops_when_empty(tmp_path):
    manager = AudioPlaylistManager(tmp_path / "music_playlist.json")
    result = await manager.add_urls([TRACK_ONE, TRACK_TWO])
    track1_key = result["queue"][0]["track_key"]
    track2_key = result["queue"][1]["track_key"]

    await manager.control("play")
    state = await manager.remove_track(track1_key)
    assert state["current_index"] == 0
    assert state["current_track"]["url"] == TRACK_TWO

    state = await manager.remove_track(track2_key)
    assert state["queue"] == []
    assert state["current_track"] is None
    assert state["is_playing"] is False
