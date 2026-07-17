from pathlib import Path
from datetime import date
import csv, json, os, re, textwrap, shutil

ROOT=Path('/mnt/data')
QA=ROOT/'QA'
BUILD='TV-cc6576a5764a'
DATE='2026-07-17'
ENV='Debian 13 x86_64; Chromium 144 headless; 1024×768 unless stated; isolated QA harness'

# ---------- helpers ----------
def write(rel, content, bom=False):
    p=QA/rel; p.parent.mkdir(parents=True,exist_ok=True)
    enc='utf-8-sig' if bom else 'utf-8'
    p.write_text(content.rstrip()+"\n",encoding=enc)

def md_table(headers, rows):
    def esc(v):
        s=str(v).replace('\n','<br>').replace('|','\\|')
        return s
    out=['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']
    out += ['| '+' | '.join(esc(x) for x in r)+' |' for r in rows]
    return '\n'.join(out)

def bullets(items): return '\n'.join(f'- {x}' for x in items)

def section(title, body): return f'## {title}\n\n{body.strip()}\n'

# ---------- model ----------
features=[
('FEAT-STATE-001','Экранные состояния','menu / upgrades / game / gameOver и переходы между ними','index.html:15-110; game.js:40-68,682-687','CONFIRMED','High','UI, input','TC-SMOKE-001; TC-UI-001','CHK-02; CHK-06','PASS'),
('FEAT-CORE-001','Начало раунда','Создание игрового состояния, 3 жизни, score 0, combo x1','game.js:689-739','CONFIRMED','Critical','Input, HUD, boosters','TC-CORE-001','CHK-03; CHK-06','PASS'),
('FEAT-INPUT-001','Управление указателем','Пылесос следует за mouse/pointer/touch координатами','game.js:610-625,878-883,895-908','CONFIRMED','Critical','Canvas, viewport','TC-INPUT-001; TC-INPUT-002','CHK-04','PARTIAL'),
('FEAT-CORE-002','Генерация мыслей','Появление good/bad/gold объектов с вероятностями и скоростью','game.js:895-997','CONFIRMED','High','RNG, viewport','TC-CORE-009; TC-CORE-010','CHK-03','NOT_RUN'),
('FEAT-CORE-003','Втягивание и магнит','Хорошие/золотые притягиваются; плохие отталкиваются активным магнитом','game.js:920-949','CONFIRMED','High','Upgrades, boosters','TC-CORE-011','CHK-03; CHK-13','NOT_RUN'),
('FEAT-CORE-004','Очки, серия и combo','Good = 10, gold = 50, множители double и combo; combo растет каждые 5 good','game.js:999-1044','CONFIRMED','Critical','HUD, tasks','TC-CORE-002; TC-CORE-006','CHK-03; CHK-05','PASS'),
('FEAT-CORE-005','Жизни, урон и поражение','Bad уменьшает жизнь; shield блокирует один раз; при 0 — gameOver','game.js:999-1021,759-791','CONFIRMED','Critical','Game state, ads','TC-CORE-003; TC-CORE-004; TC-CORE-007','CHK-03; CHK-08','PASS'),
('FEAT-CORE-006','Золотые бонусы','Gold запускает magnet/slow/double на ограниченное время','game.js:1038-1053','CONFIRMED','High','HUD, upgrades','TC-CORE-005','CHK-03','PASS'),
('FEAT-STATE-002','Системная пауза','Пауза при visibility/blur/SDK и продолжение при возврате','game.js:385-460,611-614','CONFIRMED','High','Audio, SDK','TC-STATE-001; TC-STATE-002','CHK-06','PARTIAL'),
('FEAT-UI-001','Главное меню и HUD','Меню, лучший счет, daily reward, HUD score/lives/combo, кнопки','index.html:15-110; style.css:1-743','CONFIRMED','High','Localization, state','TC-SMOKE-001; TC-UI-001; TC-UI-003','CHK-02; CHK-05','PARTIAL'),
('FEAT-UI-002','Адаптивный интерфейс','Safe-area, mobile/landscape breakpoints, прокручиваемые панели','style.css:45-743','CONFIRMED','High','Viewport, touch','TC-COMP-001..006; TC-UI-002','CHK-05; CHK-15','FAIL'),
('FEAT-GFX-001','Canvas-графика','Фон, частицы, эмодзи-мысли, картинка пылесоса и fallback-отрисовка','game.js:1416-1880','CONFIRMED','Medium','Assets, GPU/fonts','TC-GFX-001; TC-UI-002','CHK-12','PARTIAL'),
('FEAT-PROG-001','Лучший результат и звезды','Награды floor(score/100), best score, баланс звезд','game.js:759-791,873-876','CONFIRMED','High','Save, store','TC-CORE-007; TC-PROG-001','CHK-07','PARTIAL'),
('FEAT-SAVE-001','Локальное сохранение','localStorage key thoughtVacuumProgress.v1; нормализация части полей','game.js:554-608,1351-1394','CONFIRMED','Critical','All progression','TC-SAVE-001..004','CHK-09','FAIL'),
('FEAT-DAILY-001','Ежедневная награда','3 звезды один раз за локальную календарную дату','game.js:1300-1320,1408-1414','CONFIRMED','Medium','Save, local clock','TC-DAILY-001; TC-DAILY-002','CHK-07','PARTIAL'),
('FEAT-DAILY-002','Ежедневные задания','3 задачи из 5, награда 2, бонус за все 3','game.js:272-278,1193-1223,1322-1406','CONFIRMED','High','Save, gameplay','TC-DAILY-003..006','CHK-07','NOT_RUN'),
('FEAT-UPG-001','Постоянные улучшения','radius 0..5, bonus 0..5, life 0..1 за звезды','game.js:245-270,1123-1150,1286-1298','CONFIRMED','High','Economy, save','TC-UPG-001..004','CHK-07; CHK-10','NOT_RUN'),
('FEAT-BOOST-001','Расходуемые бустеры','magnetStart, shield, doubleStart; максимум 3 каждого','game.js:178-200,1151-1172,1226-1284','CONFIRMED','High','Economy, game start','TC-BOOST-001..003','CHK-07','FAIL'),
('FEAT-SKIN-001','Скины','4 ауры; blue бесплатный, остальные покупаются и выбираются','game.js:202-243,1173-1192,1240-1260','CONFIRMED','Medium','Save, renderer','TC-SKIN-001..003','CHK-07; CHK-12','NOT_RUN'),
('FEAT-ADS-001','Межстраничная реклама','После 3 завершенных раундов перед restart вызывается fullscreen ad','game.js:462-499,748-757','CONFIRMED','High','Yandex SDK, progression','TC-ADS-003; TC-ADS-004','CHK-18','BLOCKED'),
('FEAT-ADS-002','Rewarded revive','После поражения один revive за rewarded video','game.js:501-552,793-827','CONFIRMED','Critical','Yandex SDK, game state','TC-ADS-001; TC-ADS-005','CHK-08; CHK-18','FAIL'),
('FEAT-ADS-003','Rewarded x2 звезд','После поражения удвоение заработанных звезд за rewarded video','game.js:501-552,828-857','CONFIRMED','Critical','Yandex SDK, economy','TC-ADS-002; TC-ADS-006','CHK-08; CHK-18','FAIL'),
('FEAT-AUDIO-001','Синтезированный звук и mute','Web Audio для vacuum/good/bad/gold/combo/buy/over; mute сохраняется','game.js:1881-2047','CONFIRMED','Medium','Focus, localStorage','TC-AUDIO-001..004','CHK-11','PARTIAL'),
('FEAT-LOC-001','Русский и английский','Автовыбор по query/navigator/SDK; таблица строк RU/EN','game.js:78-176,291,306-382,444-454','CONFIRMED','High','UI, SDK','TC-LOC-001..005','CHK-17','PARTIAL'),
('FEAT-PLAT-001','Yandex Games SDK','/sdk.js, init, LoadingAPI, GameplayAPI, ad API','index.html:10-12; game.js:385-552','CONFIRMED','Critical','Network/platform','TC-PLAT-001..004','CHK-01; CHK-20','BLOCKED'),
]

requirements=[
('REQ-FUNC-001','После выбора «Играть» начинается раунд с базовым состоянием','UI text + startGame implementation','CONFIRMED','FEAT-CORE-001'),
('REQ-FUNC-002','Положительные мысли увеличивают score, отрицательные уменьшают lives','Game rules in menu + collectThought','CONFIRMED','FEAT-CORE-004; FEAT-CORE-005'),
('REQ-FUNC-003','Золотая мысль дает 50 очков и случайный временный бонус','Code consistency','CONFIRMED','FEAT-CORE-006'),
('REQ-FUNC-004','После 0 жизней показывается экран результата','State transition code/UI','CONFIRMED','FEAT-CORE-005; FEAT-STATE-001'),
('REQ-FUNC-005','Restart создает чистый раунд','Button label + startGame','CONFIRMED','FEAT-CORE-001'),
('REQ-SAVE-001','Корректное сохранение не должно ломать запуск и должно восстанавливаться','localStorage implementation + user expectation','CONFIRMED','FEAT-SAVE-001'),
('REQ-SAVE-002','Поврежденное сохранение обрабатывается безопасно без startup crash','Existing try/catch intent + robust recovery oracle','INFERRED','FEAT-SAVE-001'),
('REQ-ECON-001','Стоимость не списывается, если покупки нет или лимит достигнут','Button state + guard code','CONFIRMED','FEAT-UPG-001; FEAT-BOOST-001; FEAT-SKIN-001'),
('REQ-ECON-002','Расходуемый бустер списывается только при осознанном начале/продолжении раунда','User expectation; requires developer confirmation','INFERRED','FEAT-BOOST-001'),
('REQ-ADS-001','Rewarded-награда выдается только после onRewarded','Yandex SDK rewarded callback contract','CONFIRMED','FEAT-ADS-002; FEAT-ADS-003'),
('REQ-ADS-002','При SDK/ad error игра восстанавливает состояние без бесплатной награды','Platform behavior + economy integrity','INFERRED','FEAT-ADS-002; FEAT-ADS-003'),
('REQ-UI-001','Интерактивные элементы доступны и читаемы на целевых viewport','Yandex requirements + responsive CSS intent','CONFIRMED','FEAT-UI-001; FEAT-UI-002'),
('REQ-UI-002','Игровой объект остается достаточно видимым у границ','Common gameplay feedback oracle','INFERRED','FEAT-UI-002; FEAT-GFX-001'),
('REQ-INPUT-001','На mobile игра полностью управляется жестами и long-tap не вызывает browser UI','Yandex public requirements','CONFIRMED','FEAT-INPUT-001'),
('REQ-STATE-001','При minimization/blur звук и gameplay останавливаются','Yandex requirements + pause code','CONFIRMED','FEAT-STATE-002; FEAT-AUDIO-001'),
('REQ-LOC-001','Все основные UI-строки отображаются на одном выбранном языке','Translation tables + consistency oracle','CONFIRMED','FEAT-LOC-001'),
('REQ-ACC-001','Критическая информация не должна передаваться только цветом','Accessibility guideline','INFERRED','FEAT-UI-001; FEAT-GFX-001'),
('REQ-ACC-002','Кнопки должны иметь достаточный размер и различимый фокус','WCAG heuristic + game accessibility guideline','INFERRED','FEAT-UI-001'),
('REQ-PLAT-001','Yandex SDK подключен до YaGames.init и LoadingAPI.ready вызывается после загрузки','Yandex official SDK docs','CONFIRMED','FEAT-PLAT-001'),
('REQ-PLAT-002','GameplayAPI.start/stop отражают фактическую активность','Yandex official SDK docs','CONFIRMED','FEAT-PLAT-001; FEAT-STATE-002'),
]

