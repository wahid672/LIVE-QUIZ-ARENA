const $ = (id) => document.getElementById(id);
let questions = [];
let socket = null;
let reconnectTimer = null;
let liveSnapshot = null;
let musicSnapshot = null;
let musicQueueRenderKey = null;
let musicPlaylistLastMessage = "";

async function api(path, method = "GET", body = undefined) {
  const options = { method, headers: { "Content-Type": "application/json" } };
  if (body !== undefined) options.body = JSON.stringify(body);
  const response = await fetch(path, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    let msg = data.detail;
    if (Array.isArray(msg)) {
      msg = msg.map((item) => item.msg || JSON.stringify(item)).join("; ");
    } else if (typeof msg === "object" && msg !== null) {
      msg = JSON.stringify(msg);
    }
    throw new Error(msg || `HTTP ${response.status}`);
  }
  return data;
}

function setNotice(message, type = "") {
  const node = $("controlNotice");
  node.textContent = message;
  node.className = `alert mt-3 mb-0 py-2 ${type === "error" ? "alert-danger" : "alert-info"}`;
}

function setSimResult(message, type = "") {
  $("simResult").textContent = message;
  $("simResult").className = `sim-result mt-3 ${type}`;
}

function connectSocket() {
  if (socket && [WebSocket.OPEN, WebSocket.CONNECTING].includes(socket.readyState)) return;
  const protocol = location.protocol === "https:" ? "wss" : "ws";
  socket = new WebSocket(`${protocol}://${location.host}/ws`);
  socket.onopen = () => {
    $("connectionDot").classList.add("online");
    $("connectionText").textContent = "Server connected";
  };
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "game_state") {
      renderState(message.data);
      if (message.live) renderLiveState(message.live);
      if (message.connection) renderTikTokConnection(message.connection);
      if (message.music) renderMusicState(message.music);
    }
  };
  socket.onclose = () => {
    $("connectionDot").classList.remove("online");
    $("connectionText").textContent = "Reconnecting";
    clearTimeout(reconnectTimer);
    reconnectTimer = setTimeout(connectSocket, 1800);
  };
  socket.onerror = () => socket.close();
}

function updateManualQuestionOptions(preferredQuestionId = null) {
  const category = $("manualCategory").value || "all";
  const filtered = category === "all"
    ? questions
    : questions.filter((question) => question.category === category);

  const select = $("manualQuestion");
  select.replaceChildren();
  filtered.forEach((question) => {
    const option = document.createElement("option");
    option.value = question.id;
    option.textContent = `${question.id} — ${question.question}`;
    select.appendChild(option);
  });

  if (preferredQuestionId && filtered.some((question) => question.id === preferredQuestionId)) {
    select.value = preferredQuestionId;
  }
}

async function loadQuestions() {
  questions = await api("/api/questions");
  const categorySelect = $("manualCategory");
  categorySelect.replaceChildren();

  const allOption = document.createElement("option");
  allOption.value = "all";
  allOption.textContent = "All subjects";
  categorySelect.appendChild(allOption);

  [...new Set(questions.map((question) => question.category))]
    .sort((a, b) => a.localeCompare(b, "id"))
    .forEach((category) => {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = `${category} (${questions.filter((q) => q.category === category).length})`;
      categorySelect.appendChild(option);
    });

  categorySelect.value = [...categorySelect.options].some((option) => option.value === "Matematika")
    ? "Matematika"
    : "all";
  updateManualQuestionOptions();
  updateModeUI();
}

$("manualCategory").addEventListener("change", () => {
  updateManualQuestionOptions();
});


