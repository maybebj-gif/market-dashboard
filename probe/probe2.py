import re, io, urllib.request
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9",
     "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Upgrade-Insecure-Requests": "1"}
def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40) as r:
            b = r.read(); print("STATUS", r.status, r.headers.get("content-type"), len(b)); return b
    except Exception as e:
        print("ERR", type(e).__name__, str(e)[:150]); return None
print("#### ici xls")
b = get("https://www.ici.org/combined_flows_data_2026.xls")
if b:
    print("MAGIC", b[:8])
    try:
        import xlrd
        wb = xlrd.open_workbook(file_contents=b)
        for sh in wb.sheets()[:3]:
            print("SHEET", sh.name, sh.nrows, sh.ncols)
            for r in list(range(min(sh.nrows, 14))) + list(range(max(14, sh.nrows - 6), sh.nrows)):
                print(" ", r, [c for c in sh.row_values(r) if c != ""][:16])
    except Exception as e:
        print("XLRD ERR", e); print(b[:1500])
print("\n#### stax view")
b = get("https://www.schwab.com/investment-research/stax/view-schwab-trading-activity-index")
if b:
    s = b.decode("utf-8","replace")
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)))
    for m in list(re.finditer(r"STAX", t))[:8]: print(" ..", t[max(0,m.start()-150):m.start()+300])
    print("NUMS", re.findall(r"\b\d\.\d{2}\b", t)[:30])
    print("SCRIPT-DATA", re.findall(r'(?:stax|STAX)[^"]{0,40}"\s*:\s*"?[\d.]+', s)[:10])
    print("URLS", sorted(set(u for u in re.findall(r'https?://[^"\'\s<>]+', s) if any(k in u.lower() for k in ["stax","json","api","csv","tableau","chart"])))[:30])
    print("IFRAMES", re.findall(r'<iframe[^>]+src="([^"]+)"', s))
