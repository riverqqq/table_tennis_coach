const scoringTags = [
  {
    title: "发球得分",
    items: [
      { id: "S001", name: "发短下旋后对手冒高" },
      { id: "S002", name: "发不转后对手判断失误" },
      { id: "S003", name: "发急长球直接得分" },
      { id: "S004", name: "发球后对手接发冒高" },
      { id: "S005", name: "发球变化让对手不适应" }
    ]
  },
  {
    title: "接发得分",
    items: [
      { id: "S006", name: "接发球直接上手得分" },
      { id: "S007", name: "接急长球直接进攻得分" },
      { id: "S008", name: "接发控制后对手回球质量差" }
    ]
  },
  {
    title: "前三板得分",
    items: [
      { id: "S009", name: "第三板抢攻得分" },
      { id: "S010", name: "发球后连续进攻压制得分" },
      { id: "S011", name: "对手回球质量差被我抢攻得分" },
      { id: "S012", name: "前三板节奏压制得分" }
    ]
  },
  {
    title: "相持得分",
    items: [
      { id: "S013", name: "正手进攻压制得分" },
      { id: "S014", name: "反手相持压制得分" },
      { id: "S015", name: "连续进攻多板压制得分" },
      { id: "S016", name: "变线打穿对手得分" },
      { id: "S017", name: "中路或追身压制得分" }
    ]
  },
  {
    title: "利用对手弱点得分",
    items: [
      { id: "S018", name: "对手处理短球能力差而得分" },
      { id: "S019", name: "针对对手薄弱侧得分" },
      { id: "S020", name: "对手不适应旋转变化而得分" }
    ]
  }
];

const losingTags = [
  {
    title: "接发失分",
    items: [
      { id: "L001", name: "吃对手发球" },
      { id: "L002", name: "接急长球反应慢" },
      { id: "L003", name: "摆短过高" },
      { id: "L004", name: "摆短出台" },
      { id: "L005", name: "搓长质量差被抢攻" },
      { id: "L006", name: "接发冒高被打" }
    ]
  },
  {
    title: "发球轮失分",
    items: [
      { id: "L007", name: "发球被对手直接上手" },
      { id: "L008", name: "发球变化太少被适应" }
    ]
  },
  {
    title: "前三板失分",
    items: [
      { id: "L009", name: "第三板抢攻失误" },
      { id: "L010", name: "起下旋失误" },
      { id: "L011", name: "上手后衔接不好被反压" }
    ]
  },
  {
    title: "相持失分",
    items: [
      { id: "L012", name: "正手进攻失误多" },
      { id: "L013", name: "反手相持顶不住" },
      { id: "L014", name: "连续相持中主动失误" },
      { id: "L015", name: "被对手变线打穿" },
      { id: "L016", name: "被追身或中路压制" }
    ]
  },
  {
    title: "局势和针对性失分",
    items: [
      { id: "L017", name: "不适应对手节奏变化" },
      { id: "L018", name: "不适应对手旋转变化" },
      { id: "L019", name: "对手针对我方弱点连续得分" },
      { id: "L020", name: "关键分处理失误" }
    ]
  }
];

const opponentTraits = [
  { id: "O001", name: "正手强于反手" },
  { id: "O002", name: "反手强于正手" },
  { id: "O003", name: "喜欢侧身正手进攻" },
  { id: "O004", name: "喜欢反手拧/挑" },
  { id: "O005", name: "接发能力弱" },
  { id: "O006", name: "发球变化多" },
  { id: "O007", name: "发球套路单一" },
  { id: "O008", name: "近台快攻型" },
  { id: "O009", name: "相持能力强" },
  { id: "O010", name: "相持能力弱" },
  { id: "O011", name: "退台能力强" },
  { id: "O012", name: "退台后质量下降" },
  { id: "O013", name: "怕追身" },
  { id: "O014", name: "怕短球" },
  { id: "O015", name: "怕连续上旋压制" },
  { id: "O016", name: "不适应旋转变化" },
  { id: "O017", name: "节奏变化能力强" },
  { id: "O018", name: "节奏单一" },
  { id: "O019", name: "长胶打法" },
  { id: "O020", name: "削球防守型" }
];

