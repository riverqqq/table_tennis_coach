from __future__ import annotations

from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


Handedness = Literal["right", "left"]
Grip = Literal["shakehand", "penhold"]
Style = Literal["attack", "control", "rally", "defense", "chop"]
Distance = Literal["close", "mid_close", "mid_far"]
Rubber = Literal["inverted", "sticky", "tensor", "short_pips", "long_pips", "anti"]
Blade = Literal["hard", "neutral", "soft"]
MatchFormat = Literal["bo1", "bo3", "bo5", "bo7"]


class PlayerProfile(BaseModel):
    grip: Grip = "shakehand"
    handedness: Handedness = "right"
    style: Style = "attack"
    distance: Distance = "mid_close"

    forehand_rubber: Rubber = "sticky"
    backhand_rubber: Rubber = "inverted"
    blade_feel: Blade = "neutral"

    serve_skills: Dict[str, int] = Field(default_factory=dict)
    receive_skills: Dict[str, int] = Field(default_factory=dict)
    attack_skills: Dict[str, int] = Field(default_factory=dict)
    control_skills: Dict[str, int] = Field(default_factory=dict)


class MatchSetupRequest(BaseModel):
    match_format: MatchFormat


class FirstGamePlanRequest(BaseModel):
    profile: PlayerProfile
    match_format: MatchFormat


class FirstGamePlanResponse(BaseModel):
    serve_plan: List[str]
    receive_plan: List[str]
    reminders: List[str]
    summary: str
