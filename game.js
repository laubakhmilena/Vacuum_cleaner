"use strict";

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d", { alpha: false });
const VACUUM_PLAYER_FILE_SRC = new URL("assets/vacuum_player.png", window.location.href).href;
const VACUUM_PLAYER_SRC = window.VACUUM_PLAYER_DATA_URI || VACUUM_PLAYER_FILE_SRC;
const vacuumPlayerPreload = document.getElementById("vacuumPreload");
// QA-010: битмап игрока грузится ровно один раз. Уже объявленный в разметке
// preload-элемент переиспользуется как источник для canvas вместо второго Image(),
// поэтому одна и та же картинка не запрашивается дважды.
const vacuumPlayerImage = vacuumPlayerPreload instanceof HTMLImageElement ? vacuumPlayerPreload : new Image();
const vacuumPlayerImageIsPreload = vacuumPlayerImage === vacuumPlayerPreload;
let vacuumPlayerImageLoaded = false;
vacuumPlayerImage.decoding = "sync";
const criticalAssetsReady = new Promise((resolve) => {
  const loaded = () => {
    vacuumPlayerImageLoaded = true;
    resolve();
  };
  const failed = () => {
    // The existing vector renderer is usable when the bitmap fails.
    vacuumPlayerImageLoaded = false;
    resolve();
  };
  vacuumPlayerImage.onload = loaded;
  vacuumPlayerImage.onerror = failed;
  if (vacuumPlayerImage.complete && vacuumPlayerImage.getAttribute("src")) {
    if (vacuumPlayerImage.naturalWidth > 0) loaded();
    else failed();
  }
});
if (!vacuumPlayerImageIsPreload || !vacuumPlayerImage.getAttribute("src")) {
  vacuumPlayerImage.src = VACUUM_PLAYER_SRC;
}

function isVacuumBitmapReady() {
  return vacuumPlayerImageLoaded && vacuumPlayerImage.complete && vacuumPlayerImage.naturalWidth > 0;
}

if (vacuumPlayerImage.complete && vacuumPlayerImage.naturalWidth > 0) {
  vacuumPlayerImageLoaded = true;
}

const screens = {
  menu: document.getElementById("menuScreen"),
  upgrades: document.getElementById("upgradesScreen"),
  game: document.getElementById("gameScreen"),
  gameOver: document.getElementById("gameOverScreen")
};

const ui = {
  menuBestScore: document.getElementById("menuBestScore"),
  continueButton: document.getElementById("continueButton"),
  playButton: document.getElementById("playButton"),
  starsCount: document.getElementById("starsCount"),
  upgradesList: document.getElementById("upgradesList"),
  boostersList: document.getElementById("boostersList"),
  skinsList: document.getElementById("skinsList"),
  dailyRewardText: document.getElementById("dailyRewardText"),
  dailyRewardButton: document.getElementById("dailyRewardButton"),
  dailyTasksList: document.getElementById("dailyTasksList"),
  tasksBonusText: document.getElementById("tasksBonusText"),
  hudScore: document.getElementById("hudScore"),
  hudLives: document.getElementById("hudLives"),
  hudCombo: document.getElementById("hudCombo"),
  bonusPill: document.getElementById("bonusPill"),
  finalScore: document.getElementById("finalScore"),
  finalBestScore: document.getElementById("finalBestScore"),
  earnedStars: document.getElementById("earnedStars"),
  adNotice: document.getElementById("adNotice"),
  reviveAdButton: document.getElementById("reviveAdButton"),
  doubleStarsAdButton: document.getElementById("doubleStarsAdButton"),
  gameMenuButton: document.getElementById("gameMenuButton"),
  soundToggleButton: document.getElementById("soundToggleButton"),
  resetProgressButton: document.getElementById("resetProgressButton"),
  resetDialog: document.getElementById("resetDialog"),
  resetDialogTitle: document.getElementById("resetDialogTitle"),
  resetDialogText: document.getElementById("resetDialogText"),
  resetConfirmButton: document.getElementById("resetConfirmButton"),
  resetCancelButton: document.getElementById("resetCancelButton")
};

const STORAGE_KEY = "thoughtVacuumProgress.v1";
const ACTIVE_KEY = "thoughtVacuumActive.v1";
const PROGRESS_VERSION = 1;
const ACTIVE_SAVE_VERSION = 1;
const ACTIVE_SAVE_INTERVAL_MS = 1000;
const ACTIVE_SAVE_TTL_MS = 12 * 60 * 60 * 1000;
const ACTIVE_SAVE_FUTURE_SKEW_MS = 5 * 60 * 1000;
const ACTIVE_SAVE_MAX_THOUGHTS = 60;
const CLOUD_TIMEOUT_MS = 8000;
const CLOUD_DEBOUNCE_MS = 4000;
const CLOUD_MAX_RETRIES = 3;
const REWARDED_SAFETY_TIMEOUT_MS = 180000;
const PURCHASE_COOLDOWN_MS = 450;
const KEYBOARD_SPEED = 620;
const MAX_LIVES_LIMIT = 10;
const MAX_COMBO = 5;

const GOOD_EMOJIS = ["💡", "🎵", "🌸", "✨", "🍀", "😊", "🧁"];
const BAD_EMOJIS = ["⚡", "💢", "🌀", "😵", "☁️", "🔥"];
const GOLD_EMOJIS = ["⭐", "🌟", "💛"];
const RAINBOW_EMOJIS = ["🌈"];
const RAINBOW_COLORS = ["#ff6f91", "#ffae42", "#ffd75d", "#1fbfa3", "#36a3ff", "#8878ff"];
const THOUGHT_TYPES = new Set(["good", "bad", "gold", "rainbow"]);
const DAILY_REWARD_STARS = 3;
const DAILY_TASK_REWARD = 2;
const DAILY_ALL_TASKS_REWARD = 3;
const MAX_BOOSTERS = 3;
const RU_LANGUAGE_CODES = new Set(["ru", "be", "kk", "uk", "uz"]);

const diagnostics = {
  activeSaveWrites: 0,
  activeSaveRestores: 0,
  assetErrors: 0,
  cloudLoads: 0,
  cloudState: "idle",
  cloudWrites: 0,
  gameplayStartCalls: 0,
  gameplayStopCalls: 0,
  loadingReadyCalls: 0,
  mergeDecision: "none",
  rewardedRequests: 0,
  rewardedRewards: 0,
  storageWriteFailures: 0,
  playerVisualScale: 0.4,
  rainbowSpawns: 0,
  rainbowCollections: 0,
  lastRainbowPoints: 0
};
window.__thoughtVacuumDiagnostics = diagnostics;

const TRANSLATIONS = {
  ru: {
    pageTitle: "Пылесос Пыслей",
    canvasLabel: "Игровое поле",
    menuEyebrow: "Уютная аркада",
    menuTitle: "Пылесос Пыслей",
    menuLead: "Управляй милым пылесосом с магической аурой: собирай хорошие мысли, избегай вредных и лови золотые бонусы.",
    bestResult: "Лучший результат:",
    dailyRewardTitle: "Ежедневный бонус",
    dailyRewardReady: "Забери подарок за вход",
    dailyRewardClaimed: "Бонус уже получен",
    play: "Играть",
    newGame: "Начать заново",
    continueGame: "Продолжить игру",
    upgrades: "Улучшения",
    workshop: "мастерская",
    boosters: "Бустеры",
    boostersLimit: "До 3 штук каждого",
    skins: "Скины",
    skinsNote: "Только внешний вид",
    dailyTasks: "Задания дня",
    allTasksBonus: "Бонус за все: ★ {value}",
    allTasksClaimed: "Бонус за все получен",
    back: "Назад",
    score: "Очки",
    lives: "Жизни",
    combo: "Комбо",
    menu: "Меню",
    bonus: "Бонус",
    gameRoundTitle: "Игровой раунд",
    gameOverEyebrow: "поток очищен",
    gameOver: "Игра окончена",
    best: "Лучший",
    stars: "Звезды",
    reviveAd: "Смотреть рекламу: +1 жизнь",
    doubleStarsAd: "Смотреть рекламу: x2 звезды",
    restart: "Играть снова",
    max: "Макс.",
    ownedCount: "Есть: {count}/{max}",
    ownedForever: "Куплен навсегда",
    price: "Цена ★ {cost}",
    selected: "Выбран",
    select: "Выбрать",
    reward: "награда ★ {value}",
    done: "Готово",
    claim: "Забрать",
    soundOn: "Отключить звук",
    soundOff: "Включить звук",
    smartMagnet: "умный магнит",
    slow: "замедление",
    shield: "щит",
    adUnavailable: "Реклама сейчас недоступна. Награда не начислена.",
    adNotCompleted: "Реклама не была досмотрена. Награда не начислена.",
    adBusy: "Дождитесь завершения текущей рекламы.",
    resetProgress: "Сброс прогресса",
    resetDialogTitle: "Сбросить весь прогресс?",
    resetDialogText: "Будут удалены лучший результат, звезды, улучшения, бустеры, скины, ежедневные задания и незавершенный раунд. Действие необратимо.",
    resetConfirm: "Сбросить",
    resetCancel: "Отмена"
  },
  en: {
    pageTitle: "Thought Vacuum",
    canvasLabel: "Game field",
    menuEyebrow: "Cute arcade game",
    menuTitle: "Thought Vacuum",
    menuLead: "Guide a cute vacuum with a magic aura: collect good thoughts, avoid harmful ones, and catch golden bonuses.",
    bestResult: "Best score:",
    dailyRewardTitle: "Daily bonus",
    dailyRewardReady: "Claim your login gift",
    dailyRewardClaimed: "Bonus already claimed",
    play: "Play",
    newGame: "Start new game",
    continueGame: "Continue game",
    upgrades: "Upgrades",
    workshop: "workshop",
    boosters: "Boosters",
    boostersLimit: "Up to 3 of each",
    skins: "Skins",
    skinsNote: "Visual only",
    dailyTasks: "Daily tasks",
    allTasksBonus: "Bonus for all: ★ {value}",
    allTasksClaimed: "All-tasks bonus claimed",
    back: "Back",
    score: "Score",
    lives: "Lives",
    combo: "Combo",
    menu: "Menu",
    bonus: "Bonus",
    gameRoundTitle: "Game round",
    gameOverEyebrow: "stream cleared",
    gameOver: "Game over",
    best: "Best",
    stars: "Stars",
    reviveAd: "Watch ad: +1 life",
    doubleStarsAd: "Watch ad: x2 stars",
    restart: "Play again",
    max: "Max",
    ownedCount: "Owned: {count}/{max}",
    ownedForever: "Owned forever",
    price: "Price ★ {cost}",
    selected: "Selected",
    select: "Select",
    reward: "reward ★ {value}",
    done: "Done",
    claim: "Claim",
    soundOn: "Mute sound",
    soundOff: "Enable sound",
    smartMagnet: "smart magnet",
    slow: "slow",
    shield: "shield",
    adUnavailable: "Ads are unavailable right now. No reward was granted.",
    adNotCompleted: "The ad was not completed. No reward was granted.",
    adBusy: "Please wait until the current ad finishes.",
    resetProgress: "Reset progress",
    resetDialogTitle: "Reset all progress?",
    resetDialogText: "This deletes your best score, stars, upgrades, boosters, skins, daily tasks and any unfinished round. This cannot be undone.",
    resetConfirm: "Reset",
    resetCancel: "Cancel"
  }
};

const boosterInfo = {
  magnetStart: {
    title: "Умный магнит",
    titleEn: "Smart magnet",
    text: "6 секунд притягивает хорошие и золотые мысли, а вредные отталкивает.",
    textEn: "For 6 seconds, attracts good and golden thoughts while pushing harmful ones away.",
    cost: 3
  },
  shield: {
    title: "Щит от плохой мысли",
    titleEn: "Bad thought shield",
    text: "Один раз за раунд блокирует вредную мысль.",
    textEn: "Blocks one harmful thought during the next round.",
    cost: 4
  },
  doubleStart: {
    title: "Звездный старт",
    titleEn: "Star start",
    text: "Следующий раунд начнется с x2 очками на 8 секунд.",
    textEn: "The next round starts with x2 score for 8 seconds.",
    cost: 5
  }
};

const skinInfo = {
  blue: {
    title: "Голубая аура",
    titleEn: "Blue aura",
    cost: 0,
    aura: "rgba(31, 191, 163, 0.5)",
    auraFill: "rgba(255, 255, 255, 0.65)",
    sparkle: "#b9fff3",
    robe: ["#ffffff", "#8ae9ff", "#79a8ff"],
    core: "#58d6ff"
  },
  pink: {
    title: "Розовая аура",
    titleEn: "Pink aura",
    cost: 8,
    aura: "rgba(255, 111, 145, 0.55)",
    auraFill: "rgba(255, 231, 239, 0.72)",
    sparkle: "#ffd1df",
    robe: ["#ffffff", "#ff9dc2", "#cf8cff"],
    core: "#ff7fb1"
  },
  gold: {
    title: "Золотая аура",
    titleEn: "Golden aura",
    cost: 12,
    aura: "rgba(255, 184, 0, 0.58)",
    auraFill: "rgba(255, 246, 190, 0.72)",
    sparkle: "#ffe071",
    robe: ["#ffffff", "#ffd75d", "#ffac4d"],
    core: "#ffc83d"
  },
  cosmic: {
    title: "Космическая аура",
    titleEn: "Cosmic aura",
    cost: 15,
    aura: "rgba(118, 109, 255, 0.56)",
    auraFill: "rgba(230, 230, 255, 0.72)",
    sparkle: "#c5bfff",
    robe: ["#ffffff", "#9ca7ff", "#7a5cff"],
    core: "#8878ff"
  }
};

const upgradeInfo = {
  radius: {
    title: "Радиус втягивания",
    titleEn: "Pull radius",
    text: "Аура достает мысли чуть дальше.",
    textEn: "The aura reaches thoughts a little farther away.",
    max: 5,
    costs: [2, 3, 4, 5, 6]
  },
  bonus: {
    title: "Длительность бонусов",
    titleEn: "Bonus duration",
    text: "Магнит, замедление и двойные очки живут дольше.",
    textEn: "Magnet, slow, and double score last longer.",
    max: 5,
    costs: [2, 3, 4, 5, 6]
  },
  life: {
    title: "Запасное сердце",
    titleEn: "Spare heart",
    text: "Одна дополнительная жизнь в начале игры.",
    textEn: "One extra life at the start of a round.",
    max: 1,
    costs: [5]
  }
};

