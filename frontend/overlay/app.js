const $ = (id) => document.getElementById(id);

let socket = null;
let reconnectTimer = null;
let audioContext = null;
let lastSpokenQuestionId = null;
let lastBeepKey = null;
let lastGiftAlertId = null;
let centerPopupTimer = null;
let activeRoundKey = null;
let lastFastestPopupKey = null;
let lastSummaryPopupKey = null;
let characterAnimationEnabled = true;

// ============================================================
// AUDIO ENGINE (WEB AUDIO API SYNTHESIZER SFX)
// ============================================================

// Overlay berjalan tanpa interaksi langsung (display-only untuk OBS / TikTok Studio).
// Audio diinisialisasi otomatis dan dikontrol penuh dari Dashboard.
function getAudioContext() {
  if (!audioContext) {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (AudioCtx) {
      try {
        audioContext = new AudioCtx();
      } catch (_) {}
    }
  }
  if (audioContext && audioContext.state === "suspended") {
    audioContext.resume().catch(() => {});
  }
  return audioContext;
}

// Handler cadangan pasif bila dibuka di tab browser biasa yang menahan audio
function resumeAudioOnGesture() {
  if (audioContext && audioContext.state === "suspended") {
    audioContext.resume().catch(() => {});
  }
  if (audioPlayer && musicState?.is_playing && audioPlayer.paused) {
    audioPlayer.play().catch(() => {});
  }
  if ('speechSynthesis' in window && window.speechSynthesis.paused) {
    window.speechSynthesis.resume();
  }
}
document.addEventListener("pointerdown", resumeAudioOnGesture, { passive: true });
document.addEventListener("keydown", resumeAudioOnGesture, { passive: true });

// 1. COUNTDOWN BEEP SFX (CRISP, CLEAR & ENERGETIC)
function playCountdownBeep(seconds) {
  const ctx = getAudioContext();
  if (!ctx) return;

  try {
    const now = ctx.currentTime;

    // Detik 0: Buzzer Waktu Habis
    if (seconds <= 0) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(170, now);
      osc.frequency.exponentialRampToValueAtTime(75, now + 0.32);

      const filter = ctx.createBiquadFilter();
      filter.type = "lowpass";
      filter.frequency.setValueAtTime(650, now);

      gain.gain.setValueAtTime(0.28, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.33);
      return;
    }

    // Detik 1: Urgent Double Beep
    if (seconds === 1) {
      [0, 0.085].forEach((offset) => {
        const osc = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "sine";
        osc.frequency.setValueAtTime(1050, now + offset);

        osc2.type = "triangle";
        osc2.frequency.setValueAtTime(2100, now + offset);

        gain.gain.setValueAtTime(0.26, now + offset);
        gain.gain.exponentialRampToValueAtTime(0.001, now + offset + 0.06);

        osc.connect(gain);
        osc2.connect(gain);
        gain.connect(ctx.destination);

        osc.start(now + offset);
        osc.stop(now + offset + 0.065);
        osc2.start(now + offset);
        osc2.stop(now + offset + 0.065);
      });
      return;
    }

    // Detik 5, 4, 3, 2: Nada radar naik bertingkat
    const freq = 720 + (5 - seconds) * 75; // 720Hz, 795Hz, 870Hz, 945Hz
    const osc = ctx.createOscillator();
    const osc2 = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = "sine";
    osc.frequency.setValueAtTime(freq, now);

    osc2.type = "triangle";
    osc2.frequency.setValueAtTime(freq * 2, now);

    gain.gain.setValueAtTime(0.24, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

    osc.connect(gain);
    osc2.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 0.085);
    osc2.start(now);
    osc2.stop(now + 0.085);
  } catch (_) {}
}

// 2. POP-UP WAKTU HABIS / SUMMARY (EPIC GAME-SHOW CHORD FANFARE)
function playPopupSummarySFX() {
  const ctx = getAudioContext();
  if (!ctx) return;

  try {
    const now = ctx.currentTime;
    // Chords: C5 (523), E5 (659), G5 (784), C6 (1046)
    const notes = [523.25, 659.25, 783.99, 1046.50];
    notes.forEach((freq, idx) => {
      const startTime = now + idx * 0.055;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "triangle";
      osc.frequency.setValueAtTime(freq, startTime);

      gain.gain.setValueAtTime(0.001, startTime);
      gain.gain.exponentialRampToValueAtTime(0.22, startTime + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.48);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(startTime);
      osc.stop(startTime + 0.49);
    });

    // Sub-bass impact
    const bassOsc = ctx.createOscillator();
    const bassGain = ctx.createGain();
    bassOsc.type = "sine";
    bassOsc.frequency.setValueAtTime(140, now);
    bassOsc.frequency.exponentialRampToValueAtTime(60, now + 0.32);
    bassGain.gain.setValueAtTime(0.25, now);
    bassGain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
    bassOsc.connect(bassGain);
    bassGain.connect(ctx.destination);
    bassOsc.start(now);
    bassOsc.stop(now + 0.33);
  } catch (_) {}
}

