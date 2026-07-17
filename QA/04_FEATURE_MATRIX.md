# 04 — Feature Matrix

| Feature ID | Название | Описание | Источник | Статус | Критичность | Зависимости | Тесты | Checklist | Факт |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FEAT-STATE-001 | Экранные состояния | menu / upgrades / game / gameOver и переходы между ними | index.html:15-110; game.js:40-68,682-687 | CONFIRMED | High | UI, input | TC-SMOKE-001; TC-UI-001 | CHK-02; CHK-06 | PASS |
| FEAT-CORE-001 | Начало раунда | Создание игрового состояния, 3 жизни, score 0, combo x1 | game.js:689-739 | CONFIRMED | Critical | Input, HUD, boosters | TC-CORE-001 | CHK-03; CHK-06 | PASS |
| FEAT-INPUT-001 | Управление указателем | Пылесос следует за mouse/pointer/touch координатами | game.js:610-625,878-883,895-908 | CONFIRMED | Critical | Canvas, viewport | TC-INPUT-001; TC-INPUT-002 | CHK-04 | PARTIAL |
| FEAT-CORE-002 | Генерация мыслей | Появление good/bad/gold объектов с вероятностями и скоростью | game.js:895-997 | CONFIRMED | High | RNG, viewport | TC-CORE-009; TC-CORE-010 | CHK-03 | NOT_RUN |
| FEAT-CORE-003 | Втягивание и магнит | Хорошие/золотые притягиваются; плохие отталкиваются активным магнитом | game.js:920-949 | CONFIRMED | High | Upgrades, boosters | TC-CORE-011 | CHK-03; CHK-13 | NOT_RUN |
| FEAT-CORE-004 | Очки, серия и combo | Good = 10, gold = 50, множители double и combo; combo растет каждые 5 good | game.js:999-1044 | CONFIRMED | Critical | HUD, tasks | TC-CORE-002; TC-CORE-006 | CHK-03; CHK-05 | PASS |
| FEAT-CORE-005 | Жизни, урон и поражение | Bad уменьшает жизнь; shield блокирует один раз; при 0 — gameOver | game.js:999-1021,759-791 | CONFIRMED | Critical | Game state, ads | TC-CORE-003; TC-CORE-004; TC-CORE-007 | CHK-03; CHK-08 | PASS |
| FEAT-CORE-006 | Золотые бонусы | Gold запускает magnet/slow/double на ограниченное время | game.js:1038-1053 | CONFIRMED | High | HUD, upgrades | TC-CORE-005 | CHK-03 | PASS |
| FEAT-STATE-002 | Системная пауза | Пауза при visibility/blur/SDK и продолжение при возврате | game.js:385-460,611-614 | CONFIRMED | High | Audio, SDK | TC-STATE-001; TC-STATE-002 | CHK-06 | PARTIAL |
| FEAT-UI-001 | Главное меню и HUD | Меню, лучший счет, daily reward, HUD score/lives/combo, кнопки | index.html:15-110; style.css:1-743 | CONFIRMED | High | Localization, state | TC-SMOKE-001; TC-UI-001; TC-UI-003 | CHK-02; CHK-05 | PARTIAL |
| FEAT-UI-002 | Адаптивный интерфейс | Safe-area, mobile/landscape breakpoints, прокручиваемые панели | style.css:45-743 | CONFIRMED | High | Viewport, touch | TC-COMP-001..006; TC-UI-002 | CHK-05; CHK-15 | FAIL |
| FEAT-GFX-001 | Canvas-графика | Фон, частицы, эмодзи-мысли, картинка пылесоса и fallback-отрисовка | game.js:1416-1880 | CONFIRMED | Medium | Assets, GPU/fonts | TC-GFX-001; TC-UI-002 | CHK-12 | PARTIAL |
| FEAT-PROG-001 | Лучший результат и звезды | Награды floor(score/100), best score, баланс звезд | game.js:759-791,873-876 | CONFIRMED | High | Save, store | TC-CORE-007; TC-PROG-001 | CHK-07 | PARTIAL |
| FEAT-SAVE-001 | Локальное сохранение | localStorage key thoughtVacuumProgress.v1; нормализация части полей | game.js:554-608,1351-1394 | CONFIRMED | Critical | All progression | TC-SAVE-001..004 | CHK-09 | FAIL |
| FEAT-DAILY-001 | Ежедневная награда | 3 звезды один раз за локальную календарную дату | game.js:1300-1320,1408-1414 | CONFIRMED | Medium | Save, local clock | TC-DAILY-001; TC-DAILY-002 | CHK-07 | PARTIAL |
| FEAT-DAILY-002 | Ежедневные задания | 3 задачи из 5, награда 2, бонус за все 3 | game.js:272-278,1193-1223,1322-1406 | CONFIRMED | High | Save, gameplay | TC-DAILY-003..006 | CHK-07 | NOT_RUN |
| FEAT-UPG-001 | Постоянные улучшения | radius 0..5, bonus 0..5, life 0..1 за звезды | game.js:245-270,1123-1150,1286-1298 | CONFIRMED | High | Economy, save | TC-UPG-001..004 | CHK-07; CHK-10 | NOT_RUN |
| FEAT-BOOST-001 | Расходуемые бустеры | magnetStart, shield, doubleStart; максимум 3 каждого | game.js:178-200,1151-1172,1226-1284 | CONFIRMED | High | Economy, game start | TC-BOOST-001..003 | CHK-07 | FAIL |
| FEAT-SKIN-001 | Скины | 4 ауры; blue бесплатный, остальные покупаются и выбираются | game.js:202-243,1173-1192,1240-1260 | CONFIRMED | Medium | Save, renderer | TC-SKIN-001..003 | CHK-07; CHK-12 | NOT_RUN |
| FEAT-ADS-001 | Межстраничная реклама | После 3 завершенных раундов перед restart вызывается fullscreen ad | game.js:462-499,748-757 | CONFIRMED | High | Yandex SDK, progression | TC-ADS-003; TC-ADS-004 | CHK-18 | BLOCKED |
| FEAT-ADS-002 | Rewarded revive | После поражения один revive за rewarded video | game.js:501-552,793-827 | CONFIRMED | Critical | Yandex SDK, game state | TC-ADS-001; TC-ADS-005 | CHK-08; CHK-18 | FAIL |
| FEAT-ADS-003 | Rewarded x2 звезд | После поражения удвоение заработанных звезд за rewarded video | game.js:501-552,828-857 | CONFIRMED | Critical | Yandex SDK, economy | TC-ADS-002; TC-ADS-006 | CHK-08; CHK-18 | FAIL |
| FEAT-AUDIO-001 | Синтезированный звук и mute | Web Audio для vacuum/good/bad/gold/combo/buy/over; mute сохраняется | game.js:1881-2047 | CONFIRMED | Medium | Focus, localStorage | TC-AUDIO-001..004 | CHK-11 | PARTIAL |
| FEAT-LOC-001 | Русский и английский | Автовыбор по query/navigator/SDK; таблица строк RU/EN | game.js:78-176,291,306-382,444-454 | CONFIRMED | High | UI, SDK | TC-LOC-001..005 | CHK-17 | PARTIAL |
| FEAT-PLAT-001 | Yandex Games SDK | /sdk.js, init, LoadingAPI, GameplayAPI, ad API | index.html:10-12; game.js:385-552 | CONFIRMED | Critical | Network/platform | TC-PLAT-001..004 | CHK-01; CHK-20 | BLOCKED |

`PARTIAL` означает, что часть behavior проверена, но реальная платформа/device/manual feel остались непроверенными.
