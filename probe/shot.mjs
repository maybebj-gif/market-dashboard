import { chromium } from 'playwright';
const b = await chromium.launch();
for (const lang of [6, 55]) {
  const p = await b.newPage({ viewport: { width: 390, height: 640 }, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  try {
    await p.goto('http://localhost:8000/probe/widget.html?lang=' + lang, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(15000);
    await p.screenshot({ path: 'probe/inv-' + lang + '.png' });
  } catch (e) { console.log(lang, e.message.slice(0, 100)); }
  await p.close();
}
await b.close();
