import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 900 }, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
const out = [];
for (let lang = 1; lang <= 60; lang++) {
  try {
    await p.goto('http://localhost:8000/probe/widget.html#' + lang); await p.waitForTimeout(3500);
    const f = p.frames().find(x => x.url().includes('investing'));
    const t = f ? (await f.evaluate(() => document.body.innerText)).replace(/\s+/g, ' ') : 'NOFRAME';
    const cjk = /[一-鿿]/.test(t);
    console.log(lang, cjk ? 'CJK' : '   ', t.slice(0, 140));
    if (cjk) {
      out.push(lang);
      const tz = await f.evaluate(() => [...document.querySelectorAll('option, li')].map(o => (o.value || '') + ':' + o.textContent.trim()).filter(s => /8:00|台北|北京|香港/.test(s)).slice(0, 8));
      console.log('   TZ', JSON.stringify(tz));
      await p.screenshot({ path: 'probe/inv-' + lang + '.png' });
    }
  } catch (e) { console.log(lang, 'ERR', e.message.slice(0, 80)); }
}
console.log('CJK langs', out);
await b.close();
