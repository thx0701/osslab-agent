# 02 · Lark Suite、Mail、Base 與 SSO：一個工作入口

**Lark Suite 是企業團隊使用的 IM 與協作平台**：它從群組、私訊開始，但也把文件、試算表、信箱、表單、資料流程與審核放進同一個 workspace。AI agent 時代，它不只是「傳訊息給 bot」的地方；agent 可以像虛擬同事一樣，在同一個團隊流程接任務、處理、回報與等待確認。

考量 IM、Mail、文件、Base／Forms、審核、Open Platform 與企業身分的完整性，OSSLab 認為 **Lark Suite 是辦公團隊最適合的 AI bot channel**：agent 能進入既有對話、資料與審核流程，而不是要求團隊再適應另一個 AI 網站或把工作內容複製出去。

因此 OSSLab-agent 對團隊成員只提供一個入口：Lark Suite。這不是限制功能，而是避免工作散落在聊天軟體、信箱、表單工具、AI 網頁與各種帳密之間。Docs、Sheet 與 Wiki 也提供類似 Google Docs／Microsoft Office 的線上文件、試算表與知識協作，AI agent 只需要接進去，而不必把人拉到另一個 UI。

## 為什麼 Lark 不是「只拿來聊天」

| 工作需要 | Lark 在這套架構中的角色 |
| --- | --- |
| 交辦、進度與審核 | 群組、私訊、線程與互動卡片把任務、草稿、確認與結果留在大家本來就在看的地方。 |
| 多個工作信箱 | 個人企業信箱與部門公用信箱在同一個 Lark Mail 環境使用；agent 只讀取被授權的 mailbox，協助整理與草擬，不把 email 轉存到另一套工具。 |
| 文件與工作資料 | Docs、Sheet、Wiki 提供多人文件、試算表與知識協作；Base、Forms 則把需求、資料與流程放在同一個 workspace。 |
| 自動化與系統串接 | Open Platform 的 bot、事件、訊息卡片與 API 讓 agent 能從 Lark 收任務，也把結果回寫 Lark；官方 [lark-cli](https://github.com/larksuite/cli) 則把 Messenger、Docs、Base、Sheets、Mail 等常用操作提供給人員與 AI agent 使用。 |

Lark Mail 支援公用信箱由多人共同使用，也可將郵件工作與群組協作接起來；這正好符合客服、採購、業務等部門信箱情境。Lark 現行免費方案提供可自訂的商務 Email；以自有網域建立個人與多個部門／功能性信箱後，每個 Lark 企業帳號就能成為 Authentik SSO 的身分依據，而不是再發一組共用帳密。實際可用功能、帳號與信箱額度依 [Lark 現行方案](https://www.larksuite.com/global/register) 為準；[Lark Mail 官方介紹](https://www.larksuite.com/en_us/product/email)可作為功能參考。

## Base／Forms：不是 XLS，是人、agent、團隊與客戶連動的自動化表格

Lark Base 比較接近 Airtable 的工作方式，而不只是把 Excel 放到雲端：一份結構化資料可以用格狀、看板、日曆或表單視圖工作，再加上 automation、通知、權限與審核。外圍客戶透過 Form 送資料，團隊依欄位處理，AI agent 比對、補資料或觸發後續工作；每一筆紀錄都有共同的狀態與責任人。

```text
外圍客戶／同事填 Form → Base 記錄 → automation／bot event → agent 與團隊處理 → Lark 通知／草稿／審核
```

因此，很多還在調整的流程不用一開始就上完整 ERP：先用 Base 把輸入、狀態、責任人與通知跑順，agent 才有清楚的資料可以讀寫。即使是庫存、訂單與簡單出貨紀錄，也可以快速作為輕量 ERP 流程使用；當流程需要會計、採購、銷售與交付的完整控管時，再把 Odoo 作為選配 connector 接上，而不是反過來讓所有工作都被 ERP 綁住。飛書官方也提供將 ERP 資料接入多維表格的[整合方案](https://www.feishu.cn/industry_solutions/integrate/111)。

## SSO 讓多服務的登入保持順暢

Lark 企業帳號也是人員身分的起點。Authentik 將這個身分以 OIDC 提供給自架服務，讓同事用同一個企業帳號自然地登入需要的工具，而不是每套服務都重建一份帳密。

```text
同事的 Lark 企業帳號
        ↓ OIDC
Authentik 身分與 SSO 中心
   ├── Cloudflare Access：受保護公開 Web 服務的外層 SSO
   ├── NetBird：VPN 與內網存取
   ├── RustDesk：IT 遠端維護
   ├── Termix：SSH／遠端桌面維護
   └── 其他核准納入的自架服務
```

這裡的「順暢」不是放寬權限：Cloudflare Access 只保護指定公開服務，NetBird 讓內網存取走 SSO，RustDesk 與 Termix 收斂維護登入；每個服務仍保有自己的角色、群組、可見資產與稽核規則。能登入，不代表能管理全部。

Lark 的產品能力與 Open Platform 以[官方產品頁](https://www.larksuite.com/index)及[開發文件](https://open.larksuite.com/document/)為準。

下一篇：[〈管理與治理：把 agent 當成可管理的工作角色〉](03-agent-governance.md)
