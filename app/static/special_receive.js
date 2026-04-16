const receiveQueryState = {
  spin: "unknown",
  length: "unknown",
  placement: "unknown",
  speed: "unknown",
  strength: "unknown"
};

const receiveOptions = {
  spin: [
    { value: "unknown", label: "未知" },
    { value: "topspin", label: "上旋" },
    { value: "backspin", label: "下旋" },
    { value: "sidespin_clockwise", label: "侧旋（顺时针）" },
    { value: "reverse_clockwise", label: "逆旋（逆时针）" },
    { value: "side_top", label: "侧上" },
    { value: "side_bottom", label: "侧下" },
    { value: "reverse_top", label: "逆上" },
    { value: "reverse_bottom", label: "逆下" },
    { value: "no_spin", label: "不转" }
  ],
  length: [
    { value: "unknown", label: "未知" },
    { value: "short", label: "短" },
    { value: "half_long", label: "半出台" },
    { value: "long", label: "长" }
  ],
  placement: [
    { value: "unknown", label: "未知" },
    { value: "forehand", label: "正手" },
    { value: "middle", label: "中路" },
    { value: "backhand", label: "反手" }
  ],
  speed: [
    { value: "unknown", label: "未知" },
    { value: "slow", label: "慢" },
    { value: "fast", label: "快" }
  ],
  strength: [
    { value: "unknown", label: "未知" },
    { value: "weak", label: "弱" },
    { value: "strong", label: "强" }
  ]
};

const labelMaps = {
  spin: Object.fromEntries(receiveOptions.spin.map(item => [item.value, item.label])),
  length: Object.fromEntries(receiveOptions.length.map(item => [item.value, item.label])),
  placement: Object.fromEntries(receiveOptions.placement.map(item => [item.value, item.label])),
  speed: Object.fromEntries(receiveOptions.speed.map(item => [item.value, item.label])),
  strength: Object.fromEntries(receiveOptions.strength.map(item => [item.value, item.label]))
};

function setQueryHint(text) {
  const el = document.getElementById("query-hint");
  if (el) {
    el.textContent = text;
  }
}

function renderChoiceGroup(containerId, fieldKey, options) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "";

  options.forEach((option) => {
    const btn = document.createElement("button");
    btn.className = "chip" + (receiveQueryState[fieldKey] === option.value ? " active" : "");
    btn.textContent = option.label;
    btn.onclick = () => {
      receiveQueryState[fieldKey] = option.value;
      renderAllGroups();
      updateStrengthVisibility();
      updateLiveHint();
    };
    container.appendChild(btn);
  });
}

function renderAllGroups() {
  renderChoiceGroup("spin-chips", "spin", receiveOptions.spin);
  renderChoiceGroup("length-chips", "length", receiveOptions.length);
  renderChoiceGroup("placement-chips", "placement", receiveOptions.placement);
  renderChoiceGroup("speed-chips", "speed", receiveOptions.speed);
  renderChoiceGroup("strength-chips", "strength", receiveOptions.strength);
}

function updateStrengthVisibility() {
  const strengthField = document.getElementById("strength-field");
  if (!strengthField) return;

  if (receiveQueryState.spin === "no_spin") {
    strengthField.style.opacity = "0.55";
    strengthField.style.pointerEvents = "none";
    receiveQueryState.strength = "unknown";
  } else {
    strengthField.style.opacity = "1";
    strengthField.style.pointerEvents = "auto";
  }
}

function countKnownConditions() {
  let known = 0;

  if (receiveQueryState.spin !== "unknown") known += 1;
  if (receiveQueryState.length !== "unknown") known += 1;
  if (receiveQueryState.placement !== "unknown") known += 1;
  if (receiveQueryState.speed !== "unknown") known += 1;

  if (receiveQueryState.spin !== "no_spin" && receiveQueryState.strength !== "unknown") {
    known += 1;
  }

  return known;
}

function hasUnknownCondition() {
  if (receiveQueryState.spin === "unknown") return true;
  if (receiveQueryState.length === "unknown") return true;
  if (receiveQueryState.placement === "unknown") return true;
  if (receiveQueryState.speed === "unknown") return true;

  if (receiveQueryState.spin !== "no_spin" && receiveQueryState.strength === "unknown") {
    return true;
  }

  return false;
}

