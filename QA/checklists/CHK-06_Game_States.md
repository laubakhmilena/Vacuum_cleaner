# CHK-06 — Game states

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-06-001 | menu→game | Меню | game, running=true, score=0, lives=3, combo=1. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-001 |
| CHK-06-002 | game→gameOver | score=250, lives=1 | gameOver; best≥250; earned=2. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-007 |
| CHK-06-003 | gameOver→game | gameOver | score=0, lives=3, combo=1, running. | High | Manual/functional | PASS | See related test/report. |  | TC-CORE-008 |
| CHK-06-004 | menu↔upgrades | Меню | Переходы корректны; menu восстановлено. | High | Manual/functional | PASS | See related test/report. |  | TC-UI-001 |
| CHK-06-005 | System pause API | Активный раунд | running false→true; reason очищен. | High | Manual/functional | PASS | See related test/report. |  | TC-STATE-001 |
| CHK-06-006 | Real Alt+Tab | Desktop browser | Gameplay frozen; no damage; audio stopped/resumes. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-STATE-002 |
| CHK-06-007 | Ad open/close | Yandex SDK | Reward only rewarded path; buttons recover. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-ADS-005 |
| CHK-06-008 | Menu during game | Boosters активированы | Есть подтверждение либо неиспользованные boosters возвращаются. | Critical | Manual/functional | FAIL | See related test/report. | BUG-004 | TC-BOOST-002 |
| CHK-06-009 | Visibility event order | Desktop browser | Gameplay frozen; no damage; audio stopped/resumes. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-STATE-002 |
| CHK-06-010 | Repeated restart | Сборка запущена; подготовлено состояние, соответствующее исследовательской проверке. | Проверка не выявляет crash, зависание, soft-lock, потерю прогресса или необратимое состояние; наблюдения зафиксированы. | Medium | Manual/functional | NOT_RUN | Not executed. |  | EXP-08 |
