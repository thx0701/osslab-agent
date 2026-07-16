# osslab-agent 架構規格

> 狀態：WIP / draft。本文件描述系統如何組成、保存狀態及控制權限；使用情境請看 [功能規格](functionality.md)。

## 1. 架構目標

osslab-agent 把 channel、訂閱制 code agent runtime、工具、browser 與人工接手接成可追溯的工作流。它不重造 agent framework：Claude Code CLI、Codex CLI 或其他可支援 runtime 負責推理與工具決策；osslab-agent 負責 routing、session、project policy、browser、approval 與 audit 關聯。

核心判斷：

| 判斷 | 做法 |
|---|---|
| 不重造 runtime | 以現成 code agent CLI 作為可替換 agent process |
| 優先使用訂閱制 runtime | 常態任務由已授權的 CLI 執行；本地 LLM / 私有檢索是可選補充 |
| 不依賴一次性 prompt | 使用長 session、stdio、process bridge 或互動式 session 保留 context、stream 與工具調用 |
| Lark 不作長期知識庫 | Lark 處理事件、通知與批准；可重用結論進 Git artifact |
| browser 是真實執行環境 | 同一隔離 session 同時提供 agent CDP 與人類 VNC 接手 |
| 共用規範、隔離狀態 | 團隊規範與權威知識可共用；session、browser、bot identity 與 work directory 必須隔離 |

### 1.1 Shared vs Isolated

多入口不是「同一個 agent 換皮」。產品必須同時滿足兩件事：

| 層 | 可共用 | 必須隔離 |
|---|---|---|
| 規範與知識 | 團隊規則、playbook、經授權的 skill／MCP 定義、私有 Git 上的權威知識 | — |
| 執行身份與狀態 | — | chat session、conversation history、BrowserProvider profile（cookie／download／vault 狀態）、Lark bot identity、work directory、CDP／VNC 接入點 |

驗證標準：任一入口應能讀到同一份已授權的團隊規範與知識；bot A 的對話不得出現在 bot B；bot A 的 browser 登入態不得串到 bot B；每個入口使用自己的 bot identity、work directory 與 browser 接入點（除非 project 明確允許 domain-shared browser，見 §4.1）。

## 2. Git-first：長期真相與可追溯 action

私有 Git（例如 Forgejo、GitHub、Gitea）是程式、agent policy、playbook、project knowledge、筆記、技能與研究 artifact 的長期真相來源。Lark 與 Web workbench 是工作介面；它們不取代 version control。

~~~text
Lark / Web workbench / API
  交辦、討論、通知、批准、短期 session
                 ↓
project router + agent runtime + BrowserProvider
                 ↓
branch → working change → commit / PR → human approval
                 ↓
private Git: long-term truth, review, rollback and artifact history
~~~

原則如下：

1. 重要結論、可重用研究、規則、程式與 playbook 要產生可 review 的 Git 變更。
2. 每個重要 action 至少可關聯 request/task、repo、branch、commit 或 PR、批准紀錄及結果。
3. session、cache、下載暫存、browser profile、模型思考與未定草稿屬 runtime state，不需逐筆 commit。
4. 不為每次對話建立 repo；以 project repo 或專門的 knowledge / artifact repo 作為保存單位。
5. Git 只保存可公開給該 repo 成員的內容。私鑰、token、cookie、密碼、OAuth secret 與可用 invitation link 永不入庫。

### 2.1 權威知識的執行期掛載

Git-first 描述的是**正本**；執行期仍需要可讀、可更新節奏的掛載：

| 類型 | 正本 | 執行期 |
|---|---|---|
| 權威知識／policy／skill 定義 | private Git | 部署機 read-only mount 或定期 sync；agent 依任務讀取，不憑記憶改寫正本 |
| 可 review 的成果 | private Git（branch／PR） | working tree → commit／PR |
| 短期對話與草稿 | session store | Web workbench／runtime；需保留時再輸出為 artifact |

## 3. 狀態模型

| 類型 | 正本 | 例子 |
|---|---|---|
| 長期、可 review 的內容 | 私有 Git repo | code、policy、runbook、研究結論、benchmark、skill |
| 權威知識的 live 視圖 | 私有 Git（經 mount／sync） | 部署機上的 knowledge tree、runtime 注入的規範 |
| 工作中內容 | Web workbench / agent session | 對話、stream、草稿、附件工作區 |
| 事件與批准 | Lark + action record | 任務來源、批准、通知、人工接手 |
| 執行狀態 | project runtime | queue、session、download、cache、temporary artifact |
| 機密 | host secret store / private environment | SSH private key、password、OAuth secret、PAT、cookie |

