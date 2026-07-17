# QA-комплект: «Пылесос Пыслей» / Thought Vacuum

**Проверенная версия:** `TV-cc6576a5764a`  
**Дата:** 2026-07-17  
**Release verdict:** **NO-GO** — открыты два `S2`, один `S3`, один `S4`; реальная Yandex-среда не проверена.

## С чего начать

1. Прочитать [20_RELEASE_READINESS_REPORT.md](20_RELEASE_READINESS_REPORT.md).
2. Исправить `BUG-002`, затем `BUG-001`, затем `BUG-004`.
3. Выполнить [11_SMOKE_SUITE.md](11_SMOKE_SUITE.md) и Critical Regression из [12_REGRESSION_SUITE.md](12_REGRESSION_SUITE.md).
4. Зафиксировать retest в [19_TEST_EXECUTION_REPORT.md](19_TEST_EXECUTION_REPORT.md).

## Что находится в папке

- Инвентаризация и модель: `00`–`05`.
- Стратегия, риски, план: `06`–`08`.
- Чек-листы и тесты: `09`–`13`, `checklists/`.
- Дефекты и специальные отчеты: `14`–`18`.
- Итоги и процесс релиза: `19`–`25`.
- Интернет-источники: `26_SOURCES.md`.
- Доказательства: `evidence/`; логи: `logs/`; изолированные материалы: `work/`.

## Быстрые маршруты

### У меня 10 минут

Выполнить `TC-SMOKE-001`, `TC-CORE-001`, `TC-CORE-003`, `TC-CORE-007`, `TC-CORE-008`, проверить console. Если изменялись реклама или сохранение, добавить `TC-ADS-001/002` и `TC-SAVE-001/002`.

### Я изменил игровую механику

Выполнить Critical Regression: scoring/combo, good/bad/gold, lives/shield, gameOver/restart; затем charter `EXP-02` и `EXP-05`.

### Я исправил баг

Повторить точные шаги из `14_BUG_REPORTS.md`, сохранить новое доказательство, затем выполнить связанные test cases и соседние функции из Traceability Matrix.

### Я готовлю релиз

Build Verification → Smoke → Critical Regression → Core Regression → natural full-cycle session → реальная Yandex SDK/ad проверка → viewport/mobile → accessibility quick wins → Release Readiness.

## Что фактически проверено

32 browser interaction/static-state checks через Chromium harness: 27 продуктовых проверок `PASS`, 5 `FAIL`; 2 platform cases `BLOCKED`; остальное `NOT_RUN`. Harness использовал неизмененный `game.js`, кроме тестовой подстановки base URL и in-memory localStorage, поскольку политика окружения блокировала прямую навигацию браузера.

## Что не проверено

Реальные Yandex loader/ads, production ZIP, реальные Chrome/Firefox/Safari devices, audible audio quality, FPS/CPU/GPU/memory, 30-minute soak, controller/TV remote, screen reader.
