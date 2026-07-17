# 16 — Performance and Compatibility

## Фактические данные

- `TC-PERF-001`: 3000 `updateGame(0.033)` iterations, ~99.9 seconds simulated game time, spawn disabled to isolate state loop; no exception/NaN. **Не FPS/soak.**
- Responsive DOM and scroll checked at 5 viewports; touch swipe 360×640 changed panel scrollTop 0→451.
- No CPU/GPU/FPS/frame-time/memory claims were made.

## Compatibility matrix

| Конфигурация | Статус | Evidence/next step |
| --- | --- | --- |
| Chromium 144 headless, 1024×768 | PARTIAL PASS | Core harness checks |
| 320×568 touch-like | PARTIAL PASS | EV-VP-320x568; touch separately 360×640 |
| 360×640 mobile touch emulation | PASS for panel scroll | EV-008 |
| 768×1024 | PARTIAL PASS | Layout only |
| 1366×768 | PARTIAL PASS | Layout only |
| 1920×1080 | PARTIAL PASS | Layout only |
| Chrome physical desktop/mobile | NOT_TESTED | Run smoke/natural play |
| Firefox latest | NOT_TESTED | Cross-browser |
| Safari/iOS | NOT_TESTED | Web Audio/touch/emoji |
| Fullscreen/orientation/OS scaling | NOT_TESTED | TC-COMP-008 |
| Controller/TV remote | NOT_TESTED/N/A until target confirmed | Input implementation absent |

## Рекомендуемые, не нормативные пороги

- Interactive menu without visible stall after assets loaded.
- Stable 60 FPS target on mainstream devices; investigate sustained <30 FPS or input lag.
- No monotonic memory growth across 30-minute session/restart cycles.
- No single-frame stalls noticeable during particle bursts/ads close.

Пороги должны быть приняты разработчиком и измерены на real devices.
