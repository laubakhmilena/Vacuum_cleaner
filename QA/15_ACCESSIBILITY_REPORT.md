# 15 — Accessibility Report

Это техническая оценка, не заявление о полной доступности для какой-либо группы.

| Область | Применимость | Результат | Доказательство | Влияние | Рекомендация | Effort | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Text size/reflow | Да | PARTIAL: responsive, readable screenshots; no zoom audit | CSS clamp/media; viewport evidence | Medium | Test browser zoom 200%, expose text scale if needed | Medium | P2 |
| Contrast | Да | RISK: white on #ff6f91=2.65:1, #ff9671=2.13:1, #1fbfa3=2.32:1 | Static WCAG contrast calculation | High for low vision | Use darker fills or dark text; target 4.5:1 regular/3:1 large as heuristic | Low | P1 |
| Target size | Да | PASS static: buttons min-height 40–54px | style.css | Low | Keep ≥24px and spacing | Low | Maintain |
| Color dependency | Да | PARTIAL: thought type uses different emoji plus colors; bonuses have text | Source/screenshots | Medium | Test color blindness; add shape/audio consistency | Medium | P2 |
| Audio control | Да | PASS partial: mute and persistence | TC-AUDIO-001 | Medium | Move mute also to menu/settings; volume slider | Low/Medium | P2 |
| Visual alternative to audio | Да | PARTIAL: score/particles/shake exist | Source | Medium | Ensure every cue has textual/visual feedback | Medium | P2 |
| Keyboard/remap | Да | FAIL/GAP: UI tabbable, gameplay pointer-only | TC-ACC-001; source | High | Add WASD/arrows and optional sensitivity/rebind | Medium | P1 |
| One-hand/simple input | Да | Pointer movement is simple, but continuous precision required | Mechanic | Medium | Add keyboard/drag mode, larger safe area | Medium | P2 |
| Timers/difficulty | Да | No difficulty/pause control; spawn accelerates | Source | High for motor/cognitive | Add pause and optional relaxed mode | High | P2 |
| Shake/reduced motion | Да | No toggle; hit shake hard-coded | game.js:1422-1426 | Medium | Reduced motion toggle; disable shake/particles | Low | P1/P2 |
| Flashing/photosensitivity | Да | No deliberate flashing detected; not instrumentally measured | Static/render review | Medium | Review gold/particle frequency in real play | Low | P2 |
| Focus visibility | Да | Keyboard reaches controls; visual focus not fully audited | TC-ACC-001 | Medium | Explicit :focus-visible style | Low | P1 |
| Screen reader | Да | Canvas only aria-label; live score/game state absent | index.html/game.js | High | ARIA live summary, semantic controls, alternative mode | High | P2 |
| Irreversible actions | Да | FAIL: Menu loses boosters without confirmation | BUG-004 | High | Confirmation with resource warning | Low | P1 |
| Subtitles/speech/haptics | Нет/не обнаружено | NOT_APPLICABLE | No speech/haptics | Low | Reassess if added | N/A | N/A |

## Быстрые улучшения с высокой пользой

1. Darken primary/store button backgrounds or use dark text.
2. Add explicit `:focus-visible` outline.
3. Add confirm dialog for Menu with active consumables.
4. Add reduced-motion toggle and mute in main menu.
5. Document controls on first launch.

## Не проверено

Screen reader, OS high contrast, 200% zoom, physical motor/vision user testing, real mobile accessibility services.