function renderTikTokConnection(connection) {
  const status = connection?.status || "disconnected";
  const badge = $("tiktokStatusBadge");
  badge.textContent = status.replaceAll("_", " ").toUpperCase();
  badge.className = `badge ${status === "connected" ? "bg-green-lt" : status === "error" ? "bg-red-lt" : status === "connecting" ? "bg-yellow-lt" : "bg-secondary-lt"}`;
  $("tiktokConnectButton").disabled = ["connecting", "connected", "disconnecting"].includes(status);
  $("tiktokDisconnectButton").disabled = !["connecting", "connected", "disconnecting"].includes(status);

  const notice = $("tiktokConnectionNotice");
  if (status === "connected") {
    notice.className = "alert alert-success mt-3 mb-3 py-2";
    notice.textContent = `Connected to @${connection.username || "creator"}${connection.room_id ? ` · Room ${connection.room_id}` : ""}. LIVE events are being processed.`;
  } else if (status === "connecting") {
    notice.className = "alert alert-warning mt-3 mb-3 py-2";
    notice.textContent = `Connecting to @${connection.username || "creator"}… TikTok must currently be LIVE and publicly accessible.`;
  } else if (status === "error" || status === "dependency_missing") {
    notice.className = "alert alert-danger mt-3 mb-3 py-2";
    notice.textContent = connection.last_error || "TikTok LIVE connection failed.";
  } else if (status === "disconnecting") {
    notice.className = "alert alert-warning mt-3 mb-3 py-2";
    notice.textContent = "Disconnecting from TikTok LIVE…";
  } else {
    notice.className = "alert alert-secondary mt-3 mb-3 py-2";
    notice.textContent = "TikTok LIVE is disconnected. You can still test all interactions using the simulator.";
  }
}

function renderLiveState(live) {
  if (!live) return;
  liveSnapshot = live;
  $("liveLikesTotal").textContent = Number(live.likes_total || 0).toLocaleString("id-ID");
  $("liveFollowCount").textContent = Number(live.follow_bonus_count || 0).toLocaleString("id-ID");
  $("liveGiftDiamonds").textContent = Number(live.gift_total_diamonds || 0).toLocaleString("id-ID");
  const target = Math.max(1, Number(live.likes_per_reward || 100));
  const energy = Math.max(0, Number(live.like_energy || 0));
  $("liveEnergyLabel").textContent = `${energy} / ${target} likes`;
  $("liveEnergyBar").style.width = `${Math.min(100, energy / target * 100)}%`;

  const events = $("liveEventList");
  events.replaceChildren();
  if (!live.recent_events?.length) {
    const empty = document.createElement("div");
    empty.className = "text-secondary text-center py-4 small";
    empty.textContent = "No LIVE events received yet.";
    events.appendChild(empty);
  } else {
    const icons = { comment: "ti-message-circle", like: "ti-heart", follow: "ti-user-plus", gift: "ti-gift", system: "ti-bolt" };
    live.recent_events.slice(0, 12).forEach((item) => {
      const row = document.createElement("div");
      row.className = "live-event-row";
      const icon = document.createElement("div");
      icon.className = `live-event-icon ${item.type}`;
      const glyph = document.createElement("i");
      glyph.className = `ti ${icons[item.type] || "ti-activity"}`;
      icon.appendChild(glyph);
      const main = document.createElement("div");
      main.className = "live-event-main";
      const name = document.createElement("strong");
      name.textContent = item.username || "Viewer";
      const detail = document.createElement("span");
      detail.textContent = item.detail || item.type;
      main.append(name, detail);
      const time = document.createElement("div");
      time.className = "live-event-time";
      time.textContent = new Date(item.timestamp * 1000).toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      row.append(icon, main, time);
      events.appendChild(row);
    });
  }

  const supporters = $("giftSupporterList");
  supporters.replaceChildren();
  if (!live.gift_leaderboard?.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 3;
    td.className = "text-secondary text-center py-4";
    td.textContent = "No gifts received yet.";
    tr.appendChild(td);
    supporters.appendChild(tr);
  } else {
    live.gift_leaderboard.forEach((item) => {
      const tr = document.createElement("tr");
      const rank = document.createElement("td");
      rank.textContent = String(item.rank).padStart(2, "0");
      const name = document.createElement("td");
      const strong = document.createElement("strong");
      strong.textContent = item.username;
      const small = document.createElement("div");
      small.className = "text-secondary small";
      small.textContent = `${item.gift_count} gifts`;
      name.append(strong, small);
      const diamonds = document.createElement("td");
      diamonds.className = "text-end fw-bold";
      diamonds.textContent = Number(item.diamonds).toLocaleString("id-ID");
      tr.append(rank, name, diamonds);
      supporters.appendChild(tr);
    });
  }
}