function buildCurrentConditionTextFromState() {
  const parts = [];

  parts.push(`旋转：${labelMaps.spin[receiveQueryState.spin]}`);
  parts.push(`长短：${labelMaps.length[receiveQueryState.length]}`);
  parts.push(`落点：${labelMaps.placement[receiveQueryState.placement]}`);
  parts.push(`速度：${labelMaps.speed[receiveQueryState.speed]}`);

  if (receiveQueryState.spin === "no_spin") {
    parts.push("强弱：不适用");
  } else {
    parts.push(`强弱：${labelMaps.strength[receiveQueryState.strength]}`);
  }

  return parts.join(" / ");
}

function buildCurrentConditionTextFromQuery(query) {
  const parts = [];

  parts.push(`旋转：${labelMaps.spin[query.spin]}`);
  parts.push(`长短：${labelMaps.length[query.length]}`);
  parts.push(`落点：${labelMaps.placement[query.placement]}`);
  parts.push(`速度：${labelMaps.speed[query.speed]}`);

  if (query.spin === "no_spin") {
    parts.push("强弱：不适用");
  } else {
    parts.push(`强弱：${labelMaps.strength[query.strength]}`);
  }

  return parts.join(" / ");
}

function updateLiveHint() {
  const knownCount = countKnownConditions();

  if (knownCount < 3) {
    setQueryHint(`当前已知条件 ${knownCount} 项。请至少明确 3 项条件后再查询。`);
    return;
  }

  if (hasUnknownCondition()) {
    setQueryHint(`当前已知条件 ${knownCount} 项。存在“未知”，查询时将返回所有符合已知条件的候选球种。`);
    return;
  }

  setQueryHint(`当前已知条件 ${knownCount} 项。没有“未知”，查询时将返回一个明确球种的专门应对方法。`);
}

function renderInsufficientResult(message) {
  const container = document.getElementById("result-container");
  if (!container) return;

  container.innerHTML = `
    <div class="result-card">
      <h3>条件不足</h3>
      <p>${message}</p>
    </div>
  `;
}

function renderSingleResult(detail, query) {
  const container = document.getElementById("result-container");
  if (!container) return;

  if (!detail) {
    container.innerHTML = `
      <div class="result-card">
        <h3>未找到结果</h3>
        <p>当前组合暂未找到对应球种内容，请检查数据是否完整。</p>
      </div>
    `;
    return;
  }

  const imageHtml = Array.isArray(detail.image_prompts) && detail.image_prompts.length > 0
    ? detail.image_prompts.map((prompt, index) => `
        <div class="placeholder-box">示意图 ${index + 1}：${prompt}</div>
      `).join("")
    : `<div class="placeholder-box">这里后续可放 1–2 张 AI 生成示意图</div>`;

  container.innerHTML = `
    <div class="result-card">
      <h3>球种标签</h3>
      <p>${detail.label}</p>
    </div>

    <div class="result-card">
      <h3>标题</h3>
      <p>${detail.title}</p>
    </div>

    <div class="result-card">
      <h3>当前查询条件</h3>
      <p>${buildCurrentConditionTextFromQuery(query)}</p>
    </div>

    <div class="result-card">
      <h3>处理概览</h3>
      <p>${detail.summary}</p>
    </div>

    <div class="result-card">
      <h3>专门应对方法</h3>
      <p>${detail.advice}</p>
      ${imageHtml}
    </div>
  `;
}