Web workbench 可以提供 project context 與 artifact 工作區，但其長期保存策略必須以 project 的 Git policy 為準。需要保留的內容應輸出為 Markdown、結構化資料或程式碼後 commit。

## 4. Project 是部署與安全單位

~~~text
Project = runtime
        + work directory
        + channel identity
        + identity / authorization policy
        + browser policy
        + tool policy
        + data-retention policy
        + action policy
~~~

Project routing 同時決定 context、可用工具、資料來源、browser profile、保留策略與 action policy。它不是單純的 UI 分類。

允許「同一 work directory 家族、多個 runtime」（例如同一資料域下的 Claude Code、Codex、其他 CLI 入口），但每個入口仍是獨立 session 與 channel identity；不得因此共用 cookie 或未授權的 tool surface。

### 4.1 Browser 隔離與 domain-shared profile

bot 與 browser 的關係採**預設隔離**，而非絕對一對一：

| 規則 | 說明 |
|---|---|
| 預設 | 高風險登入域、客戶資料域或不同角色 → 各自 BrowserProvider profile |
| 允許共用 | 同一 data domain、相同 data policy、無跨客戶隔離需求，且 project 明文配置 domain routing |
| 禁止 | 業務登入態 bot 與 research bot 共 profile；不同客戶或不同權限域共 cookie／download |

明確的 domain routing 可以讓多個 runtime 共用同一個受控 browser profile；未配置則不得共用。

## 5. 主要資料流

~~~text
Lark group / direct message            Web workbench chat / image / file
          ↓                                          ↓
          └──────── channel adapter → project routing ─┘
                              ↓
              （可選）gateway：webhook、auth、fan-out
                              ↓
                 session bridge over stream / stdio
                              ↓
      Runtime Provider → allowed tools / MCP / skills / shell
                              ↓
              BrowserProvider: CDP / Playwright and VNC
                              ↓
    ERP, email, commerce, documents, Lark, websites and other systems
~~~

產品路徑是：**channel adapter → project router → runtime session**。reference deployment 可在 adapter 前加 gateway（webhook、auth、fan-out）；產品不得假設單一 process 扛全部 channel 與 runtime。

每個 project 可路由到獨立 session。需要登入態時，session 使用指定的 BrowserProvider profile；人與 agent 對同一 profile 接手，而不同 project 不得無意間共用 cookie、download 或 vault state。

## 6. 元件責任

| 元件 | 責任 |
|---|---|
| Lark 與 Open Platform | 事件、通知、Bot、文件、互動卡片、上游身份來源 |
| Web workbench | 長對話、圖片、檔案、project workspace、stream 與草稿（產品內建 workbench；reference 可對應 cc-connect 類 web channel） |
| channel adapter / router | 將 channel 事件正規化並路由到 project |
| session bridge | 將使用者與 project 綁到正確 runtime session |
| Runtime Provider | 推理、工具調用、生成變更候選與結果摘要（見 §6.1） |
| Tools surface | skill、MCP、shell 與其他工具的 allowlist 與可見範圍（見 §6.2） |
| 私有 Git | 程式、policy、artifact、review、approval 關聯與回滾 |
| BrowserProvider | profile 隔離、CDP/Playwright、自動化與 VNC 人工接手 |
| local LLM / private retrieval | 敏感資料、低成本或離線處理的可選擴展 |
| osslab-agent CLI | 安裝、設定、啟停與連接上述元件的產品層 |

### 6.1 Runtime Provider 契約

「可替換 runtime」需要最小契約，而不是只列產品名稱。每個 Runtime Provider 至少應定義：

| 能力 | 要求 |
|---|---|
| Session lifecycle | 啟動、恢復、結束；是否支援 resume |
| Stream 事件 | token／進度、tool call、error、完成狀態 |
| 工作目錄與 env | work directory、必要 env（例如 browser CDP 接入點）的注入方式 |
| Tools 可見範圍 | 哪些 skill／MCP／shell 對此 session 可見 |
| 失敗語意 | 斷線、額度耗盡、auth 過期、不可恢復錯誤；是否可重試或需人工接手 |

