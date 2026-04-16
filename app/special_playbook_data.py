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

# 上旋类
# 上旋 + 短 + 正手 + 慢 + 弱
_topspin_short_forehand_slow_weak_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="forehand",
    speed="slow",
    strength="weak",
)

RECEIVE_CATALOG[_topspin_short_forehand_slow_weak_key] = {
    "key": _topspin_short_forehand_slow_weak_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="forehand",
        speed="slow",
        strength="weak",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "forehand",
    "speed": "slow",
    "strength": "weak",
    "title": "弱上旋短球到正手的接发球应对",
    "summary": "这类球旋转较弱但带一定前冲，落点短且速度慢，容易被误判为不转或下旋。处理关键在于避免用过于后仰拍面去“搓”，应以主动摩擦或轻挑为主，优先控制住弧线和落点。",
    "advice": "**①正手挑打/挑拉：**站位靠近球台，右脚稍前或平行站位，身体前倾，重心压低，右手持拍时肘部自然前伸。引拍小幅向后下方，拍型略前倾约20°–30°以适应上旋。击球时机选择上升期或高点期，击球点在身体右前方、接近台面位置。触球在球的中上部，以摩擦为主、带轻微撞击。发力主要来自前臂向前上方送出，配合手腕轻微上提，方向为前+上，整体感觉是把球“提”出去并控制弧线。\n\n**②正手快点/轻打：**站位贴近球台，身体放松但前倾，肘部在身体前侧作为支点。拍型保持前倾约15°–25°。击球在高点期，击球点在身体右前方。触球在球的中部偏上，以撞击为主、摩擦为辅。发力以小幅前臂快速前送为主，手腕稳定略有前压，身体重心轻微前移，发力方向为正前方略带上。整体是借来球轻上旋把球稳定送过去，适合保守过渡。\n\n**③摆短控制：**站位非常靠近球台，上半身略探出台面，重心低且稳定。拍型接近垂直或略后仰（约80°–90°），避免因为上旋直接弹高。击球时机在上升后期，击球点在身体前方较近位置。触球在球的中下部，以轻摩擦为主。发力来自手腕和手指的细微控制，方向为略向下+轻前送。核心是通过“吸球”把球控制短，不让其因为上旋二跳出台。\n\n**④正手劈长/撇长：**站位靠近球台但准备主动发力，身体略向右侧转。拍型前倾约30°左右。击球时机在高点期或略早，击球点在身体右前方。触球在球的中部偏上，以摩擦为主带一点撞击。发力由前臂前送+手腕发力完成，方向为前+侧（可劈对方反手或中路）。整体是利用上旋的前冲性，把球快速送到对方底线，制造节奏变化。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示正手位处理短上旋发球的挑打动作，重点表现拍面略前倾、前上方发力",
        "乒乓球战术示意图，展示正手短球接发后摆短与劈长两种落点选择（近网短球与对方底线反手）"
    ],
}

# 上旋 + 短 + 正手 + 慢 + 强
_topspin_short_forehand_slow_strong_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="forehand",
    speed="slow",
    strength="strong",
)

RECEIVE_CATALOG[_topspin_short_forehand_slow_strong_key] = {
    "key": _topspin_short_forehand_slow_strong_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="forehand",
        speed="slow",
        strength="strong",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "forehand",
    "speed": "slow",
    "strength": "strong",
    "title": "强上旋短球到正手的接发球应对",
    "summary": "这类球上旋明显但落点较短，第一跳靠近网，第二跳有向前冲出台的趋势，极易被误判为不转或轻下旋。若用搓球处理很容易冒高或直接出台。应对关键在于拍型前倾、主动上手，通过前上方摩擦或控制性触球来稳定弧线。",
    "advice": "**①正手挑打/挑拉：**站位紧贴球台，右脚稍前，身体前倾，重心压低，肘部自然前伸至台内。引拍幅度小，拍头略低于来球，拍型前倾约30°–45°以压住上旋。击球时机选择上升期或接近高点期，击球点在身体右前方靠近台面。触球在球的中上部，以摩擦为主，适当带一点撞击。发力由前臂向前上方送出，配合手腕向上提拉，方向为前+上。整体感觉是主动“包住球往上带”，避免球被顶飞。\n\n**②正手快点/压制性轻打：**站位靠近球台，身体前倾但保持放松，肘部稳定在身体前方作为支点。拍型前倾约20°–30°。击球在高点期，击球点在身体右前方。触球在球的中部偏上，以撞击为主、摩擦为辅。发力主要来自前臂快速前送，手腕略微前压控制弧线，身体重心轻微前移。发力方向为正前方略带上。整体是利用来球上旋进行稳定过渡，适合在来不及充分发力时使用。\n\n**③正手劈长/撇长变化：**站位靠近球台但准备主动发力，身体略向右侧转。拍型前倾约30°–40°。击球时机在高点期或略提前，击球点在身体右前方。触球在球的中上部，以摩擦为主并带一定撞击。发力由前臂快速前送结合手腕发力完成，方向为前+侧（可劈对方反手或中路深处）。整体是利用强上旋的前冲性，把球快速送到底线，形成节奏变化或直接压制。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示正手位处理强上旋短球的挑打动作，重点表现拍面前倾和前上方发力",
        "乒乓球战术示意图，展示接强上旋短球后摆短与劈长的落点对比（近网控制与底线压制）"
    ],
}