// 3. POP-UP PENJAWAB TERCEPAT (LIGHTNING POWER-UP SWEEP)
function playPopupFastestSFX() {
  const ctx = getAudioContext();
  if (!ctx) return;

  try {
    const now = ctx.currentTime;

    // Laser pitch sweep
    const sweep = ctx.createOscillator();
    const sweepGain = ctx.createGain();
    sweep.type = "sawtooth";
    sweep.frequency.setValueAtTime(280, now);
    sweep.frequency.exponentialRampToValueAtTime(1450, now + 0.16);

    const filter = ctx.createBiquadFilter();
    filter.type = "lowpass";
    filter.frequency.setValueAtTime(2200, now);

    sweepGain.gain.setValueAtTime(0.18, now);
    sweepGain.gain.exponentialRampToValueAtTime(0.001, now + 0.17);

    sweep.connect(filter);
    filter.connect(sweepGain);
    sweepGain.connect(ctx.destination);
    sweep.start(now);
    sweep.stop(now + 0.18);

    // High energetic ping bell (A6)
    const ping = ctx.createOscillator();
    const pingGain = ctx.createGain();
    ping.type = "sine";
    ping.frequency.setValueAtTime(1760, now + 0.12);
    pingGain.gain.setValueAtTime(0.24, now + 0.12);
    pingGain.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
    ping.connect(pingGain);
    pingGain.connect(ctx.destination);
    ping.start(now + 0.12);
    ping.stop(now + 0.56);
  } catch (_) {}
}

// 4. POP-UP GIFT ALERT (MAGICAL SPARKLE COIN CHIME)
function playGiftAlertSFX() {
  const ctx = getAudioContext();
  if (!ctx) return;

  try {
    const now = ctx.currentTime;
    const sparkleNotes = [987.77, 1318.51, 1567.98, 2093.00, 2637.02];
    sparkleNotes.forEach((freq, idx) => {
      const startTime = now + idx * 0.045;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(freq, startTime);

      gain.gain.setValueAtTime(0.001, startTime);
      gain.gain.exponentialRampToValueAtTime(0.22, startTime + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.35);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(startTime);
      osc.stop(startTime + 0.36);
    });
  } catch (_) {}
}

let lastMilestoneReached = false;

// 5. POP-UP MILESTONE / ROUND GOAL REACHED (TRIUMPHANT CELEBRATION CHORD)
function playMilestoneFanfareSFX() {
  const ctx = getAudioContext();
  if (!ctx) return;

  try {
    const now = ctx.currentTime;
    const notes = [523.25, 783.99, 1046.50, 1318.51, 1567.98];
    notes.forEach((freq, idx) => {
      const startTime = now + idx * 0.08;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "triangle";
      osc.frequency.setValueAtTime(freq, startTime);

      gain.gain.setValueAtTime(0.001, startTime);
      gain.gain.exponentialRampToValueAtTime(0.28, startTime + 0.03);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.65);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(startTime);
      osc.stop(startTime + 0.66);
    });
  } catch (_) {}
}

// ============================================================
// TEXT TO SPEECH (TTS) ENGINE
// ============================================================

// ============================================================
// STABLE HIGH-PERFORMANCE TTS ENGINE (LOCKED INDONESIA & NATURAL AUDIO)
// ============================================================

let ttsMode = "locked_id";
let activeUtterance = null;
let ttsWatchdogTimer = null;
let ttsVoiceCache = null;
let ttsAudioPlayer = null;

function getTtsAudioPlayer() {
  if (!ttsAudioPlayer) {
    ttsAudioPlayer = new Audio();
    ttsAudioPlayer.id = "overlayTtsAudio";
    ttsAudioPlayer.preload = "auto";
  }
  return ttsAudioPlayer;
}