risks=[
('RISK-START-001','Запуск','Игра не запускается из-за JS/resource ошибки','Broken package or exception','Нет доступа к игре','Medium','Critical','High','High','FEAT-PLAT-001; FEAT-SAVE-001','TC-SMOKE-001; TC-SAVE-002','Исправлять до релиза','OPEN'),
('RISK-SAVE-001','Сохранение','Поврежденное состояние блокирует инициализацию','Недостаточная валидация nested data','Пользователь вынужден очищать данные','Medium','Critical','High','High','FEAT-SAVE-001','TC-SAVE-002','Добавить схему/normalization fallback','CONFIRMED'),
('RISK-SAVE-002','Сохранение','Потеря прогресса при quota/privacy error','localStorage.setItem exception','Потеря звезд/покупок','Low','High','Medium','Medium','FEAT-SAVE-001','TC-SAVE-004','Показать ненавязчивое предупреждение','OPEN'),
('RISK-SAVE-003','Сохранение','Манипуляция системной датой повторяет daily reward','Локальная дата без server time','Экономический exploit','Medium','Medium','Medium','Low','FEAT-DAILY-001','TC-DAILY-002','Принять риск или использовать server time','OPEN'),
('RISK-ADS-001','Реклама','Награда выдается без фактического rewarded video','Fallback вызывает onReward','Потеря монетизации и обход прогрессии','High','Critical','High','High','FEAT-ADS-002; FEAT-ADS-003','TC-ADS-001; TC-ADS-002','Не выдавать reward при SDK unavailable','CONFIRMED'),
('RISK-ADS-002','Реклама','Игра не восстанавливается после ad close/error','Ошибки callback/state','Soft lock или потеря раунда','Medium','High','High','Medium','FEAT-ADS-001..003','TC-ADS-004..006','Проверить на реальной платформе','OPEN'),
('RISK-ECON-001','Экономика','Расходуемые бустеры теряются при случайном выходе','Списание при start + мгновенный Menu','Потеря заработанного ресурса','High','High','High','High','FEAT-BOOST-001','TC-BOOST-002','Подтверждение или возврат','CONFIRMED'),
('RISK-CORE-001','Gameplay','Неверный score/combo','Ошибки порядка множителей','Несправедливый результат','Medium','High','High','High','FEAT-CORE-004','TC-CORE-002; TC-CORE-006','Регрессия после balance changes','MITIGATED'),
('RISK-CORE-002','Gameplay','Неверные условия поражения/revive','State transition defect','Нельзя продолжить/завершить','Medium','Critical','High','High','FEAT-CORE-005; FEAT-ADS-002','TC-CORE-007; TC-ADS-005','Critical regression','OPEN'),
('RISK-CORE-003','Gameplay','Игрок не может закончить сессию естественно','Spawn/collision/score issue','Soft lock','Low','High','Medium','Medium','FEAT-CORE-002..006','TC-CORE-012','Natural-play session','OPEN'),
('RISK-INPUT-001','Input','Потеря фокуса оставляет игру активной','Event ordering','Нечестный урон, звук в фоне','Medium','High','High','Medium','FEAT-STATE-002','TC-STATE-001; TC-STATE-002','Реальный Alt+Tab тест','PARTIAL'),
('RISK-INPUT-002','Input','Multi-touch/быстрый ввод двигает объект непредсказуемо','Нет pointerId ownership','Потеря контроля','Medium','Medium','Medium','Low','FEAT-INPUT-001','TC-INPUT-003','Mobile exploratory','OPEN'),
('RISK-UI-001','UI/GFX','Пылесос обрезается у границ','Clamp не учитывает sprite bounds','Слабая видимость состояния/коллизии','High','Low','Medium','High','FEAT-UI-002; FEAT-GFX-001','TC-UI-002','Учитывать visual bounds','CONFIRMED'),
('RISK-UI-002','UI','HUD/текст обрезается на малых экранах','Responsive edge cases','Недоступны команды/данные','Medium','High','High','Medium','FEAT-UI-002','TC-COMP-001..006','Viewport matrix','PARTIAL'),
('RISK-UI-003','UI','Недостаточный contrast белого текста кнопок','Accent colors 2.13–2.65:1','Снижение читаемости','High','Medium','High','High','FEAT-UI-001','TC-ACC-002','Темнее фон или темный текст','OPEN'),
('RISK-AUDIO-001','Audio','Звук продолжает играть в фоне','Suspend/resume race','Нарушение platform requirement','Medium','High','High','Medium','FEAT-AUDIO-001; FEAT-STATE-002','TC-AUDIO-002','Real focus test','OPEN'),
('RISK-AUDIO-002','Audio','Mute не сохраняется/не применяет все звуки','Partial state handling','Раздражение/доступность','Low','Medium','Medium','High','FEAT-AUDIO-001','TC-AUDIO-001','Regression','MITIGATED'),
('RISK-PERF-001','Performance','Рост thoughts/particles или long frames','Object churn + emoji rendering','FPS drops/input lag','Medium','High','High','Low','FEAT-GFX-001; FEAT-CORE-002','TC-PERF-001..003','Profile real session','OPEN'),
('RISK-COMP-001','Compatibility','Emoji/assets различаются или отсутствуют','OS font/image packaging','Плохая читаемость объектов','Medium','Medium','Medium','Low','FEAT-GFX-001','TC-GFX-001; TC-COMP-007','Test browsers/devices','OPEN'),
('RISK-LOC-001','Localization','Смешение RU/EN или обрезание длинных строк','Missing key/layout','Непонятный UI','Medium','Medium','Medium','High','FEAT-LOC-001','TC-LOC-001..005','Pseudo/long string checks','PARTIAL'),
('RISK-PLAT-001','Platform','SDK initialization/loader не проходит moderation','Unavailable/old loader','Нельзя опубликовать','Medium','Critical','High','Low','FEAT-PLAT-001','TC-PLAT-001','Test debug panel IT','BLOCKED'),
('RISK-PLAT-002','Platform','Архив содержит неверную структуру assets','Provided files outside assets','Missing player art/script','Medium','High','High','High','FEAT-GFX-001; FEAT-PLAT-001','TC-BUILD-001','Verify release ZIP structure','OPEN'),
('RISK-SEC-001','Security/privacy','Секреты/PII попадают в клиент или логи','Client-only integration','Exposure','Low','High','Medium','Medium','FEAT-PLAT-001','TC-SEC-001','Static secret scan','MITIGATED'),
('RISK-PHYS-001','Collision','Визуальная модель не соответствует collision radius','Sprite ~170 px vs radius 36','Непонятные попадания','Medium','Medium','Medium','Low','FEAT-GFX-001; FEAT-CORE-005','TC-CORE-013','Collision visualization session','OPEN'),
('RISK-MEM-001','Stability','Длительная сессия вызывает memory leak','Canvas/audio object lifetime','Crash/slowdown','Low','High','Medium','Low','FEAT-GFX-001; FEAT-AUDIO-001','TC-PERF-002','Real soak with profiler','OPEN'),
('RISK-ACC-001','Accessibility','Нет keyboard/gamepad gameplay','Pointer-only mechanic','Часть игроков не может играть','High','High','High','High','FEAT-INPUT-001','TC-ACC-003','Добавить keyboard alternative','OPEN'),
('RISK-ACC-002','Accessibility','Нет настройки shake/motion','Hit shake hard-coded','Дискомфорт','Medium','Medium','Medium','High','FEAT-GFX-001','TC-ACC-004','Toggle reduced motion','OPEN'),
('RISK-ACC-003','Accessibility','Canvas не передает gameplay state assistive tech','Single aria-label only','Screen reader cannot play','High','High','High','High','FEAT-GFX-001','TC-ACC-005','Alternative semantic feedback','OPEN'),
('RISK-EXT-001','External services','No network / SDK error changes rewards/state','Fallback semantics','Economy inconsistency','High','High','High','High','FEAT-ADS-001..003; FEAT-PLAT-001','TC-ADS-001..006','Explicit offline/error state','CONFIRMED'),
('RISK-COUNT-001','Counters','Большие/negative values ломают HUD/economy','Corrupt save or long play','Overflow/clipping/exploit','Low','Medium','Medium','Medium','FEAT-PROG-001; FEAT-SAVE-001','TC-PROG-002','Boundary tests','OPEN'),
]

# Test case helper
cases=[]
def tc(id,feat,risk,module,title,obj,pre,data,steps,exp,status='NOT_RUN',actual='Not executed',priority='Medium',typ='Functional',tech='Scenario',platform='Web',evidence='',bug='',notes=''):
    cases.append({'Test Case ID':id,'Feature ID':feat,'Risk ID':risk,'Module':module,'Title':title,'Objective':obj,'Preconditions':pre,'Test Data':data,'Steps':steps,'Expected Result':exp,'Actual Result':actual,'Status':status,'Priority':priority,'Test Type':typ,'Test Technique':tech,'Platform':platform,'Build':BUILD,'Environment':ENV,'Evidence':evidence,'Related Bug':bug,'Notes':notes})

# 32 executed mapped from dynamic checks
tc('TC-SMOKE-001','FEAT-STATE-001','RISK-START-001','Launch','Чистый запуск меню','Проверить базовую инициализацию','Пустое mock localStorage','ru-RU','1. Загрузить test harness.\n2. Дождаться инициализации.\n3. Проверить активный menuScreen и кнопку Играть.','Меню активно; критические элементы видимы.','PASS','Меню отображено, game.js инициализирован.','Critical','Smoke','Critical path',evidence='evidence/EV-001_menu_1024x768.png')
tc('TC-SMOKE-002','FEAT-CORE-001','RISK-START-001','Launch','Доступность runtime state','Проверить выполнение script','Игра загружена','N/A','1. Проверить typeof startGame/progress/game.','Функции и state доступны.','PASS','startGame=function, progress=object, game=object.','Critical','Smoke','Static/dynamic check')
tc('TC-LOC-001','FEAT-LOC-001','RISK-LOC-001','Localization','Автовыбор English','Проверить en locale','Чистое состояние','navigator.language=en-US','1. Запустить с en-US locale.\n2. Проверить html lang, title, Play.','UI English; lang=en.','PASS','Thought Vacuum / Play / lang=en.','High','Localization','Equivalence partition',evidence='evidence/EV-002_menu_en.png')
tc('TC-LOC-002','FEAT-LOC-001','RISK-LOC-001','Localization','Русская локализация и map codes','Проверить RU и fallback mapping','Чистое состояние','ru-RU, be-BY, kk-KZ, uk-UA, de-DE','1. Запустить ru-RU.\n2. Вызвать resolveLanguage для кодов.','ru/be/kk/uk/uz→ru; прочие→en.','PASS',"mapping=['ru','ru','ru','en']; Играть. 'uz' подтвержден статически.",'High','Localization','Decision table')
tc('TC-DAILY-001','FEAT-DAILY-001','RISK-SAVE-003','Daily','Получение daily reward один раз','Проверить начисление/persistence','Награда сегодня не получена','stars=0','1. Нажать daily reward.\n2. Проверить +3 и disabled.\n3. Перезапустить с сохраненным state.','+3; повтор недоступен; состояние восстановлено.','PASS','stars 0→3, кнопка disabled после повторной загрузки.','High','Functional','State transition')
tc('TC-UI-001','FEAT-STATE-001','RISK-UI-002','UI','Навигация в мастерскую','Проверить screen flow и карточки','Меню','N/A','1. Нажать Улучшения.\n2. Проверить 3/3/4/3 карточки.\n3. Нажать Назад.','Переходы корректны; menu восстановлено.','PASS','Counts 3 upgrades, 3 boosters, 4 skins, 3 tasks; возврат успешен.','High','Functional','User journey')
tc('TC-ACC-001','FEAT-UI-001','RISK-ACC-001','Accessibility','Tab navigation меню','Проверить клавиатурную достижимость кнопок','Меню','Tab','1. Нажимать Tab 8 раз.\n2. Записать activeElement.','Daily, Play, Upgrades получают фокус.','PASS','Фокус достиг dailyRewardButton, playButton, upgradesButton.','High','Accessibility','Exploratory')
tc('TC-CORE-001','FEAT-CORE-001','RISK-CORE-002','Gameplay','Старт раунда','Проверить стартовое состояние','Меню','Play','1. Нажать Играть.\n2. Проверить state/HUD.','game, running=true, score=0, lives=3, combo=1.','PASS','Точное стартовое состояние подтверждено.','Critical','Smoke','State transition',evidence='evidence/EV-003_game_start.png')
tc('TC-INPUT-001','FEAT-INPUT-001','RISK-INPUT-002','Input','Boundary pointer target','Проверить clamp координат','Активный раунд','(-100,-100), (2000,2000), viewport 1024×768','1. Передать координаты ниже min.\n2. Передать выше max.\n3. Проверить tx/ty.','20,20 и 1004,748.','PASS','Получены 20,20 и 1004,748.','High','Functional','Boundary value analysis')
tc('TC-STATE-001','FEAT-STATE-002','RISK-INPUT-001','State','Pause/resume API','Проверить system pause transitions','Активный раунд','reason=window','1. pauseActiveGame(window).\n2. Проверить false/reason.\n3. resumeSystemPausedGame(window).','running false→true; reason очищен.','PASS','Переход выполнен.','High','Functional','State transition')
tc('TC-CORE-002','FEAT-CORE-004','RISK-CORE-001','Gameplay','5 good thoughts повышают combo','Проверить scoring/streak','Активный раунд','5 good','1. Сбросить score/combo.\n2. Собрать 5 good.\n3. Проверить значения.','score=50, streak=5, combo=2.','PASS','50/5/x2.','Critical','Functional','Boundary value analysis')
tc('TC-CORE-003','FEAT-CORE-005','RISK-CORE-002','Gameplay','Bad без shield','Проверить урон','3 жизни, no shield','1 bad','1. Столкнуться с bad.\n2. Проверить lives/combo/streak.','lives=2; combo=1; streak=0.','PASS','Подтверждено.','Critical','Functional','State transition')
tc('TC-CORE-004','FEAT-CORE-005','RISK-CORE-002','Gameplay','Shield блокирует bad','Проверить одноразовую защиту','3 жизни, shield=true','1 bad','1. Столкнуться с bad.\n2. Проверить жизнь и shield.','lives=3; shield=false.','PASS','Подтверждено.','Critical','Functional','Decision table')
tc('TC-CORE-005','FEAT-CORE-006','RISK-CORE-001','Gameplay','Gold начисляет бонус','Проверить reward','combo=1, timers=0','1 gold','1. Собрать gold.\n2. Проверить score и timers.','score +50; один timer >0.','PASS','score=50; magnet=6 в данном run.','High','Functional','Equivalence partition')
tc('TC-CORE-006','FEAT-CORE-004','RISK-CORE-001','Gameplay','Double и combo множители','Проверить порядок множителей','combo=2, double=active','1 good','1. Собрать good.\n2. Проверить score.','10×2×2=40.','PASS','40.','High','Functional','Decision table')
tc('TC-CORE-007','FEAT-CORE-005','RISK-CORE-002','Game over','Поражение и награда','Проверить endGame','score=250, lives=1','1 bad','1. Получить bad.\n2. Проверить result screen, best, earned stars.','gameOver; best≥250; earned=2.','PASS','gameOver; best=250; earned=2.','Critical','Smoke','Critical path',evidence='evidence/EV-004_game_over.png')
tc('TC-CORE-008','FEAT-CORE-001','RISK-CORE-002','Restart','Чистый restart','Проверить повторный запуск','gameOver','Restart','1. Нажать Играть снова.\n2. Проверить state.','score=0, lives=3, combo=1, running.','PASS','Подтверждено.','Critical','Smoke','State transition')
tc('TC-SAVE-001','FEAT-SAVE-001','RISK-SAVE-001','Save','Невалидный JSON','Проверить fallback','localStorage value=not-json','not-json','1. Запустить.\n2. Проверить menu/default state.','Игра запускается с defaults и warning.','PASS','best=0, stars=0, menu; warning в browser_console.json.','Critical','Negative','Error guessing')
tc('TC-AUDIO-001','FEAT-AUDIO-001','RISK-AUDIO-002','Audio','Mute persistence','Проверить сохранение mute','Активный раунд','soundMuted false→true','1. Нажать mute.\n2. Сохранить и повторно загрузить state.\n3. Проверить aria-label.','soundMuted=true; label Включить звук.','PASS','Подтверждено.','Medium','Functional','State transition')
tc('TC-BOOST-001','FEAT-BOOST-001','RISK-ECON-001','Boosters','Активация трех boosters','Проверить списание/эффект','По 1 каждого','magnet/shield/double','1. Установить inventory.\n2. Start.\n3. Проверить inventory/timers.','Counts 0; timers active; shield true.','PASS','magnet≈5.95, double≈7.95, shield=true.','High','Functional','Decision table')
tc('TC-BOOST-002','FEAT-BOOST-001','RISK-ECON-001','Boosters','Выход в Menu после старта с boosters','Проверить защиту от случайной потери','Boosters активированы','Menu','1. Start с boosters.\n2. Нажать Menu.\n3. Проверить confirmation/return.','Есть подтверждение либо неиспользованные boosters возвращаются.','FAIL','Выход мгновенный; все boosters остаются списанными.','High','Usability/Functional','User journey',evidence='evidence/BUG-004_step-01_boosters-active.png; evidence/BUG-004_result_menu-no-confirmation.png',bug='BUG-004')
tc('TC-ADS-001','FEAT-ADS-002','RISK-ADS-001','Ads','Revive без SDK','Проверить reward integrity','gameOver; yaSdk=null; revive available','Click revive','1. Нажать Смотреть рекламу +1 жизнь.\n2. Наблюдать ad/reward.','Без onRewarded reward не выдается; выводится error/retry.','FAIL','Реклама не показывается; revive выдан синхронно, lives=1.','Critical','Negative','Decision table',platform='Yandex/standalone fallback',evidence='evidence/BUG-002_step-01_game-over.png; evidence/BUG-002_result_revived-without-ad.png',bug='BUG-002')
tc('TC-ADS-002','FEAT-ADS-003','RISK-ADS-001','Ads','x2 stars без SDK','Проверить reward integrity','gameOver; earned>0; yaSdk=null','Click x2','1. Нажать x2 stars.\n2. Наблюдать ad/reward.','Без onRewarded reward не выдается.','FAIL','stars 2→4 без рекламы.','Critical','Negative','Decision table',platform='Yandex/standalone fallback',evidence='logs/tests.log',bug='BUG-002')
tc('TC-UI-002','FEAT-UI-002','RISK-UI-001','Graphics','Пылесос у левой границы','Проверить видимость avatar','Активный раунд','pointer x=0','1. Переместить указатель к левому краю.\n2. Дождаться follow.\n3. Оценить sprite.','Основная часть sprite и feedback остаются видимыми.','FAIL','Пылесос почти полностью обрезан; center x≈23.2.','Medium','Visual','Boundary value analysis',evidence='evidence/BUG-003_result.png',bug='BUG-003')
tc('TC-PERF-001','FEAT-GFX-001','RISK-PERF-001','Performance','Update-loop stress','Проверить отсутствие exception/NaN в state loop','Активный game; spawn disabled for isolation','3000×0.033s','1. Выполнить 3000 updateGame.\n2. Проверить finite state.','Нет exception/NaN; running remains true.','PASS','~99.9s simulated; no exception.','Medium','Stability','Stress',notes='Не FPS/soak и не реальное время.')
tc('TC-SAVE-002','FEAT-SAVE-001','RISK-SAVE-001','Save','dailyTasks содержит null','Проверить nested corruption recovery','JSON valid, dailyTasks=[null,null,null]','Corrupt structured save','1. Запустить с сохранением.\n2. Наблюдать pageerror/инициализацию.','Invalid nested entries сбрасываются; menu функционально.','FAIL',"Uncaught TypeError: Cannot read properties of null (reading 'id').",'Critical','Negative','Robustness/error guessing',evidence='evidence/BUG-001_result.png; logs/page_errors.json',bug='BUG-001')
for i,(w,h) in enumerate([(320,568),(360,640),(768,1024),(1366,768),(1920,1080)],1):
    tc(f'TC-COMP-00{i}','FEAT-UI-002','RISK-UI-002','Compatibility',f'Мастерская {w}×{h}','Проверить layout/scroll','Чистое состояние',f'{w}×{h}','1. Открыть мастерскую.\n2. Проверить panel scroll и доступность Back.','Back существует; panel scrollable при необходимости.','PASS',f'panel scroll/client подтверждены; screenshot EV-VP-{w}x{h}.png.','Medium','Compatibility','Pairwise/viewport',platform='Chromium',evidence=f'evidence/EV-VP-{w}x{h}.png')