# 上旋 + 短 + 正手 + 快 + 弱
_topspin_short_forehand_fast_weak_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="forehand",
    speed="fast",
    strength="weak",
)

RECEIVE_CATALOG[_topspin_short_forehand_fast_weak_key] = {
    "key": _topspin_short_forehand_fast_weak_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="forehand",
        speed="fast",
        strength="weak",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "forehand",
    "speed": "fast",
    "strength": "weak",
    "title": "弱上旋短球到正手的接发球应对",
    "summary": "这类球虽然上旋不算很强，但球速更急、落点更短，容易让人来不及上步或误判成不转短球。处理关键不是大动作发力，而是尽早上步抢点，拍型略前倾，优先用小动作把球快而稳地处理到对方不容易直接上手的位置。",
    "advice": "**①正手快挑/快挑拉：**站位要比接慢短球更积极，脚下先启动，右手持拍时右脚迅速插入台内或至少迈出小垫步，身体前倾，重心压低到前脚掌。引拍不要大，拍头略低于来球，手腕自然放松，拍型前倾约20°–30°。击球时机尽量放在上升期偏早阶段，不能等球走到下降期再出手。击球点在身体右前方、贴近台面的位置。触球以球的中上部为主，先薄摩擦再顺势轻带一点撞击。发力主要来自前臂向前上方的小幅送出，配合手腕轻提，方向为前+上。整体感觉是“抢点把球提走”，而不是原地等球再抡拍。\n\n**②正手快点/快拨过渡：**如果来球速度快、自己上步后没有足够空间做完整挑拉，可以用更紧凑的快点方式处理。站位贴近球台，身体前倾但动作更收，肘部在身体前方保持稳定支点。拍型前倾约15°–25°，引拍幅度很小。击球时机在高点前后的一瞬间，越早越稳。击球点在身体右前方。触球在球的中部偏上，以撞击为主、轻摩擦为辅。发力主要来自前臂快速前送，手腕只做很小的前压控制，重心略向前跟进。发力方向为正前方略带上。整体目标不是一板打死，而是借来球速度把球快速送到对方反手或中路，让对方第三板不舒服。短上旋接发强调“快和长”的质量，处理短了或慢了都容易被对方下一板先上手。\n\n**③摆短控制：**这类球可以摆短，但难度比“慢短弱上旋”更高，因为来球更急，更容易一碰就弹长。站位必须非常靠近球台，上半身探入台内，手先到位再触球。拍型接近垂直或略前倾，不要后仰。击球时机要放在上升后期，尽量早碰，不能等球冲出来。击球点在身体前方近网位置。触球以球的中下部偏前为主，用很薄的摩擦把球“吸住”。发力来自手指和手腕的细小卸力动作，方向为略向下+极轻的前送。核心不是制造旋转，而是削掉来球前冲感，让球在对方台内第二跳尽量短。若上步慢、拍型后仰或触球过厚，球很容易直接冒高或二跳出台。上旋短球能搓接或摆短，但实战里通常不是最主动的接法，需要更精细的时机和拍面控制。\n\n**④正手劈长变化：**如果判断到对方发完球后准备近台抢第三板，弱上旋的短快球也可以用控制性劈长打乱节奏。站位靠近球台，右脚先上步到位，身体略向右侧转，重心仍保持向前。拍型前倾约25°–35°，不要像处理下旋那样把拍面打开太多。击球时机在高点期或略早，击球点在身体右前方。触球以球的中上部偏中间为主，用摩擦带一点撞击，把球快速送长。发力由前臂前送为主，手腕轻微外展或前送辅助，方向为前+侧前，可优先送对方反手底线或中路深处。整体感觉是“带长”而不是“砍长”，目的是利用速度和落点压住对方，而不是强行发力。劈长本身是接发中的常见变化手段，质量关键就在于足够快、足够长。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示正手位处理短快弱上旋发球的快挑动作，重点表现上步抢点、拍面略前倾、前上方小动作发力",
        "乒乓球战术示意图，展示正手短快上旋接发后的三种落点选择：反手底线、中路深处、近网短控制"
    ],
}

# 上旋 + 短 + 正手 + 快 + 强
_topspin_short_forehand_fast_strong_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="forehand",
    speed="fast",
    strength="strong",
)

