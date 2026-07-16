# 設計總覽

設計拆成兩份，避免「要幹嘛」跟「怎麼做／怎麼防呆」糊在一起：

- [功能規格](functionality.md) — 人能完成什麼、什麼時候換入口、v1 涵蓋什麼  
- [架構規格](architecture.md) — project 怎麼切、資料正本在哪、登入與批准、browser 怎麼隔離  

建議先功能、後架構。實作時：重要動作能對回 request、branch／PR、誰批的、結果是什麼；要留下來的東西進 private Git。

## 這 repo 是什麼

公開的產品設計與之後的部署零件。OSSLab 自己跑的 Forgejo、Authentik、Lark、cc-connect、Kasm Chrome、BrowseForge 只當**參考實作**，不是規定你要長一樣。

刻意不做：再造一套 openclaw／harmes 式 framework、用 headless RPA 假裝真人 browser、把 IM 當唯一知識庫。

## 幾個叫法

| 名稱 | 意思 |
|---|---|
| Web 工作台 | 長任務用的 web 對話；實作可以長得像 cc-connect 那類 web channel |
| Project | 一個可部署單位：runtime、工作目錄、bot 身份、browser、可用工具、批准規則 |
| Runtime | 真正在跑的 code agent CLI（或相容的 process） |
| BrowserProvider | 隔離的 browser profile + CDP + 人可進的 VNC |
| Action policy | 讀取／草稿／可回滾／外發／高風險，各要不要批 |

## License

[MIT](../LICENSE)