tc('TC-COMP-006','FEAT-UI-002','RISK-UI-002','Compatibility','Touch scroll 360×640','Проверить прокрутку длинной panel','Mobile emulation, touch','Swipe up','1. Открыть master.\n2. Выполнить touch swipe.\n3. Проверить scrollTop.','scrollTop увеличивается.','PASS','0→451.','High','Compatibility','Gesture test',platform='Chromium mobile emulation',evidence='evidence/EV-008_mobile_touch_scroll.png')

# remaining blocked/not-run cases
blocked_reason='Blocked: реальная среда Yandex Games и loader/debug panel недоступны.'
tc('TC-PLAT-001','FEAT-PLAT-001','RISK-PLAT-001','Platform','SDK loader indicator IT','Проверить актуальное подключение SDK','Опубликованный draft/debug panel','debug-mode=16','1. Открыть draft debug panel.\n2. Проверить loader indicator.','Indicator IT; init succeeds.','BLOCKED',blocked_reason,'Critical','Platform','Compliance check',platform='Yandex Games')
tc('TC-ADS-003','FEAT-ADS-001','RISK-ADS-002','Ads','Реальный interstitial после 3 rounds','Проверить platform ad flow','Yandex SDK, 3 completed rounds','Restart','1. Завершить 3 rounds.\n2. Restart.\n3. Наблюдать ad callbacks.','Ad API called; game resumes/start after close/error.','BLOCKED',blocked_reason,'Critical','Platform','State transition',platform='Yandex Games')
notruns=[
('TC-BUILD-001','FEAT-PLAT-001','RISK-PLAT-002','Build','Release ZIP structure','Проверить корневой index/assets','Release archive','ZIP','Распаковать; сверить paths; открыть через Yandex local server.','Нет missing resources.','Critical','Build verification','Checklist'),
('TC-INPUT-002','FEAT-INPUT-001','RISK-INPUT-002','Input','Реальное mouse/touch управление','Проверить feel/latency','Playable runtime','Mouse/touch','Играть 3 минуты на каждом input.','Точный и предсказуемый контроль.','Critical','Manual','Exploratory'),
('TC-INPUT-003','FEAT-INPUT-001','RISK-INPUT-002','Input','Multi-touch и conflict','Проверить pointer ownership','Mobile device','2 fingers','Одновременно двигать двумя пальцами/отпускать.','Нет скачков/залипания.','High','Negative','Error guessing'),
('TC-INPUT-004','FEAT-INPUT-001','RISK-ACC-001','Input','Keyboard gameplay alternative','Проверить возможность играть без pointer','Desktop','Arrows/WASD','Попробовать управлять keyboard.','Поддерживаемая альтернатива либо явно N/A по design.','Medium','Accessibility','Exploratory'),
('TC-STATE-002','FEAT-STATE-002','RISK-INPUT-001','State','Реальный Alt+Tab/blur','Проверить pause/audio','Desktop browser','Alt+Tab','Во время hazards Alt+Tab 10s и вернуться.','Gameplay frozen; no damage; audio stopped/resumes.','Critical','Manual','State transition'),
('TC-CORE-009','FEAT-CORE-002','RISK-CORE-003','Gameplay','Spawn distribution sanity','Проверить все thought types','Natural play','100 spawns','Записать 100 spawn types.','Good/bad/gold появляются; нет невозможных positions.','Medium','Exploratory','Statistical sampling'),
('TC-CORE-010','FEAT-CORE-002','RISK-PERF-001','Gameplay','Spawn pace over time','Проверить pace min boundary','Long round','elapsed 0/30/60s','Сравнить интервалы.','Pace ускоряется и не ниже 0.38 base range.','Medium','Functional','Boundary value analysis'),
('TC-CORE-011','FEAT-CORE-003','RISK-PHYS-001','Physics','Magnet attraction/repulsion','Проверить vectors visually','Magnet active','good/gold/bad around player','Разместить объекты на границе radius.','Good/gold toward; bad away; no teleport.','High','Physics','Boundary/state'),
('TC-CORE-012','FEAT-CORE-005','RISK-CORE-003','Gameplay','Natural complete session','Проверить полный цикл без state injection','Fresh profile','Mouse/touch','Играть до gameOver; restart; repeat.','Цикл завершен естественно без soft lock.','Critical','End-to-end','User journey'),
('TC-CORE-013','FEAT-GFX-001','RISK-PHYS-001','Collision','Visual vs collision radius','Проверить понятность hitbox','Active round','Bad at sprite edges','Подвести bad к видимым краям sprite.','Collision соответствует визуальному ожиданию.','High','Gameplay UX','Exploratory'),
('TC-DAILY-002','FEAT-DAILY-001','RISK-SAVE-003','Daily','Изменение системной даты','Проверить anti-exploit/date rollover','Daily claimed','Clock +1/-1 day','Менять дату и перезапускать.','Поведение определено; нет бесконечной награды либо риск принят.','Medium','Negative','Boundary/state'),
('TC-DAILY-003','FEAT-DAILY-002','RISK-CORE-001','Daily','Progress good/gold tasks','Проверить счетчики','Task selected','Exact target±1','Собирать target-1, target, target+1.','Clamp target; claim enabled exactly at target.','High','Functional','Boundary value analysis'),
('TC-DAILY-004','FEAT-DAILY-002','RISK-SAVE-002','Daily','Claim task reward once','Проверить economy/persistence','Completed task','Double click/reload','Нажать Claim быстро 2x; reload.','+2 once; claimed persists.','High','Negative','State transition'),
('TC-DAILY-005','FEAT-DAILY-002','RISK-SAVE-003','Daily','All tasks bonus','Проверить +3 once','All 3 claimed','Open upgrades repeatedly','Открыть master несколько раз.','+3 one time only.','High','Functional','Decision table'),
('TC-DAILY-006','FEAT-DAILY-002','RISK-LOC-001','Daily','Midnight rollover','Проверить reset','Near local midnight','Date transition','Оставить open/перезапустить после midnight.','Tasks reset consistently; old reward state handled.','Medium','State','Boundary value analysis'),
('TC-UPG-001','FEAT-UPG-001','RISK-ECON-001','Upgrades','Покупка каждого level','Проверить cost/level','Enough stars','All costs','Покупать по одному level.','Correct cost; level+1; persists.','High','Functional','Boundary value analysis'),
('TC-UPG-002','FEAT-UPG-001','RISK-COUNT-001','Upgrades','Max limits','Проверить 5/5,1/1','At max','Extra click','Попытаться купить beyond max.','No debit; button Max disabled.','High','Negative','Boundary value analysis'),
('TC-UPG-003','FEAT-UPG-001','RISK-ECON-001','Upgrades','Insufficient stars','Проверить disabled/guard','stars=cost-1','Each upgrade','Открыть master/call action.','No debit/level change.','High','Negative','Equivalence partition'),
('TC-UPG-004','FEAT-UPG-001','RISK-CORE-001','Upgrades','Bonus duration effect','Уточнить область действия upgrade','bonus level 0/5','Random and starting bonuses','Сравнить durations.','All intended bonus types follow specification.','Medium','Functional','Decision table'),
('TC-BOOST-003','FEAT-BOOST-001','RISK-ECON-001','Boosters','Inventory max 3','Проверить cap','stars enough','Buy 4','Купить каждый booster 4 times.','Count max 3; 4th no debit.','High','Boundary','Boundary value analysis'),
('TC-SKIN-001','FEAT-SKIN-001','RISK-ECON-001','Skins','Purchase/select/persist','Проверить store','Enough stars','pink/gold/cosmic','Купить; restart; select.','Owned/active persisted; one debit.','Medium','Functional','State transition'),
('TC-SKIN-002','FEAT-SKIN-001','RISK-ECON-001','Skins','Insufficient stars','Проверить guard','cost-1','Paid skin','Click/call purchase.','No ownership/debit.','Medium','Negative','Equivalence partition'),
('TC-SKIN-003','FEAT-SKIN-001','RISK-COMP-001','Skins','Visual distinction','Проверить aura colors/readability','All owned','4 skins','Снять screenshots same state.','Skins visually distinct; gameplay meaning unchanged.','Low','Visual','Comparative'),
('TC-ADS-004','FEAT-ADS-001','RISK-ADS-002','Ads','Interstitial error callback','Проверить recovery','Mock SDK onError','Error object','Trigger restart threshold.','Game starts after error; no stuck audio/state.','High','Integration','Decision table'),
('TC-ADS-005','FEAT-ADS-002','RISK-ADS-002','Ads','Real rewarded revive callbacks','Проверить reward only after onRewarded','Yandex SDK','Close before reward / reward / error','Выполнить 3 paths.','Reward only rewarded path; buttons recover.','Critical','Integration','Decision table'),
('TC-ADS-006','FEAT-ADS-003','RISK-ADS-002','Ads','Real rewarded x2 callbacks','Проверить stars integrity','Yandex SDK','Close/reward/error','Выполнить paths.','Stars added once only on reward.','Critical','Integration','Decision table'),
('TC-AUDIO-002','FEAT-AUDIO-001','RISK-AUDIO-001','Audio','Audio on blur/minimize','Проверить requirement','Real browser/device','Alt+Tab/minimize','Слушать до/после background.','Sound stops immediately; resumes appropriately.','High','Manual','State transition'),
('TC-AUDIO-003','FEAT-AUDIO-001','RISK-AUDIO-002','Audio','Sound event mapping','Проверить каждый cue','Audio enabled','good/combo/gold/bad/buy/over','Вызвать события и прослушать.','Distinct correct cues; no overlap artifact.','Medium','Audio','Exploratory'),
('TC-AUDIO-004','FEAT-AUDIO-001','RISK-AUDIO-002','Audio','Rapid mute/unmute','Проверить race','Active game','20 toggles','Быстро переключать.','No exception/stuck sound.','Medium','Negative','Stress'),
('TC-GFX-001','FEAT-GFX-001','RISK-COMP-001','Graphics','Missing image fallback','Проверить graceful fallback','Remove/deny image in test copy','404 image','Launch/play.','Fallback vacuum visible; warning only.','Medium','Recovery','Fault injection'),
('TC-PERF-002','FEAT-GFX-001','RISK-MEM-001','Performance','30-minute real soak','Проверить memory/stability','Production-like runtime','30 min natural play','Record memory/FPS every 5 min.','No unbounded growth/crash; thresholds documented.','High','Performance','Soak'),
('TC-PERF-003','FEAT-GFX-001','RISK-PERF-001','Performance','FPS/frame-time heavy scene','Профилировать max objects/particles','Profiler available','Gold bursts + high elapsed','Capture 60s metrics.','No unacceptable long frames per accepted target.','High','Performance','Load/stress'),
('TC-COMP-007','FEAT-GFX-001','RISK-COMP-001','Compatibility','Cross-browser matrix','Проверить Chrome/Firefox/Safari/mobile','Devices available','Latest stable browsers','Run smoke each.','No critical differences.','High','Compatibility','Pairwise'),
('TC-COMP-008','FEAT-UI-002','RISK-UI-002','Compatibility','Orientation/resize during game','Проверить layout/state','Mobile/tablet','portrait↔landscape','Rotate/resize repeatedly.','No distortion/lost state; input bounds update.','High','Compatibility','State transition'),
('TC-LOC-003','FEAT-LOC-001','RISK-LOC-001','Localization','Полный RU string audit','Проверить missing/mixed strings','All screens','ru','Обойти все states/items/tasks/bonuses.','No English/raw keys.','Medium','Localization','Checklist'),
('TC-LOC-004','FEAT-LOC-001','RISK-LOC-001','Localization','Полный EN string audit','Проверить grammar/overflow','All screens','en','Обойти all screens/items/tasks.','No Russian/raw keys/overflow.','Medium','Localization','Checklist'),
('TC-LOC-005','FEAT-LOC-001','RISK-LOC-001','Localization','Long strings/pseudo-loc','Проверить flexible layout','Instrumented strings','×1.5 length','Подставить длинные строки в QA copy.','No clipping/overlap; scroll available.','Low','Localization','Boundary'),
('TC-ACC-002','FEAT-UI-001','RISK-UI-003','Accessibility','Text contrast','Проверить button text contrast','CSS colors','white vs accent gradient','Рассчитать ratios/визуально.','Meet accepted contrast heuristic or documented exception.','High','Accessibility','Static analysis'),
('TC-ACC-003','FEAT-INPUT-001','RISK-ACC-001','Accessibility','One-hand/keyboard alternative','Оценить motor accessibility','Desktop/mobile','Keyboard/single pointer','Попытаться complete cycle.','Control alternative or documented limitation.','High','Accessibility','User journey'),
('TC-ACC-004','FEAT-GFX-001','RISK-ACC-002','Accessibility','Reduced motion/shake','Проверить option','Bad collision','Repeated hits','Искать toggle/reduced-motion OS behavior.','Shake can be reduced/disabled.','Medium','Accessibility','Checklist'),
('TC-ACC-005','FEAT-GFX-001','RISK-ACC-003','Accessibility','Screen reader gameplay state','Проверить semantics','Screen reader','Menu/game/HUD/result','Navigate/read/play.','Critical state/actions communicated.','High','Accessibility','Assistive tech'),
('TC-PROG-001','FEAT-PROG-001','RISK-COUNT-001','Progress','Score→stars boundaries','Проверить floor(score/100)','End game','0,99,100,199,200','End each score.','0,0,1,1,2 new stars.','High','Functional','Boundary value analysis'),
('TC-PROG-002','FEAT-PROG-001','RISK-COUNT-001','Progress','Large/corrupt counters','Проверить rendering/normalization','Injected save','-1, 0, 2^53, Infinity unavailable in JSON','Load values.','No negative; finite values; UI usable.','Medium','Robustness','Boundary/error guessing'),
('TC-SAVE-003','FEAT-SAVE-001','RISK-SAVE-002','Save','Write failure/quota','Проверить recovery/message','Mock setItem throw','QuotaExceededError','Trigger progress changes.','Game continues; user informed or risk documented.','High','Recovery','Fault injection'),
('TC-SAVE-004','FEAT-SAVE-001','RISK-SAVE-002','Save','Multiple sequential saves','Проверить latest state','Normal profile','100 changes','Buy/claim/play/reload.','Latest consistent state, no partial corruption.','High','Stability','Stress'),
('TC-PLAT-002','FEAT-PLAT-001','RISK-PLAT-001','Platform','LoadingAPI.ready timing','Проверить loader finish','Yandex debug panel','Cold launch','Observe loading indicator/call.','ready after playable resources loaded.','Critical','Integration','Timing'),
('TC-PLAT-003','FEAT-PLAT-001','RISK-PLAT-001','Platform','GameplayAPI lifecycle','Проверить start/stop sequence','Instrument SDK','Play/pause/ad/gameOver/menu','Record events.','No duplicate/missing; active periods match play.','High','Integration','State model'),
('TC-PLAT-004','FEAT-PLAT-001','RISK-PLAT-001','Platform','Platform moderation requirements','Проверить applicable public requirements','Draft complete','Desktop/mobile','Run Yandex requirement checklist.','No mandatory violations; evidence retained.','Critical','Compliance','Checklist'),
('TC-SEC-001','FEAT-PLAT-001','RISK-SEC-001','Security','Static secret/PII scan','Проверить client files','Source set','token/key/password patterns','Search files and inspect endpoints.','No secrets/PII.','High','Security','Static analysis'),
]
for x in notruns:
    id,feat,risk,module,title,obj,pre,data,steps,exp,priority,typ,tech=x
    tc(id,feat,risk,module,title,obj,pre,data,steps,exp,'NOT_RUN','Not executed',priority,typ,tech)

