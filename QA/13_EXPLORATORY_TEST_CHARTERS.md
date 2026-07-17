# 13 — Exploratory Test Charters

## EXP-01 — Первый запуск новым игроком

- **Цель:** исследовать Launch/menu/onboarding.
- **Риски:** startup, comprehension.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-02 — Полный основной цикл

- **Цель:** исследовать Natural play to gameOver/restart.
- **Риски:** soft lock, scoring.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-03 — Быстрый и хаотичный ввод

- **Цель:** исследовать Pointer/touch/buttons.
- **Риски:** double action, race.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-04 — Нарушение порядка действий

- **Цель:** исследовать Unexpected screen/action order.
- **Риски:** state corruption.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-05 — Границы игрового пространства

- **Цель:** исследовать All edges/corners.
- **Риски:** clipping/collision.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-06 — Переходы состояний

- **Цель:** исследовать menu/upgrades/game/gameOver.
- **Риски:** invalid transition.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-07 — Пауза, Alt+Tab и возврат

- **Цель:** исследовать Visibility/blur/audio.
- **Риски:** background damage/audio.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-08 — Многократный restart

- **Цель:** исследовать 50 cycles.
- **Риски:** leak/state carryover.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-09 — Длительная сессия

- **Цель:** исследовать 30+ minutes.
- **Риски:** memory/FPS/counters.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-10 — Минимальные и максимальные значения

- **Цель:** исследовать 0/max stars/upgrades/boosters.
- **Риски:** boundaries.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-11 — Сохранение и восстановление

- **Цель:** исследовать valid/corrupt/quota.
- **Риски:** data loss.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-12 — Слабая обратная связь

- **Цель:** исследовать Collisions/bonuses/errors.
- **Риски:** confusion.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-13 — Доступность интерфейса

- **Цель:** исследовать Keyboard/contrast/motion.
- **Риски:** exclusion.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-14 — Тяжелая сцена

- **Цель:** исследовать High spawn/particles/emoji.
- **Риски:** long frames.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.

## EXP-15 — Мягкая блокировка

- **Цель:** исследовать Interruptions/ads/focus.
- **Риски:** cannot progress.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.
