import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.schemas import (
    AnswerRequest,
    NextQuestionRequest,
    StartGameRequest,
    TikTokConnectRequest,
    TikTokTestEventRequest,
    MusicPlaylistAddRequest,
    MusicPlaylistRemoveRequest,
    MusicControlRequest,
)
from app.api.websocket import ConnectionManager
from app.core.config import APP_NAME, QUESTION_FILE
from app.game.engine import QuizEngine
from app.game.question_bank import QuestionBank
from app.live.interaction_manager import LiveInteractionManager
from app.live.tiktok_connector import TikTokLiveBridge
from app.live.music_manager import AudioPlaylistManager

BASE_DIR = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = BASE_DIR / "frontend" / "dashboard"
OVERLAY_DIR = BASE_DIR / "frontend" / "overlay"


async def _state_broadcaster(app: FastAPI) -> None:
    """Kirim snapshot game berkala agar timer overlay ikut bergerak realtime."""
    while True:
        try:
            await app.state.interactions.flush_pending_time()
            state = await app.state.engine.get_state()
            live_state = await app.state.interactions.get_state()
            connection_state = await app.state.tiktok.get_status()
            music_state = await app.state.music.get_state()
            await app.state.connections.broadcast({
                "type": "game_state",
                "data": state,
                "live": live_state,
                "connection": connection_state,
                "music": music_state,
            })
        except asyncio.CancelledError:
            raise
        except Exception:
            # Gangguan satu broadcast tidak boleh mematikan loop pembaruan.
            pass
        await asyncio.sleep(0.4)


@asynccontextmanager
async def lifespan(app: FastAPI):
    question_bank = QuestionBank.from_file(QUESTION_FILE)
    app.state.engine = QuizEngine(question_bank)
    app.state.connections = ConnectionManager()
    app.state.interactions = LiveInteractionManager(app.state.engine)
    app.state.tiktok = TikTokLiveBridge(app.state.interactions)
    app.state.music = AudioPlaylistManager(BASE_DIR / "data" / "music_playlist.json")
    broadcaster = asyncio.create_task(_state_broadcaster(app))
    try:
        yield
    finally:
        broadcaster.cancel()
        await asyncio.gather(broadcaster, return_exceptions=True)
        await app.state.tiktok.disconnect()
        await app.state.engine.shutdown()


app = FastAPI(
    title=APP_NAME,
    description="Game kuis interaktif untuk TikTok LIVE.",
    version="0.7.0",
    lifespan=lifespan,
)

app.mount(
    "/static/dashboard",
    StaticFiles(directory=str(DASHBOARD_DIR)),
    name="dashboard-static",
)
app.mount(
    "/static/overlay",
    StaticFiles(directory=str(OVERLAY_DIR)),
    name="overlay-static",
)


def get_engine(request: Request) -> QuizEngine:
    return request.app.state.engine


@app.get("/", tags=["General"])
async def home() -> dict[str, str]:
    return {
        "app": APP_NAME,
        "status": "online",
        "dashboard": "/dashboard",
        "overlay": "/overlay",
        "api_docs": "/docs",
    }


@app.get("/dashboard", include_in_schema=False)
async def dashboard() -> FileResponse:
    return FileResponse(DASHBOARD_DIR / "index.html")


@app.get("/overlay", include_in_schema=False)
async def overlay() -> FileResponse:
    return FileResponse(OVERLAY_DIR / "index.html")