assert len(cases)==83, len(cases)

bugs=[
{
'Bug ID':'BUG-001','Title':'Игра не завершает инициализацию, если сохранение содержит null в массиве dailyTasks','Confirmation':'CONFIRMED','Component':'Save / startup','Build':BUILD,'Environment':ENV,
'Preconditions':'В localStorage по ключу thoughtVacuumProgress.v1 находится валидный JSON с dailyTasks:[null,null,null].','Steps':'1. Записать указанное значение.\n2. Запустить игру.\n3. Наблюдать console/pageerror и попытаться использовать меню.',
'Actual':'В ensureDailyState вызывается task.id для null; возникает TypeError и дальнейшая инициализация прерывается.','Expected':'Некорректные nested entries должны быть отброшены, а state сброшен к безопасному default без startup exception.','Frequency':'3/3 в изолированном Chromium harness','Severity':'S2 — Critical','Priority':'P1','Impact':'Затронутый пользователь не может полноценно запустить игру, пока вручную не очистит localStorage.','Workaround':'Очистить site data/localStorage; прогресс теряется.','Regression':'Unknown; no history','Tests':'TC-SAVE-002','Features':'FEAT-SAVE-001','Evidence':'evidence/BUG-001_result.png; logs/page_errors.json; logs/tests.log','Logs':'page_errors.json: Cannot read properties of null (reading id)','Additional':'Невалидный JSON обрабатывается, но валидный JSON с некорректной структурой — нет.','Code':'game.js:1374-1394; входные данные из game.js:582-603','Cause confidence':'High'},
{
'Bug ID':'BUG-002','Title':'Rewarded-награды выдаются без рекламы, когда Yandex SDK недоступен','Confirmation':'CONFIRMED','Component':'Ads / economy','Build':BUILD,'Environment':ENV+'; yaSdk=null',
'Preconditions':'Игра запущена без доступного Yandex SDK; экран gameOver; revive или x2 stars доступны.','Steps':'1. Завершить раунд.\n2. Нажать «Смотреть рекламу: +1 жизнь» или «x2 звезды».\n3. Наблюдать отсутствие рекламы и изменение state/balance.',
'Actual':'showRewardedAd вызывает reward() и close() при !yaSdk; revive и звезды выдаются немедленно.','Expected':'Reward должен выдаваться только после SDK callback onRewarded; при unavailable/error — безопасное сообщение и отсутствие награды.','Frequency':'5/5 для обоих paths','Severity':'S2 — Critical','Priority':'P0','Impact':'Обход рекламной монетизации и прогрессии; пользователи получают revive/currency без просмотра.','Workaround':'Нет на клиенте; требуется изменение fallback policy.','Regression':'Unknown','Tests':'TC-ADS-001; TC-ADS-002','Features':'FEAT-ADS-002; FEAT-ADS-003','Evidence':'evidence/BUG-002_step-01_game-over.png; evidence/BUG-002_result_revived-without-ad.png; logs/tests.log','Logs':'DYN-022/DYN-023','Additional':'На реальной платформе риск проявляется при init failure, ad API missing или standalone hosting.','Code':'game.js:501-552, особенно 532-536; game.js:793-857','Cause confidence':'High'},
{
'Bug ID':'BUG-003','Title':'Пылесос почти полностью выходит за видимую область при перемещении к краю экрана','Confirmation':'CONFIRMED','Component':'Gameplay graphics / input bounds','Build':BUILD,'Environment':ENV+'; viewport 1024×768',
'Preconditions':'Активный раунд; изображение пылесоса загружено.','Steps':'1. Переместить указатель к x=0.\n2. Дождаться, пока player приблизится к target x=20.\n3. Оценить видимую часть sprite.',
'Actual':'Центр ограничен x=20, но sprite шириной около 169 px; большая часть пылесоса обрезается за левым краем.','Expected':'Основная визуальная модель игрока должна оставаться видимой; граница должна учитывать sprite/feedback bounds.','Frequency':'5/5 на 1024×768; статически симметрично для других краев','Severity':'S4 — Minor','Priority':'P2','Impact':'Ухудшается ориентация и понятность collision/feedback у границ.','Workaround':'Не двигать указатель вплотную к краю.','Regression':'Unknown','Tests':'TC-UI-002','Features':'FEAT-UI-002; FEAT-GFX-001','Evidence':'evidence/BUG-003_result.png','Logs':'DYN-024','Additional':'Collision radius 36 также заметно меньше визуального sprite — отдельный риск, требующий manual confirmation.','Code':'game.js:878-883; game.js:1594-1623','Cause confidence':'High'},
{
'Bug ID':'BUG-004','Title':'Кнопка «Меню» без подтверждения списывает активированные расходуемые бустеры','Confirmation':'CONFIRMED','Component':'Boosters / navigation / economy','Build':BUILD,'Environment':ENV,
'Preconditions':'В inventory есть magnetStart, shield и/или doubleStart; начат раунд.','Steps':'1. Начать раунд с бустером.\n2. Сразу нажать «Меню».\n3. Проверить inventory и наличие confirmation.','Actual':'Бустеры списываются в startGame/applyStartingBoosters; Menu мгновенно завершает раунд, confirmation/возврата нет.','Expected':'Перед необратимым выходом должно быть подтверждение с ясным предупреждением либо неиспользованные ресурсы возвращаются.','Frequency':'5/5','Severity':'S3 — Major','Priority':'P1','Impact':'Случайное нажатие приводит к потере редких ресурсов/звезд.','Workaround':'Не нажимать Menu после старта; визуального предупреждения нет.','Regression':'Unknown','Tests':'TC-BOOST-002','Features':'FEAT-BOOST-001; FEAT-STATE-001','Evidence':'evidence/BUG-004_step-01_boosters-active.png; evidence/BUG-004_result_menu-no-confirmation.png','Logs':'DYN-020/DYN-021','Additional':'Особенно вероятно на mobile: Menu расположен рядом с sound в HUD.','Code':'game.js:741-746; game.js:1262-1284','Cause confidence':'High'},
]

# ---------- documents ----------
README=f'''# QA-комплект: «Пылесос Пыслей» / Thought Vacuum

**Проверенная версия:** `{BUILD}`  
**Дата:** {DATE}  
**Release verdict:** **NO-GO** — открыты два `S2`, один `S3`, один `S4`; реальная Yandex-среда не проверена.

## С чего начать

1. Прочитать [20_RELEASE_READINESS_REPORT.md](20_RELEASE_READINESS_REPORT.md).
2. Исправить `BUG-002`, затем `BUG-001`, затем `BUG-004`.
3. Выполнить [11_SMOKE_SUITE.md](11_SMOKE_SUITE.md) и Critical Regression из [12_REGRESSION_SUITE.md](12_REGRESSION_SUITE.md).
4. Зафиксировать retest в [19_TEST_EXECUTION_REPORT.md](19_TEST_EXECUTION_REPORT.md).

## Что находится в папке

- Инвентаризация и модель: `00`–`05`.
- Стратегия, риски, план: `06`–`08`.
- Чек-листы и тесты: `09`–`13`, `checklists/`.
- Дефекты и специальные отчеты: `14`–`18`.
- Итоги и процесс релиза: `19`–`25`.
- Интернет-источники: `26_SOURCES.md`.
- Доказательства: `evidence/`; логи: `logs/`; изолированные материалы: `work/`.

## Быстрые маршруты

### У меня 10 минут

Выполнить `TC-SMOKE-001`, `TC-CORE-001`, `TC-CORE-003`, `TC-CORE-007`, `TC-CORE-008`, проверить console. Если изменялись реклама или сохранение, добавить `TC-ADS-001/002` и `TC-SAVE-001/002`.

### Я изменил игровую механику

Выполнить Critical Regression: scoring/combo, good/bad/gold, lives/shield, gameOver/restart; затем charter `EXP-02` и `EXP-05`.

### Я исправил баг

Повторить точные шаги из `14_BUG_REPORTS.md`, сохранить новое доказательство, затем выполнить связанные test cases и соседние функции из Traceability Matrix.

### Я готовлю релиз

Build Verification → Smoke → Critical Regression → Core Regression → natural full-cycle session → реальная Yandex SDK/ad проверка → viewport/mobile → accessibility quick wins → Release Readiness.

## Что фактически проверено

32 browser interaction/static-state checks через Chromium harness: 27 продуктовых проверок `PASS`, 5 `FAIL`; 2 platform cases `BLOCKED`; остальное `NOT_RUN`. Harness использовал неизмененный `game.js`, кроме тестовой подстановки base URL и in-memory localStorage, поскольку политика окружения блокировала прямую навигацию браузера.

## Что не проверено

Реальные Yandex loader/ads, production ZIP, реальные Chrome/Firefox/Safari devices, audible audio quality, FPS/CPU/GPU/memory, 30-minute soak, controller/TV remote, screen reader.
'''
write('README.md',README)