function renderMultipleResults(candidates, query, message) {
  const container = document.getElementById("result-container");
  if (!container) return;

  const listHtml = candidates.length === 0
    ? `
      <div class="result-item">
        <div class="result-item-title">暂无候选球种</div>
        <div class="result-item-desc">
          当前条件下未匹配到候选组合，请检查数据是否完整。
        </div>
      </div>
    `
    : candidates.map((item, index) => {
        return `
          <div class="result-item clickable" data-candidate-index="${index}">
            <div class="result-item-title">${item.label}</div>
            <div class="result-item-desc">
              键值：${item.key}<br />
              点击查看这个候选球种的详细专项应对内容。
            </div>
          </div>
        `;
      }).join("");

  container.innerHTML = `
    <div class="result-card">
      <h3>候选球种列表</h3>
      <p>${message}</p>
    </div>

    <div class="result-card">
      <h3>当前查询条件</h3>
      <p>${buildCurrentConditionTextFromQuery(query)}</p>
    </div>

    <div class="result-list">
      ${listHtml}
    </div>
  `;

  const clickableItems = container.querySelectorAll("[data-candidate-index]");
  clickableItems.forEach((el) => {
    el.addEventListener("click", async () => {
      const index = Number(el.getAttribute("data-candidate-index"));
      const item = candidates[index];
      if (!item) return;
      await handleCandidateClick(item);
    });
  });
}

async function fetchReceiveQuery(payload = receiveQueryState) {
  const response = await fetch("/api/special-receive-query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`请求失败：${response.status}`);
  }

  return await response.json();
}

async function handleCandidateClick(item) {
  const preciseQuery = {
    spin: item.spin,
    length: item.length,
    placement: item.placement,
    speed: item.speed,
    strength: item.spin === "no_spin" ? "unknown" : (item.strength || "unknown")
  };

  setQueryHint(`正在载入「${item.label}」的详细内容...`);

  try {
    const data = await fetchReceiveQuery(preciseQuery);

    if (data.mode === "single") {
      renderSingleResult(data.detail, data.query);
      setQueryHint(`已打开「${item.label}」的详细专项应对内容。`);
      return;
    }

    renderInsufficientResult("未能载入该候选球种的详情。");
    setQueryHint("未能载入该候选球种的详情。");
  } catch (error) {
    console.error(error);
    renderInsufficientResult(`载入候选详情失败：${error.message}`);
    setQueryHint(`载入候选详情失败：${error.message}`);
  }
}

async function handleQuery() {
  const knownCount = countKnownConditions();

  if (knownCount < 3) {
    const message = `当前已知条件只有 ${knownCount} 项。请至少明确 3 项条件后再查询。`;
    renderInsufficientResult(message);
    setQueryHint(message);
    return;
  }

  setQueryHint("正在查询专项应对结果...");

  try {
    const data = await fetchReceiveQuery();

    if (data.mode === "insufficient") {
      renderInsufficientResult(data.message);
      setQueryHint(data.message);
      return;
    }

    if (data.mode === "single") {
      renderSingleResult(data.detail, data.query);
      setQueryHint(data.message);
      return;
    }

    if (data.mode === "multiple") {
      renderMultipleResults(data.candidates || [], data.query, data.message);
      setQueryHint(data.message);
      return;
    }

    renderInsufficientResult("返回结果格式无法识别。");
    setQueryHint("返回结果格式无法识别。");
  } catch (error) {
    console.error(error);
    renderInsufficientResult(`查询失败：${error.message}`);
    setQueryHint(`查询失败：${error.message}`);
  }
}

function resetQuery() {
  receiveQueryState.spin = "unknown";
  receiveQueryState.length = "unknown";
  receiveQueryState.placement = "unknown";
  receiveQueryState.speed = "unknown";
  receiveQueryState.strength = "unknown";

  renderAllGroups();
  updateStrengthVisibility();
  updateLiveHint();

  const container = document.getElementById("result-container");
  if (container) {
    container.innerHTML = `
      <div class="placeholder-box">
        暂未查询结果。<br />
        当前已经接入后端查询接口，后续你只需要逐步补全 306 种球种的详细内容。
      </div>
    `;
  }
}

function initSpecialReceivePage() {
  renderAllGroups();
  updateStrengthVisibility();
  updateLiveHint();

  const queryBtn = document.getElementById("query-btn");
  const resetBtn = document.getElementById("reset-btn");
  const backBtn = document.getElementById("back-btn");

  queryBtn?.addEventListener("click", handleQuery);
  resetBtn?.addEventListener("click", resetQuery);
  backBtn?.addEventListener("click", () => {
    window.location.href = "/special-playbook";
  });
}

document.addEventListener("DOMContentLoaded", initSpecialReceivePage);
