import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 520 }, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
for (const lang of [6, 55, 46, 64, 70, 71, 72, 40, 49, 52, 53, 54, 56]) {
  await p.goto('http://localhost:8000/probe/widget.html?lang=' + lang); await p.waitForTimeout(8000);
  console.log(lang, p.frames().map(f => f.url().slice(0, 60)).join(' | '));
  await p.screenshot({ path: 'probe/inv-' + lang + '.png' });
}
await b.close();