function cleanQuestionTextForSpeech(text) {
  if (!text) return "";
  let clean = String(text).trim();
  clean = clean.replace(/[*_#`~]/g, "");
  clean = clean.replace(/\+/g, " tambah ");
  clean = clean.replace(/\s*-\s*/g, " kurang ");
  clean = clean.replace(/\s*[*×]\s*/g, " kali ");
  clean = clean.replace(/\s*[\/÷]\s*/g, " bagi ");
  clean = clean.replace(/\s*=\s*/g, " sama dengan ");
  clean = clean.replace(/\s*%\s*/g, " persen ");
  clean = clean.replace(/\.{2,}/g, ".");
  clean = clean.replace(/\?{2,}/g, "?");
  clean = clean.replace(/\s{2,}/g, " ");
  return clean.trim();
}

function getBestIndonesianVoice() {
  if (ttsVoiceCache) return ttsVoiceCache;
  if (!('speechSynthesis' in window)) return null;
  const voices = window.speechSynthesis.getVoices() || [];
  ttsVoiceCache = voices.find(
    (v) => v.lang && (v.lang.includes("id-ID") || v.lang.includes("id_ID") || v.lang.toLowerCase().startsWith("id"))
  ) || null;
  return ttsVoiceCache;
}

if ('speechSynthesis' in window) {
  window.speechSynthesis.onvoiceschanged = () => {
    ttsVoiceCache = null;
    getBestIndonesianVoice();
  };
}

function clearTTSWatchdog() {
  if (ttsWatchdogTimer) {
    clearInterval(ttsWatchdogTimer);
    ttsWatchdogTimer = null;
  }
}

function stopSpeech() {
  clearTTSWatchdog();
  if (ttsAudioPlayer) {
    try {
      ttsAudioPlayer.pause();
      ttsAudioPlayer.currentTime = 0;
    } catch (_) {}
  }
  if (!('speechSynthesis' in window)) return;
  try {
    window.speechSynthesis.cancel();
  } catch (_) {}
  activeUtterance = null;
}

function speakQuestion(question) {
  if (ttsMode === "disabled") return;
  if (!question || !question.question) return;
  if (question.id && question.id === lastSpokenQuestionId) return;

  lastSpokenQuestionId = question.id || question.question;
  const spokenText = cleanQuestionTextForSpeech(question.question);
  if (!spokenText) return;

  // Hentikan utterance / audio sebelumnya
  stopSpeech();

  // Mode "locked_id" (Default & Rekomendasi):
  // Menjamin 100% berbahasa Indonesia natural tanpa terpengaruh bahasa OBS / Windows
  if (ttsMode === "locked_id") {
    setTimeout(() => {
      try {
        const player = getTtsAudioPlayer();
        player.src = `/api/tts?text=${encodeURIComponent(spokenText)}`;
        player.play().catch((err) => {
          console.warn("TTS Audio autoplay caught:", err);
        });
      } catch (err) {
        console.warn("Gagal memutar audio TTS Indonesia:", err);
      }
    }, 45);
    return;
  }

  // Mode "browser": Menggunakan Web Speech API jika tersedia suara Bahasa Indonesia
  if (ttsMode === "browser") {
    const indonesianVoice = getBestIndonesianVoice();
    if (!indonesianVoice) {
      // JIKA OBS / SISTEM BAHASA INGGRIS DAN TIDAK ADA SUARA INDONESIA OFFLINE:
      // Otomatis fallback ke audio backend agar tidak membaca teks dengan suara Inggris yang merusak lafal!
      console.log("Suara id-ID offline tidak ditemukan di sistem. Fallback ke audio natural backend.");
      setTimeout(() => {
        try {
          const player = getTtsAudioPlayer();
          player.src = `/api/tts?text=${encodeURIComponent(spokenText)}`;
          player.play().catch(() => {});
        } catch (_) {}
      }, 45);
      return;
    }

    if (!('speechSynthesis' in window) || typeof SpeechSynthesisUtterance === 'undefined') return;

    setTimeout(() => {
      try {
        if (window.speechSynthesis.paused) {
          window.speechSynthesis.resume();
        }

        const utterance = new SpeechSynthesisUtterance(spokenText);
        activeUtterance = utterance;
        utterance.voice = indonesianVoice;
        utterance.lang = "id-ID";
        utterance.rate = 1.05;
        utterance.pitch = 1.0;

        utterance.onend = () => {
          clearTTSWatchdog();
          activeUtterance = null;
        };

        utterance.onerror = (e) => {
          clearTTSWatchdog();
          activeUtterance = null;
          if (e.error !== "canceled" && e.error !== "interrupted") {
            console.warn("TTS error:", e.error);
          }
        };

        clearTTSWatchdog();
        ttsWatchdogTimer = setInterval(() => {
          if (!('speechSynthesis' in window)) {
            clearTTSWatchdog();
            return;
          }
          if (window.speechSynthesis.speaking) {
            window.speechSynthesis.pause();
            window.speechSynthesis.resume();
          } else {
            clearTTSWatchdog();
          }
        }, 9000);

        window.speechSynthesis.speak(utterance);
      } catch (err) {
        console.warn("TTS tidak didukung atau tertahan browser:", err);
        clearTTSWatchdog();
        activeUtterance = null;
      }
    }, 45);
  }
}

// ============================================================
// NATIVE HTML5 AUDIO PLAYLIST ENGINE (.mp3, .wav, .mov)
// ============================================================

let audioPlayer = null;
let currentTrackKey = null;
let musicState = null;
let isEndedRequestPending = false;

function getAudioElement() {
  if (!audioPlayer) {
    audioPlayer = $("overlayAudio");
    if (!audioPlayer) {
      audioPlayer = new Audio();
      audioPlayer.id = "overlayAudio";
      audioPlayer.preload = "auto";
      document.body.appendChild(audioPlayer);
    }

    audioPlayer.addEventListener("ended", () => {
      if (!isEndedRequestPending && musicState?.is_playing) {
        isEndedRequestPending = true;
        postMusicEnded().finally(() => {
          isEndedRequestPending = false;
        });
      }
    });

    audioPlayer.addEventListener("playing", () => {
      updateMusicPill();
    });

    audioPlayer.addEventListener("error", (e) => {
      console.warn("Audio playback error:", e);
      showMusicError("Gagal memutar URL audio");
    });
  }
  return audioPlayer;
}

function updateMusicPill() {
  const pill = $("musicPill");
  if (pill) {
    pill.classList.add("hidden");
  }
}

function showMusicError(msg) {
  // Pill musik tidak ditampilkan di overlay sesuai preferensi streamer
  console.warn("Audio playback notice:", msg);
}

function applyAudioMusicState() {
  const audio = getAudioElement();
  if (!audio || !musicState) return;

  updateMusicPill();

  const track = musicState.current_track;
  if (!track) {
    audio.pause();
    audio.removeAttribute("src");
    currentTrackKey = null;
    return;
  }

  // Atur volume (0.0 - 1.0) dikontrol dari dashboard
  const volPercent = Number(musicState.volume ?? 75);
  audio.volume = Math.max(0, Math.min(1, volPercent / 100));

  const trackKey = `${track.track_key}:${musicState.play_generation || 0}`;
  if (currentTrackKey !== trackKey) {
    currentTrackKey = trackKey;
    isEndedRequestPending = false;
    audio.src = track.url;
    audio.load();

    if (musicState.is_playing) {
      audio.play().catch((err) => {
        console.warn("Audio autoplay tertahan lingkungan:", err);
      });
    }
    return;
  }

  if (musicState.is_playing && audio.paused) {
    audio.play().catch((err) => {
      console.warn("Play audio tertahan lingkungan:", err);
    });
  } else if (!musicState.is_playing && !audio.paused) {
    audio.pause();
  }
}

function handleOverlayMusicState(state) {
  if (!state) return;
  musicState = state;
  applyAudioMusicState();
}

async function postMusicEnded() {
  try {
    await fetch("/api/music/control", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "ended" }),
    });
  } catch (_) {}
}