let scoringCounts = {};
let losingCounts = {};
let selectedTraits = new Set();

const scoringGroupsEl = document.getElementById("scoring-groups");
const losingGroupsEl = document.getElementById("losing-groups");
const traitsContainerEl = document.getElementById("traits-container");
const scoringTotalEl = document.getElementById("scoring-total");
const losingTotalEl = document.getElementById("losing-total");
const traitsTotalEl = document.getElementById("traits-total");
const topScoringEl = document.getElementById("top-scoring");
const topLosingEl = document.getElementById("top-losing");
const summaryEl = document.getElementById("summary");
const mainStrategyEl = document.getElementById("main-strategy");
const riskAlertEl = document.getElementById("risk-alert");
const actionsEl = document.getElementById("actions");
const statusMessageEl = document.getElementById("status-message");
const analyzeBtn = document.getElementById("analyze-btn");
const resetBtn = document.getElementById("reset-btn");
const finishGameBtn = document.getElementById("finish-game-btn");
const myScoreInput = document.getElementById("my-score");
const opponentScoreInput = document.getElementById("opponent-score");

const matchFormatTextEl = document.getElementById("match-format-text");
const currentGameNumberEl = document.getElementById("current-game-number");
const matchScoreTextEl = document.getElementById("match-score-text");
const matchStatusBadgeEl = document.getElementById("match-status-badge");
const planPanelTitleEl = document.getElementById("plan-panel-title");
const mainLabelEl = document.getElementById("main-label");
const riskLabelEl = document.getElementById("risk-label");
const actionsLabelEl = document.getElementById("actions-label");

function emptyRoundState() {
  scoringCounts = {};
  losingCounts = {};
  selectedTraits = new Set();
}

function renderTagGroups(container, groups, type) {
  container.innerHTML = "";

  groups.forEach(group => {
    const block = document.createElement("div");
    block.className = "group-block";

    const title = document.createElement("h3");
    title.className = "group-title";
    title.textContent = group.title;
    block.appendChild(title);

    const grid = document.createElement("div");
    grid.className = "tag-grid";

    group.items.forEach(item => {
      const tagItem = document.createElement("div");
      tagItem.className = "tag-item";

      const textWrap = document.createElement("div");
      textWrap.className = "tag-text";

      const name = document.createElement("div");
      name.className = "tag-name";
      name.textContent = item.name;

      const tagId = document.createElement("div");
      tagId.className = "tag-id";
      tagId.textContent = item.id;

      textWrap.appendChild(name);
      textWrap.appendChild(tagId);

      const controls = document.createElement("div");
      controls.className = "counter-controls";

      const minusBtn = document.createElement("button");
      minusBtn.className = "counter-btn-secondary";
      minusBtn.textContent = "−";
      minusBtn.addEventListener("click", () => changeCount(type, item.id, -1));

      const value = document.createElement("div");
      value.className = "counter-value";
      value.id = `${type}-${item.id}`;
      value.textContent = "0";

      const plusBtn = document.createElement("button");
      plusBtn.className = "counter-btn";
      plusBtn.textContent = "+";
      plusBtn.addEventListener("click", () => changeCount(type, item.id, 1));

      controls.appendChild(minusBtn);
      controls.appendChild(value);
      controls.appendChild(plusBtn);

      tagItem.appendChild(textWrap);
      tagItem.appendChild(controls);
      grid.appendChild(tagItem);
    });

    block.appendChild(grid);
    container.appendChild(block);
  });
}

