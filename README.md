# osslab-agent

> **狀態：WIP / draft.** 設計文稿先公開，部署腳本與 chrome 容器 image 陸續推上。

一套自架的**訂閱制 AI agent 多入口協同作業架構**。它把 Larksuite 群組、cc web 對話、Claude Code CLI / Codex CLI 這類訂閱制 code agent 與 Chrome 容器串成同一套工作流：短任務在 Lark 裡交辦與審核，研究和知識沉澱進 cc web，需要登入真實系統時再由 Chrome 容器接手。

AI 不是按鈕、不是單一聊天視窗，而是能存在於不同 channel 的同事：能在 Lark 裡被 @，能在 cc web 裡做長研究，能依 research / dev / it 等 project context 保留整理結果，也能操作真實 Chrome 查 ERP、寫文件、reply email、遇到 captcha / 2FA 時請人類接手。

## 核心差異

osslab-agent 不是再做一套 openclaw / harmes 那種自研 agent framework；它是把**現成 CLI 訂閱方案當 agent runtime 調用**。Claude Code CLI、Codex CLI 或其他 code agent CLI 負責模型推理與工具決策，osslab-agent 負責 channel routing、session 管理、web 對話、Lark 審核、Chrome 容器與人工接手。

這樣可以直接使用訂閱制額度，大幅降低純 API 帳單壓力；即使某些 CLI 的一次性 prompt 模式（例如 `-p` 類用法）不穩定或不可用，也可以改用長 session / stdio / process bridge 的方式維持 agent 執行。

## 核心分層

- **Lark 行動層**：報價、ERP、打文件、採購、回信、通知、審核、人工介入。
- **cc web 研究與知識層**：stream 對話、圖片 / 檔案輸入、web research、比價、來源整理、關鍵結論沉澱。
- **cc web project context**：research / dev / it 等上下文分流，避免工具、文件、權限與記憶互相污染。
- **Chrome 執行層**：每個 bot / 工作流可綁定獨立 Chrome 容器（CDP + KasmVNC），登入 vault / cookie / profile 隔離。

## 為什麼這樣設計

- **Lark 適合行動，不適合全部沉澱**：IM 是事件流，適合交辦、通知、審核、稽核；長研究與知識整理應進 cc web。
- **訂閱制 AI agent 優先**：可合規使用 Claude Code CLI / Codex CLI / 各家 CLI 訂閱，降低 AI API 成本；敏感知識可逐步接本地 LLM / 私有檢索。
- **一人 N agent / N bot**：採購、客服、業務、research、dev、it 都可以分開配置，agent 數量跟人數沒綁。
- **真人可接手真瀏覽器**：AI 跑到付款、captcha、2FA、第一次登入時，人類從 KasmVNC 接手同一個 browser session，處理完 AI 接續做。

## 文件

- 完整設計：[`docs/design.md`](docs/design.md)
- 從實際營運出發的四篇說明：[`docs/field-notes/`](docs/field-notes/README.md)

## 不是只有架構圖：目前怎麼用

這個專案不把 AI agent 寫成萬能自動化的展示。實際上，agent 先在 Lark 接到可追蹤的任務；長研究與資料整理留在 cc web；需要登入、付款或送出外部訊息時，才由人類審核或接手同一個瀏覽器工作階段。

Lark Suite 也是既有團隊協作與身分入口：企業帳號經 Authentik 與 OIDC 串接自架服務，Cloudflare Access 保護指定的公開 Web 服務，NetBird 提供 SSO 連線的內網存取。除 agent 工作流外，IT 維護使用的 RustDesk 與 Termix 也已納入同一條 SSO 路徑；帳號不必在每個維護系統各自建立、各自回收。詳情與技術邊界見下列四篇文章。

| 主題 | 說明 |
| --- | --- |
| [01 · AI agent 應用](docs/field-notes/01-ai-agent-applications.md) | 從交辦、研究到真人接手，AI 如何進到真實工作流。 |
| [02 · Lark Suite 與 SSO](docs/field-notes/02-lark-suite-and-sso.md) | 為何 Lark 不只是聊天工具，而是協作、資料與身分入口。 |
| [03 · 管理與治理](docs/field-notes/03-agent-governance.md) | 如何分權、審核、留痕與避免上下文混用。 |
| [04 · 自架平台與 IT 維護](docs/field-notes/04-open-source-it-operations.md) | 身分、VPN、Git、ERP、密碼庫、Agent Server、RustDesk／Termix 如何分工。 |

## License

[MIT License](LICENSE)
