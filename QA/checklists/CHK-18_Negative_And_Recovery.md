# CHK-18 — Negative/recovery

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-18-001 | Invalid JSON recovery | localStorage value=not-json | Игра запускается с defaults и warning. | Critical | Manual/functional | PASS | See related test/report. |  | TC-SAVE-001 |
| CHK-18-002 | Nested corrupt recovery | JSON valid, dailyTasks=[null,null,null] | Invalid nested entries сбрасываются; menu функционально. | Critical | Manual/functional | FAIL | See related test/report. | BUG-001 | TC-SAVE-002 |
| CHK-18-003 | Storage write failure | Mock setItem throw | Game continues; user informed or risk documented. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-SAVE-003 |
| CHK-18-004 | No SDK rewarded | gameOver; yaSdk=null; revive available | Без onRewarded reward не выдается; выводится error/retry. | Critical | Manual/functional | FAIL | See related test/report. | BUG-002 | TC-ADS-001..002 |
| CHK-18-005 | Ad onError recovery | Mock SDK onError | Game starts after error; no stuck audio/state. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-ADS-004..006 |
| CHK-18-006 | Missing image fallback | Remove/deny image in test copy | Fallback vacuum visible; warning only. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-GFX-001 |
| CHK-18-007 | Rapid UI input | Сборка запущена; подготовлено состояние, соответствующее исследовательской проверке. | Проверка не выявляет crash, зависание, soft-lock, потерю прогресса или необратимое состояние; наблюдения зафиксированы. | Medium | Manual/functional | NOT_RUN | Not executed. |  | EXP-03 |
| CHK-18-008 | Wrong action order | Сборка запущена; подготовлено состояние, соответствующее исследовательской проверке. | Проверка не выявляет crash, зависание, soft-lock, потерю прогресса или необратимое состояние; наблюдения зафиксированы. | Medium | Manual/functional | NOT_RUN | Not executed. |  | EXP-04 |
| CHK-18-009 | Focus loss | Desktop browser | Gameplay frozen; no damage; audio stopped/resumes. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-STATE-002 |
| CHK-18-010 | No network | Draft complete | No mandatory violations; evidence retained. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-PLAT-004 |
