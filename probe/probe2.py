import re, urllib.request
H = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
     "Accept": "text/html", "Accept-Language": "zh-TW,zh;q=0.9", "Referer": "https://maybebj-gif.github.io/"}
base = "https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=3&features=datepicker,timezone&countries=5&calType=day&timeZone=8&lang={}"
for lang in [1, 6, 46, 55]:
    print("\n#### lang", lang)
    try:
        with urllib.request.urlopen(urllib.request.Request(base.format(lang), headers=H), timeout=30) as r:
            b = r.read().decode("utf-8", "replace"); print("STATUS", r.status, len(b), "XFO", r.headers.get("x-frame-options"), "CSP", (r.headers.get("content-security-policy") or "")[:200])
    except Exception as e:
        print("ERR", e); continue
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", b, flags=re.S)))
    print("TEXT", t[:700])
    opts = re.findall(r'<option[^>]*value="(\d+)"[^>]*>([^<]+)</option>', b)
    print("TZ", [o for o in opts if "+8" in o[1] or "+08" in o[1] or "Taipei" in o[1] or "台北" in o[1] or "北京" in o[1]][:10], len(opts))
    if lang == 46: print("LINKS", re.findall(r'href="([^"]+)"', b)[:15])
