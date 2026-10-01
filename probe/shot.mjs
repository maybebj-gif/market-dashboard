import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 800 } });
await p.goto('http://localhost:8000/probe/widget.html'); await p.waitForTimeout(8000);
await p.screenshot({ path: 'probe/widget.png', fullPage: true });
const p2 = await b.newPage({ viewport: { width: 390, height: 900 } });
await p2.goto('https://maybebj-gif.github.io/market-dashboard/'); await p2.waitForTimeout(8000);
await p2.screenshot({ path: 'probe/site.png', fullPage: true });
await b.close();
