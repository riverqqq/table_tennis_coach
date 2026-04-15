const MATCH_STATE_KEY = "tt_match_state";

function getMatchState() {
  try {
    return JSON.parse(localStorage.getItem(MATCH_STATE_KEY) || "null");
  } catch (error) {
    console.error("读取比赛状态失败：", error);
    return null;
  }
}

function saveMatchState(state) {
  localStorage.setItem(MATCH_STATE_KEY, JSON.stringify(state));
}

function clearMatchState() {
  localStorage.removeItem(MATCH_STATE_KEY);
}

function getNeededWins(matchFormat) {
  const map = {
    bo1: 1,
    bo3: 2,
    bo5: 3,
    bo7: 4
  };
  return map[matchFormat] || 2;
}

function getFormatLabel(matchFormat) {
  const map = {
    bo1: "一局一胜",
    bo3: "三局两胜",
    bo5: "五局三胜",
    bo7: "七局四胜"
  };
  return map[matchFormat] || "三局两胜";
}

function getCurrentGame(state) {
  if (!state || !Array.isArray(state.games)) return null;
  return state.games.find(game => game.game_number === state.current_game) || null;
}

function persistCurrentGameInputs(state, scoringCounts, losingCounts, selectedTraits) {
  const currentGame = getCurrentGame(state);
  if (!currentGame) return;

  currentGame.scoring_counts = { ...scoringCounts };
  currentGame.losing_counts = { ...losingCounts };
  currentGame.opponent_traits = Array.from(selectedTraits);
}

function recordCurrentGameScore(state, myScore, opponentScore) {
  const currentGame = getCurrentGame(state);
  if (!currentGame) return;

  currentGame.score_me = myScore;
  currentGame.score_opponent = opponentScore;

  if (myScore > opponentScore) {
    state.match_score_me += 1;
  } else if (opponentScore > myScore) {
    state.match_score_opponent += 1;
  }
}

function isMatchFinished(state) {
  const neededWins = getNeededWins(state.match_format);
  return (
    state.match_score_me >= neededWins ||
    state.match_score_opponent >= neededWins
  );
}

function createNextGame(state, nextPlan) {
  const nextGameNumber = state.current_game + 1;

  const nextGame = {
    game_number: nextGameNumber,
    score_me: null,
    score_opponent: null,
    scoring_counts: {},
    losing_counts: {},
    opponent_traits: [],
    plan: nextPlan
  };

  state.games.push(nextGame);
  state.current_game = nextGameNumber;
}

function resetRoundInputs() {
  return {
    scoring_counts: {},
    losing_counts: {},
    opponent_traits: []
  };
}
