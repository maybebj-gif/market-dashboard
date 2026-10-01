import re, sys, urllib.request, datetime as dt
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
      "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"}
d = (dt.date.today() - dt.timedelta(days=1))
while d.weekday() >= 5: d -= dt.timedelta(days=1)
ymd, ymd8 = d.isoformat(), d.strftime("%Y%m%d")
URLS = [
 ("cboe_cdn_json", f"https://cdn.cboe.com/data/us/options/market_statistics/daily/{ymd}_daily_options"),
 ("cboe_page", f"https://www.cboe.com/us/options/market_statistics/daily/?dt={ymd}"),
 ("naaim_page", "https://naaim.org/programs/naaim-exposure-index/"),
 ("finra_page", "https://www.finra.org/rules-guidance/key-topics/margin-accounts/margin-statistics"),
 ("ici_page", "https://www.ici.org/research/stats/flows"),
 ("ici_combined", "https://www.ici.org/research/stats/combined_flows"),
 ("stax_page", "https://www.schwab.com/investment-research/stax"),
 ("twse_margin", f"https://www.twse.com.tw/rwd/zh/marginTrading/MI_MARGN?date={ymd8}&selectType=MS&response=json"),
 ("jpx_margin", "https://www.jpx.co.jp/english/markets/statistics-equities/margin/index.html"),
 ("kofia", "https://freesis.kofia.or.kr/"),
 ("ff_week", "https://nfs.faireconomy.media/ff_calendar_thisweek.json"),
]
for name, url in URLS:
    print(f"\n######## {name}  {url}")
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=40) as r:
            body = r.read()
            print("STATUS", r.status, r.headers.get("content-type"), "CORS=", r.headers.get("access-control-allow-origin"), "len", len(body))
    except Exception as e:
        print("ERR", type(e).__name__, str(e)[:200]); continue
    t = body.decode("utf-8", "replace")
    links = sorted(set(re.findall(r'href="([^"]+\.(?:xlsx?|csv)[^"]*)"', t)))
    print("LINKS", links[:15])
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt); txt = re.sub(r"\s+", " ", txt)
    for kw in ["Exposure", "PUT/CALL", "Put/Call", "TOTAL", "Debit Balances", "STAX", "融資", "Equity", "Bond"]:
        for m in list(re.finditer(re.escape(kw), txt))[:3]:
            print(f"  [{kw}]", txt[max(0, m.start()-120):m.start()+250])
    print("HEAD", t[:600].replace("\n", " "))
