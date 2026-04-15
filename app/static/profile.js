let profileConfig = null;

const profileState = {
  grip: "shakehand",
  handedness: "right",
  style: "attack",
  distance: "mid_close",
  forehand_rubber: "sticky",
  backhand_rubber: "inverted",
  blade_feel: "neutral",
  serve_skills: {},
  receive_skills: {},
  attack_skills: {},
  control_skills: {}
};

function setStatus(msg) {
  document.getElementById("status").textContent = msg;
}

function createChoiceField(container, label, key, options) {
  const field = document.createElement("div");
  field.className = "field";

  const title = document.createElement("div");
  title.className = "field-label";
  title.textContent = label;

  const chips = document.createElement("div");
  chips.className = "chips";

  options.forEach(opt => {
    const btn = document.createElement("button");
    btn.className = "chip" + (profileState[key] === opt.value ? " active" : "");
    btn.textContent = opt.label;
    btn.onclick = () => {
      profileState[key] = opt.value;
      [...chips.children].forEach(el => el.classList.remove("active"));
      btn.classList.add("active");
    };
    chips.appendChild(btn);
  });

  field.appendChild(title);
  field.appendChild(chips);
  container.appendChild(field);
}

function createSkillSection(containerId, titleText, configKey, stateKey) {
  const container = document.getElementById(containerId);
  container.innerHTML = `<h2>${titleText}</h2><p class="desc">请按 0–5 分选择，0 表示不会，5 表示核心武器。</p>`;

  profileConfig[configKey].forEach(skill => {
    const row = document.createElement("div");
    row.className = "skill-row";

    const label = document.createElement("div");
    label.textContent = skill.label;

    const rateGroup = document.createElement("div");
    rateGroup.className = "rate-group";

    for (let i = 0; i <= 5; i++) {
      const btn = document.createElement("button");
      btn.className = "rate-btn" + ((profileState[stateKey][skill.key] ?? 0) === i ? " active" : "");
      btn.textContent = String(i);
      btn.onclick = () => {
        profileState[stateKey][skill.key] = i;
        [...rateGroup.children].forEach(el => el.classList.remove("active"));
        btn.classList.add("active");
      };
      rateGroup.appendChild(btn);
    }

    row.appendChild(label);
    row.appendChild(rateGroup);
    container.appendChild(row);
  });
}

function renderBasic() {
  const basic = document.getElementById("basic-section");
  basic.innerHTML = "<h2>基础打法信息</h2>";
  createChoiceField(basic, "握拍", "grip", profileConfig.basic.grip);
  createChoiceField(basic, "惯用手", "handedness", profileConfig.basic.handedness);
  createChoiceField(basic, "风格", "style", profileConfig.basic.style);
  createChoiceField(basic, "常用站位", "distance", profileConfig.basic.distance);
}

function renderEquipment() {
  const section = document.getElementById("equipment-section");
  section.innerHTML = "<h2>器材信息</h2>";
  createChoiceField(section, "正手胶皮", "forehand_rubber", profileConfig.equipment.forehand_rubber);
  createChoiceField(section, "反手胶皮", "backhand_rubber", profileConfig.equipment.backhand_rubber);
  createChoiceField(section, "底板倾向", "blade_feel", profileConfig.equipment.blade_feel);
}

async function saveProfile(goNext = false) {
  const res = await fetch("/api/profile", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(profileState)
  });

  if (!res.ok) {
    setStatus("保存失败。");
    return;
  }

  localStorage.setItem("tt_profile", JSON.stringify(profileState));
  setStatus("技能包已保存。");

  if (goNext) {
    window.location.href = "/match-setup";
  }
}

async function init() {
  const res = await fetch("/api/profile-config");
  profileConfig = await res.json();

  const saved = localStorage.getItem("tt_profile");
  if (saved) {
    Object.assign(profileState, JSON.parse(saved));
  }

  renderBasic();
  renderEquipment();
  createSkillSection("serve-section", "发球技能", "serve_skills", "serve_skills");
  createSkillSection("receive-section", "接发技能", "receive_skills", "receive_skills");
  createSkillSection("attack-section", "进攻能力", "attack_skills", "attack_skills");
  createSkillSection("control-section", "控制能力", "control_skills", "control_skills");

  document.getElementById("save-btn").onclick = () => saveProfile(false);
  document.getElementById("save-start-btn").onclick = () => saveProfile(true);
}

init();
