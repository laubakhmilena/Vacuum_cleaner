# 12 — Regression Suite

## Critical Regression

Когда: любое изменение gameplay, save, ads, state, release candidate.  
Tests: `TC-SMOKE-001/002`, `TC-CORE-001..008`, `TC-SAVE-001/002`, `TC-ADS-001/002/005/006`, `TC-STATE-001/002`, `TC-BOOST-001/002`.  
Проход: 100% executed PASS, no open S1/S2. Трудоемкость: компактный набор, но real ads/state требуют platform session.

## Core Regression

Critical + daily, upgrades, boosters limits, skins, all localization screens, five core viewports.

## Extended Regression

Core + negative/recovery, audio, orientation, missing assets, multi-touch, 30-minute soak.

## Full Regression

Все 83 cases, 20 checklists, 15 exploratory charters и Yandex public requirement review.

## Change impact map

| Изменение | Минимум |
| --- | --- |
| UI/CSS | UI-001/002, COMP-001..006, LOC-003..005, ACC-001/002 |
| Input | INPUT-001..004, STATE-002, CORE-012 |
| Gameplay/scoring | CORE-001..013, PROG-001 |
| Save/schema | SAVE-001..004, DAILY/STORE persistence |
| Ads/SDK | ADS-001..006, PLAT-001..004, STATE/AUDIO |
| Assets/render | GFX-001, UI-002, COMP-007/008, PERF-003 |
