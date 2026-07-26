# 02 · Lark Suite 與 SSO：協作工具，也是身分入口

Lark Suite 對我們不是單純的公司聊天室。它把群組溝通、文件、表格、多維表格、行事曆、信箱、任務與開放平台放在同一個工作面；更重要的是，既有的企業帳號已經是同事每天使用的身分入口。

這也是 osslab-agent 以 Lark 作為行動與審核層的理由：AI 不必要求團隊改用另一個陌生的任務系統。交辦、卡片通知、草稿確認與人工介入，都能留在原本的協作脈絡中；長研究再回到 cc web 整理，避免把 IM 當成雜亂的永久知識庫。

## 強的地方不只在 IM

| 工作需要 | Lark 在我們工作流中的角色 |
| --- | --- |
| 即時交辦與確認 | 群組、私訊、線程與互動卡片承接通知、待辦與審核。 |
| 共用工作資料 | Docs、Sheet、Base 與 Wiki 讓文件、表格、結構化資料能留在同一個 workspace。 |
| 日常協作 | Mail、Calendar、Meeting、Task 與 Approval 把跨工具的來回減少到可管理的範圍。 |
| 接入自架系統 | Open Platform 的 bot、事件與 API 讓 agent 可以把結果回寫到人正在工作的地方。 |

這些能力的關鍵不是「功能很多」，而是同一個企業帳號、同一份通訊錄與同一個協作上下文可以被安全地延伸。Lark 的產品能力與開放平台以[官方產品頁](https://www.larksuite.com/index)及[開發文件](https://open.larksuite.com/document/)為準。

## SSO 把帳號生命週期收回來

我們目前以 Lark 企業帳號作為人員登入的起點，透過 Authentik 的 OIDC 身分橋接登入自架服務。使用者不需要為每一個維護平台重新註冊與記憶一組密碼；人員到職、異動或離職時，帳號生命週期也能從同一個企業身分處理。

```text
同事的 Lark 企業帳號
        ↓ OIDC
Authentik 身分橋接
   ├── Cloudflare Access：受保護公開 Web 服務的外層 SSO
   ├── NetBird：VPN 與內網存取
   ├── RustDesk：IT 遠端維護
   ├── Termix：SSH／遠端桌面維護
   └── 其他核准納入的自架服務
```

其中 Cloudflare Access、NetBird、RustDesk 與 Termix 已經走這條 SSO 路徑。Cloudflare Access 先在外層驗證指定公開 Web 服務的使用者；NetBird 讓同事以同一個企業身分連入內網；RustDesk 與 Termix 則收斂日常的遠端維護登入。這讓「誰能登入維護工具」不再是一份散在各服務裡的帳密清單，而能與人員的公司身分連結。

SSO 只負責辨識「你是誰」，不等於自動取得所有權限。每個服務仍保留自己的角色、群組、管理者與稽核規則；能登入 RustDesk，不代表就能管理所有 peer 或開永久分享；能登入 Termix，也不代表就能連上全部主機。這條分界是便利與安全能同時成立的原因。

下一篇：[〈管理與治理：把 agent 當成可管理的工作角色〉](03-agent-governance.md)
