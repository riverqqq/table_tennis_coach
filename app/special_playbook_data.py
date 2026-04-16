from __future__ import annotations

from typing import Dict, List, Optional

SPIN_LABELS: Dict[str, str] = {
    "topspin": "上旋",
    "backspin": "下旋",
    "sidespin_clockwise": "侧旋（顺时针）",
    "reverse_clockwise": "逆旋（逆时针）",
    "side_top": "侧上",
    "side_bottom": "侧下",
    "reverse_top": "逆上",
    "reverse_bottom": "逆下",
    "no_spin": "不转",
    "unknown": "未知",
}

LENGTH_LABELS: Dict[str, str] = {
    "short": "短",
    "half_long": "半出台",
    "long": "长",
    "unknown": "未知",
}

PLACEMENT_LABELS: Dict[str, str] = {
    "forehand": "正手",
    "middle": "中路",
    "backhand": "反手",
    "unknown": "未知",
}

SPEED_LABELS: Dict[str, str] = {
    "slow": "慢",
    "fast": "快",
    "unknown": "未知",
}

STRENGTH_LABELS: Dict[str, str] = {
    "weak": "弱",
    "strong": "强",
    "unknown": "未知",
}

RECEIVE_SPINS: List[str] = [
    "topspin",
    "backspin",
    "sidespin_clockwise",
    "reverse_clockwise",
    "side_top",
    "side_bottom",
    "reverse_top",
    "reverse_bottom",
    "no_spin",
]

RECEIVE_LENGTHS: List[str] = [
    "short",
    "half_long",
    "long",
]

RECEIVE_PLACEMENTS: List[str] = [
    "forehand",
    "middle",
    "backhand",
]

RECEIVE_SPEEDS: List[str] = [
    "slow",
    "fast",
]

RECEIVE_STRENGTHS: List[str] = [
    "weak",
    "strong",
]


def build_receive_key(
        spin: str,
        length: str,
        placement: str,
        speed: str,
        strength: Optional[str],
) -> str:
    """
    为每一种接发球组合生成唯一 key。
    不转球不带 strength。
    """
    if spin == "no_spin":
        return f"receive__{spin}__{length}__{placement}__{speed}"

    if not strength:
        raise ValueError("非不转球必须提供 strength")

    return f"receive__{spin}__{length}__{placement}__{speed}__{strength}"


def build_receive_label(
        spin: str,
        length: str,
        placement: str,
        speed: str,
        strength: Optional[str],
) -> str:
    """
    生成前端展示用标签。
    """
    parts = [
        SPIN_LABELS[spin],
        LENGTH_LABELS[length],
        PLACEMENT_LABELS[placement],
        SPEED_LABELS[speed],
    ]

    if spin != "no_spin" and strength:
        parts.append(STRENGTH_LABELS[strength])

    return " · ".join(parts)


def build_receive_catalog_skeleton() -> Dict[str, dict]:
    """
    生成 324 种接发球组合的骨架数据。
    说明：
    - 8 种带旋转强弱的旋转 * 3 * 3 * 2 * 2 = 288
    - 1 种不转 * 3 * 3 * 2 = 18
    实际总数是 306。

    你之前按 324 估算，是把“不转”也乘了强弱。
    如果坚持要做成 324，也可以人为给不转保留 weak/strong 两档，
    但从逻辑上更自然的是不转不分强弱。
    """
    catalog: Dict[str, dict] = {}

    spin_with_strength = [
        "topspin",
        "backspin",
        "sidespin_clockwise",
        "reverse_clockwise",
        "side_top",
        "side_bottom",
        "reverse_top",
        "reverse_bottom",
    ]

    for spin in spin_with_strength:
        for length in RECEIVE_LENGTHS:
            for placement in RECEIVE_PLACEMENTS:
                for speed in RECEIVE_SPEEDS:
                    for strength in RECEIVE_STRENGTHS:
                        key = build_receive_key(
                            spin=spin,
                            length=length,
                            placement=placement,
                            speed=speed,
                            strength=strength,
                        )
                        label = build_receive_label(
                            spin=spin,
                            length=length,
                            placement=placement,
                            speed=speed,
                            strength=strength,
                        )

                        catalog[key] = {
                            "key": key,
                            "label": label,
                            "spin": spin,
                            "length": length,
                            "placement": placement,
                            "speed": speed,
                            "strength": strength,
                            "title": f"{label} 的接发球应对",
                            "summary": "待补充",
                            "advice": "待补充",
                            "image_prompts": [],
                        }

    for length in RECEIVE_LENGTHS:
        for placement in RECEIVE_PLACEMENTS:
            for speed in RECEIVE_SPEEDS:
                key = build_receive_key(
                    spin="no_spin",
                    length=length,
                    placement=placement,
                    speed=speed,
                    strength=None,
                )
                label = build_receive_label(
                    spin="no_spin",
                    length=length,
                    placement=placement,
                    speed=speed,
                    strength=None,
                )

                catalog[key] = {
                    "key": key,
                    "label": label,
                    "spin": "no_spin",
                    "length": length,
                    "placement": placement,
                    "speed": speed,
                    "strength": None,
                    "title": f"{label} 的接发球应对",
                    "summary": "待补充",
                    "advice": "待补充",
                    "image_prompts": [],
                }

    return catalog


RECEIVE_CATALOG: Dict[str, dict] = build_receive_catalog_skeleton()

# 示例：先手动补一个真实球种，方便测试整条链是否正常显示。
_demo_key = build_receive_key(
    spin="side_top",
    length="half_long",
    placement="backhand",
    speed="fast",
    strength="strong",
)

RECEIVE_CATALOG[_demo_key] = {
    "key": _demo_key,
    "label": build_receive_label(
        spin="side_top",
        length="half_long",
        placement="backhand",
        speed="fast",
        strength="strong",
    ),
    "spin": "side_top",
    "length": "half_long",
    "placement": "backhand",
    "speed": "fast",
    "strength": "strong",
    "title": "强侧上半出台到反手的接发球应对",
    "summary": "这一类球通常兼有明显前冲感和侧拐，半出台又会让人犹豫是摆短还是直接上手。处理重点不是一味发力，而是先把拍型和摩擦方向调对，优先保证第一板判断正确。",
    "advice": "优先思路是以前上方摩擦和顺着来球侧拐方向去控制，不要用过于平的拍面硬顶。若你判断到球速快、旋转足，第一板可以选择更稳的控制型拧拉或过渡型挑打，先把球送到对方中路或反手，不必上来就强行变大角。若自己上手把握一般，也可以用带一点摩擦的压制性回接，把球控制到对方不舒服的位置，核心是别吃侧旋后直接把球弹飞或挂网。处理这类球时，脚下要先到位，尤其反手位不要站死；如果来不及完全发力，也要先完成拍型调整，再做小动作出手。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示反手位处理强侧上半出台发球，重点表现拍面略前倾、向前上方摩擦、站位中近台",
        "乒乓球专项训练示意图，展示接反手位快速强侧上半出台发球后的推荐回球线路，优先回中路或对手反手位"
    ],
}