RECEIVE_CATALOG[_topspin_short_forehand_fast_strong_key] = {
    "key": _topspin_short_forehand_fast_strong_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="forehand",
        speed="fast",
        strength="strong",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "forehand",
    "speed": "fast",
    "strength": "strong",
    "title": "强上旋短球到正手的接发球应对",
    "summary": "这类球虽然落点短，但来球更急、弹跳更顶、二跳前冲感更强，最容易让人上步慢半拍或拍型稍一打开就直接冒高、出台。处理关键是先上步抢点，再把拍型压住，优先用小动作主动碰球，不要等球走出来以后再被动处理。",
    "advice": "**①正手快挑/挑打：**站位要比接慢短球更积极，判断到短球后右手持拍时右脚立即上步插入台内，身体前倾，重心压到前脚掌，手臂提前伸到台内等球。引拍不能大，拍头略低于来球，拍型前倾约30°–45°，先把上旋压住。击球时机尽量放在上升期偏早阶段，不能等球顶起来。击球点在身体右前方、贴近台面的位置。触球以球的中上部为主，以摩擦为主、带一点撞击。发力主要来自前臂向前上方的短促送出，手腕轻微上提辅助，方向为前+上。整体感觉是“抢在球顶起来之前把球提走”。\n\n**②正手快点/快拨过渡：**如果来球太急，自己虽然上到了位，但来不及做完整挑打动作，可以采用更紧凑的快点处理。站位依旧贴台，身体前倾但动作更收，肘部在身体前侧形成稳定支点。拍型前倾约20°–30°。击球时机在高点前后的一瞬间，越早越容易压住球。击球点在身体右前方。触球在球的中部偏上，以撞击为主、轻摩擦为辅。发力主要来自前臂快速前送，手腕只做小幅前压，重心轻微向前跟进，发力方向为正前方略带上。整体目标不是发死力，而是借来球速度把球快速送到对方反手或中路，让对方第三板没法舒服发力。\n\n**③正手劈长变化：**这类球可以劈长，但属于中高难度变化，不适合拍面打开后去“砍”。站位靠近球台，右脚先上步到位，身体略向右侧转但重心仍向前。拍型前倾约25°–35°，比接下旋时更压一些。击球时机在高点期或略早，不能拖晚。击球点在身体右前方。触球以球的中部到中上部为主，用摩擦带一点撞击，把球“带长”而不是“削长”。发力由前臂前送为主，手腕轻微外展或前送辅助，方向为前+侧前，可优先送对方反手底线或中路深处。整体感觉是借上旋前冲把球送到底线，质量重点是快、低、长。劈长是接短球的常见技术，特点就是高点击球、速度快、线路长，但处理上旋时拍面必须更压、更主动。\n\n**④正手兜一板控制过渡：**如果来球又急又顶，自己判断也稍慢，不适合硬挑或硬劈时，可以用一板更柔和的控制性兜接先把球安全送过去。站位同样要上步贴台，身体前倾，手先伸到位。拍型前倾约25°–35°，不要后仰。击球时机放在上升后期到高点前，击球点在身体右前方。触球在球的中上部，以薄摩擦为主，减少硬撞。发力主要来自前臂向前上方的小幅包送，手腕只做柔和配合，方向为前+微上。整体感觉是“顺着来球把球兜过去”，落点优先中路或对方反手位，先化掉对方这板短快强上旋的冲劲，再进入下一板。上旋球接发的拍面原则本身就是不能亮拍，必须竖直或下压一些，这种控制兜接本质上也是先把拍型和时机卡住。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示正手位处理短快强上旋发球的快挑动作，重点表现上步抢点、拍面前倾、前上方短促发力",
        "乒乓球战术示意图，展示正手短快强上旋接发后的三种主要落点：反手底线、中路深处、反手小三角压制"
    ],
}

# 上旋 + 短 + 中路 + 慢 + 弱
_topspin_short_middle_slow_weak_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="middle",
    speed="slow",
    strength="weak",
)

RECEIVE_CATALOG[_topspin_short_middle_slow_weak_key] = {
    "key": _topspin_short_middle_slow_weak_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="middle",
        speed="slow",
        strength="weak",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "middle",
    "speed": "slow",
    "strength": "weak",
    "title": "弱上旋短球到中路的接发球应对",
    "summary": "这类球旋转不算很强，但落点顶在身体中间，容易让人正反手选择犹豫、上步路线混乱。处理关键不是一味抢攻，而是先把脚下让位做清楚，再用小动作主动迎前，优先保证拍型前倾和击球点靠前，避免把球顶高或处理得过于被动。",
    "advice": "**①侧身正手挑打/挑拉：**判断到短中路球后，第一反应不是直接伸手，而是右手持拍时先用左脚微调、右脚小步上前并略向身体右侧让位，把击球空间腾给正手。身体前倾，重心压低，肘部自然前伸。引拍幅度要小，拍头略低于来球，拍型前倾约20°–30°。击球时机放在上升期到高点期，击球点尽量放在身体前方偏右的位置，不要等球顶到肚子前。触球在球的中上部，以摩擦为主、轻带撞击。发力主要来自前臂向前上方送出，手腕轻微上提辅助，方向为前+上。整体感觉是先让开位置，再用正手小动作把球提过去。\n\n**②反手拧/反手快拨：**如果来球更贴近中线左侧，或者自己不想侧身过大，也可以直接用反手在台内处理。站位贴近球台，双脚前后幅度不要太大，身体略微含胸收腹，把肘部放在身体前方形成稳定支点。拍型前倾约15°–25°。击球时机在上升期或高点前后，击球点放在身体前方略偏左，但不要太贴身体。触球位置以球的中上部为主，薄摩擦可以做成轻拧，厚一点则做成快拨过渡。发力主要来自前臂短促前送，手腕只做小幅内旋或前压，方向为前+微上。中路短球本来就常见“横拍台内反手拧起来、略带挑打”的处理思路，这种球的核心就是先把身体空间让出来，再用小动作主动迎前。\n\n**③摆短控制：**这一条可以写，因为是弱上旋、又是慢短球，仍然存在摆短空间，但重点是动作要细。站位非常靠近球台，上半身略探入台内，先把身体稍微侧开，避免来球顶在正中间。拍型接近垂直或略前倾，不要后仰。击球时机放在上升后期，越早越容易控短。击球点在身体前方近网位置。触球在球的中下部，用很薄的摩擦去“吸”球。发力来自手指和手腕的细微卸力，方向为略向下+轻前送。整体目标是削掉来球轻上旋的前冲感，让球第二跳尽量停短。上旋短球确实不如短下旋好摆，但在旋转较弱、速度较慢时，控制得当仍可以摆短。\n\n**④控制性劈长/晃撇长：**如果不想在中路和对手玩台内小球，也可以直接把球送长打乱对方第三板。站位靠近球台，但先通过小垫步把身体让开，不要让来球卡在肘部。拍型前倾约20°–30°，比接下旋时更压一点。击球时机在高点期或略早，击球点在身体前方。触球以球的中部到中上部为主，用摩擦带一点撞击，把球快速送到对方反手底线或中路深处。发力由前臂前送为主，手腕轻微外展或前送辅助，方向为前+侧前。中路短球本来就有“非长即短”的处理思路，而劈长、晃撇正是常见的变化手段；关键不是猛砍，而是线路够长、弧线够低。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示处理中路短弱上旋发球时先让位再用正手小挑的动作，重点表现脚下小垫步、身体侧开、拍面略前倾",
        "乒乓球战术示意图，展示中路短上旋接发后的三种线路：反手底线劈长、中路深处控制、近网摆短"
    ],
}