function updateEventSimulatorFields() {
  const selected = $("eventSimType").value;
  document.querySelectorAll(".event-sim-field").forEach((field) => {
    field.classList.toggle("hidden", field.dataset.event !== selected);
  });
}


function renderMusicState(state) {
  if (!state) return;
  musicSnapshot = state;
  const queue = state.queue || [];
  const current = state.current_track;

  $("musicTrackCount").textContent = `${queue.length} track${queue.length === 1 ? "" : "s"}`;
  $("musicNowPlaying").textContent = current
    ? `${current.title}${state.is_playing ? " · PLAYING" : " · PAUSED"}`
    : "Nothing is playing";

  if (!musicPlaylistLastMessage) {
    $("musicPlaylistStatus").textContent = queue.length
      ? `Playlist ready · ${state.current_index + 1} of ${queue.length}${state.loop ? " · Loop enabled" : ""}`
      : "No music playlist loaded.";
  }

  $("musicPlayButton").disabled = queue.length === 0 || state.is_playing;
  $("musicPauseButton").disabled = !state.is_playing;
  $("musicPreviousButton").disabled = queue.length === 0;
  $("musicNextButton").disabled = queue.length === 0;
  $("musicLoopSwitch").checked = Boolean(state.loop);

  if (document.activeElement !== $("musicVolume")) {
    $("musicVolume").value = String(state.volume ?? 65);
  }
  $("musicVolumeValue").textContent = `${state.volume ?? 65}%`;

  const container = $("musicQueue");
  const renderKey = JSON.stringify({
    keys: queue.map((track) => track.track_key),
    index: state.current_index,
    playing: state.is_playing,
    volume: state.volume,
    loop: state.loop,
  });

  if (renderKey === musicQueueRenderKey) return;
  musicQueueRenderKey = renderKey;

  container.replaceChildren();
  if (!queue.length) {
    const empty = document.createElement("div");
    empty.className = "text-secondary small text-center py-3";
    empty.textContent = "Tambahkan tautan URL audio (.mp3, .wav, .mov) ke playlist.";
    container.appendChild(empty);
    return;
  }

  queue.forEach((track, index) => {
    const row = document.createElement("div");
    row.className = `music-queue-row${index === state.current_index ? " active" : ""}`;

    const number = document.createElement("div");
    number.className = "music-queue-index";
    number.textContent = String(index + 1).padStart(2, "0");

    const info = document.createElement("div");
    info.className = "min-w-0";
    const title = document.createElement("div");
    title.className = "music-queue-title";
    title.textContent = track.title || track.url || "Audio track";
    const kind = document.createElement("div");
    kind.className = "music-queue-kind";
    kind.textContent = track.kind ? `${track.kind.toUpperCase()} file` : "Audio stream";
    info.append(title, kind);

    const select = document.createElement("button");
    select.type = "button";
    select.className = "btn btn-sm btn-outline-primary";
    select.innerHTML = index === state.current_index && state.is_playing
      ? '<i class="ti ti-volume"></i>'
      : '<i class="ti ti-player-play"></i>';
    select.title = "Play this track";
    select.addEventListener("click", async () => {
      musicPlaylistLastMessage = `Playing: ${track.title}`;
      $("musicPlaylistStatus").textContent = musicPlaylistLastMessage;
      await controlMusic("select", { track_key: track.track_key });
    });

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "btn btn-sm btn-outline-danger";
    remove.innerHTML = '<i class="ti ti-trash"></i>';
    remove.title = "Remove from playlist";
    remove.addEventListener("click", async () => {
      try {
        const result = await api("/api/music/playlist/remove", "POST", { track_key: track.track_key });
        musicPlaylistLastMessage = `Removed: ${track.title}`;
        $("musicPlaylistStatus").textContent = musicPlaylistLastMessage;
        renderMusicState(result);
      } catch (error) {
        musicPlaylistLastMessage = error.message;
        $("musicPlaylistStatus").textContent = musicPlaylistLastMessage;
      }
    });

    row.append(number, info, select, remove);
    container.appendChild(row);
  });
}