const taskDefinitions = {
  goodThoughts: { title: "Собери 20 хороших мыслей", titleEn: "Collect 20 good thoughts", target: 20 },
  goldThoughts: { title: "Поймай 2 золотые мысли", titleEn: "Catch 2 golden thoughts", target: 2 },
  combo: { title: "Набери комбо x4", titleEn: "Reach combo x4", target: 4 },
  score: { title: "Заработай 300 очков за раунд", titleEn: "Score 300 points in one round", target: 300 },
  rounds: { title: "Сыграй 3 раунда", titleEn: "Play 3 rounds", target: 3 }
};

let yaSdk = null;
let cloudPlayer = null;
let cloudSaveTimer = 0;
let cloudSaveInFlight = false;
let cloudSavePending = false;
let cloudRetries = 0;
let sdkSettled = false;
let criticalAssetsSettled = false;
let initialUiReady = false;
let loadingReadySent = false;
let audioContext = null;
let vacuumLoop = null;
let bubbleNoiseBuffer = null;
const VACUUM_START_DURATION = 3.2;
let dpr = 1;
let width = 0;
let height = 0;
let lastTime = 0;
let currentScreen = "menu";
let gameplayMarkedActive = false;
let activeRewardedRequest = null;
let rewardedRequestSequence = 0;
let transactionInProgress = false;
const purchaseCooldowns = new Map();
const pressedMovementKeys = new Set();
const systemPauseReasons = new Set();
const MOVEMENT_KEYS = new Map([
  ["ArrowUp", [0, -1]],
  ["ArrowDown", [0, 1]],
  ["ArrowLeft", [-1, 0]],
  ["ArrowRight", [1, 0]],
  ["KeyW", [0, -1]],
  ["KeyS", [0, 1]],
  ["KeyA", [-1, 0]],
  ["KeyD", [1, 0]]
]);
const screenHeadingIds = {
  menu: "menuTitle",
  upgrades: "upgradesTitle",
  game: "gameRoundTitle",
  gameOver: "resultTitle"
};
const screenOpeners = {};
let lastActiveSaveAt = 0;
let activeSaveRevision = 0;
let resetDialogOpener = null;
let progressStorageNeedsRepair = false;
let currentLang = resolveLanguage(new URLSearchParams(window.location.search).get("lang") || navigator.language);
let progress = loadProgress();
ensureDailyState();
if (progressStorageNeedsRepair) {
  progressStorageNeedsRepair = false;
  saveProgress();
}
let game = null;
let backgroundBubbles = [];

async function initializeApplication() {
  await Promise.all([initYandexSdk(), criticalAssetsReady]);
  criticalAssetsSettled = true;
  if (!isVacuumBitmapReady()) diagnostics.assetErrors += 1;
  applyLanguage();
  resizeCanvas();
  renderUpgrades();
  updateMenu();
  // Reload still opens Menu, with an explicit Continue action for a saved run.
  switchScreen("menu", { initial: true });
  bindEvents();
  const menuLayoutObserver = new ResizeObserver(fitMenuToViewport);
  menuLayoutObserver.observe(screens.menu);
  menuLayoutObserver.observe(screens.menu.querySelector('.panel'));
  fitMenuToViewport();
  await new Promise(requestAnimationFrame);
  draw();
  initialUiReady = true;
  // Tell Yandex that loading is complete while the startup lock is still
  // active. The first user-visible frame is released only after this call.
  maybeSignalLoadingReady();
  document.body.removeAttribute("data-starting");
  document.body.removeAttribute("aria-busy");
  document.body.inert = false;
  requestAnimationFrame(loop);
}

initializeApplication().catch((error) => {
  console.error("Application startup failed:", error);
});

/* ---------------------------------------------------------------- language */

function resolveLanguage(lang) {
  const code = String(lang || "ru").toLowerCase().split("-")[0];
  return RU_LANGUAGE_CODES.has(code) ? "ru" : "en";
}

function setLanguage(lang) {
  const nextLang = resolveLanguage(lang);
  if (currentLang === nextLang) return;
  currentLang = nextLang;
  applyLanguage();
  renderUpgrades();
  updateMenu();
  updateSoundControls();
  if (game) updateHud();
}

function tr(key, values = {}) {
  const dictionary = TRANSLATIONS[currentLang] || TRANSLATIONS.ru;
  let value = dictionary[key] || TRANSLATIONS.ru[key] || key;
  Object.entries(values).forEach(([name, replacement]) => {
    value = value.replaceAll(`{${name}}`, replacement);
  });
  return value;
}

function infoTitle(info) {
  return currentLang === "en" && info.titleEn ? info.titleEn : info.title;
}

function infoText(info) {
  return currentLang === "en" && info.textEn ? info.textEn : info.text;
}

function setText(selector, value) {
  const element = document.querySelector(selector);
  if (element) element.textContent = value;
}

function applyLanguage() {
  document.documentElement.lang = currentLang;
  document.title = tr("pageTitle");
  canvas.setAttribute("aria-label", tr("canvasLabel"));

  setText("#menuScreen .eyebrow", tr("menuEyebrow"));
  setText("#menuScreen h1", tr("menuTitle"));
  setText("#menuScreen .lead", tr("menuLead"));
  const bestRow = document.querySelector(".best-row");
  if (bestRow) bestRow.innerHTML = `${tr("bestResult")} <strong id="menuBestScore">${progress.bestScore}</strong>`;
  ui.menuBestScore = document.getElementById("menuBestScore");
  setText("#dailyRewardCard strong", tr("dailyRewardTitle"));
  setText("#playButton", tr("play"));
  setText("#continueButton", tr("continueGame"));
  setText("#upgradesButton", tr("upgrades"));

  setText("#upgradesScreen .eyebrow", tr("workshop"));
  setText("#upgradesScreen h2", tr("upgrades"));
  setText("#boostersTitle", tr("boosters"));
  setText("#boostersNote", tr("boostersLimit"));
  setText("#skinsTitle", tr("skins"));
  setText("#skinsNote", tr("skinsNote"));
  setText(".tasks-panel .tasks-head h3", tr("dailyTasks"));
  setText("#resetProgressButton", tr("resetProgress"));
  setText("#backFromUpgradesButton", tr("back"));

  setText("#gameRoundTitle", tr("gameRoundTitle"));
  setText(".hud-item:nth-child(1) span", tr("score"));
  setText(".hud-item:nth-child(2) span", tr("lives"));
  setText(".hud-item:nth-child(3) span", tr("combo"));
  setText("#gameMenuButton", tr("menu"));
  setText("#bonusPill", tr("bonus"));

  setText("#gameOverScreen .eyebrow", tr("gameOverEyebrow"));
  setText("#gameOverScreen h2", tr("gameOver"));
  setText(".result-grid div:nth-child(1) span", tr("score"));
  setText(".result-grid div:nth-child(2) span", tr("best"));
  setText(".result-grid div:nth-child(3) span", tr("stars"));
  setText("#reviveAdButton", tr("reviveAd"));
  setText("#doubleStarsAdButton", tr("doubleStarsAd"));
  setText("#restartButton", tr("restart"));
  setText("#menuButton", tr("menu"));
  setText("#resetDialogTitle", tr("resetDialogTitle"));
  setText("#resetDialogText", tr("resetDialogText"));
  setText("#resetConfirmButton", tr("resetConfirm"));
  setText("#resetCancelButton", tr("resetCancel"));
  updateSoundControls();
}

/* ------------------------------------------------------- storage utilities */

function storageGet(key) {
  try {
    return window.localStorage.getItem(key);
  } catch (error) {
    return null;
  }
}

function storageSet(key, value) {
  try {
    window.localStorage.setItem(key, value);
    return true;
  } catch (error) {
    diagnostics.storageWriteFailures += 1;
    return false;
  }
}

