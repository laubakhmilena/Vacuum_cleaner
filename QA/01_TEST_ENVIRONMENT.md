# 01 — Тестовое окружение

| Поле | Значение |
|---|---|
| Дата/время | 2026-07-17; command logs use UTC |
| Build | `TV-cc6576a5764a` |
| OS | Debian GNU/Linux 13 (trixie), Linux x86_64 |
| CPU | 56 logical CPUs exposed to container; host model not used as performance claim |
| Memory | 4.0 GiB available container limit (observed); no swap |
| GPU | Не определен; headless Chromium, hardware performance не оценивается |
| Display | Environment 1024×768; viewport matrix 320×568, 360×640, 768×1024, 1366×768, 1920×1080 |
| Browser | Chromium 144.0.7559.96 headless |
| Runtime | Node 22.16.0; Python 3.13.5 |
| Input | Playwright mouse, keyboard, CDP touch emulation |
| Engine | Custom Canvas 2D JS loop; engine version N/A |
| Save | In-memory localStorage-compatible harness for repeatable cases |

## Команды

```bash
node --check game.js
node --check vacuum_player_data.js
python QA/work/run_dynamic_tests_harness.py
```

Прямой предусмотренный запуск: static hosting/Yandex local server с `index.html` в root и `assets/` рядом. В текущем sandbox прямые `http://127.0.0.1` и `file://` browser navigation блокировались административной политикой, поэтому использован изолированный `set_content` harness. Он не меняет product logic; заменены только невозможный base URL и storage backend.

## Логи

- `logs/build.log`
- `logs/tests.log`
- `logs/browser_console.json`
- `logs/page_errors.json`
- `logs/source_hashes.sha256`

## Ограничения

Нет Yandex runtime/debug panel, реальных ads, audible device validation, GPU/FPS/memory profiler, physical mobile/controller, Firefox/Safari.