# 上旋 + 短 + 中路 + 慢 + 强
_topspin_short_middle_slow_strong_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="middle",
    speed="slow",
    strength="strong",
)

RECEIVE_CATALOG[_topspin_short_middle_slow_strong_key] = {
    "key": _topspin_short_middle_slow_strong_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="middle",
        speed="slow",
        strength="strong",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "middle",
    "speed": "slow",
    "strength": "strong",
    "title": "强上旋短球到中路的接发球应对",
    "summary": "这类球落点短但上旋更明显，来球容易顶到身体正前方，让人正反手选择犹豫，稍微拍面一开就容易冒高或出台。处理关键不是原地伸手够球，而是先用脚下让出击球空间，再以前倾拍型主动迎前，优先在身体前方把球处理掉。",
    "advice": "**①侧身正手挑打/挑拉：**判断到短中路强上旋后，右手持拍时先用左脚小调位、右脚向前上一步并略向身体右侧让位，把击球空间腾给正手。身体前倾，重心压低到前脚掌，肘部自然前伸。引拍不要大，拍头略低于来球，拍型前倾约30°–45°，先压住上旋。击球时机放在上升期到高点期，越早越好。击球点必须在身体前方偏右，不能等球顶到肚子前。触球在球的中上部，以摩擦为主，带一点向前的撞击。发力主要来自前臂向前上方的短促送出，手腕轻微上提辅助，方向为前+上。整体感觉是先让位，再把球主动提走。\n\n**②反手拧/反手快拨：**如果来球更贴近身体左半侧，或者自己不想大侧身，也可以直接在台内用反手处理。站位贴近球台，双脚小幅前后开立，身体略含胸收腹，把肘部放在身体前方形成支点。拍型前倾约20°–30°。击球时机在上升期或高点前后，不能拖到下降期。击球点放在身体前方略偏左，不要太贴身体。触球以球的中上部为主，薄一点做控制性拧拉，厚一点做快拨过渡。发力主要来自前臂短促前送，手腕只做小幅内旋或前压，方向为前+微上。整体目标是用更紧凑的动作把中路顶身球先处理出去，优先送对方反手或中路深处。\n\n**③控制性劈长/晃撇长：**如果判断到对方发完球后准备近台抢第三板，中路强上旋短球也可以用控制性劈长打乱节奏。站位靠近球台，但先用小垫步把身体让开，不要让来球顶在肘部。拍型前倾约25°–35°，比处理下旋时更压一些。击球时机在高点期或略早，不能晚。击球点在身体前方。触球以球的中部到中上部为主，用摩擦带一点撞击，把球快速送到对方反手底线或中路深处。发力由前臂前送为主，手腕轻微外展或前送辅助，方向为前+侧前。整体感觉是“带长”而不是“砍长”，重点是线路够长、弧线够低、让对方第三板不好直接发力。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示处理中路短强上旋发球时先让位再用正手挑打的动作，重点表现脚下小垫步、身体侧开、拍面前倾",
        "乒乓球战术示意图，展示中路短强上旋接发后的三种线路：反手底线劈长、中路深处控制、台内反手拧拨过渡"
    ],
}

# 上旋 + 短 + 中路 + 快 + 弱
_topspin_short_middle_fast_weak_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="middle",
    speed="fast",
    strength="weak",
)

