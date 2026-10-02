import { chromium } from 'playwright';
const b = await chromium.launch();
for (const lang of ['46', '6']) {
  const p = await b.newPage({ viewport: { width: 390, height: 900 }, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  await p.goto('http://localhost:8000/probe/widget.html#' + lang); await p.waitForTimeout(10000);
  await p.screenshot({ path: 'probe/inv-' + lang + '.png' });
}
await b.close();
