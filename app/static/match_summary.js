function getTagNameByIdFromSummary(id) {
  const allGroups = [
    {
      items: [
        { id: "S001", name: "发短下旋后对手冒高" },
        { id: "S002", name: "发不转后对手判断失误" },
        { id: "S003", name: "发急长球直接得分" },
        { id: "S004", name: "发球后对手接发冒高" },
        { id: "S005", name: "发球变化让对手不适应" },
        { id: "S006", name: "接发球直接上手得分" },
        { id: "S007", name: "接急长球直接进攻得分" },
        { id: "S008", name: "接发控制后对手回球质量差" },
        { id: "S009", name: "第三板抢攻得分" },
        { id: "S010", name: "发球后连续进攻压制得分" },
        { id: "S011", name: "对手回球质量差被我抢攻得分" },
        { id: "S012", name: "前三板节奏压制得分" },
        { id: "S013", name: "正手进攻压制得分" },
        { id: "S014", name: "反手相持压制得分" },
        { id: "S015", name: "连续进攻多板压制得分" },
        { id: "S016", name: "变线打穿对手得分" },
        { id: "S017", name: "中路或追身压制得分" },
        { id: "S018", name: "对手处理短球能力差而得分" },
        { id: "S019", name: "针对对手薄弱侧得分" },
        { id: "S020", name: "对手不适应旋转变化而得分" }
      ]
    },
    {
      items: [
        { id: "L001", name: "吃对手发球" },
        { id: "L002", name: "接急长球反应慢" },
        { id: "L003", name: "摆短过高" },
        { id: "L004", name: "摆短出台" },
        { id: "L005", name: "搓长质量差被抢攻" },
        { id: "L006", name: "接发冒高被打" },
        { id: "L007", name: "发球被对手直接上手" },
        { id: "L008", name: "发球变化太少被适应" },
        { id: "L009", name: "第三板抢攻失误" },
        { id: "L010", name: "起下旋失误" },
        { id: "L011", name: "上手后衔接不好被反压" },
        { id: "L012", name: "正手进攻失误多" },
        { id: "L013", name: "反手相持顶不住" },
        { id: "L014", name: "连续相持中主动失误" },
        { id: "L015", name: "被对手变线打穿" },
        { id: "L016", name: "被追身或中路压制" },
        { id: "L017", name: "不适应对手节奏变化" },
        { id: "L018", name: "不适应对手旋转变化" },
        { id: "L019", name: "对手针对我方弱点连续得分" },
        { id: "L020", name: "关键分处理失误" }
      ]
    }
  ];

  const traits = [
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

  for (const group of allGroups) {
    for (const item of group.items) {
      if (item.id === id) return item.name;
    }
  }

  const trait = traits.find((x) => x.id === id);
  return trait ? trait.name : id;
}

function mergeCountsFromGames(games, key) {
  const result = {};
  games.forEach((game) => {
    const counts = game[key] || {};
    Object.entries(counts).forEach(([id, count]) => {
      result[id] = (result[id] || 0) + count;
    });
  });
  return result;
}

function collectTraitCounts(games) {
  const result = {};
  games.forEach((game) => {
    const traits = game.opponent_traits || [];
    traits.forEach((id) => {
      result[id] = (result[id] || 0) + 1;
    });
  });
  return result;
}

function getTopEntries(obj, limit = 5) {
  return Object.entries(obj)
    .filter(([, count]) => count > 0)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit);
}

async function loadSummary() {
  const state = getMatchState();

  if (!state || !Array.isArray(state.games) || state.games.length === 0) {
    document.getElementById("final-result").textContent = "未找到比赛记录。";
    document.getElementById("overall-summary").textContent = "请先完成一场比赛。";
    return;
  }

  const res = await fetch("/api/match-summary", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(state)
  });

  if (!res.ok) {
    document.getElementById("final-result").textContent = "生成赛后总结失败。";
    document.getElementById("overall-summary").textContent = "请稍后重试。";
    return;
  }

  const summary = await res.json();

  document.getElementById("final-result").textContent = summary.final_result;
  document.getElementById("overall-summary").textContent = summary.overall_summary;

  const gameListEl = document.getElementById("game-list");
  gameListEl.innerHTML = state.games
    .map((game) => {
      const myScore = game.score_me ?? "-";
      const opponentScore = game.score_opponent ?? "-";
      return `<div>第 ${game.game_number} 局：我方 ${myScore} - ${opponentScore} 对手</div>`;
    })
    .join("");

  const scoringCounts = mergeCountsFromGames(state.games, "scoring_counts");
  const losingCounts = mergeCountsFromGames(state.games, "losing_counts");
  const traitCounts = collectTraitCounts(state.games);

  const topScoring = getTopEntries(scoringCounts, 5);
  const topLosing = getTopEntries(losingCounts, 5);
  const topTraits = getTopEntries(traitCounts, 5);

  document.getElementById("top-scoring-summary").innerHTML =
    topScoring.length === 0
      ? "<div class='muted'>暂无明显高频得分点</div>"
      : topScoring.map(([id, count]) => `<div>${getTagNameByIdFromSummary(id)} × ${count}</div>`).join("");

  document.getElementById("top-losing-summary").innerHTML =
    topLosing.length === 0
      ? "<div class='muted'>暂无明显高频失分点</div>"
      : topLosing.map(([id, count]) => `<div>${getTagNameByIdFromSummary(id)} × ${count}</div>`).join("");

  document.getElementById("opponent-traits-summary").innerHTML =
    topTraits.length === 0
      ? "本场未记录明显对手特征。"
      : topTraits.map(([id, count]) => `${getTagNameByIdFromSummary(id)}（出现 ${count} 局）`).join("；");

  const trainingEl = document.getElementById("training-actions");
  const actions = Array.isArray(summary.training_actions) ? summary.training_actions : [];
  trainingEl.innerHTML =
    actions.length === 0
      ? "<li class='muted'>暂无训练建议</li>"
      : actions.map((x) => `<li>${x}</li>`).join("");

  document.getElementById("back-home-btn").onclick = () => {
    window.location.href = "/home";
  };

  document.getElementById("restart-btn").onclick = () => {
    clearMatchState();
    window.location.href = "/match-setup";
  };
}

document.addEventListener("DOMContentLoaded", loadSummary);
