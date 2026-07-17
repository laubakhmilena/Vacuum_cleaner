# CHK-02 — Main menu and navigation

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-02-001 | Menu visible | Пустое mock localStorage | Меню активно; критические элементы видимы. | Critical | Manual/functional | PASS | See related test/report. |  | TC-SMOKE-001 |
| CHK-02-002 | Play transition | Меню | game, running=true, score=0, lives=3, combo=1. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-001 |
| CHK-02-003 | Upgrades/back | Меню | Переходы корректны; menu восстановлено. | High | Manual/functional | PASS | See related test/report. |  | TC-UI-001 |
| CHK-02-004 | Keyboard focus | Меню | Daily, Play, Upgrades получают фокус. | High | Manual/functional | PASS | See related test/report. |  | TC-ACC-001 |
| CHK-02-005 | Rapid clicks | Сборка запущена; доступна область «Rapid clicks». | Сценарий «Rapid clicks» выполняется предсказуемо, без crash, потери данных, блокировки управления и визуальных дефектов. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-UI-004 |
| CHK-02-006 | Double click daily | Награда сегодня не получена | +3; повтор недоступен; состояние восстановлено. | Medium | Manual/functional | PASS | See related test/report. |  | TC-DAILY-001 |
| CHK-02-007 | Impossible transitions | Сборка запущена; доступна область «Impossible transitions». | Сценарий «Impossible transitions» выполняется предсказуемо, без crash, потери данных, блокировки управления и визуальных дефектов. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-STATE-003 |
| CHK-02-008 | Menu during round confirmation | Boosters активированы | Есть подтверждение либо неиспользованные boosters возвращаются. | Critical | Manual/functional | FAIL | See related test/report. | BUG-004 | TC-BOOST-002 |
| CHK-02-009 | GameOver menu | Fresh profile | Цикл завершен естественно без soft lock. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-012 |
| CHK-02-010 | Back/browser gestures suppressed | Mobile/tablet | No distortion/lost state; input bounds update. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-COMP-008 |
