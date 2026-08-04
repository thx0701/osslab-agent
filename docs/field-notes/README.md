# OSSLab-agent 的實際工作筆記

這不是功能清單，也不是把尚未上線的構想當成現況。這些文章說明 OSSLab-agent 為什麼以 Lark Suite 作為**唯一的人員工作入口**：同事用既有企業帳號在訊息、Mail、Base 與表單中工作；訂閱制 code agent、隔離瀏覽器與各項系統工具留在後端，而人類保留審核與接手權。

| 文章 | 要回答的問題 |
| --- | --- |
| [01 · 多人 AI agent 應用](01-ai-agent-applications.md) | 同事只用 Lark，agent 如何在後端進入真實工作？ |
| [02 · Lark Suite、Mail、Base 與 SSO](02-lark-suite-and-sso.md) | 為何 Lark 是唯一工作入口，也是登入入口？ |
| [03 · 管理與治理](03-agent-governance.md) | 多個 agent 怎麼分工、授權、審核與留痕？ |
| [04 · 自架平台與 IT 維護](04-open-source-it-operations.md) | 身分、VPN、Git、密碼庫、Agent Server、Odoo 選配與維護服務怎麼組成一個可維護的底座？ |
| [05 · LarkSuite 作為 AI agent channel 的三方 review](05-larksuite-as-ai-agent-channel-review.md) | **定案**：AI agent 團隊以 LarkSuite 為 channel（Free／Basic ~$6、SSO 主因、實作已完成；三方 review） |
| [06 · 隱私脫敏 gateway 架構](06-privacy-masking-gateway.md) | 訂閱制雲端 agent 之前，客戶對話、Odoo 與 email 的個資怎麼脫敏與還原？（**已部署上線並通過驗收**：自建 sidecar；原 LiteLLM 方案未採用） |

前四篇共同說明元件、通訊架構、實際工作情境與治理邊界；第 05 篇是公開討論**定案**（Grok／GPT-5.6-Luna／Kimi；已釘成本、實作、SSO）；第 06 篇是隱私脫敏的架構紀錄：spike 前的 LiteLLM 原始設計完整保留，文末附 as-built 更新節（自建 privacy sidecar＋Codex＋CLIProxyAPI），25 項 acceptance 全數通過、已上線。
