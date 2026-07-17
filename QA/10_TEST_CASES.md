# 10 — Test Cases

Build: `TV-cc6576a5764a`. Источник статусов: фактические checks и ограничения окружения.

| Status | Count |
| --- | --- |
| PASS | 27 |
| FAIL | 5 |
| BLOCKED | 2 |
| NOT_RUN | 49 |
| NOT_APPLICABLE | 0 |

## TC-SMOKE-001 — Чистый запуск меню

| Field | Value |
| --- | --- |
| Test Case ID | TC-SMOKE-001 |
| Feature ID | FEAT-STATE-001 |
| Risk ID | RISK-START-001 |
| Module | Launch |
| Title | Чистый запуск меню |
| Objective | Проверить базовую инициализацию |
| Preconditions | Пустое mock localStorage |
| Test Data | ru-RU |
| Steps | 1. Загрузить test harness.<br>2. Дождаться инициализации.<br>3. Проверить активный menuScreen и кнопку Играть. |
| Expected Result | Меню активно; критические элементы видимы. |
| Actual Result | Меню отображено, game.js инициализирован. |
| Status | PASS |
| Priority | Critical |
| Test Type | Smoke |
| Test Technique | Critical path |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-001_menu_1024x768.png |
| Related Bug |  |
| Notes |  |

## TC-SMOKE-002 — Доступность runtime state

| Field | Value |
| --- | --- |
| Test Case ID | TC-SMOKE-002 |
| Feature ID | FEAT-CORE-001 |
| Risk ID | RISK-START-001 |
| Module | Launch |
| Title | Доступность runtime state |
| Objective | Проверить выполнение script |
| Preconditions | Игра загружена |
| Test Data | N/A |
| Steps | 1. Проверить typeof startGame/progress/game. |
| Expected Result | Функции и state доступны. |
| Actual Result | startGame=function, progress=object, game=object. |
| Status | PASS |
| Priority | Critical |
| Test Type | Smoke |
| Test Technique | Static/dynamic check |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-LOC-001 — Автовыбор English

| Field | Value |
| --- | --- |
| Test Case ID | TC-LOC-001 |
| Feature ID | FEAT-LOC-001 |
| Risk ID | RISK-LOC-001 |
| Module | Localization |
| Title | Автовыбор English |
| Objective | Проверить en locale |
| Preconditions | Чистое состояние |
| Test Data | navigator.language=en-US |
| Steps | 1. Запустить с en-US locale.<br>2. Проверить html lang, title, Play. |
| Expected Result | UI English; lang=en. |
| Actual Result | Thought Vacuum / Play / lang=en. |
| Status | PASS |
| Priority | High |
| Test Type | Localization |
| Test Technique | Equivalence partition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-002_menu_en.png |
| Related Bug |  |
| Notes |  |

## TC-LOC-002 — Русская локализация и map codes

| Field | Value |
| --- | --- |
| Test Case ID | TC-LOC-002 |
| Feature ID | FEAT-LOC-001 |
| Risk ID | RISK-LOC-001 |
| Module | Localization |
| Title | Русская локализация и map codes |
| Objective | Проверить RU и fallback mapping |
| Preconditions | Чистое состояние |
| Test Data | ru-RU, be-BY, kk-KZ, uk-UA, de-DE |
| Steps | 1. Запустить ru-RU.<br>2. Вызвать resolveLanguage для кодов. |
| Expected Result | ru/be/kk/uk/uz→ru; прочие→en. |
| Actual Result | mapping=['ru','ru','ru','en']; Играть. 'uz' подтвержден статически. |
| Status | PASS |
| Priority | High |
| Test Type | Localization |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-DAILY-001 — Получение daily reward один раз

| Field | Value |
| --- | --- |
| Test Case ID | TC-DAILY-001 |
| Feature ID | FEAT-DAILY-001 |
| Risk ID | RISK-SAVE-003 |
| Module | Daily |
| Title | Получение daily reward один раз |
| Objective | Проверить начисление/persistence |
| Preconditions | Награда сегодня не получена |
| Test Data | stars=0 |
| Steps | 1. Нажать daily reward.<br>2. Проверить +3 и disabled.<br>3. Перезапустить с сохраненным state. |
| Expected Result | +3; повтор недоступен; состояние восстановлено. |
| Actual Result | stars 0→3, кнопка disabled после повторной загрузки. |
| Status | PASS |
| Priority | High |
| Test Type | Functional |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-UI-001 — Навигация в мастерскую

| Field | Value |
| --- | --- |
| Test Case ID | TC-UI-001 |
| Feature ID | FEAT-STATE-001 |
| Risk ID | RISK-UI-002 |
| Module | UI |
| Title | Навигация в мастерскую |
| Objective | Проверить screen flow и карточки |
| Preconditions | Меню |
| Test Data | N/A |
| Steps | 1. Нажать Улучшения.<br>2. Проверить 3/3/4/3 карточки.<br>3. Нажать Назад. |
| Expected Result | Переходы корректны; menu восстановлено. |
| Actual Result | Counts 3 upgrades, 3 boosters, 4 skins, 3 tasks; возврат успешен. |
| Status | PASS |
| Priority | High |
| Test Type | Functional |
| Test Technique | User journey |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ACC-001 — Tab navigation меню

| Field | Value |
| --- | --- |
| Test Case ID | TC-ACC-001 |
| Feature ID | FEAT-UI-001 |
| Risk ID | RISK-ACC-001 |
| Module | Accessibility |
| Title | Tab navigation меню |
| Objective | Проверить клавиатурную достижимость кнопок |
| Preconditions | Меню |
| Test Data | Tab |
| Steps | 1. Нажимать Tab 8 раз.<br>2. Записать activeElement. |
| Expected Result | Daily, Play, Upgrades получают фокус. |
| Actual Result | Фокус достиг dailyRewardButton, playButton, upgradesButton. |
| Status | PASS |
| Priority | High |
| Test Type | Accessibility |
| Test Technique | Exploratory |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-001 — Старт раунда

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-001 |
| Feature ID | FEAT-CORE-001 |
| Risk ID | RISK-CORE-002 |
| Module | Gameplay |
| Title | Старт раунда |
| Objective | Проверить стартовое состояние |
| Preconditions | Меню |
| Test Data | Play |
| Steps | 1. Нажать Играть.<br>2. Проверить state/HUD. |
| Expected Result | game, running=true, score=0, lives=3, combo=1. |
| Actual Result | Точное стартовое состояние подтверждено. |
| Status | PASS |
| Priority | Critical |
| Test Type | Smoke |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-003_game_start.png |
| Related Bug |  |
| Notes |  |

## TC-INPUT-001 — Boundary pointer target