function renderTraits() {
  traitsContainerEl.innerHTML = "";

  opponentTraits.forEach(item => {
    const chip = document.createElement("button");
    chip.className = "trait-chip";
    chip.textContent = `${item.name} (${item.id})`;

    chip.addEventListener("click", () => {
      if (selectedTraits.has(item.id)) {
        selectedTraits.delete(item.id);
        chip.classList.remove("active");
      } else {
        selectedTraits.add(item.id);
        chip.classList.add("active");
      }
      updateTraitCount();
      syncCurrentGameInputsToStorage();
    });

    traitsContainerEl.appendChild(chip);
  });
}

function changeCount(type, id, delta) {
  const target = type === "scoring" ? scoringCounts : losingCounts;
  const current = target[id] || 0;
  const next = Math.max(0, current + delta);
  target[id] = next;

  const valueEl = document.getElementById(`${type}-${id}`);
  if (valueEl) {
    valueEl.textContent = String(next);
  }

  updateTotals();
  renderTopSummary();
  syncCurrentGameInputsToStorage();
}

function sumCounts(obj) {
  return Object.values(obj).reduce((sum, value) => sum + value, 0);
}

function updateTotals() {
  scoringTotalEl.textContent = String(sumCounts(scoringCounts));
  losingTotalEl.textContent = String(sumCounts(losingCounts));
}

function updateTraitCount() {
  traitsTotalEl.textContent = String(selectedTraits.size);
}

function getTagNameById(id) {
  const allGroups = [...scoringTags, ...losingTags];
  for (const group of allGroups) {
    for (const item of group.items) {
      if (item.id === id) return item.name;
    }
  }
  const trait = opponentTraits.find(item => item.id === id);
  return trait ? trait.name : id;
}

function getTopEntries(obj, limit = 3) {
  return Object.entries(obj)
    .filter(([, count]) => count > 0)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit);
}

function renderTopSummary() {
  const topScoring = getTopEntries(scoringCounts, 3);
  const topLosing = getTopEntries(losingCounts, 3);

  if (topScoring.length === 0) {
    topScoringEl.innerHTML = `<div class="empty-text">暂无记录</div>`;
  } else {
    topScoringEl.innerHTML = topScoring
      .map(([id, count]) => `<div>${getTagNameById(id)} × ${count}</div>`)
      .join("");
  }

  if (topLosing.length === 0) {
    topLosingEl.innerHTML = `<div class="empty-text">暂无记录</div>`;
  } else {
    topLosingEl.innerHTML = topLosing
      .map(([id, count]) => `<div>${getTagNameById(id)} × ${count}</div>`)
      .join("");
  }
}

function setStatus(message, type = "") {
  statusMessageEl.textContent = message;
  statusMessageEl.className = "status-message";
  if (type) {
    statusMessageEl.classList.add(type);
  }
}

function renderPlan(plan, gameNumber = null) {
  if (!plan) {
    summaryEl.textContent = "暂无建议。";
    mainStrategyEl.textContent = "暂无建议。";
    riskAlertEl.textContent = "暂无建议。";
    actionsEl.innerHTML = `<li class="muted">暂无建议。</li>`;
    return;
  }

  if (plan.plan_type === "first_game") {
    planPanelTitleEl.textContent = gameNumber ? `第 ${gameNumber} 局开局建议` : "第一局建议";
    mainLabelEl.textContent = "发球建议";
    riskLabelEl.textContent = "接发建议";
    actionsLabelEl.textContent = "注意事项";

    summaryEl.textContent = plan.summary || "暂无局势判断。";
    mainStrategyEl.innerHTML = (plan.serve_plan || []).map(x => `• ${x}`).join("<br>") || "暂无发球建议。";
    riskAlertEl.innerHTML = (plan.receive_plan || []).map(x => `• ${x}`).join("<br>") || "暂无接发建议。";

    const reminders = Array.isArray(plan.reminders) ? plan.reminders : [];
    if (reminders.length === 0) {
      actionsEl.innerHTML = `<li class="muted">暂无注意事项。</li>`;
    } else {
      actionsEl.innerHTML = reminders.map(x => `<li>${x}</li>`).join("");
    }
  } else {
    planPanelTitleEl.textContent = gameNumber ? `第 ${gameNumber} 局建议` : "下一局建议";
    mainLabelEl.textContent = "主战术";
    riskLabelEl.textContent = "风险提醒";
    actionsLabelEl.textContent = "执行方案";

    summaryEl.textContent = plan.summary || "暂无局势判断。";
    mainStrategyEl.textContent = plan.main_strategy || "暂无主战术。";
    riskAlertEl.textContent = plan.risk_alert || "暂无风险提醒。";

    const actions = Array.isArray(plan.actions) ? plan.actions : [];
    if (actions.length === 0) {
      actionsEl.innerHTML = `<li class="muted">暂无执行方案。</li>`;
    } else {
      actionsEl.innerHTML = actions.map(action => `<li>${action}</li>`).join("");
    }
  }
}

