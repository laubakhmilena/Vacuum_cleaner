# 06 — Test Strategy

## Цели

Проверить критический игровой путь, целостность прогрессии/экономики, устойчивость сохранения, input/state transitions и готовность Yandex integration. Стратегия оптимизирована для одного разработчика: сначала тесты с максимальным риском и короткой обратной связью.

## Scope

Входит: static web files, gameplay, UI, local save, daily/store, ads integration branches, audio state, RU/EN, responsive layout.  
Не входит без окружения: moderation, real ad inventory, payment/account/leaderboard, device lab, full accessibility certification.

## Подход

- Risk-based order: startup/save/ads/core → input/state → economy/daily → UI/localization → performance/accessibility.
- Techniques: equivalence, boundaries, decision tables, state transitions, user journeys, error guessing, exploratory charters, limited pairwise viewports.
- Retest: exact bug steps on clean and affected save, then adjacent feature tests.
- Regression tiers: Critical/Core/Extended/Full.

## Entry criteria

Source identified; build/hash recorded; launch method known; test data backup possible.

## Suspension criteria

Startup crash for clean profile, non-deterministic data loss, environment changes that invalidate evidence, or >1 open S1.

## Exit criteria

- Smoke and critical path pass.
- No open S1/S2 without explicit accepted risk.
- Save corruption and rewarded branches tested.
- Real Yandex loader/ads checked for release.
- Known issues and verdict updated.

## Evidence rules

Screenshot/log must reference build and test/bug ID. Do not overwrite evidence of previous build; add suffix/date. Secrets and personal data must be removed.

## При нехватке времени

1. Startup + save corruption.
2. Natural core loop/gameOver/restart.
3. Reward integrity and ad recovery.
4. Booster/economy persistence.
5. Mobile viewport/touch.
6. Remaining UI/accessibility/performance.