| Field | Value |
| --- | --- |
| Test Case ID | TC-INPUT-001 |
| Feature ID | FEAT-INPUT-001 |
| Risk ID | RISK-INPUT-002 |
| Module | Input |
| Title | Boundary pointer target |
| Objective | Проверить clamp координат |
| Preconditions | Активный раунд |
| Test Data | (-100,-100), (2000,2000), viewport 1024×768 |
| Steps | 1. Передать координаты ниже min.<br>2. Передать выше max.<br>3. Проверить tx/ty. |
| Expected Result | 20,20 и 1004,748. |
| Actual Result | Получены 20,20 и 1004,748. |
| Status | PASS |
| Priority | High |
| Test Type | Functional |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-STATE-001 — Pause/resume API

| Field | Value |
| --- | --- |
| Test Case ID | TC-STATE-001 |
| Feature ID | FEAT-STATE-002 |
| Risk ID | RISK-INPUT-001 |
| Module | State |
| Title | Pause/resume API |
| Objective | Проверить system pause transitions |
| Preconditions | Активный раунд |
| Test Data | reason=window |
| Steps | 1. pauseActiveGame(window).<br>2. Проверить false/reason.<br>3. resumeSystemPausedGame(window). |
| Expected Result | running false→true; reason очищен. |
| Actual Result | Переход выполнен. |
| Status | PASS |
| Priority | High |
| Test Type | Functional |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-002 — 5 good thoughts повышают combo

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-002 |
| Feature ID | FEAT-CORE-004 |
| Risk ID | RISK-CORE-001 |
| Module | Gameplay |
| Title | 5 good thoughts повышают combo |
| Objective | Проверить scoring/streak |
| Preconditions | Активный раунд |
| Test Data | 5 good |
| Steps | 1. Сбросить score/combo.<br>2. Собрать 5 good.<br>3. Проверить значения. |
| Expected Result | score=50, streak=5, combo=2. |
| Actual Result | 50/5/x2. |
| Status | PASS |
| Priority | Critical |
| Test Type | Functional |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-003 — Bad без shield

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-003 |
| Feature ID | FEAT-CORE-005 |
| Risk ID | RISK-CORE-002 |
| Module | Gameplay |
| Title | Bad без shield |
| Objective | Проверить урон |
| Preconditions | 3 жизни, no shield |
| Test Data | 1 bad |
| Steps | 1. Столкнуться с bad.<br>2. Проверить lives/combo/streak. |
| Expected Result | lives=2; combo=1; streak=0. |
| Actual Result | Подтверждено. |
| Status | PASS |
| Priority | Critical |
| Test Type | Functional |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-004 — Shield блокирует bad

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-004 |
| Feature ID | FEAT-CORE-005 |
| Risk ID | RISK-CORE-002 |
| Module | Gameplay |
| Title | Shield блокирует bad |
| Objective | Проверить одноразовую защиту |
| Preconditions | 3 жизни, shield=true |
| Test Data | 1 bad |
| Steps | 1. Столкнуться с bad.<br>2. Проверить жизнь и shield. |
| Expected Result | lives=3; shield=false. |
| Actual Result | Подтверждено. |
| Status | PASS |
| Priority | Critical |
| Test Type | Functional |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-005 — Gold начисляет бонус

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-005 |
| Feature ID | FEAT-CORE-006 |
| Risk ID | RISK-CORE-001 |
| Module | Gameplay |
| Title | Gold начисляет бонус |
| Objective | Проверить reward |
| Preconditions | combo=1, timers=0 |
| Test Data | 1 gold |
| Steps | 1. Собрать gold.<br>2. Проверить score и timers. |
| Expected Result | score +50; один timer >0. |
| Actual Result | score=50; magnet=6 в данном run. |
| Status | PASS |
| Priority | High |
| Test Type | Functional |
| Test Technique | Equivalence partition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-006 — Double и combo множители

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-006 |
| Feature ID | FEAT-CORE-004 |
| Risk ID | RISK-CORE-001 |
| Module | Gameplay |
| Title | Double и combo множители |
| Objective | Проверить порядок множителей |
| Preconditions | combo=2, double=active |
| Test Data | 1 good |
| Steps | 1. Собрать good.<br>2. Проверить score. |
| Expected Result | 10×2×2=40. |
| Actual Result | 40. |
| Status | PASS |
| Priority | High |
| Test Type | Functional |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-007 — Поражение и награда

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-007 |
| Feature ID | FEAT-CORE-005 |
| Risk ID | RISK-CORE-002 |
| Module | Game over |
| Title | Поражение и награда |
| Objective | Проверить endGame |
| Preconditions | score=250, lives=1 |
| Test Data | 1 bad |
| Steps | 1. Получить bad.<br>2. Проверить result screen, best, earned stars. |
| Expected Result | gameOver; best≥250; earned=2. |
| Actual Result | gameOver; best=250; earned=2. |
| Status | PASS |
| Priority | Critical |
| Test Type | Smoke |
| Test Technique | Critical path |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-004_game_over.png |
| Related Bug |  |
| Notes |  |

## TC-CORE-008 — Чистый restart

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-008 |
| Feature ID | FEAT-CORE-001 |
| Risk ID | RISK-CORE-002 |
| Module | Restart |
| Title | Чистый restart |
| Objective | Проверить повторный запуск |
| Preconditions | gameOver |
| Test Data | Restart |
| Steps | 1. Нажать Играть снова.<br>2. Проверить state. |
| Expected Result | score=0, lives=3, combo=1, running. |
| Actual Result | Подтверждено. |
| Status | PASS |
| Priority | Critical |
| Test Type | Smoke |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-SAVE-001 — Невалидный JSON

| Field | Value |
| --- | --- |
| Test Case ID | TC-SAVE-001 |
| Feature ID | FEAT-SAVE-001 |
| Risk ID | RISK-SAVE-001 |
| Module | Save |
| Title | Невалидный JSON |
| Objective | Проверить fallback |
| Preconditions | localStorage value=not-json |
| Test Data | not-json |
| Steps | 1. Запустить.<br>2. Проверить menu/default state. |
| Expected Result | Игра запускается с defaults и warning. |
| Actual Result | best=0, stars=0, menu; warning в browser_console.json. |
| Status | PASS |
| Priority | Critical |
| Test Type | Negative |
| Test Technique | Error guessing |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-AUDIO-001 — Mute persistence

| Field | Value |
| --- | --- |
| Test Case ID | TC-AUDIO-001 |
| Feature ID | FEAT-AUDIO-001 |
| Risk ID | RISK-AUDIO-002 |
| Module | Audio |
| Title | Mute persistence |
| Objective | Проверить сохранение mute |
| Preconditions | Активный раунд |
| Test Data | soundMuted false→true |
| Steps | 1. Нажать mute.<br>2. Сохранить и повторно загрузить state.<br>3. Проверить aria-label. |
| Expected Result | soundMuted=true; label Включить звук. |
| Actual Result | Подтверждено. |
| Status | PASS |
| Priority | Medium |
| Test Type | Functional |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-BOOST-001 — Активация трех boosters

