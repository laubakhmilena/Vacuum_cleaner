# CHK-04 — Controls and input

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-04-001 | Pointer boundaries | Активный раунд | 20,20 и 1004,748. | Critical | Manual/functional | PASS | See related test/report. |  | TC-INPUT-001 |
| CHK-04-002 | Real mouse feel | Playable runtime | Точный и предсказуемый контроль. | Critical | Manual/functional | NOT_RUN | Not executed. |  | TC-INPUT-002 |
| CHK-04-003 | Touch drag | Playable runtime | Точный и предсказуемый контроль. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-INPUT-002 |
| CHK-04-004 | Multi-touch | Mobile device | Нет скачков/залипания. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-INPUT-003 |
| CHK-04-005 | Keyboard gameplay | Desktop | Поддерживаемая альтернатива либо явно N/A по design. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-INPUT-004 |
| CHK-04-006 | Rapid input | Сборка запущена; подготовлено состояние, соответствующее исследовательской проверке. | Проверка не выявляет crash, зависание, soft-lock, потерю прогресса или необратимое состояние; наблюдения зафиксированы. | Medium | Manual/functional | NOT_RUN | Not executed. |  | EXP-03 |
| CHK-04-007 | Conflicting input | Mobile device | Нет скачков/залипания. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-INPUT-003 |
| CHK-04-008 | Input during pause | Desktop browser | Gameplay frozen; no damage; audio stopped/resumes. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-STATE-002 |
| CHK-04-009 | Input on result | Yandex SDK | Reward only rewarded path; buttons recover. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-ADS-005 |
| CHK-04-010 | Controller disconnect | Статический анализ исходного кода и интерфейса завершен. | Система отсутствует или неприменима для текущей версии; повторно оценить после добавления функции. | Medium | Manual/functional | NOT_APPLICABLE | See related test/report. |  | N/A |
