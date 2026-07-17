# 00 — Инвентаризация проекта

**Дата анализа:** 2026-07-17  
**Версия:** `TV-cc6576a5764a`; Git metadata отсутствует.

## Краткое описание

| Параметр | Значение | Статус | Источник |
|---|---|---|---|
| Название | «Пылесос Пыслей» / `Thought Vacuum` | CONFIRMED | `index.html:6`, `game.js:80-177` |
| Жанр | Casual arcade / survival collector, endless round | INFERRED | Основной цикл и отсутствие levels |
| Аудитория | Широкая casual, визуально детская/семейная | INFERRED | Art/UI tone; возрастной рейтинг не указан |
| Основная механика | Перемещать пылесос указателем, собирать good/gold, избегать bad | CONFIRMED | Menu lead; `game.js:895-1044` |
| Условие победы | Фиксированной победы/финального уровня нет | NOT_APPLICABLE | Endless score loop |
| Поражение | Lives ≤ 0 | CONFIRMED | `game.js:1009-1019` |
| Прогресс | Best score, stars, upgrades, boosters, skins, daily | CONFIRMED | `game.js:554-608` |
| Управление | Pointer/mouse/touch; UI keyboard focus частично | CONFIRMED | `game.js:610-625`; DYN-007 |
| Обучение | Только текстовое описание на menu | CONFIRMED | `index.html:19` |
| Levels/scenes | 4 UI screens, уровней нет | CONFIRMED | `screens` object |
| Пауза | Автоматическая system pause, нет пользовательской pause screen | CONFIRMED | `game.js:415-460` |
| Settings | Только mute в игровом HUD | CONFIRMED | `game.js:2028-2047` |
| Save | localStorage | CONFIRMED | key `thoughtVacuumProgress.v1` |
| Audio | Web Audio synthesized cues | CONFIRMED | `game.js:1881-2027` |
| Localization | Russian/English | CONFIRMED | `TRANSLATIONS` |
| Network | Yandex SDK/ads; core game может работать без SDK | CONFIRMED | `index.html:11`; `game.js:444-552` |
| Achievements/accounts/IAP/UGC/mods | Не обнаружены | NOT_APPLICABLE | Source scan |
| Analytics/telemetry | GameplayAPI markers only; analytics SDK не обнаружен | CONFIRMED | `game.js:393-413` |
| Controller/TV remote | Не обнаружено | UNKNOWN/NOT_IMPLEMENTED | Input scan |
| Ads | Interstitial + rewarded | CONFIRMED | `game.js:462-552` |

## Технический стек

- HTML5/CSS/JavaScript ES2020+, Canvas 2D, Web Audio, localStorage.
- Движок: собственная browser loop на `requestAnimationFrame`; сторонний engine отсутствует.
- Build system/package manager: отсутствуют; static files.
- Entry point: `index.html` → `vacuum_player_data.js` → `game.js`.
- Target: Yandex Games web, desktop/mobile inferred from `/sdk.js`, responsive CSS and SDK calls.
- Dependencies: browser APIs и runtime-provided Yandex Games SDK.

## Файлы

| Файл | Назначение | Статус |
| --- | --- | --- |
| index.html | DOM screens/HUD, SDK/resource links | CONFIRMED |
| style.css | Responsive presentation and touch layout | CONFIRMED |
| game.js | All gameplay/state/economy/audio/integration | CONFIRMED |
| vacuum_player.png | Player art, 423×430 PNG | CONFIRMED |
| vacuum_player_data.js | Embedded data URI fallback/source | CONFIRMED |
| README/package.json/git | Не предоставлены | UNKNOWN |

## Пользовательские потоки

1. Launch → daily reward optional → Play → collect/avoid → gameOver → revive/x2/restart/menu.
2. Launch → Upgrades → buy permanent/booster/skin → back → Play.
3. Gameplay → system blur/visibility → automatic pause → resume.

## Неизвестные параметры

- Финальное официальное название и допустима ли форма «Пыслей».
- Реальный Yandex app ID, draft settings, supported device types/orientations.
- Требования к score balance, session length, FPS, memory.
- Intended behavior for offline SDK and for quitting with boosters.
- Release archive structure; supplied upload flattened `assets`.

## Предположения

| ID | Предположение | Риск |
| --- | --- | --- |
| ASM-001 | Yandex Games — основная платформа | High if wrong |
| ASM-002 | Endless score loop intentionally has no win | Medium |
| ASM-003 | Reward requires actual onRewarded callback | High |
| ASM-004 | Player should remain mostly visible at edges | Low/UX |
| ASM-005 | One developer maintains all QA docs | Confirmed by task |