| Field | Value |
| --- | --- |
| Test Case ID | TC-BOOST-001 |
| Feature ID | FEAT-BOOST-001 |
| Risk ID | RISK-ECON-001 |
| Module | Boosters |
| Title | Активация трех boosters |
| Objective | Проверить списание/эффект |
| Preconditions | По 1 каждого |
| Test Data | magnet/shield/double |
| Steps | 1. Установить inventory.<br>2. Start.<br>3. Проверить inventory/timers. |
| Expected Result | Counts 0; timers active; shield true. |
| Actual Result | magnet≈5.95, double≈7.95, shield=true. |
| Status | PASS |
| Priority | High |
| Test Type | Functional |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-BOOST-002 — Выход в Menu после старта с boosters

| Field | Value |
| --- | --- |
| Test Case ID | TC-BOOST-002 |
| Feature ID | FEAT-BOOST-001 |
| Risk ID | RISK-ECON-001 |
| Module | Boosters |
| Title | Выход в Menu после старта с boosters |
| Objective | Проверить защиту от случайной потери |
| Preconditions | Boosters активированы |
| Test Data | Menu |
| Steps | 1. Start с boosters.<br>2. Нажать Menu.<br>3. Проверить confirmation/return. |
| Expected Result | Есть подтверждение либо неиспользованные boosters возвращаются. |
| Actual Result | Выход мгновенный; все boosters остаются списанными. |
| Status | FAIL |
| Priority | High |
| Test Type | Usability/Functional |
| Test Technique | User journey |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/BUG-004_step-01_boosters-active.png; evidence/BUG-004_result_menu-no-confirmation.png |
| Related Bug | BUG-004 |
| Notes |  |

## TC-ADS-001 — Revive без SDK

| Field | Value |
| --- | --- |
| Test Case ID | TC-ADS-001 |
| Feature ID | FEAT-ADS-002 |
| Risk ID | RISK-ADS-001 |
| Module | Ads |
| Title | Revive без SDK |
| Objective | Проверить reward integrity |
| Preconditions | gameOver; yaSdk=null; revive available |
| Test Data | Click revive |
| Steps | 1. Нажать Смотреть рекламу +1 жизнь.<br>2. Наблюдать ad/reward. |
| Expected Result | Без onRewarded reward не выдается; выводится error/retry. |
| Actual Result | Реклама не показывается; revive выдан синхронно, lives=1. |
| Status | FAIL |
| Priority | Critical |
| Test Type | Negative |
| Test Technique | Decision table |
| Platform | Yandex/standalone fallback |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/BUG-002_step-01_game-over.png; evidence/BUG-002_result_revived-without-ad.png |
| Related Bug | BUG-002 |
| Notes |  |

## TC-ADS-002 — x2 stars без SDK

| Field | Value |
| --- | --- |
| Test Case ID | TC-ADS-002 |
| Feature ID | FEAT-ADS-003 |
| Risk ID | RISK-ADS-001 |
| Module | Ads |
| Title | x2 stars без SDK |
| Objective | Проверить reward integrity |
| Preconditions | gameOver; earned>0; yaSdk=null |
| Test Data | Click x2 |
| Steps | 1. Нажать x2 stars.<br>2. Наблюдать ad/reward. |
| Expected Result | Без onRewarded reward не выдается. |
| Actual Result | stars 2→4 без рекламы. |
| Status | FAIL |
| Priority | Critical |
| Test Type | Negative |
| Test Technique | Decision table |
| Platform | Yandex/standalone fallback |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | logs/tests.log |
| Related Bug | BUG-002 |
| Notes |  |

## TC-UI-002 — Пылесос у левой границы

| Field | Value |
| --- | --- |
| Test Case ID | TC-UI-002 |
| Feature ID | FEAT-UI-002 |
| Risk ID | RISK-UI-001 |
| Module | Graphics |
| Title | Пылесос у левой границы |
| Objective | Проверить видимость avatar |
| Preconditions | Активный раунд |
| Test Data | pointer x=0 |
| Steps | 1. Переместить указатель к левому краю.<br>2. Дождаться follow.<br>3. Оценить sprite. |
| Expected Result | Основная часть sprite и feedback остаются видимыми. |
| Actual Result | Пылесос почти полностью обрезан; center x≈23.2. |
| Status | FAIL |
| Priority | Medium |
| Test Type | Visual |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/BUG-003_result.png |
| Related Bug | BUG-003 |
| Notes |  |

## TC-PERF-001 — Update-loop stress

| Field | Value |
| --- | --- |
| Test Case ID | TC-PERF-001 |
| Feature ID | FEAT-GFX-001 |
| Risk ID | RISK-PERF-001 |
| Module | Performance |
| Title | Update-loop stress |
| Objective | Проверить отсутствие exception/NaN в state loop |
| Preconditions | Активный game; spawn disabled for isolation |
| Test Data | 3000×0.033s |
| Steps | 1. Выполнить 3000 updateGame.<br>2. Проверить finite state. |
| Expected Result | Нет exception/NaN; running remains true. |
| Actual Result | ~99.9s simulated; no exception. |
| Status | PASS |
| Priority | Medium |
| Test Type | Stability |
| Test Technique | Stress |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes | Не FPS/soak и не реальное время. |

## TC-SAVE-002 — dailyTasks содержит null

| Field | Value |
| --- | --- |
| Test Case ID | TC-SAVE-002 |
| Feature ID | FEAT-SAVE-001 |
| Risk ID | RISK-SAVE-001 |
| Module | Save |
| Title | dailyTasks содержит null |
| Objective | Проверить nested corruption recovery |
| Preconditions | JSON valid, dailyTasks=[null,null,null] |
| Test Data | Corrupt structured save |
| Steps | 1. Запустить с сохранением.<br>2. Наблюдать pageerror/инициализацию. |
| Expected Result | Invalid nested entries сбрасываются; menu функционально. |
| Actual Result | Uncaught TypeError: Cannot read properties of null (reading 'id'). |
| Status | FAIL |
| Priority | Critical |
| Test Type | Negative |
| Test Technique | Robustness/error guessing |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/BUG-001_result.png; logs/page_errors.json |
| Related Bug | BUG-001 |
| Notes |  |

## TC-COMP-001 — Мастерская 320×568

