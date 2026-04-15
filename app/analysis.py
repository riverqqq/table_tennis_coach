"""Match pattern analysis layer.

This layer converts raw tag counts into human-meaningful match states.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


def _sum(counts: Dict[str, int], ids: List[str]) -> int:
    return sum(counts.get(tag_id, 0) for tag_id in ids)


def _level(score: int) -> str:
    if score >= 6:
        return "very_high"
    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    if score >= 1:
        return "low"
    return "none"


def analyze_match_pattern(
    scoring_counts: Dict[str, int],
    losing_counts: Dict[str, int],
    opponent_traits: List[str],
) -> Dict[str, object]:
    serve_adv = _sum(scoring_counts, ["S001", "S002", "S003", "S004", "S005", "S009", "S010"]) 
    receive_adv = _sum(scoring_counts, ["S006", "S007", "S008"]) 
    rally_adv = _sum(scoring_counts, ["S013", "S014", "S015", "S016", "S017", "S018", "S019", "S020"]) 

    receive_problem = _sum(losing_counts, ["L001", "L002", "L003", "L004", "L005", "L006"]) 
    serve_problem = _sum(losing_counts, ["L007", "L008", "L009"]) 
    rally_problem = _sum(losing_counts, ["L010", "L011", "L012", "L013", "L014", "L015", "L016"])
    adaptation_problem = _sum(losing_counts, ["L017", "L018", "L019", "L020"])

    strengths: List[Tuple[str, int]] = [
        ("serve_adv", serve_adv),
        ("receive_adv", receive_adv),
        ("rally_adv", rally_adv),
    ]
    weaknesses: List[Tuple[str, int]] = [
        ("receive_problem", receive_problem),
        ("serve_problem", serve_problem),
        ("rally_problem", rally_problem),
        ("adaptation_problem", adaptation_problem),
    ]

    strengths.sort(key=lambda x: x[1], reverse=True)
    weaknesses.sort(key=lambda x: x[1], reverse=True)

    dominant_strength = strengths[0][0] if strengths[0][1] > 0 else "balanced"
    dominant_problem = weaknesses[0][0] if weaknesses[0][1] > 0 else "stable"

    labels = []
    if serve_adv >= 4:
        labels.append("serve_dominant")
    if receive_problem >= 4:
        labels.append("receive_under_pressure")
    if rally_problem >= 4:
        labels.append("rally_under_pressure")
    if adaptation_problem >= 3:
        labels.append("reading_opponent_poorly")
    if rally_adv >= 4:
        labels.append("rally_can_score")
    if receive_adv >= 3:
        labels.append("receive_can_score")
    if "O013" in opponent_traits:
        labels.append("opponent_fears_body")
    if "O014" in opponent_traits:
        labels.append("opponent_weak_short_game")
    if "O016" in opponent_traits:
        labels.append("opponent_hates_spin_change")

    return {
        "scores": {
            "serve_adv": serve_adv,
            "receive_adv": receive_adv,
            "rally_adv": rally_adv,
            "receive_problem": receive_problem,
            "serve_problem": serve_problem,
            "rally_problem": rally_problem,
            "adaptation_problem": adaptation_problem,
        },
        "levels": {
            "serve_adv": _level(serve_adv),
            "receive_adv": _level(receive_adv),
            "rally_adv": _level(rally_adv),
            "receive_problem": _level(receive_problem),
            "serve_problem": _level(serve_problem),
            "rally_problem": _level(rally_problem),
            "adaptation_problem": _level(adaptation_problem),
        },
        "dominant_strength": dominant_strength,
        "dominant_problem": dominant_problem,
        "labels": labels,
        "top_strengths": strengths,
        "top_weaknesses": weaknesses,
    }
