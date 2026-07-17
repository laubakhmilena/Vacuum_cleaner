# CHK-20 — Release candidate

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-20-001 | Release ZIP assets | Release archive | Нет missing resources. | Critical | Manual/functional | NOT_RUN | Not executed. |  | TC-BUILD-001 |
| CHK-20-002 | Clean launch | Пустое mock localStorage | Меню активно; критические элементы видимы. | Critical | Manual/functional | PASS | See related test/report. |  | TC-SMOKE-001 |
| CHK-20-003 | No S1/S2 | Сборка запущена; доступна область «No S1/S2». | Сценарий «No S1/S2» выполняется предсказуемо, без crash, потери данных, блокировки управления и визуальных дефектов. | Critical | Manual/functional | FAIL | See related test/report. |  | Bug register |
| CHK-20-004 | Smoke | Сборка запущена; доступна область «Smoke». | Сценарий «Smoke» выполняется предсказуемо, без crash, потери данных, блокировки управления и визуальных дефектов. | High | Manual/functional | NOT_RUN | Есть частичное статическое/автоматизированное наблюдение; полная ручная проверка не выполнялась. |  | 11_SMOKE_SUITE |
| CHK-20-005 | Critical path natural | Fresh profile | Цикл завершен естественно без soft lock. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-012 |
| CHK-20-006 | Save corruption | JSON valid, dailyTasks=[null,null,null] | Invalid nested entries сбрасываются; menu функционально. | Critical | Manual/functional | FAIL | See related test/report. | BUG-001 | TC-SAVE-002 |
| CHK-20-007 | Yandex loader IT | Опубликованный draft/debug panel | Indicator IT; init succeeds. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-PLAT-001 |
| CHK-20-008 | Real ads | Yandex SDK, 3 completed rounds | Ad API called; game resumes/start after close/error. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-ADS-003..006 |
| CHK-20-009 | Mobile/desktop matrix | Чистое состояние | Back существует; panel scrollable при необходимости. | Medium | Manual/functional | NOT_RUN | Есть частичное статическое/автоматизированное наблюдение; полная ручная проверка не выполнялась. |  | TC-COMP-001..006 |
| CHK-20-010 | Known issues/verdict updated | Сборка запущена; доступна область «Known issues/verdict updated». | Сценарий «Known issues/verdict updated» выполняется предсказуемо, без crash, потери данных, блокировки управления и визуальных дефектов. | Medium | Manual/functional | PASS | See related test/report. |  | Docs |
