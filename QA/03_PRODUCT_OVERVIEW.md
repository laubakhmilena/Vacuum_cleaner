# 03 — Product Overview

## Назначение и идея

Короткая endless arcade-сессия: игрок управляет милым пылесосом, собирает хорошие и золотые мысли, избегает вредных. За score начисляются stars; они расходуются на upgrades, boosters и cosmetic skins.

## Основной цикл

`Menu → optional daily/store → Start → Move → Collect/Avoid → Score/Combo/Bonus → Lose lives → GameOver → Reward/Revive/Restart/Menu`.

## Сущности и правила

| Сущность | Правило |
| --- | --- |
| Player vacuum | Target follows pointer; collision radius 36; suction radius 86 + 13×radius level |
| Good thought | 10×combo×double points; streak +1; every 5 → combo up to 5 |
| Bad thought | Shield consumed or lives −1; combo/streak reset |
| Gold thought | 50×combo×double; random magnet/slow/double |
| Stars | floor(score/100) incremental award; spend in store |
| Lives | 3 + 1 if life upgrade |
| Boosters | Consumed at round start |
| Daily | Local-date reward and 3 deterministic daily tasks |

## Состояния

```text
menu ──Play──> game ──lives=0──> gameOver ──Restart──> game
  │              │                    │
  └─Upgrades─> upgrades─Back──────────┘─Menu───────> menu
                 game ──Menu──────────────────────> menu
                 game ──blur/hidden/sdk pause──> paused flag ──resume──> game
```

## Ожидаемые реакции

- Pointer movement изменяет target, но не score.
- Good/gold feedback: score, particles, sound; bad: shake/life feedback.
- UI reflects score/lives/combo and active bonuses.
- Invalid optional external service must not corrupt progression.
- Persistent state restores best/stars/store/settings/daily.

## Нефункциональные ожидания

Responsive desktop/mobile, no background audio, safe interruption, readable UI, no long-frame spikes, recoverable saves. Формальные FPS/load targets отсутствуют.
