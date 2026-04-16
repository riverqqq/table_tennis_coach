from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator


SpinType = Literal[
    "topspin",
    "backspin",
    "sidespin_clockwise",
    "reverse_clockwise",
    "side_top",
    "side_bottom",
    "reverse_top",
    "reverse_bottom",
    "no_spin",
    "unknown",
]

LengthType = Literal[
    "short",
    "half_long",
    "long",
    "unknown",
]

PlacementType = Literal[
    "forehand",
    "middle",
    "backhand",
    "unknown",
]

SpeedType = Literal[
    "slow",
    "fast",
    "unknown",
]

StrengthType = Literal[
    "weak",
    "strong",
    "unknown",
]


class ReceiveQueryRequest(BaseModel):
    spin: SpinType = "unknown"
    length: LengthType = "unknown"
    placement: PlacementType = "unknown"
    speed: SpeedType = "unknown"
    strength: StrengthType = "unknown"

    @model_validator(mode="after")
    def normalize_strength_for_no_spin(self) -> "ReceiveQueryRequest":
        if self.spin == "no_spin":
            self.strength = "unknown"
        return self


class ReceiveAdviceItem(BaseModel):
    key: str
    label: str
    spin: SpinType
    length: LengthType
    placement: PlacementType
    speed: SpeedType
    strength: Optional[StrengthType] = None


class ReceiveAdviceDetail(BaseModel):
    key: str
    label: str
    spin: SpinType
    length: LengthType
    placement: PlacementType
    speed: SpeedType
    strength: Optional[StrengthType] = None

    title: str
    summary: str
    advice: str
    image_prompts: List[str] = Field(default_factory=list)


class ReceiveQueryResponse(BaseModel):
    mode: Literal["insufficient", "single", "multiple"]
    known_count: int
    message: str

    query: ReceiveQueryRequest
    detail: Optional[ReceiveAdviceDetail] = None
    candidates: List[ReceiveAdviceItem] = Field(default_factory=list)
