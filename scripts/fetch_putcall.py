"""CBOE 每日 Put/Call 比率 → data/putcall.json

series: [日期, 全市場 Total, 個股 Equity]
第一次跑會往回補一年；之後只補缺的交易日。
"""
import json
import time
from datetime import date, timedelta

from common import get, run

URL = "https://cdn.cboe.com/data/us/options/market_statistics/daily/{}_daily_options"
DAYS = 365


def one_day(d):
    j = json.loads(get(URL.format(d.isoformat()), {"Accept": "application/json"}))
    vals = {r["name"]: float(r["value"]) for r in j["ratios"]}
    return [d.isoformat(), vals["TOTAL PUT/CALL RATIO"], vals["EQUITY PUT/CALL RATIO"]]


def update(old):
    have = {row[0] for row in old.get("series", [])}
    series = list(old.get("series", []))
    today = date.today()
    d, misses = today, 0
    while d > today - timedelta(days=DAYS):
        if d.weekday() < 5 and d.isoformat() not in have:
            try:
                series.append(one_day(d))
                time.sleep(0.2)
            except Exception:  # 假日或還沒公布
                misses += 1
        d -= timedelta(days=1)
    if not series:
        raise RuntimeError("一天都沒抓到")
    series.sort()
    return {"source": "cboe", "series": series[-260:]}


if __name__ == "__main__":
    run("putcall.json", update)
