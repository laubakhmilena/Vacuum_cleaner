# CHK-14 — Performance/stability

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-14-001 | JS syntax | Игра загружена | Функции и state доступны. | Critical | Manual/functional | PASS | See related test/report. |  | TC-SMOKE-002 |
| CHK-14-002 | Simulated update stress | Активный game; spawn disabled for isolation | Нет exception/NaN; running remains true. | Critical | Manual/functional | PASS | See related test/report. |  | TC-PERF-001 |
| CHK-14-003 | Real 30-min soak | Production-like runtime | No unbounded growth/crash; thresholds documented. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-PERF-002 |
| CHK-14-004 | FPS/frame time | Profiler available | No unacceptable long frames per accepted target. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-PERF-003 |
| CHK-14-005 | Memory growth | Production-like runtime | No unbounded growth/crash; thresholds documented. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-PERF-002 |
| CHK-14-006 | Repeated restart | Сборка запущена; подготовлено состояние, соответствующее исследовательской проверке. | Проверка не выявляет crash, зависание, soft-lock, потерю прогресса или необратимое состояние; наблюдения зафиксированы. | Medium | Manual/functional | NOT_RUN | Not executed. |  | EXP-08 |
| CHK-14-007 | Mass particles | Profiler available | No unacceptable long frames per accepted target. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-PERF-003 |
| CHK-14-008 | Resize stress | Mobile/tablet | No distortion/lost state; input bounds update. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-COMP-008 |
| CHK-14-009 | Audio object lifecycle | Active game | No exception/stuck sound. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-004 |
| CHK-14-010 | Crash logs | JSON valid, dailyTasks=[null,null,null] | Invalid nested entries сбрасываются; menu функционально. | Critical | Manual/functional | FAIL | See related test/report. | BUG-001 | TC-SAVE-002 |
