# CHK-09 — Save/load/persistence

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-09-001 | First save | Награда сегодня не получена | +3; повтор недоступен; состояние восстановлено. | Critical | Manual/functional | PASS | See related test/report. |  | TC-DAILY-001 |
| CHK-09-002 | Reload valid state | Награда сегодня не получена | +3; повтор недоступен; состояние восстановлено. | Critical | Manual/functional | PASS | See related test/report. |  | TC-DAILY-001 |
| CHK-09-003 | Invalid JSON | localStorage value=not-json | Игра запускается с defaults и warning. | High | Manual/functional | PASS | See related test/report. |  | TC-SAVE-001 |
| CHK-09-004 | Nested corruption | JSON valid, dailyTasks=[null,null,null] | Invalid nested entries сбрасываются; menu функционально. | Critical | Manual/functional | FAIL | See related test/report. | BUG-001 | TC-SAVE-002 |
| CHK-09-005 | Write failure | Mock setItem throw | Game continues; user informed or risk documented. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-SAVE-003 |
| CHK-09-006 | Sequential saves | Normal profile | Latest consistent state, no partial corruption. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-SAVE-004 |
| CHK-09-007 | Settings persistence | Активный раунд | soundMuted=true; label Включить звук. | Medium | Manual/functional | PASS | See related test/report. |  | TC-AUDIO-001 |
| CHK-09-008 | Store persistence | Enough stars | Owned/active persisted; one debit. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-SKIN-001 |
| CHK-09-009 | Close during save | Normal profile | Latest consistent state, no partial corruption. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-SAVE-004 |
| CHK-09-010 | Cross-device/cloud | Статический анализ исходного кода и интерфейса завершен. | Система отсутствует или неприменима для текущей версии; повторно оценить после добавления функции. | Medium | Manual/functional | NOT_APPLICABLE | See related test/report. |  | N/A |
