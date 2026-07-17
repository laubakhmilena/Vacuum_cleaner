# CHK-05 — UI and HUD

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-05-001 | Score/lives/combo initial | Меню | game, running=true, score=0, lives=3, combo=1. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-001 |
| CHK-05-002 | HUD updates | Активный раунд | score=50, streak=5, combo=2. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-002 |
| CHK-05-003 | Bonus pill | combo=1, timers=0 | score +50; один timer >0. | High | Manual/functional | PASS | See related test/report. |  | TC-CORE-005 |
| CHK-05-004 | Small viewports | Чистое состояние | Back существует; panel scrollable при необходимости. | High | Manual/functional | PASS | See related test/report. |  | TC-COMP-001..002 |
| CHK-05-005 | Tablet/desktop | Чистое состояние | Back существует; panel scrollable при необходимости. | High | Manual/functional | PASS | See related test/report. |  | TC-COMP-003..005 |
| CHK-05-006 | Touch scroll | Mobile emulation, touch | scrollTop увеличивается. | Medium | Manual/functional | PASS | See related test/report. |  | TC-COMP-006 |
| CHK-05-007 | Player fully visible | Активный раунд | Основная часть sprite и feedback остаются видимыми. | Critical | Manual/functional | FAIL | See related test/report. | BUG-003 | TC-UI-002 |
| CHK-05-008 | Large counter values | Injected save | No negative; finite values; UI usable. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-PROG-002 |
| CHK-05-009 | Disabled controls | stars=cost-1 | No debit/level change. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-UPG-003 |
| CHK-05-010 | Focus visibility | Меню | Daily, Play, Upgrades получают фокус. | Medium | Manual/functional | NOT_RUN | Есть частичное статическое/автоматизированное наблюдение; полная ручная проверка не выполнялась. |  | TC-ACC-001 |
