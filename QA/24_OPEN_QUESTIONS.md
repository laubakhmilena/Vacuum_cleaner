# 24 — Open Questions

| ID | Вопрос | Почему важен | Компонент | Текущее предположение | Риск | Решение |
| --- | --- | --- | --- | --- | --- | --- |
| Q-001 | Какое финальное название: «Пыслей» или «Мыслей»? | Store/listing/localization | Brand | «Пыслей» — намеренный pun | Medium | Подтвердить и закрепить glossary |
| Q-002 | Yandex Games — единственная target platform? | SDK paths/input requirements | Platform | Да | High | Подтвердить device types/orientation |
| Q-003 | Reward fallback должен существовать в debug build? | BUG-002 treatment | Ads | Production reward only on onRewarded | Critical | Разделить debug flag and production behavior |
| Q-004 | Должен ли Menu подтверждать потерю boosters? | BUG-004 oracle | Economy/UX | Да | High | Define confirm/cancel/refund |
| Q-005 | Bonus duration upgrade влияет на start boosters? | Potential mismatch | Upgrades | Все magnet/double effects | Medium | Write explicit design rule |
| Q-006 | Допустим ли local-clock daily exploit? | Economy | Daily | Risk not accepted for monetized release | Medium | Server time/SDK or explicit acceptance |
| Q-007 | Какие performance targets/devices? | Release gates | Performance | 60 FPS preferred, no formal target | High | Define minimum devices and thresholds |
| Q-008 | Нужны ли keyboard/controller/TV controls? | Accessibility/platform reach | Input | Desktop mouse + mobile touch only | High | Confirm catalog device declarations |
| Q-009 | Как выглядит final release ZIP? | Build validity | Packaging | assets directory required | High | Provide archive and run TC-BUILD-001 |
