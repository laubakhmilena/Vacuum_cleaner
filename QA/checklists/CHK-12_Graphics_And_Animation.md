# CHK-12 — Graphics and animation

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-12-001 | Player bitmap | Пустое mock localStorage | Меню активно; критические элементы видимы. | Critical | Manual/functional | PASS | See related test/report. |  | TC-SMOKE-001 |
| CHK-12-002 | Image fallback | Remove/deny image in test copy | Fallback vacuum visible; warning only. | Critical | Manual/functional | NOT_RUN | Not executed. |  | TC-GFX-001 |
| CHK-12-003 | Thought emojis | Natural play | Good/bad/gold появляются; нет невозможных positions. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-009 |
| CHK-12-004 | Particles | combo=1, timers=0 | score +50; один timer >0. | High | Manual/functional | NOT_RUN | Есть частичное статическое/автоматизированное наблюдение; полная ручная проверка не выполнялась. |  | TC-CORE-005 |
| CHK-12-005 | Edge clipping | Активный раунд | Основная часть sprite и feedback остаются видимыми. | Critical | Manual/functional | FAIL | See related test/report. | BUG-003 | TC-UI-002 |
| CHK-12-006 | Skin visuals | All owned | Skins visually distinct; gameplay meaning unchanged. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-SKIN-003 |
| CHK-12-007 | Aspect ratios | Чистое состояние | Back существует; panel scrollable при необходимости. | Medium | Manual/functional | PASS | See related test/report. |  | TC-COMP-001..005 |
| CHK-12-008 | Camera shake | Bad collision | Shake can be reduced/disabled. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-ACC-004 |
| CHK-12-009 | Animation transitions | Меню | Переходы корректны; menu восстановлено. | Medium | Manual/functional | NOT_RUN | Есть частичное статическое/автоматизированное наблюдение; полная ручная проверка не выполнялась. |  | TC-UI-001 |
| CHK-12-010 | Missing texture warning | Remove/deny image in test copy | Fallback vacuum visible; warning only. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-GFX-001 |