async function controlMusic(action, extra = {}) {
  try {
    const result = await api("/api/music/control", "POST", { action, ...extra });
    if (action === "play") musicPlaylistLastMessage = "Music playback started.";
    if (action === "pause") musicPlaylistLastMessage = "Music playback paused.";
    if (action === "next") musicPlaylistLastMessage = "Skipped to next track.";
    if (action === "previous") musicPlaylistLastMessage = "Returned to previous track.";
    if (action === "volume") musicPlaylistLastMessage = `Volume set to ${extra.volume}%`;
    if (action === "loop") musicPlaylistLastMessage = extra.loop ? "Playlist loop enabled." : "Playlist loop disabled.";
    $("musicPlaylistStatus").textContent = musicPlaylistLastMessage;
    renderMusicState(result);
  } catch (error) {
    musicPlaylistLastMessage = error.message;
    $("musicPlaylistStatus").textContent = musicPlaylistLastMessage;
  }
}

function updateModeUI() {
  const manual = $("questionMode").value === "manual";
  $("manualQuestionWrap").classList.toggle("hidden", !manual);
  $("modeBadge").textContent = manual ? "MANUAL MODE" : "RANDOM MODE";
  $("autoPlayHint").textContent = manual
    ? "After the starting question, Auto Play follows the question bank order."
    : "After revealing the answer, the next unused random question starts automatically.";
}

function renderLeaderboard(rows) {
  const container = $("leaderboard");
  container.replaceChildren();
  if (!rows || rows.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 3;
    td.className = "text-secondary text-center py-4";
    td.textContent = "No players yet. Waiting for answers.";
    tr.appendChild(td);
    container.appendChild(tr);
    return;
  }

  rows.slice(0, 8).forEach((player) => {
    const tr = document.createElement("tr");
    const rankCell = document.createElement("td");
    const rank = document.createElement("span");
    rank.className = "player-rank";
    rank.textContent = String(player.rank).padStart(2, "0");
    rankCell.appendChild(rank);

    const playerCell = document.createElement("td");
    const name = document.createElement("div");
    name.className = "player-name";
    name.textContent = player.username;
    const meta = document.createElement("div");
    meta.className = "player-meta";
    meta.textContent = `${player.correct_answers} correct · streak ${player.streak}`;
    playerCell.append(name, meta);

    const scoreCell = document.createElement("td");
    scoreCell.className = "text-end";
    const score = document.createElement("span");
    score.className = "player-score";
    score.textContent = Number(player.score).toLocaleString("id-ID");
    scoreCell.appendChild(score);

    tr.append(rankCell, playerCell, scoreCell);
    container.appendChild(tr);
  });
}

function renderOptions(question, phase) {
  const grid = $("optionGrid");
  grid.replaceChildren();
  const options = question?.options || { A: "Option A", B: "Option B", C: "Option C", D: "Option D" };
  Object.entries(options).forEach(([letter, text]) => {
    const col = document.createElement("div");
    col.className = "col-sm-6";
    const option = document.createElement("div");
    option.className = "answer-option";
    if (["reveal", "finished"].includes(phase) && question?.correct_answer === letter) {
      option.classList.add("correct");
    }
    const key = document.createElement("b");
    key.textContent = letter;
    const label = document.createElement("span");
    label.textContent = text;
    option.append(key, label);
    col.appendChild(option);
    grid.appendChild(col);
  });
}