| Field | Value |
| --- | --- |
| Test Case ID | TC-COMP-001 |
| Feature ID | FEAT-UI-002 |
| Risk ID | RISK-UI-002 |
| Module | Compatibility |
| Title | Мастерская 320×568 |
| Objective | Проверить layout/scroll |
| Preconditions | Чистое состояние |
| Test Data | 320×568 |
| Steps | 1. Открыть мастерскую.<br>2. Проверить panel scroll и доступность Back. |
| Expected Result | Back существует; panel scrollable при необходимости. |
| Actual Result | panel scroll/client подтверждены; screenshot EV-VP-320x568.png. |
| Status | PASS |
| Priority | Medium |
| Test Type | Compatibility |
| Test Technique | Pairwise/viewport |
| Platform | Chromium |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-VP-320x568.png |
| Related Bug |  |
| Notes |  |

## TC-COMP-002 — Мастерская 360×640

| Field | Value |
| --- | --- |
| Test Case ID | TC-COMP-002 |
| Feature ID | FEAT-UI-002 |
| Risk ID | RISK-UI-002 |
| Module | Compatibility |
| Title | Мастерская 360×640 |
| Objective | Проверить layout/scroll |
| Preconditions | Чистое состояние |
| Test Data | 360×640 |
| Steps | 1. Открыть мастерскую.<br>2. Проверить panel scroll и доступность Back. |
| Expected Result | Back существует; panel scrollable при необходимости. |
| Actual Result | panel scroll/client подтверждены; screenshot EV-VP-360x640.png. |
| Status | PASS |
| Priority | Medium |
| Test Type | Compatibility |
| Test Technique | Pairwise/viewport |
| Platform | Chromium |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-VP-360x640.png |
| Related Bug |  |
| Notes |  |

## TC-COMP-003 — Мастерская 768×1024

| Field | Value |
| --- | --- |
| Test Case ID | TC-COMP-003 |
| Feature ID | FEAT-UI-002 |
| Risk ID | RISK-UI-002 |
| Module | Compatibility |
| Title | Мастерская 768×1024 |
| Objective | Проверить layout/scroll |
| Preconditions | Чистое состояние |
| Test Data | 768×1024 |
| Steps | 1. Открыть мастерскую.<br>2. Проверить panel scroll и доступность Back. |
| Expected Result | Back существует; panel scrollable при необходимости. |
| Actual Result | panel scroll/client подтверждены; screenshot EV-VP-768x1024.png. |
| Status | PASS |
| Priority | Medium |
| Test Type | Compatibility |
| Test Technique | Pairwise/viewport |
| Platform | Chromium |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-VP-768x1024.png |
| Related Bug |  |
| Notes |  |

## TC-COMP-004 — Мастерская 1366×768

| Field | Value |
| --- | --- |
| Test Case ID | TC-COMP-004 |
| Feature ID | FEAT-UI-002 |
| Risk ID | RISK-UI-002 |
| Module | Compatibility |
| Title | Мастерская 1366×768 |
| Objective | Проверить layout/scroll |
| Preconditions | Чистое состояние |
| Test Data | 1366×768 |
| Steps | 1. Открыть мастерскую.<br>2. Проверить panel scroll и доступность Back. |
| Expected Result | Back существует; panel scrollable при необходимости. |
| Actual Result | panel scroll/client подтверждены; screenshot EV-VP-1366x768.png. |
| Status | PASS |
| Priority | Medium |
| Test Type | Compatibility |
| Test Technique | Pairwise/viewport |
| Platform | Chromium |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-VP-1366x768.png |
| Related Bug |  |
| Notes |  |

## TC-COMP-005 — Мастерская 1920×1080

| Field | Value |
| --- | --- |
| Test Case ID | TC-COMP-005 |
| Feature ID | FEAT-UI-002 |
| Risk ID | RISK-UI-002 |
| Module | Compatibility |
| Title | Мастерская 1920×1080 |
| Objective | Проверить layout/scroll |
| Preconditions | Чистое состояние |
| Test Data | 1920×1080 |
| Steps | 1. Открыть мастерскую.<br>2. Проверить panel scroll и доступность Back. |
| Expected Result | Back существует; panel scrollable при необходимости. |
| Actual Result | panel scroll/client подтверждены; screenshot EV-VP-1920x1080.png. |
| Status | PASS |
| Priority | Medium |
| Test Type | Compatibility |
| Test Technique | Pairwise/viewport |
| Platform | Chromium |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-VP-1920x1080.png |
| Related Bug |  |
| Notes |  |

## TC-COMP-006 — Touch scroll 360×640

| Field | Value |
| --- | --- |
| Test Case ID | TC-COMP-006 |
| Feature ID | FEAT-UI-002 |
| Risk ID | RISK-UI-002 |
| Module | Compatibility |
| Title | Touch scroll 360×640 |
| Objective | Проверить прокрутку длинной panel |
| Preconditions | Mobile emulation, touch |
| Test Data | Swipe up |
| Steps | 1. Открыть master.<br>2. Выполнить touch swipe.<br>3. Проверить scrollTop. |
| Expected Result | scrollTop увеличивается. |
| Actual Result | 0→451. |
| Status | PASS |
| Priority | High |
| Test Type | Compatibility |
| Test Technique | Gesture test |
| Platform | Chromium mobile emulation |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence | evidence/EV-008_mobile_touch_scroll.png |
| Related Bug |  |
| Notes |  |

## TC-PLAT-001 — SDK loader indicator IT

| Field | Value |
| --- | --- |
| Test Case ID | TC-PLAT-001 |
| Feature ID | FEAT-PLAT-001 |
| Risk ID | RISK-PLAT-001 |
| Module | Platform |
| Title | SDK loader indicator IT |
| Objective | Проверить актуальное подключение SDK |
| Preconditions | Опубликованный draft/debug panel |
| Test Data | debug-mode=16 |
| Steps | 1. Открыть draft debug panel.<br>2. Проверить loader indicator. |
| Expected Result | Indicator IT; init succeeds. |
| Actual Result | Blocked: реальная среда Yandex Games и loader/debug panel недоступны. |
| Status | BLOCKED |
| Priority | Critical |
| Test Type | Platform |
| Test Technique | Compliance check |
| Platform | Yandex Games |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ADS-003 — Реальный interstitial после 3 rounds

| Field | Value |
| --- | --- |
| Test Case ID | TC-ADS-003 |
| Feature ID | FEAT-ADS-001 |
| Risk ID | RISK-ADS-002 |
| Module | Ads |
| Title | Реальный interstitial после 3 rounds |
| Objective | Проверить platform ad flow |
| Preconditions | Yandex SDK, 3 completed rounds |
| Test Data | Restart |
| Steps | 1. Завершить 3 rounds.<br>2. Restart.<br>3. Наблюдать ad callbacks. |
| Expected Result | Ad API called; game resumes/start after close/error. |
| Actual Result | Blocked: реальная среда Yandex Games и loader/debug panel недоступны. |
| Status | BLOCKED |
| Priority | Critical |
| Test Type | Platform |
| Test Technique | State transition |
| Platform | Yandex Games |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-BUILD-001 — Release ZIP structure

