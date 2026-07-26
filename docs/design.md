# OSSLab-agent — Lark-first 的多人 AI agent 與 SSO 架構

> [!NOTE]
> **OSSLab-agent 的人員工作入口只有 Lark Suite。**
> 同事不需要在另一個 AI 網頁、另一組信箱或另一套帳密之間切換：在 Lark 群組、私訊、信箱、Base 與表單裡交辦工作；agent 在後端執行研究、讀取核准範圍內的資料、產出草稿，必要時再由真人接手瀏覽器。登入自架服務時，則以同一個 Lark 企業帳號走 SSO。

**Lark Suite 是企業團隊使用的 IM 與協作平台**：它不只有群組與私訊，還有文件、試算表、信箱、表單、資料流程與審核。OSSLab-agent 讓 AI agent 進入這個既有的協作環境，像虛擬同事一樣接任務、執行、回報與等待確認，而不是另開一個孤立的 AI 聊天網站。

這個 repo 是公開的架構與部署基礎，不公開主機、帳號、secret、瀏覽器 profile、cookie 或業務資料。OSSLab 正在測試上線中；後續會將可公開的環境差異整理為 patch file，並釋出有前置條件、安裝、驗證與回復步驟的 plan，讓人或 AI agent 都能沿著同一個可重放流程部署。

# 1. 要解決的不是「AI 不夠多」，而是多人工作不能各自為政

團隊每天都在群組、信箱、表單、文件、庫存、客戶與維護系統之間切換。傳統做法常是每個系統一組帳密、每個人一套收件匣、每個 agent 一個獨立聊天 UI；新同事要學很多入口，離職或權限異動也難以收回。

OSSLab-agent 的判斷很直接：**把人留在一個已經每天使用的 Lark Suite workspace，把複雜性留在後端。**

- 每位同事以自己的 Lark 企業帳號工作，這也是 SSO 身分；不共用人員帳密。
- **每位同事都有自己的專屬 agent**。agent session、browser profile、bot identity、project context 與可用工具分開；同事 A、B 的 agent 可以有完全不同的能力與工作範圍，也不會互相污染。
- Lark 是唯一的人員入口；`cc-connect`、訂閱制 code agent、MCP、瀏覽器與內網服務都在後端協作。
- 同一份企業身分可延伸到 Cloudflare Access、NetBird、RustDesk、Termix 與其他核准服務，讓登入體驗一致又容易回收。

# 2. 為什麼只使用 Lark Suite

這不是因為 Lark 只有聊天，而是它把多人協作需要的工作面放在一起：群組與私訊、Docs、Sheet、Base、Forms、Calendar、Approval、Mail 與 Open Platform。Docs、Sheet 與 Wiki 提供類似 Google Docs／Microsoft Office 的線上文件、試算表與知識協作；對同事而言，不必另外安裝一個「AI 工作台」；對 agent 而言，則能在同一個有身分、權限與協作紀錄的地方收任務、回報結果與等待審核。

| 工作面 | 在 OSSLab-agent 的用途 |
| --- | --- |
| **群組／私訊／線程** | 交辦、通知、進度、草稿確認、例外處理與人工審核。 |
| **Lark Mail** | 人員信箱與部門公用信箱都留在 Lark；agent 依授權讀取來信、整理重點、建立待辦與草擬回覆。對外寄送仍保留人工確認。 |
| **Docs／Wiki／Sheet** | 類似 Google Docs／Microsoft Office 的多人文件、知識庫、報表與試算表協作層。 |
| **Base／Forms** | 不是 XLS 附件，而是可自動化的多維表格與資料流程：外圍客戶填表、人員與 agent 依欄位共同更新，事件可通知、分派或交審。庫存、訂單與簡單出貨紀錄都能先在這裡做成輕量 ERP 流程。 |
| **Open Platform** | bot、事件、訊息卡片與 API，讓 agent 不離開 Lark 就能把結果放回正確的群組、文件或資料表。 |