function storageRemove(key) {
  try {
    window.localStorage.removeItem(key);
  } catch (error) {
    diagnostics.storageWriteFailures += 1;
  }
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function finiteNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function readInt(value, min, max, fallback) {
  if (!finiteNumber(value)) return fallback;
  const rounded = Math.trunc(value);
  if (rounded < min || rounded > max) return clamp(rounded, min, max);
  return rounded;
}

function readFloat(value, min, max, fallback) {
  if (!finiteNumber(value)) return fallback;
  return clamp(value, min, max);
}

function readBool(value, fallback) {
  return typeof value === "boolean" ? value : fallback;
}

function readDateKey(value) {
  return typeof value === "string" && /^\d{4}-\d{2}-\d{2}$/.test(value) ? value : "";
}

/* ------------------------------------------------------------ Yandex SDK */

function maybeSignalLoadingReady() {
  if (loadingReadySent) return;
  if (!sdkSettled || !criticalAssetsSettled || !initialUiReady) return;
  loadingReadySent = true;
  try {
    if (typeof yaSdk?.features?.LoadingAPI?.ready === "function") {
      yaSdk.features.LoadingAPI.ready();
      diagnostics.loadingReadyCalls += 1;
    }
  } catch (error) {
    /* LoadingAPI недоступен — локальный запуск всё равно продолжится. */
  }
}

function markGameplayStart() {
  if (gameplayMarkedActive) return;
  gameplayMarkedActive = true;
  startVacuumLoop();
  try {
    if (typeof yaSdk?.features?.GameplayAPI?.start === "function") {
      yaSdk.features.GameplayAPI.start();
      diagnostics.gameplayStartCalls += 1;
    }
  } catch (error) {
    /* GameplayAPI недоступен — игра продолжается без телеметрии. */
  }
}

function markGameplayStop() {
  if (!gameplayMarkedActive) return;
  gameplayMarkedActive = false;
  stopVacuumLoop();
  try {
    if (typeof yaSdk?.features?.GameplayAPI?.stop === "function") {
      yaSdk.features.GameplayAPI.stop();
      diagnostics.gameplayStopCalls += 1;
    }
  } catch (error) {
    /* GameplayAPI недоступен — игра продолжается без телеметрии. */
  }
}

async function initYandexSdk() {
  if (!window.YaGames || typeof window.YaGames.init !== "function") {
    sdkSettled = true;
    diagnostics.cloudState = "unavailable";
    return;
  }

  try {
    // Do not treat a slow SDK as unavailable: its language must win before access.
    yaSdk = await window.YaGames.init() || null;
  } catch (error) {
    sdkSettled = true;
    diagnostics.cloudState = "unavailable";
    return;
  }
  const platformLanguage = yaSdk?.environment?.i18n?.lang;
  if (platformLanguage) currentLang = resolveLanguage(platformLanguage);
  applyLanguage();
  try {
    if (typeof yaSdk?.on === "function") {
      yaSdk.on("game_api_pause", () => pauseActiveGame("sdk"));
      yaSdk.on("game_api_resume", () => resumeSystemPausedGame("sdk"));
    }
  } catch (error) {
    console.warn("SDK lifecycle subscription unavailable:", error);
  }
  await initCloudSave();
  sdkSettled = true;
}

function withTimeout(promise, timeoutMs) {
  return new Promise((resolve, reject) => {
    let settled = false;
    const timer = window.setTimeout(() => {
      if (settled) return;
      settled = true;
      reject(new Error("timeout"));
    }, timeoutMs);
    Promise.resolve(promise).then(
      (value) => {
        if (settled) return;
        settled = true;
        window.clearTimeout(timer);
        resolve(value);
      },
      (error) => {
        if (settled) return;
        settled = true;
        window.clearTimeout(timer);
        reject(error);
      }
    );
  });
}

/* --------------------------------------------------------------- cloud save
 * Детерминированная merge policy (одна и та же для всех устройств):
 *   1. Облако пустое/невалидное  -> оставляем локальный прогресс и отправляем его.
 *   2. Облако "пустое по смыслу" (нет best/stars/upgrades/скинов/бустеров),
 *      а локально данные есть   -> локальный прогресс НИКОГДА не перезаписывается.
 *   3. revision больше          -> побеждает большая revision.
 *   4. revision равны           -> побеждает больший updatedAt.
 *   5. Полное равенство         -> побеждает локальная копия (стабильный выбор).
 * Активный раунд (thoughtVacuumActive.v1) намеренно local-only:
 * продолжение раунда на другом устройстве не входит в product contract.
 */

async function initCloudSave() {
  if (!yaSdk || typeof yaSdk.getPlayer !== "function") {
    diagnostics.cloudState = "unavailable";
    return;
  }

  let player = null;
  try {
    player = await withTimeout(yaSdk.getPlayer({ scopes: false }), CLOUD_TIMEOUT_MS);
  } catch (error) {
    diagnostics.cloudState = "unavailable";
    return;
  }

  if (!player || typeof player.getData !== "function" || typeof player.setData !== "function") {
    diagnostics.cloudState = "unavailable";
    return;
  }

  cloudPlayer = player;

  let remoteRaw = null;
  try {
    remoteRaw = await withTimeout(player.getData([STORAGE_KEY]), CLOUD_TIMEOUT_MS);
    diagnostics.cloudLoads += 1;
  } catch (error) {
    diagnostics.cloudState = "read-error";
    return;
  }

  diagnostics.cloudState = "ready";
  applyCloudSnapshot(isPlainObject(remoteRaw) ? remoteRaw[STORAGE_KEY] : null);
}

function isMeaningfulProgress(value) {
  if (!value) return false;
  const boosterTotal = value.boosters.magnetStart + value.boosters.shield + value.boosters.doubleStart;
  const upgradeTotal = value.upgrades.radius + value.upgrades.bonus + value.upgrades.life;
  return (
    value.bestScore > 0 ||
    value.stars > 0 ||
    boosterTotal > 0 ||
    upgradeTotal > 0 ||
    value.ownedSkins.length > 1 ||
    value.dailyRewardDate !== "" ||
    value.dailyTasks.some((task) => task.progress > 0 || task.claimed)
  );
}

function applyCloudSnapshot(rawRemote) {
  if (!isPlainObject(rawRemote)) {
    diagnostics.mergeDecision = "local-no-remote";
    scheduleCloudSave(true);
    return;
  }

  const remote = normalizeProgress(rawRemote);
  const localMeaningful = isMeaningfulProgress(progress);
  const remoteMeaningful = isMeaningfulProgress(remote);

  if (!remoteMeaningful && localMeaningful) {
    diagnostics.mergeDecision = "local-remote-empty";
    scheduleCloudSave(true);
    return;
  }

  let adoptRemote = false;
  if (remote.revision > progress.revision) adoptRemote = true;
  else if (remote.revision === progress.revision && remote.updatedAt > progress.updatedAt) adoptRemote = true;

  if (!adoptRemote) {
    diagnostics.mergeDecision = "local-newer";
    scheduleCloudSave(true);
    return;
  }

  diagnostics.mergeDecision = "remote-newer";
  progress = remote;
  ensureDailyState();
  storageSet(STORAGE_KEY, JSON.stringify(progress));
  applyLanguage();
  renderUpgrades();
  updateMenu();
  updateSoundControls();
}

function scheduleCloudSave(immediate = false) {
  if (!cloudPlayer) return;
  cloudSavePending = true;
  if (cloudSaveTimer) window.clearTimeout(cloudSaveTimer);
  cloudSaveTimer = window.setTimeout(flushCloudSave, immediate ? 0 : CLOUD_DEBOUNCE_MS);
}

function flushCloudSave() {
  if (cloudSaveTimer) {
    window.clearTimeout(cloudSaveTimer);
    cloudSaveTimer = 0;
  }
  if (!cloudPlayer || !cloudSavePending || cloudSaveInFlight) return;

  cloudSaveInFlight = true;
  cloudSavePending = false;
  const payload = { [STORAGE_KEY]: JSON.parse(JSON.stringify(progress)) };

  let request = null;
  try {
    request = cloudPlayer.setData(payload, true);
  } catch (error) {
    cloudSaveInFlight = false;
    handleCloudSaveFailure();
    return;
  }

  Promise.resolve(request)
    .then(() => {
      cloudSaveInFlight = false;
      cloudRetries = 0;
      diagnostics.cloudWrites += 1;
      if (cloudSavePending) scheduleCloudSave(true);
    })
    .catch(() => {
      cloudSaveInFlight = false;
      handleCloudSaveFailure();
    });
}

function handleCloudSaveFailure() {
  diagnostics.cloudState = "write-error";
  if (cloudRetries >= CLOUD_MAX_RETRIES) return;
  cloudRetries += 1;
  cloudSavePending = true;
  if (cloudSaveTimer) window.clearTimeout(cloudSaveTimer);
  cloudSaveTimer = window.setTimeout(flushCloudSave, CLOUD_DEBOUNCE_MS * cloudRetries);
}

/* ------------------------------------------------------------- meta save */

function defaultProgress() {
  const today = getTodayKey();
  return {
    version: PROGRESS_VERSION,
    revision: 0,
    updatedAt: 0,
    bestScore: 0,
    stars: 0,
    roundsSinceInterstitial: 0,
    boosters: { magnetStart: 0, shield: 0, doubleStart: 0 },
    ownedSkins: ["blue"],
    activeSkin: "blue",
    dailyRewardDate: "",
    dailyTasksDate: today,
    dailyTasks: createDailyTasks(today),
    dailyTasksCompletedBonusClaimed: false,
    soundMuted: false,
    upgrades: { radius: 0, bonus: 0, life: 0 }
  };
}

function normalizeProgress(parsed) {
  const fallback = defaultProgress();
  if (!isPlainObject(parsed)) return fallback;

  const ownedSkins = normalizeOwnedSkins(parsed.ownedSkins);
  return {
    version: readInt(parsed.version, 0, 1000, PROGRESS_VERSION),
    revision: readInt(parsed.revision, 0, Number.MAX_SAFE_INTEGER, 0),
    updatedAt: readInt(parsed.updatedAt, 0, Number.MAX_SAFE_INTEGER, 0),
    bestScore: readInt(parsed.bestScore, 0, 1e12, 0),
    stars: readInt(parsed.stars, 0, 1e9, 0),
    roundsSinceInterstitial: readInt(parsed.roundsSinceInterstitial, 0, 1e6, 0),
    boosters: normalizeBoosters(parsed.boosters),
    ownedSkins,
    activeSkin: ownedSkins.includes(parsed.activeSkin) ? parsed.activeSkin : "blue",
    dailyRewardDate: readDateKey(parsed.dailyRewardDate),
    dailyTasksDate: readDateKey(parsed.dailyTasksDate),
    dailyTasks: normalizeDailyTasks(parsed.dailyTasks),
    dailyTasksCompletedBonusClaimed: readBool(parsed.dailyTasksCompletedBonusClaimed, false),
    soundMuted: readBool(parsed.soundMuted, false),
    upgrades: {
      radius: readInt(parsed.upgrades?.radius, 0, upgradeInfo.radius.max, 0),
      bonus: readInt(parsed.upgrades?.bonus, 0, upgradeInfo.bonus.max, 0),
      life: readInt(parsed.upgrades?.life, 0, upgradeInfo.life.max, 0)
    }
  };
}

function loadProgress() {
  const raw = storageGet(STORAGE_KEY);
  if (!raw) return defaultProgress();
  try {
    const parsed = JSON.parse(raw);
    const normalized = normalizeProgress(parsed);
    // Любая нормализация должна быть записана обратно сразу, иначе типово
    // повреждённая запись живёт в storage до первого пользовательского save.
    if (!isPlainObject(parsed) || JSON.stringify(normalized) !== JSON.stringify(parsed)) {
      progressStorageNeedsRepair = true;
    }
    return normalized;
  } catch (error) {
    progressStorageNeedsRepair = true;
    return defaultProgress();
  }
}

function saveProgress() {
  progress.version = PROGRESS_VERSION;
  progress.revision = readInt(progress.revision, 0, Number.MAX_SAFE_INTEGER, 0) + 1;
  progress.updatedAt = Date.now();
  storageSet(STORAGE_KEY, JSON.stringify(progress));
  scheduleCloudSave();
}

function normalizeBoosters(boosters) {
  return {
    magnetStart: readInt(boosters?.magnetStart, 0, MAX_BOOSTERS, 0),
    shield: readInt(boosters?.shield, 0, MAX_BOOSTERS, 0),
    doubleStart: readInt(boosters?.doubleStart, 0, MAX_BOOSTERS, 0)
  };
}

function normalizeOwnedSkins(ownedSkins) {
  const owned = Array.isArray(ownedSkins)
    ? ownedSkins.filter((key) => typeof key === "string" && Object.hasOwn(skinInfo, key))
    : [];
  if (!owned.includes("blue")) owned.unshift("blue");
  return [...new Set(owned)];
}

function normalizeDailyTasks(dailyTasks) {
  if (!Array.isArray(dailyTasks)) return [];
  return dailyTasks
    .filter((task) => isPlainObject(task) && typeof task.id === "string" && Object.hasOwn(taskDefinitions, task.id))
    .slice(0, 3)
    .map((task) => ({
      id: task.id,
      progress: readInt(task.progress, 0, taskDefinitions[task.id].target, 0),
      claimed: readBool(task.claimed, false)
    }));
}

/* ------------------------------------------------------------ active save */

function createActiveSnapshot() {
  activeSaveRevision += 1;
  return {
    version: ACTIVE_SAVE_VERSION,
    phase: "running",
    revision: activeSaveRevision,
    updatedAt: Date.now(),
    score: game.score,
    lives: game.lives,
    maxLives: game.maxLives,
    combo: game.combo,
    streak: game.streak,
    maxComboThisRun: game.maxComboThisRun,
    elapsed: game.elapsed,
    spawnTimer: game.spawnTimer,
    slowTimer: game.slowTimer,
    magnetTimer: game.magnetTimer,
    doubleTimer: game.doubleTimer,
    vacuumStartTimer: game.vacuumStartTimer,
    shieldActive: game.shieldActive,
    revivedOnce: game.revivedOnce,
    starsAwarded: game.starsAwarded,
    starsDoubled: game.starsDoubled,
    earnedStarsThisRun: game.earnedStarsThisRun,
    rewardedStarsBonus: game.rewardedStarsBonus,
    interstitialCounted: game.interstitialCounted,
    pausedBySystem: typeof game.pausedBySystem === "string" ? game.pausedBySystem : "",
    player: {
      x: game.player.x,
      y: game.player.y,
      tx: game.player.tx,
      ty: game.player.ty,
      radius: game.player.radius,
      suckRadius: game.player.suckRadius
    },
    thoughts: game.thoughts.slice(0, ACTIVE_SAVE_MAX_THOUGHTS).map((thought) => ({
      x: thought.x,
      y: thought.y,
      vx: thought.vx,
      vy: thought.vy,
      radius: thought.radius,
      type: thought.type,
      emoji: thought.emoji,
      spin: thought.spin,
      spinSpeed: thought.spinSpeed,
      pulse: thought.pulse
    }))
  };
}

function saveActiveRound(force = false) {
  if (!game || game.finished) return;
  const now = Date.now();
  if (!force && now - lastActiveSaveAt < ACTIVE_SAVE_INTERVAL_MS) return;
  lastActiveSaveAt = now;
  if (storageSet(ACTIVE_KEY, JSON.stringify(createActiveSnapshot()))) {
    diagnostics.activeSaveWrites += 1;
  }
}

function clearActiveRound() {
  storageRemove(ACTIVE_KEY);
}

function getResumableActiveRound() {
  const raw = storageGet(ACTIVE_KEY);
  if (!raw) return null;

  const snapshot = parseActiveSnapshot(raw);
  if (!snapshot) {
    clearActiveRound();
    return null;
  }

  return snapshot;
}

function parseActiveSnapshot(raw) {
  let parsed = null;
  try {
    parsed = JSON.parse(raw);
  } catch (error) {
    return null;
  }

  if (!isPlainObject(parsed)) return null;
  if (parsed.version !== ACTIVE_SAVE_VERSION) return null;
  if (parsed.phase !== "running") return null;
  const revision = strictInt(parsed.revision, 1, Number.MAX_SAFE_INTEGER);
  if (revision === null) return null;
  if (!finiteNumber(parsed.updatedAt)) return null;

  const now = Date.now();
  if (parsed.updatedAt > now + ACTIVE_SAVE_FUTURE_SKEW_MS) return null;
  if (now - parsed.updatedAt > ACTIVE_SAVE_TTL_MS) return null;

  const maxLives = strictInt(parsed.maxLives, 1, MAX_LIVES_LIMIT);
  if (maxLives === null) return null;
  const lives = strictInt(parsed.lives, 1, maxLives);
  if (lives === null) return null;
  const combo = strictInt(parsed.combo, 1, MAX_COMBO);
  if (combo === null) return null;
  const maxComboThisRun = strictInt(parsed.maxComboThisRun, combo, MAX_COMBO);
  if (maxComboThisRun === null) return null;
  const streak = strictInt(parsed.streak, 0, 1e7);
  if (streak === null) return null;
  const score = strictNumber(parsed.score, 0, 1e12);
  if (score === null) return null;

  const numericTimers = {};
  for (const key of ["elapsed", "spawnTimer", "slowTimer", "magnetTimer", "doubleTimer", "vacuumStartTimer"]) {
    const value = strictNumber(parsed[key], 0, 1e7);
    if (value === null) return null;
    numericTimers[key] = value;
  }

  const counters = {};
  for (const key of ["earnedStarsThisRun", "rewardedStarsBonus"]) {
    const value = strictInt(parsed[key], 0, 1e9);
    if (value === null) return null;
    counters[key] = value;
  }

  for (const key of ["shieldActive", "revivedOnce", "starsAwarded", "starsDoubled", "interstitialCounted"]) {
    if (typeof parsed[key] !== "boolean") return null;
  }

  if (!isPlainObject(parsed.player)) return null;
  const player = {};
  for (const key of ["x", "y", "tx", "ty"]) {
    const value = strictNumber(parsed.player[key], -1e6, 1e6);
    if (value === null) return null;
    player[key] = value;
  }
  const radius = strictNumber(parsed.player.radius, 1, 1000);
  const suckRadius = strictNumber(parsed.player.suckRadius, 1, 5000);
  if (radius === null || suckRadius === null) return null;
  player.radius = radius;
  player.suckRadius = suckRadius;

  const thoughts = Array.isArray(parsed.thoughts)
    ? parsed.thoughts.filter(isValidThought).slice(0, ACTIVE_SAVE_MAX_THOUGHTS)
    : [];

  return {
    version: ACTIVE_SAVE_VERSION,
    phase: "running",
    revision,
    updatedAt: parsed.updatedAt,
    score,
    lives,
    maxLives,
    combo,
    streak,
    maxComboThisRun,
    ...numericTimers,
    ...counters,
    shieldActive: parsed.shieldActive,
    revivedOnce: parsed.revivedOnce,
    starsAwarded: parsed.starsAwarded,
    starsDoubled: parsed.starsDoubled,
    interstitialCounted: parsed.interstitialCounted,
    pausedBySystem: typeof parsed.pausedBySystem === "string" ? parsed.pausedBySystem : "",
    player,
    thoughts
  };
}

function strictNumber(value, min, max) {
  if (!finiteNumber(value)) return null;
  if (value < min || value > max) return null;
  return value;
}

function strictInt(value, min, max) {
  if (!finiteNumber(value) || !Number.isInteger(value)) return null;
  if (value < min || value > max) return null;
  return value;
}

function isValidThought(thought) {
  if (!isPlainObject(thought)) return false;
  if (!THOUGHT_TYPES.has(thought.type)) return false;
  if (typeof thought.emoji !== "string" || thought.emoji.length === 0 || thought.emoji.length > 8) return false;
  for (const key of ["x", "y", "vx", "vy", "spin", "spinSpeed", "pulse"]) {
    if (!finiteNumber(thought[key])) return false;
  }
  return finiteNumber(thought.radius) && thought.radius > 0 && thought.radius < 500;
}

function restoreActiveRound() {
  const raw = storageGet(ACTIVE_KEY);
  if (!raw) return false;

  const snapshot = parseActiveSnapshot(raw);
  if (!snapshot) {
    clearActiveRound();
    return false;
  }

  const startX = clamp(snapshot.player.x, 20, Math.max(21, width - 20));
  const startY = clamp(snapshot.player.y, 20, Math.max(21, height - 20));

  game = {
    running: true,
    finished: false,
    pausedBySystem: "",
    score: snapshot.score,
    lives: snapshot.lives,
    maxLives: snapshot.maxLives,
    combo: snapshot.combo,
    streak: snapshot.streak,
    spawnTimer: snapshot.spawnTimer,
    elapsed: snapshot.elapsed,
    shake: 0,
    slowTimer: snapshot.slowTimer,
    magnetTimer: snapshot.magnetTimer,
    doubleTimer: snapshot.doubleTimer,
    vacuumStartTimer: snapshot.vacuumStartTimer,
    shieldActive: snapshot.shieldActive,
    revivedOnce: snapshot.revivedOnce,
    starsAwarded: snapshot.starsAwarded,
    starsDoubled: snapshot.starsDoubled,
    earnedStarsThisRun: snapshot.earnedStarsThisRun,
    rewardedStarsBonus: snapshot.rewardedStarsBonus,
    interstitialCounted: snapshot.interstitialCounted,
    maxComboThisRun: snapshot.maxComboThisRun,
    player: {
      x: startX,
      y: startY,
      tx: clamp(snapshot.player.tx, 20, Math.max(21, width - 20)),
      ty: clamp(snapshot.player.ty, 20, Math.max(21, height - 20)),
      radius: snapshot.player.radius,
      suckRadius: snapshot.player.suckRadius
    },
    thoughts: snapshot.thoughts.map((thought) => ({ ...thought })),
    particles: []
  };

  activeSaveRevision = snapshot.revision;
  diagnostics.activeSaveRestores += 1;
  ui.bonusPill.classList.add("hidden");
  saveActiveRound(true);
  return true;
}

/* ---------------------------------------------------------------- lifecycle */

function pauseActiveGame(reason) {
  systemPauseReasons.add(reason);
  if (!game || game.finished) return;
  game.pausedBySystem = reason;
  if (!game.running) return;
  saveActiveRound(true);
  game.running = false;
  game.pausedBySystem = reason;
  pressedMovementKeys.clear();
  stopVacuumLoop(true);
  markGameplayStop();
  if (audioContext && audioContext.state === "running") {
    audioContext.suspend().catch(() => {});
  }
}

function resumeSystemPausedGame(reason) {
  systemPauseReasons.delete(reason);
  if (systemPauseReasons.size || isRewardedLocked() || !game || game.running || game.finished || !game.pausedBySystem || currentScreen !== "game") return;
  game.pausedBySystem = "";
  game.running = true;
  if (!progress.soundMuted && audioContext && audioContext.state === "suspended") {
    audioContext.resume().catch(() => {});
  }
  markGameplayStart();
}

function handleVisibilityChange() {
  if (document.hidden) {
    saveActiveRound(true);
    pauseActiveGame("visibility");
    flushCloudSave();
  } else {
    resumeSystemPausedGame("visibility");
  }
}

function handlePageHide() {
  saveActiveRound(true);
  flushCloudSave();
}

/* ------------------------------------------------------------------- ads */

function showAdNotice(messageKey) {
  if (!ui.adNotice) return;
  ui.adNotice.textContent = messageKey ? tr(messageKey) : "";
  ui.adNotice.classList.toggle("hidden", !messageKey);
}

/**
 * Транзиентное состояние "идёт реклама" помечается aria-busy, а не disabled:
 * кнопка обязана оставаться в tab order и принимать активацию, чтобы попытка
 * запустить второй rewarded была реально перехвачена общим mutex,
 * а не спрятана за неактивным контролом. Фактическая блокировка —
 * activeRewardedRequest, а не состояние DOM.
 */
function setRewardedBusy(busy) {
  [ui.reviveAdButton, ui.doubleStarsAdButton].forEach((button) => {
    if (!button) return;
    button.setAttribute("aria-busy", busy ? "true" : "false");
    button.classList.toggle("is-busy", busy);
  });
}

function isRewardedLocked() {
  return activeRewardedRequest !== null;
}

/**
 * Единственная точка запуска rewarded-рекламы на всю игру.
 * Награда выдаётся ТОЛЬКО из подтверждённого onRewarded активного запроса.
 * Отсутствие SDK/adv/метода, throw, onError и close-до-награды -> fail closed.
 */
function showRewardedAd({ action, onSettled }) {
  if (isRewardedLocked()) {
    showAdNotice("adBusy");
    return false;
  }

  if (!yaSdk || !yaSdk.adv || typeof yaSdk.adv.showRewardedVideo !== "function") {
    showAdNotice("adUnavailable");
    return false;
  }

  const request = {
    game,
    action,
    id: (rewardedRequestSequence += 1),
    rewarded: false,
    settled: false,
    safetyTimer: 0,
    wasRunning: Boolean(game?.running),
    audioWasRunning: Boolean(audioContext && audioContext.state === "running")
  };

  activeRewardedRequest = request;
  diagnostics.rewardedRequests += 1;
  setRewardedBusy(true);
  showAdNotice(null);

  if (game) game.running = false;
  if (request.wasRunning) markGameplayStop();
  if (request.audioWasRunning) audioContext.suspend().catch(() => {});

  const settle = () => {
    if (request.settled) return;
    request.settled = true;
    if (request.safetyTimer) window.clearTimeout(request.safetyTimer);
    if (activeRewardedRequest === request) activeRewardedRequest = null;
    setRewardedBusy(false);

    if (request.audioWasRunning && !systemPauseReasons.size && !progress.soundMuted && audioContext) {
      audioContext.resume().catch(() => {});
    }
    if (request.wasRunning && game === request.game && !game.finished && !systemPauseReasons.size) {
      game.running = true;
      markGameplayStart();
    }
    if (request.rewarded) diagnostics.rewardedRewards += 1;
    // A late ad callback belongs only to the round which requested it.
    if (game === request.game) onSettled(request.rewarded);
  };

  const grantReward = () => {
    if (request.settled || request.rewarded) return;
    request.rewarded = true;
  };

  // Страховочный таймер освобождает общий mutex, если платформа не прислала
  // ни onClose, ни onError. Награду он никогда не выдаёт.
  request.safetyTimer = window.setTimeout(settle, REWARDED_SAFETY_TIMEOUT_MS);

  try {
    yaSdk.adv.showRewardedVideo({
      callbacks: {
        onOpen: () => {},
        onRewarded: grantReward,
        onClose: settle,
        onError: () => settle()
      }
    });
  } catch (error) {
    settle();
  }

  return true;
}

function showFullscreenAd(onClose) {
  if (systemPauseReasons.has("fullscreen")) return;
  systemPauseReasons.add("fullscreen");
  const adGame = game;
  const wasRunning = Boolean(game?.running);
  const audioWasRunning = Boolean(audioContext && audioContext.state === "running");
  let closed = false;

  if (game) {
    game.running = false;
    if (!game.finished) game.pausedBySystem = "fullscreen";
  }
  if (wasRunning) markGameplayStop();
  if (audioWasRunning) audioContext.suspend().catch(() => {});

  const finish = () => {
    if (closed) return;
    closed = true;
    systemPauseReasons.delete("fullscreen");
    if (audioWasRunning && !systemPauseReasons.size && !progress.soundMuted && audioContext) audioContext.resume().catch(() => {});
    if (wasRunning && game === adGame && !game.finished && !systemPauseReasons.size) {
      game.running = true;
      game.pausedBySystem = "";
      markGameplayStart();
    }
    if (typeof onClose === "function") onClose();
  };

  if (!yaSdk || !yaSdk.adv || typeof yaSdk.adv.showFullscreenAdv !== "function") {
    finish();
    return;
  }

  try {
    yaSdk.adv.showFullscreenAdv({
      callbacks: {
        onOpen: () => {},
        onClose: finish,
        onError: finish
      }
    });
  } catch (error) {
    finish();
  }
}

function reviveWithAd() {
  if (!game || game.running || game.revivedOnce || !game.finished) return;
  if (isRewardedLocked()) {
    showAdNotice("adBusy");
    return;
  }

  const started = showRewardedAd({
    action: "revive",
    onSettled: (rewarded) => {
      if (!rewarded) {
        showAdNotice("adNotCompleted");
        updateRewardButtons();
        return;
      }
      applyRevive();
    }
  });

  if (!started) updateRewardButtons();
}

function applyRevive() {
  if (!game || game.revivedOnce) return;
  showAdNotice(null);
  game.revivedOnce = true;
  game.finished = false;
  game.running = systemPauseReasons.size === 0;
  game.pausedBySystem = systemPauseReasons.values().next().value || "";
  game.lives = 1;
  game.combo = 1;
  game.streak = 0;
  game.shake = 0;
  game.vacuumStartTimer = VACUUM_START_DURATION;
  game.thoughts = [];
  game.particles = [];
  updateHud();
  updateRewardButtons();
  switchScreen("game");
  if (game.running) markGameplayStart();
  saveActiveRound(true);
  playSound("buy");
}

function doubleStarsWithAd() {
  if (!game || game.running || game.starsDoubled || game.earnedStarsThisRun <= 0) return;
  if (isRewardedLocked()) {
    showAdNotice("adBusy");
    return;
  }

  const started = showRewardedAd({
    action: "doubleStars",
    onSettled: (rewarded) => {
      if (!rewarded) {
        showAdNotice("adNotCompleted");
        updateRewardButtons();
        return;
      }
      applyDoubleStars();
    }
  });

  if (!started) updateRewardButtons();
}

function applyDoubleStars() {
  if (!game || game.starsDoubled || game.earnedStarsThisRun <= 0) return;
  showAdNotice(null);
  const bonusStars = game.earnedStarsThisRun;
  game.starsDoubled = true;
  game.rewardedStarsBonus += bonusStars;
  progress.stars = Math.max(0, progress.stars + bonusStars);
  saveProgress();
  ui.earnedStars.textContent = getResultStarsTotal();
  updateRewardButtons();
  updateMenu();
  renderUpgrades();
  playSound("gold");
}

function updateRewardButtons() {
  if (!game || game.running) {
    ui.reviveAdButton.classList.add("hidden");
    ui.doubleStarsAdButton.classList.add("hidden");
    return;
  }

  const locked = isRewardedLocked();
  ui.reviveAdButton.classList.toggle("hidden", game.revivedOnce);
  ui.reviveAdButton.disabled = game.revivedOnce;

  const canDoubleStars = game.earnedStarsThisRun > 0 && !game.starsDoubled;
  ui.doubleStarsAdButton.classList.toggle("hidden", !canDoubleStars);
  ui.doubleStarsAdButton.disabled = !canDoubleStars;
  setRewardedBusy(locked);
}

function getResultStarsTotal() {
  if (!game) return 0;
  return game.earnedStarsThisRun + (game.rewardedStarsBonus || 0);
}

/* ------------------------------------------------------------------ events */

function bindEvents() {
  window.addEventListener("resize", resizeCanvas);
  document.addEventListener("visibilitychange", handleVisibilityChange);
  window.addEventListener("blur", () => {
    saveActiveRound(true);
    pauseActiveGame("window");
  });
  window.addEventListener("focus", () => resumeSystemPausedGame("window"));
  window.addEventListener("pagehide", handlePageHide);
  window.addEventListener("beforeunload", handlePageHide);

  // Игра занимает всю страницу: блокируем браузерные жесты во всех её
  // состояниях, чтобы правый клик, выделение текста и drag не перехватывали
  // управление игрой и не показывали системное меню браузера.
  document.addEventListener("contextmenu", suppressBrowserGesture);
  document.addEventListener("selectstart", suppressBrowserGesture);
  document.addEventListener("dragstart", suppressBrowserGesture);
  document.addEventListener("touchmove", suppressGameplayTouchMove, { passive: false });
  window.addEventListener("pointermove", handlePointerMove, { passive: false });
  window.addEventListener("pointerdown", (event) => {
    suppressGameplayPointerEvent(event);
    unlockAudio();
    updatePointer(event);
  }, { passive: false });
  window.addEventListener("keydown", handleKeyDown, { passive: false });
  window.addEventListener("keyup", handleKeyUp);

  ui.continueButton.addEventListener("click", () => continueSavedGame());
  ui.playButton.addEventListener("click", () => startGame());
  ui.dailyRewardButton.addEventListener("click", () => claimDailyReward());
  document.getElementById("restartButton").addEventListener("click", () => restartGameWithOptionalAd());
  ui.reviveAdButton.addEventListener("click", () => reviveWithAd());
  ui.doubleStarsAdButton.addEventListener("click", () => doubleStarsWithAd());
  ui.gameMenuButton.addEventListener("click", () => returnToMenuFromGame());
  ui.soundToggleButton.addEventListener("click", () => toggleSound());
  updateSoundControls();

  document.getElementById("menuButton").addEventListener("click", () => {
    updateMenu();
    switchScreen("menu");
  });
  document.getElementById("upgradesButton").addEventListener("click", (event) => {
    renderUpgrades();
    switchScreen("upgrades", { opener: event.currentTarget });
  });
  document.getElementById("backFromUpgradesButton").addEventListener("click", () => {
    updateMenu();
    switchScreen("menu", { focusTarget: screenOpeners.upgrades });
  });

  if (ui.resetProgressButton) ui.resetProgressButton.addEventListener("click", () => openResetDialog());
  if (ui.resetCancelButton) ui.resetCancelButton.addEventListener("click", () => closeResetDialog("cancel"));
  if (ui.resetConfirmButton) ui.resetConfirmButton.addEventListener("click", () => confirmReset());
  if (ui.resetDialog) {
    ui.resetDialog.addEventListener("close", () => {
      if (resetDialogOpener && document.contains(resetDialogOpener)) {
        try {
          resetDialogOpener.focus({ preventScroll: true });
        } catch (error) {
          resetDialogOpener.focus();
        }
      }
      resetDialogOpener = null;
    });
    ui.resetDialog.addEventListener("cancel", (event) => {
      event.preventDefault();
      closeResetDialog("cancel");
    });
  }
}

function suppressBrowserGesture(event) {
  if (event.cancelable) event.preventDefault();
  return false;
}

function suppressGameplayTouchMove(event) {
  if (currentScreen !== "game" || !event.cancelable) return;
  if (event.target instanceof Element && event.target.closest("button")) return;
  event.preventDefault();
}

function suppressGameplayPointerEvent(event) {
  if (!game || !game.running || !event.cancelable) return;
  if (event.target instanceof Element && event.target.closest("button")) return;
  event.preventDefault();
}

function handlePointerMove(event) {
  suppressGameplayPointerEvent(event);
  updatePointer(event);
}

function handleKeyDown(event) {
  if (ui.resetDialog?.open) return;

  if (event.key === "Escape" && currentScreen === "game" && game) {
    event.preventDefault();
    returnToMenuFromGame();
    return;
  }

  if (!MOVEMENT_KEYS.has(event.code)) return;
  if (currentScreen !== "game" || !game || !game.running) return;

  pressedMovementKeys.add(event.code);
  if (event.code.startsWith("Arrow") && event.cancelable) event.preventDefault();
}

function handleKeyUp(event) {
  pressedMovementKeys.delete(event.code);
}

function applyKeyboardMovement(dt) {
  if (!pressedMovementKeys.size || !game || !game.running) return;

  let dx = 0;
  let dy = 0;
  for (const code of pressedMovementKeys) {
    const vector = MOVEMENT_KEYS.get(code);
    if (!vector) continue;
    dx += vector[0];
    dy += vector[1];
  }
  if (dx === 0 && dy === 0) return;

  const length = Math.hypot(dx, dy) || 1;
  const player = game.player;
  player.tx = clamp(player.tx + (dx / length) * KEYBOARD_SPEED * dt, 20, Math.max(21, width - 20));
  player.ty = clamp(player.ty + (dy / length) * KEYBOARD_SPEED * dt, 20, Math.max(21, height - 20));
}

/* ----------------------------------------------------------------- screens */

function resizeCanvas() {
  dpr = Math.min(2, window.devicePixelRatio || 1);
  width = Math.max(1, window.innerWidth);
  height = Math.max(1, window.innerHeight);
  canvas.width = Math.floor(width * dpr);
  canvas.height = Math.floor(height * dpr);
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  if (!backgroundBubbles.length) {
    backgroundBubbles = Array.from({ length: 24 }, createBackgroundBubble);
  }
}

function fitMenuToViewport() {
  const screen = screens.menu;
  const panel = screen.querySelector('.panel');
  const styles = getComputedStyle(screen);
  const top = parseFloat(styles.paddingTop);
  const bottom = parseFloat(styles.paddingBottom);
  const left = parseFloat(styles.paddingLeft);
  const right = parseFloat(styles.paddingRight);
  const available = Math.max(1, screen.clientHeight - top - bottom);
  panel.style.setProperty('--menu-scale', Math.min(1, available / Math.max(1, panel.offsetHeight)));
  panel.style.top = `${top + available / 2}px`;
  panel.style.left = `${left + (screen.clientWidth - left - right) / 2}px`;
}

function switchScreen(name, options = {}) {
  const previous = currentScreen;
  currentScreen = name;
  if (options.opener) screenOpeners[name] = options.opener;
  if (name !== "gameOver") showAdNotice(null);

  Object.entries(screens).forEach(([screenName, element]) => {
    const isActive = screenName === name;
    element.classList.toggle("screen-active", isActive);
    if (isActive) {
      element.removeAttribute("inert");
      element.removeAttribute("aria-hidden");
    } else {
      element.setAttribute("inert", "");
      element.setAttribute("aria-hidden", "true");
    }
  });

  if (options.initial) return;
  if (previous === name && !options.focusTarget) return;
  moveFocusIntoScreen(name, options.focusTarget);
}

function moveFocusIntoScreen(name, explicitTarget) {
  const screen = screens[name];
  if (!screen) return;

  // Класс переключён в этом же такте: без принудительного пересчёта стилей
  // экран ещё считается visibility:hidden и focus() молча не срабатывает.
  if (getComputedStyle(screen).visibility !== "visible") return;

  let target = null;
  if (explicitTarget && screen.contains(explicitTarget) && !explicitTarget.disabled) {
    target = explicitTarget;
  }
  if (!target) target = document.getElementById(screenHeadingIds[name]);
  if (!target || !screen.contains(target)) target = screen.querySelector("button:not([disabled])");
  if (!target) return;

  try {
    target.focus({ preventScroll: true });
  } catch (error) {
    target.focus();
  }
}

/* -------------------------------------------------------------- game flow */

function startGame() {
  if (vacuumPlayerImage.complete && vacuumPlayerImage.naturalWidth > 0) {
    vacuumPlayerImageLoaded = true;
  }

  // Явный запуск нового раунда всегда отбрасывает сохранённый незавершённый
  // раунд, чтобы кнопки «Начать заново» и «Продолжить игру» не пересекались.
  clearActiveRound();
  ensureDailyState();
  unlockAudio();
  const extraLife = progress.upgrades.life > 0 ? 1 : 0;
  const startX = width * 0.5;
  const startY = height * 0.58;

  game = {
    running: systemPauseReasons.size === 0,
    finished: false,
    pausedBySystem: systemPauseReasons.values().next().value || "",
    score: 0,
    lives: 3 + extraLife,
    maxLives: 3 + extraLife,
    combo: 1,
    streak: 0,
    spawnTimer: 0.4,
    elapsed: 0,
    shake: 0,
    slowTimer: 0,
    magnetTimer: 0,
    doubleTimer: 0,
    vacuumStartTimer: VACUUM_START_DURATION,
    shieldActive: false,
    revivedOnce: false,
    starsAwarded: false,
    starsDoubled: false,
    earnedStarsThisRun: 0,
    rewardedStarsBonus: 0,
    interstitialCounted: false,
    maxComboThisRun: 1,
    player: {
      x: startX,
      y: startY,
      tx: startX,
      ty: startY,
      radius: 36,
      suckRadius: 86 + progress.upgrades.radius * 13
    },
    thoughts: [],
    particles: []
  };

  applyStartingBoosters();
  pressedMovementKeys.clear();
  activeSaveRevision = 0;
  ui.bonusPill.classList.add("hidden");
  showAdNotice(null);
  updateHud();
  switchScreen("game");
  if (game.running) markGameplayStart();
  saveActiveRound(true);
}

function continueSavedGame() {
  if (game && !game.finished) return;
  if (!restoreActiveRound()) {
    updateMenu();
    return;
  }

  game.running = systemPauseReasons.size === 0;
  game.pausedBySystem = systemPauseReasons.values().next().value || "";

  unlockAudio();
  updateHud();
  updateRewardButtons();
  switchScreen("game");
  if (game.running) markGameplayStart();
}

function returnToMenuFromGame() {
  saveActiveRound(true);
  markGameplayStop();
  if (game) {
    game.running = false;
    game.finished = true;
  }
  game = null;
  pressedMovementKeys.clear();
  ui.bonusPill.classList.add("hidden");
  updateMenu();
  switchScreen("menu");
}

function restartGameWithOptionalAd() {
  if (progress.roundsSinceInterstitial >= 3) {
    progress.roundsSinceInterstitial = 0;
    saveProgress();
    showFullscreenAd(() => startGame());
    return;
  }

  startGame();
}

function endGame() {
  if (!game || !game.running) return;
  markGameplayStop();
  game.running = false;
  game.finished = true;
  pressedMovementKeys.clear();

  // Активный ключ очищается ДО показа Result, чтобы reload на Result
  // не мог восстановить завершённый раунд и повторно начислить награды.
  clearActiveRound();

  if (!game.interstitialCounted) {
    progress.roundsSinceInterstitial += 1;
    addTaskProgress("rounds", 1);
    game.interstitialCounted = true;
  }

  addTaskProgress("score", game.score);
  addTaskProgress("combo", game.maxComboThisRun);

  const totalEarned = Math.floor(game.score / 100);
  const earned = Math.max(0, totalEarned - game.earnedStarsThisRun);
  game.earnedStarsThisRun += earned;
  game.starsAwarded = true;
  progress.stars = Math.max(0, progress.stars + earned);
  progress.bestScore = Math.max(progress.bestScore, game.score);
  saveProgress();

  ui.finalScore.textContent = game.score;
  ui.finalBestScore.textContent = progress.bestScore;
  ui.earnedStars.textContent = getResultStarsTotal();
  showAdNotice(null);
  updateRewardButtons();
  updateMenu();
  renderUpgrades();
  switchScreen("gameOver");
  playSound("over");
}

function updatePointer(event) {
  if (!game || !game.running) return;
  game.player.tx = clamp(event.clientX, 20, Math.max(21, width - 20));
  game.player.ty = clamp(event.clientY, 20, Math.max(21, height - 20));
}

function loop(time) {
  const dt = Math.min(0.033, (time - lastTime) / 1000 || 0.016);
  lastTime = time;

  updateBackground(dt);
  if (game && game.running) updateGame(dt);
  draw();

  requestAnimationFrame(loop);
}

function updateGame(dt) {
  game.elapsed += dt;
  game.shake = Math.max(0, game.shake - dt * 18);
  game.slowTimer = Math.max(0, game.slowTimer - dt);
  game.magnetTimer = Math.max(0, game.magnetTimer - dt);
  game.doubleTimer = Math.max(0, game.doubleTimer - dt);
  game.vacuumStartTimer = Math.max(0, game.vacuumStartTimer - dt);

  applyKeyboardMovement(dt);

  const player = game.player;
  const follow = 1 - Math.pow(0.0009, dt);
  player.x += (player.tx - player.x) * follow;
  player.y += (player.ty - player.y) * follow;

  game.spawnTimer -= dt;
  if (game.spawnTimer <= 0) {
    spawnThought();
    const pace = Math.max(0.38, 0.95 - game.elapsed * 0.012);
    game.spawnTimer = random(pace * 0.55, pace * 1.1);
  }

  for (let i = game.thoughts.length - 1; i >= 0; i -= 1) {
    const thought = game.thoughts[i];
    const speedScale = game.slowTimer > 0 && thought.type !== "gold" ? 0.48 : 1;

    thought.x += thought.vx * dt * speedScale;
    thought.y += thought.vy * dt * speedScale;
    thought.spin += thought.spinSpeed * dt;
    thought.pulse += dt * 5;

    const dx = player.x - thought.x;
    const dy = player.y - thought.y;
    const dist = Math.hypot(dx, dy) || 1;
    const pullRadius = player.suckRadius + (game.magnetTimer > 0 ? 95 : 0);

    if (dist < pullRadius) {
      const influence = 1 - dist / pullRadius;
      if (thought.type === "bad" && game.magnetTimer > 0) {
        const repel = influence * 940;
        thought.vx -= (dx / dist) * repel * dt;
        thought.vy -= (dy / dist) * repel * dt;
      } else if (thought.type !== "bad") {
        const pull = influence * (game.magnetTimer > 0 ? 860 : 500);
        thought.vx += (dx / dist) * pull * dt;
        thought.vy += (dy / dist) * pull * dt;
      }
    }

    if (dist < player.radius + thought.radius * 0.65) {
      game.thoughts.splice(i, 1);
      collectThought(thought);
      if (!game || !game.running) return;
      continue;
    }

    if (thought.x < -100 || thought.x > width + 100 || thought.y < -100 || thought.y > height + 100) {
      game.thoughts.splice(i, 1);
    }
  }

  updateParticles(dt);
  updateHud();
  saveActiveRound();
}

function spawnThought() {
  const side = Math.floor(random(0, 4));
  const padding = 54;
  let x = 0;
  let y = 0;

  if (side === 0) {
    x = random(-padding, 0);
    y = random(40, height - 40);
  } else if (side === 1) {
    x = random(width, width + padding);
    y = random(40, height - 40);
  } else if (side === 2) {
    x = random(40, width - 40);
    y = random(-padding, 0);
  } else {
    x = random(40, width - 40);
    y = random(height, height + padding);
  }

  const targetX = random(width * 0.16, width * 0.84);
  const targetY = random(height * 0.16, height * 0.84);
  const angle = Math.atan2(targetY - y, targetX - x) + random(-0.65, 0.65);
  const speed = random(60, 128) + Math.min(70, game.elapsed * 2);
  const roll = Math.random();
  const type = roll < 0.14 ? "bad" : roll > 0.92 ? "gold" : roll > 0.87 ? "rainbow" : "good";
  const emojis = type === "bad"
    ? BAD_EMOJIS
    : type === "gold"
      ? GOLD_EMOJIS
      : type === "rainbow"
        ? RAINBOW_EMOJIS
        : GOOD_EMOJIS;
  if (type === "rainbow") diagnostics.rainbowSpawns += 1;

  game.thoughts.push({
    x,
    y,
    vx: Math.cos(angle) * speed,
    vy: Math.sin(angle) * speed,
    radius: type === "gold" ? 25 : type === "rainbow" ? 24 : 22,
    type,
    emoji: pick(emojis),
    spin: random(0, Math.PI * 2),
    spinSpeed: random(-1.2, 1.2),
    pulse: random(0, Math.PI * 2)
  });
}

function collectThought(thought) {
  playSound("pop");

  if (thought.type === "bad") {
    if (game.shieldActive) {
      game.shieldActive = false;
      game.combo = 1;
      game.streak = 0;
      game.shake = 0.45;
      burst(thought.x, thought.y, "#b9fff3", 22);
      playSound("gold");
      saveActiveRound(true);
      return;
    }

    game.lives -= 1;
    game.combo = 1;
    game.streak = 0;
    game.shake = 1;
    burst(thought.x, thought.y, "#ff5b6e", 18);
    playSound("bad");
    if (game.lives <= 0) {
      endGame();
      return;
    }
    saveActiveRound(true);
    return;
  }

  let points = thought.type === "gold" ? 50 : thought.type === "rainbow" ? 25 : 10;
  if (game.doubleTimer > 0) points *= 2;
  points *= game.combo;
  game.score += points;
  if (thought.type === "rainbow") diagnostics.lastRainbowPoints = points;

  if (thought.type === "good" || thought.type === "rainbow") {
    if (thought.type === "rainbow") diagnostics.rainbowCollections += 1;
    addTaskProgress("goodThoughts", 1);
    game.streak += 1;
    if (game.streak % 5 === 0) {
      game.combo = Math.min(MAX_COMBO, game.combo + 1);
      game.maxComboThisRun = Math.max(game.maxComboThisRun, game.combo);
      addTaskProgress("combo", game.combo);
      playSound("combo");
      saveActiveRound(true);
    } else {
      playSound("good");
    }
    burst(thought.x, thought.y, thought.type === "rainbow" ? "#8878ff" : "#7ee7c8", thought.type === "rainbow" ? 20 : 14);
  } else {
    addTaskProgress("goldThoughts", 1);
    applyRandomBonus();
    burst(thought.x, thought.y, "#ffd34f", 24);
    playSound("gold");
    saveActiveRound(true);
  }
}

function applyRandomBonus() {
  const bonusDuration = 6 + progress.upgrades.bonus * 1.2;
  const bonus = pick(["magnet", "slow", "double"]);

  if (bonus === "magnet") game.magnetTimer = bonusDuration;
  if (bonus === "slow") game.slowTimer = bonusDuration;
  if (bonus === "double") game.doubleTimer = bonusDuration;
}

function burst(x, y, color, count) {
  for (let i = 0; i < count; i += 1) {
    const angle = random(0, Math.PI * 2);
    const speed = random(50, 230);
    game.particles.push({
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: random(0.35, 0.8),
      maxLife: 0.8,
      size: random(3, 8),
      color
    });
  }
}

function updateParticles(dt) {
  for (let i = game.particles.length - 1; i >= 0; i -= 1) {
    const particle = game.particles[i];
    particle.life -= dt;
    particle.x += particle.vx * dt;
    particle.y += particle.vy * dt;
    particle.vy += 120 * dt;
    particle.vx *= 0.985;
    if (particle.life <= 0) game.particles.splice(i, 1);
  }
}

function updateBackground(dt) {
  for (const bubble of backgroundBubbles) {
    bubble.x += bubble.vx * dt;
    bubble.y += bubble.vy * dt;
    bubble.wobble += dt;
    if (bubble.x < -80) bubble.x = width + 80;
    if (bubble.x > width + 80) bubble.x = -80;
    if (bubble.y < -80) bubble.y = height + 80;
    if (bubble.y > height + 80) bubble.y = -80;
  }
}

function updateHud() {
  if (!game) return;
  ui.hudScore.textContent = game.score;
  ui.hudLives.textContent = "♥".repeat(Math.max(0, game.lives));
  ui.hudCombo.textContent = `x${game.combo}`;

  const activeBonus = getActiveBonusText();
  ui.bonusPill.textContent = activeBonus;
  ui.bonusPill.classList.toggle("hidden", !activeBonus);
}

function getActiveBonusText() {
  if (!game) return "";
  const active = [];
  if (game.magnetTimer > 0) active.push(`${tr("smartMagnet")} ${Math.ceil(game.magnetTimer)}s`);
  if (game.slowTimer > 0) active.push(`${tr("slow")} ${Math.ceil(game.slowTimer)}s`);
  if (game.doubleTimer > 0) active.push(`x2 ${Math.ceil(game.doubleTimer)}s`);
  if (game.shieldActive) active.push(tr("shield"));
  return active.join(" · ");
}

function updateMenu() {
  ensureDailyState();
  ui.menuBestScore.textContent = progress.bestScore;
  renderDailyReward();

  const hasResumableRound = Boolean(getResumableActiveRound());
  screens.menu.classList.toggle("has-resumable-round", hasResumableRound);
  if (ui.continueButton) {
    ui.continueButton.classList.toggle("hidden", !hasResumableRound);
    ui.continueButton.setAttribute("aria-hidden", String(!hasResumableRound));
  }
  if (ui.playButton) {
    ui.playButton.textContent = hasResumableRound ? tr("newGame") : tr("play");
    ui.playButton.classList.toggle("primary-button", !hasResumableRound);
    ui.playButton.classList.toggle("secondary-button", hasResumableRound);
  }
}

/* ------------------------------------------------------- shop and dailies */

function beginTransaction(key) {
  if (transactionInProgress) return false;
  const now = Date.now();
  if (now < (purchaseCooldowns.get(key) || 0)) return false;
  transactionInProgress = true;
  return true;
}

function endTransaction(key, committed) {
  transactionInProgress = false;
  if (committed) purchaseCooldowns.set(key, Date.now() + PURCHASE_COOLDOWN_MS);
}

function renderUpgrades() {
  ensureDailyState();
  ui.starsCount.textContent = progress.stars;
  ui.upgradesList.innerHTML = "";
  ui.boostersList.innerHTML = "";
  ui.skinsList.innerHTML = "";
  ui.dailyTasksList.innerHTML = "";

  Object.entries(upgradeInfo).forEach(([key, info]) => {
    const level = progress.upgrades[key];
    const cost = info.costs[level] || 0;
    const isMax = level >= info.max;
    const card = document.createElement("article");
    card.className = "upgrade-card";

    const text = document.createElement("div");
    text.innerHTML = `<h3>${infoTitle(info)} ${level}/${info.max}</h3><p>${infoText(info)}</p>`;

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = isMax ? tr("max") : `★ ${cost}`;
    button.disabled = isMax || progress.stars < cost;
    button.addEventListener("click", () => buyUpgrade(key));

    card.append(text, button);
    ui.upgradesList.append(card);
  });

  Object.entries(boosterInfo).forEach(([key, info]) => {
    const count = progress.boosters[key] || 0;
    const card = document.createElement("article");
    card.className = "store-card";

    const preview = document.createElement("div");
    preview.className = "store-preview";
    preview.style.background = key === "magnetStart" ? "#c8fff2" : key === "shield" ? "#b9d7ff" : "#fff1a8";

    const text = document.createElement("div");
    text.innerHTML = `<strong>${infoTitle(info)}</strong><span>${infoText(info)} ${tr("ownedCount", { count, max: MAX_BOOSTERS })}</span>`;

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = count >= MAX_BOOSTERS ? tr("max") : `★ ${info.cost}`;
    button.disabled = count >= MAX_BOOSTERS || progress.stars < info.cost;
    button.addEventListener("click", () => buyBooster(key));

    card.append(preview, text, button);
    ui.boostersList.append(card);
  });

  Object.entries(skinInfo).forEach(([key, info]) => {
    const owned = progress.ownedSkins.includes(key);
    const selected = progress.activeSkin === key;
    const card = document.createElement("article");
    card.className = "store-card";

    const preview = document.createElement("div");
    preview.className = "store-preview";
    preview.style.background = `linear-gradient(135deg, ${info.robe[1]}, ${info.robe[2]})`;

    const text = document.createElement("div");
    text.innerHTML = `<strong>${infoTitle(info)}</strong><span>${owned ? tr("ownedForever") : tr("price", { cost: info.cost })}</span>`;

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = selected ? tr("selected") : owned ? tr("select") : `★ ${info.cost}`;
    // Скины ведут себя как единая toggle-группа: ровно один owned скин выбран.
    button.setAttribute("aria-pressed", selected ? "true" : "false");
    button.disabled = selected || (!owned && progress.stars < info.cost);
    button.addEventListener("click", () => buyOrSelectSkin(key));

    card.append(preview, text, button);
    ui.skinsList.append(card);
  });

  progress.dailyTasks.forEach((task) => {
    const info = taskDefinitions[task.id];
    if (!info) return;

    const current = Math.min(task.progress, info.target);
    const isDone = current >= info.target;
    const card = document.createElement("article");
    card.className = "task-card";

    const text = document.createElement("div");
    text.innerHTML = `<strong>${infoTitle(info)}</strong><span>${current}/${info.target} · ${tr("reward", { value: DAILY_TASK_REWARD })}</span>`;

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = task.claimed ? tr("done") : isDone ? tr("claim") : `${current}/${info.target}`;
    button.disabled = task.claimed || !isDone;
    button.addEventListener("click", () => claimTaskReward(task.id));

    card.append(text, button);
    ui.dailyTasksList.append(card);
  });

  const allClaimed = progress.dailyTasks.length > 0 && progress.dailyTasks.every((task) => task.claimed);
  if (allClaimed && !progress.dailyTasksCompletedBonusClaimed) {
    progress.stars = Math.max(0, progress.stars + DAILY_ALL_TASKS_REWARD);
    progress.dailyTasksCompletedBonusClaimed = true;
    saveProgress();
    ui.starsCount.textContent = progress.stars;
    playSound("gold");
  }

  ui.tasksBonusText.textContent = progress.dailyTasksCompletedBonusClaimed
    ? tr("allTasksClaimed")
    : tr("allTasksBonus", { value: DAILY_ALL_TASKS_REWARD });
}

function buyUpgrade(key) {
  const info = upgradeInfo[key];
  if (!info) return;

  const transactionKey = `upgrade:${key}`;
  if (!beginTransaction(transactionKey)) return;
  let committed = false;

  try {
    const level = readInt(progress.upgrades[key], 0, info.max, 0);
    const cost = info.costs[level] || 0;
    if (level >= info.max || cost <= 0 || progress.stars < cost) return;

    progress.stars = Math.max(0, progress.stars - cost);
    progress.upgrades[key] = level + 1;
    committed = true;
    saveProgress();
    renderUpgrades();
    playSound("buy");
  } finally {
    endTransaction(transactionKey, committed);
  }
}

function buyBooster(key) {
  const info = boosterInfo[key];
  if (!info) return;

  const transactionKey = `booster:${key}`;
  if (!beginTransaction(transactionKey)) return;
  let committed = false;

  try {
    const count = readInt(progress.boosters[key], 0, MAX_BOOSTERS, 0);
    if (count >= MAX_BOOSTERS || progress.stars < info.cost) return;

    progress.stars = Math.max(0, progress.stars - info.cost);
    progress.boosters[key] = count + 1;
    committed = true;
    saveProgress();
    renderUpgrades();
    playSound("buy");
  } finally {
    endTransaction(transactionKey, committed);
  }
}

function buyOrSelectSkin(key) {
  const info = skinInfo[key];
  if (!info) return;

  const transactionKey = `skin:${key}`;
  if (!beginTransaction(transactionKey)) return;
  let committed = false;

  try {
    if (progress.ownedSkins.includes(key)) {
      // Выбор уже купленного скина ничего не списывает и идемпотентен по своей природе
      // (повторный выбор того же скина — no-op), поэтому антидребезг покупок к нему не применяется.
      if (progress.activeSkin === key) return;
      progress.activeSkin = key;
      saveProgress();
      renderUpgrades();
      playSound("buy");
      return;
    }

    if (progress.stars < info.cost) return;

    progress.stars = Math.max(0, progress.stars - info.cost);
    progress.ownedSkins.push(key);
    progress.activeSkin = key;
    committed = true;
    saveProgress();
    renderUpgrades();
    playSound("gold");
  } finally {
    endTransaction(transactionKey, committed);
  }
}

function applyStartingBoosters() {
  let changed = false;

  if (progress.boosters.magnetStart > 0) {
    progress.boosters.magnetStart -= 1;
    game.magnetTimer = Math.max(game.magnetTimer, 6);
    changed = true;
  }

  if (progress.boosters.doubleStart > 0) {
    progress.boosters.doubleStart -= 1;
    game.doubleTimer = Math.max(game.doubleTimer, 8);
    changed = true;
  }

  if (progress.boosters.shield > 0) {
    progress.boosters.shield -= 1;
    game.shieldActive = true;
    changed = true;
  }

  if (changed) saveProgress();
}

function isDailyRewardClaimed() {
  const today = getTodayKey();
  // Сравнение ">=" защищает от перевода часов назад: дата из будущего
  // считается уже полученной наградой и не даёт фармить бонус.
  return progress.dailyRewardDate !== "" && progress.dailyRewardDate >= today;
}

function renderDailyReward() {
  const isClaimed = isDailyRewardClaimed();
  ui.dailyRewardText.textContent = isClaimed ? tr("dailyRewardClaimed") : tr("dailyRewardReady");
  ui.dailyRewardButton.textContent = isClaimed ? tr("done") : `★ ${DAILY_REWARD_STARS}`;
  ui.dailyRewardButton.disabled = isClaimed;
}

function claimDailyReward() {
  ensureDailyState();
  if (isDailyRewardClaimed()) return;

  const transactionKey = "daily:reward";
  if (!beginTransaction(transactionKey)) return;
  let committed = false;

  try {
    if (isDailyRewardClaimed()) return;
    progress.dailyRewardDate = getTodayKey();
    progress.stars = Math.max(0, progress.stars + DAILY_REWARD_STARS);
    committed = true;
    saveProgress();
    renderDailyReward();
    renderUpgrades();
    playSound("gold");
  } finally {
    endTransaction(transactionKey, committed);
  }
}

function claimTaskReward(taskId) {
  ensureDailyState();
  const transactionKey = `task:${taskId}`;
  if (!beginTransaction(transactionKey)) return;
  let committed = false;

  try {
    const task = progress.dailyTasks.find((item) => item.id === taskId);
    const info = taskDefinitions[taskId];
    if (!task || !info || task.claimed || task.progress < info.target) return;

    task.claimed = true;
    progress.stars = Math.max(0, progress.stars + DAILY_TASK_REWARD);
    committed = true;
    saveProgress();
    renderUpgrades();
    playSound("buy");
  } finally {
    endTransaction(transactionKey, committed);
  }
}

function addTaskProgress(taskId, amount) {
  ensureDailyState();
  const task = progress.dailyTasks.find((item) => item.id === taskId);
  const info = taskDefinitions[taskId];
  if (!task || !info || task.claimed) return;
  if (!finiteNumber(amount)) return;

  if (taskId === "score" || taskId === "combo") {
    task.progress = Math.max(task.progress, Math.trunc(amount));
  } else {
    task.progress += Math.trunc(amount);
  }

  task.progress = clamp(task.progress, 0, info.target);
  saveProgress();
}

function getActiveSkin() {
  return skinInfo[progress.activeSkin] || skinInfo.blue;
}

function ensureDailyState() {
  const today = getTodayKey();
  const validTasks = Array.isArray(progress.dailyTasks) &&
    progress.dailyTasks.length === 3 &&
    progress.dailyTasks.every((task) => isPlainObject(task) && Object.hasOwn(taskDefinitions, task.id));

  // Сброс только при реально новом дне. Дата из будущего (часы переведены назад)
  // не сбрасывает задания, иначе прогресс можно было бы фармить бесконечно.
  const isNewDay = progress.dailyTasksDate === "" || progress.dailyTasksDate < today;

  if (isNewDay || !validTasks) {
    progress.dailyTasksDate = today;
    progress.dailyTasks = createDailyTasks(today);
    progress.dailyTasksCompletedBonusClaimed = false;
    saveProgress();
    return;
  }

  progress.dailyTasks = progress.dailyTasks.map((task) => ({
    id: task.id,
    progress: readInt(task.progress, 0, taskDefinitions[task.id].target, 0),
    claimed: readBool(task.claimed, false)
  }));
}

function createDailyTasks(dateKey) {
  const ids = Object.keys(taskDefinitions);
  const seed = String(dateKey).split("").reduce((sum, char) => sum + char.charCodeAt(0), 0);
  const shifted = ids.map((id, index) => ids[(index + seed) % ids.length]);

  return shifted.slice(0, 3).map((id) => ({
    id,
    progress: 0,
    claimed: false
  }));
}

function getTodayKey() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

/* ------------------------------------------------------------ reset flow */

function openResetDialog() {
  if (!ui.resetDialog || ui.resetDialog.open) return;
  resetDialogOpener = document.activeElement instanceof HTMLElement ? document.activeElement : ui.resetProgressButton;
  ui.resetDialog.showModal();
  try {
    ui.resetCancelButton?.focus({ preventScroll: true });
  } catch (error) {
    ui.resetCancelButton?.focus();
  }
}

function closeResetDialog() {
  if (!ui.resetDialog || !ui.resetDialog.open) return;
  ui.resetDialog.close();
}

function confirmReset() {
  const previousRevision = readInt(progress.revision, 0, Number.MAX_SAFE_INTEGER, 0);
  // Фокус после сброса уходит в Menu, а не обратно на кнопку в скрытом экране.
  resetDialogOpener = null;

  storageRemove(ACTIVE_KEY);
  storageRemove(STORAGE_KEY);

  markGameplayStop();
  game = null;
  pressedMovementKeys.clear();
  purchaseCooldowns.clear();

  progress = defaultProgress();
  // Revision продолжает расти, иначе облачная копия старого прогресса
  // выиграла бы merge и вернула удалённые данные обратно.
  progress.revision = previousRevision;
  ensureDailyState();
  saveProgress();
  scheduleCloudSave(true);

  ui.bonusPill.classList.add("hidden");
  showAdNotice(null);
  applyLanguage();
  renderUpgrades();
  updateMenu();
  updateSoundControls();
  closeResetDialog();
  switchScreen("menu");
  playSound("buy");
}

/* ------------------------------------------------------------- rendering */

function draw() {
  drawBackground();

  if (!game || !game.running) {
    return;
  }

  ctx.save();
  if (game.shake > 0) {
    ctx.translate(random(-8, 8) * game.shake, random(-8, 8) * game.shake);
  }

  drawSuctionField();
  game.thoughts.forEach(drawThought);
  game.particles.forEach(drawParticle);
  drawPlayer(game.player.x, game.player.y);
  ctx.restore();
}

function drawBackground() {
  const gradient = ctx.createLinearGradient(0, 0, width, height);
  gradient.addColorStop(0, "#b6f3ff");
  gradient.addColorStop(0.48, "#f9f0ff");
  gradient.addColorStop(1, "#ffe8a8");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);

  backgroundBubbles.forEach((bubble) => {
    ctx.beginPath();
    ctx.arc(bubble.x + Math.sin(bubble.wobble) * 8, bubble.y, bubble.r, 0, Math.PI * 2);
    ctx.fillStyle = bubble.color;
    ctx.fill();
  });
}

