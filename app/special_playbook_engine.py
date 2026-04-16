from __future__ import annotations

from typing import List, Optional

from .special_models import (
    ReceiveAdviceDetail,
    ReceiveAdviceItem,
    ReceiveQueryRequest,
    ReceiveQueryResponse,
)
from .special_playbook_data import RECEIVE_CATALOG, build_receive_key


def _known_count(query: ReceiveQueryRequest) -> int:
    count = 0

    if query.spin != "unknown":
        count += 1
    if query.length != "unknown":
        count += 1
    if query.placement != "unknown":
        count += 1
    if query.speed != "unknown":
        count += 1

    if query.spin != "no_spin" and query.strength != "unknown":
        count += 1

    return count


def _has_unknown(query: ReceiveQueryRequest) -> bool:
    if query.spin == "unknown":
        return True
    if query.length == "unknown":
        return True
    if query.placement == "unknown":
        return True
    if query.speed == "unknown":
        return True

    if query.spin != "no_spin" and query.strength == "unknown":
        return True

    return False


def _matches_query(item: dict, query: ReceiveQueryRequest) -> bool:
    if query.spin != "unknown" and item["spin"] != query.spin:
        return False

    if query.length != "unknown" and item["length"] != query.length:
        return False

    if query.placement != "unknown" and item["placement"] != query.placement:
        return False

    if query.speed != "unknown" and item["speed"] != query.speed:
        return False

    if query.spin != "no_spin" and query.strength != "unknown":
        if item["strength"] != query.strength:
            return False

    return True


def _to_candidate(item: dict) -> ReceiveAdviceItem:
    return ReceiveAdviceItem(
        key=item["key"],
        label=item["label"],
        spin=item["spin"],
        length=item["length"],
        placement=item["placement"],
        speed=item["speed"],
        strength=item.get("strength"),
    )


def _to_detail(item: dict) -> ReceiveAdviceDetail:
    return ReceiveAdviceDetail(
        key=item["key"],
        label=item["label"],
        spin=item["spin"],
        length=item["length"],
        placement=item["placement"],
        speed=item["speed"],
        strength=item.get("strength"),
        title=item["title"],
        summary=item["summary"],
        advice=item["advice"],
        image_prompts=item.get("image_prompts", []),
    )


def query_receive_advice(query: ReceiveQueryRequest) -> ReceiveQueryResponse:
    known_count = _known_count(query)

    if known_count < 3:
        return ReceiveQueryResponse(
            mode="insufficient",
            known_count=known_count,
            message=f"当前已知条件只有 {known_count} 项，请至少明确 3 项条件后再查询。",
            query=query,
            detail=None,
            candidates=[],
        )

    if not _has_unknown(query):
        strength: Optional[str] = None if query.spin == "no_spin" else query.strength
        key = build_receive_key(
            spin=query.spin,
            length=query.length,
            placement=query.placement,
            speed=query.speed,
            strength=strength,
        )
        item = RECEIVE_CATALOG.get(key)

        if item is None:
            return ReceiveQueryResponse(
                mode="single",
                known_count=known_count,
                message="未找到对应球种，请检查数据是否完整。",
                query=query,
                detail=None,
                candidates=[],
            )

        return ReceiveQueryResponse(
            mode="single",
            known_count=known_count,
            message="已找到明确球种的专项应对内容。",
            query=query,
            detail=_to_detail(item),
            candidates=[],
        )

    matched_items: List[dict] = [
        item for item in RECEIVE_CATALOG.values() if _matches_query(item, query)
    ]

    matched_items.sort(key=lambda x: x["label"])

    candidates = [_to_candidate(item) for item in matched_items]

    return ReceiveQueryResponse(
        mode="multiple",
        known_count=known_count,
        message=f"当前存在“未知”，共匹配到 {len(candidates)} 种可能球种。",
        query=query,
        detail=None,
        candidates=candidates,
    )
