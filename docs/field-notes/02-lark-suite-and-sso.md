# 02 · Lark Suite、Mail、Base 與 SSO：一個工作入口

OSSLab-agent 對團隊成員只提供一個入口：**Lark Suite**。這不是限制功能，而是避免工作散落在聊天軟體、信箱、表單工具、AI 網頁與各種帳密之間。Lark 已經把這些日常需要的工作面放在同一個 workspace，AI agent 只需要接進去，而不必把人拉到另一個 UI。

## 為什麼 Lark 不是「只拿來聊天」

| 工作需要 | Lark 在這套架構中的角色 |
| --- | --- |
| 交辦、進度與審核 | 群組、私訊、線程與互動卡片把任務、草稿、確認與結果留在大家本來就在看的地方。 |
| 多個工作信箱 | 個人企業信箱與部門公用信箱在同一個 Lark Mail 環境使用；agent 只讀取被授權的 mailbox，協助整理與草擬，不把 email 轉存到另一套工具。 |
| 表單與工作資料 | Base、Sheet、Forms、Docs 與 Wiki 將需求、資料、文件與流程放在同一個 workspace。 |
| 自動化與系統串接 | Open Platform 的 bot、事件、訊息卡片與 API 讓 agent 能從 Lark 收任務，也把結果回寫 Lark。 |

Lark Mail 支援公用信箱由多人共同使用，也可將郵件工作與群組協作接起來；這正好符合客服、採購、業務等部門信箱情境。[Lark Mail 官方介紹](https://www.larksuite.com/en_us/product/email)與其公用信箱說明可作為功能參考。

## Base／Forms：Airtable 類型的表格，自動化流程的起點

Lark Base 比較接近 Airtable 的工作方式，而不只是把 Excel 放到雲端：一份結構化資料可以用格狀、看板、日曆或表單視圖工作，再加上 automation、通知與權限。它適合先把客戶、詢價、庫存、採購、維修、任務與申請流程做成可靠的欄位與狀態。

```text
表單提交 → Base 記錄 → automation／bot event → agent 處理 → Lark 通知／草稿／審核
```

因此，很多還在調整的流程不用一開始就上完整 ERP：先用 Base 把輸入、狀態、責任人與通知跑順，agent 才有清楚的資料可以讀寫。飛書官方也提供將 ERP 資料接入多維表格的[整合方案](https://www.feishu.cn/industry_solutions/integrate/111)；當流程需要完整 ERP 控管時，再把 Odoo 作為選配 connector 接上，而不是反過來讓所有工作都被 ERP 綁住。

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
