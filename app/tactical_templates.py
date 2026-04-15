"""Structured tactical templates for richer between-game coaching."""

from __future__ import annotations

from typing import Any, Dict, List


def _count(counts: Dict[str, int], tag_id: str) -> int:
    return counts.get(tag_id, 0)


def select_tactical_templates(
        analysis: Dict[str, Any],
        scoring_counts: Dict[str, int],
        losing_counts: Dict[str, int],
        opponent_traits: List[str],
) -> List[Dict[str, Any]]:
    templates: List[Dict[str, Any]] = []
    scores = analysis["scores"]
    labels = set(analysis["labels"])

    # 1. 发球 + 第三板
    if scores["serve_adv"] >= 4 and (
            _count(scoring_counts, "S001") >= 2
            or _count(scoring_counts, "S003") >= 2
            or _count(scoring_counts, "S009") >= 2
            or _count(scoring_counts, "S010") >= 2
    ):
        if _count(scoring_counts, "S003") >= 2 and _count(scoring_counts, "S009") >= 2:
            templates.append(
                {
                    "name": "serve_long_third_attack",
                    "priority": 108,
                    "main": "发急长结合第三板抢攻",
                    "risk": "不要把急长发球发成质量一般的半出台，否则容易被先上手。",
                    "summary_boost": "你当前最稳定的主动来源在发球轮，尤其适合继续围绕抢先上手展开。",
                    "actions": [
                        "发急长到对手反手或追身位，优先争取直接打乱对手接发节奏。",
                        "如果对手只是勉强顶回，第三板优先抢中路或反手，不必第一板就强行搏大角。",
                        "一旦对手开始适应急长，再夹入短下旋或短不转，保持长短结合。",
                    ],
                }
            )
        else:
            templates.append(
                {
                    "name": "serve_short_third_attack",
                    "priority": 104,
                    "main": "围绕发球抢第三板继续施压",
                    "risk": "重点不是发球花，而是发球质量和第三板准备要连起来。",
                    "summary_boost": "这一局你在发球轮更容易主动建立优势，可以继续把节奏握在自己手里。",
                    "actions": [
                        "优先用短下旋或短不转到中路、反手位，先逼出不舒服的接发。",
                        "预判对手长搓或冒高后，第三板先压中路或反手，再准备下一板变线。",
                        "不要发完球站死，发球后的第一步移动和上手准备要更主动。",
                    ],
                }
            )

    # 2. 接发问题大，先稳住
    if scores["receive_problem"] >= 4:
        actions = [
            "接发先以稳摆短、稳劈长为主，优先把球接低、接短、接到中路或反手。",
            "对急长发球提前准备，不要站位过于靠前，先防对手偷长。",
            "这一局先少用低把握度抢接发，先把接发轮失误率压下来。",
        ]
        if _count(losing_counts, "L003") >= 2 or _count(losing_counts, "L004") >= 2:
            actions[0] = "摆短时先求低和短，质量不够时直接改劈长到底线，不要摆成半出台。"
        if _count(losing_counts, "L001") >= 3:
            actions[2] = "先按一种清晰判断去接发，不要边犹豫边出手；先稳住，再慢慢增加变化。"

        templates.append(
            {
                "name": "receive_stabilize",
                "priority": 110,
                "main": "接发轮先稳住，别先送分",
                "risk": "现在最大问题不是不够凶，而是接发轮直接亏分太快。",
                "summary_boost": "这一局最需要先处理的是接发轮风险，下一局应先把最低失误方案立住。",
                "actions": actions,
            }
        )

    # 3. 相持能压制
    if scores["rally_adv"] >= 4 and scores["rally_problem"] <= 2:
        actions = [
            "相持先压中路或追身一到两板，不要一上来就只打空档大角。",
            "等对手重心和站位被压住后，再突然变线到正手大角或薄弱侧。",
            "上手后别急着一板解决，多准备第二板和第三板的连续压制。",
        ]
        if "O012" in opponent_traits:
            actions[2] = "有机会把对手拉出台，退台后继续压一板，不要轻易停手。"
        if "O013" in opponent_traits:
            actions[0] = "优先多打中路和追身，减少让对手舒展发力的机会。"

        templates.append(
            {
                "name": "rally_pressure",
                "priority": 101,
                "main": "把优势拉到相持中，用连续压制拿分",
                "risk": "相持占优时最怕自己先急躁失误，所以先压住再变线。",
                "summary_boost": "你在相持阶段已经有明显得分能力，下一局可以把主动带到中后段。",
                "actions": actions,
            }
        )

    # 4. 反手相持吃亏
    if _count(losing_counts, "L013") >= 2:
        templates.append(
            {
                "name": "avoid_bh_lock",
                "priority": 102,
                "main": "避免长时间反手对反手硬顶",
                "risk": "如果继续按对手舒服的反手节奏打，很容易被一点点压死。",
                "summary_boost": "当前相持短板主要出现在反手位，下一局需要主动改线路，不要被锁住。",
                "actions": [
                    "少主动进入反手对反手长相持，优先把第一板先压中路。",
                    "一旦对手习惯反手节奏，就尽快转到追身或正手大角，打断其连续性。",
                    "相持时先求线路变化和落点破坏，不要只拼单板质量。",
                ],
            }
        )

    # 5. 对手怕追身 / 中路
    if "opponent_fears_body" in labels or "O013" in opponent_traits:
        templates.append(
            {
                "name": "exploit_body_line",
                "priority": 98,
                "main": "重点针对中路和追身位",
                "risk": "别一味只拉两个大角，真正有效的是先让对手难受，再找空档。",
                "summary_boost": "你已经识别到对手对追身和中路处理不舒服，这一条值得继续放大。",
                "actions": [
                    "发球后或相持中优先打中路、肘部、追身位，限制对手舒展。",
                    "如果对手为了让位而侧身，下一板立刻去其空出来的一侧。",
                    "中路压住后再变线，比一开始直接搏角更稳更有效。",
                ],
            }
        )

    # 6. 对手怕短球
    if "opponent_weak_short_game" in labels or "O014" in opponent_traits or _count(scoring_counts, "S018") >= 2:
        templates.append(
            {
                "name": "short_game_exploit",
                "priority": 97,
                "main": "继续用短球控制拆对手短球处理",
                "risk": "短球战术的关键是质量，不是只要碰短就算成功。",
                "summary_boost": "对手短球处理已经暴露问题，下一局可以继续通过短球制造先手机会。",
                "actions": [
                    "发球多给短下旋、短不转和中路短球，观察对手是否继续摆高或出台。",
                    "接发能摆短时尽量摆到中路短，逼对手上步处理不舒服。",
                    "只要对手短球质量一松，就立刻准备上手，不要错过第一时间。",
                ],
            }
        )

    # 7. 对手不适应旋转变化
    if "opponent_hates_spin_change" in labels or "O016" in opponent_traits or _count(scoring_counts, "S020") >= 2:
        templates.append(
            {
                "name": "spin_variation_exploit",
                "priority": 96,
                "main": "继续用旋转变化扰乱对手判断",
                "risk": "旋转变化要建立在动作一致和基本质量上，不能为了变化而牺牲落点。",
                "summary_boost": "对手对旋转变化的适应较差，这一条可以继续作为主要突破口。",
                "actions": [
                    "发球在短下旋、短不转、侧下之间切换，但动作和节奏尽量保持相似。",
                    "相持中不要总给一种上旋质量，可偶尔加转、减转或节奏变化。",
                    "当对手开始明显犹豫时，优先把下一板打到中路或薄弱侧，而不是只追求速度。",
                ],
            }
        )

    # 8. 对手喜欢侧身正手
    if "O003" in opponent_traits:
        templates.append(
            {
                "name": "anti_pivot",
                "priority": 92,
                "main": "限制对手侧身正手，优先打其衔接空档",
                "risk": "别只看对手正手威胁，更要利用他侧身后的空位。",
                "summary_boost": "对手喜欢侧身正手，下一局要主动打他侧身后的结构漏洞。",
                "actions": [
                    "多压反手位和追身，不让对手轻松腾出位置侧身。",
                    "一旦对手侧身，下一板优先去反手空档或身前，别再回到其正手舒服位。",
                    "发球和接发尽量先把球定到中路，再观察其是否抢侧身。",
                ],
            }
        )

    # 9. 对长胶或削球
    if "O019" in opponent_traits:
        templates.append(
            {
                "name": "vs_long_pips",
                "priority": 90,
                "main": "对长胶先把旋转关系看清，再决定发力",
                "risk": "最怕一味硬冲，结果自己连续吃旋转或失误。",
                "summary_boost": "面对长胶时，稳定判断旋转关系比单纯加质量更重要。",
                "actions": [
                    "先用一两板稳的球确认回球性质，不要上来就持续暴冲。",
                    "尽量把落点打得明确，别给对手轻松借力和怪异回球空间。",
                    "有机会时再上强度，但先确保自己知道来球是什么性质。",
                ],
            }
        )

    if "O020" in opponent_traits:
        templates.append(
            {
                "name": "vs_chopper",
                "priority": 91,
                "main": "打削球要有连续进攻和二次上手准备",
                "risk": "不要指望一板打死，重点是把下一板也提前想好。",
                "summary_boost": "面对削球或防守型时，连续进攻组织比单板蛮冲更重要。",
                "actions": [
                    "第一板先进攻建立主动，但重心要准备好下一板继续上手。",
                    "落点先压中路或反手，再找空档，不要每板都只冲大角。",
                    "如果一板质量一般，不要硬续大力，先重新组织下一次机会。",
                ],
            }
        )

    # 10. 主动失误偏多
    if _count(losing_counts, "L014") >= 3 or _count(losing_counts, "L020") >= 2:
        templates.append(
            {
                "name": "reduce_unforced_errors",
                "priority": 103,
                "main": "先把主动失误降下来，再谈扩大优势",
                "risk": "现在不是没有办法，而是太多分先送掉了。",
                "summary_boost": "下一局最重要的不是变得更凶，而是把低质量失误先降下来。",
                "actions": [
                    "优先重复已经验证有效的套路，不熟的高风险搏杀先收住。",
                    "关键分只用最熟的发球、接发和上手组合，不临时换方案。",
                    "上手时先求上台率和落点，再逐步提高质量，不要每板都想一击结束。",
                ],
            }
        )

    templates.sort(key=lambda item: item["priority"], reverse=True)
    return templates