function renderState(state) {
  const phase = state.phase || "idle";
  const upperPhase = phase.toUpperCase();

  $("statPhase").textContent = upperPhase;
  $("phaseTag").textContent = upperPhase;
  $("statQuestion").textContent = state.endless
    ? `${state.question_number || 0} / ∞`
    : `${state.question_number || 0} / ${state.question_count || 0}`;
  $("statPlayers").textContent = state.players_count ?? 0;
  $("statAnswers").textContent = state.answered_count ?? 0;

  const active = phase === "question";
  const paused = phase === "paused";
  const reveal = phase === "reveal";
  const waitingGift = phase === "waiting_gift";
  const autoPlay = Boolean(state.auto_play);
  const duration = Math.max(1, Number(state.answer_duration || 15));
  const remaining = Math.max(0, Number(state.remaining_seconds || 0));
  const advanceDelay = Math.max(1, Number(state.auto_advance_delay || 4));
  const advanceRemaining = Math.max(0, Number(state.auto_advance_remaining_seconds || 0));

  let timerValue = "—";
  let timerUnit = "SECONDS";
  let timerCaption = "Waiting for game";
  let progress = 0;

  if (waitingGift) {
    const wg = state.waiting_gift || {};
    timerValue = `${wg.collected ?? 0}/${wg.target ?? 0}`;
    timerUnit = "GIFT";
    timerCaption = wg.reached
      ? "Target gift tercapai! Memulai ronde baru..."
      : `Menunggu gift penonton (${wg.remaining ?? 0} diamonds lagi untuk lanjut)`;
    progress = wg.progress_percent ?? 0;
  } else if (active || paused) {
    timerValue = String(Math.ceil(remaining));
    timerCaption = active ? "Answer window is open" : "Game paused";
    progress = Math.min(100, (remaining / duration) * 100);
  } else if (reveal && autoPlay) {
    timerValue = String(Math.ceil(advanceRemaining));
    timerUnit = "NEXT";
    timerCaption = `Next question starts in ${Math.ceil(advanceRemaining)} seconds`;
    progress = Math.min(100, (advanceRemaining / advanceDelay) * 100);
  } else if (reveal) {
    timerCaption = "Round completed · waiting for manual next";
  } else if (phase === "finished") {
    timerCaption = "Session completed";
  }

  $("timerValue").textContent = timerValue;
  $("timerUnit").textContent = timerUnit;
  $("timerCaption").textContent = timerCaption;
  $("timerRing").style.background = `conic-gradient(#5bd4cb ${progress}%, #263448 ${progress}%)`;
  $("timerProgress").style.width = `${progress}%`;
  $("timerPercent").textContent = `${Math.round(progress)}%`;

  const q = state.current_question;
  if (q) {
    $("questionCategory").textContent = q.category || "GENERAL";
    $("questionNumber").textContent = `QUESTION ${String(state.question_number).padStart(2, "0")}`;
    $("questionText").textContent = q.question;
    renderOptions(q, phase);
    const explanation = $("answerExplanation");
    if (q.correct_answer) {
      explanation.classList.remove("hidden");
      explanation.textContent = `Correct answer: ${q.correct_answer}. ${q.explanation || ""}`;
    } else {
      explanation.classList.add("hidden");
      explanation.textContent = "";
    }
  } else {
    $("questionCategory").textContent = "NO CATEGORY";
    $("questionNumber").textContent = "QUESTION 00";
    $("questionText").textContent = waitingGift
      ? `Target ${state.question_count || 100} soal selesai! Kirim gift untuk memulai ronde berikutnya.`
      : "No active question.";
    renderOptions(null, phase);
    $("answerExplanation").classList.add("hidden");
  }

  $("startButton").disabled = !["idle", "finished"].includes(phase);
  $("pauseButton").disabled = !active;
  $("resumeButton").disabled = !paused;
  $("nextButton").disabled = !reveal;
  $("endButton").disabled = phase === "idle";
  $("simulateButton").disabled = !active;

  const continueBtn = $("continueButton");
  if (continueBtn) {
    continueBtn.classList.toggle("hidden", !waitingGift);
    continueBtn.disabled = !waitingGift;
  }

  if (!["idle", "finished"].includes(phase)) {
    $("autoPlaySwitch").checked = autoPlay;
    $("autoAdvanceDelay").value = String(state.auto_advance_delay || 4);
    $("questionMode").value = state.mode || "random";
    updateModeUI();
  }
  $("modeBadge").textContent = `${(state.mode || "random").toUpperCase()} MODE${autoPlay ? " · AUTO PLAY" : ""}${state.endless ? " · ENDLESS" : ""}`;
  renderLeaderboard(state.leaderboard || []);
}

$("questionMode").addEventListener("change", updateModeUI);
$("autoPlaySwitch").addEventListener("change", () => {
  if ($("autoPlaySwitch").checked) {
    setNotice("Auto Play will advance after the answer reveal delay when this session starts.");
  }
});

