# OSSLab-agent

> **狀態：OSSLab 正在測試上線中。** 現階段先公開架構與可公開的 Chrome 容器；後續預定釋出可重放的 patch file 與安裝／部署 plan，讓人或 AI agent 都能依步驟完成安裝，而不必從零猜測環境差異。

**Lark Suite 是給企業團隊使用的 IM 與協作平台**：除了群組、私訊，也整合文件、試算表、信箱、表單、資料流程與審核，讓團隊在一個 workspace 裡溝通和做事。

OSSLab-agent 是一套自架的**多人 AI agent 與 SSO 協同架構**。同事只使用 Lark Suite：在群組、私訊、Mail、Base 與表單裡交辦工作、讀信、看進度與確認草稿；AI agent 則像虛擬同事一樣，在同一個工作流程接任務、執行、回報並等待確認。`cc-connect`、[lark-cli](https://github.com/larksuite/cli)、訂閱制 code agent、資料工具與隔離 Chrome 容器都在後端運作。

綜合 IM、Mail、文件、Base／Forms、審核、Open Platform 與企業身分這些辦公團隊真正需要的功能，**OSSLab 的結論是：Lark Suite 是最適合做 AI bot channel 的工作入口**。bot 不必另開一個聊天網站，而是能直接進入團隊原本的對話、資料、文件與審核脈絡，成為可被管理的虛擬同事。

它不是再做一個 AI 聊天網站。Lark 是唯一的人員工作入口，也是企業身分的起點：同一個帳號經 Authentik／OIDC 延伸到 Cloudflare Access、NetBird、RustDesk、Termix 與其他核准服務。登入順暢，權限仍按服務與角色分開管理。

## 核心原則

- **每位同事一個專屬 agent**：每位同事以自己的 Lark 企業帳號作為 SSO 身分，不共用人員帳密；專屬 agent 的 session、browser profile、bot identity、project context 與能力設定獨立，可依同事需求不同。
- **只使用 Lark Suite**：不論人員或 AI agent，訊息、文件、部門公用信箱、email 讀取、Base、表單、審核與 bot 都以同一個 workspace 作為協作與工作入口。Docs、Sheet、Wiki 提供類似 Google Docs／Microsoft Office 的多人文件與試算表協作；不要求團隊改用第二套聊天 UI。
- **Base／Forms 先行**：Base 是可自動化的多維表格與資料流程，而非 XLS 檔。它讓人員、agent、團隊與外圍客戶透過表單、欄位、事件、通知與審核連動；即使只是庫存、訂單或簡單出貨紀錄，也能先快速形成輕量 ERP 流程。需要完整 ERP 控管時，Odoo 才是選配。
- **企業 Mail 是身分基礎**：Lark 現行免費方案提供可自訂的商務 Email；可用自有網域建立個人與部門／功能性信箱。這些企業帳號是 SSO 的身分依據，搭配 Authentik 才能把同一個登入脈絡延伸到自架服務；實際額度與功能依 Lark 方案為準。
- **SSO 優先**：Lark → Authentik → Cloudflare Access／NetBird／維護服務，減少帳密散落與新人上手成本。
- **只採訂閱制 agent runtime**：AI Agent Server 以 cc-connect 串接多個 Codex、Grok 等訂閱制 agent build；費用遠比純 API 計價可控，因此不採 OpenClaw 或 Hermes 這類需自行承擔 API 用量的架構。
- **人先解鎖，agent 才接手**：專屬 agent 的 Chrome 使用對應同事的 Web 身分；本人先在 [OSSLab-agent 修改版 KasmVNC Chrome](docker/chrome/README.md) 解鎖 Vaultwarden，agent 才能在已解鎖的工作階段內協助操作，且永遠不取得主密碼。
- **AI 是可控的虛擬助理**：依授權，agent 可直接操作 ERP、讀取與回覆 email、上架、查訪價格，或執行其他辦公室工作流；權限也能細緻限制為查詢、整理或草稿。寄信、付款、刪除、改權限與例外情況仍可要求人工確認或由真人接手。

## 工作流

```text
Lark 群組／私訊／Mail／Base／Forms
                  ↓
  cc-connect + lark-cli + AI Agent Server
                  ↓
 Codex／Grok 等訂閱制 runtime + 受限工具／資料
                  ↓
     隔離 Chrome、內網服務或可選 Odoo
                  ↓
       結果、草稿、審核全部回到 Lark
```

實際上，agent 可整理客服信箱詢價、依 Base 表單分派需求、比較報價、查詢 Base／Odoo 的庫存與客戶狀態，或在網站操作到需要人判斷的步驟再通知接手。完整情境見[〈多人 AI agent 應用〉的工作如何落地](docs/field-notes/01-ai-agent-applications.md#工作如何落地)。

## 文件

- 從實際營運出發的四篇文章：[docs/field-notes/](docs/field-notes/README.md)

| 主題 | 說明 |
| --- | --- |
| [01 · 多人 AI agent 應用](docs/field-notes/01-ai-agent-applications.md) | 同事只用 Lark，agent 如何在後端協助並讓真人接手。 |
| [02 · Lark Suite、Mail、Base 與 SSO](docs/field-notes/02-lark-suite-and-sso.md) | 為何 Lark 是唯一工作入口，以及多信箱、表單、Base 與 SSO 如何接在一起。 |
| [03 · 管理與治理](docs/field-notes/03-agent-governance.md) | 多人、多 agent 的分權、審核、留痕與資料隔離。 |
| [04 · 自架平台與 IT 維護](docs/field-notes/04-open-source-it-operations.md) | 身分、VPN、Git、密碼庫、Agent Server、Odoo 選配與維護服務如何分工。 |

## 公開進度

OSSLab 正在測試上線；現階段的文件描述已驗證的方向與尚在整理中的部署基礎。預定把可公開的環境差異整理成 **patch file**，把前置條件、安裝順序、驗證與回復方式整理成 **plan**，讓後續的人或 AI agent 可以照同一條可追溯的路徑部署，而不是重做一次猜測與手動設定。

## License

[MIT License](LICENSE)