首批預期實作以訂閱制 code agent CLI 為主（Claude Code CLI、Codex CLI 等）。**Orchestrator runtime**（多 worker：實作 → 審查，或類似互審流程）是可選能力，不是所有 runtime 的預設行為；若部署此類 runtime，仍須遵守同一 session／tool／browser 隔離規則。

### 6.2 Tools surface：skills 與 MCP

Tools 是 project 的安全邊界，不是全域插件池。

| 層 | 內容 |
|---|---|
| Project tool policy | allowlist：shell、browser、MCP server、skills 集合、外部 API |
| Skills | 可版控；按 project 掛載。不得把僅適用某一 runtime 的儀式或專屬 skill 強塞進所有 runtime |
| MCP | 按 project 啟停；credential 只進 host secret store；連線失敗要可觀測 |
| 與 Git 的關係 | skill 定義與 policy 正本在 private Git；live mount 是部署細節 |

agent 只能使用當前 project 允許的 tools；跨 project 不得隱式繼承高權限 tool surface。

## 7. 身份、授權與批准

身份驗證、產品授權與 action 批准是三個不同層次：

~~~text
identity provider → product session
        身份驗證：誰在使用

project role + data policy + tool policy
        授權：可讀哪些資料、可使用哪些 project 與工具

request + action class + approval record
        批准：這一個外發、下單、付款或正式寫入能否執行
~~~

產品應支援標準 OIDC provider。OSSLab reference deployment 已有 Authentik，並以 Lark 作為上游身份來源；新部署可以接自己的 OIDC provider。Lark direct OAuth 是部署選項，不應與產品授權或 bot credential 混在一起。

Web SSO 只處理人員登入。Git SSH、PAT、API、CI 與 bot 使用自己的 transport credential；不得用人員 web session 取代。每個產品仍在本地判斷 reader、operator、approver、admin 及 project / data scope，不因使用者可登入 Lark 就自動提權。

### 7.1 三種 actor

稽核與授權要分開三種角色，不可混成「某個人／某個 bot」：

| Actor | 是什麼 | 例子 |
|---|---|---|
| Identity | 誰在使用產品 | OIDC 使用者、Lark 使用者 |
| Git operator | 誰寫入 version control | 人類帳號、bot 帳號、CI 帳號 |
| Approver | 誰批准某個 action | Lark 訊息批准、PR review、二次確認 workflow |

群組訊息可以作批准來源，但批准必須關聯特定 request 與**內容版本或 commit**；不能把模糊或舊的同意套用到新的 action。Git operator 與 Approver 可以是不同人；bot 可以是 Git operator，但不能自行充當高風險 action 的 Approver。

### 7.2 最小 action policy

| 類別 | 例子 | 預設 | 最低紀錄 |
|---|---|---|---|
| 讀取 | 查文件、查狀態、公開 research | 可直接執行 | request、source、result 摘要 |
| 草稿 | Markdown、email draft、程式草稿 | 可直接執行 | session artifact 或 branch |
| 可回滾內部變更 | branch、commit、PR、草稿資料 | 依 project policy | repo、branch、commit/PR、驗證結果 |
| 對外 / 營運寫入 | 寄信、發文、正式資料寫入、下單 | 需明確批准 | approver、批准時間、action/result、驗證結果 |
| 高風險不可逆 | 付款、刪資料、改權限、正式部署 | 需二次確認或既定 workflow | action record、結果與回復資訊 |

### 7.3 寫入後驗證

對正式系統（ERP、電商後台、生產設定等）的寫入，agent 應在**同一 project** 的 browser 或 API 做最小驗證，再回報完成。

| 規則 | 說明 |
|---|---|
| 同 project 驗證 | 使用該 project 的 BrowserProvider／API credential，不借其他 project 的 browser |
| 失敗要明講 | 驗證不了時，回報必須說明哪段未驗證，不得裝成已完成 |
| 紀錄 | 寫入類 action record 應能關聯驗證結果或未驗證原因 |

## 8. BrowserProvider 與人工接手

BrowserProvider 是執行資源，不是身份或授權本身。每個 project 應定義：

- provider 與版本，例如 Kasm Chrome、BrowseForge 或其他兼容實作；
- profile / volume 隔離等級；
- CDP 或 Playwright 接入點；
- VNC 或其他 human takeover 方式；
- 可登入系統與工具 allowlist；
- download、cookie 與 profile 的 retention / cleanup 規則。

