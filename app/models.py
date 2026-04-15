"""Pydantic models used by the API."""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field, field_validator


class TacticRequest(BaseModel):
    scoring_counts: Dict[str, int] = Field(default_factory=dict)
    losing_counts: Dict[str, int] = Field(default_factory=dict)
    opponent_traits: List[str] = Field(default_factory=list)

    @field_validator("scoring_counts", "losing_counts")
    @classmethod
    def validate_counts(cls, value: Dict[str, int]) -> Dict[str, int]:
        cleaned: Dict[str, int] = {}
        for key, count in value.items():
            if not isinstance(count, int):
                raise ValueError(f"{key} 的计数必须是整数")
            if count < 0:
                raise ValueError(f"{key} 的计数不能是负数")
            if count > 99:
                raise ValueError(f"{key} 的计数过大")
            if count > 0:
                cleaned[key] = count
        return cleaned

    @field_validator("opponent_traits")
    @classmethod
    def validate_opponent_traits(cls, value: List[str]) -> List[str]:
        cleaned = []
        seen = set()
        for item in value:
            if not isinstance(item, str):
                raise ValueError("对手特征必须是字符串")
            if item not in seen:
                seen.add(item)
                cleaned.append(item)
        return cleaned[:3]


class TacticResponse(BaseModel):
    summary: str
    main_strategy: str
    risk_alert: str
    actions: List[str]
    analysis: Dict[str, object]