async function fetchInitialMusicState() {
  try {
    const res = await fetch("/api/music/state");
    if (res.ok) {
      const data = await res.json();
      handleOverlayMusicState(data);
    }
  } catch (_) {}
}

// ============================================================
// MODULAR THEME SWITCHING ENGINE
// ============================================================

function applyTheme(themeId) {
  if (!themeId) return;
  const link = $("themeStylesheet");
  if (!link) return;
  const targetHref = `/static/overlay/themes/${encodeURIComponent(themeId)}/style.css`;
  const currentHref = link.getAttribute("href") || "";
  if (!currentHref.includes(targetHref)) {
    link.href = targetHref;
  }
}

// ============================================================
// WEBSOCKET & RENDERING ENGINE
// ============================================================

function connect() {
  if (socket && [WebSocket.OPEN, WebSocket.CONNECTING].includes(socket.readyState)) return;
  const protocol = location.protocol === "https:" ? "wss" : "ws";
  socket = new WebSocket(`${protocol}://${location.host}/ws`);
  socket.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data);
      if (message.type === "game_state") {
        render(message.data, message.live);
        if (message.music) {
          handleOverlayMusicState(message.music);
        }
        if (message.theme && !window.__LOCKED_THEME__) {
          applyTheme(message.theme);
        }
        if (message.tts_mode) {
          ttsMode = message.tts_mode;
        }
      } else if (message.type === "theme_changed") {
        if (!window.__LOCKED_THEME__ && message.theme) {
          applyTheme(message.theme);
        }
      } else if (message.type === "tts_setting_changed") {
        if (message.tts_mode) {
          ttsMode = message.tts_mode;
        }
      }
    } catch (_) {}
  };
  socket.onclose = () => {
    clearTimeout(reconnectTimer);
    reconnectTimer = setTimeout(connect, 1800);
  };
  socket.onerror = () => socket.close();
}

function renderAnswers(question, phase) {
  const grid = $("answersGrid");
  if (!grid) return;
  grid.replaceChildren();
  const options = question?.options || {};
  ["A", "B", "C", "D"].forEach((key) => {
    const card = document.createElement("div");
    card.className = `answer-card opt-${key.toLowerCase()}`;
    if ((phase === "reveal" || phase === "finished") && question?.correct_answer === key) {
      card.classList.add("correct");
    } else if ((phase === "reveal" || phase === "finished") && question?.correct_answer && question.correct_answer !== key) {
      card.classList.add("dimmed");
    }

    const badge = document.createElement("div");
    badge.className = "answer-badge";
    badge.textContent = key;

    const copy = document.createElement("div");
    copy.className = "answer-copy";

    const title = document.createElement("div");
    title.className = "answer-title";
    title.textContent = `PILIHAN ${key}`;

    const text = document.createElement("div");
    text.className = "answer-text";
    text.textContent = options[key] || "-";

    copy.append(title, text);
    card.append(badge, copy);
    grid.appendChild(card);
  });
}

function renderLeaderboard(rows, playersCount) {
  const container = $("leaderboard");
  if (!container) return;
  container.replaceChildren();
  const countEl = $("leaderboardCount");
  if (countEl) countEl.textContent = `${playersCount || rows?.length || 0} pemain`;

  const meter = $("leaderboardMeter");
  if (meter) {
    const pct = Math.min(100, Math.max(0, ((rows?.length || 0) / 10) * 100));
    meter.style.width = `${pct}%`;
  }

  if (!rows || rows.length === 0) {
    const empty = document.createElement("div");
    empty.className = "arcade-empty-box";
    empty.innerHTML = `
      <div class="empty-icon yellow-box">🏆</div>
      <p class="empty-title">Belum ada pemain</p>
      <span class="empty-sub text-yellow">JADILAH #1</span>
    `;
    container.appendChild(empty);
    return;
  }

  // Muat hingga 5 pemain secara rapi dan kompak di panel brutalist
  rows.slice(0, 5).forEach((player, index) => {
    const row = document.createElement("div");
    row.className = "panel-row";

    const rank = document.createElement("div");
    rank.className = "row-rank";
    rank.textContent = String(index + 1);

    const info = document.createElement("div");
    info.className = "row-info";
    const name = document.createElement("div");
    name.className = "row-name";
    name.textContent = player.username || "Viewer";
    const meta = document.createElement("div");
    meta.className = "row-meta";
    meta.textContent = `${player.correct_answers || 0} benar`;
    info.append(name, meta);

    const score = document.createElement("div");
    score.className = "row-score";
    score.textContent = player.score ?? 0;

    row.append(rank, info, score);
    container.appendChild(row);
  });
}