function renderMatchInfo() {
  const state = getMatchState();
  if (!state) return;

  matchFormatTextEl.textContent = getFormatLabel(state.match_format);
  currentGameNumberEl.textContent = String(state.current_game);
  matchScoreTextEl.textContent = `${state.match_score_me} : ${state.match_score_opponent}`;

  if (state.status === "finished") {
    matchStatusBadgeEl.textContent = "比赛已结束";
    matchStatusBadgeEl.className = "badge danger";
  } else {
    matchStatusBadgeEl.textContent = "比赛进行中";
    matchStatusBadgeEl.className = "badge success";
  }
}

function loadCurrentGameIntoUI() {
  const state = getMatchState();
  if (!state) {
    setStatus("未找到比赛状态，请先从技能包页进入比赛流程。", "error");
    return;
  }

  const currentGame = getCurrentGame(state);
  if (!currentGame) {
    setStatus("未找到当前局数据。", "error");
    return;
  }

  emptyRoundState();
  scoringCounts = { ...(currentGame.scoring_counts || {}) };
  losingCounts = { ...(currentGame.losing_counts || {}) };
  selectedTraits = new Set(currentGame.opponent_traits || []);

  updateCounterValuesInDOM();
  updateTotals();
  updateTraitCount();
  renderTopSummary();
  applyTraitSelectionToDOM();
  renderPlan(currentGame.plan, currentGame.game_number);
  renderMatchInfo();

  myScoreInput.value = currentGame.score_me ?? "";
  opponentScoreInput.value = currentGame.score_opponent ?? "";
}

function updateCounterValuesInDOM() {
  document.querySelectorAll(".counter-value").forEach(el => {
    el.textContent = "0";
  });

  Object.entries(scoringCounts).forEach(([id, count]) => {
    const el = document.getElementById(`scoring-${id}`);
    if (el) el.textContent = String(count);
  });

  Object.entries(losingCounts).forEach(([id, count]) => {
    const el = document.getElementById(`losing-${id}`);
    if (el) el.textContent = String(count);
  });
}

function applyTraitSelectionToDOM() {
  document.querySelectorAll(".trait-chip").forEach(el => {
    el.classList.remove("active");
  });

  document.querySelectorAll(".trait-chip").forEach(el => {
    const text = el.textContent;
    const match = text.match(/\((O\d+)\)$/);
    if (match && selectedTraits.has(match[1])) {
      el.classList.add("active");
    }
  });
}

function syncCurrentGameInputsToStorage() {
  const state = getMatchState();
  if (!state) return;

  persistCurrentGameInputs(state, scoringCounts, losingCounts, selectedTraits);
  saveMatchState(state);
}

