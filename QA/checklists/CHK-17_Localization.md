# CHK-17 — Localization

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-17-001 | RU auto | Чистое состояние | ru/be/kk/uk/uz→ru; прочие→en. | Critical | Manual/functional | PASS | See related test/report. |  | TC-LOC-002 |
| CHK-17-002 | EN auto | Чистое состояние | UI English; lang=en. | Critical | Manual/functional | PASS | See related test/report. |  | TC-LOC-001 |
| CHK-17-003 | Language mapping | Чистое состояние | ru/be/kk/uk/uz→ru; прочие→en. | High | Manual/functional | PASS | See related test/report. |  | TC-LOC-002 |
| CHK-17-004 | Full RU audit | All screens | No English/raw keys. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-LOC-003 |
| CHK-17-005 | Full EN audit | All screens | No Russian/raw keys/overflow. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-LOC-004 |
| CHK-17-006 | Long strings | Instrumented strings | No clipping/overlap; scroll available. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-LOC-005 |
| CHK-17-007 | Variables/plurals | All screens | No English/raw keys. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-LOC-003 |
| CHK-17-008 | Dates/numbers | Near local midnight | Tasks reset consistently; old reward state handled. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-DAILY-006 |
| CHK-17-009 | Text on images | Статический анализ исходного кода и интерфейса завершен. | Система отсутствует или неприменима для текущей версии; повторно оценить после добавления функции. | Medium | Manual/functional | NOT_APPLICABLE | See related test/report. |  | N/A |
| CHK-17-010 | Title spelling | Сборка запущена; доступна область «Title spelling». | Сценарий «Title spelling» выполняется предсказуемо, без crash, потери данных, блокировки управления и визуальных дефектов. | Medium | Manual/functional | NOT_RUN | Ожидаемое поведение или окружение требует уточнения; фактическая проверка не выполнялась. |  | Open question |