RECEIVE_CATALOG[_topspin_short_middle_fast_weak_key] = {
    "key": _topspin_short_middle_fast_weak_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="middle",
        speed="fast",
        strength="weak",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "middle",
    "speed": "fast",
    "strength": "weak",
    "title": "弱上旋短球到中路的接发球应对",
    "summary": "这类球落点短但来球较急，容易顶在身体中间，让人来不及选择正反手。虽然旋转不强，但仍有前冲感，若拍型控制不好容易冒高或出台。处理关键是快速上步让位，在身体前方抢点击球，用小动作主动处理。",
    "advice": "**①侧身正手快挑：**判断到中路短球后，第一步先小垫步让位，右手持拍时右脚迅速上前并略向右侧移动，把击球空间让给正手。身体前倾，重心压低，肘部提前伸到台内。拍型前倾约20°–30°。击球时机在上升期偏早阶段，击球点放在身体前方偏右位置。触球在球的中上部，以摩擦为主、轻带撞击。发力来自前臂向前上方的小幅送出，手腕轻提，方向为前+上。整体是抢点把球提过去。\n\n**②反手快拨/小拧：**如果来球更贴身体左侧或来不及侧身，可以直接用反手处理。站位贴台，身体略含胸，肘部在身体前方。拍型前倾约15°–25°。击球在高点前后，击球点在身体前方略偏左。触球在球的中上部，薄摩擦可做小拧，厚一点做快拨。发力以前臂短促前送为主，手腕轻微内旋或前压，方向为前+微上。重点是动作紧凑，先把球处理出去。\n\n**③控制性劈长：**如果不想在中路纠缠台内球，可以直接送长打乱对方节奏。上步到位后身体稍侧开，拍型前倾约20°–30°。击球时机在高点期或略早，击球点在身体前方。触球在球的中部偏上，用摩擦带一点撞击把球送长。发力由前臂前送，手腕辅助，方向为前+侧前。落点优先对方反手底线或中路深处。整体是“带长”，不是“砍长”。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示处理中路短快弱上旋发球的正手快挑动作，重点表现上步让位、拍面略前倾、前上方发力",
        "乒乓球战术示意图，展示中路短快上旋接发后的落点选择：反手底线与中路深处压制"
    ],
}

# 上旋 + 短 + 中路 + 快 + 强
_topspin_short_middle_fast_strong_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="middle",
    speed="fast",
    strength="strong",
)

RECEIVE_CATALOG[_topspin_short_middle_fast_strong_key] = {
    "key": _topspin_short_middle_fast_strong_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="middle",
        speed="fast",
        strength="strong",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "middle",
    "speed": "fast",
    "strength": "strong",
    "title": "强上旋短球到中路的接发球应对",
    "summary": "这类球上旋强、来球急且落点顶在中路，是典型的卡身体发球。球容易向上弹和向前冲，如果拍型稍微打开就会直接冒高或出台。处理关键是快速上步让位，在身体前方抢点击球，并用前倾拍型主动压住来球。",
    "advice": "**①侧身正手快挑：**判断到中路短快球后，第一步必须先让位。右手持拍时通过小垫步让身体略向左侧腾开，右脚迅速上前插入台内，形成正手击球空间。身体前倾，重心压低到前脚掌，肘部提前伸到台内。拍型前倾约30°–45°以压住强上旋。击球时机在上升期偏早阶段，绝不能等球顶起来。击球点在身体前方偏右位置。触球在球的中上部，以摩擦为主、带少量撞击。发力来自前臂向前上方的短促送出，手腕轻微上提，方向为前+上。整体感觉是抢在球弹起前把球提走。\n\n**②反手快拨/小拧：**如果来球更贴身体左侧或来不及完全侧身，可以直接用反手台内处理。站位贴台，身体略含胸收腹，肘部在身体前方形成稳定支点。拍型前倾约20°–30°。击球时机在上升期或高点前后，必须提前。击球点在身体前方略偏左，不要让球贴身。触球在球的中上部，薄摩擦可做控制性小拧，厚一点做快拨。发力以前臂快速前送为主，手腕小幅内旋或前压，方向为前+微上。整体目标是用最小动作把球先稳定处理出去。\n\n**③控制性劈长：**当判断对方准备抢第三板时，可以直接送长打乱节奏。上步后通过小调整把身体让开，避免卡在中路。拍型前倾约25°–35°，比接下旋更压。击球时机在高点期或略早，不能拖晚。击球点在身体前方。触球在球的中部到中上部，以摩擦为主带一点撞击，把球“带长”。发力由前臂前送，手腕辅助，方向为前+侧前，优先送对方反手底线或中路深处。关键是快、低、长，而不是发力猛。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示处理中路短快强上旋发球的正手快挑动作，重点表现上步让位、拍面前倾、提前击球",
        "乒乓球战术示意图，展示中路短快强上旋接发后的落点选择：反手底线压制与中路深处控制"
    ],
}

# 上旋 + 短 + 反手 + 慢 + 弱
_topspin_short_backhand_slow_weak_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="backhand",
    speed="slow",
    strength="weak",
)

