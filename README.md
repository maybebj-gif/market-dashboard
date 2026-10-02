# 觀察指標儀表板

一頁看完常用的外部指標。電腦上卡片左右並排，手機上上下排列。

網址：https://maybebj-gif.github.io/market-dashboard/

| 卡片 | 資料來源 | 做法 | 更新頻率 |
|---|---|---|---|
| FedWatch | CME | 嵌入原圖表 | 即時 |
| 財經日曆（美國・高重要性） | Investing.com（中文） | 嵌入原工具 | 即時 |
| 恐懼與貪婪 | CNN | `scripts/fetch_fng.py` | 每天 |
| Put/Call 比率 | CBOE | `scripts/fetch_putcall.py` | 每天 |
| 基金資金流 | ICI | `scripts/fetch_fundflows.py` | 每週（另存每月歷史） |
| 台灣融資餘額 | 證交所 | `scripts/fetch_margin_tw.py` | 每天 |
| 日本融資餘額 | JPX | `scripts/fetch_margin_jp.py` | 每週 |
| 嘉信 STAX | Schwab | 嵌入原圖表 | 每月 |

- 自動抓：GitHub Actions「更新指標資料」，台灣平日晚上 6:55～凌晨 0:55 每小時一次，加早上 5:55 一次
- 抓不到時保留上次資料，卡片標「尚未更新」；每個來源各自獨立，一個壞了不影響其他
- 手動更新：Actions → 「更新指標資料」→ Run workflow
- 沒放進來的：NAAIM（2026/8 起付費）、FINRA 美國融資餘額（網站擋自動抓取）、高盛／德銀／Vanda（投行付費資料）
