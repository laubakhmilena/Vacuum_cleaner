# 17 — Localization Report

## Languages

RU and EN tables exist. `ru/be/kk/uk/uz` map to Russian; all other primary language codes map to English. SDK language can override navigator after init.

## Выполнено

- English main menu/title/lang: PASS.
- Russian main menu and mapping function: PASS.
- Dynamic store/task strings use `titleEn/textEn`: static CONFIRMED.

## Не выполнено

Complete every-screen linguistic audit, pseudo-localization, long string overflow, date/number locale semantics, native speaker review.

## Терминологический словарь

| RU | EN | Комментарий |
| --- | --- | --- |
| Пылесос Пыслей | Thought Vacuum | Название требует подтверждения spelling/pun |
| Хорошая мысль | Good thought | Collectible |
| Вредная мысль | Bad/harmful thought | Damage |
| Золотая мысль | Golden thought | Bonus collectible |
| Очки | Score | Round score |
| Жизни | Lives | Hearts |
| Комбо | Combo | Multiplier |
| Звезды | Stars | Currency |
| Улучшения | Upgrades | Permanent |
| Бустеры | Boosters | Consumable |
| Щит | Shield | One bad thought block |
| Умный магнит | Smart magnet | Attract good/gold, repel bad |
| Замедление | Slow | Temporary effect |

## Риски

Title spelling, translated language mapping for Belarusian/Kazakh/Ukrainian/Uzbek, English text length in store, seconds suffix `s` not localized to Russian convention.
