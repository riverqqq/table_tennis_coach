"""FastAPI entrypoint for the table tennis coach MVP."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .profile_config import PROFILE_CONFIG
from .profile_engine import build_first_game_plan
from .profile_models import FirstGamePlanRequest, FirstGamePlanResponse, PlayerProfile

from .models import TacticRequest, TacticResponse
from .rules_engine import build_tactical_plan
from .tags import losing_reasons, opponent_traits, scoring_reasons

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Table Tennis Coach MVP", version="0.1.0")

SAVED_PROFILE: PlayerProfile | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def home():
    return FileResponse("app/static/home.html")


@app.get("/match")
def match():
    return FileResponse("app/static/index.html")


@app.get("/api/tags")
def get_tags() -> dict:
    return {
        "scoring_reasons": scoring_reasons,
        "losing_reasons": losing_reasons,
        "opponent_traits": opponent_traits,
    }


@app.get("/profile")
def read_profile_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "profile.html")


@app.get("/match-setup")
def read_match_setup_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "match_setup.html")


@app.get("/api/profile-config")
def get_profile_config() -> dict:
    return PROFILE_CONFIG


@app.post("/api/profile")
def save_profile(profile: PlayerProfile) -> dict:
    global SAVED_PROFILE
    SAVED_PROFILE = profile
    return {"ok": True}


@app.post("/api/first-game-plan", response_model=FirstGamePlanResponse)
def first_game_plan(request: FirstGamePlanRequest) -> FirstGamePlanResponse:
    return build_first_game_plan(request.profile, request.match_format)


@app.post("/api/tactical-plan", response_model=TacticResponse)
def tactical_plan(request: TacticRequest) -> TacticResponse:
    plan = build_tactical_plan(
        scoring_counts=request.scoring_counts,
        losing_counts=request.losing_counts,
        opponent_traits=request.opponent_traits,
    )
    return TacticResponse(**plan)


@app.get("/home")
def home_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "home.html")


@app.get("/match-summary")
def read_match_summary_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "match_summary.html")


@app.post("/api/match-summary")
def build_match_summary(payload: dict) -> dict:
    games = payload.get("games", [])
    match_score_me = payload.get("match_score_me", 0)
    match_score_opponent = payload.get("match_score_opponent", 0)

    if match_score_me > match_score_opponent:
        final_result = f"比赛结束，你以大比分 {match_score_me} : {match_score_opponent} 获胜。"
    else:
        final_result = f"比赛结束，你以大比分 {match_score_me} : {match_score_opponent} 失利。"

    total_scoring = {}
    total_losing = {}

    for game in games:
        for tag_id, count in game.get("scoring_counts", {}).items():
            total_scoring[tag_id] = total_scoring.get(tag_id, 0) + count
        for tag_id, count in game.get("losing_counts", {}).items():
            total_losing[tag_id] = total_losing.get(tag_id, 0) + count

    top_scoring = sorted(total_scoring.items(), key=lambda x: x[1], reverse=True)[:3]
    top_losing = sorted(total_losing.items(), key=lambda x: x[1], reverse=True)[:3]

    if top_scoring and top_losing:
        overall_summary = "本场比赛中，你有比较明确的得分手段，同时也暴露出若干稳定失分模式，适合围绕高频得分点继续强化，并优先修正最明显的失分环节。"
    elif top_scoring:
        overall_summary = "本场比赛中，你的主要得分模式较清晰，说明已有稳定得分武器，接下来应继续放大这些优势。"
    elif top_losing:
        overall_summary = "本场比赛中，失分模式比得分模式更明显，说明当前更需要先补短板、减少直接失误。"
    else:
        overall_summary = "本场比赛记录较少，暂时无法提炼出很明确的模式，后续建议继续完整记录比赛过程。"

    training_actions = []

    top_losing_ids = [tag_id for tag_id, _ in top_losing]

    if "L001" in top_losing_ids or "L006" in top_losing_ids:
        training_actions.append("重点练接发判断，尤其是识别旋转后再决定摆短、搓长或直接上手。")

    if "L002" in top_losing_ids:
        training_actions.append("加强接急长球启动训练，提升第一时间反应和上手质量。")

    if "L009" in top_losing_ids or "L010" in top_losing_ids:
        training_actions.append("增加前三板上手稳定性训练，尤其是第三板抢攻和起下旋质量。")

    if "L012" in top_losing_ids or "L014" in top_losing_ids:
        training_actions.append("加强正手连续进攻中的稳定性，减少主动失误。")

    if "L013" in top_losing_ids:
        training_actions.append("加强反手相持质量和落点控制，避免被持续压制。")

    if "L015" in top_losing_ids or "L016" in top_losing_ids:
        training_actions.append("加强中路、追身和变线下的衔接训练，提升相持中的应变能力。")

    if not training_actions:
        training_actions = [
            "保留本场最有效的发球和接发套路，形成自己的固定开局组合。",
            "继续记录每局最明显的得分与失分原因，让后续总结更准确。",
            "下一场比赛优先验证本场最有效的一项战术是否仍然成立。"
        ]

    return {
        "final_result": final_result,
        "overall_summary": overall_summary,
        "training_actions": training_actions
    }
