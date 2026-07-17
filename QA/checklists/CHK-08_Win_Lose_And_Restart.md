# CHK-08 — Win/lose/restart

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-08-001 | Win condition absent | Статический анализ исходного кода и интерфейса завершен. | Система отсутствует или неприменима для текущей версии; повторно оценить после добавления функции. | Critical | Manual/functional | NOT_APPLICABLE | See related test/report. |  | N/A |
| CHK-08-002 | Lose at 0 lives | score=250, lives=1 | gameOver; best≥250; earned=2. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-007 |
| CHK-08-003 | Restart clean | gameOver | score=0, lives=3, combo=1, running. | High | Manual/functional | PASS | See related test/report. |  | TC-CORE-008 |
| CHK-08-004 | Revive one time | Yandex SDK | Reward only rewarded path; buttons recover. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-ADS-005 |
| CHK-08-005 | Revive fallback integrity | gameOver; yaSdk=null; revive available | Без onRewarded reward не выдается; выводится error/retry. | Critical | Manual/functional | FAIL | See related test/report. | BUG-002 | TC-ADS-001 |
| CHK-08-006 | Double stars integrity | gameOver; earned>0; yaSdk=null | Без onRewarded reward не выдается. | Critical | Manual/functional | FAIL | See related test/report. | BUG-002 | TC-ADS-002 |
| CHK-08-007 | Second death after revive | Yandex SDK | Reward only rewarded path; buttons recover. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-ADS-005 |
| CHK-08-008 | Interstitial threshold | Yandex SDK, 3 completed rounds | Ad API called; game resumes/start after close/error. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-ADS-003 |
| CHK-08-009 | Menu from results | Fresh profile | Цикл завершен естественно без soft lock. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-CORE-012 |
| CHK-08-010 | Rapid result buttons | Yandex SDK | Stars added once only on reward. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-ADS-006 |
