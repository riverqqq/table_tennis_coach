const PROFILE_KEY = "tt_profile";
const MATCH_STATE_KEY = "tt_match_state";

function readJson(key) {
  try {
    return JSON.parse(localStorage.getItem(key) || "null");
  } catch (error) {
    console.error(`读取 ${key} 失败:`, error);
    return null;
  }
}

function hasUsefulProfile(profile) {
  if (!profile || typeof profile !== "object") return false;

  const basicFields = ["grip", "handedness", "style", "distance"];
  return basicFields.some((key) => Boolean(profile[key]));
}

function hasInProgressMatch(matchState) {
  return !!(
    matchState &&
    typeof matchState === "object" &&
    Array.isArray(matchState.games) &&
    matchState.games.length > 0 &&
    matchState.status !== "finished"
  );
}

function setStatus(text) {
  const el = document.getElementById("home-status");
  if (el) {
    el.textContent = text;
  }
}

function goToProfile() {
  window.location.href = "/profile";
}

function goToMatchSetup() {
  const profile = readJson(PROFILE_KEY);

  if (!hasUsefulProfile(profile)) {
    setStatus("还没有完整的技能包，请先填写用户信息。");
    window.location.href = "/profile";
    return;
  }

  window.location.href = "/match-setup";
}

function continueMatch() {
  const matchState = readJson(MATCH_STATE_KEY);

  if (!hasInProgressMatch(matchState)) {
    setStatus("没有可继续的比赛记录，请先开始一场新比赛。");
    return;
  }

  window.location.href = "/match";
}

function clearMatch() {
  localStorage.removeItem(MATCH_STATE_KEY);
  setStatus("已清空本地比赛记录。现在可以重新开始比赛。");
}

function initHome() {
  const profile = readJson(PROFILE_KEY);
  const matchState = readJson(MATCH_STATE_KEY);

  const goProfileBtn = document.getElementById("go-profile-btn");
  const goMatchSetupBtn = document.getElementById("go-match-setup-btn");
  const continueMatchBtn = document.getElementById("continue-match-btn");
  const clearMatchBtn = document.getElementById("clear-match-btn");

  goProfileBtn?.addEventListener("click", goToProfile);
  goMatchSetupBtn?.addEventListener("click", goToMatchSetup);
  continueMatchBtn?.addEventListener("click", continueMatch);
  clearMatchBtn?.addEventListener("click", clearMatch);

  const hasProfile = hasUsefulProfile(profile);
  const hasMatch = hasInProgressMatch(matchState);

  if (!hasProfile) {
    setStatus("当前未检测到完整技能包。建议先进入“用户信息”页面。");
    return;
  }

  if (hasMatch) {
    const currentGame = matchState.current_game ?? 1;
    const format = matchState.match_format ?? "bo3";
    setStatus(`已检测到未结束比赛：${format}，当前第 ${currentGame} 局。你可以继续比赛，或清空后重新开始。`);
    return;
  }

  setStatus("技能包已存在。可以直接点击“开始比赛”进入赛制选择。");
}

document.addEventListener("DOMContentLoaded", initHome);
