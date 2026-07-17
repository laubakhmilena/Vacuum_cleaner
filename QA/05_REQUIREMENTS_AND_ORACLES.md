# 05 — Requirements and Oracles

## Иерархия оракулов

1. Явные UI-тексты и source behavior.
2. Внутренняя согласованность правил.
3. Публичные Yandex requirements/SDK contracts.
4. Accessibility guidance.
5. Общепринятое ожидание игрока — помечено INFERRED.

| Requirement ID | Ожидаемое поведение | Oracle/source | Статус | Features |
| --- | --- | --- | --- | --- |
| REQ-FUNC-001 | После выбора «Играть» начинается раунд с базовым состоянием | UI text + startGame implementation | CONFIRMED | FEAT-CORE-001 |
| REQ-FUNC-002 | Положительные мысли увеличивают score, отрицательные уменьшают lives | Game rules in menu + collectThought | CONFIRMED | FEAT-CORE-004; FEAT-CORE-005 |
| REQ-FUNC-003 | Золотая мысль дает 50 очков и случайный временный бонус | Code consistency | CONFIRMED | FEAT-CORE-006 |
| REQ-FUNC-004 | После 0 жизней показывается экран результата | State transition code/UI | CONFIRMED | FEAT-CORE-005; FEAT-STATE-001 |
| REQ-FUNC-005 | Restart создает чистый раунд | Button label + startGame | CONFIRMED | FEAT-CORE-001 |
| REQ-SAVE-001 | Корректное сохранение не должно ломать запуск и должно восстанавливаться | localStorage implementation + user expectation | CONFIRMED | FEAT-SAVE-001 |
| REQ-SAVE-002 | Поврежденное сохранение обрабатывается безопасно без startup crash | Existing try/catch intent + robust recovery oracle | INFERRED | FEAT-SAVE-001 |
| REQ-ECON-001 | Стоимость не списывается, если покупки нет или лимит достигнут | Button state + guard code | CONFIRMED | FEAT-UPG-001; FEAT-BOOST-001; FEAT-SKIN-001 |
| REQ-ECON-002 | Расходуемый бустер списывается только при осознанном начале/продолжении раунда | User expectation; requires developer confirmation | INFERRED | FEAT-BOOST-001 |
| REQ-ADS-001 | Rewarded-награда выдается только после onRewarded | Yandex SDK rewarded callback contract | CONFIRMED | FEAT-ADS-002; FEAT-ADS-003 |
| REQ-ADS-002 | При SDK/ad error игра восстанавливает состояние без бесплатной награды | Platform behavior + economy integrity | INFERRED | FEAT-ADS-002; FEAT-ADS-003 |
| REQ-UI-001 | Интерактивные элементы доступны и читаемы на целевых viewport | Yandex requirements + responsive CSS intent | CONFIRMED | FEAT-UI-001; FEAT-UI-002 |
| REQ-UI-002 | Игровой объект остается достаточно видимым у границ | Common gameplay feedback oracle | INFERRED | FEAT-UI-002; FEAT-GFX-001 |
| REQ-INPUT-001 | На mobile игра полностью управляется жестами и long-tap не вызывает browser UI | Yandex public requirements | CONFIRMED | FEAT-INPUT-001 |
| REQ-STATE-001 | При minimization/blur звук и gameplay останавливаются | Yandex requirements + pause code | CONFIRMED | FEAT-STATE-002; FEAT-AUDIO-001 |
| REQ-LOC-001 | Все основные UI-строки отображаются на одном выбранном языке | Translation tables + consistency oracle | CONFIRMED | FEAT-LOC-001 |
| REQ-ACC-001 | Критическая информация не должна передаваться только цветом | Accessibility guideline | INFERRED | FEAT-UI-001; FEAT-GFX-001 |
| REQ-ACC-002 | Кнопки должны иметь достаточный размер и различимый фокус | WCAG heuristic + game accessibility guideline | INFERRED | FEAT-UI-001 |
| REQ-PLAT-001 | Yandex SDK подключен до YaGames.init и LoadingAPI.ready вызывается после загрузки | Yandex official SDK docs | CONFIRMED | FEAT-PLAT-001 |
| REQ-PLAT-002 | GameplayAPI.start/stop отражают фактическую активность | Yandex official SDK docs | CONFIRMED | FEAT-PLAT-001; FEAT-STATE-002 |

## Требуют подтверждения разработчиком

- Должен ли upgrade bonus duration влиять на стартовые boosters.
- Является ли мгновенный выход с потерей boosters намеренным.
- Допустима ли выдача rewarded rewards в standalone debug mode; для production это считается defect.
- Требуется ли полностью видимый sprite у границ или допускается clipping.
- Желаемые score/session/FPS targets.
