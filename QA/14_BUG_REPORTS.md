# 14 — Bug Reports

Build: `TV-cc6576a5764a`. Подтверждены только воспроизведенные проблемы.

## BUG-001 — Игра не завершает инициализацию, если сохранение содержит null в массиве dailyTasks

| Field | Value |
| --- | --- |
| Bug ID | BUG-001 |
| Title | Игра не завершает инициализацию, если сохранение содержит null в массиве dailyTasks |
| Confirmation | CONFIRMED |
| Component | Save / startup |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Preconditions | В localStorage по ключу thoughtVacuumProgress.v1 находится валидный JSON с dailyTasks:[null,null,null]. |
| Steps | 1. Записать указанное значение.<br>2. Запустить игру.<br>3. Наблюдать console/pageerror и попытаться использовать меню. |
| Actual | В ensureDailyState вызывается task.id для null; возникает TypeError и дальнейшая инициализация прерывается. |
| Expected | Некорректные nested entries должны быть отброшены, а state сброшен к безопасному default без startup exception. |
| Frequency | 3/3 в изолированном Chromium harness |
| Severity | S2 — Critical |
| Priority | P1 |
| Impact | Затронутый пользователь не может полноценно запустить игру, пока вручную не очистит localStorage. |
| Workaround | Очистить site data/localStorage; прогресс теряется. |
| Regression | Unknown; no history |
| Tests | TC-SAVE-002 |
| Features | FEAT-SAVE-001 |
| Evidence | evidence/BUG-001_result.png; logs/page_errors.json; logs/tests.log |
| Logs | page_errors.json: Cannot read properties of null (reading id) |
| Additional | Невалидный JSON обрабатывается, но валидный JSON с некорректной структурой — нет. |
| Code | game.js:1374-1394; входные данные из game.js:582-603 |
| Cause confidence | High |

## BUG-002 — Rewarded-награды выдаются без рекламы, когда Yandex SDK недоступен

| Field | Value |
| --- | --- |
| Bug ID | BUG-002 |
| Title | Rewarded-награды выдаются без рекламы, когда Yandex SDK недоступен |
| Confirmation | CONFIRMED |
| Component | Ads / economy |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness; yaSdk=null |
| Preconditions | Игра запущена без доступного Yandex SDK; экран gameOver; revive или x2 stars доступны. |
| Steps | 1. Завершить раунд.<br>2. Нажать «Смотреть рекламу: +1 жизнь» или «x2 звезды».<br>3. Наблюдать отсутствие рекламы и изменение state/balance. |
| Actual | showRewardedAd вызывает reward() и close() при !yaSdk; revive и звезды выдаются немедленно. |
| Expected | Reward должен выдаваться только после SDK callback onRewarded; при unavailable/error — безопасное сообщение и отсутствие награды. |
| Frequency | 5/5 для обоих paths |
| Severity | S2 — Critical |
| Priority | P0 |
| Impact | Обход рекламной монетизации и прогрессии; пользователи получают revive/currency без просмотра. |
| Workaround | Нет на клиенте; требуется изменение fallback policy. |
| Regression | Unknown |
| Tests | TC-ADS-001; TC-ADS-002 |
| Features | FEAT-ADS-002; FEAT-ADS-003 |
| Evidence | evidence/BUG-002_step-01_game-over.png; evidence/BUG-002_result_revived-without-ad.png; logs/tests.log |
| Logs | DYN-022/DYN-023 |
| Additional | На реальной платформе риск проявляется при init failure, ad API missing или standalone hosting. |
| Code | game.js:501-552, особенно 532-536; game.js:793-857 |
| Cause confidence | High |

## BUG-003 — Пылесос почти полностью выходит за видимую область при перемещении к краю экрана

| Field | Value |
| --- | --- |
| Bug ID | BUG-003 |
| Title | Пылесос почти полностью выходит за видимую область при перемещении к краю экрана |
| Confirmation | CONFIRMED |
| Component | Gameplay graphics / input bounds |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness; viewport 1024×768 |
| Preconditions | Активный раунд; изображение пылесоса загружено. |
| Steps | 1. Переместить указатель к x=0.<br>2. Дождаться, пока player приблизится к target x=20.<br>3. Оценить видимую часть sprite. |
| Actual | Центр ограничен x=20, но sprite шириной около 169 px; большая часть пылесоса обрезается за левым краем. |
| Expected | Основная визуальная модель игрока должна оставаться видимой; граница должна учитывать sprite/feedback bounds. |
| Frequency | 5/5 на 1024×768; статически симметрично для других краев |
| Severity | S4 — Minor |
| Priority | P2 |
| Impact | Ухудшается ориентация и понятность collision/feedback у границ. |
| Workaround | Не двигать указатель вплотную к краю. |
| Regression | Unknown |
| Tests | TC-UI-002 |
| Features | FEAT-UI-002; FEAT-GFX-001 |
| Evidence | evidence/BUG-003_result.png |
| Logs | DYN-024 |
| Additional | Collision radius 36 также заметно меньше визуального sprite — отдельный риск, требующий manual confirmation. |
| Code | game.js:878-883; game.js:1594-1623 |
| Cause confidence | High |

## BUG-004 — Кнопка «Меню» без подтверждения списывает активированные расходуемые бустеры

| Field | Value |
| --- | --- |
| Bug ID | BUG-004 |
| Title | Кнопка «Меню» без подтверждения списывает активированные расходуемые бустеры |
| Confirmation | CONFIRMED |
| Component | Boosters / navigation / economy |
| Build | TV-cc6576a5764a |
| Environment | Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness |
| Preconditions | В inventory есть magnetStart, shield и/или doubleStart; начат раунд. |
| Steps | 1. Начать раунд с бустером.<br>2. Сразу нажать «Меню».<br>3. Проверить inventory и наличие confirmation. |
| Actual | Бустеры списываются в startGame/applyStartingBoosters; Menu мгновенно завершает раунд, confirmation/возврата нет. |
| Expected | Перед необратимым выходом должно быть подтверждение с ясным предупреждением либо неиспользованные ресурсы возвращаются. |
| Frequency | 5/5 |
| Severity | S3 — Major |
| Priority | P1 |
| Impact | Случайное нажатие приводит к потере редких ресурсов/звезд. |
| Workaround | Не нажимать Menu после старта; визуального предупреждения нет. |
| Regression | Unknown |
| Tests | TC-BOOST-002 |
| Features | FEAT-BOOST-001; FEAT-STATE-001 |
| Evidence | evidence/BUG-004_step-01_boosters-active.png; evidence/BUG-004_result_menu-no-confirmation.png |
| Logs | DYN-020/DYN-021 |
| Additional | Особенно вероятно на mobile: Menu расположен рядом с sound в HUD. |
| Code | game.js:741-746; game.js:1262-1284 |
| Cause confidence | High |

## Potential Defects Requiring Runtime Confirmation

| ID | Наблюдение | Почему не confirmed | Связанный test |
| --- | --- | --- | --- |
| POT-001 | Bonus duration upgrade применяется к random bonus, но start boosters имеют fixed 6/8 seconds. | Design intent неизвестен. | TC-UPG-004 |
| POT-002 | Daily reward зависит только от local clock. | Нужно подтвердить anti-cheat requirement. | TC-DAILY-002 |
| POT-003 | Collision radius 36 значительно меньше bitmap footprint. | Нужно natural visual collision test. | TC-CORE-013 |
| POT-004 | Supplied root не содержит assets/; возможно flattening upload, а не package defect. | Нет release ZIP. | TC-BUILD-001 |