const endlessSwitch = $("endlessModeSwitch");
if (endlessSwitch) {
  endlessSwitch.addEventListener("change", () => {
    const isEndless = endlessSwitch.checked;
    $("questionCount").disabled = isEndless;
    const hint = $("questionCountHint");
    if (hint) {
      hint.textContent = isEndless
        ? "Mode tanpa henti aktif: kuis akan terus berjalan tanpa batas soal hingga distop manual."
        : "Jumlah soal per sesi (misal 100, 200). Aktifkan switch untuk tanpa henti.";
    }
  });
}

$("startButton").addEventListener("click", async () => {
  try {
    const mode = $("questionMode").value;
    const endless = Boolean($("endlessModeSwitch")?.checked);
    const countVal = Number($("questionCount").value || 10);
    const payload = {
      mode,
      endless,
      question_count: endless ? 0 : countVal,
      answer_duration: Number($("answerDuration").value),
      auto_play: $("autoPlaySwitch").checked,
      auto_advance_delay: Number($("autoAdvanceDelay").value),
      gift_target_to_continue: Number($("giftTargetInput")?.value || 5),
    };
    if (mode === "manual") payload.question_id = $("manualQuestion").value;
    await api("/api/game/start", "POST", payload);
    const countText = endless ? "Mode Tanpa Henti (Endless)" : `${payload.question_count} soal`;
    const autoText = payload.auto_play ? ` Auto Play aktif; jeda pindah soal ${payload.auto_advance_delay} detik.` : " Auto Play nonaktif.";
    const giftText = payload.gift_target_to_continue > 0 ? ` Target gift lanjut: ${payload.gift_target_to_continue} diamonds.` : "";
    setNotice(`Quiz started (${countText}).${autoText}${giftText}`);
  } catch (error) {
    setNotice(error.message, "error");
  }
});

const continueBtn = $("continueButton");
if (continueBtn) {
  continueBtn.addEventListener("click", async () => {
    try {
      await api("/api/game/continue-round", "POST", {});
      setNotice("Ronde berikutnya berhasil dimulai secara manual.");
    } catch (error) {
      setNotice(error.message, "error");
    }
  });
}

$("pauseButton").addEventListener("click", async () => {
  try { await api("/api/game/pause", "POST", {}); setNotice("Game paused."); }
  catch (error) { setNotice(error.message, "error"); }
});

$("resumeButton").addEventListener("click", async () => {
  try { await api("/api/game/resume", "POST", {}); setNotice("Game resumed."); }
  catch (error) { setNotice(error.message, "error"); }
});

$("nextButton").addEventListener("click", async () => {
  try {
    const mode = $("questionMode").value;
    const payload = { mode };
    if (mode === "manual") payload.question_id = $("manualQuestion").value;
    await api("/api/game/next", "POST", payload);
    setNotice("Next question started manually.");
  } catch (error) { setNotice(error.message, "error"); }
});

$("endButton").addEventListener("click", async () => {
  try { await api("/api/game/end", "POST", {}); setNotice("Game ended."); }
  catch (error) { setNotice(error.message, "error"); }
});

$("simulatorForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const result = await api("/api/game/answer", "POST", {
      username: $("simUsername").value.trim(),
      user_id: $("simUserId").value.trim() || null,
      answer: $("simAnswer").value,
    });
    if (result.accepted) {
      setSimResult(`${result.username}: ${result.answer} · ${result.is_correct ? "CORRECT" : "INCORRECT"} · +${result.points_awarded} points`, "success");
    } else {
      setSimResult(result.message || result.reason, "error");
    }
  } catch (error) {
    setSimResult(error.message, "error");
  }
});


$("tiktokConnectForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    renderTikTokConnection({ status: "connecting", username: $("tiktokUsername").value.trim() });
    const connection = await api("/api/tiktok/connect", "POST", { username: $("tiktokUsername").value.trim() });
    renderTikTokConnection(connection);
  } catch (error) {
    renderTikTokConnection({ status: "error", last_error: error.message });
  }
});

$("tiktokDisconnectButton").addEventListener("click", async () => {
  try {
    const connection = await api("/api/tiktok/disconnect", "POST", {});
    renderTikTokConnection(connection);
  } catch (error) {
    renderTikTokConnection({ status: "error", last_error: error.message });
  }
});

$("eventSimType").addEventListener("change", updateEventSimulatorFields);