@app.get("/health", tags=["General"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(status_code=204)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    manager: ConnectionManager = websocket.app.state.connections
    await manager.connect(websocket)
    try:
        state = await websocket.app.state.engine.get_state()
        live_state = await websocket.app.state.interactions.get_state()
        connection_state = await websocket.app.state.tiktok.get_status()
        music_state = await websocket.app.state.music.get_state()
        await websocket.send_json({
            "type": "game_state", "data": state,
            "live": live_state, "connection": connection_state,
            "music": music_state,
        })
        # Client tidak perlu mengirim data; menunggu disconnect menjaga koneksi hidup.
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await manager.disconnect(websocket)


@app.get("/api/game/state", tags=["Game"])
async def game_state(request: Request) -> dict[str, Any]:
    return await get_engine(request).get_state()


@app.get("/api/questions", tags=["Questions"])
async def list_questions(request: Request) -> list[dict[str, Any]]:
    # Endpoint admin lokal ini menyertakan kunci jawaban. Jangan publikasikan
    # server tanpa autentikasi dan pembatasan akses.
    return get_engine(request).admin_questions()


@app.post("/api/game/start", tags=["Game"])
async def start_game(
    payload: StartGameRequest,
    request: Request,
) -> dict[str, Any]:
    try:
        result = await get_engine(request).start_game(
            mode=payload.mode,
            question_id=payload.question_id,
            question_count=payload.question_count,
            answer_duration=payload.answer_duration,
            auto_play=payload.auto_play,
            auto_advance_delay=payload.auto_advance_delay,
            endless=payload.endless,
            gift_target_to_continue=payload.gift_target_to_continue,
        )
        await request.app.state.interactions.reset_session()
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/game/continue-round", tags=["Game"])
async def continue_round(request: Request) -> dict[str, Any]:
    try:
        return await get_engine(request).continue_next_round(force=True)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/game/answer", tags=["Game"])
async def submit_answer(
    payload: AnswerRequest,
    request: Request,
) -> dict[str, Any]:
    try:
        result = await get_engine(request).submit_answer(
            username=payload.username,
            user_id=payload.user_id,
            answer=payload.answer,
        )
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/game/next", tags=["Game"])
async def next_question(
    payload: NextQuestionRequest,
    request: Request,
) -> dict[str, Any]:
    try:
        return await get_engine(request).next_question(
            mode=payload.mode,
            question_id=payload.question_id,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/game/pause", tags=["Game"])
async def pause_game(request: Request) -> dict[str, Any]:
    try:
        return await get_engine(request).pause_game()
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/game/resume", tags=["Game"])
async def resume_game(request: Request) -> dict[str, Any]:
    try:
        return await get_engine(request).resume_game()
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error



@app.get("/api/tiktok/status", tags=["TikTok LIVE"])
async def tiktok_status(request: Request) -> dict[str, Any]:
    return {
        "connection": await request.app.state.tiktok.get_status(),
        "interactions": await request.app.state.interactions.get_state(),
    }


@app.post("/api/tiktok/connect", tags=["TikTok LIVE"])
async def tiktok_connect(
    payload: TikTokConnectRequest,
    request: Request,
) -> dict[str, Any]:
    try:
        return await request.app.state.tiktok.connect(payload.username)
    except (ValueError, RuntimeError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/tiktok/disconnect", tags=["TikTok LIVE"])
async def tiktok_disconnect(request: Request) -> dict[str, Any]:
    return await request.app.state.tiktok.disconnect()


@app.post("/api/tiktok/test-event", tags=["TikTok LIVE"])
async def tiktok_test_event(
    payload: TikTokTestEventRequest,
    request: Request,
) -> dict[str, Any]:
    interactions = request.app.state.interactions
    if payload.event_type == "comment":
        return await interactions.process_comment(
            payload.username, payload.user_id, payload.comment, source="simulator"
        )
    if payload.event_type == "like":
        return await interactions.process_like(
            payload.like_count, payload.username, source="simulator"
        )
    if payload.event_type == "follow":
        return await interactions.process_follow(
            payload.username, payload.user_id, source="simulator"
        )
    return await interactions.process_gift(
        payload.username, payload.user_id, payload.gift_name,
        payload.diamonds, payload.quantity, source="simulator"
    )



@app.get("/api/music/state", tags=["Music"])
async def music_state(request: Request) -> dict[str, Any]:
    return await request.app.state.music.get_state()


@app.post("/api/music/playlist/add", tags=["Music"])
async def music_add_tracks(
    payload: MusicPlaylistAddRequest,
    request: Request,
) -> dict[str, Any]:
    return await request.app.state.music.add_urls(payload.urls)


@app.post("/api/music/playlist/remove", tags=["Music"])
async def music_remove_track(
    payload: MusicPlaylistRemoveRequest,
    request: Request,
) -> dict[str, Any]:
    try:
        return await request.app.state.music.remove_track(payload.track_key)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/music/control", tags=["Music"])
async def music_control(
    payload: MusicControlRequest,
    request: Request,
) -> dict[str, Any]:
    try:
        return await request.app.state.music.control(
            action=payload.action,
            track_key=payload.track_key,
            volume=payload.volume,
            loop=payload.loop,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/game/end", tags=["Game"])
async def end_game(request: Request) -> dict[str, Any]:
    return await get_engine(request).end_game()
