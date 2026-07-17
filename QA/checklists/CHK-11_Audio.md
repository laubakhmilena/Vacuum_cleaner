# CHK-11 — Audio

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-11-001 | Sound toggle state | Активный раунд | soundMuted=true; label Включить звук. | Critical | Manual/functional | PASS | See related test/report. |  | TC-AUDIO-001 |
| CHK-11-002 | Good cue | Audio enabled | Distinct correct cues; no overlap artifact. | Critical | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-003 |
| CHK-11-003 | Bad cue | Audio enabled | Distinct correct cues; no overlap artifact. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-003 |
| CHK-11-004 | Gold/combo/buy/over cues | Audio enabled | Distinct correct cues; no overlap artifact. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-003 |
| CHK-11-005 | Vacuum startup | Audio enabled | Distinct correct cues; no overlap artifact. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-003 |
| CHK-11-006 | Mute all sounds | Активный раунд | soundMuted=true; label Включить звук. | Medium | Manual/functional | NOT_RUN | Есть частичное статическое/автоматизированное наблюдение; полная ручная проверка не выполнялась. |  | TC-AUDIO-001 |
| CHK-11-007 | Audio in pause | Real browser/device | Sound stops immediately; resumes appropriately. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-002 |
| CHK-11-008 | Audio after Alt+Tab | Real browser/device | Sound stops immediately; resumes appropriately. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-002 |
| CHK-11-009 | No overlap/stuck loop | Active game | No exception/stuck sound. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-AUDIO-004 |
| CHK-11-010 | Volume control | Статический анализ исходного кода и интерфейса завершен. | Система отсутствует или неприменима для текущей версии; повторно оценить после добавления функции. | Medium | Manual/functional | NOT_APPLICABLE | See related test/report. |  | N/A |
