# 08 — Полный тест-план

| Поле | Значение |
|---|---|
| Document ID | `TP-TV-001` |
| Version | 1.1 |
| Date | 2026-07-17 |
| Test build | `TV-cc6576a5764a` |
| Product | «Пылесос Пыслей» / Thought Vacuum |
| Owner | Один разработчик; самостоятельная QA-проверка |
| Status | Active; release verdict находится в `20_RELEASE_READINESS_REPORT.md` |

## 1. Цели

Подтвердить, что сборка запускается, основной бесконечный игровой цикл работает без блокировки, прогресс и экономика не повреждаются, рекламные награды выдаются корректно, управление и интерфейс остаются пригодными на поддерживаемых экранах, а критические platform-интеграции готовы к публикации.

## 2. Область тестирования

**Входит:** HTML/CSS/JavaScript package; Canvas 2D gameplay; menu/upgrades/game/gameOver; pointer/touch input; score/combo/lives; good/bad/gold thoughts; temporary bonuses; permanent upgrades; consumable boosters; skins; daily reward/tasks; localStorage; RU/EN; synthesized audio; pause on focus/visibility; Yandex SDK branches; responsive layout; recovery, accessibility, stability and compatibility risks.

**Не входит как подтвержденное без отдельного окружения:** модерация и закрытые platform requirements; реальные рекламные показы/inventory; лидерборды и cloud save, которых в реализации нет; платежи, accounts, multiplayer, achievements, UGC; полноценная security-аудит/penetration test; сертификация accessibility; аппаратная производительность на device lab.

## 3. Тестовые объекты

| Объект | Основные файлы/источники | Критичность |
|---|---|---|
| Entry/package | `index.html`, asset paths, `/sdk.js` | Critical |
| Runtime/game loop | `game.js`, `requestAnimationFrame`, state object | Critical |
| UI/layout | `index.html`, `style.css` | High |
| Persistence | `localStorage`, key `thoughtVacuumProgress.v1` | Critical |
| Economy/progression | stars, upgrades, boosters, skins, daily state | Critical |
| Ads/platform | Yandex SDK init, LoadingAPI, GameplayAPI, interstitial/rewarded | Critical |
| Media/localization | image assets, Web Audio, RU/EN dictionaries | Medium/High |

## 4. Платформы и окружения

Базовое окружение описано в `01_TEST_ENVIRONMENT.md`. Текущий анализ использовал Chromium 144 headless и viewport-матрицу. Для release candidate обязательны реальные актуальные Chrome desktop, Chrome/Android и Safari/iOS либо официально утвержденный меньший target set; Firefox — если заявлена широкая web-поддержка. Реальная Yandex draft/debug-среда обязательна для platform и ads tests.

## 5. Тестовые данные

- чистый профиль без localStorage;
- валидный профиль с best score, stars, upgrades, boosters и skins;
- invalid JSON и валидный JSON с поврежденной nested-структурой;
- score boundaries `0/99/100/199/200`, combo boundaries, lives `0/1/max`;
- booster inventory `0/1/3/>3` через безопасную инъекцию test state;
- RU, EN и неизвестный language code;
- viewports `320×568`, `360×640`, `768×1024`, `1366×768`, `1920×1080`;
- SDK outcomes: unavailable, init error, open, reward, close-without-reward, ad error.

Перед destructive save tests необходимо экспортировать site data или использовать отдельный browser profile.

## 6. Типы тестирования и техники

Build verification, smoke, functional, integration, state-transition, negative/recovery, exploratory, usability, accessibility review, localization, compatibility, stability/performance profiling, regression и release-candidate verification. Применяются equivalence partitioning, boundary value analysis, decision tables, state models, user journeys, pairwise viewport/input combinations, error guessing и session-based exploratory testing.

## 7. Порядок выполнения

1. Build Verification Test.
2. Smoke.
3. Критический путь: launch → play → score/damage → gameOver → reward calculation → restart/menu.
4. Functional и negative tests по Feature/Risk Matrix.
5. Exploratory charters.
6. Save/state/recovery.
7. UI/UX и accessibility.
8. Performance/stability и compatibility.
9. Retest исправлений.
10. Risk-based regression.
11. Release Candidate на реальном package и Yandex draft.

## 8. Зависимости

Корректная структура `assets/`; браузер с Canvas/Web Audio/localStorage; загрузка `/sdk.js` в Yandex-среде; доступные рекламные placements; стабильный Build ID; возможность очистить/подменить test profile. Изменение SDK, save schema, scoring или store автоматически расширяет regression scope.

## 9. Основные риски

