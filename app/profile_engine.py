from __future__ import annotations

from .profile_models import FirstGamePlanResponse, PlayerProfile


def _top_skill(skill_map: dict[str, int]) -> list[str]:
    return [k for k, v in skill_map.items() if v >= 4]


def build_first_game_plan(profile: PlayerProfile, match_format: str) -> FirstGamePlanResponse:
    serve_strong = _top_skill(profile.serve_skills)
    receive_strong = _top_skill(profile.receive_skills)
    attack_strong = _top_skill(profile.attack_skills)
    control_strong = _top_skill(profile.control_skills)

    serve_plan: list[str] = []
    receive_plan: list[str] = []
    reminders: list[str] = []

    # 发球建议
    if "short_backspin" in serve_strong:
        serve_plan.append("第一局先以短下旋发球试探对手短球处理和摆短质量。")
    if "long_fast" in serve_strong:
        serve_plan.append("每个发球轮可加入1次急长发球，优先打反手或追身位，观察对手反应。")
    if "short_nospin" in serve_strong:
        serve_plan.append("在短下旋基础上夹入短不转，测试对手对旋转变化的判断。")
    if "sidespin_hook" in serve_strong:
        serve_plan.append("如果侧旋/勾手较熟练，可作为变化球使用，但第一局不要过度暴露全部发球套路。")

    if not serve_plan:
        serve_plan.append("第一局发球先以最稳的两种发球为主，优先保证质量，再观察对手适应情况。")

    # 接发建议
    if "short_touch" in receive_strong:
        receive_plan.append("接短球优先稳摆短，先看对手会不会摆高或处理不稳。")
    if "long_push" in receive_strong:
        receive_plan.append("遇到不适合上手的发球，优先劈长到反手或中路，先求质量。")
    if "attack_long_serve" in receive_strong:
        receive_plan.append("对手发急长时，有机会可直接上手，但第一局仍以稳定性优先。")
    if "banana" in receive_strong or "flip" in receive_strong:
        receive_plan.append("如果对短球上手有把握，可少量试一次，判断对手对接发变化的应对。")

    if not receive_plan:
        receive_plan.append("第一局接发先默认准备快长球，短球先求上台率和落点质量，不急于抢攻。")

    # 注意事项
    reminders.append("第一局目标不是完全摊牌，而是先收集信息：对手怕短球、追身、中路还是连续上旋。")
    reminders.append("前几分重点观察对手接发质量、发球旋转、习惯落点和相持偏好。")

    if "fh_open_backspin" in attack_strong:
        reminders.append("若发现对手搓长质量一般，可在后半局逐步增加正手起下旋的使用。")
    if "bh_rally" not in attack_strong:
        reminders.append("如果反手相持不是强项，第一局尽量不要过早进入反手对反手长相持。")
    if "body_target" in control_strong:
        reminders.append("中路和追身位可作为试探落点，观察对手让位和衔接能力。")
    if profile.style == "control":
        reminders.append("你偏控制型，第一局更适合通过落点和节奏变化先建立稳定性。")
    if profile.style == "attack":
        reminders.append("你偏进攻型，第一局可以主动争前三板，但不要用不熟练手段硬上。")

    summary = "第一局建议以“稳中带试探”为主：先用你最熟练的发球和接发方案观察对手，再逐步放大优势。"

    return FirstGamePlanResponse(
        serve_plan=serve_plan[:3],
        receive_plan=receive_plan[:3],
        reminders=reminders[:4],
        summary=summary,
    )
