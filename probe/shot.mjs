import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 900 } });
await new Promise(r => setTimeout(r, 30000));  // 等 Pages 部署
await p.goto('https://maybebj-gif.github.io/market-dashboard/?v=' + Date.now()); await p.waitForTimeout(12000);
for (const id of ['cal', 'stax', 'fundflows']) await (await p.$('#' + id)).screenshot({ path: 'probe/live-' + id + '.png' });
await b.close();
