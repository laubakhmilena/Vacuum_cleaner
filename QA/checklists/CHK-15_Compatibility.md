# CHK-15 — Compatibility

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-15-001 | 320×568 | Чистое состояние | Back существует; panel scrollable при необходимости. | Critical | Manual/functional | PASS | See related test/report. |  | TC-COMP-001 |
| CHK-15-002 | 360×640 | Чистое состояние | Back существует; panel scrollable при необходимости. | Critical | Manual/functional | PASS | See related test/report. |  | TC-COMP-002 |
| CHK-15-003 | 768×1024 | Чистое состояние | Back существует; panel scrollable при необходимости. | High | Manual/functional | PASS | See related test/report. |  | TC-COMP-003 |
| CHK-15-004 | 1366×768 | Чистое состояние | Back существует; panel scrollable при необходимости. | High | Manual/functional | PASS | See related test/report. |  | TC-COMP-004 |
| CHK-15-005 | 1920×1080 | Чистое состояние | Back существует; panel scrollable при необходимости. | High | Manual/functional | PASS | See related test/report. |  | TC-COMP-005 |
| CHK-15-006 | Touch scroll | Mobile emulation, touch | scrollTop увеличивается. | Medium | Manual/functional | PASS | See related test/report. |  | TC-COMP-006 |
| CHK-15-007 | Chrome physical | Devices available | No critical differences. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-COMP-007 |
| CHK-15-008 | Firefox/Safari | Devices available | No critical differences. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-COMP-007 |
| CHK-15-009 | Orientation change | Mobile/tablet | No distortion/lost state; input bounds update. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-COMP-008 |
| CHK-15-010 | OS scaling/controller/TV | Статический анализ исходного кода и интерфейса завершен. | Система отсутствует или неприменима для текущей версии; повторно оценить после добавления функции. | Medium | Manual/functional | NOT_RUN | Not executed. |  | N/A |
