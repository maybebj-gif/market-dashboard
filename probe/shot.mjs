import { chromium } from 'playwright';
const b = await chromium.launch();
const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36' });
const p = await ctx.newPage();
try {
  const r = await p.goto('https://www.finra.org/rules-guidance/key-topics/margin-accounts/margin-statistics', { timeout: 60000 });
  await p.waitForTimeout(5000);
  console.log('FINRA status', r.status(), await p.title());
  const links = await p.$$eval('a', as => as.map(a => a.href).filter(h => /xlsx?|csv/i.test(h)));
  console.log('FINRA links', links.slice(0, 10));
  const t = await p.evaluate(() => document.body.innerText);
  const i = t.indexOf('Debit'); console.log('FINRA text', t.slice(Math.max(0, i - 300), i + 1500));
} catch (e) { console.log('FINRA ERR', e.message); }
try {
  const p3 = await ctx.newPage();
  await p3.goto('https://www.schwab.com/investment-research/stax', { timeout: 60000 }); await p3.waitForTimeout(4000);
  const links = await p3.$$eval('a', as => as.map(a => [a.innerText.trim(), a.href]).filter(([t, h]) => /stax/i.test(t + h)));
  console.log('STAX links', JSON.stringify(links.slice(0, 15)));
} catch (e) { console.log('STAX ERR', e.message); }
const p2 = await b.newPage({ viewport: { width: 390, height: 900 } });
await p2.goto('https://maybebj-gif.github.io/market-dashboard/'); await p2.waitForTimeout(8000);
await p2.screenshot({ path: 'probe/site.png', fullPage: true });
await b.close();
