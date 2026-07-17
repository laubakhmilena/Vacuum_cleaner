# CHK-01 — Installation and first launch

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-01-001 | Чистый запуск из release package | Пустое mock localStorage | Меню активно; критические элементы видимы. | Critical | Manual/functional | PASS | See related test/report. |  | TC-SMOKE-001 |
| CHK-01-002 | Повторный запуск с сохранением | Награда сегодня не получена | +3; повтор недоступен; состояние восстановлено. | Critical | Manual/functional | PASS | See related test/report. |  | TC-DAILY-001 |
| CHK-01-003 | Запуск после crash | Normal profile | Latest consistent state, no partial corruption. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-SAVE-004 |
| CHK-01-004 | Невалидный JSON | localStorage value=not-json | Игра запускается с defaults и warning. | High | Manual/functional | PASS | See related test/report. |  | TC-SAVE-001 |
| CHK-01-005 | Структурно поврежденный save | JSON valid, dailyTasks=[null,null,null] | Invalid nested entries сбрасываются; menu функционально. | Critical | Manual/functional | FAIL | See related test/report. | BUG-001 | TC-SAVE-002 |
| CHK-01-006 | Отсутствующие asset files | Remove/deny image in test copy | Fallback vacuum visible; warning only. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-GFX-001 |
| CHK-01-007 | SDK loader IT | Опубликованный draft/debug panel | Indicator IT; init succeeds. | Critical | Manual/functional | BLOCKED | See related test/report. |  | TC-PLAT-001 |
| CHK-01-008 | Корректное закрытие/повторное открытие | Normal profile | Latest consistent state, no partial corruption. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-SAVE-004 |
| CHK-01-009 | Создание storage entry | Награда сегодня не получена | +3; повтор недоступен; состояние восстановлено. | Medium | Manual/functional | PASS | See related test/report. |  | TC-DAILY-001 |
| CHK-01-010 | Ошибки в console | Игра загружена | Функции и state доступны. | Medium | Manual/functional | PASS | See related test/report. |  | TC-SMOKE-002 |
