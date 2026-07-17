# CHK-16 — Accessibility

Build: `TV-cc6576a5764a`.

| Check ID | Проверка | Предусловие | Ожидаемый результат | Priority | Type | Status | Комментарий | Bug | Evidence/Test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-16-001 | Keyboard reaches menu | Меню | Daily, Play, Upgrades получают фокус. | Critical | Manual/functional | PASS | See related test/report. |  | TC-ACC-001 |
| CHK-16-002 | Gameplay keyboard alternative | Desktop/mobile | Control alternative or documented limitation. | Critical | Manual/functional | NOT_RUN | Not executed. |  | TC-ACC-003 |
| CHK-16-003 | Contrast | CSS colors | Meet accepted contrast heuristic or documented exception. | High | Manual/functional | NOT_RUN | Not executed. |  | TC-ACC-002 |
| CHK-16-004 | Target sizes ≥24px | Сборка запущена; доступна область «Target sizes ≥24px». | Сценарий «Target sizes ≥24px» выполняется предсказуемо, без crash, потери данных, блокировки управления и визуальных дефектов. | High | Manual/functional | PASS | See related test/report. |  | Static CSS |
| CHK-16-005 | Color-only info | Сборка запущена; доступна область «Color-only info». | Сценарий «Color-only info» выполняется предсказуемо, без crash, потери данных, блокировки управления и визуальных дефектов. | High | Manual/functional | NOT_RUN | Есть частичное статическое/автоматизированное наблюдение; полная ручная проверка не выполнялась. |  | Review |
| CHK-16-006 | Mute control | Активный раунд | soundMuted=true; label Включить звук. | Medium | Manual/functional | PASS | See related test/report. |  | TC-AUDIO-001 |
| CHK-16-007 | Reduced motion/shake | Bad collision | Shake can be reduced/disabled. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-ACC-004 |
| CHK-16-008 | Screen reader state | Screen reader | Critical state/actions communicated. | Medium | Manual/functional | NOT_RUN | Not executed. |  | TC-ACC-005 |
| CHK-16-009 | Focus visibility | Меню | Daily, Play, Upgrades получают фокус. | Medium | Manual/functional | NOT_RUN | Есть частичное статическое/автоматизированное наблюдение; полная ручная проверка не выполнялась. |  | TC-ACC-001 |
| CHK-16-010 | Irreversible action confirmation | Boosters активированы | Есть подтверждение либо неиспользованные boosters возвращаются. | Critical | Manual/functional | FAIL | See related test/report. | BUG-004 | TC-BOOST-002 |
