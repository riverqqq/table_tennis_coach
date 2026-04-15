"""Core recommendation engine for the table tennis coach MVP."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from .analysis import analyze_match_pattern
from .tactical_templates import select_tactical_templates


def _count(counter_dict: Dict[str, int], tag_id: str) -> int:
    return counter_dict.get(tag_id, 0)


def _pick_best(candidates: Sequence[Tuple[str, int]], n: int) -> List[str]:
    seen = set()
    result: List[str] = []
    for text, score in sorted(candidates, key=lambda x: x[1], reverse=True):
        if text not in seen:
            seen.add(text)
            result.append(text)
        if len(result) >= n:
            break
    return result


def _build_summary(analysis: Dict[str, object], selected_template: Dict[str, object] | None = None) -> str:
    dominant_strength = analysis["dominant_strength"]
    dominant_problem = analysis["dominant_problem"]

    strength_text_map = {
        "serve_adv": "发球轮更容易主动拿分",
        "receive_adv": "接发轮存在直接上手机会",
        "rally_adv": "相持阶段有持续压制能力",
        "balanced": "目前没有单一绝对优势",
    }
    problem_text_map = {
        "receive_problem": "接发轮是最大风险点",
        "serve_problem": "发球质量需要立刻调整",
        "rally_problem": "相持阶段明显吃亏",
        "adaptation_problem": "对对手变化适应不足",
        "stable": "当前没有特别突出的短板",
    }

    base = f"这一局的整体局势是：{strength_text_map.get(dominant_strength, '有可利用优势')}，但{problem_text_map.get(dominant_problem, '也有需要处理的问题')}。"

    if selected_template and selected_template.get("summary_boost"):
        return f"{base}{selected_template['summary_boost']}"
    return base


def build_tactical_plan(
        scoring_counts: Dict[str, int],
        losing_counts: Dict[str, int],
        opponent_traits: List[str] | None = None,
) -> Dict[str, object]:
    if opponent_traits is None:
        opponent_traits = []

    analysis = analyze_match_pattern(scoring_counts, losing_counts, opponent_traits)

    main_strategy_candidates: List[Tuple[str, int]] = []
    risk_alert_candidates: List[Tuple[str, int]] = []
    action_candidates: List[Tuple[str, int]] = []

    # High-level state first: this makes the system feel more coach-like.
    if analysis["scores"]["serve_adv"] >= 4 and analysis["scores"]["receive_problem"] >= 4:
        main_strategy_candidates.append(("发球轮继续主动，但接发轮必须优先稳住", 110))
    if analysis["scores"]["serve_adv"] >= 4 and analysis["scores"]["rally_problem"] >= 4:
        main_strategy_candidates.append(("继续围绕发球和前三板拿分，尽量别把回合拖长", 108))
    if analysis["scores"]["rally_adv"] >= 4 and analysis["scores"]["receive_problem"] < 4:
        main_strategy_candidates.append(("相持阶段可以继续加压，把主动拉到中后段", 102))
    if analysis["scores"]["receive_problem"] >= 4:
        risk_alert_candidates.append(("接发轮判断吃亏明显，下一局先求稳再求抢", 105))
    if analysis["scores"]["rally_problem"] >= 4:
        risk_alert_candidates.append(("相持阶段明显吃亏，不要硬拼对方舒服节奏", 103))
    if analysis["scores"]["adaptation_problem"] >= 3:
        risk_alert_candidates.append(("对手变化已经影响判断，下一局先把选择缩窄", 96))

    # Specific scoring patterns.
    if _count(scoring_counts, "S003") >= 3:
        main_strategy_candidates.append(("继续以急长发球抢先手", 95))
        action_candidates.append(("发急长到反手或追身位", 94))

    if _count(scoring_counts, "S001") >= 3:
        main_strategy_candidates.append(("继续用短下旋发球制造高球机会", 93))
        action_candidates.append(("优先发短下旋，准备下一板上手", 92))

    if _count(scoring_counts, "S005") >= 3:
        action_candidates.append(("继续保持发球长短和旋转变化，别被对手猜到节奏", 86))

    if _count(scoring_counts, "S009") >= 2:
        action_candidates.append(("发球后主动准备第三板抢攻", 90))

    if _count(scoring_counts, "S010") >= 2:
        action_candidates.append(("前三板争取连续压制，不要只打一板", 87))

    if _count(scoring_counts, "S003") >= 3 and _count(scoring_counts, "S009") >= 2:
        main_strategy_candidates.append(("急长发球结合第三板抢攻是当前最有效套路", 104))

    if _count(scoring_counts, "S013") >= 2 and _count(scoring_counts, "S015") >= 2:
        main_strategy_candidates.append(("正手连续压制是主要得分来源", 99))
        action_candidates.append(("上手后继续压第二、第三板，不要一板结束思维", 84))

    if _count(scoring_counts, "S017") >= 2:
        action_candidates.append(("多打中路和追身，别总是只拉大角", 85))

    if _count(scoring_counts, "S018") >= 2:
        action_candidates.append(("继续用短球控制，逼对手处理短球出质量问题", 84))

    if _count(scoring_counts, "S020") >= 2:
        action_candidates.append(("继续给旋转变化，不要把球路做得太单一", 83))

    # Specific losing patterns.
    if _count(losing_counts, "L001") >= 3:
        risk_alert_candidates.append(("接发球判断吃亏明显，下一局先求稳", 100))
        action_candidates.append(("接发先以稳摆短、稳劈长为主，不要盲目抢攻", 97))

    if _count(losing_counts, "L002") >= 2:
        action_candidates.append(("对急长发球提前准备，站位不要过于靠前", 85))

    if _count(losing_counts, "L003") >= 2 or _count(losing_counts, "L004") >= 2:
        risk_alert_candidates.append(("短球处理质量不够，容易给对手上手机会", 92))
        action_candidates.append(("摆短时先求低和短，质量不够就改劈长", 88))

    if _count(losing_counts, "L005") >= 2:
        action_candidates.append(("搓长不要给对手舒服位，优先压深到反手或中路", 86))

    if _count(losing_counts, "L010") >= 2:
        risk_alert_candidates.append(("起下旋稳定性不足，别把强起当成唯一方案", 91))
        action_candidates.append(("下旋球先求拉上台和质量，不要一味发力", 87))

    if _count(losing_counts, "L013") >= 2:
        risk_alert_candidates.append(("反手相持处于下风，下一局尽量避免硬顶", 98))
        action_candidates.append(("少进入反手对反手长相持，先压中路再转线路", 95))

    if _count(losing_counts, "L014") >= 3:
        risk_alert_candidates.append(("主动失误偏多，下一局要先把稳定性提上来", 94))
        action_candidates.append(("不熟的搏杀先收住，优先重复已验证有效的套路", 84))

    if _count(losing_counts, "L015") >= 2:
        action_candidates.append(("相持中注意对手变线，站位别过早偏一侧", 83))

    if _count(losing_counts, "L016") >= 2:
        action_candidates.append(("优先准备处理中路和追身球，别让衔接卡住", 84))

    if _count(losing_counts, "L017") >= 2:
        action_candidates.append(("对方节奏在变，下一局先用简单落点把节奏拖回自己手里", 82))

    if _count(losing_counts, "L018") >= 2:
        action_candidates.append(("接发和相持都先按一种清晰判断处理，别临时猜旋转", 82))

    if _count(losing_counts, "L020") >= 2:
        risk_alert_candidates.append(("关键分执行质量下降，下一局关键分只用熟套路", 90))

    # Opponent traits.
    if "O013" in opponent_traits:
        action_candidates.append(("多给追身和中路，别让对手轻松伸展开", 90))
    if "O014" in opponent_traits:
        action_candidates.append(("继续用短球控制，逼对手短球处理出问题", 88))
    if "O010" in opponent_traits:
        main_strategy_candidates.append(("相持中继续加压，对手连续对抗能力一般", 89))
    if "O012" in opponent_traits:
        action_candidates.append(("有机会把对手拉出台，退台后继续加压", 86))
    if "O016" in opponent_traits:
        action_candidates.append(("多用旋转变化，不要总给一种球", 87))
    if "O003" in opponent_traits:
        action_candidates.append(("注意对手侧身后的空档，优先压反手再打身前", 85))
    if "O004" in opponent_traits:
        risk_alert_candidates.append(("对手接发喜欢反手拧挑，发球不要太暴露", 88))
    if "O019" in opponent_traits:
        risk_alert_candidates.append(("对长胶不要急着一味发力，先把旋转关系看清", 87))
    if "O020" in opponent_traits:
        main_strategy_candidates.append(("打削球手时要有连续进攻和二次上手准备", 86))

    # Template-based tactical chaining.
    selected_templates = select_tactical_templates(
        analysis=analysis,
        scoring_counts=scoring_counts,
        losing_counts=losing_counts,
        opponent_traits=opponent_traits,
    )
    best_template = selected_templates[0] if selected_templates else None

    # Default fallbacks.
    if not main_strategy_candidates:
        main_strategy_candidates.append(("先围绕本局最稳定的得分方式继续执行，不轻易大改", 70))

    if not risk_alert_candidates:
        risk_alert_candidates.append(("下一局先保持稳定，不要因为一两分急于搏杀", 70))

    if len(action_candidates) < 3:
        action_candidates.extend([
            ("发球和接发先求质量，再考虑抢攻", 60),
            ("相持中先争取落点主动，不急着一板打死", 60),
            ("优先重复本局已经验证有效的套路", 60),
        ])

    if best_template:
        main_strategy = str(best_template["main"])
        risk_alert = str(best_template["risk"])
        actions = list(best_template["actions"])[:3]
    else:
        main_strategy = _pick_best(main_strategy_candidates, 1)[0]
        risk_alert = _pick_best(risk_alert_candidates, 1)[0]
        actions = _pick_best(action_candidates, 3)

    summary = _build_summary(analysis, best_template)

    return {
        "summary": summary,
        "main_strategy": main_strategy,
        "risk_alert": risk_alert,
        "actions": actions,
        "analysis": {
            **analysis,
            "selected_template": best_template["name"] if best_template else None,
            "candidate_template_count": len(selected_templates),
        },
    }