progress='''# Прогресс QA-анализа

## Статус фаз

'''+md_table(['Фаза','Статус','Результат'],[[i,'DONE',x] for i,x in enumerate([
'Безопасная инвентаризация; source hash и структура.','Статические проверки, изолированный запуск, логи.','Product overview, feature matrix, oracles.','Risk strategy/register.','Test plan.','20 подробных checklist-файлов.','83 test cases в MD/CSV.','Smoke/regression suites.','15 exploratory charters.','32 dynamic checks и evidence.','4 confirmed bugs + potential defects.','Accessibility review.','Performance/compatibility matrix.','RU/EN localization review.','Traceability MD/CSV.','Execution report.','NO-GO readiness verdict.','Solo developer workflow.','Known issues/changelog/open questions.','Documentation audit.'
],1)])+f'''

## Итог

- Build ID: `{BUILD}`.
- Source SHA-256 aggregate: `cc6576a5764ade719ac02b3b7a9a1f3f7d5b5111eccc2698ece60cba5a2977f6`.
- Product test status: `PASS 27`, `FAIL 5`, `BLOCKED 2`, `NOT_RUN 49`.
- Confirmed bugs: `S2=2`, `S3=1`, `S4=1`.
- Исходный код не изменялся.

## Ограничения и решения

- В предоставленном root отсутствует каталог `assets`, хотя HTML его ожидает. Для запуска создана копия `QA/work/runtime/assets`; это не исправление проекта.
- Прямая навигация Chromium к localhost/file блокировалась политикой `ERR_BLOCKED_BY_ADMINISTRATOR`; применен `set_content` harness.
- Реальные platform SDK, ads и production packaging не доступны — соответствующие tests `BLOCKED/NOT_RUN`.
- Simulated update-loop не считается FPS/soak.
'''
write('PROGRESS.md',progress)

inventory=f'''# 00 — Инвентаризация проекта

**Дата анализа:** {DATE}  
**Версия:** `{BUILD}`; Git metadata отсутствует.

## Краткое описание

| Параметр | Значение | Статус | Источник |
|---|---|---|---|
| Название | «Пылесос Пыслей» / `Thought Vacuum` | CONFIRMED | `index.html:6`, `game.js:80-177` |
| Жанр | Casual arcade / survival collector, endless round | INFERRED | Основной цикл и отсутствие levels |
| Аудитория | Широкая casual, визуально детская/семейная | INFERRED | Art/UI tone; возрастной рейтинг не указан |
| Основная механика | Перемещать пылесос указателем, собирать good/gold, избегать bad | CONFIRMED | Menu lead; `game.js:895-1044` |
| Условие победы | Фиксированной победы/финального уровня нет | NOT_APPLICABLE | Endless score loop |
| Поражение | Lives ≤ 0 | CONFIRMED | `game.js:1009-1019` |
| Прогресс | Best score, stars, upgrades, boosters, skins, daily | CONFIRMED | `game.js:554-608` |
| Управление | Pointer/mouse/touch; UI keyboard focus частично | CONFIRMED | `game.js:610-625`; DYN-007 |
| Обучение | Только текстовое описание на menu | CONFIRMED | `index.html:19` |
| Levels/scenes | 4 UI screens, уровней нет | CONFIRMED | `screens` object |
| Пауза | Автоматическая system pause, нет пользовательской pause screen | CONFIRMED | `game.js:415-460` |
| Settings | Только mute в игровом HUD | CONFIRMED | `game.js:2028-2047` |
| Save | localStorage | CONFIRMED | key `thoughtVacuumProgress.v1` |
| Audio | Web Audio synthesized cues | CONFIRMED | `game.js:1881-2027` |
| Localization | Russian/English | CONFIRMED | `TRANSLATIONS` |
| Network | Yandex SDK/ads; core game может работать без SDK | CONFIRMED | `index.html:11`; `game.js:444-552` |
| Achievements/accounts/IAP/UGC/mods | Не обнаружены | NOT_APPLICABLE | Source scan |
| Analytics/telemetry | GameplayAPI markers only; analytics SDK не обнаружен | CONFIRMED | `game.js:393-413` |
| Controller/TV remote | Не обнаружено | UNKNOWN/NOT_IMPLEMENTED | Input scan |
| Ads | Interstitial + rewarded | CONFIRMED | `game.js:462-552` |

## Технический стек

- HTML5/CSS/JavaScript ES2020+, Canvas 2D, Web Audio, localStorage.
- Движок: собственная browser loop на `requestAnimationFrame`; сторонний engine отсутствует.
- Build system/package manager: отсутствуют; static files.
- Entry point: `index.html` → `vacuum_player_data.js` → `game.js`.
- Target: Yandex Games web, desktop/mobile inferred from `/sdk.js`, responsive CSS and SDK calls.
- Dependencies: browser APIs и runtime-provided Yandex Games SDK.

## Файлы

'''+md_table(['Файл','Назначение','Статус'],[
['index.html','DOM screens/HUD, SDK/resource links','CONFIRMED'],['style.css','Responsive presentation and touch layout','CONFIRMED'],['game.js','All gameplay/state/economy/audio/integration','CONFIRMED'],['vacuum_player.png','Player art, 423×430 PNG','CONFIRMED'],['vacuum_player_data.js','Embedded data URI fallback/source','CONFIRMED'],['README/package.json/git','Не предоставлены','UNKNOWN']
])+'''

## Пользовательские потоки

1. Launch → daily reward optional → Play → collect/avoid → gameOver → revive/x2/restart/menu.
2. Launch → Upgrades → buy permanent/booster/skin → back → Play.
3. Gameplay → system blur/visibility → automatic pause → resume.

## Неизвестные параметры

- Финальное официальное название и допустима ли форма «Пыслей».
- Реальный Yandex app ID, draft settings, supported device types/orientations.
- Требования к score balance, session length, FPS, memory.
- Intended behavior for offline SDK and for quitting with boosters.
- Release archive structure; supplied upload flattened `assets`.

## Предположения

'''+md_table(['ID','Предположение','Риск'],[
['ASM-001','Yandex Games — основная платформа','High if wrong'],['ASM-002','Endless score loop intentionally has no win','Medium'],['ASM-003','Reward requires actual onRewarded callback','High'],['ASM-004','Player should remain mostly visible at edges','Low/UX'],['ASM-005','One developer maintains all QA docs','Confirmed by task']
])
write('00_PROJECT_INVENTORY.md',inventory)

# Environment
import platform, subprocess
mem='4.0 GiB available container limit (observed); no swap'
envdoc=f'''# 01 — Тестовое окружение

| Поле | Значение |
|---|---|
| Дата/время | {DATE}; command logs use UTC |
| Build | `{BUILD}` |
| OS | Debian GNU/Linux 13 (trixie), Linux x86_64 |
| CPU | 56 logical CPUs exposed to container; host model not used as performance claim |
| Memory | {mem} |
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
'''
write('01_TEST_ENVIRONMENT.md',envdoc)

bvr=f'''# 02 — Build Verification Report

**Build:** `{BUILD}`  
**Результат:** `CONDITIONAL PASS` для статической/browser-logic проверки; production package/platform launch не подтвержден.

## Выполнено

'''+md_table(['Проверка','Результат','Доказательство'],[
['`node --check game.js`','PASS','logs/build.log'],['`node --check vacuum_player_data.js`','PASS','logs/build.log'],['HTML parse, 36 unique IDs','PASS','logs/build.log'],['31 JS DOM IDs найдены в HTML','PASS','logs/build.log'],['CSS brace balance 113/113','PASS','logs/build.log'],['Изолированный Chromium launch','PASS','DYN-001/002'],['Production-like direct navigation','BLOCKED','ERR_BLOCKED_BY_ADMINISTRATOR'],['Yandex SDK init/moderation loader','BLOCKED','Runtime unavailable'],['Source root asset paths','WARNING','`assets/*` отсутствуют в supplied root']
])+'''

## Команды и длительность

Точные команды находятся в `logs/build.log` и `logs/tests.log`. Длительность не используется как product performance metric: harness и административные ограничения делают ее нерепрезентативной.

## Блокирующие/предрелизные действия

1. Собрать реальный ZIP со структурой `index.html`, `style.css`, `game.js`, `assets/vacuum_player.png`, `assets/vacuum_player_data.js`.
2. Открыть через официальный Yandex local server/draft debug panel.
3. Проверить loader `IT`, LoadingAPI, GameplayAPI, real ads.
4. Устранить BUG-001/002 до release candidate.
'''
write('02_BUILD_VERIFICATION_REPORT.md',bvr)

product=f'''# 03 — Product Overview

## Назначение и идея

Короткая endless arcade-сессия: игрок управляет милым пылесосом, собирает хорошие и золотые мысли, избегает вредных. За score начисляются stars; они расходуются на upgrades, boosters и cosmetic skins.

## Основной цикл

`Menu → optional daily/store → Start → Move → Collect/Avoid → Score/Combo/Bonus → Lose lives → GameOver → Reward/Revive/Restart/Menu`.

## Сущности и правила

'''+md_table(['Сущность','Правило'],[
['Player vacuum','Target follows pointer; collision radius 36; suction radius 86 + 13×radius level'],['Good thought','10×combo×double points; streak +1; every 5 → combo up to 5'],['Bad thought','Shield consumed or lives −1; combo/streak reset'],['Gold thought','50×combo×double; random magnet/slow/double'],['Stars','floor(score/100) incremental award; spend in store'],['Lives','3 + 1 if life upgrade'],['Boosters','Consumed at round start'],['Daily','Local-date reward and 3 deterministic daily tasks']
])+'''

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
'''
write('03_PRODUCT_OVERVIEW.md',product)

feature_rows=[]
for f in features:
    feature_rows.append([f[0],f[1],f[2],f[3],f[4],f[5],f[6],f[7],f[8],f[9]])
write('04_FEATURE_MATRIX.md','# 04 — Feature Matrix\n\n'+md_table(['Feature ID','Название','Описание','Источник','Статус','Критичность','Зависимости','Тесты','Checklist','Факт'],feature_rows)+'''\n\n`PARTIAL` означает, что часть behavior проверена, но реальная платформа/device/manual feel остались непроверенными.\n''')

oracles='# 05 — Requirements and Oracles\n\n## Иерархия оракулов\n\n1. Явные UI-тексты и source behavior.\n2. Внутренняя согласованность правил.\n3. Публичные Yandex requirements/SDK contracts.\n4. Accessibility guidance.\n5. Общепринятое ожидание игрока — помечено INFERRED.\n\n'+md_table(['Requirement ID','Ожидаемое поведение','Oracle/source','Статус','Features'],requirements)+'''\n\n## Требуют подтверждения разработчиком\n\n- Должен ли upgrade bonus duration влиять на стартовые boosters.\n- Является ли мгновенный выход с потерей boosters намеренным.\n- Допустима ли выдача rewarded rewards в standalone debug mode; для production это считается defect.\n- Требуется ли полностью видимый sprite у границ или допускается clipping.\n- Желаемые score/session/FPS targets.\n'''
write('05_REQUIREMENTS_AND_ORACLES.md',oracles)

strategy=f'''# 06 — Test Strategy

## Цели

Проверить критический игровой путь, целостность прогрессии/экономики, устойчивость сохранения, input/state transitions и готовность Yandex integration. Стратегия оптимизирована для одного разработчика: сначала тесты с максимальным риском и короткой обратной связью.

## Scope

Входит: static web files, gameplay, UI, local save, daily/store, ads integration branches, audio state, RU/EN, responsive layout.  
Не входит без окружения: moderation, real ad inventory, payment/account/leaderboard, device lab, full accessibility certification.

## Подход

- Risk-based order: startup/save/ads/core → input/state → economy/daily → UI/localization → performance/accessibility.
- Techniques: equivalence, boundaries, decision tables, state transitions, user journeys, error guessing, exploratory charters, limited pairwise viewports.
- Retest: exact bug steps on clean and affected save, then adjacent feature tests.
- Regression tiers: Critical/Core/Extended/Full.

## Entry criteria

Source identified; build/hash recorded; launch method known; test data backup possible.

## Suspension criteria

Startup crash for clean profile, non-deterministic data loss, environment changes that invalidate evidence, or >1 open S1.

## Exit criteria

- Smoke and critical path pass.
- No open S1/S2 without explicit accepted risk.
- Save corruption and rewarded branches tested.
- Real Yandex loader/ads checked for release.
- Known issues and verdict updated.

## Evidence rules

Screenshot/log must reference build and test/bug ID. Do not overwrite evidence of previous build; add suffix/date. Secrets and personal data must be removed.

## При нехватке времени

1. Startup + save corruption.
2. Natural core loop/gameOver/restart.
3. Reward integrity and ad recovery.
4. Booster/economy persistence.
5. Mobile viewport/touch.
6. Remaining UI/accessibility/performance.
'''
write('06_TEST_STRATEGY.md',strategy)

