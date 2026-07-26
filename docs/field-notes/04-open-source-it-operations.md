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
| **AI Agent Server** | 一台專用的 agent server 承載多個隔離的工作角色與 session。各角色共享核准的知識與工具，但瀏覽器 profile、bot identity、project context 與工作目錄分開，避免資料和登入狀態串在一起。 |
| **[cc-connect](https://github.com/chenhg5/cc-connect)** | AI agent 的跨訊息通道：把 Lark、cc web、訂閱制 code agent 與各 project 的 session routing 接起來。它負責把任務送到對的工作角色、回傳進度與請求人工介入；它不是另一個模型框架。 |
| **[Odoo 18 Community Edition](https://github.com/odoo/odoo)** | 公司的 ERP 與業務資料主體。針對現有客製需求，以社群版加上自有 addons 持續調整；AI agent 可以協助高頻率地改碼、測試與驗證，因此我們不把企業版授權當成滿足客製流程的必要前提。 |

## 密碼與遠端維護

| 範圍 | 元件 | 在整體中的位置 |
| --- | --- | --- |
| agent runtime | Claude Code CLI、Codex CLI 等訂閱制 code agent | 負責推理、規劃與工具決策；這一層可替換，並非自行重寫模型框架。 |
| 真實網站操作 | Chrome 容器、CDP、Playwright、KasmVNC | 提供隔離的登入狀態；真人可接手與 agent 同一個瀏覽器工作階段。 |
| 密碼管理 | [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | 人類直接使用瀏覽器／桌面密碼管理外掛；AI 則以各自的帳號與 API／CLI helper，在執行時讀取自己 collection 中被白名單允許的秘密欄位。AI 不共用 human vault，也不能瀏覽整座密碼庫。 |
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
