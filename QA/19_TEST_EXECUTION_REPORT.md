# 19 — Test Execution Report

**Build:** `TV-cc6576a5764a`  
**Execution date:** 2026-07-17

## Scope executed

Static syntax/DOM/CSS checks; isolated browser interactions for launch/localization/daily/navigation/core math/state/save/audio setting/boosters/reward fallback/viewports/touch; evidence screenshots.

## Metrics

| Metric | Count |
| --- | --- |
| Total test cases | 83 |
| Passed | 27 |
| Failed | 5 |
| Blocked | 2 |
| Not Run | 49 |
| Not Applicable | 0 |

**Pass rate of executed product tests:** `27 / (27 + 5) = 84.4%`. Blocked and Not Run are excluded from denominator and shown separately.

## Results by module

| Module | Key result |
| --- | --- |
| Launch/Build | Static PASS; direct/platform launch blocked |
| Core | Scoring/damage/bonus/gameOver/restart PASS; natural full cycle NOT_RUN |
| Save | Invalid JSON PASS; structured corruption FAIL BUG-001 |
| Ads | Fallback reward integrity FAIL BUG-002; real ads BLOCKED |
| Boosters/Economy | Activation PASS; exit loss FAIL BUG-004 |
| UI/Compatibility | Viewport/scroll PASS partial; edge clipping FAIL BUG-003 |
| Audio | Mute persistence PASS; audible/background NOT_RUN |
| Localization | Main RU/EN PASS; full audit NOT_RUN |
| Performance | Simulated state stress PASS; FPS/memory NOT_RUN |

## Defects

- Confirmed: 4 (`S2=2`, `S3=1`, `S4=1`; `P0=1`, `P1=2`, `P2=1`).
- Potential defects: 4, separated in Bug Reports.

## Smoke / critical path / regression

Smoke is incomplete and fails save resilience. Injected critical logic path passed, but natural-play and real input/platform paths are not complete. No full regression performed.

## Confidence

Medium for deterministic client logic; low for release/platform/performance/accessibility because environments unavailable.

## Recommendation

NO-GO. Fix BUG-002 and BUG-001; confirm package and run real Yandex tests; then retest BUG-004/003 and execute Critical/Core Regression.