預設 browser 實作可以是基於 Kasm 的 Chrome 容器：完整 Chrome、持久 profile、CDP 對外、web VNC、中文輸入與可選 Bitwarden extension。BrowserProvider contract 必須容許使用 BrowseForge 等既有 profile-isolation provider，而不將產品鎖死於單一 image。

人類接手主要用於 captcha、OTP / 2FA、首次登入、付款及其他需要真人判斷的步驟。agent 應在原 channel 提示並提供正確 project 的接手入口；人完成後，agent 再在同一 session 續作。

### 8.1 Kasm Chrome reference image

Kasm Chrome 是預設 provider 的 reference image，而非唯一實作。其目標是讓 AI 與人操作同一台完整 browser，不是用 headless browser 或另開遠端桌面取代登入態。

| 能力 | reference 實作方向 |
|---|---|
| 中文輸入 | 提供 fcitx-chewing、傳統桌面輸入法與必要的鍵盤注入設定，讓 Mac、Windows 與 iPad 的 VNC 使用者可輸入中文 |
| 輕量與持久化 | image 層共用；每個 profile 以 volume 保存 cookie、擴充、書籤與下載檔 |
| Web 接手 | KasmVNC 讓使用者從一般 browser 直接進入，不要求另裝遠端桌面 client |
| CDP | Chrome debug port 預設只在容器內可見時，以受控 relay 對 project 暴露 CDP；不可公開暴露給未授權網路 |
| 密碼管理 | 可由 managed policy 安裝 Bitwarden extension，但是否解鎖、是否保存密碼仍由 project security policy 決定 |

## 9. 密碼與 browser profile 策略

產品提供兩種可選策略：

| 策略 | 做法 | 取捨 |
|---|---|---|
| 不保存密碼 | browser 不存密碼；人類在 VNC 以 Bitwarden auto-fill，cookie 可保留 | 安全性高，但每個新網站需要人工首次登入 |
| 長期保存於隔離 profile | browser / vault 狀態存於專屬 volume | 操作方便，但需更嚴格主機、vault 與網路防護 |

預設推薦不保存密碼但使用密碼管理器。agent 不得讀取、輸出或把 vault secret 寫入 Git；未來如整合 vault API，必須額外定義最小權限、批准與 audit。

### 9.1 角色身份與 browser 配置分離

真人角色身份與 bot / browser 配置是兩層不同的東西：

- 真人角色可以有自己的私有 email、Lark 身份與 password-vault 身份；這是可交接的責任身份。
- 對外長期聯絡可使用共享收件匣，但每個實際寄件者應有可辨識的身份與簽名。
- bot / BrowserProvider profile 只是 CDP、VNC、volume、cookie 與下載檔的執行配置；它不可自行取得真人角色的所有權限。

這個區分可讓人員交接、密碼輪替與 browser 重新建立各自進行，也避免把個人身份、共享 inbox 與 agent profile 混為同一個帳號。

## 10. 資料與工具邊界

每個 project 指定資料來源、可用工具、保留策略與外送規則。建議最低分為：

- research：公開 research、比價、來源整理。
- dev：程式碼、issue、PR、技術設計。
- it：infra、主機、部署與排障。
- business / ops：ERP、報價、採購與客戶聯絡，採用更嚴格權限。

敏感資料可只進本地檔案、本地向量索引或本地 LLM。外部模型需要處理敏感內容時，先摘要、遮蔽或只傳必要片段。Lark Bot 的事件 scope、OpenAPI scope、可加入群組及可呼叫使用者也應採最小權限。

## 11. 併發、額度與失敗

訂閱制 multi-bot 的日常風險是 concurrent session 與 rate limit，不是單次 prompt 寫法。

| 項目 | 產品期望 |
|---|---|
| 併發 | 每 project 可設 max concurrent session；超出時排隊或拒絕並回明確錯誤 |
| 額度 | 訂閱額度耗盡時可降級（排隊、改其他已授權 runtime、或只允許讀取／草稿） |
| 優先序 | 可選：短 Lark action 優先於長 research（由部署策略決定） |

### 11.1 失敗與接手