$("liveEventSimulatorForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const eventType = $("eventSimType").value;
  const payload = {
    event_type: eventType,
    username: $("eventSimUsername").value.trim(),
    user_id: $("eventSimUserId").value.trim() || null,
  };
  if (eventType === "comment") payload.comment = $("eventSimComment").value;
  if (eventType === "like") payload.like_count = Number($("eventSimLikeCount").value);
  if (eventType === "gift") {
    payload.gift_name = $("eventSimGiftName").value.trim();
    payload.diamonds = Number($("eventSimDiamonds").value);
    payload.quantity = Number($("eventSimQuantity").value);
  }
  try {
    const result = await api("/api/tiktok/test-event", "POST", payload);
    const resultNode = $("liveEventSimResult");
    resultNode.className = "sim-result mt-3 " + (result.accepted ? "success" : "error");
    resultNode.textContent = result.accepted
      ? `${eventType.toUpperCase()} test event processed successfully.`
      : `Event not applied: ${result.message || result.reason || "not accepted"}`;
  } catch (error) {
    $("liveEventSimResult").textContent = error.message;
  }
});


$("musicPlaylistForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const raw = $("youtubeLinks").value || "";
  const urls = raw
    .split(/\r?\n|,/)
    .map((value) => value.trim())
    .filter(Boolean);

  if (!urls.length) {
    musicPlaylistLastMessage = "Masukkan minimal satu URL file audio (.mp3, .wav, .mov).";
    $("musicPlaylistStatus").textContent = musicPlaylistLastMessage;
    return;
  }

  $("musicAddButton").disabled = true;
  try {
    const result = await api("/api/music/playlist/add", "POST", { urls });
    renderMusicState(result);
    const invalidCount = result.invalid?.length || 0;
    const addedCount = result.added_count || 0;
    if (addedCount) {
      musicPlaylistLastMessage = `${addedCount} audio berhasil ditambahkan ke playlist.`;
      $("youtubeLinks").value = "";
    } else if (invalidCount) {
      musicPlaylistLastMessage = `Tidak ada audio yang ditambahkan. ${result.invalid.map((item) => item.error).join("; ")}`;
    } else {
      musicPlaylistLastMessage = "Tidak ada audio baru. URL mungkin sudah ada di playlist.";
    }
    if (invalidCount && addedCount) {
      musicPlaylistLastMessage += ` ${invalidCount} dilewati: ${result.invalid.map((item) => item.error).join("; ")}`;
    }
    $("musicPlaylistStatus").textContent = musicPlaylistLastMessage;
  } catch (error) {
    musicPlaylistLastMessage = error.message;
    $("musicPlaylistStatus").textContent = musicPlaylistLastMessage;
  } finally {
    $("musicAddButton").disabled = false;
  }
});

$("musicPlayButton").addEventListener("click", () => controlMusic("play"));
$("musicPauseButton").addEventListener("click", () => controlMusic("pause"));
$("musicPreviousButton").addEventListener("click", () => controlMusic("previous"));
$("musicNextButton").addEventListener("click", () => controlMusic("next"));
$("musicLoopSwitch").addEventListener("change", () => controlMusic("loop", { loop: $("musicLoopSwitch").checked }));
$("musicVolume").addEventListener("change", () => controlMusic("volume", { volume: Number($("musicVolume").value) }));

(async function init() {
  try {
    await loadQuestions();
    setNotice("Question bank loaded. Configure the session and start when ready.");
  } catch (error) {
    setNotice(`Could not load question bank: ${error.message}`, "error");
  }
  connectSocket();
  updateEventSimulatorFields();
  try {
    renderMusicState(await api("/api/music/state"));
  } catch (error) {
    $("musicPlaylistStatus").textContent = `Could not load music playlist: ${error.message}`;
  }
  try {
    const liveStatus = await api("/api/tiktok/status");
    renderTikTokConnection(liveStatus.connection);
    renderLiveState(liveStatus.interactions);
  } catch (error) {
    renderTikTokConnection({ status: "error", last_error: error.message });
  }
  try {
    renderState(await api("/api/game/state"));
  } catch (error) {
    setNotice(error.message, "error");
  }
})();