| Field | Value |
| --- | --- |
| Test Case ID | TC-BUILD-001 |
| Feature ID | FEAT-PLAT-001 |
| Risk ID | RISK-PLAT-002 |
| Module | Build |
| Title | Release ZIP structure |
| Objective | Проверить корневой index/assets |
| Preconditions | Release archive |
| Test Data | ZIP |
| Steps | Распаковать; сверить paths; открыть через Yandex local server. |
| Expected Result | Нет missing resources. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Critical |
| Test Type | Build verification |
| Test Technique | Checklist |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-INPUT-002 — Реальное mouse/touch управление

| Field | Value |
| --- | --- |
| Test Case ID | TC-INPUT-002 |
| Feature ID | FEAT-INPUT-001 |
| Risk ID | RISK-INPUT-002 |
| Module | Input |
| Title | Реальное mouse/touch управление |
| Objective | Проверить feel/latency |
| Preconditions | Playable runtime |
| Test Data | Mouse/touch |
| Steps | Играть 3 минуты на каждом input. |
| Expected Result | Точный и предсказуемый контроль. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Critical |
| Test Type | Manual |
| Test Technique | Exploratory |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-INPUT-003 — Multi-touch и conflict

| Field | Value |
| --- | --- |
| Test Case ID | TC-INPUT-003 |
| Feature ID | FEAT-INPUT-001 |
| Risk ID | RISK-INPUT-002 |
| Module | Input |
| Title | Multi-touch и conflict |
| Objective | Проверить pointer ownership |
| Preconditions | Mobile device |
| Test Data | 2 fingers |
| Steps | Одновременно двигать двумя пальцами/отпускать. |
| Expected Result | Нет скачков/залипания. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Negative |
| Test Technique | Error guessing |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-INPUT-004 — Keyboard gameplay alternative

| Field | Value |
| --- | --- |
| Test Case ID | TC-INPUT-004 |
| Feature ID | FEAT-INPUT-001 |
| Risk ID | RISK-ACC-001 |
| Module | Input |
| Title | Keyboard gameplay alternative |
| Objective | Проверить возможность играть без pointer |
| Preconditions | Desktop |
| Test Data | Arrows/WASD |
| Steps | Попробовать управлять keyboard. |
| Expected Result | Поддерживаемая альтернатива либо явно N/A по design. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Accessibility |
| Test Technique | Exploratory |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-STATE-002 — Реальный Alt+Tab/blur

| Field | Value |
| --- | --- |
| Test Case ID | TC-STATE-002 |
| Feature ID | FEAT-STATE-002 |
| Risk ID | RISK-INPUT-001 |
| Module | State |
| Title | Реальный Alt+Tab/blur |
| Objective | Проверить pause/audio |
| Preconditions | Desktop browser |
| Test Data | Alt+Tab |
| Steps | Во время hazards Alt+Tab 10s и вернуться. |
| Expected Result | Gameplay frozen; no damage; audio stopped/resumes. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Critical |
| Test Type | Manual |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-009 — Spawn distribution sanity

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-009 |
| Feature ID | FEAT-CORE-002 |
| Risk ID | RISK-CORE-003 |
| Module | Gameplay |
| Title | Spawn distribution sanity |
| Objective | Проверить все thought types |
| Preconditions | Natural play |
| Test Data | 100 spawns |
| Steps | Записать 100 spawn types. |
| Expected Result | Good/bad/gold появляются; нет невозможных positions. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Exploratory |
| Test Technique | Statistical sampling |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-010 — Spawn pace over time

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-010 |
| Feature ID | FEAT-CORE-002 |
| Risk ID | RISK-PERF-001 |
| Module | Gameplay |
| Title | Spawn pace over time |
| Objective | Проверить pace min boundary |
| Preconditions | Long round |
| Test Data | elapsed 0/30/60s |
| Steps | Сравнить интервалы. |
| Expected Result | Pace ускоряется и не ниже 0.38 base range. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Functional |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-011 — Magnet attraction/repulsion

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-011 |
| Feature ID | FEAT-CORE-003 |
| Risk ID | RISK-PHYS-001 |
| Module | Physics |
| Title | Magnet attraction/repulsion |
| Objective | Проверить vectors visually |
| Preconditions | Magnet active |
| Test Data | good/gold/bad around player |
| Steps | Разместить объекты на границе radius. |
| Expected Result | Good/gold toward; bad away; no teleport. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Physics |
| Test Technique | Boundary/state |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-012 — Natural complete session

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-012 |
| Feature ID | FEAT-CORE-005 |
| Risk ID | RISK-CORE-003 |
| Module | Gameplay |
| Title | Natural complete session |
| Objective | Проверить полный цикл без state injection |
| Preconditions | Fresh profile |
| Test Data | Mouse/touch |
| Steps | Играть до gameOver; restart; repeat. |
| Expected Result | Цикл завершен естественно без soft lock. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Critical |
| Test Type | End-to-end |
| Test Technique | User journey |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-CORE-013 — Visual vs collision radius

| Field | Value |
| --- | --- |
| Test Case ID | TC-CORE-013 |
| Feature ID | FEAT-GFX-001 |
| Risk ID | RISK-PHYS-001 |
| Module | Collision |
| Title | Visual vs collision radius |
| Objective | Проверить понятность hitbox |
| Preconditions | Active round |
| Test Data | Bad at sprite edges |
| Steps | Подвести bad к видимым краям sprite. |
| Expected Result | Collision соответствует визуальному ожиданию. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Gameplay UX |
| Test Technique | Exploratory |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-DAILY-002 — Изменение системной даты

| Field | Value |
| --- | --- |
| Test Case ID | TC-DAILY-002 |
| Feature ID | FEAT-DAILY-001 |
| Risk ID | RISK-SAVE-003 |
| Module | Daily |
| Title | Изменение системной даты |
| Objective | Проверить anti-exploit/date rollover |
| Preconditions | Daily claimed |
| Test Data | Clock +1/-1 day |
| Steps | Менять дату и перезапускать. |
| Expected Result | Поведение определено; нет бесконечной награды либо риск принят. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Negative |
| Test Technique | Boundary/state |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-DAILY-003 — Progress good/gold tasks

| Field | Value |
| --- | --- |
| Test Case ID | TC-DAILY-003 |
| Feature ID | FEAT-DAILY-002 |
| Risk ID | RISK-CORE-001 |
| Module | Daily |
| Title | Progress good/gold tasks |
| Objective | Проверить счетчики |
| Preconditions | Task selected |
| Test Data | Exact target±1 |
| Steps | Собирать target-1, target, target+1. |
| Expected Result | Clamp target; claim enabled exactly at target. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Functional |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-DAILY-004 — Claim task reward once

