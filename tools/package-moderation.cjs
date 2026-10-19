// Runtime-only archive. Promo media are uploaded separately in the console.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const JSZip = require('jszip');
const root = path.resolve(__dirname, '..');
const files = ['index.html', 'style.css', 'game.js', 'assets/vacuum_player.png'];
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
async function build() {
  const zip = new JSZip();
  for (const name of files) zip.file(name, fs.readFileSync(path.join(root, name)), {
    date: new Date(2000, 0, 1, 0, 0, 0), createFolders: false
  });
  return zip.generateAsync({type:'nodebuffer',compression:'DEFLATE',compressionOptions:{level:9},platform:'DOS'});
}
(async () => {
  const bytes = await build();
  if (!bytes.equals(await build())) throw new Error('Non-identical rebuild');
  const extracted = await JSZip.loadAsync(bytes, {checkCRC32:true});
  if (JSON.stringify(Object.keys(extracted.files)) !== JSON.stringify(files)) throw new Error('Unexpected archive files');
  for (const name of files) if (!(await extracted.file(name).async('nodebuffer')).equals(fs.readFileSync(path.join(root,name)))) throw new Error(`Mismatch: ${name}`);
  const name = 'Пылесос_Пыслей_финальный_релиз_2026-09-18.zip';
  fs.writeFileSync(path.join(root,'release',name),bytes);
  const manifest = {archive:name,bytes:bytes.length,sha256:sha(bytes),files:files.map(name=>({name,sha256:sha(fs.readFileSync(path.join(root,name)))}))};
  fs.writeFileSync(path.join(root,'release','Манифест_финальный_релиз_2026-09-18.json'),JSON.stringify(manifest,null,2)+'\n');
  console.log(JSON.stringify(manifest,null,2));
})().catch(error=>{console.error(error);process.exitCode=1;});
