# 觀察指標儀表板

一頁看完常用的外部指標。電腦上卡片左右並排，手機上上下排列。

| 卡片 | 資料來源 | 更新方式 |
|---|---|---|
| 恐懼與貪婪指數 | CNN Fear & Greed | GitHub Actions 平日每天抓兩次，存進 `data/fng.json`；抓不到就保留上次數字並標「尚未更新」 |
| FedWatch | CME FedWatch | 直接嵌入 CME 的原圖表；嵌不進來就看 `img/` 的截圖 |

- 手動更新資料：Actions → 「更新指標資料」→ Run workflow
- 新增指標：在 `index.html` 加一張 `<section class="card">`