| Field | Value |
| --- | --- |
| Test Case ID | TC-DAILY-004 |
| Feature ID | FEAT-DAILY-002 |
| Risk ID | RISK-SAVE-002 |
| Module | Daily |
| Title | Claim task reward once |
| Objective | Проверить economy/persistence |
| Preconditions | Completed task |
| Test Data | Double click/reload |
| Steps | Нажать Claim быстро 2x; reload. |
| Expected Result | +2 once; claimed persists. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Negative |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-DAILY-005 — All tasks bonus

| Field | Value |
| --- | --- |
| Test Case ID | TC-DAILY-005 |
| Feature ID | FEAT-DAILY-002 |
| Risk ID | RISK-SAVE-003 |
| Module | Daily |
| Title | All tasks bonus |
| Objective | Проверить +3 once |
| Preconditions | All 3 claimed |
| Test Data | Open upgrades repeatedly |
| Steps | Открыть master несколько раз. |
| Expected Result | +3 one time only. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Functional |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-DAILY-006 — Midnight rollover

| Field | Value |
| --- | --- |
| Test Case ID | TC-DAILY-006 |
| Feature ID | FEAT-DAILY-002 |
| Risk ID | RISK-LOC-001 |
| Module | Daily |
| Title | Midnight rollover |
| Objective | Проверить reset |
| Preconditions | Near local midnight |
| Test Data | Date transition |
| Steps | Оставить open/перезапустить после midnight. |
| Expected Result | Tasks reset consistently; old reward state handled. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | State |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-UPG-001 — Покупка каждого level

| Field | Value |
| --- | --- |
| Test Case ID | TC-UPG-001 |
| Feature ID | FEAT-UPG-001 |
| Risk ID | RISK-ECON-001 |
| Module | Upgrades |
| Title | Покупка каждого level |
| Objective | Проверить cost/level |
| Preconditions | Enough stars |
| Test Data | All costs |
| Steps | Покупать по одному level. |
| Expected Result | Correct cost; level+1; persists. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Functional |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-UPG-002 — Max limits

| Field | Value |
| --- | --- |
| Test Case ID | TC-UPG-002 |
| Feature ID | FEAT-UPG-001 |
| Risk ID | RISK-COUNT-001 |
| Module | Upgrades |
| Title | Max limits |
| Objective | Проверить 5/5,1/1 |
| Preconditions | At max |
| Test Data | Extra click |
| Steps | Попытаться купить beyond max. |
| Expected Result | No debit; button Max disabled. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Negative |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-UPG-003 — Insufficient stars

| Field | Value |
| --- | --- |
| Test Case ID | TC-UPG-003 |
| Feature ID | FEAT-UPG-001 |
| Risk ID | RISK-ECON-001 |
| Module | Upgrades |
| Title | Insufficient stars |
| Objective | Проверить disabled/guard |
| Preconditions | stars=cost-1 |
| Test Data | Each upgrade |
| Steps | Открыть master/call action. |
| Expected Result | No debit/level change. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Negative |
| Test Technique | Equivalence partition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-UPG-004 — Bonus duration effect

| Field | Value |
| --- | --- |
| Test Case ID | TC-UPG-004 |
| Feature ID | FEAT-UPG-001 |
| Risk ID | RISK-CORE-001 |
| Module | Upgrades |
| Title | Bonus duration effect |
| Objective | Уточнить область действия upgrade |
| Preconditions | bonus level 0/5 |
| Test Data | Random and starting bonuses |
| Steps | Сравнить durations. |
| Expected Result | All intended bonus types follow specification. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Functional |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-BOOST-003 — Inventory max 3

| Field | Value |
| --- | --- |
| Test Case ID | TC-BOOST-003 |
| Feature ID | FEAT-BOOST-001 |
| Risk ID | RISK-ECON-001 |
| Module | Boosters |
| Title | Inventory max 3 |
| Objective | Проверить cap |
| Preconditions | stars enough |
| Test Data | Buy 4 |
| Steps | Купить каждый booster 4 times. |
| Expected Result | Count max 3; 4th no debit. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Boundary |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-SKIN-001 — Purchase/select/persist

| Field | Value |
| --- | --- |
| Test Case ID | TC-SKIN-001 |
| Feature ID | FEAT-SKIN-001 |
| Risk ID | RISK-ECON-001 |
| Module | Skins |
| Title | Purchase/select/persist |
| Objective | Проверить store |
| Preconditions | Enough stars |
| Test Data | pink/gold/cosmic |
| Steps | Купить; restart; select. |
| Expected Result | Owned/active persisted; one debit. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Functional |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-SKIN-002 — Insufficient stars

| Field | Value |
| --- | --- |
| Test Case ID | TC-SKIN-002 |
| Feature ID | FEAT-SKIN-001 |
| Risk ID | RISK-ECON-001 |
| Module | Skins |
| Title | Insufficient stars |
| Objective | Проверить guard |
| Preconditions | cost-1 |
| Test Data | Paid skin |
| Steps | Click/call purchase. |
| Expected Result | No ownership/debit. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Negative |
| Test Technique | Equivalence partition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-SKIN-003 — Visual distinction

| Field | Value |
| --- | --- |
| Test Case ID | TC-SKIN-003 |
| Feature ID | FEAT-SKIN-001 |
| Risk ID | RISK-COMP-001 |
| Module | Skins |
| Title | Visual distinction |
| Objective | Проверить aura colors/readability |
| Preconditions | All owned |
| Test Data | 4 skins |
| Steps | Снять screenshots same state. |
| Expected Result | Skins visually distinct; gameplay meaning unchanged. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Low |
| Test Type | Visual |
| Test Technique | Comparative |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ADS-004 — Interstitial error callback

| Field | Value |
| --- | --- |
| Test Case ID | TC-ADS-004 |
| Feature ID | FEAT-ADS-001 |
| Risk ID | RISK-ADS-002 |
| Module | Ads |
| Title | Interstitial error callback |
| Objective | Проверить recovery |
| Preconditions | Mock SDK onError |
| Test Data | Error object |
| Steps | Trigger restart threshold. |
| Expected Result | Game starts after error; no stuck audio/state. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Integration |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ADS-005 — Real rewarded revive callbacks

| Field | Value |
| --- | --- |
| Test Case ID | TC-ADS-005 |
| Feature ID | FEAT-ADS-002 |
| Risk ID | RISK-ADS-002 |
| Module | Ads |
| Title | Real rewarded revive callbacks |
| Objective | Проверить reward only after onRewarded |
| Preconditions | Yandex SDK |
| Test Data | Close before reward / reward / error |
| Steps | Выполнить 3 paths. |
| Expected Result | Reward only rewarded path; buttons recover. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Critical |
| Test Type | Integration |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ADS-006 — Real rewarded x2 callbacks