| 情況 | 預期 |
|---|---|
| Runtime session 中斷 | 若契約支援則 resume；否則在原 channel 回失敗摘要，不靜默假裝成功 |
| CDP／browser 斷線 | 停止依賴 browser 的步驟；提示正確 project 的 VNC 或重連 |
| Lark webhook 重複／亂序 | request 具 idempotent id；同一 action 不重複外發 |
| 半套 Git 變更 | 不回報「已完成」；附 branch／PR 狀態與下一步 |
| 寫入後驗證失敗 | 依 §7.3 明講未驗證段落與建議人工檢查點 |

## 12. 安裝與部署

v1 目標環境是 Ubuntu LTS、Docker、Node 20+，以及已完成登入的受支援 code agent CLI。

預期安裝流程：

1. 檢查 Linux、Docker、Node 與 code agent runtime。
2. 安裝 channel router、Lark CLI 與必要 browser provider。
3. 選擇 Lark、Web workbench 或兩者入口。
4. 建立 project，配置 runtime、work directory、channel identity、tool 與 browser policy。
5. 視入口設定 Lark App 或 OIDC client；secret 只進 host secret store。
6. 建立 browser profile 與 VNC human takeover。
7. 註冊 service，初始化 project workspace。
8. 以低風險流程驗證 request、branch、PR、approval 與 artifact link。

### 12.1 Reference deployment 對照

OSSLab 的既有部署是 **reference deployment**，不是所有使用者都必須複製的服務拓撲。概念對可替換元件：

| 產品概念 | 可替換實例（示例） |
|---|---|
| private Git | Forgejo / GitHub / Gitea |
| Identity provider | Authentik 或任意 OIDC |
| Channel | Lark adapter；其他 IM 可後續接 |
| Web workbench | 產品 workbench；reference 可對應 cc-connect 類 web channel |
| Channel router / session bridge | cc-connect-class bridge；可加 gateway 前置 |
| BrowserProvider | Kasm Chrome / BrowseForge / 兼容實作 |
| Runtime Provider | Claude Code CLI / Codex CLI / 其他契約相容 runtime |

### 12.2 Lark App 設定

啟用 Lark channel 時，安裝流程需要取得 App ID 與 App Secret、設定 callback / event subscription，並只申請工作流所需的最小 scope。Lark 的一鍵 launcher 可作為建立自建 App 的捷徑，但不免除 scope、可用範圍、callback 與 secret 保管的檢查；截圖僅為示例 UI，不是唯一安裝路徑。

App Secret 只應進 host secret store 或私有 environment；不得出現在 config example、commit、issue、聊天紀錄或 browser screenshot。

![Lark intelligent-agent launcher：填入名稱後建立 App，再回到安裝流程填入 App ID 與 App Secret（示例 UI）](assets/img_1778392141449_0.jpg)

## 13. 範圍與暫不處理

### 13.1 v1 納入（契約層）

- Ubuntu LTS + Docker + Node 20+。
- Lark channel + Web workbench 入口。
- 至少一種 Runtime Provider（訂閱制 code agent CLI）與 BrowserProvider。
- Project 隔離、Git-first artifact、最小 action policy、寫入後驗證期望。
- Skills／MCP 的 project allowlist（作為 tools surface）。

### 13.2 v1 可選

- Orchestrator runtime（多 worker 互審）。
- Domain-shared browser profile。
- 併發／額度排隊策略的進階 UI。

### 13.3 暫不處理

- 非 Ubuntu OS。
- 完整多租戶管理與視覺化營運後台。
- 所有非首批 runtime 的正式支援保證。
- 本地 LLM 的完整部署包。
- GPU 加速與音訊。
- code agent CLI 認證與 API key 生命週期管理。
- 跨產品角色同步、SCIM 或自動提權。
- 排程／自主 cron 任務的完整產品化（若部署，須用 machine identity 與更嚴 action policy；v1 不保證）。
- 大型獨立 audit database；v1 可先以 Git artifact 與 action record 關聯落地。

## 14. License 與相關專案

本 repo 的 osslab-agent 與 browser image 薄層採 MIT License。Kasm Chrome、cc-connect、Lark CLI、Claude Code CLI、Codex CLI、Playwright 與 Bitwarden 各自遵循原專案的授權條款；本 repo 不重新分發它們。

相關專案：

- Larksuite / 飛書
- Lark CLI
- cc-connect
- Claude Code
- Codex CLI
- Playwright
- Kasm Chrome
- Bitwarden
