# 21 — Solo Developer QA Workflow

## Перед каждым коммитом

1. Test changed function with smallest related cases.
2. Check console/errors.
3. Run adjacent state/save/economy tests from Traceability.
4. Do not mark PASS without actual execution.

## Перед тестовой сборкой

Static checks → clean launch → smoke → core critical path → save valid/corrupt → known issue spot checks.

## Перед релизом

Release ZIP verification → full smoke → Critical/Core Regression → natural exploratory session → 30-minute soak → Yandex debug loader/ads → release readiness → known issues update.

## После bug fix

Exact repro → confirm expected result → repeat on clean/affected profile → local regression → adjacent system → evidence → status/changelog/verdict.

## Минимальный change-based набор

| Изменение | Минимальный набор |
| --- | --- |
| UI | UI/COMP/LOC/ACC |
| Input | INPUT + STATE + natural core |
| Physics/collision | CORE-003..013 + edge charter |
| Save | SAVE-001..004 + all persistence |
| Settings/audio | AUDIO-001..004 + focus |
| Balance | CORE-002/005/006 + PROG/DAILY |
| SDK/dependency | PLAT/ADS + smoke/fullscreen/background |
| Crash fix | Exact crash + smoke + full affected module |
| Release | All gates in 20 report |

## Практика

Keep one immutable test profile backup, one corrupt profile corpus, one release checklist. Update only statuses/evidence for each build; do not duplicate whole documents unless behavior changes.
