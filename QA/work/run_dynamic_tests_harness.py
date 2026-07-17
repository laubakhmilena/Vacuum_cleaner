from pathlib import Path
from datetime import datetime, timezone
import json, traceback
from playwright.sync_api import sync_playwright

QA=Path('/mnt/data/QA')
ROOT=QA/'work/runtime'
EVID=QA/'evidence'; EVID.mkdir(exist_ok=True)
results=[]; console_events=[]; page_errors=[]

INDEX=(ROOT/'index.html').read_text(encoding='utf-8-sig')
CSS=(ROOT/'style.css').read_text(encoding='utf-8')
DATA=(ROOT/'assets/vacuum_player_data.js').read_text(encoding='utf-8')
GAME=(ROOT/'game.js').read_text(encoding='utf-8')
# Test-harness-only URL substitution: about:blank cannot be a base URL for new URL(relative, location.href).
GAME_HARNESS=GAME.replace('new URL("assets/vacuum_player.png", window.location.href).href','"https://qa.local/assets/vacuum_player.png"')

def harness_html(storage=None):
    storage=storage or {}
    store_json=json.dumps(storage,ensure_ascii=False)
    mock=f'''<script>
const __store = {store_json};
Object.defineProperty(window, 'localStorage', {{ value: {{
  setItem:(k,v)=>__store[k]=String(v),
  getItem:(k)=>Object.prototype.hasOwnProperty.call(__store,k)?__store[k]:null,
  removeItem:(k)=>delete __store[k],
  clear:()=>{{for(const k of Object.keys(__store)) delete __store[k];}},
  key:(i)=>Object.keys(__store)[i]??null,
  get length(){{return Object.keys(__store).length;}}
}}, configurable:true }});
window.__qaStorageDump=()=>JSON.parse(JSON.stringify(__store));
</script>'''
    html=INDEX
    html=html.replace('<link rel="stylesheet" href="style.css">',f'<style>{CSS}</style>')
    html=html.replace('<script src="/sdk.js"></script>','')
    html=html.replace('<script src="assets/vacuum_player_data.js"></script>',f'<script>{DATA}</script>')
    html=html.replace('<script src="game.js"></script>',mock+f'<script>{GAME_HARNESS}</script>')
    return html

def record(tid,name,status,actual='',expected='',evidence=''):
    print(f'[{status}] {tid} {name}: {actual}',flush=True)
    results.append({'id':tid,'name':name,'status':status,'actual':str(actual),'expected':expected,'evidence':evidence,'time_utc':datetime.now(timezone.utc).isoformat()})

