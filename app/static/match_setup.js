let configData = null;
let selectedFormat = "bo3";
let latestPlan = null;

function renderList(containerId, items) {
  const el = document.getElementById(containerId);
  if (!items || items.length === 0) {
    el.innerHTML = "<div class='desc'>暂无建议</div>";
    return;
  }
  el.innerHTML = `<ul>${items.map(x => `<li>${x}</li>`).join("")}</ul>`;
}

async function generateFirstPlan() {
  const profile = JSON.parse(localStorage.getItem("tt_profile") || "{}");

  const res = await fetch("/api/first-game-plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      profile,
      match_format: selectedFormat
    })
  });

  if (!res.ok) {
    document.getElementById("summary").textContent = "生成第一局建议失败。";
    return;
  }

  latestPlan = await res.json();
  document.getElementById("summary").textContent = latestPlan.summary;
  renderList("serve-plan", latestPlan.serve_plan);
  renderList("receive-plan", latestPlan.receive_plan);
  renderList("reminders", latestPlan.reminders);
}

async function init() {
  const res = await fetch("/api/profile-config");
  configData = await res.json();

  const chips = document.getElementById("format-chips");
  configData.match_formats.forEach(fmt => {
    const btn = document.createElement("button");
    btn.className = "chip" + (fmt.value === selectedFormat ? " active" : "");
    btn.textContent = fmt.label;
    btn.onclick = async () => {
      selectedFormat = fmt.value;
      [...chips.children].forEach(el => el.classList.remove("active"));
      btn.classList.add("active");
      await generateFirstPlan();
    };
    chips.appendChild(btn);
  });

  document.getElementById("back-btn").onclick = () => {
    window.location.href = "/profile";
  };

  document.getElementById("start-btn").onclick = () => {
    const profile = JSON.parse(localStorage.getItem("tt_profile") || "{}");

    if (!latestPlan) {
      alert("请先生成第一局建议。");
      return;
    }

    const matchState = {
      profile,
      match_format: selectedFormat,
      current_game: 1,
      games: [
        {
          game_number: 1,
          score_me: null,
          score_opponent: null,
          scoring_counts: {},
          losing_counts: {},
          opponent_traits: [],
          plan: {
            plan_type: "first_game",
            ...latestPlan
          }
        }
      ],
      match_score_me: 0,
      match_score_opponent: 0,
      status: "in_progress"
    };

    localStorage.setItem("tt_match_state", JSON.stringify(matchState));
    window.location.href = "/";
  };

  await generateFirstPlan();
}

init();
