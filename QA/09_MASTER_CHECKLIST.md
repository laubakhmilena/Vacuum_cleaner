# 09 — Master Checklist

**Build:** `TV-cc6576a5764a`  
**Правило статусов:** используются только `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE`. Частичные наблюдения не считаются выполненным тестом и отмечены `NOT_RUN` с пояснением.

| ID | Область | Файл | Статусы |
| --- | --- | --- | --- |
| CHK-01 | Installation And First Launch | checklists/CHK-01_Installation_And_First_Launch.md | PASS:5, FAIL:1, BLOCKED:1, NOT_RUN:3 |
| CHK-02 | Main Menu And Navigation | checklists/CHK-02_Main_Menu_And_Navigation.md | PASS:5, FAIL:1, NOT_RUN:4 |
| CHK-03 | Core Gameplay | checklists/CHK-03_Core_Gameplay.md | PASS:6, NOT_RUN:4 |
| CHK-04 | Controls And Input | checklists/CHK-04_Controls_And_Input.md | PASS:1, BLOCKED:1, NOT_RUN:7, NOT_APPLICABLE:1 |
| CHK-05 | UI And HUD | checklists/CHK-05_UI_And_HUD.md | PASS:6, FAIL:1, NOT_RUN:3 |
| CHK-06 | Game States | checklists/CHK-06_Game_States.md | PASS:5, FAIL:1, BLOCKED:1, NOT_RUN:3 |
| CHK-07 | Levels And Progression | checklists/CHK-07_Levels_And_Progression.md | PASS:3, FAIL:1, NOT_RUN:5, NOT_APPLICABLE:1 |
| CHK-08 | Win Lose And Restart | checklists/CHK-08_Win_Lose_And_Restart.md | PASS:2, FAIL:2, BLOCKED:2, NOT_RUN:3, NOT_APPLICABLE:1 |
| CHK-09 | Save Load And Persistence | checklists/CHK-09_Save_Load_And_Persistence.md | PASS:4, FAIL:1, NOT_RUN:4, NOT_APPLICABLE:1 |
| CHK-10 | Settings | checklists/CHK-10_Settings.md | PASS:3, NOT_RUN:1, NOT_APPLICABLE:6 |
| CHK-11 | Audio | checklists/CHK-11_Audio.md | PASS:1, NOT_RUN:8, NOT_APPLICABLE:1 |
| CHK-12 | Graphics And Animation | checklists/CHK-12_Graphics_And_Animation.md | PASS:2, FAIL:1, NOT_RUN:7 |
| CHK-13 | Physics And Collisions | checklists/CHK-13_Physics_And_Collisions.md | PASS:4, FAIL:1, NOT_RUN:5 |
| CHK-14 | Performance And Stability | checklists/CHK-14_Performance_And_Stability.md | PASS:2, FAIL:1, NOT_RUN:7 |
| CHK-15 | Compatibility | checklists/CHK-15_Compatibility.md | PASS:6, NOT_RUN:4 |
| CHK-16 | Accessibility | checklists/CHK-16_Accessibility.md | PASS:3, FAIL:1, NOT_RUN:6 |
| CHK-17 | Localization | checklists/CHK-17_Localization.md | PASS:3, NOT_RUN:6, NOT_APPLICABLE:1 |
| CHK-18 | Negative And Recovery | checklists/CHK-18_Negative_And_Recovery.md | PASS:1, FAIL:2, BLOCKED:1, NOT_RUN:6 |
| CHK-19 | Long Session | checklists/CHK-19_Long_Session.md | PASS:1, BLOCKED:1, NOT_RUN:8 |
| CHK-20 | Release Candidate | checklists/CHK-20_Release_Candidate.md | PASS:2, FAIL:2, BLOCKED:2, NOT_RUN:4 |

## Порядок использования

1. Для новой сборки скопировать комплект или зафиксировать новый Build ID.
2. Сбросить только выполняемые заново пункты в `NOT_RUN`; исторические результаты не перезаписывать без evidence.
3. Выполнять CHK-01 → CHK-03/04/06 → CHK-08/09 → risk-based области.
4. Для `FAIL` создать/связать Bug ID; для `BLOCKED` записать точный blocker и владельца действия.
5. Ссылки `Evidence/Test` ведут к детальным тест-кейсам, charter или доказательствам.