risk_rows=[[r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12]] for r in risks]
write('07_RISK_REGISTER.md','# 07 — Risk Register\n\nШкала: probability `Low/Medium/High`; impact `Low/Medium/High/Critical`; итог — качественная оценка без псевдоточной арифметики.\n\n'+md_table(['Risk ID','Компонент','Риск','Причина','Последствие','Вероятность','Влияние','Уровень','Обнаруживаемость','Features','Tests','Действие','Статус'],risk_rows))

plan=f'''# 08 — Test Plan

| Поле | Значение |
|---|---|
| Document ID | TP-TV-001 |
| Version | 1.0 |
| Date | {DATE} |
| Build | `{BUILD}` |
| Owner | Solo developer / QA self-check |

## Цели и объекты

Проверить static package, browser runtime, core loop, state/save/economy/ads, UI/input/audio/localization, platform readiness.

## Порядок

1. Build Verification.
2. Smoke.
3. Critical path.
4. Functional and negative.
5. Exploratory.
6. Save/state.
7. UI/UX and accessibility.
8. Performance/compatibility.
9. Regression.
10. Release Candidate on Yandex draft.

## Test data

Clean profile; valid profile with stars/store; invalid JSON; structurally invalid JSON; score boundaries; all boosters; RU/EN; viewport matrix.

## Severity/Priority

Используются S1–S4 и P0–P3 из Bug Reports. Priority учитывает reach, release stage, monetization, workaround and regression risk.

## Entry/exit/stop/resume

Совпадают с Strategy. Для release обязательны real platform tests `TC-PLAT-001..004` и `TC-ADS-003..006`.

## Reporting

Test cases CSV is source of status counts; defects only if runtime-confirmed. Potential defects stay separate. Evidence links are relative to QA root.

## Open questions

See `24_OPEN_QUESTIONS.md`.
'''
write('08_TEST_PLAN.md',plan)