| Field | Value |
| --- | --- |
| Test Case ID | TC-ADS-006 |
| Feature ID | FEAT-ADS-003 |
| Risk ID | RISK-ADS-002 |
| Module | Ads |
| Title | Real rewarded x2 callbacks |
| Objective | Проверить stars integrity |
| Preconditions | Yandex SDK |
| Test Data | Close/reward/error |
| Steps | Выполнить paths. |
| Expected Result | Stars added once only on reward. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Critical |
| Test Type | Integration |
| Test Technique | Decision table |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-AUDIO-002 — Audio on blur/minimize

| Field | Value |
| --- | --- |
| Test Case ID | TC-AUDIO-002 |
| Feature ID | FEAT-AUDIO-001 |
| Risk ID | RISK-AUDIO-001 |
| Module | Audio |
| Title | Audio on blur/minimize |
| Objective | Проверить requirement |
| Preconditions | Real browser/device |
| Test Data | Alt+Tab/minimize |
| Steps | Слушать до/после background. |
| Expected Result | Sound stops immediately; resumes appropriately. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Manual |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-AUDIO-003 — Sound event mapping

| Field | Value |
| --- | --- |
| Test Case ID | TC-AUDIO-003 |
| Feature ID | FEAT-AUDIO-001 |
| Risk ID | RISK-AUDIO-002 |
| Module | Audio |
| Title | Sound event mapping |
| Objective | Проверить каждый cue |
| Preconditions | Audio enabled |
| Test Data | good/combo/gold/bad/buy/over |
| Steps | Вызвать события и прослушать. |
| Expected Result | Distinct correct cues; no overlap artifact. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Audio |
| Test Technique | Exploratory |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-AUDIO-004 — Rapid mute/unmute

| Field | Value |
| --- | --- |
| Test Case ID | TC-AUDIO-004 |
| Feature ID | FEAT-AUDIO-001 |
| Risk ID | RISK-AUDIO-002 |
| Module | Audio |
| Title | Rapid mute/unmute |
| Objective | Проверить race |
| Preconditions | Active game |
| Test Data | 20 toggles |
| Steps | Быстро переключать. |
| Expected Result | No exception/stuck sound. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Negative |
| Test Technique | Stress |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-GFX-001 — Missing image fallback

| Field | Value |
| --- | --- |
| Test Case ID | TC-GFX-001 |
| Feature ID | FEAT-GFX-001 |
| Risk ID | RISK-COMP-001 |
| Module | Graphics |
| Title | Missing image fallback |
| Objective | Проверить graceful fallback |
| Preconditions | Remove/deny image in test copy |
| Test Data | 404 image |
| Steps | Launch/play. |
| Expected Result | Fallback vacuum visible; warning only. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Recovery |
| Test Technique | Fault injection |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-PERF-002 — 30-minute real soak

| Field | Value |
| --- | --- |
| Test Case ID | TC-PERF-002 |
| Feature ID | FEAT-GFX-001 |
| Risk ID | RISK-MEM-001 |
| Module | Performance |
| Title | 30-minute real soak |
| Objective | Проверить memory/stability |
| Preconditions | Production-like runtime |
| Test Data | 30 min natural play |
| Steps | Record memory/FPS every 5 min. |
| Expected Result | No unbounded growth/crash; thresholds documented. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Performance |
| Test Technique | Soak |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-PERF-003 — FPS/frame-time heavy scene

| Field | Value |
| --- | --- |
| Test Case ID | TC-PERF-003 |
| Feature ID | FEAT-GFX-001 |
| Risk ID | RISK-PERF-001 |
| Module | Performance |
| Title | FPS/frame-time heavy scene |
| Objective | Профилировать max objects/particles |
| Preconditions | Profiler available |
| Test Data | Gold bursts + high elapsed |
| Steps | Capture 60s metrics. |
| Expected Result | No unacceptable long frames per accepted target. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Performance |
| Test Technique | Load/stress |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-COMP-007 — Cross-browser matrix

| Field | Value |
| --- | --- |
| Test Case ID | TC-COMP-007 |
| Feature ID | FEAT-GFX-001 |
| Risk ID | RISK-COMP-001 |
| Module | Compatibility |
| Title | Cross-browser matrix |
| Objective | Проверить Chrome/Firefox/Safari/mobile |
| Preconditions | Devices available |
| Test Data | Latest stable browsers |
| Steps | Run smoke each. |
| Expected Result | No critical differences. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Compatibility |
| Test Technique | Pairwise |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-COMP-008 — Orientation/resize during game

| Field | Value |
| --- | --- |
| Test Case ID | TC-COMP-008 |
| Feature ID | FEAT-UI-002 |
| Risk ID | RISK-UI-002 |
| Module | Compatibility |
| Title | Orientation/resize during game |
| Objective | Проверить layout/state |
| Preconditions | Mobile/tablet |
| Test Data | portrait↔landscape |
| Steps | Rotate/resize repeatedly. |
| Expected Result | No distortion/lost state; input bounds update. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Compatibility |
| Test Technique | State transition |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-LOC-003 — Полный RU string audit

| Field | Value |
| --- | --- |
| Test Case ID | TC-LOC-003 |
| Feature ID | FEAT-LOC-001 |
| Risk ID | RISK-LOC-001 |
| Module | Localization |
| Title | Полный RU string audit |
| Objective | Проверить missing/mixed strings |
| Preconditions | All screens |
| Test Data | ru |
| Steps | Обойти все states/items/tasks/bonuses. |
| Expected Result | No English/raw keys. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Localization |
| Test Technique | Checklist |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-LOC-004 — Полный EN string audit

| Field | Value |
| --- | --- |
| Test Case ID | TC-LOC-004 |
| Feature ID | FEAT-LOC-001 |
| Risk ID | RISK-LOC-001 |
| Module | Localization |
| Title | Полный EN string audit |
| Objective | Проверить grammar/overflow |
| Preconditions | All screens |
| Test Data | en |
| Steps | Обойти all screens/items/tasks. |
| Expected Result | No Russian/raw keys/overflow. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Localization |
| Test Technique | Checklist |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-LOC-005 — Long strings/pseudo-loc

| Field | Value |
| --- | --- |
| Test Case ID | TC-LOC-005 |
| Feature ID | FEAT-LOC-001 |
| Risk ID | RISK-LOC-001 |
| Module | Localization |
| Title | Long strings/pseudo-loc |
| Objective | Проверить flexible layout |
| Preconditions | Instrumented strings |
| Test Data | ×1.5 length |
| Steps | Подставить длинные строки в QA copy. |
| Expected Result | No clipping/overlap; scroll available. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Low |
| Test Type | Localization |
| Test Technique | Boundary |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ACC-002 — Text contrast

