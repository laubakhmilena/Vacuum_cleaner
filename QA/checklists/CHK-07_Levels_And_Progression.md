# CHK-07 — Progression/economy

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-07-001 | No levels | Статический анализ исходного кода и интерфейса завершен. | Система отсутствует или неприменима для текущей версии; повторно оценить после добавления функции. | Critical | Manual/functional | NOT_APPLICABLE | See related test/report. |  | N/A |
| CHK-07-002 | Best score | score=250, lives=1 | gameOver; best≥250; earned=2. | Critical | Manual/functional | PASS | See related test/report. |  | TC-CORE-007 |
| CHK-07-003 | Score→stars boundaries | End game | 0,0,1,1,2 new stars. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-PROG-001 |
| CHK-07-004 | Daily reward | Награда сегодня не получена | +3; повтор недоступен; состояние восстановлено. | High | Manual/functional | PASS | See related test/report. |  | TC-DAILY-001 |
| CHK-07-005 | Daily tasks | Task selected | Clamp target; claim enabled exactly at target. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-DAILY-003..006 |
| CHK-07-006 | Permanent upgrades | Enough stars | Correct cost; level+1; persists. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-UPG-001..004 |
| CHK-07-007 | Booster activation | По 1 каждого | Counts 0; timers active; shield true. | Medium | Manual/functional | PASS | See related test/report. |  | TC-BOOST-001 |
| CHK-07-008 | Booster exit loss | Boosters активированы | Есть подтверждение либо неиспользованные boosters возвращаются. | Critical | Manual/functional | FAIL | See related test/report. | BUG-004 | TC-BOOST-002 |
| CHK-07-009 | Skins | Enough stars | Owned/active persisted; one debit. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-SKIN-001..003 |
| CHK-07-010 | Economy negative/large values | Injected save | No negative; finite values; UI usable. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-PROG-002 |