function renderSupporters(live) {
  const supporters = live?.gift_leaderboard || [];
  const countEl = $("gifterCount");
  if (countEl) countEl.textContent = `${supporters.length} supporter`;

  const meter = $("supportersMeter");
  if (meter) {
    const pct = Math.min(100, Math.max(0, (supporters.length / 5) * 100));
    meter.style.width = `${pct}%`;
  }

  const container = $("supportersList");
  if (!container) return;
  container.replaceChildren();

  if (!supporters.length) {
    const empty = document.createElement("div");
    empty.className = "arcade-empty-box";
    empty.innerHTML = `
      <div class="empty-icon pink-box">🎁</div>
      <p class="empty-title">Belum ada gift</p>
      <span class="empty-sub text-pink">KIRIM KOIN</span>
    `;
    container.appendChild(empty);
    return;
  }

  // Muat hingga 5 supporter secara rapi dan kompak
  supporters.slice(0, 5).forEach((item) => {
    const row = document.createElement("div");
    row.className = "panel-row";

    const rank = document.createElement("div");
    rank.className = "row-rank";
    rank.textContent = String(item.rank);

    const info = document.createElement("div");
    info.className = "row-info";
    const name = document.createElement("div");
    name.className = "row-name";
    name.textContent = item.username;
    const meta = document.createElement("div");
    meta.className = "row-meta";
    meta.textContent = `${item.gift_count} gifts`;
    info.append(name, meta);

    const score = document.createElement("div");
    score.className = "row-score";
    score.textContent = `${Number(item.diamonds || 0).toLocaleString("id-ID")} ♦`;

    row.append(rank, info, score);
    container.appendChild(row);
  });
}

function renderLive(live) {
  if (!live) return;

  renderSupporters(live);

  const alert = live.gift_alert;
  const alertNode = $("giftAlert");
  if (alertNode) {
    if (alert && alert.expires_at * 1000 > Date.now()) {
      if (lastGiftAlertId !== alert.id) {
        lastGiftAlertId = alert.id;
        const alertText = $("giftAlertText");
        if (alertText) alertText.textContent = `${alert.username} mengirim ${alert.quantity}× ${alert.gift_name}!`;
        alertNode.classList.remove("hidden");
        alertNode.style.animation = "none";
        void alertNode.offsetWidth;
        alertNode.style.animation = "";

        // Putar suara koin hadiah magis jika audio sudah di-unlock
        playGiftAlertSFX();
      }
    } else {
      alertNode.classList.add("hidden");
    }
  }
}

function updateCountdown(phase, remaining, total, autoPlayRemaining) {
  const floatNode = $("countdownFloat");
  const circle = $("countdownProgress");
  if (!floatNode || !circle) return;

  const radius = circle.r?.baseVal?.value || 41;
  const circumference = 2 * Math.PI * radius;

  let label = "VOTING";
  let caption = "SEKON";
  let value = "--";
  let progress = 0;

  if (phase === "question") {
    const seconds = Math.ceil(Math.max(0, remaining));
    label = "VOTING";
    caption = "SEKON";
    value = String(seconds);
    progress = Math.max(0, Math.min(1, remaining / Math.max(1, total)));
    const urgent = seconds > 0 && seconds <= 5;
    floatNode.classList.toggle("urgent", urgent);

    if (!urgent && seconds > 5) {
      lastBeepKey = null;
    } else if (urgent) {
      const beepKey = `q:${seconds}`;
      if (beepKey !== lastBeepKey) {
        lastBeepKey = beepKey;
        playCountdownBeep(seconds);
      }
    }
  } else if (phase === "reveal") {
    const seconds = Math.ceil(Math.max(0, autoPlayRemaining));
    label = "AUTO";
    caption = "NEXT";
    value = String(seconds > 0 ? seconds : 0);
    progress = seconds / Math.max(1, seconds || 1);
    floatNode.classList.remove("urgent");

    // Bunyikan buzzer jika baru saja berpindah ke reveal
    if (lastBeepKey !== "done") {
      lastBeepKey = "done";
      playCountdownBeep(0);
    }
  } else if (phase === "waiting_gift") {
    label = "GIFT";
    caption = "GOAL";
    value = "🎁";
    progress = 1;
    floatNode.classList.remove("urgent");
    lastBeepKey = null;
  } else if (phase === "paused") {
    label = "PAUSE";
    caption = "STREAM";
    value = "||";
    progress = 0;
    floatNode.classList.remove("urgent");
    lastBeepKey = null;
  } else if (phase === "finished") {
    label = "DONE";
    caption = "SESI";
    value = "✓";
    progress = 0;
    floatNode.classList.remove("urgent");
    lastBeepKey = null;
  } else {
    floatNode.classList.remove("urgent");
    lastBeepKey = null;
  }

  const timerLabel = $("timerLabel");
  if (timerLabel) timerLabel.textContent = label;
  const timerCaption = $("timerCaption");
  if (timerCaption) timerCaption.textContent = caption;
  const timerText = $("timerText");
  if (timerText) timerText.textContent = value;

  circle.style.strokeDasharray = String(circumference);
  circle.style.strokeDashoffset = String(circumference * (1 - progress));
}