Lark Mail 的價值不只是「有一個收信畫面」。它能把個人工作信箱與多個部門公用信箱放在同一套協作環境；被授權的 agent 可處理收件、分類、摘要與草稿，讓客服、採購或業務不必把 email 另外搬到一個 AI 工具。Lark 對公用信箱與跨裝置郵件使用的功能說明見[官方 Mail 介紹](https://www.larksuite.com/en_us/product/email)。

## 2.1 Base 與表單：不是 Excel 附件，而是人、agent 與客戶連動的資料流程

Lark Base 的定位接近 Airtable：可把資料做成格狀、看板、日曆、表單等不同工作視圖，再用 automation 串通知、分派、審核與後續處理。它不是傳統 XLS 檔，而是一個讓外圍客戶填表、團隊成員處理、AI agent 更新與比對、管理者核准的連動架構；同一筆資料可以在不同角色之間有一致的欄位、狀態與紀錄。

```text
外圍客戶／同事以 Lark Form 收集需求
        ↓
Lark Base 建立／更新訂單、庫存或出貨紀錄
        ↓ automation / bot event
agent 整理、比對、補資料或建立草稿
        ↓
Lark 群組、文件或待辦通知團隊確認
```

這不是要把所有資料都硬塞進同一張表；而是先用表單與結構化欄位把流程說清楚，讓人與 agent 都有可靠的輸入。詢價、庫存、訂單與簡單出貨紀錄都能先快速運作成輕量 ERP；真正需要會計、採購、銷售與交付的完整控管時，再接入 Odoo。可參考飛書官方的[ERP 資料同步到多維表格方案](https://www.feishu.cn/industry_solutions/integrate/111)；產品能力與限制仍以 [Lark Base 官方頁](https://www.larksuite.com/product/base) 為準。

# 3. 多人 SSO：一個帳號，順暢登入，但權限不混在一起

Lark 企業帳號是人員身分的起點；Authentik 將它以 OIDC 提供給自架服務。Lark 現行免費方案也提供可自訂的商務 Email，讓自有網域能建立個人與多個部門／功能性信箱；這些帳號正是 SSO 最需要的可靠身分依據。這讓同事在日常使用上是「同一個工作帳號、同一個登入脈絡」，而不是每接一套服務就建立另一組帳密；免費方案的功能與額度仍應以 [Lark 現行方案](https://www.larksuite.com/global/register) 為準。

```text
同事的 Lark 企業帳號
          ↓ OIDC
Authentik：統一身分驗證與 SSO 中心
   ├── Cloudflare Access：指定公開 Web 服務的外層 SSO
   ├── NetBird：VPN 與內網存取
   ├── RustDesk：IT 遠端維護
   ├── Termix：SSH／遠端桌面維護
   └── 其他核准納入的自架服務
```

- **Cloudflare Access** 先保護指定的公開 Web 服務，遠端同事先完成企業 SSO 才能到達服務本體。
- **NetBird** 以 SSO 提供受控 VPN／內網存取，減少為了維護而公開管理埠或共用 VPN 帳密。
- **RustDesk 與 Termix** 讓遠端桌面、SSH 與主機維護沿用相同身分。人員異動時，可以從企業身分與各服務角色一起回收。

SSO 是「確認你是誰」，不是「給你所有權限」。每個服務依然有自己的角色、群組、可見資產與稽核紀錄；能登入 Termix 不等於能連全部主機，能登入 RustDesk 也不等於能建立永久分享。

# 4. Agent Server：人只在 Lark，後端才處理 session 與工具

一台 AI Agent Server 承載多個隔離的 agent session。它由 `cc-connect` 加上一組 Codex、Grok 等訂閱制 agent build 組成；`cc-connect` 是跨訊息通道與 session bridge，接到 Lark 的事件後，依同事、群組與 project 路由到正確的專屬 agent；結果、草稿或需要人工決策的事項再回寫 Lark。

```text
Lark 群組／私訊／Mail／Base／Forms
          ↓ Lark 事件、API、訊息卡片
cc-connect（routing + session bridge）
          ↓
AI Agent Server：每位同事的專屬 agent／隔離 session
          ↓
Codex／Grok 等訂閱制 agent build + MCP + lark-cli
          ↓
受限資料來源、隔離 Chrome 容器、內網服務
```

Codex、Grok 等訂閱制 code agent runtime 負責推理與工具決策；OSSLab-agent 不重做模型框架，而是管理多人路由、session 隔離、Lark 互動、瀏覽器接手與稽核。**這套架構只使用訂閱制 runtime**：相對於純 API 按量計價，成本差異很大且更難預估，因此不採 OpenClaw 或 Hermes 這類需要自行承擔 API 用量的 agent 架構。對同事來說，這仍是 Lark 裡的一個專屬 agent，而不是另一個必須學會的聊天網站。

## 4.1 工作如何落地

| 人在 Lark 裡交辦的事 | agent 在後端做什麼 | 回到 Lark 的結果 |
| --- | --- | --- |
| 「整理今天客服信箱的詢價」 | 讀取已授權信箱、分類、擷取需求與待確認事項 | 群組摘要、待辦或回覆草稿。 |
| 「這份表單的需求先分派」 | 讀取 Base 紀錄、依欄位規則整理與比對 | 更新欄位、建立待審核項目、通知負責群組。 |
| 「比較三家報價，先不要送信」 | 讀取附件／公開來源、比價、標示風險 | Lark Doc 或群組中的結論與草稿。 |
| 「查目前庫存或客戶狀態」 | 查 Base；若已啟用 ERP connector，再查 Odoo | 帶來源與時間點的查詢結果。 |
| 「幫我處理這個網站，但付款先叫我」 | 在隔離 Chrome 操作至需要判斷的步驟 | Lark 通知加上真人可接手的瀏覽器入口。 |

# 5. Odoo 是選配，不是架構前提

OSSLab-agent 不要求每個團隊先買或先導入完整 ERP。對表單驅動、流程還在調整的工作，Lark Base／Forms 常常是更快的起點：先把資料欄位、責任人、狀態與通知機制跑順，再判斷是否真的需要 ERP 的庫存、會計、採購、銷售與交付能力。

當流程已經需要 ERP 時，可接入 **Odoo 18 Community Edition** 與自有 addons。對我們目前的客製需求，社群版加上可版本化的自訂模組就足以調整流程；AI agent 能協助高頻率修改、測試與驗證，不把企業版授權當成「想改流程」的前提。

```text
先用 Lark Base／Forms 驗證流程
          ↓
需要完整 ERP 控管時才選配 Odoo CE connector
          ↓
agent 依授權讀寫資料，重要寫入仍回 Lark 審核
```

# 6. 專屬 agent 的 Chrome 與 Vaultwarden：本人解鎖後才可使用

每位同事的專屬 agent 都有獨立的 Chrome profile，使用該同事對應的 Web 身分；這讓 agent 能在已授權的工作情境中協助操作，而不是借用別人的登入態。

Chrome 採用本 repo 維護的[修改版 KasmVNC Chrome 容器](../docker/chrome/README.md)：以 `kasmweb/chrome` 為 base，加入繁中輸入法、受控的 CDP relay 與 Bitwarden policy，並且不把 profile、cookie、登入狀態或 vault 資料寫進 image。真人與 agent 看的是同一個 browser session，真人可隨時接手。

第一次使用或 vault 已鎖定時，**同事本人必須先在 KasmVNC 裡解鎖 Vaultwarden**。agent 只能在已解鎖的工作階段中使用已允許的登入資料完成操作；它不會取得、保存或輸出 Vaultwarden 的主密碼。工作結束或不需使用時應重新鎖定。

# 7. 權限、人工接手與資料邊界

AI agent 能讀信、查表、操作瀏覽器，因此必須先把可做與不可做寫清楚。

| 原則 | 做法 |
| --- | --- |
| **每個人有自己的身分** | Lark 帳號與 SSO 是人員身分；不以共享帳密代替人員管理。 |
| **每個 agent 有自己的邊界** | 一人一個專屬 agent；session、Lark app scope、資料來源、browser profile、vault collection 與工作目錄都隔離，能力可依人設定不同。 |
| **KasmVNC 操作對同事可見** | agent 進行網站操作時，同事可在自己的[修改版 KasmVNC Chrome](../docker/chrome/README.md)即時看見同一個 browser session，並可隨時暫停或接手。 |
| **Vaultwarden 由本人解鎖** | 網站登入前由同事在 KasmVNC Chrome 解鎖自己的 extension；agent 只在目前已解鎖的 session 使用被允許資料。agent runtime 若需要服務秘密，才用自己的受限 API／CLI helper 讀取白名單 collection。任何 agent 都不能取得 human master password。 |
| **高風險動作可停** | 對外寄送、付款、刪除、改權限、第一次登入與不確定例外，先在 Lark 等人確認或由真人接手。 |
| **過程可回看** | 請求、草稿、確認與結果留在 Lark 或受控 project 記錄；部署與程式變更則留在 Forgejo。 |

# 8. 技術元件與責任

| 元件 | 角色 |
| --- | --- |
| **Lark Suite + Open Platform** | 唯一的人員工作入口：訊息、Mail、Docs、Base、Forms、審核與 bot API。 |
| **[Authentik](https://github.com/goauthentik/authentik)** | 統一身分驗證與 OIDC SSO 中心。 |
| **[Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/)** | 指定公開 Web 服務的外層存取政策與 SSO。 |
| **[NetBird](https://github.com/netbirdio/netbird)** | SSO 登入的 VPN／內網存取層。 |
| **[Forgejo](https://forgejo.org/)** | 自架 Git：程式、部署設定、操作與開發記錄的可追溯正本。只有管理者可用 Git 調整每個專屬 agent 的特性、能力、工具與權限。 |
| **AI Agent Server + [cc-connect](https://github.com/chenhg5/cc-connect)** | 多人 Lark 事件的跨訊息通道；一台 server 承載每位同事的專屬 agent 與隔離 session。 |
| **Codex／Grok 等訂閱制 agent build** | 唯一採用的 agent runtime；以訂閱制成本運行，不採 OpenClaw／Hermes 的純 API 用量架構。 |
| **Lark Base／Forms** | Airtable 類型的結構化資料、表單、視圖與工作流程自動化。 |
| **[Odoo 18 Community Edition](https://github.com/odoo/odoo)** | 可選 ERP connector；流程需要完整 ERP 時才納入。 |
| **[Vaultwarden](https://github.com/dani-garcia/vaultwarden)** | 人先在專屬 KasmVNC Chrome 解鎖自己的 vault；AI 的服務秘密則走受限 API／helper，兩者不混用。 |
| **[lejianwen/rustdesk-server](https://github.com/lejianwen/rustdesk-server)** | 自架 RustDesk server／API，處理 IT 遠端維護與有期限的分享。 |
| **[Termix](https://github.com/Termix-SSH/Termix)** | 自架 SSH／遠端桌面管理入口。 |
| **[修改版 KasmVNC Chrome](../docker/chrome/README.md) + CDP + Playwright** | 本 repo 維護的真實瀏覽器執行層，含繁中輸入、CDP relay 與 Bitwarden policy；每位同事與其專屬 agent 使用獨立登入態。 |

# 9. Scope 與暫不處理

- 不提供第二個給同事日常使用的聊天 UI；人員工作入口就是 Lark Suite。
- 不假設每個團隊都需要 Odoo；Base／Forms 是可先上線的預設流程層。
- 不把人類 master password、銀行、個人 2FA、cookie、profile、資料庫或 token 放進 agent 可讀設定或公開 repo。
- 不讓 agent 預設自行完成付款、對外承諾、刪除資料或改權限。
- 不採 OpenClaw、Hermes 或純 API 按量計價的 agent 架構；runtime 只採 Codex、Grok 等訂閱制 agent build。
- 完整本地 LLM 套件與視覺化管理後台可後續擴充，但不改變 Lark-first 原則。

# 10. License & related projects

- 本 repo（OSSLab-agent 文件與 Chrome 容器薄層）：[MIT License](../LICENSE)
- Lark Suite：[產品頁](https://www.larksuite.com/)／[開放平台](https://open.larksuite.com/document/)
- [lark-cli](https://github.com/larksuite/cli)、[cc-connect](https://github.com/chenhg5/cc-connect)、[Codex CLI](https://github.com/openai/codex)、[Playwright](https://github.com/microsoft/playwright) 與其他相依元件各自維持其授權。