Приоритет имеют startup/save corruption, reward/economy bypass, невозможность закончить/перезапустить раунд, потеря consumables, неправильные score/lives/combo, focus/ad state race, mobile input/layout, asset loading и platform lifecycle. Полный перечень и порядок — `07_RISK_REGISTER.md`.

## 10. Критерии входа

- исходный набор файлов идентифицирован и hash зафиксирован;
- существует воспроизводимая команда/процедура запуска;
- test profile можно изолировать и восстановить;
- критические assets доступны;
- scope и build не меняются во время execution либо изменение зарегистрировано.

## 11. Критерии выхода

- BVT, Smoke и Critical Regression завершены;
- нет открытых S1/S2 без письменного risk acceptance;
- startup, save corruption, natural core loop, ads reward integrity и mobile input проверены;
- реальные LoadingAPI/GameplayAPI/ads paths пройдены в Yandex draft;
- все FAIL имеют Bug ID, все BLOCKED — причину и следующее действие;
- release report обновлен, evidence сохранены.

## 12. Остановка и возобновление

**Остановить**, если clean launch невозможен, обнаружена массовая потеря/повреждение прогресса, окружение или build изменились, evidence недостоверны, либо дефект S1 делает последующие результаты бессмысленными. **Возобновить** после фиксации нового Build ID, восстановления test data, устранения blocker и повторного BVT/Smoke затронутой области.

## 13. Отчетность и доказательства

`10_TEST_CASES.csv` — источник статусов test cases; `19_TEST_EXECUTION_REPORT.md` — итог прогона; `14_BUG_REPORTS.*` — confirmed defects; `evidence/` и `logs/` — доказательства. Имя нового evidence должно включать Test/Bug ID и build/date. Предположение не переводится в FAIL до воспроизведения против определенного oracle.

## 14. Severity и Priority

- `S1 Blocker`: продукт/платформа недоступны для всех, разрушительная потеря данных без обхода.
- `S2 Critical`: критический путь, startup части пользователей, экономика/монетизация или серьезная потеря прогресса.
- `S3 Major`: значимая функция нарушена, но есть обход или ограниченный охват.
- `S4 Minor`: косметика/локальное неудобство без нарушения основного цикла.

`P0–P3` задают порядок исправления с учетом reach, release proximity, workaround, monetization и regression risk; Priority не заменяет Severity.

## 15. Smoke-план

Запуск clean profile; menu и Play; движение; good/bad/gold; HUD; gameOver; restart/menu; сохранение/reload; отсутствие uncaught errors. При изменениях рекламы — safe no-reward on unavailable/error и one-time reward on callback. Полный набор — `11_SMOKE_SUITE.md`.

## 16. Regression-план

- **Critical:** startup/save/ads/core/gameOver/restart.
- **Core:** плюс input/state/economy/daily/upgrades/boosters.
- **Extended:** UI/audio/localization/viewports/recovery.
- **Full:** все 83 test cases, 20 checklists и relevant charters.

Выбор tier зависит от измененных файлов/функций и риска; матрица — `12_REGRESSION_SUITE.md` и `18_TRACEABILITY_MATRIX.*`.

## 17. Exploratory-план

Сессии 30–60 минут с charter, timebox, test data, notes, evidence и debrief. В первую очередь: rapid input/state races, save abuse, economy exploits, edge/collision behavior, mobile ergonomics, ads lifecycle и long-session degradation. Charters — `13_EXPLORATORY_TEST_CHARTERS.md`.

## 18. Retest исправлений

1. Подтвердить новый Build ID и точный fix scope.
2. Повторить исходные steps/data/environment.
3. Проверить expected result и отсутствие side effects.
4. Выполнить связанные Feature/Risk tests и соседний regression tier.
5. Не закрывать bug без evidence; статус `Cannot Reproduce` требует перечисления отличий окружения.

## 19. Ограничения текущего прогона

Direct browser navigation заблокирована политикой sandbox; использован изолированный harness. Реальные SDK/ads, audible audio, natural long play, FPS/memory, physical devices, screen reader и production ZIP не проверены. Эти gaps не заменяются статическим анализом и остаются `BLOCKED`/`NOT_RUN`.

## 20. Открытые вопросы и процесс для одного разработчика

Решения по target browsers/devices, performance targets, keyboard alternative, anti-cheat, ad fallback и booster exit policy находятся в `24_OPEN_QUESTIONS.md`. Ежедневный минимальный процесс: BVT → 10-minute smoke → test changed feature → adjacent risk regression → update bug/evidence → release gate. Подробно — `21_SOLO_DEVELOPER_QA_WORKFLOW.md`.