function hideCenterPopup() {
  const popup = $("centerPopup");
  const charWrap = $("popupCharacterWrap");
  if (!popup) return;
  popup.classList.add("hide-out");
  clearTimeout(centerPopupTimer);
  centerPopupTimer = setTimeout(() => {
    popup.classList.add("hidden");
    popup.classList.remove("hide-out", "fastest", "summary");
    if (charWrap) charWrap.classList.add("hidden");
  }, 300);
}

function showFastestPopup(fastest) {
  const popup = $("centerPopup");
  const card = $("centerPopupCard");
  const charWrap = $("popupCharacterWrap");
  if (!popup || !card || !fastest) return;

  clearTimeout(centerPopupTimer);
  card.replaceChildren();

  // KARAKTER 3D TRANSPARAN DI ATAS POPUP JAWABAN TERCEPAT
  if (charWrap) {
    if (characterAnimationEnabled) {
      charWrap.classList.remove("hidden");
      const charImg = $("popupCharacterGif");
      if (charImg && !charImg.src.includes("/static/overlay/assets/karakter_3d_transparan.gif")) {
        charImg.src = "/static/overlay/assets/karakter_3d_transparan.gif";
      }
    } else {
      charWrap.classList.add("hidden");
    }
  }

  // Mainkan SFX Kilat Penjawab Tercepat
  playPopupFastestSFX();

  const icon = document.createElement("div");
  icon.className = "center-popup-icon";
  icon.textContent = "⚡";

  const eyebrow = document.createElement("div");
  eyebrow.className = "center-popup-eyebrow";
  eyebrow.textContent = "PENJAWAB TERCEPAT";

  const title = document.createElement("div");
  title.className = "center-popup-title";
  title.textContent = "Jawaban Tercepat!";

  const name = document.createElement("div");
  name.className = "center-popup-name";
  name.textContent = fastest.username || "Viewer";

  const points = document.createElement("div");
  points.className = "center-popup-points";
  points.textContent = `+${Number(fastest.bonus_points || 50)} POIN`;

  const note = document.createElement("div");
  note.className = "center-popup-note";
  note.textContent = "Penjawab benar pertama ronde ini";

  card.append(icon, eyebrow, title, name, points, note);
  popup.classList.remove("hidden", "hide-out", "summary");
  popup.classList.add("fastest");
  centerPopupTimer = setTimeout(hideCenterPopup, 3800);
}

// SATUKAN POPUP HASIL WAKTU HABIS DENGAN KUNCI JAWABAN & PENJELASAN
function showRoundSummary(summary, question) {
  const popup = $("centerPopup");
  const card = $("centerPopupCard");
  if (!popup || !card || !summary) return;

  clearTimeout(centerPopupTimer);
  card.replaceChildren();

  // Mainkan SFX Fanfare Pengumuman Hasil
  playPopupSummarySFX();

  const icon = document.createElement("div");
  icon.className = "center-popup-icon";
  icon.textContent = "⏱";

  const eyebrow = document.createElement("div");
  eyebrow.className = "center-popup-eyebrow";
  eyebrow.textContent = "WAKTU HABIS · HASIL RONDE";

  const title = document.createElement("div");
  title.className = "center-popup-title";
  title.textContent = "Waktu Habis!";

  card.append(icon, eyebrow, title);

  // KOTAK KUNCI JAWABAN & PENJELASAN TERPADU
  if (question?.correct_answer) {
    const answerBox = document.createElement("div");
    answerBox.className = "center-popup-answer-box";

    const answerBadge = document.createElement("div");
    answerBadge.className = "center-popup-answer-badge";
    answerBadge.textContent = `✓ Jawaban Benar: ${question.correct_answer}`;
    answerBox.appendChild(answerBadge);

    if (question.explanation) {
      const exp = document.createElement("div");
      exp.className = "center-popup-explanation";
      exp.textContent = question.explanation;
      answerBox.appendChild(exp);
    }
    card.appendChild(answerBox);
  }

  // STATISTIK PERTANYAAN
  const stats = document.createElement("div");
  stats.className = "center-popup-stats";

  const correct = document.createElement("div");
  correct.className = "center-popup-stat good";
  const correctValue = document.createElement("strong");
  correctValue.textContent = String(summary.correct_count || 0);
  const correctLabel = document.createElement("span");
  correctLabel.textContent = "Jawaban Benar";
  correct.append(correctValue, correctLabel);

  const wrong = document.createElement("div");
  wrong.className = "center-popup-stat bad";
  const wrongValue = document.createElement("strong");
  wrongValue.textContent = String(summary.wrong_count || 0);
  const wrongLabel = document.createElement("span");
  wrongLabel.textContent = "Jawaban Salah";
  wrong.append(wrongValue, wrongLabel);

  stats.append(correct, wrong);

  const total = document.createElement("div");
  total.className = "center-popup-total";
  total.textContent = `${Number(summary.answered_count || 0)} PENONTON MENJAWAB`;

  card.append(stats, total);

  // KARAKTER 3D TRANSPARAN DI BAWAH POPUP WAKTU SELESAI
  const charWrap = $("popupCharacterWrap");
  if (charWrap) {
    if (characterAnimationEnabled) {
      charWrap.classList.remove("hidden");
      const charImg = $("popupCharacterGif");
      if (charImg && !charImg.src.includes("/static/overlay/assets/karakter_3d_transparan.gif")) {
        charImg.src = "/static/overlay/assets/karakter_3d_transparan.gif";
      }
    } else {
      charWrap.classList.add("hidden");
    }
  }

  popup.classList.remove("hidden", "hide-out", "fastest");
  popup.classList.add("summary");
  centerPopupTimer = setTimeout(hideCenterPopup, 5200);
}

