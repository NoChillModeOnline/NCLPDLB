"""
FastAPI Web Backend — REST + WebSocket API for the React dashboard.
Serves draft board, standings, team data, replays, and video metadata.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config import settings
from src.data.pokeapi import pokemon_db
from src.services.analytics_service import AnalyticsService
from src.services.draft_service import DraftService
from src.services.elo_service import EloService
from src.services.team_service import TeamService

log = logging.getLogger(__name__)

# Active WebSocket connections per guild
_ws_clients: dict[str, list[WebSocket]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pokemon_db.load()
    log.info("Pokemon database loaded")
    yield


app = FastAPI(
    title="Pokemon Draft League API",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

draft_svc = DraftService()
elo_svc = EloService()
team_svc = TeamService()
analytics_svc = AnalyticsService()


# ── Health ────────────────────────────────────────────────────
@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "pokemon_loaded": len(pokemon_db.all())}


# ── Pokemon ───────────────────────────────────────────────────
@app.get("/api/pokemon")
async def list_pokemon(tier: str = "", gen: int = 0, q: str = "") -> list[dict]:
    if q:
        results = pokemon_db.search(q)
    elif tier:
        results = pokemon_db.filter_by_tier(tier)
    elif gen:
        results = pokemon_db.filter_by_generation(gen)
    else:
        results = pokemon_db.all()
    return [p.model_dump() for p in results[:100]]


@app.get("/api/pokemon/{name}")
async def get_pokemon(name: str) -> dict:
    p = pokemon_db.find(name)
    if not p:
        raise HTTPException(404, f"Pokemon '{name}' not found")
    return p.model_dump()


# ── Drafts ────────────────────────────────────────────────────
@app.get("/api/drafts/{guild_id}")
async def get_draft(guild_id: str) -> dict:
    draft = await draft_svc.get_active_draft(guild_id)
    if not draft:
        raise HTTPException(404, "No active draft")
    return draft.model_dump()


class PickRequest(BaseModel):
    player_id: str
    pokemon_name: str

@app.post("/api/drafts/{guild_id}/pick")
async def make_pick(guild_id: str, req: PickRequest) -> dict:
    result = await draft_svc.make_pick(guild_id, req.player_id, req.pokemon_name)
    if not result.success:
        raise HTTPException(400, result.error)
    await _broadcast(guild_id, {"event": "pick", "pokemon": req.pokemon_name, "player": req.player_id})
    return {"success": True, "next_player": result.next_player_name}


# ── Teams ─────────────────────────────────────────────────────
@app.get("/api/teams/{guild_id}/{player_id}")
async def get_team(guild_id: str, player_id: str) -> dict:
    roster = await team_svc.get_team(guild_id, player_id)
    if not roster:
        raise HTTPException(404, "Team not found")
    return roster.model_dump()


@app.get("/api/teams/{guild_id}/{player_id}/analysis")
async def get_analysis(guild_id: str, player_id: str) -> dict:
    report = await analytics_svc.analyze_team(guild_id, player_id)
    return {
        "coverage": report.coverage_summary,
        "weaknesses": report.weakness_summary,
        "speed_tiers": report.speed_tiers,
        "archetype": report.archetype,
        "threat_score": report.threat_score,
        "role_distribution": report.role_distribution,
    }


# ── Standings ─────────────────────────────────────────────────
@app.get("/api/leagues/{guild_id}/standings")
async def get_standings(guild_id: str) -> list[dict]:
    standings = await elo_svc.get_standings(guild_id)
    return [
        {
            "player_id": p.player_id,
            "display_name": p.display_name,
            "elo": p.elo,
            "wins": p.wins,
            "losses": p.losses,
            "win_rate": round(p.win_rate, 1),
        }
        for p in standings
    ]


# ── Matchup ───────────────────────────────────────────────────
@app.get("/api/matchups/{guild_id}/{p1_id}/{p2_id}")
async def get_matchup(guild_id: str, p1_id: str, p2_id: str) -> dict:
    from src.services.battle_sim import BattleSimService
    sim = BattleSimService()
    result = await sim.compare_teams(guild_id, p1_id, p2_id)
    return {
        "advantage": result.advantage_summary,
        "p1_threats": result.p1_threats,
        "p2_threats": result.p2_threats,
        "type_summary": result.type_summary,
        "p1_score": result.p1_score,
        "p2_score": result.p2_score,
    }


# ── WebSocket — Live Draft Board ──────────────────────────────
@app.websocket("/ws/{guild_id}")
async def websocket_draft(websocket: WebSocket, guild_id: str):
    await websocket.accept()
    _ws_clients.setdefault(guild_id, []).append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep-alive ping
    except WebSocketDisconnect:
        _ws_clients[guild_id].remove(websocket)


async def _broadcast(guild_id: str, data: dict) -> None:
    """Broadcast a draft event to all connected dashboard clients."""
    dead = []
    for ws in _ws_clients.get(guild_id, []):
        try:
            await ws.send_json(data)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _ws_clients[guild_id].remove(ws)