RECEIVE_CATALOG[_topspin_short_backhand_slow_weak_key] = {
    "key": _topspin_short_backhand_slow_weak_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="backhand",
        speed="slow",
        strength="weak",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "backhand",
    "speed": "slow",
    "strength": "weak",
    "title": "弱上旋短球到反手的接发球应对",
    "summary": "这类球落点短、速度不快，但带轻微前冲，容易让人误判成不转短球后把拍面打开过多。处理关键是先上步到位，在身体前方主动迎球，优先用反手台内小动作处理，不要等球顶到身前再被动去碰。",
    "advice": "**①反手拧拉/小拧：**站位贴近球台，右手持拍时右脚可小幅上步到台内，身体前倾，重心压低，肘部放在身体前方。引拍不要大，拍头略向下，手腕自然内收，拍型前倾约15°–25°。击球时机放在上升期到高点期，击球点尽量在身体左前方，不要让球进得太深。触球以球的中上部偏后为主，以摩擦为主、轻带一点撞击。发力主要来自前臂向前上方的小幅送出，配合手腕内旋，方向为前+微上。整体感觉是把球“拧起来”而不是硬挑。反手拧拉本来就是处理台内球、主动制造上旋的常见方法，而面对不转或上旋来球时，手腕动作会更偏向向前把拍子带过球顶。\n\n**②反手快拨/快挑：**如果不想做太多摩擦，也可以用更简洁的反手快拨处理。站位贴台，身体略含胸，肘部在身体前方形成稳定支点。拍型前倾约10°–20°。击球时机在高点前后，越早越容易控住弧线。击球点在身体左前方。触球以球的中部偏上为主，以撞击为主、摩擦为辅。发力主要来自前臂短促前送，手腕只做小幅前压，方向为正前方略带上。整体目标是借来球轻上旋把球快速送到对方中路或反手，不追求一板打死，先抢到主动。接上旋球常见的主流处理本来就包括挑打或快拨，这种短慢弱上旋尤其适合用紧凑动作先上手。\n\n**③摆短控制：**这一条可以保留，因为来球是弱上旋、而且速度慢，摆短仍是比较实用的主流控制手段。站位非常靠近球台，上半身略探入台内，重心低且稳定。拍型接近垂直或略前倾，不要后仰。击球时机放在上升后期，尽量早碰。击球点在身体左前方近网位置。触球以球的中下部为主，用很薄的摩擦去“吸”球。发力来自手指和手腕的细微卸力，方向为略向下+极轻前送。核心是把来球轻微前冲感卸掉，让球二跳尽量停短。短球接发里，摆短本来就是主流控制手段之一；只是面对上旋时不能单纯等球碰拍，而要主动细摩擦。\n\n**④反手撇长/劈长变化：**如果判断到对方发完球后准备在近台抢第三板，可以直接用一板反手撇长打乱节奏。站位贴近球台，右脚小幅上步，身体前倾，肘部前伸。拍型前倾约20°–30°。击球时机在高点期或略早，击球点在身体左前方。触球以球的中部到中上部为主，用摩擦带一点撞击，把球快速送长。发力由前臂前送为主，手腕轻微外展或前送辅助，方向为前+侧前，落点优先对方反手底线或中路深处。整体感觉是“带长”而不是“削长”，目的是线路突然、落点够深。接短球常见的长球变化本来就包括拨、劈长等手段，关键是出手突然、线路清晰。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示反手位处理短慢弱上旋发球的反手小拧动作，重点表现上步到位、拍面略前倾、前上方摩擦",
        "乒乓球战术示意图，展示反手短上旋接发后的三种线路：反手拧到中路、摆短到近网、撇长到对方反手底线"
    ],
}

# 上旋 + 短 + 反手 + 慢 + 强
_topspin_short_backhand_slow_strong_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="backhand",
    speed="slow",
    strength="strong",
)

RECEIVE_CATALOG[_topspin_short_backhand_slow_strong_key] = {
    "key": _topspin_short_backhand_slow_strong_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="backhand",
        speed="slow",
        strength="strong",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "backhand",
    "speed": "slow",
    "strength": "strong",
    "title": "强上旋短球到反手的接发球应对",
    "summary": "这类球虽然速度不算很急，但上旋明显，球更容易向前顶、向上弹。落点又在反手短球区域，如果拍型稍微打开，就容易直接冒高或出台。处理关键是先上步到位，在身体前方主动迎球，以前倾拍型和小动作优先把球处理出去。",
    "advice": "**①反手快挑/快拨：**站位贴近球台，右手持拍时右脚可小幅上步进台，身体前倾，重心压低，肘部放在身体前方形成稳定支点。引拍不要大，拍头略低于来球，拍型前倾约20°–30°。击球时机放在上升期到高点期，越早越容易压住强上旋。击球点在身体左前方，不要让球进得太深。触球以球的中上部为主，以撞击为主、轻带摩擦。发力主要来自前臂短促前送，手腕小幅前压，方向为正前方略带上。整体目标是先把这板球快而稳地送出去，优先落到对方中路或反手位。\n\n**②反手小拧/拧拉：**如果自己台内反手手感更好，可以用更主动的拧拉处理。站位同样贴台，身体前倾，重心放在前脚掌，肘部略向前抬起。拍型前倾约15°–25°，拍头略向下，手腕自然内收。击球时机在上升期或高点前后，击球点在身体左前方。触球以球的中上部偏后为主，以摩擦为主、轻带一点撞击。发力主要来自前臂向前上方的小幅送出，配合手腕内旋，方向为前+微上。整体感觉是顺着来球把球“拧出去”，不是硬抡拍。面对 上旋/不转 的短球，拧拉类动作通常会更强调向前越过球顶去带球，而不是像接下旋那样更多向上挑。\n\n**③反手撇长/控制性劈长：**如果判断对方发完这板强上旋短球后准备近台抢第三板，可以直接用一板长球变化打乱节奏。站位贴近球台，右脚小幅上步，身体前倾，肘部前伸。拍型前倾约20°–30°，不要像接下旋那样把拍面打开。击球时机在高点期或略早，击球点在身体左前方。触球以球的中部到中上部为主，用摩擦带一点撞击，把球快速送长。发力由前臂前送为主，手腕轻微外展或前送辅助，方向为前+侧前，落点优先对方反手底线或中路深处。整体感觉是“带长”而不是“削长”，重点是线路突然、弧线低、落点深。接短球时用劈长或长线路变化本身就是常见思路，关键在于高点击球和线路够深。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示反手位处理短慢强上旋发球的反手快挑动作，重点表现上步到位、拍面前倾、身体前倾抢点",
        "乒乓球战术示意图，展示反手短强上旋接发后的三种主流线路：反手快拨到中路、反手小拧到对方反手、撇长到反手底线"
    ],
}
# 上旋 + 短 + 反手 + 快 + 弱
_topspin_short_backhand_fast_weak_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="backhand",
    speed="fast",
    strength="weak",
)