function handleRoundPopups(state, phase, question) {
  const roundKey = `${state.question_number || 0}:${question?.id || "none"}`;

  if (phase === "question" && roundKey !== activeRoundKey) {
    activeRoundKey = roundKey;
    lastFastestPopupKey = null;
    lastSummaryPopupKey = null;
    // BACA SOAL SECARA OTOMATIS JIKA BROWSER MENDUKUNG TTS & SUDAH UNLOCKED
    speakQuestion(question);
  }

  if (phase !== "question") {
    stopSpeech();
  }

  if (phase === "question" && state.fastest_answer) {
    const fastestKey = `${roundKey}:${state.fastest_answer.username || "viewer"}`;
    if (fastestKey !== lastFastestPopupKey) {
      lastFastestPopupKey = fastestKey;
      showFastestPopup(state.fastest_answer);
    }
  }

  if ((phase === "reveal" || phase === "finished") && state.round_summary) {
    const summaryKey = `${roundKey}:summary`;
    if (summaryKey !== lastSummaryPopupKey) {
      lastSummaryPopupKey = summaryKey;
      showRoundSummary(state.round_summary, question);
    }
  }

  if (phase === "idle" || phase === "finished") {
    activeRoundKey = null;
  }
  if (phase === "idle") {
    lastFastestPopupKey = null;
    lastSummaryPopupKey = null;
    stopSpeech();
  }
}