# Test cases CSV and MD
headers=list(cases[0].keys())
with (QA/'10_TEST_CASES.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(cases)
status_counts={s:sum(c['Status']==s for c in cases) for s in ['PASS','FAIL','BLOCKED','NOT_RUN','NOT_APPLICABLE']}
summary_rows=[[s,n] for s,n in status_counts.items()]
md=['# 10 — Test Cases','',f'Build: `{BUILD}`. Источник статусов: фактические checks и ограничения окружения.','',md_table(['Status','Count'],summary_rows),'']
for c in cases:
    md += [f"## {c['Test Case ID']} — {c['Title']}", '', md_table(['Field','Value'],[[k,c[k]] for k in headers]),'']
write('10_TEST_CASES.md','\n'.join(md))

# Checklists
check_specs={
'CHK-01_Installation_And_First_Launch.md':('CHK-01','Installation and first launch',[
('Чистый запуск из release package','TC-SMOKE-001','PASS'),('Повторный запуск с сохранением','TC-DAILY-001','PASS'),('Запуск после crash','TC-SAVE-004','NOT_RUN'),('Невалидный JSON','TC-SAVE-001','PASS'),('Структурно поврежденный save','TC-SAVE-002','FAIL'),('Отсутствующие asset files','TC-GFX-001','NOT_RUN'),('SDK loader IT','TC-PLAT-001','BLOCKED'),('Корректное закрытие/повторное открытие','TC-SAVE-004','NOT_RUN'),('Создание storage entry','TC-DAILY-001','PASS'),('Ошибки в console','TC-SMOKE-002','PASS')]),
'CHK-02_Main_Menu_And_Navigation.md':('CHK-02','Main menu and navigation',[
('Menu visible','TC-SMOKE-001','PASS'),('Play transition','TC-CORE-001','PASS'),('Upgrades/back','TC-UI-001','PASS'),('Keyboard focus','TC-ACC-001','PASS'),('Rapid clicks','TC-UI-004','NOT_RUN'),('Double click daily','TC-DAILY-001','PASS'),('Impossible transitions','TC-STATE-003','NOT_RUN'),('Menu during round confirmation','TC-BOOST-002','FAIL'),('GameOver menu','TC-CORE-012','NOT_RUN'),('Back/browser gestures suppressed','TC-COMP-008','NOT_RUN')]),
'CHK-03_Core_Gameplay.md':('CHK-03','Core gameplay',[
('Start state','TC-CORE-001','PASS'),('Good scoring','TC-CORE-002','PASS'),('Bad damage','TC-CORE-003','PASS'),('Shield','TC-CORE-004','PASS'),('Gold bonus','TC-CORE-005','PASS'),('Double×combo','TC-CORE-006','PASS'),('Spawn types','TC-CORE-009','NOT_RUN'),('Suction/repulsion','TC-CORE-011','NOT_RUN'),('Natural full loop','TC-CORE-012','NOT_RUN'),('Soft-lock attempt','EXP-15','NOT_RUN')]),
'CHK-04_Controls_And_Input.md':('CHK-04','Controls and input',[
('Pointer boundaries','TC-INPUT-001','PASS'),('Real mouse feel','TC-INPUT-002','NOT_RUN'),('Touch drag','TC-INPUT-002','NOT_RUN'),('Multi-touch','TC-INPUT-003','NOT_RUN'),('Keyboard gameplay','TC-INPUT-004','NOT_RUN'),('Rapid input','EXP-03','NOT_RUN'),('Conflicting input','TC-INPUT-003','NOT_RUN'),('Input during pause','TC-STATE-002','NOT_RUN'),('Input on result','TC-ADS-005','BLOCKED'),('Controller disconnect','N/A','NOT_APPLICABLE')]),
'CHK-05_UI_And_HUD.md':('CHK-05','UI and HUD',[
('Score/lives/combo initial','TC-CORE-001','PASS'),('HUD updates','TC-CORE-002','PASS'),('Bonus pill','TC-CORE-005','PASS'),('Small viewports','TC-COMP-001..002','PASS'),('Tablet/desktop','TC-COMP-003..005','PASS'),('Touch scroll','TC-COMP-006','PASS'),('Player fully visible','TC-UI-002','FAIL'),('Large counter values','TC-PROG-002','NOT_RUN'),('Disabled controls','TC-UPG-003','NOT_RUN'),('Focus visibility','TC-ACC-001','PARTIAL')]),
'CHK-06_Game_States.md':('CHK-06','Game states',[
('menu→game','TC-CORE-001','PASS'),('game→gameOver','TC-CORE-007','PASS'),('gameOver→game','TC-CORE-008','PASS'),('menu↔upgrades','TC-UI-001','PASS'),('System pause API','TC-STATE-001','PASS'),('Real Alt+Tab','TC-STATE-002','NOT_RUN'),('Ad open/close','TC-ADS-005','BLOCKED'),('Menu during game','TC-BOOST-002','FAIL'),('Visibility event order','TC-STATE-002','NOT_RUN'),('Repeated restart','EXP-08','NOT_RUN')]),
'CHK-07_Levels_And_Progression.md':('CHK-07','Progression/economy',[
('No levels','N/A','NOT_APPLICABLE'),('Best score','TC-CORE-007','PASS'),('Score→stars boundaries','TC-PROG-001','NOT_RUN'),('Daily reward','TC-DAILY-001','PASS'),('Daily tasks','TC-DAILY-003..006','NOT_RUN'),('Permanent upgrades','TC-UPG-001..004','NOT_RUN'),('Booster activation','TC-BOOST-001','PASS'),('Booster exit loss','TC-BOOST-002','FAIL'),('Skins','TC-SKIN-001..003','NOT_RUN'),('Economy negative/large values','TC-PROG-002','NOT_RUN')]),
'CHK-08_Win_Lose_And_Restart.md':('CHK-08','Win/lose/restart',[
('Win condition absent','N/A','NOT_APPLICABLE'),('Lose at 0 lives','TC-CORE-007','PASS'),('Restart clean','TC-CORE-008','PASS'),('Revive one time','TC-ADS-005','BLOCKED'),('Revive fallback integrity','TC-ADS-001','FAIL'),('Double stars integrity','TC-ADS-002','FAIL'),('Second death after revive','TC-ADS-005','NOT_RUN'),('Interstitial threshold','TC-ADS-003','BLOCKED'),('Menu from results','TC-CORE-012','NOT_RUN'),('Rapid result buttons','TC-ADS-006','NOT_RUN')]),
'CHK-09_Save_Load_And_Persistence.md':('CHK-09','Save/load/persistence',[
('First save','TC-DAILY-001','PASS'),('Reload valid state','TC-DAILY-001','PASS'),('Invalid JSON','TC-SAVE-001','PASS'),('Nested corruption','TC-SAVE-002','FAIL'),('Write failure','TC-SAVE-003','NOT_RUN'),('Sequential saves','TC-SAVE-004','NOT_RUN'),('Settings persistence','TC-AUDIO-001','PASS'),('Store persistence','TC-SKIN-001','NOT_RUN'),('Close during save','TC-SAVE-004','NOT_RUN'),('Cross-device/cloud','N/A','NOT_APPLICABLE')]),
'CHK-10_Settings.md':('CHK-10','Settings',[
('Sound default','TC-AUDIO-001','PASS'),('Mute/unmute','TC-AUDIO-001','PASS'),('Mute persistence','TC-AUDIO-001','PASS'),('Rapid toggle','TC-AUDIO-004','NOT_RUN'),('Resolution setting','N/A','NOT_APPLICABLE'),('Fullscreen setting','N/A','NOT_APPLICABLE'),('Sensitivity','N/A','NOT_APPLICABLE'),('Rebind','N/A','NOT_APPLICABLE'),('Language menu','N/A','NOT_APPLICABLE'),('Reset settings','N/A','NOT_APPLICABLE')]),
'CHK-11_Audio.md':('CHK-11','Audio',[
('Sound toggle state','TC-AUDIO-001','PASS'),('Good cue','TC-AUDIO-003','NOT_RUN'),('Bad cue','TC-AUDIO-003','NOT_RUN'),('Gold/combo/buy/over cues','TC-AUDIO-003','NOT_RUN'),('Vacuum startup','TC-AUDIO-003','NOT_RUN'),('Mute all sounds','TC-AUDIO-001','PARTIAL'),('Audio in pause','TC-AUDIO-002','NOT_RUN'),('Audio after Alt+Tab','TC-AUDIO-002','NOT_RUN'),('No overlap/stuck loop','TC-AUDIO-004','NOT_RUN'),('Volume control','N/A','NOT_APPLICABLE')]),
'CHK-12_Graphics_And_Animation.md':('CHK-12','Graphics and animation',[
('Player bitmap','TC-SMOKE-001','PASS'),('Image fallback','TC-GFX-001','NOT_RUN'),('Thought emojis','TC-CORE-009','NOT_RUN'),('Particles','TC-CORE-005','PARTIAL'),('Edge clipping','TC-UI-002','FAIL'),('Skin visuals','TC-SKIN-003','NOT_RUN'),('Aspect ratios','TC-COMP-001..005','PASS'),('Camera shake','TC-ACC-004','NOT_RUN'),('Animation transitions','TC-UI-001','PARTIAL'),('Missing texture warning','TC-GFX-001','NOT_RUN')]),
'CHK-13_Physics_And_Collisions.md':('CHK-13','Physics/collisions',[
('Good collision','TC-CORE-002','PASS'),('Bad collision','TC-CORE-003','PASS'),('Gold collision','TC-CORE-005','PASS'),('Shield decision','TC-CORE-004','PASS'),('Suction radius boundary','TC-CORE-011','NOT_RUN'),('Magnet bad repulsion','TC-CORE-011','NOT_RUN'),('Visual hitbox match','TC-CORE-013','NOT_RUN'),('Out-of-bounds thought removal','TC-CORE-010','NOT_RUN'),('High-speed tunneling','EXP-03','NOT_RUN'),('Player boundary clipping','TC-UI-002','FAIL')]),
'CHK-14_Performance_And_Stability.md':('CHK-14','Performance/stability',[
('JS syntax','TC-SMOKE-002','PASS'),('Simulated update stress','TC-PERF-001','PASS'),('Real 30-min soak','TC-PERF-002','NOT_RUN'),('FPS/frame time','TC-PERF-003','NOT_RUN'),('Memory growth','TC-PERF-002','NOT_RUN'),('Repeated restart','EXP-08','NOT_RUN'),('Mass particles','TC-PERF-003','NOT_RUN'),('Resize stress','TC-COMP-008','NOT_RUN'),('Audio object lifecycle','TC-AUDIO-004','NOT_RUN'),('Crash logs','TC-SAVE-002','FAIL')]),
'CHK-15_Compatibility.md':('CHK-15','Compatibility',[
('320×568','TC-COMP-001','PASS'),('360×640','TC-COMP-002','PASS'),('768×1024','TC-COMP-003','PASS'),('1366×768','TC-COMP-004','PASS'),('1920×1080','TC-COMP-005','PASS'),('Touch scroll','TC-COMP-006','PASS'),('Chrome physical','TC-COMP-007','NOT_RUN'),('Firefox/Safari','TC-COMP-007','NOT_RUN'),('Orientation change','TC-COMP-008','NOT_RUN'),('OS scaling/controller/TV','N/A','NOT_RUN')]),
'CHK-16_Accessibility.md':('CHK-16','Accessibility',[
('Keyboard reaches menu','TC-ACC-001','PASS'),('Gameplay keyboard alternative','TC-ACC-003','NOT_RUN'),('Contrast','TC-ACC-002','NOT_RUN'),('Target sizes ≥24px','Static CSS','PASS'),('Color-only info','Review','PARTIAL'),('Mute control','TC-AUDIO-001','PASS'),('Reduced motion/shake','TC-ACC-004','NOT_RUN'),('Screen reader state','TC-ACC-005','NOT_RUN'),('Focus visibility','TC-ACC-001','PARTIAL'),('Irreversible action confirmation','TC-BOOST-002','FAIL')]),
'CHK-17_Localization.md':('CHK-17','Localization',[
('RU auto','TC-LOC-002','PASS'),('EN auto','TC-LOC-001','PASS'),('Language mapping','TC-LOC-002','PASS'),('Full RU audit','TC-LOC-003','NOT_RUN'),('Full EN audit','TC-LOC-004','NOT_RUN'),('Long strings','TC-LOC-005','NOT_RUN'),('Variables/plurals','TC-LOC-003','NOT_RUN'),('Dates/numbers','TC-DAILY-006','NOT_RUN'),('Text on images','N/A','NOT_APPLICABLE'),('Title spelling','Open question','UNKNOWN')]),
'CHK-18_Negative_And_Recovery.md':('CHK-18','Negative/recovery',[
('Invalid JSON recovery','TC-SAVE-001','PASS'),('Nested corrupt recovery','TC-SAVE-002','FAIL'),('Storage write failure','TC-SAVE-003','NOT_RUN'),('No SDK rewarded','TC-ADS-001..002','FAIL'),('Ad onError recovery','TC-ADS-004..006','BLOCKED'),('Missing image fallback','TC-GFX-001','NOT_RUN'),('Rapid UI input','EXP-03','NOT_RUN'),('Wrong action order','EXP-04','NOT_RUN'),('Focus loss','TC-STATE-002','NOT_RUN'),('No network','TC-PLAT-004','NOT_RUN')]),
'CHK-19_Long_Session.md':('CHK-19','Long session',[
('100s simulated update','TC-PERF-001','PASS'),('30-min natural session','TC-PERF-002','NOT_RUN'),('Memory samples','TC-PERF-002','NOT_RUN'),('FPS samples','TC-PERF-003','NOT_RUN'),('Long score/counter','TC-PROG-002','NOT_RUN'),('Spawn pace minimum','TC-CORE-010','NOT_RUN'),('Daily rollover','TC-DAILY-006','NOT_RUN'),('Repeated ads','TC-ADS-003..006','BLOCKED'),('Repeated restarts','EXP-08','NOT_RUN'),('Audio stability','TC-AUDIO-004','NOT_RUN')]),
'CHK-20_Release_Candidate.md':('CHK-20','Release candidate',[
('Release ZIP assets','TC-BUILD-001','NOT_RUN'),('Clean launch','TC-SMOKE-001','PASS'),('No S1/S2','Bug register','FAIL'),('Smoke','11_SMOKE_SUITE','PARTIAL'),('Critical path natural','TC-CORE-012','NOT_RUN'),('Save corruption','TC-SAVE-002','FAIL'),('Yandex loader IT','TC-PLAT-001','BLOCKED'),('Real ads','TC-ADS-003..006','BLOCKED'),('Mobile/desktop matrix','TC-COMP-001..006','PARTIAL'),('Known issues/verdict updated','Docs','PASS')]),
}

check_summary=[]
for filename,(cid,title,items) in check_specs.items():
    rows=[]
    for idx,(check,ref,status) in enumerate(items,1):
        priority='Critical' if status in ('FAIL','BLOCKED') or idx<=2 else 'High' if idx<=5 else 'Medium'
        expected={
            'FAIL':'Функция соответствует requirement; defect отсутствует.',
            'BLOCKED':'Проверка выполняется в требуемом platform environment.',
            'NOT_APPLICABLE':'Система отсутствует или неприменима.',
        }.get(status,'Наблюдаемое поведение соответствует описанию проверки.')
        comment='See related test/report.' if status!='NOT_RUN' else 'Not executed.'
        bug='BUG-001' if ref=='TC-SAVE-002' else 'BUG-002' if 'TC-ADS-001' in ref or 'TC-ADS-002' in ref else 'BUG-003' if ref=='TC-UI-002' else 'BUG-004' if ref=='TC-BOOST-002' else ''
        rows.append([f'{cid}-{idx:03}',check,'Состояние/экран готов для проверки.',expected,priority,'Manual/functional',status,comment,bug,ref])
    body=f'# {cid} — {title}\n\nBuild: `{BUILD}`.\n\n'+md_table(['Check ID','Проверка','Предусловие','Ожидаемый результат','Priority','Type','Status','Комментарий','Bug','Evidence/Test'],rows)
    write('checklists/'+filename,body)
    counts={s:sum(i[2]==s for i in items) for s in ['PASS','FAIL','BLOCKED','NOT_RUN','NOT_APPLICABLE','PARTIAL','UNKNOWN']}
    check_summary.append([cid,title,filename,', '.join(f'{k}:{v}' for k,v in counts.items() if v)])
write('09_MASTER_CHECKLIST.md','# 09 — Master Checklist\n\n'+md_table(['ID','Область','Файл','Статусы'],check_summary)+'''\n\nПри обновлении build сначала сбросить фактические статусы в `NOT_RUN`, затем выполнять checklist и связывать failures с Bug ID.\n''')

smoke=f'''# 11 — Smoke Suite

## Цель

За минимальное число шагов определить, пригодна ли сборка для дальнейшего тестирования.

'''+md_table(['Порядок','Test','Текущий статус','Критерий'],[
['1','TC-BUILD-001','NOT_RUN','Release package resources resolve'],['2','TC-SMOKE-001','PASS','Menu launches'],['3','TC-CORE-001','PASS','Round starts'],['4','TC-INPUT-002','NOT_RUN','Real input controllable'],['5','TC-CORE-002/003','PASS','Good/bad core reactions'],['6','TC-CORE-007','PASS','GameOver works'],['7','TC-CORE-008','PASS','Restart works'],['8','TC-STATE-002','NOT_RUN','Real pause/background'],['9','TC-SAVE-002','FAIL','Corrupt save does not block'],['10','TC-PLAT-001','BLOCKED','Yandex SDK loader IT']
])+'''

**Smoke verdict:** FAIL/INCOMPLETE. BUG-001 fails resilience; real input/platform cases remain.
'''
write('11_SMOKE_SUITE.md',smoke)

reg=f'''# 12 — Regression Suite

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

'''+md_table(['Изменение','Минимум'],[
['UI/CSS','UI-001/002, COMP-001..006, LOC-003..005, ACC-001/002'],['Input','INPUT-001..004, STATE-002, CORE-012'],['Gameplay/scoring','CORE-001..013, PROG-001'],['Save/schema','SAVE-001..004, DAILY/STORE persistence'],['Ads/SDK','ADS-001..006, PLAT-001..004, STATE/AUDIO'],['Assets/render','GFX-001, UI-002, COMP-007/008, PERF-003']
])
write('12_REGRESSION_SUITE.md',reg)

charters=[]
charter_titles=[
('EXP-01','Первый запуск новым игроком','Launch/menu/onboarding','startup, comprehension'),('EXP-02','Полный основной цикл','Natural play to gameOver/restart','soft lock, scoring'),('EXP-03','Быстрый и хаотичный ввод','Pointer/touch/buttons','double action, race'),('EXP-04','Нарушение порядка действий','Unexpected screen/action order','state corruption'),('EXP-05','Границы игрового пространства','All edges/corners','clipping/collision'),('EXP-06','Переходы состояний','menu/upgrades/game/gameOver','invalid transition'),('EXP-07','Пауза, Alt+Tab и возврат','Visibility/blur/audio','background damage/audio'),('EXP-08','Многократный restart','50 cycles','leak/state carryover'),('EXP-09','Длительная сессия','30+ minutes','memory/FPS/counters'),('EXP-10','Минимальные и максимальные значения','0/max stars/upgrades/boosters','boundaries'),('EXP-11','Сохранение и восстановление','valid/corrupt/quota','data loss'),('EXP-12','Слабая обратная связь','Collisions/bonuses/errors','confusion'),('EXP-13','Доступность интерфейса','Keyboard/contrast/motion','exclusion'),('EXP-14','Тяжелая сцена','High spawn/particles/emoji','long frames'),('EXP-15','Мягкая блокировка','Interruptions/ads/focus','cannot progress')]
for cid,title,area,risk in charter_titles:
    charters.append(f'''## {cid} — {title}

- **Цель:** исследовать {area}.
- **Риски:** {risk}.
- **Идеи:** too fast/slow/many/few/zero/max; repeat/cancel/interrupt; focus loss; missing resource; corrupt data; simultaneous actions.
- **Timebox:** 20–40 минут в зависимости от scope; фиксировать фактическое время.
- **Data:** clean и affected profiles, mobile/desktop где применимо.
- **Наблюдения:** NOT_RUN, кроме частичных evidence из dynamic checks.
- **Найденные проблемы:** связать только после повторного воспроизведения.
- **Вопросы/вывод:** заполнить после session.
''')
write('13_EXPLORATORY_TEST_CHARTERS.md','# 13 — Exploratory Test Charters\n\n'+'\n'.join(charters))

# bugs CSV/MD
bug_headers=list(bugs[0].keys())
with (QA/'14_BUG_REPORTS.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=bug_headers); w.writeheader(); w.writerows(bugs)
bmd=['# 14 — Bug Reports','',f'Build: `{BUILD}`. Подтверждены только воспроизведенные проблемы.','']
for b in bugs:
    bmd += [f"## {b['Bug ID']} — {b['Title']}",'',md_table(['Field','Value'],[[k,b[k]] for k in bug_headers]),'']
bmd += ['## Potential Defects Requiring Runtime Confirmation','',md_table(['ID','Наблюдение','Почему не confirmed','Связанный test'],[
['POT-001','Bonus duration upgrade применяется к random bonus, но start boosters имеют fixed 6/8 seconds.','Design intent неизвестен.','TC-UPG-004'],['POT-002','Daily reward зависит только от local clock.','Нужно подтвердить anti-cheat requirement.','TC-DAILY-002'],['POT-003','Collision radius 36 значительно меньше bitmap footprint.','Нужно natural visual collision test.','TC-CORE-013'],['POT-004','Supplied root не содержит assets/; возможно flattening upload, а не package defect.','Нет release ZIP.','TC-BUILD-001']
])]
write('14_BUG_REPORTS.md','\n'.join(bmd))

acc=f'''# 15 — Accessibility Report

Это техническая оценка, не заявление о полной доступности для какой-либо группы.

'''+md_table(['Область','Применимость','Результат','Доказательство','Влияние','Рекомендация','Effort','Priority'],[
['Text size/reflow','Да','PARTIAL: responsive, readable screenshots; no zoom audit','CSS clamp/media; viewport evidence','Medium','Test browser zoom 200%, expose text scale if needed','Medium','P2'],
['Contrast','Да','RISK: white on #ff6f91=2.65:1, #ff9671=2.13:1, #1fbfa3=2.32:1','Static WCAG contrast calculation','High for low vision','Use darker fills or dark text; target 4.5:1 regular/3:1 large as heuristic','Low','P1'],
['Target size','Да','PASS static: buttons min-height 40–54px','style.css','Low','Keep ≥24px and spacing','Low','Maintain'],
['Color dependency','Да','PARTIAL: thought type uses different emoji plus colors; bonuses have text','Source/screenshots','Medium','Test color blindness; add shape/audio consistency','Medium','P2'],
['Audio control','Да','PASS partial: mute and persistence','TC-AUDIO-001','Medium','Move mute also to menu/settings; volume slider','Low/Medium','P2'],
['Visual alternative to audio','Да','PARTIAL: score/particles/shake exist','Source','Medium','Ensure every cue has textual/visual feedback','Medium','P2'],
['Keyboard/remap','Да','FAIL/GAP: UI tabbable, gameplay pointer-only','TC-ACC-001; source','High','Add WASD/arrows and optional sensitivity/rebind','Medium','P1'],
['One-hand/simple input','Да','Pointer movement is simple, but continuous precision required','Mechanic','Medium','Add keyboard/drag mode, larger safe area','Medium','P2'],
['Timers/difficulty','Да','No difficulty/pause control; spawn accelerates','Source','High for motor/cognitive','Add pause and optional relaxed mode','High','P2'],
['Shake/reduced motion','Да','No toggle; hit shake hard-coded','game.js:1422-1426','Medium','Reduced motion toggle; disable shake/particles','Low','P1/P2'],
['Flashing/photosensitivity','Да','No deliberate flashing detected; not instrumentally measured','Static/render review','Medium','Review gold/particle frequency in real play','Low','P2'],
['Focus visibility','Да','Keyboard reaches controls; visual focus not fully audited','TC-ACC-001','Medium','Explicit :focus-visible style','Low','P1'],
['Screen reader','Да','Canvas only aria-label; live score/game state absent','index.html/game.js','High','ARIA live summary, semantic controls, alternative mode','High','P2'],
['Irreversible actions','Да','FAIL: Menu loses boosters without confirmation','BUG-004','High','Confirmation with resource warning','Low','P1'],
['Subtitles/speech/haptics','Нет/не обнаружено','NOT_APPLICABLE','No speech/haptics','Low','Reassess if added','N/A','N/A']
])+'''

## Быстрые улучшения с высокой пользой

1. Darken primary/store button backgrounds or use dark text.
2. Add explicit `:focus-visible` outline.
3. Add confirm dialog for Menu with active consumables.
4. Add reduced-motion toggle and mute in main menu.
5. Document controls on first launch.

## Не проверено

Screen reader, OS high contrast, 200% zoom, physical motor/vision user testing, real mobile accessibility services.
'''
write('15_ACCESSIBILITY_REPORT.md',acc)

perf=f'''# 16 — Performance and Compatibility

## Фактические данные

- `TC-PERF-001`: 3000 `updateGame(0.033)` iterations, ~99.9 seconds simulated game time, spawn disabled to isolate state loop; no exception/NaN. **Не FPS/soak.**
- Responsive DOM and scroll checked at 5 viewports; touch swipe 360×640 changed panel scrollTop 0→451.
- No CPU/GPU/FPS/frame-time/memory claims were made.

## Compatibility matrix

'''+md_table(['Конфигурация','Статус','Evidence/next step'],[
['Chromium 144 headless, 1024×768','PARTIAL PASS','Core harness checks'],['320×568 touch-like','PARTIAL PASS','EV-VP-320x568; touch separately 360×640'],['360×640 mobile touch emulation','PASS for panel scroll','EV-008'],['768×1024','PARTIAL PASS','Layout only'],['1366×768','PARTIAL PASS','Layout only'],['1920×1080','PARTIAL PASS','Layout only'],['Chrome physical desktop/mobile','NOT_TESTED','Run smoke/natural play'],['Firefox latest','NOT_TESTED','Cross-browser'],['Safari/iOS','NOT_TESTED','Web Audio/touch/emoji'],['Fullscreen/orientation/OS scaling','NOT_TESTED','TC-COMP-008'],['Controller/TV remote','NOT_TESTED/N/A until target confirmed','Input implementation absent']
])+'''

## Рекомендуемые, не нормативные пороги

- Interactive menu without visible stall after assets loaded.
- Stable 60 FPS target on mainstream devices; investigate sustained <30 FPS or input lag.
- No monotonic memory growth across 30-minute session/restart cycles.
- No single-frame stalls noticeable during particle bursts/ads close.

Пороги должны быть приняты разработчиком и измерены на real devices.
'''
write('16_PERFORMANCE_AND_COMPATIBILITY.md',perf)

loc=f'''# 17 — Localization Report

## Languages

RU and EN tables exist. `ru/be/kk/uk/uz` map to Russian; all other primary language codes map to English. SDK language can override navigator after init.

## Выполнено

- English main menu/title/lang: PASS.
- Russian main menu and mapping function: PASS.
- Dynamic store/task strings use `titleEn/textEn`: static CONFIRMED.

## Не выполнено

Complete every-screen linguistic audit, pseudo-localization, long string overflow, date/number locale semantics, native speaker review.

## Терминологический словарь

'''+md_table(['RU','EN','Комментарий'],[
['Пылесос Пыслей','Thought Vacuum','Название требует подтверждения spelling/pun'],['Хорошая мысль','Good thought','Collectible'],['Вредная мысль','Bad/harmful thought','Damage'],['Золотая мысль','Golden thought','Bonus collectible'],['Очки','Score','Round score'],['Жизни','Lives','Hearts'],['Комбо','Combo','Multiplier'],['Звезды','Stars','Currency'],['Улучшения','Upgrades','Permanent'],['Бустеры','Boosters','Consumable'],['Щит','Shield','One bad thought block'],['Умный магнит','Smart magnet','Attract good/gold, repel bad'],['Замедление','Slow','Temporary effect']
])+'''

## Риски

Title spelling, translated language mapping for Belarusian/Kazakh/Ukrainian/Uzbek, English text length in store, seconds suffix `s` not localized to Russian convention.
'''
write('17_LOCALIZATION_REPORT.md',loc)

# traceability
req_by_feat={}
for rid,desc,src,st,flist in requirements:
    for f in [x.strip() for x in flist.split(';')]: req_by_feat.setdefault(f,[]).append(rid)
risk_by_feat={}
for r in risks:
    for f in [x.strip() for x in r[9].replace('..003','').split(';')]:
        if f.startswith('FEAT-'): risk_by_feat.setdefault(f,[]).append(r[0])
test_by_feat={}
for c in cases: test_by_feat.setdefault(c['Feature ID'],[]).append(c['Test Case ID'])
bug_by_feat={}
for b in bugs:
    for f in [x.strip() for x in b['Features'].split(';')]: bug_by_feat.setdefault(f,[]).append(b['Bug ID'])
trace=[]
for f in features:
    fid=f[0]
    tests=test_by_feat.get(fid,[])
    statuses=sorted(set(c['Status'] for c in cases if c['Feature ID']==fid))
    trace.append([fid,', '.join(req_by_feat.get(fid,[])) or 'Oracle in feature matrix',', '.join(risk_by_feat.get(fid,[])[:4]) or 'See risk register',', '.join(tests),f[8],'/'.join(statuses) or 'NO_CASE',', '.join(bug_by_feat.get(fid,[])),'Yes' if any(c['Status'] in ('NOT_RUN','BLOCKED') for c in cases if c['Feature ID']==fid) else 'No'])
trace_headers=['Feature ID','Requirements','Risks','Test Cases','Checklist','Results','Bugs','Residual uncovered risk']
with (QA/'18_TRACEABILITY_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(trace_headers); w.writerows(trace)
write('18_TRACEABILITY_MATRIX.md','# 18 — Traceability Matrix\n\n'+md_table(trace_headers,trace))

exec_report=f'''# 19 — Test Execution Report

**Build:** `{BUILD}`  
**Execution date:** {DATE}

## Scope executed

Static syntax/DOM/CSS checks; isolated browser interactions for launch/localization/daily/navigation/core math/state/save/audio setting/boosters/reward fallback/viewports/touch; evidence screenshots.

## Metrics

'''+md_table(['Metric','Count'],[['Total test cases',83],['Passed',27],['Failed',5],['Blocked',2],['Not Run',30],['Not Applicable',0]])+'''

**Pass rate of executed product tests:** `27 / (27 + 5) = 84.4%`. Blocked and Not Run are excluded from denominator and shown separately.

## Results by module

'''+md_table(['Module','Key result'],[
['Launch/Build','Static PASS; direct/platform launch blocked'],['Core','Scoring/damage/bonus/gameOver/restart PASS; natural full cycle NOT_RUN'],['Save','Invalid JSON PASS; structured corruption FAIL BUG-001'],['Ads','Fallback reward integrity FAIL BUG-002; real ads BLOCKED'],['Boosters/Economy','Activation PASS; exit loss FAIL BUG-004'],['UI/Compatibility','Viewport/scroll PASS partial; edge clipping FAIL BUG-003'],['Audio','Mute persistence PASS; audible/background NOT_RUN'],['Localization','Main RU/EN PASS; full audit NOT_RUN'],['Performance','Simulated state stress PASS; FPS/memory NOT_RUN']
])+'''

## Defects

- Confirmed: 4 (`S2=2`, `S3=1`, `S4=1`; `P0=1`, `P1=2`, `P2=1`).
- Potential defects: 4, separated in Bug Reports.

## Smoke / critical path / regression

Smoke is incomplete and fails save resilience. Injected critical logic path passed, but natural-play and real input/platform paths are not complete. No full regression performed.

## Confidence

Medium for deterministic client logic; low for release/platform/performance/accessibility because environments unavailable.

## Recommendation

NO-GO. Fix BUG-002 and BUG-001; confirm package and run real Yandex tests; then retest BUG-004/003 and execute Critical/Core Regression.
'''
write('19_TEST_EXECUTION_REPORT.md',exec_report)

readiness=f'''# 20 — Release Readiness Report

# Verdict: **NO-GO**

## Основание

- Open `S2`: BUG-001 startup blocker for corrupted state; BUG-002 ad/economy bypass.
- Open `S3`: BUG-004 resource loss on normal navigation.
- Real Yandex loader/ads and release package not verified.
- Smoke/critical path incomplete in natural production-like environment.

## Gate status

'''+md_table(['Gate','Status','Reason'],[
['No open S1','PASS','0'],['No open S2','FAIL','2'],['Smoke','FAIL/INCOMPLETE','Save resilience fail; platform/input gaps'],['Critical path','PARTIAL','Injected logic pass; natural play not run'],['Startup stability','PARTIAL','Clean pass; affected save crash'],['Progress integrity','FAIL','Save crash and reward bypass'],['Performance acceptable','INSUFFICIENT DATA','No FPS/memory/real soak'],['Controls understandable','PARTIAL','Pointer mechanic; no natural/manual accessibility session'],['Platform readiness','BLOCKED','No Yandex draft/debug panel']
])+'''

## Обязательные исправления

1. BUG-002 — P0.
2. BUG-001 — P1.
3. BUG-004 — P1 or explicit accepted design with strong warning (not recommended).
4. Verify release ZIP and Yandex SDK loader/ad callbacks.

## Рекомендуемые

BUG-003; contrast/focus/reduced motion; keyboard alternative; full localization and performance pass.

## Условия смены на CONDITIONAL GO/GO

- BUG-001/002 retest PASS.
- Smoke and Critical Regression PASS on real package.
- Yandex `IT`, LoadingAPI/GameplayAPI, real rewarded/interstitial paths PASS.
- Natural full cycle on desktop and mobile PASS.
- No new S1/S2; remaining risk explicitly accepted.
'''
write('20_RELEASE_READINESS_REPORT.md',readiness)

workflow='''# 21 — Solo Developer QA Workflow

## Перед каждым коммитом

1. Test changed function with smallest related cases.
2. Check console/errors.
3. Run adjacent state/save/economy tests from Traceability.
4. Do not mark PASS without actual execution.

## Перед тестовой сборкой

Static checks → clean launch → smoke → core critical path → save valid/corrupt → known issue spot checks.

## Перед релизом

Release ZIP verification → full smoke → Critical/Core Regression → natural exploratory session → 30-minute soak → Yandex debug loader/ads → release readiness → known issues update.

## После bug fix

Exact repro → confirm expected result → repeat on clean/affected profile → local regression → adjacent system → evidence → status/changelog/verdict.

## Минимальный change-based набор

'''+md_table(['Изменение','Минимальный набор'],[
['UI','UI/COMP/LOC/ACC'],['Input','INPUT + STATE + natural core'],['Physics/collision','CORE-003..013 + edge charter'],['Save','SAVE-001..004 + all persistence'],['Settings/audio','AUDIO-001..004 + focus'],['Balance','CORE-002/005/006 + PROG/DAILY'],['SDK/dependency','PLAT/ADS + smoke/fullscreen/background'],['Crash fix','Exact crash + smoke + full affected module'],['Release','All gates in 20 report']
])+'''

## Практика

Keep one immutable test profile backup, one corrupt profile corpus, one release checklist. Update only statuses/evidence for each build; do not duplicate whole documents unless behavior changes.
'''
write('21_SOLO_DEVELOPER_QA_WORKFLOW.md',workflow)

known='# 22 — Known Issues\n\n'+md_table(['Bug','Severity','Priority','Кратко','Workaround'],[[b['Bug ID'],b['Severity'],b['Priority'],b['Title'],b['Workaround']] for b in bugs])
write('22_KNOWN_ISSUES.md',known)

changelog=f'''# 23 — QA Changelog

| Date | Build | Changes | Bugs | Verdict |
|---|---|---|---|---|
| {DATE} | `{BUILD}` | Создан полный QA-комплект; 83 cases; 20 checklists; 32 dynamic checks; evidence/logs | Added BUG-001..004 | NO-GO |
'''
write('23_QA_CHANGELOG.md',changelog)

questions='# 24 — Open Questions\n\n'+md_table(['ID','Вопрос','Почему важен','Компонент','Текущее предположение','Риск','Решение'],[
['Q-001','Какое финальное название: «Пыслей» или «Мыслей»?','Store/listing/localization','Brand','«Пыслей» — намеренный pun','Medium','Подтвердить и закрепить glossary'],['Q-002','Yandex Games — единственная target platform?','SDK paths/input requirements','Platform','Да','High','Подтвердить device types/orientation'],['Q-003','Reward fallback должен существовать в debug build?','BUG-002 treatment','Ads','Production reward only on onRewarded','Critical','Разделить debug flag and production behavior'],['Q-004','Должен ли Menu подтверждать потерю boosters?','BUG-004 oracle','Economy/UX','Да','High','Define confirm/cancel/refund'],['Q-005','Bonus duration upgrade влияет на start boosters?','Potential mismatch','Upgrades','Все magnet/double effects','Medium','Write explicit design rule'],['Q-006','Допустим ли local-clock daily exploit?','Economy','Daily','Risk not accepted for monetized release','Medium','Server time/SDK or explicit acceptance'],['Q-007','Какие performance targets/devices?','Release gates','Performance','60 FPS preferred, no formal target','High','Define minimum devices and thresholds'],['Q-008','Нужны ли keyboard/controller/TV controls?','Accessibility/platform reach','Input','Desktop mouse + mobile touch only','High','Confirm catalog device declarations'],['Q-009','Как выглядит final release ZIP?','Build validity','Packaging','assets directory required','High','Provide archive and run TC-BUILD-001']
])
write('24_OPEN_QUESTIONS.md',questions)

sources='''# 26 — Sources (checked 2026-07-17)

1. ISTQB CTFL Syllabus v4.0.1 — official ISTQB PDF/overview. https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
2. ISO/IEC/IEEE 29119-1:2022 General concepts. https://www.iso.org/standard/81291.html
3. ISO/IEC/IEEE 29119-2:2021 Test processes. https://www.iso.org/obp/ui/en/
4. ISO/IEC/IEEE 29119-3:2021 Test documentation. https://www.iso.org/standard/79429.html
5. ISO/IEC/IEEE 29119-4:2021 Test techniques. https://www.iso.org/standard/79430.html
6. Yandex Games game requirements, last updated 2026-07-01. https://yandex.com/dev/games/doc/en/concepts/requirements
7. Yandex Games SDK connection and usage. https://yandex.com/dev/games/doc/en/sdk/sdk-about
8. Yandex Games advertising / rewarded callbacks. https://yandex.com/dev/games/doc/en/sdk/sdk-adv
9. Yandex Games loading/gameplay markup. https://yandex.com/dev/games/doc/en/sdk/sdk-game-events
10. Game Accessibility Guidelines. https://gameaccessibilityguidelines.com/basic/
11. W3C WCAG 2.2 contrast and target size understanding. https://www.w3.org/WAI/WCAG22/quickref/ ; https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum

Публичные источники используются как methodology/oracle, а не как заявление о сертификации или moderation pass.
'''
write('26_SOURCES.md',sources)

# audit after preliminary creation will be updated later by verification script
write('25_DOCUMENTATION_AUDIT.md','# 25 — Documentation Audit\n\nPending automated consistency audit.\n')

print('Generated',len(list(QA.glob('*.md'))),'root markdown files,',len(cases),'test cases,',len(bugs),'bugs,',len(check_specs),'checklists')
