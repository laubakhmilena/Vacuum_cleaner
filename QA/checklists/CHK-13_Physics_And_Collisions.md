# CHK-13 — Physics/collisions

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-13-001 | Good collision | Активный раунд | score=50, streak=5, combo=2. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-002 |
| CHK-13-002 | Bad collision | 3 жизни, no shield | lives=2; combo=1; streak=0. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-003 |
| CHK-13-003 | Gold collision | combo=1, timers=0 | score +50; один timer >0. | High | Manual/functional | PASS | See related test/report. |  | TC-CORE-005 |
| CHK-13-004 | Shield decision | 3 жизни, shield=true | lives=3; shield=false. | High | Manual/functional | PASS | See related test/report. |  | TC-CORE-004 |
| CHK-13-005 | Suction radius boundary | Magnet active | Good/gold toward; bad away; no teleport. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-011 |
| CHK-13-006 | Magnet bad repulsion | Magnet active | Good/gold toward; bad away; no teleport. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-011 |
| CHK-13-007 | Visual hitbox match | Active round | Collision соответствует визуальному ожиданию. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-013 |
| CHK-13-008 | Out-of-bounds thought removal | Long round | Pace ускоряется и не ниже 0.38 base range. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-010 |
| CHK-13-009 | High-speed tunneling | Сборка запущена; подготовлено состояние, соответствующее исследовательской проверке. | Проверка не выявляет crash, зависание, soft-lock, потерю прогресса или необратимое состояние; наблюдения зафиксированы. | Medium | Manual/functional | NOT_RUN | Not executed. |  | EXP-03 |
| CHK-13-010 | Player boundary clipping | Активный раунд | Основная часть sprite и feedback остаются видимыми. | Critical | Manual/functional | FAIL | See related test/report. | BUG-003 | TC-UI-002 |