function render(state, live) {
  const phase = state.phase || "idle";
  const question = state.current_question || null;
  const answerDuration = Math.max(1, Number(state.answer_duration || 15));
  const remaining = Math.max(0, Number(state.remaining_seconds || 0));
  const autoPlay = Boolean(state.auto_play);
  const autoAdvanceRemaining = Math.max(0, Number(state.auto_advance_remaining_seconds || 0));

  handleRoundPopups(state, phase, question);

  // SINKRONISASI TOGGLE ANIMASI KARAKTER SECARA REALTIME
  if (state.character_animation !== undefined) {
    characterAnimationEnabled = Boolean(state.character_animation);
    const charWrap = $("popupCharacterWrap");
    const centerPopup = $("centerPopup");
    if (charWrap && centerPopup) {
      if (!centerPopup.classList.contains("hidden")) {
        charWrap.classList.toggle("hidden", !characterAnimationEnabled);
      }
    }
    const mCharWrap = $("milestoneCharacterWrap");
    const mPopup = $("milestonePopup");
    if (mCharWrap && mPopup) {
      if (!mPopup.classList.contains("hidden")) {
        mCharWrap.classList.toggle("hidden", !characterAnimationEnabled);
      }
    }
  }

  const roundText = $("roundText");
  if (roundText) {
    const qNum = String(state.question_number || 1).padStart(2, "0");
    const qTotal = state.endless ? "∞" : String(state.question_count || 10).padStart(2, "0");
    if (state.batch_round && state.batch_round > 1) {
      roundText.innerHTML = `R${state.batch_round} · SOAL <span class="round-num">${qNum}</span> / <span class="round-total">${qTotal}</span>`;
    } else {
      roundText.innerHTML = `ROUND <span class="round-num">${qNum}</span> / <span class="round-total">${qTotal}</span>`;
    }
  }

  const categoryText = $("categoryText");
  if (categoryText) categoryText.textContent = question?.category || "GENERAL";

  const questionId = $("questionId");
  if (questionId) questionId.textContent = question?.id ? `ID #${String(question.id).toUpperCase()}` : "LIVE ROUND";

  const questionText = $("questionText");
  if (questionText) {
    questionText.textContent = question?.question || (
      phase === "waiting_gift" ? `Target ${state.question_count || 100} soal selesai! Kirim gift untuk membuka ronde berikutnya.` :
      (phase === "finished" ? "Sesi kuis telah selesai. Terima kasih sudah bermain!" : "Menunggu streamer memulai kuis...")
    );
  }

  const answerStats = $("answerStats");
  if (answerStats) {
    answerStats.innerHTML = `
      <span class="stat-pill"><svg class="stat-icon text-cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 01-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" stroke-linecap="round" stroke-linejoin="round"></path></svg>${state.players_count || 0} PEMAIN</span>
      <span class="stat-dot">•</span>
      <span class="stat-pill"><svg class="stat-icon text-green" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round"></path></svg>${state.answered_count || 0} JAWABAN</span>
    `;
  }

  const statusBadge = $("questionStatusBadge");
  if (statusBadge) {
    if (phase === "question") {
      statusBadge.textContent = "ACTIVE";
      statusBadge.className = "status-badge active";
    } else if (phase === "reveal") {
      statusBadge.textContent = "REVEAL";
      statusBadge.className = "status-badge reveal";
    } else if (phase === "waiting_gift") {
      statusBadge.textContent = "GIFT GOAL";
      statusBadge.className = "status-badge gift";
    } else if (phase === "paused") {
      statusBadge.textContent = "PAUSED";
      statusBadge.className = "status-badge paused";
    } else {
      statusBadge.textContent = "IDLE";
      statusBadge.className = "status-badge idle";
    }
  }

  renderAnswers(question, phase);
  renderLeaderboard(state.leaderboard || [], state.players_count || 0);
  renderLive(live);
  updateCountdown(phase, remaining, answerDuration, autoPlay ? autoAdvanceRemaining : 0);

  const hint = $("chatHint");
  if (hint) {
    if (phase === "question") {
      hint.innerHTML = '<span class="hint-icon">💬</span> <span class="hint-label">KETIK</span> <span class="hint-badge badge-a">A</span> <span class="hint-slash">/</span> <span class="hint-badge badge-b">B</span> <span class="hint-slash">/</span> <span class="hint-badge badge-c">C</span> <span class="hint-slash">/</span> <span class="hint-badge badge-d">D</span> <span class="hint-label">DI KOMENTAR LIVE</span>';
    } else if (phase === "reveal" && autoPlay) {
      hint.innerHTML = '<span class="hint-icon">⚡</span> <span class="hint-label">AUTO PLAY · SOAL BERIKUTNYA SEGERA DIMULAI</span>';
    } else if (phase === "reveal") {
      hint.innerHTML = '<span class="hint-icon">⏱</span> <span class="hint-label">WAKTU HABIS · HASIL RONDE</span>';
    } else if (phase === "waiting_gift") {
      hint.innerHTML = '<span class="hint-icon">🎁</span> <span class="hint-label">KIRIM GIFT UNTUK MEMULAI RONDE BERIKUTNYA!</span>';
    } else if (phase === "paused") {
      hint.innerHTML = '<span class="hint-icon">⏸</span> <span class="hint-label">PERMAINAN DIJEDA OLEH STREAMER</span>';
    } else if (phase === "finished") {
      hint.innerHTML = '<span class="hint-icon">🏁</span> <span class="hint-label">SESI KUIS TELAH SELESAI</span>';
    } else {
      hint.innerHTML = '<span class="hint-icon">⚡</span> <span class="hint-label">PLAY TOGETHER · WIN TOGETHER</span>';
    }
  }

  // Handle Milestone / Waiting-Gift Popup
  const milestonePopup = $("milestonePopup");
  if (milestonePopup) {
    if (phase === "waiting_gift" && state.waiting_gift) {
      const wg = state.waiting_gift;
      milestonePopup.classList.remove("hidden");
      const centerPop = $("centerPopup");
      if (centerPop) centerPop.classList.add("hidden");

      const colEl = $("milestoneGiftCollected");
      if (colEl) colEl.textContent = wg.collected ?? 0;
      const tarEl = $("milestoneGiftTarget");
      if (tarEl) tarEl.textContent = wg.target ?? 0;
      const fillEl = $("milestoneProgressFill");
      if (fillEl) fillEl.style.width = `${wg.progress_percent ?? 0}%`;

      const statusEl = $("milestoneGiftStatus");
      const titleEl = $("milestoneTitle");
      const cardEl = $("milestonePopupCard");

      // KARAKTER 3D TRANSPARAN DI BAWAH POPUP RONDE SELESAI
      const mCharWrap = $("milestoneCharacterWrap");
      if (mCharWrap) {
        if (characterAnimationEnabled) {
          mCharWrap.classList.remove("hidden");
          const mImg = $("milestoneCharacterGif");
          if (mImg && !mImg.src.includes("/static/overlay/assets/karakter_3d_transparan.gif")) {
            mImg.src = "/static/overlay/assets/karakter_3d_transparan.gif";
          }
        } else {
          mCharWrap.classList.add("hidden");
        }
      }

      if (wg.reached) {
        if (!lastMilestoneReached) {
          lastMilestoneReached = true;
          playMilestoneFanfareSFX();
        }
        if (cardEl) cardEl.classList.add("reached");
        if (titleEl) titleEl.textContent = "Target Gift Tercapai! 🎉";
        if (statusEl) statusEl.textContent = "Memulai ronde baru dalam hitungan detik...";
      } else {
        lastMilestoneReached = false;
        if (cardEl) cardEl.classList.remove("reached");
        if (titleEl) titleEl.textContent = "Ronde Selesai!";
        if (statusEl) {
          statusEl.textContent = `Terkumpul ${wg.progress_percent ?? 0}% · Butuh ${wg.remaining ?? 0} diamonds lagi`;
        }
      }
    } else {
      milestonePopup.classList.add("hidden");
      const mCharWrap = $("milestoneCharacterWrap");
      if (mCharWrap) mCharWrap.classList.add("hidden");
      lastMilestoneReached = false;
    }
  }
}

// Inisialisasi awal
fetchInitialMusicState();
connect();
