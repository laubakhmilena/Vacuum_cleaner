# 11 — Smoke Suite

## Цель

За минимальное число шагов определить, пригодна ли сборка для дальнейшего тестирования.

| Порядок | Test | Текущий статус | Критерий |
| --- | --- | --- | --- |
| 1 | TC-BUILD-001 | NOT_RUN | Release package resources resolve |
| 2 | TC-SMOKE-001 | PASS | Menu launches |
| 3 | TC-CORE-001 | PASS | Round starts |
| 4 | TC-INPUT-002 | NOT_RUN | Real input controllable |
| 5 | TC-CORE-002/003 | PASS | Good/bad core reactions |
| 6 | TC-CORE-007 | PASS | GameOver works |
| 7 | TC-CORE-008 | PASS | Restart works |
| 8 | TC-STATE-002 | NOT_RUN | Real pause/background |
| 9 | TC-SAVE-002 | FAIL | Corrupt save does not block |
| 10 | TC-PLAT-001 | BLOCKED | Yandex SDK loader IT |

**Smoke verdict:** FAIL/INCOMPLETE. BUG-001 fails resilience; real input/platform cases remain.