RECEIVE_CATALOG[_topspin_short_backhand_fast_weak_key] = {
    "key": _topspin_short_backhand_fast_weak_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="backhand",
        speed="fast",
        strength="weak",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "backhand",
    "speed": "fast",
    "strength": "weak",
    "title": "弱上旋短球到反手的接发球应对",
    "summary": "这类球落点短但来球更急，虽然上旋不算很强，却容易因为速度快而让人来不及上步，最后在反手位被球顶住。处理关键不是大动作发力，而是尽快上步到位，在身体前方抢点击球，用反手台内小动作主动把球处理出去。",
    "advice": "**①反手快拨/快挑：**站位贴近球台，右手持拍时右脚小幅上步进台，身体前倾，重心压到前脚掌，肘部放在身体前方形成稳定支点。引拍不要大，拍头略低于来球，拍型前倾约15°–25°。击球时机放在上升期偏早阶段或高点前后，越早越容易借住来球速度。击球点在身体左前方，不要让球进得太深。触球以球的中部偏上为主，以撞击为主、轻带摩擦。发力主要来自前臂短促前送，手腕小幅前压，方向为正前方略带上。整体目标是用最小动作把球快而稳地送到对方中路或反手位。短球接发里，反手主动 flick 本来就是主流方案之一，尤其适合这类短而急、但旋转不算很重的球。\n\n**②反手小拧：**如果自己反手台内摩擦手感更好，可以用更主动的小拧处理。站位同样贴台，身体前倾，肘部略向前抬，手腕自然内收。拍型前倾约15°–25°，拍头略向下。击球时机放在上升期到高点期，击球点在身体左前方，尽量不要等球贴近身体。触球以球的中上部偏后为主，以薄摩擦为主、带一点向前的撞击。发力主要来自前臂向前上方的小幅送出，配合手腕内旋，方向为前+微上。整体感觉是顺着来球把球“拧出去”，不是向上硬抬。公开教学里也明确提到，对 上旋/不转 的短球，拧拉的触球会更偏向向前带过球顶。\n\n**③反手撇长/深长控制：**如果判断对方发完球后准备近台抢第三板，可以直接用一板深长变化打乱节奏。站位贴近球台，右脚小幅上步，身体前倾，肘部前伸。拍型前倾约20°–30°，不要像接下旋那样打开拍面。击球时机在高点期或略早，击球点在身体左前方。触球以球的中部到中上部为主，用摩擦带一点撞击，把球快速送长。发力由前臂前送为主，手腕轻微外展或前送辅助，方向为前+侧前，落点优先对方反手底线或中路深处。整体感觉是“带长”而不是“削长”，重点是突然、低平、够深。接发球战术里，快速深长的 push/撇长本身就是常见的变化方式，用来限制对方第三板准备。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示反手位处理短快弱上旋发球的反手快拨动作，重点表现上步到位、拍面略前倾、身体前倾抢点",
        "乒乓球战术示意图，展示反手短快上旋接发后的三种主流线路：反手快拨到中路、反手小拧到对方反手、撇长到反手底线"
    ],
}

# 上旋 + 短 + 反手 + 快 + 强
_topspin_short_backhand_fast_strong_key = build_receive_key(
    spin="topspin",
    length="short",
    placement="backhand",
    speed="fast",
    strength="strong",
)