| Field | Value |
| --- | --- |
| Test Case ID | TC-ACC-002 |
| Feature ID | FEAT-UI-001 |
| Risk ID | RISK-UI-003 |
| Module | Accessibility |
| Title | Text contrast |
| Objective | Проверить button text contrast |
| Preconditions | CSS colors |
| Test Data | white vs accent gradient |
| Steps | Рассчитать ratios/визуально. |
| Expected Result | Meet accepted contrast heuristic or documented exception. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Accessibility |
| Test Technique | Static analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ACC-003 — One-hand/keyboard alternative

| Field | Value |
| --- | --- |
| Test Case ID | TC-ACC-003 |
| Feature ID | FEAT-INPUT-001 |
| Risk ID | RISK-ACC-001 |
| Module | Accessibility |
| Title | One-hand/keyboard alternative |
| Objective | Оценить motor accessibility |
| Preconditions | Desktop/mobile |
| Test Data | Keyboard/single pointer |
| Steps | Попытаться complete cycle. |
| Expected Result | Control alternative or documented limitation. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Accessibility |
| Test Technique | User journey |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ACC-004 — Reduced motion/shake

| Field | Value |
| --- | --- |
| Test Case ID | TC-ACC-004 |
| Feature ID | FEAT-GFX-001 |
| Risk ID | RISK-ACC-002 |
| Module | Accessibility |
| Title | Reduced motion/shake |
| Objective | Проверить option |
| Preconditions | Bad collision |
| Test Data | Repeated hits |
| Steps | Искать toggle/reduced-motion OS behavior. |
| Expected Result | Shake can be reduced/disabled. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Accessibility |
| Test Technique | Checklist |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-ACC-005 — Screen reader gameplay state

| Field | Value |
| --- | --- |
| Test Case ID | TC-ACC-005 |
| Feature ID | FEAT-GFX-001 |
| Risk ID | RISK-ACC-003 |
| Module | Accessibility |
| Title | Screen reader gameplay state |
| Objective | Проверить semantics |
| Preconditions | Screen reader |
| Test Data | Menu/game/HUD/result |
| Steps | Navigate/read/play. |
| Expected Result | Critical state/actions communicated. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Accessibility |
| Test Technique | Assistive tech |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-PROG-001 — Score→stars boundaries

| Field | Value |
| --- | --- |
| Test Case ID | TC-PROG-001 |
| Feature ID | FEAT-PROG-001 |
| Risk ID | RISK-COUNT-001 |
| Module | Progress |
| Title | Score→stars boundaries |
| Objective | Проверить floor(score/100) |
| Preconditions | End game |
| Test Data | 0,99,100,199,200 |
| Steps | End each score. |
| Expected Result | 0,0,1,1,2 new stars. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Functional |
| Test Technique | Boundary value analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-PROG-002 — Large/corrupt counters

| Field | Value |
| --- | --- |
| Test Case ID | TC-PROG-002 |
| Feature ID | FEAT-PROG-001 |
| Risk ID | RISK-COUNT-001 |
| Module | Progress |
| Title | Large/corrupt counters |
| Objective | Проверить rendering/normalization |
| Preconditions | Injected save |
| Test Data | -1, 0, 2^53, Infinity unavailable in JSON |
| Steps | Load values. |
| Expected Result | No negative; finite values; UI usable. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Medium |
| Test Type | Robustness |
| Test Technique | Boundary/error guessing |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-SAVE-003 — Write failure/quota

| Field | Value |
| --- | --- |
| Test Case ID | TC-SAVE-003 |
| Feature ID | FEAT-SAVE-001 |
| Risk ID | RISK-SAVE-002 |
| Module | Save |
| Title | Write failure/quota |
| Objective | Проверить recovery/message |
| Preconditions | Mock setItem throw |
| Test Data | QuotaExceededError |
| Steps | Trigger progress changes. |
| Expected Result | Game continues; user informed or risk documented. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Recovery |
| Test Technique | Fault injection |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-SAVE-004 — Multiple sequential saves

| Field | Value |
| --- | --- |
| Test Case ID | TC-SAVE-004 |
| Feature ID | FEAT-SAVE-001 |
| Risk ID | RISK-SAVE-002 |
| Module | Save |
| Title | Multiple sequential saves |
| Objective | Проверить latest state |
| Preconditions | Normal profile |
| Test Data | 100 changes |
| Steps | Buy/claim/play/reload. |
| Expected Result | Latest consistent state, no partial corruption. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Stability |
| Test Technique | Stress |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-PLAT-002 — LoadingAPI.ready timing

| Field | Value |
| --- | --- |
| Test Case ID | TC-PLAT-002 |
| Feature ID | FEAT-PLAT-001 |
| Risk ID | RISK-PLAT-001 |
| Module | Platform |
| Title | LoadingAPI.ready timing |
| Objective | Проверить loader finish |
| Preconditions | Yandex debug panel |
| Test Data | Cold launch |
| Steps | Observe loading indicator/call. |
| Expected Result | ready after playable resources loaded. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Critical |
| Test Type | Integration |
| Test Technique | Timing |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-PLAT-003 — GameplayAPI lifecycle

| Field | Value |
| --- | --- |
| Test Case ID | TC-PLAT-003 |
| Feature ID | FEAT-PLAT-001 |
| Risk ID | RISK-PLAT-001 |
| Module | Platform |
| Title | GameplayAPI lifecycle |
| Objective | Проверить start/stop sequence |
| Preconditions | Instrument SDK |
| Test Data | Play/pause/ad/gameOver/menu |
| Steps | Record events. |
| Expected Result | No duplicate/missing; active periods match play. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Integration |
| Test Technique | State model |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-PLAT-004 — Platform moderation requirements

| Field | Value |
| --- | --- |
| Test Case ID | TC-PLAT-004 |
| Feature ID | FEAT-PLAT-001 |
| Risk ID | RISK-PLAT-001 |
| Module | Platform |
| Title | Platform moderation requirements |
| Objective | Проверить applicable public requirements |
| Preconditions | Draft complete |
| Test Data | Desktop/mobile |
| Steps | Run Yandex requirement checklist. |
| Expected Result | No mandatory violations; evidence retained. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | Critical |
| Test Type | Compliance |
| Test Technique | Checklist |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |

## TC-SEC-001 — Static secret/PII scan

| Field | Value |
| --- | --- |
| Test Case ID | TC-SEC-001 |
| Feature ID | FEAT-PLAT-001 |
| Risk ID | RISK-SEC-001 |
| Module | Security |
| Title | Static secret/PII scan |
| Objective | Проверить client files |
| Preconditions | Source set |
| Test Data | token/key/password patterns |
| Steps | Search files and inspect endpoints. |
| Expected Result | No secrets/PII. |
| Actual Result | Not executed |
| Status | NOT_RUN |
| Priority | High |
| Test Type | Security |
| Test Technique | Static analysis |
| Platform | Web |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Evidence |  |
| Related Bug |  |
| Notes |  |