function drawSuctionField() {
  const player = game.player;
  const radius = player.suckRadius + (game.magnetTimer > 0 ? 95 : 0);
  const alpha = game.magnetTimer > 0 ? 0.2 : 0.1;

  ctx.beginPath();
  ctx.arc(player.x, player.y, radius, 0, Math.PI * 2);
  ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
  ctx.fill();
  ctx.strokeStyle = game.magnetTimer > 0 ? "rgba(255, 202, 62, 0.72)" : "rgba(255, 255, 255, 0.38)";
  ctx.lineWidth = 2;
  ctx.setLineDash([8, 10]);
  ctx.stroke();
  ctx.setLineDash([]);
}

function drawThought(thought) {
  const bob = Math.sin(thought.pulse) * 3;
  ctx.save();
  ctx.translate(thought.x, thought.y + bob);
  ctx.rotate(thought.spin * 0.12);

  const style = {
    good: {
      gradient: ["#ffffff", "#b9f7df"],
      stroke: "#1fbf7f",
      glow: "rgba(31, 191, 127, 0.22)",
      badge: "+",
      badgeFill: "#1fbf7f"
    },
    bad: {
      gradient: ["#fff1f4", "#ff8fa3"],
      stroke: "#f03e63",
      glow: "rgba(240, 62, 99, 0.26)",
      badge: "!",
      badgeFill: "#f03e63"
    },
    gold: {
      gradient: ["#fff9c9", "#ffc83d"],
      stroke: "#ffae00",
      glow: "rgba(255, 200, 61, 0.34)",
      badge: "★",
      badgeFill: "#ffae00"
    },
    rainbow: {
      gradient: ["#ffffff", "#e9e3ff"],
      stroke: "#8878ff",
      glow: "rgba(136, 120, 255, 0.30)",
      badge: "✦",
      badgeFill: "#8878ff"
    }
  }[thought.type];

  ctx.beginPath();
  ctx.arc(0, 0, thought.radius + 8, 0, Math.PI * 2);
  ctx.fillStyle = style.glow;
  ctx.fill();

  const gradient = ctx.createRadialGradient(-8, -10, 4, 0, 0, thought.radius + 10);
  gradient.addColorStop(0, style.gradient[0]);
  gradient.addColorStop(1, style.gradient[1]);

  ctx.beginPath();
  ctx.arc(0, 0, thought.radius, 0, Math.PI * 2);
  ctx.fillStyle = gradient;
  ctx.fill();
  ctx.lineWidth = 4;
  ctx.strokeStyle = style.stroke;
  ctx.stroke();

  if (thought.type === "rainbow") {
    ctx.save();
    ctx.lineWidth = 3;
    ctx.lineCap = "round";
    RAINBOW_COLORS.forEach((color, index) => {
      const start = -Math.PI / 2 + (index / RAINBOW_COLORS.length) * Math.PI * 2;
      const end = -Math.PI / 2 + ((index + 0.82) / RAINBOW_COLORS.length) * Math.PI * 2;
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.arc(0, 0, thought.radius + 6, start, end);
      ctx.stroke();
    });
    ctx.restore();
  }

  ctx.font = `${thought.radius + 3}px "Segoe UI Emoji", "Apple Color Emoji", sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(thought.emoji, 0, 1);

  ctx.beginPath();
  ctx.arc(thought.radius * 0.63, -thought.radius * 0.62, 9, 0, Math.PI * 2);
  ctx.fillStyle = style.badgeFill;
  ctx.fill();
  ctx.lineWidth = 2;
  ctx.strokeStyle = "#ffffff";
  ctx.stroke();

  ctx.fillStyle = "#ffffff";
  ctx.font = thought.type === "gold" ? "700 12px Arial" : "900 15px Arial";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(style.badge, thought.radius * 0.63, -thought.radius * 0.62 + 0.5);

  ctx.restore();
}

function drawParticle(particle) {
  const alpha = Math.max(0, particle.life / particle.maxLife);
  ctx.globalAlpha = alpha;
  ctx.beginPath();
  ctx.arc(particle.x, particle.y, particle.size * alpha, 0, Math.PI * 2);
  ctx.fillStyle = particle.color;
  ctx.fill();
  ctx.globalAlpha = 1;
}

function drawPlayer(x, y) {
  ctx.save();
  ctx.translate(x, y);

  // Масштабирует только presentation-layer. Collision/suction radius остаются
  // в игровых координатах и не меняют баланс на мобильных экранах.
  const visualScale = getPlayerVisualScale(window.innerWidth, window.innerHeight);
  diagnostics.playerVisualScale = visualScale;
  ctx.scale(visualScale, visualScale);

  const auraPulse = game && game.running ? 1 + Math.sin(game.elapsed * 4) * 0.06 : 1;
  const skin = getActiveSkin();
  const startProgress = game ? clamp(game.vacuumStartTimer / VACUUM_START_DURATION, 0, 1) : 0;
  const startShake = startProgress > 0 ? Math.sin(game.elapsed * 72) * startProgress * 1.8 : 0;
  const bob = game && game.running ? Math.sin(game.elapsed * 8) * 1.4 + startShake : 0;
  const startupGlow = startProgress > 0 ? 0.16 + Math.sin(game.elapsed * 18) * 0.06 : 0;

  // Soft magical suction aura around the vacuum.
  ctx.save();
  ctx.globalAlpha = 0.28;
  ctx.beginPath();
  ctx.arc(2, -1, 47 * auraPulse, 0, Math.PI * 2);
  ctx.fillStyle = skin.auraFill;
  ctx.fill();
  ctx.globalAlpha = 0.42;
  ctx.lineWidth = 3;
  ctx.strokeStyle = skin.aura;
  ctx.setLineDash([7, 9]);
  ctx.beginPath();
  ctx.arc(2, -1, 56 * auraPulse, 0, Math.PI * 2);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();

  drawSparkle(-45, -28, 6, "#ffd75d");
  drawSparkle(38, -34, 5, "#ffffff");
  drawSparkle(43, 22, 6, "#b9fff3");

  ctx.translate(0, bob);
  if (startProgress > 0) {
    ctx.rotate(Math.sin(game.elapsed * 58) * startProgress * 0.025);
  }
  ctx.lineJoin = "round";
  ctx.lineCap = "round";

  if (isVacuumBitmapReady()) {
    drawVacuumBitmap(startProgress, startupGlow);
  } else {
    drawVacuumFallback(startProgress, startupGlow);
  }
  ctx.restore();
  return;
}

function getPlayerVisualScale(viewportWidth = window.innerWidth, viewportHeight = window.innerHeight) {
  if (viewportHeight <= 520 || viewportWidth <= 340) return 0.28;
  if (viewportWidth <= 420) return 0.32;
  return 0.4;
}

function drawVacuumBitmap(startProgress, startupGlow) {
  const scale = 0.4;
  const drawWidth = vacuumPlayerImage.naturalWidth * scale;
  const drawHeight = vacuumPlayerImage.naturalHeight * scale;
  const bodyCenterX = 255 * scale;
  const bodyCenterY = 260 * scale;

  ctx.save();
  ctx.shadowColor = "rgba(23, 36, 61, 0.22)";
  ctx.shadowBlur = 10;
  ctx.shadowOffsetY = 5;
  ctx.drawImage(vacuumPlayerImage, -bodyCenterX, -bodyCenterY, drawWidth, drawHeight);
  ctx.restore();

  if (startupGlow > 0) {
    ctx.save();
    ctx.globalCompositeOperation = "screen";
    ctx.globalAlpha = startupGlow;
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.ellipse(0, -2, 45, 31, -0.05, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  if (startProgress > 0) {
    drawStartupSuction(startProgress);
  }
}

function drawVacuumFallback(startProgress, startupGlow) {
  ctx.save();
  ctx.scale(0.84, 0.84);

  ctx.shadowColor = "rgba(23, 36, 61, 0.24)";
  ctx.shadowBlur = 12;
  ctx.shadowOffsetY = 7;

  const hoseGradient = ctx.createLinearGradient(-28, -86, 58, -62);
  hoseGradient.addColorStop(0, "#17233a");
  hoseGradient.addColorStop(0.45, "#64758e");
  hoseGradient.addColorStop(1, "#222d45");

  ctx.lineWidth = 14;
  ctx.strokeStyle = hoseGradient;
  ctx.beginPath();
  ctx.moveTo(-16, -57);
  ctx.bezierCurveTo(-8, -104, 62, -108, 76, -54);
  ctx.stroke();

  ctx.lineWidth = 3;
  ctx.strokeStyle = "rgba(255,255,255,0.26)";
  for (let i = 0; i < 8; i += 1) {
    const x = -6 + i * 11;
    ctx.beginPath();
    ctx.moveTo(x, -86 + Math.sin(i) * 5);
    ctx.lineTo(x + 5, -71 + Math.cos(i) * 4);
    ctx.stroke();
  }

  ctx.lineWidth = 11;
  ctx.strokeStyle = "#e8f4ff";
  ctx.beginPath();
  ctx.moveTo(-76, 32);
  ctx.lineTo(-42, -44);
  ctx.stroke();
  ctx.lineWidth = 15;
  ctx.strokeStyle = "#202b42";
  ctx.beginPath();
  ctx.moveTo(-44, -45);
  ctx.lineTo(-32, -53);
  ctx.stroke();

  ctx.fillStyle = "#1f2a42";
  roundRectPath(ctx, -112, 47, 72, 28, 6);
  ctx.fill();
  const nozzleGradient = ctx.createLinearGradient(-109, 48, -43, 72);
  nozzleGradient.addColorStop(0, "#f8fcff");
  nozzleGradient.addColorStop(0.6, "#e5f1f8");
  nozzleGradient.addColorStop(1, "#9aacbd");
  ctx.fillStyle = nozzleGradient;
  roundRectPath(ctx, -107, 42, 78, 21, 5);
  ctx.fill();
  ctx.lineWidth = 4;
  ctx.strokeStyle = "#14213a";
  ctx.stroke();

  const bodyGradient = ctx.createLinearGradient(-48, -36, 78, 72);
  bodyGradient.addColorStop(0, "#4fefff");
  bodyGradient.addColorStop(0.55, "#18bbe4");
  bodyGradient.addColorStop(1, "#1177bd");
  ctx.fillStyle = bodyGradient;
  roundRectPath(ctx, -54, -45, 126, 93, 38);
  ctx.fill();
  ctx.lineWidth = 5;
  ctx.strokeStyle = "#16243d";
  ctx.stroke();

  const sideGradient = ctx.createLinearGradient(47, -31, 93, 30);
  sideGradient.addColorStop(0, "#ffe29b");
  sideGradient.addColorStop(1, "#ff9f18");
  ctx.fillStyle = sideGradient;
  roundRectPath(ctx, 50, -26, 39, 63, 12);
  ctx.fill();
  ctx.strokeStyle = "#14213a";
  ctx.stroke();

  ctx.fillStyle = "#26334c";
  roundRectPath(ctx, -50, 30, 139, 27, 11);
  ctx.fill();
  ctx.fillStyle = "rgba(255,255,255,0.24)";
  roundRectPath(ctx, -39, 33, 65, 6, 3);
  ctx.fill();

  ctx.fillStyle = "#1d2941";
  ctx.beginPath();
  ctx.arc(73, 49, 30, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#52647d";
  ctx.beginPath();
  ctx.arc(73, 49, 20, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#a9c6e9";
  ctx.beginPath();
  ctx.arc(73, 49, 10, 0, Math.PI * 2);
  ctx.fill();

  drawVacuumFallbackEye(-21, -7);
  drawVacuumFallbackEye(25, -7);
  ctx.strokeStyle = "#101a2d";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(2, 13, 15, 0.18 * Math.PI, 0.82 * Math.PI);
  ctx.stroke();

  ctx.fillStyle = "#ff7890";
  ctx.globalAlpha = 0.82;
  ctx.beginPath();
  ctx.ellipse(-45, 16, 10, 7, -0.2, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(47, 16, 10, 7, 0.2, 0, Math.PI * 2);
  ctx.fill();
  ctx.globalAlpha = 1;

  ctx.fillStyle = "rgba(255,255,255,0.72)";
  ctx.beginPath();
  ctx.ellipse(13, -32, 26, 10, 0.12, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();

  if (startupGlow > 0) {
    ctx.save();
    ctx.globalCompositeOperation = "screen";
    ctx.globalAlpha = startupGlow * 0.75;
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.ellipse(0, -2, 45, 31, -0.05, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  if (startProgress > 0) {
    drawStartupSuction(startProgress);
  }
}

function drawVacuumFallbackEye(x, y) {
  ctx.save();
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.ellipse(x, y, 15, 20, -0.08, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#081225";
  ctx.beginPath();
  ctx.ellipse(x + 2, y + 2, 9, 13, -0.04, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.arc(x - 3, y - 6, 4, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function roundRectPath(context, x, y, widthValue, heightValue, radius) {
  const r = Math.min(radius, widthValue / 2, heightValue / 2);
  context.beginPath();
  context.moveTo(x + r, y);
  context.lineTo(x + widthValue - r, y);
  context.quadraticCurveTo(x + widthValue, y, x + widthValue, y + r);
  context.lineTo(x + widthValue, y + heightValue - r);
  context.quadraticCurveTo(x + widthValue, y + heightValue, x + widthValue - r, y + heightValue);
  context.lineTo(x + r, y + heightValue);
  context.quadraticCurveTo(x, y + heightValue, x, y + heightValue - r);
  context.lineTo(x, y + r);
  context.quadraticCurveTo(x, y, x + r, y);
  context.closePath();
}

function drawStartupSuction(strength) {
  ctx.save();
  const alpha = Math.min(0.9, 0.25 + strength * 0.65);
  const t = game?.elapsed || 0;

  ctx.globalAlpha = alpha * 0.28;
  const cone = ctx.createLinearGradient(-138, 20, -66, 40);
  cone.addColorStop(0, "rgba(31, 191, 163, 0)");
  cone.addColorStop(0.55, "rgba(126, 231, 200, 0.65)");
  cone.addColorStop(1, "rgba(255, 255, 255, 0.95)");
  ctx.beginPath();
  ctx.moveTo(-145, 8);
  ctx.quadraticCurveTo(-102, 27, -68, 34);
  ctx.quadraticCurveTo(-103, 56, -145, 64);
  ctx.closePath();
  ctx.fillStyle = cone;
  ctx.fill();

  const colors = ["#ffffff", "#7ee7c8", "#ffd75d", "#ff8fb0"];
  for (let i = 0; i < 9; i += 1) {
    const phase = (t * 115 + i * 19) % 58;
    const x = -142 + phase;
    const y = 12 + i * 6 + Math.sin(t * 8 + i) * 4;
    ctx.globalAlpha = alpha * (0.55 + (i % 3) * 0.12);
    ctx.lineWidth = 2.4 + (i % 3) * 0.8;
    ctx.strokeStyle = colors[i % colors.length];
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.bezierCurveTo(x + 23, y - 13, -103, 43 + Math.sin(i) * 8, -70, 37 + Math.cos(i) * 5);
    ctx.stroke();
  }

  for (let i = 0; i < 14; i += 1) {
    const phase = (t * 125 + i * 23) % 74;
    const size = 2 + (i % 4) * 0.7;
    ctx.globalAlpha = alpha * (0.5 + (phase / 74) * 0.35);
    ctx.fillStyle = colors[(i + 1) % colors.length];
    ctx.beginPath();
    ctx.arc(-145 + phase, 15 + (i % 7) * 7 + Math.sin(t * 9 + i) * 4, size, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.globalAlpha = alpha;
  for (let i = 0; i < 4; i += 1) {
    drawSparkle(-130 + ((t * 80 + i * 28) % 58), 20 + i * 10, 3.2, colors[(i + 2) % colors.length]);
  }

  ctx.restore();
}

function drawSparkle(x, y, size, color) {
  ctx.save();
  ctx.translate(x, y);
  ctx.beginPath();
  ctx.moveTo(0, -size);
  ctx.lineTo(size * 0.32, -size * 0.32);
  ctx.lineTo(size, 0);
  ctx.lineTo(size * 0.32, size * 0.32);
  ctx.lineTo(0, size);
  ctx.lineTo(-size * 0.32, size * 0.32);
  ctx.lineTo(-size, 0);
  ctx.lineTo(-size * 0.32, -size * 0.32);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
  ctx.lineWidth = 2;
  ctx.strokeStyle = "rgba(255,255,255,0.85)";
  ctx.stroke();
  ctx.restore();
}
function createBackgroundBubble() {
  return {
    x: random(0, Math.max(width, 320)),
    y: random(0, Math.max(height, 420)),
    r: random(18, 74),
    vx: random(-10, 10),
    vy: random(-8, 8),
    wobble: random(0, 10),
    color: pick([
      "rgba(255,255,255,0.22)",
      "rgba(255,111,145,0.10)",
      "rgba(31,191,163,0.10)",
      "rgba(255,200,61,0.12)"
    ])
  };
}

function unlockAudio() {
  if (progress.soundMuted) return;
  if (!audioContext) {
    const AudioCtor = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtor) return;
    audioContext = new AudioCtor();
  }

  if (audioContext.state === "suspended") {
    audioContext.resume().catch(() => {});
  }
}

function getSoundVolume() {
  return progress.soundMuted ? 0 : 0.72;
}

function startVacuumLoop() {
  if (progress.soundMuted || !audioContext || !game || !game.running || vacuumLoop) return;

  const now = audioContext.currentTime;
  const duration = VACUUM_START_DURATION;
  game.vacuumStartTimer = Math.max(game.vacuumStartTimer || 0, duration);
  const volume = getSoundVolume();
  const hum = audioContext.createOscillator();
  const humGain = audioContext.createGain();
  const rumble = audioContext.createOscillator();
  const rumbleGain = audioContext.createGain();
  const noise = audioContext.createBufferSource();
  const motorNoiseFilter = audioContext.createBiquadFilter();
  const motorNoiseGain = audioContext.createGain();
  const airNoiseFilter = audioContext.createBiquadFilter();
  const airNoiseGain = audioContext.createGain();
  const airLfo = audioContext.createOscillator();
  const airLfoGain = audioContext.createGain();
  const compressor = audioContext.createDynamicsCompressor();
  const masterGain = audioContext.createGain();
  const bufferSize = Math.max(1, Math.floor(audioContext.sampleRate * 0.55));
  const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
  const data = buffer.getChannelData(0);
  let brownNoise = 0;

  for (let i = 0; i < bufferSize; i += 1) {
    brownNoise = brownNoise * 0.985 + (Math.random() * 2 - 1) * 0.11;
    data[i] = clamp(brownNoise * 3.2, -1, 1);
  }

  // Низкий синус и мягкий треугольник имитируют двигатель без режущих
  // гармоник, которые давали неприятный «писк» у старой пилы.
  hum.type = "sine";
  hum.frequency.setValueAtTime(52, now);
  hum.frequency.exponentialRampToValueAtTime(74, now + 0.65);
  hum.frequency.setTargetAtTime(70, now + 0.8, 0.75);
  humGain.gain.setValueAtTime(0.16, now);

  rumble.type = "triangle";
  rumble.frequency.setValueAtTime(31, now);
  rumble.frequency.exponentialRampToValueAtTime(43, now + 0.55);
  rumbleGain.gain.setValueAtTime(0.11, now);

  noise.buffer = buffer;
  noise.loop = true;
  motorNoiseFilter.type = "lowpass";
  motorNoiseFilter.frequency.setValueAtTime(300, now);
  motorNoiseFilter.frequency.exponentialRampToValueAtTime(520, now + 0.7);
  motorNoiseFilter.Q.setValueAtTime(0.45, now);
  motorNoiseGain.gain.setValueAtTime(0.34, now);

  // Небольшая приглушённая воздушная составляющая делает звук похожим на
  // работающий бытовой пылесос, но не добавляет болезненного верхнего шума.
  airNoiseFilter.type = "bandpass";
  airNoiseFilter.frequency.setValueAtTime(560, now);
  airNoiseFilter.frequency.exponentialRampToValueAtTime(900, now + 0.65);
  airNoiseFilter.Q.setValueAtTime(0.55, now);
  airNoiseGain.gain.setValueAtTime(0.105, now);
  airLfo.type = "sine";
  airLfo.frequency.setValueAtTime(0.7, now);
  airLfoGain.gain.setValueAtTime(0.022, now);

  compressor.threshold.setValueAtTime(-28, now);
  compressor.knee.setValueAtTime(18, now);
  compressor.ratio.setValueAtTime(4, now);
  compressor.attack.setValueAtTime(0.02, now);
  compressor.release.setValueAtTime(0.3, now);

  masterGain.gain.setValueAtTime(0.001, now);
  masterGain.gain.exponentialRampToValueAtTime(Math.max(0.001, volume * 0.055), now + 0.25);
  masterGain.gain.setTargetAtTime(Math.max(0.001, volume * 0.04), now + 0.7, 0.6);
  masterGain.gain.exponentialRampToValueAtTime(0.001, now + duration);

  hum.connect(humGain);
  humGain.connect(compressor);
  rumble.connect(rumbleGain);
  rumbleGain.connect(compressor);
  noise.connect(motorNoiseFilter);
  motorNoiseFilter.connect(motorNoiseGain);
  motorNoiseGain.connect(compressor);
  noise.connect(airNoiseFilter);
  airNoiseFilter.connect(airNoiseGain);
  airNoiseGain.connect(compressor);
  airLfo.connect(airLfoGain);
  airLfoGain.connect(airNoiseGain.gain);
  compressor.connect(masterGain);
  masterGain.connect(audioContext.destination);

  hum.start(now);
  rumble.start(now);
  noise.start(now);
  airLfo.start(now);
  hum.stop(now + duration + 0.03);
  rumble.stop(now + duration + 0.03);
  noise.stop(now + duration + 0.03);
  airLfo.stop(now + duration + 0.03);
  vacuumLoop = { hum, rumble, noise, airLfo, masterGain, endTime: now + duration };
  window.setTimeout(() => {
    if (vacuumLoop?.hum === hum) vacuumLoop = null;
  }, Math.ceil((duration + 0.08) * 1000));
}

function stopVacuumLoop(immediate = false) {
  if (!vacuumLoop || !audioContext) {
    vacuumLoop = null;
    return;
  }

  const loop = vacuumLoop;
  const now = audioContext.currentTime;
  const fade = immediate ? 0.01 : 0.22;
  vacuumLoop = null;

  try {
    loop.masterGain.gain.cancelScheduledValues(now);
    loop.masterGain.gain.setValueAtTime(Math.max(0.001, loop.masterGain.gain.value), now);
    loop.masterGain.gain.exponentialRampToValueAtTime(0.001, now + fade);
    loop.hum.stop(now + fade + 0.02);
    loop.rumble?.stop(now + fade + 0.02);
    loop.noise.stop(now + fade + 0.02);
    loop.airLfo?.stop(now + fade + 0.02);
  } catch (error) {
    console.warn("Не удалось остановить звук пылесоса:", error);
  }
}

function getBubbleNoiseBuffer() {
  if (!audioContext) return null;
  if (bubbleNoiseBuffer?.sampleRate === audioContext.sampleRate) return bubbleNoiseBuffer;

  const bufferSize = Math.max(1, Math.floor(audioContext.sampleRate * 0.14));
  const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i += 1) {
    const envelope = 1 - i / bufferSize;
    data[i] = (Math.random() * 2 - 1) * envelope;
  }
  bubbleNoiseBuffer = buffer;
  return buffer;
}

function playBubblePop() {
  if (progress.soundMuted || !audioContext) return;

  const now = audioContext.currentTime;
  const body = audioContext.createOscillator();
  const bodyGain = audioContext.createGain();
  const tick = audioContext.createOscillator();
  const tickGain = audioContext.createGain();
  const tickFilter = audioContext.createBiquadFilter();
  const bodyFilter = audioContext.createBiquadFilter();
  const noise = audioContext.createBufferSource();
  const noiseFilter = audioContext.createBiquadFilter();
  const noiseGain = audioContext.createGain();
  const peak = Math.max(0.001, getSoundVolume());

  body.type = "sine";
  body.frequency.setValueAtTime(470, now);
  body.frequency.exponentialRampToValueAtTime(145, now + 0.12);
  bodyFilter.type = "lowpass";
  bodyFilter.frequency.setValueAtTime(1250, now);
  bodyFilter.Q.setValueAtTime(0.35, now);
  bodyGain.gain.setValueAtTime(0.001, now);
  bodyGain.gain.exponentialRampToValueAtTime(peak * 0.065, now + 0.006);
  bodyGain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);

  tick.type = "triangle";
  tick.frequency.setValueAtTime(760, now);
  tick.frequency.exponentialRampToValueAtTime(340, now + 0.055);
  tickFilter.type = "lowpass";
  tickFilter.frequency.setValueAtTime(1200, now);
  tickFilter.Q.setValueAtTime(0.35, now);
  tickGain.gain.setValueAtTime(0.001, now);
  tickGain.gain.exponentialRampToValueAtTime(peak * 0.014, now + 0.003);
  tickGain.gain.exponentialRampToValueAtTime(0.001, now + 0.065);

  noiseFilter.type = "lowpass";
  noiseFilter.frequency.setValueAtTime(1650, now);
  noiseFilter.Q.setValueAtTime(0.35, now);
  noiseGain.gain.setValueAtTime(peak * 0.035, now);
  noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.075);

  body.connect(bodyFilter);
  bodyFilter.connect(bodyGain);
  bodyGain.connect(audioContext.destination);
  tick.connect(tickFilter);
  tickFilter.connect(tickGain);
  tickGain.connect(audioContext.destination);

  const bubbleBuffer = getBubbleNoiseBuffer();
  if (bubbleBuffer) {
    noise.buffer = bubbleBuffer;
    noise.connect(noiseFilter);
    noiseFilter.connect(noiseGain);
    noiseGain.connect(audioContext.destination);
    noise.start(now);
    noise.stop(now + 0.15);
  }

  body.start(now);
  tick.start(now);
  body.stop(now + 0.16);
  tick.stop(now + 0.08);
}

function playSound(type) {
  if (progress.soundMuted || !audioContext) return;

  if (type === "pop") {
    playBubblePop();
    return;
  }

  const now = audioContext.currentTime;
  const gain = audioContext.createGain();
  const oscillator = audioContext.createOscillator();
  const settings = {
    good: [450, 0.08, "sine", 0.025],
    combo: [650, 0.11, "sine", 0.035],
    gold: [780, 0.14, "sine", 0.045],
    bad: [165, 0.18, "sine", 0.025],
    buy: [520, 0.09, "triangle", 0.022],
    over: [180, 0.26, "sine", 0.03]
  }[type] || [440, 0.06, "sine", 0.04];
  const filter = audioContext.createBiquadFilter();

  oscillator.type = settings[2];
  oscillator.frequency.setValueAtTime(settings[0], now);
  if (type === "bad" || type === "over") {
    oscillator.frequency.exponentialRampToValueAtTime(80, now + settings[1]);
  } else {
    oscillator.frequency.exponentialRampToValueAtTime(settings[0] * 1.5, now + settings[1]);
  }

  gain.gain.setValueAtTime(Math.max(0.001, settings[3] * getSoundVolume()), now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + settings[1]);
  filter.type = "lowpass";
  filter.frequency.setValueAtTime(type === "bad" ? 900 : 1400, now);
  filter.Q.setValueAtTime(0.35, now);
  oscillator.connect(filter);
  filter.connect(gain);
  gain.connect(audioContext.destination);
  oscillator.start(now);
  oscillator.stop(now + settings[1] + 0.02);
}

function toggleSound() {
  progress.soundMuted = !progress.soundMuted;
  if (progress.soundMuted && audioContext && audioContext.state === "running") {
    stopVacuumLoop(true);
    audioContext.suspend().catch(() => {});
  } else if (!progress.soundMuted) {
    unlockAudio();
    startVacuumLoop();
    playSound("buy");
  }
  saveProgress();
  updateSoundControls();
}

function updateSoundControls() {
  if (!ui.soundToggleButton) return;
  ui.soundToggleButton.textContent = progress.soundMuted ? "🔇" : "🔊";
  ui.soundToggleButton.setAttribute("aria-label", progress.soundMuted ? tr("soundOff") : tr("soundOn"));
  ui.soundToggleButton.title = progress.soundMuted ? tr("soundOff") : tr("soundOn");
}

function random(min, max) {
  return Math.random() * (max - min) + min;
}

function pick(items) {
  return items[Math.floor(Math.random() * items.length)];
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}
