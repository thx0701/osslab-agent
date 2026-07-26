# OSSLab-agent

> **狀態：WIP / draft.** 架構與公開安全的 Chrome 容器先公開；部署腳本與其他元件陸續整理。

一套自架的**多人 AI agent 與 SSO 協同架構**。同事只使用 **Lark Suite**：在群組、私訊、Mail、Base 與表單裡交辦工作、讀信、看進度與確認草稿；`cc-connect`、訂閱制 code agent、資料工具與隔離 Chrome 容器都在後端運作。

它不是再做一個 AI 聊天網站。Lark 是唯一的人員工作入口，也是企業身分的起點：同一個帳號經 Authentik／OIDC 延伸到 Cloudflare Access、NetBird、RustDesk、Termix 與其他核准服務。登入順暢，權限仍按服務與角色分開管理。

## 核心原則

- **多人而非共用帳號**：每位同事以自己的 Lark 身分工作；agent session、browser profile、bot identity、project context 與資料權限依角色隔離。
- **只使用 Lark Suite**：訊息、文件、部門公用信箱、email 讀取、Base、表單、審核與 bot 都留在同一個 workspace；不要求團隊改用第二套聊天 UI。
- **Base／Forms 先行**：以 Airtable 類型的多維表格、表單與 automation 快速把流程跑起來。Odoo 是需要完整 ERP 控管時才接入的選配，不是架構前提。
- **SSO 優先**：Lark → Authentik → Cloudflare Access／NetBird／維護服務，減少帳密散落與新人上手成本。
- **AI 可做事，也可停下來**：agent 產出查詢、整理與草稿；寄信、付款、刪除、改權限與例外情況保留人工確認或瀏覽器接手。

## 工作流

```text
Lark 群組／私訊／Mail／Base／Forms
                  ↓
        cc-connect + AI Agent Server
                  ↓
    Code agent runtime + 受限工具／資料
                  ↓
     隔離 Chrome、內網服務或可選 Odoo
                  ↓
       結果、草稿、審核全部回到 Lark
```

## 文件

- 完整架構：[docs/design.md](docs/design.md)
- 從實際營運出發的四篇文章：[docs/field-notes/](docs/field-notes/README.md)

| 主題 | 說明 |
| --- | --- |
| [01 · 多人 AI agent 應用](docs/field-notes/01-ai-agent-applications.md) | 同事只用 Lark，agent 如何在後端協助並讓真人接手。 |
| [02 · Lark Suite、Mail、Base 與 SSO](docs/field-notes/02-lark-suite-and-sso.md) | 為何 Lark 是唯一工作入口，以及多信箱、表單、Base 與 SSO 如何接在一起。 |
| [03 · 管理與治理](docs/field-notes/03-agent-governance.md) | 多人、多 agent 的分權、審核、留痕與資料隔離。 |
| [04 · 自架平台與 IT 維護](docs/field-notes/04-open-source-it-operations.md) | 身分、VPN、Git、密碼庫、Agent Server、Odoo 選配與維護服務如何分工。 |

## License

[MIT License](LICENSE)
