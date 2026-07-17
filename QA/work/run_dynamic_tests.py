from pathlib import Path
from datetime import datetime, timezone
import json, time, traceback
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8765/index.html'
QA = Path('/mnt/data/QA')
EVID = QA/'evidence'
EVID.mkdir(exist_ok=True)
results=[]
console_events=[]
page_errors=[]

def record(tid, name, status, actual='', expected='', evidence=''):
    print(f'[{status}] {tid} {name}: {actual}', flush=True)
    results.append({
        'id':tid,'name':name,'status':status,'actual':actual,'expected':expected,'evidence':evidence,
        'time_utc':datetime.now(timezone.utc).isoformat()
    })

def run(tid,name,fn,expected=''):
    try:
        actual,evidence = fn()
        record(tid,name,'PASS',str(actual),expected,evidence or '')
    except AssertionError as e:
        record(tid,name,'FAIL',str(e),expected,'')
    except Exception as e:
        record(tid,name,'BLOCKED',f'{type(e).__name__}: {e}',expected,'')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'])
    context = browser.new_context(viewport={'width':1024,'height':768}, locale='ru-RU')
    page = context.new_page()
    page.on('console', lambda msg: console_events.append({'type':msg.type,'text':msg.text,'url':page.url}))
    page.on('pageerror', lambda err: page_errors.append({'error':str(err),'url':page.url}))

    def clean_load(url=BASE):
        page.goto(url, wait_until='load')
        page.evaluate('localStorage.clear()')
        page.reload(wait_until='load')
        page.wait_for_timeout(250)

    def t_launch():
        clean_load()
        assert page.locator('#menuScreen').get_attribute('class').find('screen-active') >= 0, 'Главный экран не активен'
        assert page.locator('#playButton').is_visible(), 'Кнопка Играть не видна'
        path=EVID/'EV-001_menu_1024x768.png'; page.screenshot(path=str(path), full_page=True)
        return 'Главное меню отображено; JS инициализирован', str(path.relative_to(QA))
    run('DYN-001','Чистый запуск и отображение главного меню',t_launch,'Меню активно, кнопки доступны, нет фатальной ошибки')

    def t_no_errors():
        fat=[x for x in page_errors]
        assert not fat, f'Ошибки страницы: {fat}'
        return f'pageerror={len(fat)}', ''
    run('DYN-002','Отсутствие необработанных JS-ошибок при чистом запуске',t_no_errors,'0 pageerror')

    def t_en():
        page.goto(BASE+'?lang=en',wait_until='load'); page.wait_for_timeout(150)
        assert page.locator('html').get_attribute('lang')=='en'
        assert page.locator('#playButton').inner_text()=='Play'
        assert page.title()=='Thought Vacuum'
        path=EVID/'EV-002_menu_en.png'; page.screenshot(path=str(path))
        return 'lang=en, title=Thought Vacuum, Play', str(path.relative_to(QA))
    run('DYN-003','Переключение локализации через ?lang=en',t_en,'Интерфейс и document.lang на английском')

    def t_ru():
        page.goto(BASE+'?lang=ru',wait_until='load'); page.wait_for_timeout(100)
        assert page.locator('html').get_attribute('lang')=='ru'
        assert page.locator('#playButton').inner_text()=='Играть'
        return 'lang=ru, Играть', ''
    run('DYN-004','Явная русская локализация',t_ru,'Интерфейс на русском')

    def t_daily():
        clean_load(BASE+'?lang=ru')
        before=page.evaluate('progress.stars')
        page.locator('#dailyRewardButton').click()
        after=page.evaluate('progress.stars')
        disabled=page.locator('#dailyRewardButton').is_disabled()
        assert after-before==3, f'Звезды: {before}->{after}'
        assert disabled, 'Кнопка не заблокирована после получения'
        page.reload(wait_until='load'); page.wait_for_timeout(100)
        assert page.evaluate('progress.stars')==after
        assert page.locator('#dailyRewardButton').is_disabled()
        return f'+3 звезды, сохранено после reload; stars={after}', ''
    run('DYN-005','Ежедневная награда: получение один раз и сохранение',t_daily,'+3, повторное получение заблокировано, состояние сохраняется')

    def t_nav():
        page.locator('#upgradesButton').click()
        assert page.locator('#upgradesScreen').get_attribute('class').find('screen-active')>=0
        assert page.locator('#upgradesList .upgrade-card').count()==3
        assert page.locator('#boostersList .store-card').count()==3
        assert page.locator('#skinsList .store-card').count()==4
        assert page.locator('#dailyTasksList .task-card').count()==3
        page.locator('#backFromUpgradesButton').click()
        assert page.locator('#menuScreen').get_attribute('class').find('screen-active')>=0
        return 'Меню→Улучшения→Меню; 3 улучшения, 3 бустера, 4 скина, 3 задания', ''
    run('DYN-006','Навигация в мастерскую и обратно',t_nav,'Экраны переключаются, карточки отрисованы')

    def t_keyboard_nav():
        clean_load()
        page.keyboard.press('Tab')
        first=page.evaluate('document.activeElement.id')
        assert first in {'dailyRewardButton','playButton'}, f'Первый фокус: {first}'
        seen=[]
        for _ in range(6):
            seen.append(page.evaluate('document.activeElement.id'))
            page.keyboard.press('Tab')
        assert 'playButton' in seen and 'upgradesButton' in seen, f'Фокус-цикл: {seen}'
        return f'Фокус достигает основных кнопок: {seen}', ''
    run('DYN-007','Клавиатурная навигация по меню',t_keyboard_nav,'Tab достигает Играть и Улучшения')

    def t_start():
        clean_load()
        page.locator('#playButton').click(); page.wait_for_timeout(100)
        state=page.evaluate('({screen:currentScreen,running:game.running,score:game.score,lives:game.lives,combo:game.combo})')
        assert state=={'screen':'game','running':True,'score':0,'lives':3,'combo':1}, state
        path=EVID/'EV-003_game_start.png'; page.screenshot(path=str(path))
        return state, str(path.relative_to(QA))
    run('DYN-008','Начало нового раунда',t_start,'game, running, 0 очков, 3 жизни, x1')

    def t_pointer_bounds():
        page.mouse.move(-100,-100)
        page.wait_for_timeout(30)
        a=page.evaluate('({tx:game.player.tx,ty:game.player.ty})')
        page.mouse.move(2000,2000); page.wait_for_timeout(30)
        b=page.evaluate('({tx:game.player.tx,ty:game.player.ty,w:width,h:height})')
        assert a['tx']==20 and a['ty']==20, a
        assert b['tx']==b['w']-20 and b['ty']==b['h']-20, b
        return f'Нижняя/верхняя границы: {a}; {b}', ''
    run('DYN-009','Ограничение цели указателя границами canvas',t_pointer_bounds,'tx/ty ограничены диапазоном 20..width/height-20')

    def t_pause_resume():
        state=page.evaluate("pauseActiveGame('window'); ({running:game.running,reason:game.pausedBySystem,marked:gameplayMarkedActive})")
        assert state['running'] is False and state['reason']=='window'
        state2=page.evaluate("resumeSystemPausedGame('window'); ({running:game.running,reason:game.pausedBySystem,marked:gameplayMarkedActive})")
        assert state2['running'] is True and state2['reason']==''
        return f'{state} -> {state2}', ''
    run('DYN-010','Системная пауза и продолжение',t_pause_resume,'Раунд останавливается и возобновляется по совпадающей причине')

    def t_good_combo():
        data=page.evaluate("""
        game.score=0; game.combo=1; game.streak=0; game.maxComboThisRun=1;
        for(let i=0;i<5;i++) collectThought({type:'good',x:100,y:100});
        ({score:game.score,combo:game.combo,streak:game.streak,max:game.maxComboThisRun})
        """)
        assert data['score']==50 and data['combo']==2 and data['streak']==5, data
        return data,''
    run('DYN-011','Подсчет очков и повышение комбо после 5 хороших мыслей',t_good_combo,'50 очков, combo x2, streak 5')

    def t_bad_life():
        data=page.evaluate("game.lives=3; game.shieldActive=false; collectThought({type:'bad',x:100,y:100}); ({lives:game.lives,combo:game.combo,streak:game.streak})")
        assert data['lives']==2 and data['combo']==1 and data['streak']==0, data
        return data,''
    run('DYN-012','Столкновение с вредной мыслью без щита',t_bad_life,'-1 жизнь, сброс combo/streak')

    def t_shield():
        data=page.evaluate("game.lives=3; game.shieldActive=true; collectThought({type:'bad',x:100,y:100}); ({lives:game.lives,shield:game.shieldActive})")
        assert data['lives']==3 and data['shield'] is False, data
        return data,''
    run('DYN-013','Щит блокирует одну вредную мысль',t_shield,'Жизнь не теряется, щит расходуется')

    def t_gold():
        data=page.evaluate("game.score=0; game.combo=1; game.magnetTimer=0; game.slowTimer=0; game.doubleTimer=0; collectThought({type:'gold',x:100,y:100}); ({score:game.score,active:[game.magnetTimer,game.slowTimer,game.doubleTimer]})")
        assert data['score']==50, data
        assert any(v>0 for v in data['active']), data
        return data,''
    run('DYN-014','Золотая мысль: очки и случайный бонус',t_gold,'+50 при x1 и один активный бонус')

    def t_double_score():
        data=page.evaluate("game.score=0; game.combo=2; game.doubleTimer=5; game.streak=0; collectThought({type:'good',x:100,y:100}); game.score")
        assert data==40, data
        return data,''
    run('DYN-015','Двойные очки вместе с combo',t_double_score,'10×2×combo2 = 40')

    def t_end():
        page.evaluate("game.score=250; game.lives=1; game.running=true; collectThought({type:'bad',x:100,y:100})")
        page.wait_for_timeout(100)
        st=page.evaluate('({screen:currentScreen,running:game.running,score:progress.bestScore,stars:progress.stars,earned:game.earnedStarsThisRun})')
        assert st['screen']=='gameOver' and st['running'] is False and st['score']>=250 and st['earned']==2, st
        path=EVID/'EV-004_game_over.png'; page.screenshot(path=str(path))
        return st,str(path.relative_to(QA))
    run('DYN-016','Поражение, экран результата и начисление звезд',t_end,'gameOver, best>=250, 2 звезды за 250 очков')

    def t_restart():
        page.locator('#restartButton').click(); page.wait_for_timeout(80)
        st=page.evaluate('({screen:currentScreen,running:game.running,score:game.score,lives:game.lives,combo:game.combo})')
        assert st['screen']=='game' and st['running'] and st['score']==0 and st['lives']==3 and st['combo']==1, st
        return st,''
    run('DYN-017','Перезапуск после поражения',t_restart,'Новый чистый раунд')

    def t_save_corrupt_json():
        page.evaluate("localStorage.setItem('thoughtVacuumProgress.v1','not-json')")
        page.reload(wait_until='load'); page.wait_for_timeout(100)
        st=page.evaluate('({best:progress.bestScore,stars:progress.stars,screen:currentScreen})')
        assert st=={'best':0,'stars':0,'screen':'menu'}, st
        return st,''
    run('DYN-018','Поврежденное сохранение: невалидный JSON',t_save_corrupt_json,'Безопасный fallback на значения по умолчанию')

    def t_persistence_settings():
        clean_load()
        page.locator('#playButton').click(); page.locator('#soundToggleButton').click(); page.wait_for_timeout(50)
        muted=page.evaluate('progress.soundMuted')
        page.reload(wait_until='load'); page.wait_for_timeout(80)
        muted2=page.evaluate('progress.soundMuted')
        assert muted and muted2 and page.locator('#soundToggleButton').get_attribute('aria-label')=='Включить звук'
        return 'soundMuted=true сохраняется; aria-label обновлен',''
    run('DYN-019','Сохранение настройки звука',t_persistence_settings,'Mute сохраняется после reload')

    def t_boosters():
        clean_load()
        page.evaluate("progress.stars=20; progress.boosters={magnetStart:1,shield:1,doubleStart:1}; saveProgress(); updateMenu()")
        page.locator('#playButton').click(); page.wait_for_timeout(50)
        st=page.evaluate('({boosters:progress.boosters,magnet:game.magnetTimer,shield:game.shieldActive,double:game.doubleTimer})')
        assert st['boosters']=={'magnetStart':0,'shield':0,'doubleStart':0}, st
        assert st['magnet']>0 and st['shield'] and st['double']>0, st
        return st,''
    run('DYN-020','Применение и расход стартовых бустеров',t_boosters,'Все три бустера расходуются и активируются')

    def t_exit_consumes():
        page.locator('#gameMenuButton').click(); page.wait_for_timeout(50)
        st=page.evaluate('({screen:currentScreen,boosters:progress.boosters,running:game.running})')
        assert st['screen']=='menu' and st['running'] is False
        assert st['boosters']=={'magnetStart':0,'shield':0,'doubleStart':0}
        path=EVID/'EV-005_menu_after_booster_exit.png'; page.screenshot(path=str(path))
        return 'Выход выполнен без подтверждения; ранее активированные бустеры не возвращены',str(path.relative_to(QA))
    run('DYN-021','Выход в меню после расхода бустеров',t_exit_consumes,'Фиксация фактического поведения для bug oracle')

    def t_reward_fallback_revive():
        clean_load(); page.locator('#playButton').click()
        page.evaluate("game.score=100; game.lives=1; game.running=true; collectThought({type:'bad',x:1,y:1})")
        assert page.locator('#reviveAdButton').is_visible()
        before=page.evaluate('({sdk:yaSdk,running:game.running,revived:game.revivedOnce})')
        page.locator('#reviveAdButton').click(); page.wait_for_timeout(100)
        after=page.evaluate('({screen:currentScreen,running:game.running,revived:game.revivedOnce,lives:game.lives,sdk:yaSdk})')
        assert before['sdk'] is None and after['sdk'] is None
        assert after['running'] and after['revived'] and after['lives']==1 and after['screen']=='game', after
        return f'Без SDK награда выдана автоматически: {before} -> {after}',''
    run('DYN-022','Rewarded revive при недоступном SDK',t_reward_fallback_revive,'Фиксация: награда не должна выдаваться без просмотра рекламы')

    def t_reward_fallback_double():
        page.evaluate("game.score=200; game.lives=1; game.running=true; collectThought({type:'bad',x:1,y:1})")
        assert page.locator('#doubleStarsAdButton').is_visible()
        before=page.evaluate('progress.stars')
        earned=page.evaluate('game.earnedStarsThisRun')
        page.locator('#doubleStarsAdButton').click(); page.wait_for_timeout(100)
        after=page.evaluate('progress.stars')
        doubled=page.evaluate('game.starsDoubled')
        assert doubled and after-before==earned, (before,after,earned)
        return f'Без SDK автоматически добавлено {earned} звезд ({before}->{after})',''
    run('DYN-023','Rewarded x2 звезд при недоступном SDK',t_reward_fallback_double,'Фиксация: награда не должна выдаваться без просмотра рекламы')

    def t_player_clipping():
        page.locator('#restartButton').click(); page.wait_for_timeout(50)
        page.mouse.move(0,350); page.wait_for_timeout(700)
        st=page.evaluate('({x:game.player.x,tx:game.player.tx,radius:game.player.radius})')
        path=EVID/'EV-006_player_at_left_edge.png'; page.screenshot(path=str(path))
        assert st['tx']==20
        return st,str(path.relative_to(QA))
    run('DYN-024','Перемещение пылесоса к левой границе',t_player_clipping,'Скриншот для оценки визуального обрезания')

    def t_simulated_long():
        # Avoid wall-clock delay: deterministic state-loop stress, explicitly recorded as simulated time.
        st=page.evaluate("""
        game.thoughts=[]; game.particles=[]; game.running=true; game.lives=9999;
        let ok=true; let error='';
        try { const oldSpawn=spawnThought; spawnThought=()=>{}; for(let i=0;i<3000;i++){ updateGame(0.033); if(!Number.isFinite(game.score)) throw new Error('non-finite score'); } }
        catch(e){ok=false; error=String(e)} finally { spawnThought=oldSpawn; }
        ({ok,error,elapsed:game.elapsed,thoughts:game.thoughts.length,particles:game.particles.length,score:game.score,running:game.running})
        """)
        assert st['ok'] and st['elapsed']>95 and st['running'], st
        return f"Симулировано {st['elapsed']:.1f}s update-loop; thoughts={st['thoughts']}, particles={st['particles']}, score={st['score']}",''
    run('DYN-025','Стресс update-loop с симуляцией ~100 секунд игрового времени',t_simulated_long,'Нет исключения/NaN; это не реальный soak/FPS-тест')

    # Corrupted structured save: separate context to capture startup blocker.
    def t_corrupt_structured():
        c=browser.new_context(viewport={'width':800,'height':600}, locale='ru-RU')
        pg=c.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        pg.add_init_script("localStorage.setItem('thoughtVacuumProgress.v1', JSON.stringify({dailyTasks:[null,null,null]}));")
        pg.goto(BASE,wait_until='load'); pg.wait_for_timeout(200)
        play_visible=pg.locator('#playButton').is_visible()
        active=pg.locator('#menuScreen').get_attribute('class')
        # Script abort is evidenced by pageerror and missing expected initialized state (e.g. generated task cards on navigation).
        path=EVID/'EV-007_corrupt_save_startup.png'; pg.screenshot(path=str(path))
        c.close()
        assert errs, f'Ожидалась pageerror, получено {errs}'
        return f'pageerror={errs}; статическая разметка видна={play_visible}; class={active}',str(path.relative_to(QA))
    run('DYN-026','Поврежденное структурированное сохранение с null в dailyTasks',t_corrupt_structured,'Ожидается устойчивый fallback; фактически проверяется наличие startup exception')

    # Viewport checks.
    def viewport_check(w,h,label):
        c=browser.new_context(viewport={'width':w,'height':h}, locale='ru-RU')
        pg=c.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(BASE,wait_until='load'); pg.evaluate('localStorage.clear()'); pg.reload(wait_until='load'); pg.wait_for_timeout(100)
        pg.locator('#upgradesButton').click(); pg.wait_for_timeout(100)
        metrics=pg.evaluate("""({
          vw:innerWidth,vh:innerHeight,
          screenScroll:document.querySelector('#upgradesScreen').scrollHeight,
          screenClient:document.querySelector('#upgradesScreen').clientHeight,
          panelScroll:document.querySelector('#upgradesScreen .panel').scrollHeight,
          panelClient:document.querySelector('#upgradesScreen .panel').clientHeight,
          backVisible:!!document.querySelector('#backFromUpgradesButton').offsetParent
        })""")
        path=EVID/f'EV-VP-{label}.png'; pg.screenshot(path=str(path))
        c.close()
        assert not errs, errs
        assert metrics['backVisible']
        return metrics,str(path.relative_to(QA))
    for tid,w,h,label in [('DYN-027',320,568,'320x568'),('DYN-028',360,640,'360x640'),('DYN-029',768,1024,'768x1024'),('DYN-030',1366,768,'1366x768'),('DYN-031',1920,1080,'1920x1080')]:
        run(tid,f'Отображение мастерской при {label}',lambda w=w,h=h,label=label:viewport_check(w,h,label),'Экран доступен, без JS error; прокрутка при необходимости')

    # Mobile touch scroll test.
    def t_touch_scroll():
        c=browser.new_context(viewport={'width':360,'height':640}, locale='ru-RU', is_mobile=True, has_touch=True, device_scale_factor=2)
        pg=c.new_page(); pg.goto(BASE,wait_until='load'); pg.evaluate('localStorage.clear()'); pg.reload(wait_until='load'); pg.locator('#upgradesButton').click(); pg.wait_for_timeout(100)
        panel=pg.locator('#upgradesScreen .panel'); box=panel.bounding_box(); assert box
        before=panel.evaluate('(e)=>e.scrollTop')
        cdp=c.new_cdp_session(pg)
        x=box['x']+box['width']/2; y1=min(box['y']+box['height']-70,600); y2=box['y']+90
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y1,'radiusX':2,'radiusY':2,'force':1}]})
        steps=8
        for i in range(1,steps+1):
            y=y1+(y2-y1)*i/steps
            cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y,'radiusX':2,'radiusY':2,'force':1}]})
            pg.wait_for_timeout(20)
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        pg.wait_for_timeout(400)
        after=panel.evaluate('(e)=>e.scrollTop')
        path=EVID/'EV-008_mobile_touch_scroll.png'; pg.screenshot(path=str(path))
        c.close()
        assert after>before+10, f'touch scrollTop {before}->{after}'
        return f'scrollTop {before}->{after}',str(path.relative_to(QA))
    run('DYN-032','Сенсорная прокрутка длинной мастерской 360×640',t_touch_scroll,'scrollTop увеличивается после свайпа')

    browser.close()

(QA/'logs/dynamic_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
(QA/'logs/browser_console.json').write_text(json.dumps(console_events,ensure_ascii=False,indent=2),encoding='utf-8')
(QA/'logs/page_errors.json').write_text(json.dumps(page_errors,ensure_ascii=False,indent=2),encoding='utf-8')
summary={s:sum(1 for r in results if r['status']==s) for s in ['PASS','FAIL','BLOCKED','NOT_RUN']}
print(json.dumps({'summary':summary,'results':results},ensure_ascii=False,indent=2))
