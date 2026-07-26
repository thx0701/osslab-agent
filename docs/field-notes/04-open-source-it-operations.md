# 04 · 自架平台與 IT 維護：把既有服務接成可長期維護的底座

osslab-agent 的技術方向不是從零發明每一層，而是把成熟元件放在正確的位置，再把登入、權限、升級與人工接手接好。這套底座從外到內依序處理公開服務的保護、企業身分、內網連線、開發紀錄、業務資料、密碼與 AI 執行。開源讓我們能掌握部署與資料邊界；但開源不是「裝完就不用管」，設定、版本、帳號與上游更新仍要持續維護。

## 先讓身分與網路有秩序

```text
同事的 Lark 企業帳號
          ↓
Authentik：統一身分驗證與 SSO 中心
   ├── Cloudflare Access：指定公開 Web 服務的外層保護
   ├── NetBird：VPN 與內網存取
   ├── RustDesk、Termix：IT 維護服務
   └── 其他核准納入的自架系統
```

| 元件 | 在我們架構中的角色 |
| --- | --- |
| **[Authentik](https://github.com/goauthentik/authentik)** | 統一的身分驗證與 SSO 中心。它把 Lark 企業帳號轉成標準 OIDC 身分，讓自架系統不用各自維護一套人員帳密。 |
| **[Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/)** | 在指定公開 Web 服務的最外層先做身分驗證與存取政策，再把請求送到服務本體。它不是取代應用程式登入，而是額外的一道 SSO 保護與稽核邊界。客戶入口、webhook 或身分中心本身不會硬塞進這一層。 |
| **[NetBird](https://github.com/netbirdio/netbird)** | VPN 與內網存取層。使用者經 SSO 登入後取得受控的內網連線，而不是靠共用 VPN 帳密或把管理埠直接開到網際網路。這也是遠端維護登入體驗能保持順暢的關鍵。 |

## 開發、AI 與業務系統

| 元件 | 在我們架構中的角色 |
| --- | --- |
| **[Forgejo](https://forgejo.org/)** | 自架 Git 平台。程式、部署設定、文件與操作／開發紀錄都以 repository、commit、branch、PR 的方式留下可追溯變更；它不是只拿來放原始碼。 |
| **AI Agent Server** | 一台專用 server 承載每位同事的專屬 agent。每個 agent 的 session、browser profile、bot identity、project context 與能力設定都可不同，避免資料和登入狀態串在一起。 |
| **[cc-connect](https://github.com/chenhg5/cc-connect)** | AI agent 的跨訊息通道：把 Lark 事件路由到對應同事的專屬 agent，再回傳進度與人工介入請求；對同事不會另外露出第二個聊天 UI。 |
| **[lark-cli](https://github.com/larksuite/cli)** | Lark 官方維護、為人員與 AI agent 設計的 CLI。agent 透過它以受控權限操作 Messenger、Docs、Base、Sheets、Mail、Tasks 等 Lark 工作面，再由 cc-connect 把任務與結果接回對的對話脈絡。 |
| **[Odoo 18 Community Edition](https://github.com/odoo/odoo)** | **選配 ERP connector**。日常表單與流程可先由 Lark Base／Forms 承接；只有需要完整 ERP 控管時才接入 Odoo CE。現有客製以社群版加自有 addons 持續調整，AI 可協助高頻率改碼、測試與驗證，因此不把企業版授權當成改流程的必要前提。 |

## 密碼與遠端維護

| 範圍 | 元件 | 在整體中的位置 |
| --- | --- | --- |
| agent runtime | Codex、Grok 等訂閱制 code agent build | 只採訂閱制，避免純 API 用量成本；不採 OpenClaw 或 Hermes 架構。 |
| 真實網站操作 | [OSSLab-agent 修改版 KasmVNC Chrome](../../docker/chrome/README.md)、CDP、Playwright | 以 Kasm Chrome 為 base 的修改版，含繁中輸入、CDP relay 與 Bitwarden policy。每位同事／agent 有自己的 profile，真人可接手同一個瀏覽器工作階段。 |
| 密碼管理 | [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | 同事先在自己的 KasmVNC Chrome 解鎖 Vaultwarden，專屬 agent 才能在該 session 使用登入資料，永遠不取得主密碼；服務秘密另以受限 API／CLI helper 讀取。 |
| 遠端維護 | [lejianwen/rustdesk-server](https://github.com/lejianwen/rustdesk-server) | 自架 RustDesk server／API，處理 IT 遠端維護與短期分享需求。 |
| SSH／遠端桌面維護 | [Termix](https://github.com/Termix-SSH/Termix) | 自架的 SSH 與遠端桌面管理入口，供主機維護與連線管理使用。 |

前兩項不是都屬於開源軟體：訂閱制 code agent 是刻意保留的外部 runtime；其餘元件則提供可以自架、檢視、更新與替換的技術底座。這種組合比把所有責任壓在單一 SaaS 或單一自研框架更務實。

## RustDesk 與 Termix 已經納入 SSO

IT 維護是最不適合帳密四散的場景，所以兩個服務都已接到同一條企業登入路徑：

```text
Lark 企業帳號 → Authentik / OIDC → RustDesk、Termix
```

RustDesk 用於電腦與工作站的遠端支援；需要對外協助時，分享應設有效期，而不是把永久密碼當作維護流程。Termix 則把 SSH 與遠端桌面管理集中成可控的入口。兩者使用同一個企業身分，並不表示所有人都能管理所有主機：系統內仍依管理角色、可見資產與連線權限做限制。需要更敏感的內網管理時，再透過 NetBird 進入受控網路，而不是擴大公開入口。

## 維護比選型更重要

我們把部署設定與必要的客製放進版控，跟上游專案分開看待。上游升級時先看 release 與安全變更、在隔離環境驗證登入與既有流程，再安排更新；不把 profile、cookie、金鑰、資料庫或分享 token 放進公開 repository。

同一個原則也適用於 agent：容器和 session 必須依 bot／工作流隔離；真人登入後的狀態不應被另一個 bot 共用；需要權限或人工判斷時，讓人接手，而不是把秘密硬寫進設定檔。這才是自架系統能長期運作的方式。

回到系列首頁：[〈osslab-agent 的實際工作筆記〉](README.md)
