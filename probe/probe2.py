import re, json, io, urllib.request, datetime as dt
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9",
     "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Upgrade-Insecure-Requests": "1"}
def get(url, h=H):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=40) as r:
            b = r.read(); print("STATUS", r.status, r.headers.get("content-type"), len(b)); return b
    except Exception as e:
        print("ERR", type(e).__name__, str(e)[:150]); return None
def txt(b):
    t = b.decode("utf-8", "replace"); t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
for name, url in [("finra", "https://www.finra.org/rules-guidance/key-topics/margin-accounts/margin-statistics"),
                  ("finra_xlsx", "https://www.finra.org/sites/default/files/2021-03/margin-statistics.xlsx"),
                  ("ici", "https://www.ici.org/research/stats/flows"),
                  ("ici_etf", "https://www.ici.org/research/stats/etf_flows")]:
    print("\n####", name); get(url)
print("\n#### naaim detail")
b = get("https://naaim.org/programs/naaim-exposure-index/")
if b:
    t = txt(b); i = t.find("Effective August"); print(t[i-200:i+1200])
    print("NUMS", re.findall(r"\b\d{1,3}\.\d{2}\b", t)[:20])
    print("IMGS", re.findall(r'<img[^>]+src="([^"]+)"', b.decode("utf-8","replace"))[:20])
print("\n#### stax detail")
b = get("https://www.schwab.com/investment-research/stax")
if b:
    s = b.decode("utf-8", "replace"); t = txt(b)
    for m in list(re.finditer(r"STAX (?:score|reading|value|was|is|rose|fell|decreased|increased)", t))[:5]: print(" ..", t[m.start()-200:m.start()+300])
    print("IFRAMES", re.findall(r'<iframe[^>]+src="([^"]+)"', s)[:10])
    print("JSONURLS", sorted(set(re.findall(r'https?://[^"\' ]+(?:json|api)[^"\' ]*', s)))[:20])
    print("PDF", sorted(set(re.findall(r'href="([^"]+\.pdf)"', s)))[:10])
    i = t.find("View the STAX"); print("CTX", t[i:i+1500])
print("\n#### stax sub")
b = get("https://www.schwab.com/investment-research/stax/view-the-stax") 
if b:
    t = txt(b); i = t.find("STAX"); print(t[i:i+1500])
print("\n#### cboe history")
for d in ["2026-06-30", "2025-09-30"]:
    b = get(f"https://cdn.cboe.com/data/us/options/market_statistics/daily/{d}_daily_options")
    if b: j = json.loads(b); print(d, [r for r in j["ratios"] if "EQUITY" in r["name"] or "TOTAL" in r["name"]], list(j.keys()))
print("\n#### jpx xlsx")
b = get("https://www.jpx.co.jp/english/markets/statistics-equities/margin/tvdivq0000001r92-att/20260929_mtdaily.xlsx")
if b:
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(b), data_only=True)
    for ws in wb.worksheets[:2]:
        print("SHEET", ws.title, ws.max_row, ws.max_column)
        for row in ws.iter_rows(min_row=1, max_row=40, values_only=True):
            if any(c is not None for c in row): print(" ", [c for c in row if c is not None][:12])
print("\n#### jpx weekly page")
b = get("https://www.jpx.co.jp/english/markets/statistics-equities/margin/04.html")
if b: print(sorted(set(re.findall(r'href="([^"]+\.(?:xlsx?|pdf))"', b.decode("utf-8","replace"))))[:10])
