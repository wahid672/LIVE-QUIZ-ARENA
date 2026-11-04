from typing import Literal

from pydantic import BaseModel, Field

from app.core.config import DEFAULT_ANSWER_DURATION, DEFAULT_QUESTION_COUNT


class StartGameRequest(BaseModel):
    mode: Literal["random", "manual"] = "random"
    question_id: str | None = None
    question_count: int = Field(default=DEFAULT_QUESTION_COUNT, ge=0, le=10000)
    answer_duration: int = Field(default=DEFAULT_ANSWER_DURATION, ge=5, le=120)
    auto_play: bool = False
    auto_advance_delay: int = Field(default=4, ge=1, le=30)
    endless: bool = False
    gift_target_to_continue: int = Field(default=5, ge=0, le=100000)


class ContinueRoundRequest(BaseModel):
    force: bool = True


class SetGiftTargetRequest(BaseModel):
    target: int = Field(default=5, ge=0, le=100000)


class ToggleCharacterAnimationRequest(BaseModel):
    enabled: bool


class ThemeChangeRequest(BaseModel):
    theme: str = Field(min_length=1, max_length=64)


class TTSSettingRequest(BaseModel):
    mode: Literal["locked_id", "browser", "disabled"] = "locked_id"


class NextQuestionRequest(BaseModel):
    mode: Literal["random", "manual"] | None = None
    question_id: str | None = None


class AnswerRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    user_id: str | None = Field(default=None, max_length=128)
    answer: str = Field(min_length=1, max_length=20)


class TikTokConnectRequest(BaseModel):
    username: str = Field(min_length=2, max_length=100)


class TikTokTestEventRequest(BaseModel):
    event_type: Literal["comment", "like", "follow", "gift"]
    username: str = Field(default="TestViewer", min_length=1, max_length=64)
    user_id: str | None = Field(default="test-viewer-001", max_length=128)
    comment: str = Field(default="A", max_length=200)
    like_count: int = Field(default=100, ge=1, le=100000)
    gift_name: str = Field(default="Rose", max_length=64)
    diamonds: int = Field(default=1, ge=0, le=100000)
    quantity: int = Field(default=1, ge=1, le=1000)


class MusicPlaylistAddRequest(BaseModel):
    urls: list[str] = Field(min_length=1, max_length=30)


class MusicPlaylistRemoveRequest(BaseModel):
    track_key: str = Field(min_length=3, max_length=160)


class MusicControlRequest(BaseModel):
    action: Literal["play", "pause", "next", "previous", "select", "volume", "loop", "ended"]
    track_key: str | None = Field(default=None, max_length=160)
    volume: int | None = Field(default=None, ge=0, le=100)
    loop: bool | None = None


class QuestionCreateRequest(BaseModel):
    id: str | None = Field(default=None, max_length=32)
    category: str = Field(min_length=1, max_length=64)
    question: str = Field(min_length=1, max_length=1000)
    options: dict[str, str]
    correct_answer: Literal["A", "B", "C", "D"]
    explanation: str = Field(default="", max_length=2000)
    hint: str = Field(default="", max_length=500)


class QuestionUpdateRequest(BaseModel):
    category: str = Field(min_length=1, max_length=64)
    question: str = Field(min_length=1, max_length=1000)
    options: dict[str, str]
    correct_answer: Literal["A", "B", "C", "D"]
    explanation: str = Field(default="", max_length=2000)
    hint: str = Field(default="", max_length=500)