async function fetchTacticalPlan() {
  const response = await fetch("/api/tactical-plan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      scoring_counts: scoringCounts,
      losing_counts: losingCounts,
      opponent_traits: Array.from(selectedTraits)
    })
  });

  if (!response.ok) {
    throw new Error(`请求失败：${response.status}`);
  }

  const data = await response.json();
  return {
    plan_type: "tactical",
    ...data
  };
}

async function generatePlan() {
  const scoringTotal = sumCounts(scoringCounts);
  const losingTotal = sumCounts(losingCounts);

  if (scoringTotal === 0 && losingTotal === 0) {
    setStatus("请至少记录一个得分或失分事件，再开始布置战术。", "error");
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "分析中...";
  setStatus("正在生成下一局建议...", "");

  try {
    syncCurrentGameInputsToStorage();

    const nextPlan = await fetchTacticalPlan();
    const state = getMatchState();
    const currentGame = getCurrentGame(state);

    if (currentGame) {
      currentGame.generated_next_plan = nextPlan;
      saveMatchState(state);
    }

    renderPlan(nextPlan, state ? state.current_game + 1 : null);
    setStatus("下一局建议预览已更新。打完本局后可直接进入下一局。", "success");
  } catch (error) {
    console.error(error);
    setStatus(`生成失败：${error.message}`, "error");
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "开始布置战术";
  }
}

function resetCurrentRoundOnly() {
  emptyRoundState();
  updateCounterValuesInDOM();
  updateTotals();
  updateTraitCount();
  renderTopSummary();
  applyTraitSelectionToDOM();
  myScoreInput.value = "";
  opponentScoreInput.value = "";

  const state = getMatchState();
  if (state) {
    persistCurrentGameInputs(state, scoringCounts, losingCounts, selectedTraits);
    saveMatchState(state);
  }

  setStatus("本局记录已清空。", "success");
}

async function finishCurrentGame() {
  const myScore = Number(myScoreInput.value);
  const opponentScore = Number(opponentScoreInput.value);

  if (Number.isNaN(myScore) || Number.isNaN(opponentScore)) {
    setStatus("请先填写本局比分。", "error");
    return;
  }

  if (myScore === opponentScore) {
    setStatus("比分不能相同，请输入有效的比赛结果。", "error");
    return;
  }

  const state = getMatchState();
  if (!state) {
    setStatus("未找到比赛状态，请重新从开始比赛进入。", "error");
    return;
  }

  syncCurrentGameInputsToStorage();
  recordCurrentGameScore(state, myScore, opponentScore);

  if (isMatchFinished(state)) {
    state.status = "finished";
    saveMatchState(state);
    window.location.href = "/match-summary";
    return;
  }

  let nextPlan = null;
  const currentGame = getCurrentGame(state);

  if (currentGame && currentGame.generated_next_plan) {
    nextPlan = currentGame.generated_next_plan;
  } else {
    try {
      nextPlan = await fetchTacticalPlan();
    } catch (error) {
      console.error(error);
      setStatus(`生成下一局建议失败：${error.message}`, "error");
      return;
    }
  }

  createNextGame(state, nextPlan);
  saveMatchState(state);

  emptyRoundState();
  updateCounterValuesInDOM();
  updateTotals();
  updateTraitCount();
  renderTopSummary();
  applyTraitSelectionToDOM();

  myScoreInput.value = "";
  opponentScoreInput.value = "";

  loadCurrentGameIntoUI();
  setStatus(`已进入第 ${state.current_game} 局。`, "success");
}

function init() {
  renderTagGroups(scoringGroupsEl, scoringTags, "scoring");
  renderTagGroups(losingGroupsEl, losingTags, "losing");
  renderTraits();

  updateTotals();
  updateTraitCount();
  renderTopSummary();

  analyzeBtn.addEventListener("click", generatePlan);
  resetBtn.addEventListener("click", resetCurrentRoundOnly);
  finishGameBtn.addEventListener("click", finishCurrentGame);

  loadCurrentGameIntoUI();
}

init();
