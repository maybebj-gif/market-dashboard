"""台灣證交所 上市融資餘額（金額）→ data/margin_tw.json

series: [日期, 融資餘額(億元)]
證交所說當日餘額晚上公布、隔天還會微調，所以每次都重抓最近 5 天。
"""
import json
import time
from datetime import date, timedelta

from common import get, run

URL = "https://www.twse.com.tw/rwd/zh/marginTrading/MI_MARGN?date={}&selectType=MS&response=json"
BACKFILL_DAYS = 120


def one_day(d):
    j = json.loads(get(URL.format(d.strftime("%Y%m%d")), {"Accept": "application/json"}, timeout=15))
    if j.get("stat") != "OK":
        return None
    for row in j["tables"][0]["data"]:
        if row[0].startswith("融資金額"):
            return [d.isoformat(), round(int(row[5].replace(",", "")) / 1e5, 1)]  # 仟元 → 億元
    return None


def update(old):
    rows = {r[0]: r for r in old.get("series", [])}
    today = date.today()
    span = 7 if rows else BACKFILL_DAYS
    d, fails = today, 0
    while d > today - timedelta(days=span):
        if d.weekday() < 5 and (d.isoformat() not in rows or (today - d).days <= 5):
            try:
                r = one_day(d)
                fails = 0
            except Exception as e:
                fails += 1
                print(f"  {d} 失敗：{e}", flush=True)
                if fails >= 3:  # 連續失敗多半是被擋了，先停，下次再補
                    break
                r = None
            if r:
                rows[r[0]] = r
            time.sleep(3)  # 證交所會擋太快的請求
        d -= timedelta(days=1)
    if not rows:
        raise RuntimeError("一天都沒抓到")
    return {"source": "twse", "unit": "億元", "series": sorted(rows.values())[-260:]}


if __name__ == "__main__":
    run("margin_tw.json", update)
