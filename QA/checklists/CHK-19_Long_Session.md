# CHK-19 — Long session

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-19-001 | 100s simulated update | Активный game; spawn disabled for isolation | Нет exception/NaN; running remains true. | Critical | Manual/functional | PASS | See related test/report. |  | TC-PERF-001 |
| CHK-19-002 | 30-min natural session | Production-like runtime | No unbounded growth/crash; thresholds documented. | Critical | Manual/functional | NOT_RUN | Not executed. |  | TC-PERF-002 |
| CHK-19-003 | Memory samples | Production-like runtime | No unbounded growth/crash; thresholds documented. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-PERF-002 |
| CHK-19-004 | FPS samples | Profiler available | No unacceptable long frames per accepted target. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-PERF-003 |
| CHK-19-005 | Long score/counter | Injected save | No negative; finite values; UI usable. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-PROG-002 |
| CHK-19-006 | Spawn pace minimum | Long round | Pace ускоряется и не ниже 0.38 base range. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-010 |
| CHK-19-007 | Daily rollover | Near local midnight | Tasks reset consistently; old reward state handled. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-DAILY-006 |
| CHK-19-008 | Repeated ads | Yandex SDK, 3 completed rounds | Ad API called; game resumes/start after close/error. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-ADS-003..006 |
| CHK-19-009 | Repeated restarts | Сборка запущена; подготовлено состояние, соответствующее исследовательской проверке. | Проверка не выявляет crash, зависание, soft-lock, потерю прогресса или необратимое состояние; наблюдения зафиксированы. | Medium | Manual/functional | NOT_RUN | Not executed. |  | EXP-08 |
| CHK-19-010 | Audio stability | Active game | No exception/stuck sound. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-004 |