RECEIVE_CATALOG[_topspin_short_backhand_fast_strong_key] = {
    "key": _topspin_short_backhand_fast_strong_key,
    "label": build_receive_label(
        spin="topspin",
        length="short",
        placement="backhand",
        speed="fast",
        strength="strong",
    ),
    "spin": "topspin",
    "length": "short",
    "placement": "backhand",
    "speed": "fast",
    "strength": "strong",
    "title": "强上旋短球到反手的接发球应对",
    "summary": "这类球落点短但来球更急，上旋又强，容易在反手位把人顶住。球既会向前冲，又容易向上弹，若拍型稍微打开或击球点稍晚，就容易直接冒高或出台。处理关键是尽快上步到位，在身体前方抢点击球，用前倾拍型和紧凑小动作主动把球处理出去。",
    "advice": "**①反手快挑/快拨：**站位贴近球台，右手持拍时右脚小幅上步进台，身体前倾，重心压到前脚掌，肘部放在身体前方形成稳定支点。引拍不要大，拍头略低于来球，拍型前倾约20°–30°，先把上旋压住。击球时机放在上升期偏早阶段或高点前后，不能等球走深。击球点在身体左前方。触球以球的中上部为主，以撞击为主、轻带摩擦。发力主要来自前臂短促前送，手腕小幅前压，方向为正前方略带上。整体目标是用最小动作把球快而稳地送到对方中路或反手位。\n\n**②反手小拧：**如果自己反手台内手感更好，可以用更主动的小拧来接。站位同样贴台，身体前倾，肘部略向前抬，手腕自然内收，拍型前倾约15°–25°。击球时机放在上升期到高点期，越早越容易把强上旋压住。击球点在身体左前方，不要让球贴身。触球以球的中上部偏后为主，以薄摩擦为主，带一点向前的撞击。发力主要来自前臂向前上方的小幅送出，配合手腕内旋，方向为前+微上。整体感觉是顺着来球把球“拧出去”，而不是向上硬抬。\n\n**③反手撇长/深长控制：**如果判断对方发完球后准备在近台抢第三板，可以直接用一板深长变化打乱节奏。站位贴近球台，右脚小幅上步，身体前倾，肘部前伸。拍型前倾约20°–30°，不要像接下旋那样打开拍面。击球时机在高点期或略早，击球点在身体左前方。触球以球的中部到中上部为主，用摩擦带一点撞击，把球快速送长。发力由前臂前送为主，手腕轻微外展或前送辅助，方向为前+侧前，落点优先对方反手底线或中路深处。整体感觉是“带长”而不是“削长”，重点是突然、低平、够深。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示反手位处理短快强上旋发球的反手快挑动作，重点表现上步到位、拍面前倾、身体前倾抢点",
        "乒乓球战术示意图，展示反手短快强上旋接发后的三种主流线路：反手快拨到中路、反手小拧到对方反手、撇长到反手底线"
    ],
}

# 侧上类：强侧上 + 半出台 + 反手 + 快 + 强
_side_top_half_long_backhand_fast_strong_key = build_receive_key(
    spin="side_top",
    length="half_long",
    placement="backhand",
    speed="fast",
    strength="strong",
)

RECEIVE_CATALOG[_side_top_half_long_backhand_fast_strong_key] = {
    "key": _side_top_half_long_backhand_fast_strong_key,
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
    "advice": "**①反手拧拉/拧冲：**站位贴近球台约一拳距离，右手持拍时右脚稍后，身体前倾、重心压低，肘部在身体前侧。引拍时拍头略向下，手腕放松内收，拍型前倾约30°–45°以压住上旋。击球时机在上升期到高点期，击球点位于身体左前方。触球位置在球的中上部偏侧（顺侧旋方向），以摩擦为主、轻带撞击。发力顺序为蹬地→转腰→前臂→手腕内旋，发力方向为前+右前（顺旋转），整体感觉是包住球往前带。\n\n**②反手快撕/快带：**站位比拧拉略退半步，身体前倾但更放松，肘部固定在身体前方。拍型前倾约20°–30°，引拍小而紧凑。击球在高点期，击球点在身体正前偏左。触球位置在球的中上部偏中间，以撞击为主、轻摩擦为辅。发力主要来自前臂快速前送和手腕小幅前压，身体重心略向前移动，发力方向为正前方略带顺旋转，整体是借力带出去。\n\n**③摆短控制：**站位非常靠近球台，上半身略探出台面，重心低且稳定。拍型略后仰或接近垂直（约80°–90°）以卸掉上旋。击球时机在上升后期到高点前，击球点在身体前方较近位置。触球在球的中下部偏侧，以轻摩擦为主几乎不撞击。发力来自手腕和手指的细微控制，方向为略向下+顺侧旋轻带，核心是吸住球，让球短且不出台。\n\n**④撇长变化：**站位与摆短类似但更主动，身体略侧转。拍型前倾约30°。击球在高点期或略早，击球点在身体前方偏左。触球在球的中部偏侧（顺旋转一侧），以摩擦为主带一点撞击。发力由前臂前送+手腕外展或内旋完成，方向为前+侧（可撇对方反手或中路），整体是顺着旋转把球快速撇出去，强调落点突然性。",
    "image_prompts": [
        "乒乓球接发球教学示意图，展示反手位处理强侧上半出台发球，重点表现拍面略前倾、向前上方摩擦、站位中近台",
        "乒乓球专项训练示意图，展示接反手位快速强侧上半出台发球后的推荐回球线路，优先回中路或对手反手位"
    ],
}
