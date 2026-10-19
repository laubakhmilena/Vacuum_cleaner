const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const { chromium, webkit } = require('playwright');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
let browser, server, origin;
before(async () => {
  const root = path.resolve(__dirname, '..');
  server = http.createServer((req, res) => {
    const file = path.join(root, new URL(req.url, 'http://localhost').pathname === '/' ? 'index.html' : new URL(req.url, 'http://localhost').pathname);
    if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) { res.writeHead(404); res.end(); return; }
    res.setHeader('Content-Type', ({'.js':'text/javascript','.css':'text/css','.html':'text/html','.png':'image/png'})[path.extname(file)] || 'application/octet-stream');
    res.end(fs.readFileSync(file));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  origin = `http://127.0.0.1:${server.address().port}`;
  browser = process.env.QA_ENGINE === 'webkit'
    ? await webkit.launch({headless:true})
    : await chromium.launch({headless:true, channel:'chrome'});
});
after(async () => { await browser?.close(); await new Promise(resolve => server?.close(resolve)); });
async function open(t, options = {}) {
  const context = await browser.newContext({locale:'en-US', ...(options.viewport ? {viewport:options.viewport,hasTouch:true,isMobile:true} : {})});
  t.after(() => context.close());
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  t.after(() => assert.deepEqual(errors, [], 'No uncaught production errors'));
  await page.addInitScript(opts => {
    window.testEvents = []; window.sdkHandlers = {};
    window.addEventListener('unhandledrejection', e => window.testEvents.push({rejection:String(e.reason)}));
    window.testSdk = {
      environment:{i18n:{lang:opts.lang || 'ru'}},
      on:(name, cb) => {window.sdkHandlers[name] = cb;},
      features:{
        LoadingAPI:{ready:() => window.testEvents.push({ready:true, lang:document.documentElement.lang,
          title:document.getElementById('menuTitle').textContent, inert:document.body.inert,
          visible:getComputedStyle(document.querySelector('.ui-shell')).visibility,
          image:document.getElementById('vacuumPreload').complete,
          stars:document.getElementById('starsCount').textContent})},
        GameplayAPI:{start:() => window.testEvents.push('start'),stop:() => window.testEvents.push('stop')}
      },
      adv:{showRewardedVideo:({callbacks}) => {window.rewardCallbacks=callbacks;},
        showFullscreenAdv:({callbacks}) => {window.fullCallbacks=callbacks;}}
    };
    if(opts.cloud) window.testSdk.getPlayer = async () => ({getData:() => new Promise(r => window.releaseCloud=r),setData:async()=>{}});
    if(opts.missingMethods) window.testSdk = {environment:{i18n:{lang:'en'}}};
    if(opts.readyThrows) window.testSdk.features.LoadingAPI.ready=()=>{window.readyAttempts=(window.readyAttempts||0)+1;throw new Error('ready unavailable');};
    if(opts.storageBlocked) {Storage.prototype.getItem=()=>{throw new Error('denied');};Storage.prototype.setItem=()=>{throw new Error('denied');};Storage.prototype.removeItem=()=>{throw new Error('denied');};}
    if(!opts.missing) window.YaGames={init:() => {
      if(opts.throw) throw new Error('SDK failure');
      if(opts.reject) return Promise.reject(new Error('SDK failure'));
      if(opts.delay) return new Promise(r => window.releaseSdk=()=>r(window.testSdk));
      return Promise.resolve(window.testSdk);
    }};
    if(opts.corrupt) localStorage.setItem('thoughtVacuumProgress.v1', opts.corrupt);
  }, options);
  await page.route('**/sdk.js', route => route.fulfill({contentType:'text/javascript',body:''}));
  if(options.imageDelay) await page.route('**/assets/vacuum_player.png', async route => {
    await new Promise(r => setTimeout(r, 5500)); await route.continue();
  });
  if(options.imageError) await page.route('**/assets/vacuum_player.png', route => route.abort());
  await page.goto(origin, {waitUntil:'domcontentloaded'});
  return page;
}
async function usable(page) {
  await page.waitForFunction(() => !document.body.inert && getComputedStyle(document.querySelector('.ui-shell')).visibility === 'visible');
}
async function result(page) {
  await page.click('#playButton');
  await page.evaluate(() => { for(let i=0;i<12;i++) collectThought({type:'good',x:100,y:100}); endGame(); });
}
for (const lang of ['ru','en']) test(`mobile bounds and static menu: ${lang}`,async t=>{
  const page=await open(t,{lang,viewport:{width:390,height:510}});await usable(page);
  const sizes=[[320,430],[360,480],[390,510],[412,600],[700,272],[812,320],[568,240],[768,1024],[1366,768]];
  for(const [width,height] of sizes){
    await page.setViewportSize({width,height});
    for(const saved of [false,true]){
      if(saved){await page.evaluate(()=>{startGame();returnToMenuFromGame();});}
      await page.waitForTimeout(260);
      const bounds=await page.evaluate(()=>{
        const panel=document.querySelector('#menuScreen .panel'), p=panel.getBoundingClientRect();
        return {scroll:panel.scrollHeight>panel.clientHeight+1,items:[...panel.querySelectorAll('h1,.lead,.best-row,.daily-card,button')].filter(e=>e.getClientRects().length).map(e=>{const r=e.getBoundingClientRect();return {id:e.id||e.className,x:r.x,y:r.y,right:r.right,bottom:r.bottom,pBottom:p.bottom};})};
      });
      assert.equal(bounds.scroll,false,`${width}x${height} menu must not clip content`);
      for(const r of bounds.items) assert.ok(r.x>=-1&&r.y>=-1&&r.right<=width+1&&r.bottom<=height+1&&r.bottom<=r.pBottom+1,`${width}x${height} ${JSON.stringify(r)}`);
    }
    if(lang==='ru'&&[320,700].includes(width)) await page.screenshot({path:`screenshots/menu-mobile-${width}x${height}.png`});
    await page.click('#upgradesButton');await page.waitForTimeout(250);
    await page.locator('#backFromUpgradesButton').scrollIntoViewIfNeeded();
    const back=await page.locator('#backFromUpgradesButton').boundingBox();assert.ok(back.y>=0&&back.y+back.height<=height+1);
    await page.click('#backFromUpgradesButton');await page.click('#playButton');
    await page.evaluate(()=>{game.magnetTimer=6;updateHud();});
    const overlap=await page.evaluate(()=>{const a=document.querySelector('.hud').getBoundingClientRect(),b=document.querySelector('#bonusPill').getBoundingClientRect();return b.top<a.bottom;});
    assert.equal(overlap,false,`${width}x${height} bonus overlaps HUD`);
    await page.evaluate(()=>{endGame();});await page.waitForTimeout(250);
    for(const id of ['reviveAdButton','restartButton','menuButton']){
      await page.locator('#'+id).scrollIntoViewIfNeeded();const r=await page.locator('#'+id).boundingBox();
      assert.ok(r.x>=0&&r.y>=0&&r.x+r.width<=width+1&&r.y+r.height<=height+1,`Result ${id} ${width}x${height}`);
    }
    await page.locator('#menuButton').scrollIntoViewIfNeeded();await page.click('#menuButton');
  }
});
test('safe area, reset dialog and native mobile store pan',async t=>{
  const page=await open(t,{viewport:{width:390,height:510}});await usable(page);
  await page.evaluate(()=>{const s=document.documentElement.style;s.setProperty('--safe-top','44px');s.setProperty('--safe-bottom','34px');s.setProperty('--safe-left','24px');});
  await page.waitForTimeout(300);
  const r=await page.locator('#menuScreen .panel').boundingBox();assert.ok(r.y>=44&&r.y+r.height<=476);
  await page.click('#upgradesButton');await page.waitForTimeout(300);
  const panel=page.locator('#upgradesScreen .panel');
  assert.equal(await panel.evaluate(e=>e.scrollTop),0);
  const cdp=await page.context().newCDPSession(page);
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:195,y:350}]});
  for(let y=330;y>=100;y-=20){await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:195,y}]});await page.waitForTimeout(16);}
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  await page.waitForTimeout(300);
  assert.ok(await panel.evaluate(e=>e.scrollTop>0),'native touch must scroll shop');
  await page.locator('#resetProgressButton').scrollIntoViewIfNeeded();await page.click('#resetProgressButton');
  for(const id of ['resetCancelButton','resetConfirmButton']){await page.locator('#'+id).scrollIntoViewIfNeeded();const b=await page.locator('#'+id).boundingBox();assert.ok(b.x>=0&&b.y>=0&&b.x+b.width<=390&&b.y+b.height<=510);}
});
for (const lang of ['ru','en']) test(`startup: SDK ${lang} is applied before access and ready`, async t => {
  const page = await open(t,{lang,delay:true});
  assert.equal(await page.evaluate(() => document.body.inert), true);
  assert.equal(await page.evaluate(() => getComputedStyle(document.getElementById('menuScreen')).visibility), 'hidden');
  await page.evaluate(() => document.getElementById('playButton').click());
  assert.equal(await page.evaluate(() => game), null);
  assert.deepEqual(await page.evaluate(() => testEvents), []);
  await page.evaluate(() => releaseSdk()); await usable(page);
  await page.waitForFunction(() => testEvents.some(e=>e.ready));
  const events = await page.evaluate(() => testEvents.filter(e=>e.ready));
  assert.equal(events.length,1); assert.equal(events[0].lang,lang);
  assert.equal(events[0].title,lang==='ru'?'Пылесос Пыслей':'Thought Vacuum');
  assert.equal(events[0].inert,true); assert.equal(events[0].visible,'hidden'); assert.equal(events[0].image,true);
});
test('Game Ready is emitted before the first user-visible frame is released', async t => {
  const page = await open(t, {lang:'ru'});
  await usable(page);
  const ready = await page.evaluate(() => testEvents.find(event => event.ready));
  assert.ok(ready, 'LoadingAPI.ready must be called');
  assert.equal(ready.inert, true);
  assert.equal(ready.visible, 'hidden');
  assert.equal(await page.evaluate(() => document.body.inert), false);
  assert.equal(await page.evaluate(() => getComputedStyle(document.getElementById('menuScreen')).visibility), 'visible');
});
test('startup: pending asset cannot become ready merely after five seconds', async t => {
  const page=await open(t,{imageDelay:true});
  await new Promise(r=>setTimeout(r,5100));
  assert.equal(await page.evaluate(()=>testEvents.filter(e=>e.ready).length),0);
  assert.equal(await page.evaluate(()=>document.body.inert),true);
  await usable(page); await page.waitForFunction(()=>testEvents.some(e=>e.ready));
});
test('startup: cloud progress is settled before access and ready', async t => {
  const page=await open(t,{cloud:true});
  await page.waitForFunction(()=>typeof releaseCloud==='function');
  assert.equal(await page.evaluate(()=>document.body.inert),true);
  assert.equal(await page.evaluate(()=>testEvents.filter(e=>e.ready).length),0);
  await page.evaluate(()=>releaseCloud({})); await usable(page);
});
for (const opts of [{missing:true},{reject:true},{throw:true},{missingMethods:true},{imageError:true}]) test(`startup fallback ${JSON.stringify(opts)}`,async t=>{
  const page=await open(t,opts); await usable(page); await page.click('#playButton');
  assert.equal(await page.evaluate(()=>game.running),true);
  assert.equal(await page.evaluate(()=>testEvents.some(e=>e.rejection)),false);
});
test('ready once across play, result, restart, menu, continue and new document',async t=>{
  const page=await open(t); await usable(page); await result(page);
  await page.click('#restartButton'); await page.click('#gameMenuButton'); await page.click('#continueButton');
  await page.evaluate(()=>endGame()); await page.click('#menuButton');
  assert.equal(await page.evaluate(()=>testEvents.filter(e=>e.ready).length),1);
  await page.reload(); await usable(page);
  assert.equal(await page.evaluate(()=>testEvents.filter(e=>e.ready).length),1);
});
test('regression: active save reload, lifecycle and result do not duplicate progress',async t=>{
  const page=await open(t); await usable(page); await page.click('#playButton');
  for(const reason of ['blur','visibility','sdk','pagehide']) {
    await page.evaluate(reason=>{
      collectThought({type:'good',x:100,y:100});
      if(reason==='blur') window.dispatchEvent(new Event('blur'));
      if(reason==='visibility') {Object.defineProperty(document,'hidden',{configurable:true,value:true}); document.dispatchEvent(new Event('visibilitychange'));}
      if(reason==='sdk') sdkHandlers.game_api_pause();
      if(reason==='pagehide') window.dispatchEvent(new Event('pagehide'));
    },reason);
    const state=await page.evaluate(()=>({score:game.score,saved:JSON.parse(localStorage.getItem('thoughtVacuumActive.v1'))}));
    assert.equal(state.saved.score,state.score); assert.ok(state.saved.revision>=1);
    await page.reload(); await usable(page); assert.equal(await page.evaluate(()=>currentScreen),'menu');
    await page.click('#continueButton'); assert.equal(await page.evaluate(()=>game.score),state.score);
  }
  await page.evaluate(()=>{endGame();endGame();});
  const meta=await page.evaluate(()=>localStorage.getItem('thoughtVacuumProgress.v1'));
  assert.equal(await page.evaluate(()=>localStorage.getItem('thoughtVacuumActive.v1')),null);
  await page.reload(); await usable(page);
  assert.equal(await page.evaluate(()=>localStorage.getItem('thoughtVacuumProgress.v1')),meta);
});
for(const order of ['reward','close','error','missing']) test(`regression: rewarded ${order}`,async t=>{
  const page=await open(t,{missing:order==='missing'}); await usable(page); await result(page);
  const stars=await page.evaluate(()=>progress.stars);
  await page.click('#doubleStarsAdButton');
  if(order!=='missing') await page.evaluate(order=>{
    const cb=rewardCallbacks;
    if(order==='reward'){cb.onRewarded();cb.onRewarded();cb.onClose();cb.onClose();}
    if(order==='close'){cb.onClose();cb.onRewarded();cb.onClose();}
    if(order==='error'){cb.onError();cb.onRewarded();}
  },order);
  assert.equal(await page.evaluate(()=>progress.stars),order==='reward'?stars*2:stars);
});
test('reward callback must not revive a different, newly started round',async t=>{
  const page=await open(t); await usable(page); await result(page); await page.click('#reviveAdButton');
  await page.click('#menuButton'); await page.click('#playButton');
  await page.evaluate(()=>{rewardCallbacks.onRewarded();rewardCallbacks.onClose();});
  assert.equal(await page.evaluate(()=>game.lives),3);
  assert.equal(await page.evaluate(()=>game.revivedOnce),false);
});
test('regression: revive once, concurrent rewarded lock and fullscreen close once',async t=>{
  const page=await open(t); await usable(page); await result(page); await page.click('#reviveAdButton');
  await page.click('#doubleStarsAdButton');
  assert.equal(await page.evaluate(()=>diagnostics.rewardedRequests),1);
  await page.evaluate(()=>{rewardCallbacks.onRewarded();rewardCallbacks.onClose();rewardCallbacks.onClose();});
  assert.equal(await page.evaluate(()=>game.lives),1);
  await page.evaluate(()=>{endGame();reviveWithAd();});
  assert.equal(await page.evaluate(()=>diagnostics.rewardedRequests),1);
  await page.evaluate(()=>showFullscreenAd(()=>{window.closeCount=(window.closeCount||0)+1;}));
  await page.evaluate(()=>{fullCallbacks.onOpen();fullCallbacks.onClose();fullCallbacks.onError();});
  assert.equal(await page.evaluate(()=>closeCount),1);
});
test('regression: corrupt storage repair, menu/shop cycles, purchases and reset',async t=>{
  const page=await open(t,{corrupt:'{"stars":"Infinity","upgrades":null}'}); await usable(page);
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('thoughtVacuumProgress.v1')).stars),0);
  for(let i=0;i<20;i++){await page.click('#upgradesButton');await page.click('#backFromUpgradesButton');}
  await page.click('#dailyRewardButton');
  const stars=await page.evaluate(()=>progress.stars); assert.ok(stars>0);
  assert.equal(await page.isDisabled('#dailyRewardButton'),true);
  await page.evaluate(()=>claimDailyReward()); assert.equal(await page.evaluate(()=>progress.stars),stars);
  await page.evaluate(()=>buyUpgrade('radius'));
  assert.equal(await page.evaluate(()=>progress.upgrades.radius),1);
  assert.equal(await page.evaluate(()=>progress.stars),stars-2);
  await page.click('#upgradesButton'); await page.click('#resetProgressButton'); await page.click('#resetCancelButton');
  assert.equal(await page.evaluate(()=>progress.stars),stars-2);
  await page.click('#resetProgressButton'); await page.click('#resetConfirmButton');
  assert.equal(await page.evaluate(()=>progress.stars),0);
});
test('collected thought is absent from the snapshot written during collision',async t=>{
  const page=await open(t); await usable(page); await page.click('#playButton');
  const snapshot=await page.evaluate(()=>{
    // Production creates the object; position and RNG are deterministic collision inputs.
    const rng=Math.random;
    try {Math.random=()=>0.95;spawnThought();} finally {Math.random=rng;}
    const thought=game.thoughts.at(-1);
    thought.x=game.player.x;thought.y=game.player.y;
    thought.vx=0;thought.vy=0;
    updateGame(0);
    return JSON.parse(localStorage.getItem('thoughtVacuumActive.v1'));
  });
  assert.equal(snapshot.score,50);
  assert.equal(snapshot.thoughts.length,0);
});
test('overlapping SDK and window pause cannot resume until both are released',async t=>{
  const page=await open(t); await usable(page); await page.click('#playButton');
  await page.evaluate(()=>{sdkHandlers.game_api_pause();window.dispatchEvent(new Event('blur'));sdkHandlers.game_api_resume();});
  assert.equal(await page.evaluate(()=>game.running),false);
  await page.evaluate(()=>window.dispatchEvent(new Event('focus')));
  assert.equal(await page.evaluate(()=>game.running),true);
});
test('startup: slow SDK remains gated and eventually uses platform language',async t=>{
  const page=await open(t,{delay:true,lang:'ru'});
  await new Promise(r=>setTimeout(r,5200));
  assert.equal(await page.evaluate(()=>document.body.inert),true);
  assert.equal(await page.evaluate(()=>testEvents.filter(e=>e.ready).length),0);
  await page.evaluate(()=>releaseSdk());await usable(page);
  assert.equal(await page.evaluate(()=>document.documentElement.lang),'ru');
});
test('startup: throwing LoadingAPI does not crash or retry on navigation',async t=>{
  const page=await open(t,{readyThrows:true});await usable(page);
  await page.click('#playButton');await page.click('#gameMenuButton');
  assert.equal(await page.evaluate(()=>readyAttempts),1);
});
test('regression: blocked storage permits local gameplay',async t=>{
  const page=await open(t,{storageBlocked:true,missing:true});await usable(page);await result(page);
  assert.equal(await page.evaluate(()=>currentScreen),'gameOver');
});
test('regression: missing active revision is rejected without loss of meta',async t=>{
  const page=await open(t);await usable(page);await page.click('#dailyRewardButton');await page.click('#playButton');
  await page.evaluate(()=>{window.dispatchEvent(new Event('blur'));const s=JSON.parse(localStorage.getItem('thoughtVacuumActive.v1'));delete s.revision;localStorage.setItem('thoughtVacuumActive.v1',JSON.stringify(s));game=null;});
  const stars=await page.evaluate(()=>progress.stars);
  await page.reload();await usable(page);
  assert.equal(await page.evaluate(()=>currentScreen),'menu');
  assert.equal(await page.evaluate(()=>localStorage.getItem('thoughtVacuumActive.v1')),null);
  assert.equal(await page.evaluate(()=>progress.stars),stars);
});
for(const outcome of ['close','error','missing']) test(`regression: fullscreen ${outcome} restores gameplay once`,async t=>{
  const page=await open(t,{missing:outcome==='missing'});await usable(page);await page.click('#playButton');
  await page.evaluate(()=>showFullscreenAd(()=>{window.closeCount=(window.closeCount||0)+1;}));
  if(outcome!=='missing') {
    assert.equal(await page.evaluate(()=>game.running),false);
    await page.evaluate(outcome=>{if(outcome==='close')fullCallbacks.onClose();else fullCallbacks.onError();fullCallbacks.onClose();},outcome);
    assert.equal(await page.evaluate(()=>diagnostics.gameplayStartCalls),2);
  }
  assert.equal(await page.evaluate(()=>game.running),true);
  assert.equal(await page.evaluate(()=>closeCount),1);
});
test('regression: fullscreen close followed by SDK resume starts restart only after resume',async t=>{
  const page=await open(t);await usable(page);await result(page);
  await page.evaluate(()=>{showFullscreenAd(()=>startGame());sdkHandlers.game_api_pause();fullCallbacks.onClose();});
  assert.equal(await page.evaluate(()=>game.finished),false);
  assert.equal(await page.evaluate(()=>game.running),false);
  await page.evaluate(()=>sdkHandlers.game_api_resume());
  assert.equal(await page.evaluate(()=>game.running),true);
});
