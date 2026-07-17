from pathlib import Path
import json
from playwright.sync_api import sync_playwright
QA=Path('/mnt/data/QA'); ROOT=QA/'work/runtime'; E=QA/'evidence'
INDEX=(ROOT/'index.html').read_text(encoding='utf-8-sig'); CSS=(ROOT/'style.css').read_text(); DATA=(ROOT/'assets/vacuum_player_data.js').read_text(); GAME=(ROOT/'game.js').read_text().replace('new URL("assets/vacuum_player.png", window.location.href).href','"https://qa.local/assets/vacuum_player.png"')
def html():
 mock='''<script>const __store={};Object.defineProperty(window,'localStorage',{value:{setItem:(k,v)=>__store[k]=String(v),getItem:(k)=>Object.prototype.hasOwnProperty.call(__store,k)?__store[k]:null,removeItem:(k)=>delete __store[k],clear:()=>{for(const k of Object.keys(__store))delete __store[k]}},configurable:true});</script>'''
 return INDEX.replace('<link rel="stylesheet" href="style.css">',f'<style>{CSS}</style>').replace('<script src="/sdk.js"></script>','').replace('<script src="assets/vacuum_player_data.js"></script>',f'<script>{DATA}</script>').replace('<script src="game.js"></script>',mock+f'<script>{GAME}</script>')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 q=b.new_page(viewport={'width':1024,'height':768},locale='ru-RU'); q.set_content(html(),wait_until='load'); q.wait_for_timeout(150)
 q.locator('#playButton').click(); q.evaluate("game.score=100;game.lives=1;game.running=true;collectThought({type:'bad',x:1,y:1})"); q.wait_for_timeout(300)
 q.screenshot(path=str(E/'BUG-002_step-01_game-over.png'))
 q.locator('#reviveAdButton').click(); q.wait_for_timeout(300)
 q.screenshot(path=str(E/'BUG-002_result_revived-without-ad.png'))
 q.evaluate("returnToMenuFromGame(); progress.boosters={magnetStart:1,shield:1,doubleStart:1};saveProgress();startGame()"); q.wait_for_timeout(300)
 q.screenshot(path=str(E/'BUG-004_step-01_boosters-active.png'))
 q.locator('#gameMenuButton').click(); q.wait_for_timeout(300)
 q.screenshot(path=str(E/'BUG-004_result_menu-no-confirmation.png'))
 b.close()