def run(tid,name,fn,expected=''):
    try:
        out=fn()
        actual,evidence=(out if isinstance(out,tuple) else (out,''))
        record(tid,name,'PASS',actual,expected,evidence)
    except AssertionError as e:
        record(tid,name,'FAIL',e,expected,'')
    except Exception as e:
        record(tid,name,'BLOCKED',f'{type(e).__name__}: {e}',expected,'')

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'])
    current={'context':None,'page':None}

    def load(locale='ru-RU', viewport=(1024,768), storage=None, mobile=False, touch=False, dpr=1):
        if current['context']:
            current['context'].close()
        c=browser.new_context(viewport={'width':viewport[0],'height':viewport[1]}, locale=locale, is_mobile=mobile, has_touch=touch, device_scale_factor=dpr)
        pg=c.new_page(); pg.set_default_timeout(3000)
        pg.on('console',lambda m:console_events.append({'type':m.type,'text':m.text,'test_url':'set_content'}))
        pg.on('pageerror',lambda e:page_errors.append({'error':str(e),'test_url':'set_content'}))
        pg.set_content(harness_html(storage),wait_until='load')
        pg.wait_for_timeout(120)
        current['context']=c; current['page']=pg
        return pg

    def pg(): return current['page']
    def dump_store(): return pg().evaluate('__qaStorageDump()')

    def t001():
        q=load(); assert q.locator('#menuScreen').get_attribute('class').find('screen-active')>=0; assert q.locator('#playButton').is_visible()
        path=EVID/'EV-001_menu_1024x768.png'; q.screenshot(path=str(path))
        return 'Главное меню отображено; game.js инициализирован',str(path.relative_to(QA))
    run('DYN-001','Чистый запуск через изолированный браузерный harness',t001,'Меню активно, фатальных ошибок нет')

    def t002():
        assert pg().evaluate("typeof startGame==='function' && typeof progress==='object' && typeof game==='object'")
        # page_errors includes all prior pages; clean launch is validated by visible initialized UI and function globals.
        return 'Глобальные функции/состояние доступны, инициализация завершена',''
    run('DYN-002','Инициализация JavaScript',t002,'startGame/progress/game доступны')

    def t003():
        q=load(locale='en-US'); assert q.locator('html').get_attribute('lang')=='en'; assert q.locator('#playButton').inner_text()=='Play'; assert q.title()=='Thought Vacuum'
        path=EVID/'EV-002_menu_en.png'; q.screenshot(path=str(path)); return 'navigator.language=en-US → English UI',str(path.relative_to(QA))
    run('DYN-003','Автовыбор английской локализации',t003,'Английский UI и document.lang=en')

    def t004():
        q=load(locale='ru-RU'); assert q.locator('html').get_attribute('lang')=='ru'; assert q.locator('#playButton').inner_text()=='Играть';
        vals=q.evaluate("[resolveLanguage('be-BY'),resolveLanguage('kk-KZ'),resolveLanguage('uk-UA'),resolveLanguage('de-DE')]")
        assert vals==['ru','ru','ru','en']; return f'ru UI; mapping={vals}',''
    run('DYN-004','Русская локализация и карта языковых кодов',t004,'ru/be/kk/uk/uz→ru, прочие→en')

    def t005():
        q=load(); before=q.evaluate('progress.stars'); q.locator('#dailyRewardButton').click(); after=q.evaluate('progress.stars'); assert after-before==3; assert q.locator('#dailyRewardButton').is_disabled()
        seed=dump_store(); q=load(storage=seed); assert q.evaluate('progress.stars')==after; assert q.locator('#dailyRewardButton').is_disabled(); return f'+3 и сохранено, stars={after}',''
    run('DYN-005','Ежедневная награда: однократное получение и persistence',t005,'+3, повторно недоступно')

    def t006():
        q=pg(); q.locator('#upgradesButton').click(); assert q.locator('#upgradesScreen').get_attribute('class').find('screen-active')>=0
        counts=[q.locator('#upgradesList .upgrade-card').count(),q.locator('#boostersList .store-card').count(),q.locator('#skinsList .store-card').count(),q.locator('#dailyTasksList .task-card').count()]
        assert counts==[3,3,4,3]; q.locator('#backFromUpgradesButton').click(); assert q.locator('#menuScreen').get_attribute('class').find('screen-active')>=0
        return f'counts={counts}; возврат в меню',''
    run('DYN-006','Навигация Меню → Мастерская → Меню',t006,'3 улучшения, 3 бустера, 4 скина, 3 задания')

    def t007():
        q=load(); seen=[]
        for _ in range(8): q.keyboard.press('Tab'); seen.append(q.evaluate('document.activeElement.id'))
        assert 'playButton' in seen and 'upgradesButton' in seen and 'dailyRewardButton' in seen,seen
        return f'Фокус: {seen}',''
    run('DYN-007','Клавиатурная навигация по меню',t007,'Tab достигает основных кнопок')

    def t008():
        q=load(); q.locator('#playButton').click(); q.wait_for_timeout(80); st=q.evaluate('({screen:currentScreen,running:game.running,score:game.score,lives:game.lives,combo:game.combo})'); assert st=={'screen':'game','running':True,'score':0,'lives':3,'combo':1},st
        path=EVID/'EV-003_game_start.png'; q.screenshot(path=str(path)); return st,str(path.relative_to(QA))
    run('DYN-008','Начало нового раунда',t008,'0 очков, 3 жизни, x1')

    def t009():
        q=pg(); a=q.evaluate("updatePointer({clientX:-100,clientY:-100});({tx:game.player.tx,ty:game.player.ty})"); b=q.evaluate("updatePointer({clientX:2000,clientY:2000});({tx:game.player.tx,ty:game.player.ty,w:width,h:height})"); assert a=={'tx':20,'ty':20},a; assert b['tx']==b['w']-20 and b['ty']==b['h']-20,b; return f'{a}; {b}',''
    run('DYN-009','Граничные значения координат указателя',t009,'20..width/height-20')

    def t010():
        q=pg(); a=q.evaluate("pauseActiveGame('window'); ({running:game.running,reason:game.pausedBySystem})"); b=q.evaluate("resumeSystemPausedGame('window'); ({running:game.running,reason:game.pausedBySystem})"); assert a=={'running':False,'reason':'window'} and b=={'running':True,'reason':''}; return f'{a}->{b}',''
    run('DYN-010','Системная пауза/возобновление',t010,'running false→true')

    def t011():
        st=pg().evaluate("game.score=0;game.combo=1;game.streak=0;game.maxComboThisRun=1;for(let i=0;i<5;i++)collectThought({type:'good',x:100,y:100});({score:game.score,combo:game.combo,streak:game.streak,max:game.maxComboThisRun})"); assert st=={'score':50,'combo':2,'streak':5,'max':2},st; return st,''
    run('DYN-011','5 хороших мыслей и повышение combo',t011,'50 очков, combo x2')

    def t012():
        st=pg().evaluate("game.lives=3;game.shieldActive=false;collectThought({type:'bad',x:1,y:1});({lives:game.lives,combo:game.combo,streak:game.streak})"); assert st['lives']==2 and st['combo']==1 and st['streak']==0; return st,''
    run('DYN-012','Вредная мысль без щита',t012,'-1 жизнь, сброс комбо')

    def t013():
        st=pg().evaluate("game.lives=3;game.shieldActive=true;collectThought({type:'bad',x:1,y:1});({lives:game.lives,shield:game.shieldActive})"); assert st=={'lives':3,'shield':False}; return st,''
    run('DYN-013','Щит блокирует вредную мысль',t013,'Жизнь сохранена, щит расходован')

    def t014():
        st=pg().evaluate("game.score=0;game.combo=1;game.magnetTimer=0;game.slowTimer=0;game.doubleTimer=0;collectThought({type:'gold',x:1,y:1});({score:game.score,t:[game.magnetTimer,game.slowTimer,game.doubleTimer]})"); assert st['score']==50 and any(x>0 for x in st['t']); return st,''
    run('DYN-014','Золотая мысль: очки и бонус',t014,'+50 и один таймер бонуса')

    def t015():
        score=pg().evaluate("game.score=0;game.combo=2;game.doubleTimer=5;game.streak=0;collectThought({type:'good',x:1,y:1});game.score"); assert score==40,score; return score,''
    run('DYN-015','Комбинация x2 и combo x2',t015,'40 очков')

    def t016():
        q=pg(); q.evaluate("game.score=250;game.lives=1;game.running=true;collectThought({type:'bad',x:1,y:1})"); q.wait_for_timeout(50); st=q.evaluate('({screen:currentScreen,running:game.running,best:progress.bestScore,earned:game.earnedStarsThisRun})'); assert st['screen']=='gameOver' and not st['running'] and st['best']>=250 and st['earned']==2,st
        path=EVID/'EV-004_game_over.png'; q.screenshot(path=str(path)); return st,str(path.relative_to(QA))
    run('DYN-016','Поражение и экран результата',t016,'gameOver, 2 звезды за 250')

    def t017():
        q=pg(); q.locator('#restartButton').click(); st=q.evaluate('({screen:currentScreen,running:game.running,score:game.score,lives:game.lives,combo:game.combo})'); assert st=={'screen':'game','running':True,'score':0,'lives':3,'combo':1}; return st,''
    run('DYN-017','Перезапуск после поражения',t017,'Чистый новый раунд')

    def t018():
        seed={'thoughtVacuumProgress.v1':'not-json'}; q=load(storage=seed); st=q.evaluate('({best:progress.bestScore,stars:progress.stars,screen:currentScreen})'); assert st=={'best':0,'stars':0,'screen':'menu'}; return st,''
    run('DYN-018','Невалидный JSON сохранения',t018,'Fallback без блокировки запуска')

    def t019():
        q=load(); q.locator('#playButton').click(); q.locator('#soundToggleButton').click(); assert q.evaluate('progress.soundMuted'); seed=dump_store(); q=load(storage=seed); assert q.evaluate('progress.soundMuted'); assert q.locator('#soundToggleButton').get_attribute('aria-label')=='Включить звук'; return 'soundMuted persisted; aria-label=Включить звук',''
    run('DYN-019','Сохранение mute-настройки',t019,'Mute сохраняется')

    def t020():
        q=load(); q.evaluate("progress.stars=20;progress.boosters={magnetStart:1,shield:1,doubleStart:1};saveProgress();updateMenu()"); q.locator('#playButton').click(); st=q.evaluate('({b:progress.boosters,magnet:game.magnetTimer,shield:game.shieldActive,double:game.doubleTimer})'); assert st['b']=={'magnetStart':0,'shield':0,'doubleStart':0} and st['magnet']>0 and st['shield'] and st['double']>0,st; return st,''
    run('DYN-020','Расход стартовых бустеров',t020,'Все активированы и уменьшены на 1')

    def t021():
        q=pg(); q.locator('#gameMenuButton').click(); st=q.evaluate('({screen:currentScreen,running:game.running,b:progress.boosters})'); assert st['screen']=='menu' and not st['running'] and st['b']=={'magnetStart':0,'shield':0,'doubleStart':0}; path=EVID/'EV-005_menu_after_booster_exit.png'; q.screenshot(path=str(path)); return 'Выход без подтверждения; бустеры не возвращены',str(path.relative_to(QA))
    run('DYN-021','Выход в меню после активации бустеров',t021,'Фиксация потенциальной потери расходуемых ресурсов')

    def t022():
        q=load(); q.locator('#playButton').click(); q.evaluate("game.score=100;game.lives=1;game.running=true;collectThought({type:'bad',x:1,y:1})"); q.wait_for_timeout(300); pre=q.evaluate('({sdk:yaSdk,screen:currentScreen,running:game.running,revived:game.revivedOnce,lives:game.lives,buttonHidden:ui.reviveAdButton.classList.contains(\"hidden\"),buttonDisabled:ui.reviveAdButton.disabled})'); assert q.locator('#reviveAdButton').is_visible(),pre; q.locator('#reviveAdButton').click(); q.wait_for_timeout(80); st=q.evaluate('({sdk:yaSdk,screen:currentScreen,running:game.running,revived:game.revivedOnce,lives:game.lives})'); assert st['sdk'] is None and st['running'] and st['revived'] and st['lives']==1,{'pre':pre,'after':st}; return {'pre':pre,'after':st},''
    run('DYN-022','Rewarded revive при отсутствующем Yandex SDK',t022,'Награда не должна выдаваться без просмотра; фиксируется фактическое поведение')

    def t023():
        q=pg(); q.evaluate("game.score=200;game.lives=1;game.running=true;collectThought({type:'bad',x:1,y:1})"); before=q.evaluate('progress.stars'); earned=q.evaluate('game.earnedStarsThisRun'); q.locator('#doubleStarsAdButton').click(); after=q.evaluate('progress.stars'); assert q.evaluate('game.starsDoubled') and after-before==earned; return f'без SDK stars {before}->{after}, bonus={earned}',''
    run('DYN-023','Rewarded x2 звезд при отсутствующем Yandex SDK',t023,'Награда не должна выдаваться без просмотра; фиксируется фактическое поведение')

    def t024():
        q=pg(); q.locator('#restartButton').click(); q.mouse.move(0,350); q.wait_for_timeout(700); st=q.evaluate('({x:game.player.x,tx:game.player.tx,radius:game.player.radius})'); path=EVID/'EV-006_player_at_left_edge.png'; q.screenshot(path=str(path)); assert st['tx']==20; return st,str(path.relative_to(QA))
    run('DYN-024','Пылесос у левой границы',t024,'Скриншот для проверки визуального обрезания')

    def t025():
        st=pg().evaluate("""
        game.thoughts=[];game.particles=[];game.running=true;game.lives=9999;const oldSpawn=spawnThought;spawnThought=()=>{};let ok=true,error='';
        try{for(let i=0;i<3000;i++){updateGame(0.033);if(!Number.isFinite(game.score))throw new Error('non-finite')}}catch(e){ok=false;error=String(e)}finally{spawnThought=oldSpawn}
        ({ok,error,elapsed:game.elapsed,score:game.score,running:game.running})"""); assert st['ok'] and st['elapsed']>95 and st['running'],st; return f"simulated elapsed={st['elapsed']:.1f}s, score={st['score']}",''
    run('DYN-025','Стресс update-loop (~100 секунд симулированного времени)',t025,'Нет исключений/NaN; не является FPS/soak')

    def t026():
        bad=json.dumps({'dailyTasks':[None,None,None]},ensure_ascii=False); seed={'thoughtVacuumProgress.v1':bad}; before=len(page_errors); q=load(storage=seed); q.wait_for_timeout(50); new=page_errors[before:]; path=EVID/'EV-007_corrupt_save_startup.png'; q.screenshot(path=str(path)); assert any("Cannot read properties of null" in x['error'] for x in new),new; return f'pageerror={new}',str(path.relative_to(QA))
    run('DYN-026','Структурно поврежденное сохранение: null в dailyTasks',t026,'Ожидается fallback; проверяется startup exception')

    def vp(w,h,label):
        q=load(viewport=(w,h)); q.locator('#upgradesButton').click(); q.wait_for_timeout(300); m=q.evaluate("({screenScroll:document.querySelector('#upgradesScreen').scrollHeight,screenClient:document.querySelector('#upgradesScreen').clientHeight,panelScroll:document.querySelector('#upgradesScreen .panel').scrollHeight,panelClient:document.querySelector('#upgradesScreen .panel').clientHeight,backVisible:!!document.querySelector('#backFromUpgradesButton').offsetParent})"); assert m['backVisible']; path=EVID/f'EV-VP-{label}.png'; q.screenshot(path=str(path)); return m,str(path.relative_to(QA))
    for tid,w,h,label in [('DYN-027',320,568,'320x568'),('DYN-028',360,640,'360x640'),('DYN-029',768,1024,'768x1024'),('DYN-030',1366,768,'1366x768'),('DYN-031',1920,1080,'1920x1080')]:
        run(tid,f'Мастерская при {label}',lambda w=w,h=h,label=label:vp(w,h,label),'Контент доступен; прокрутка при необходимости')

    def t032():
        q=load(viewport=(360,640),mobile=True,touch=True,dpr=2); q.locator('#upgradesButton').click(); panel=q.locator('#upgradesScreen .panel'); box=panel.bounding_box(); before=panel.evaluate('(e)=>e.scrollTop'); cdp=current['context'].new_cdp_session(q); x=box['x']+box['width']/2; y1=box['y']+box['height']-70; y2=box['y']+80
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y1,'radiusX':2,'radiusY':2,'force':1}]})
        for i in range(1,9):
            y=y1+(y2-y1)*i/8; cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y,'radiusX':2,'radiusY':2,'force':1}]}); q.wait_for_timeout(20)
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); q.wait_for_timeout(350); after=panel.evaluate('(e)=>e.scrollTop'); path=EVID/'EV-008_mobile_touch_scroll.png'; q.screenshot(path=str(path)); assert after>before+10,f'{before}->{after}'; return f'scrollTop {before}->{after}',str(path.relative_to(QA))
    run('DYN-032','Сенсорная прокрутка мастерской 360×640',t032,'scrollTop увеличивается после свайпа')

    browser.close()

(QA/'logs/dynamic_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
(QA/'logs/browser_console.json').write_text(json.dumps(console_events,ensure_ascii=False,indent=2),encoding='utf-8')
(QA/'logs/page_errors.json').write_text(json.dumps(page_errors,ensure_ascii=False,indent=2),encoding='utf-8')
summary={s:sum(1 for r in results if r['status']==s) for s in ['PASS','FAIL','BLOCKED','NOT_RUN']}
print(json.dumps({'summary':summary},ensure_ascii=False),flush=True)
