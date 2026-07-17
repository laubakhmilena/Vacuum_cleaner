# CHK-03 — Core gameplay

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-03-001 | Start state | Меню | game, running=true, score=0, lives=3, combo=1. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-001 |
| CHK-03-002 | Good scoring | Активный раунд | score=50, streak=5, combo=2. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-002 |
| CHK-03-003 | Bad damage | 3 жизни, no shield | lives=2; combo=1; streak=0. | High | Manual/functional | PASS | See related test/report. |  | TC-CORE-003 |
| CHK-03-004 | Shield | 3 жизни, shield=true | lives=3; shield=false. | High | Manual/functional | PASS | See related test/report. |  | TC-CORE-004 |
| CHK-03-005 | Gold bonus | combo=1, timers=0 | score +50; один timer >0. | High | Manual/functional | PASS | See related test/report. |  | TC-CORE-005 |
| CHK-03-006 | Double×combo | combo=2, double=active | 10×2×2=40. | Medium | Manual/functional | PASS | See related test/report. |  | TC-CORE-006 |
| CHK-03-007 | Spawn types | Natural play | Good/bad/gold появляются; нет невозможных positions. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-009 |
| CHK-03-008 | Suction/repulsion | Magnet active | Good/gold toward; bad away; no teleport. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-011 |
| CHK-03-009 | Natural full loop | Fresh profile | Цикл завершен естественно без soft lock. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-012 |
| CHK-03-010 | Soft-lock attempt | Сборка запущена; подготовлено состояние, соответствующее исследовательской проверке. | Проверка не выявляет crash, зависание, soft-lock, потерю прогресса или необратимое состояние; наблюдения зафиксированы. | Medium | Manual/functional | NOT_RUN | Not executed. |  | EXP-15 |
