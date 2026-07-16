# osslab-agent 功能規格

> 狀態：WIP / draft。本文件描述使用者能完成什麼；實作邊界、資料保存、身份與部署請看 [架構規格](architecture.md)。

## 1. 要解決的工作

日常工作常是開瀏覽器、登入系統、填表、複製貼上與回信：查即時庫存、物流與訂單狀態，採購、銷售、客戶聯絡及助理事務。另一類工作是研究外部資訊、比價、整理來源，並將可重用結論留給不同 project。

osslab-agent 以三個入口接住這些工作：

| 層 | 主要能力 | 使用時機 |
|---|---|---|
| Lark 行動層 | 交辦、通知、人工審核、群組協作、人工介入 | 短任務與需要決定的 action |
| Web workbench | 長對話、stream、圖片與檔案、research、project context | 研究、整理、草稿與長任務 |
| Browser 執行層 | 已登入的真實系統、CDP、VNC 人工接手 | 查詢、填表、草稿及受批准的外部 action |

**Web workbench** 是產品內的正式長任務工作台（stream、檔案、project context、草稿），不是附屬 chat UI。reference deployment 可用既有 web channel 實作，但產品敘事統一使用 Web workbench，避免與第三方「某家 code agent 的 web」混淆。

它不重做模型調度核心；Claude Code CLI、Codex CLI 或其他符合 Runtime Provider 契約的 code agent CLI 是可替換的 runtime。osslab-agent 負責 channel routing、session、專案上下文、tools（含 skills／MCP）、審核與人工接手。一個人可以有多個 agent；團隊也可以按角色、工作流及 project 分流。

共用的是規範與知識；隔離的是 session、browser 登入態、bot identity 與 work directory。詳見 [架構規格 · Shared vs Isolated](architecture.md#11-shared-vs-isolated)。

## 2. Lark：行動與協作入口

v1 的行動與審核入口是 Larksuite。它提供 IM、群組、私訊、線程、文件、Sheet、Base、行事曆、會議、郵件、OpenAPI、Bot 平台與互動卡片，適合接住人與 agent 的即時協作。

Lark 是事件與決定的入口，而不是唯一的知識庫。交辦、通知、審核、人工接手與結果摘要留在 Lark；長研究、來源與可重用結論則在 Web workbench 工作後，整理成可保存的 artifact。

| 能力 | 對工作流的意義 |
|---|---|
| IM | 群組、私訊、線程與視訊承接即時交辦、通知與稽核 |
| 雲端文件 | Docx、Sheet、Base、Whiteboard 與 slides 可讓人與 agent 同步協作 |
| Mail / Calendar / Meeting | 郵件、行程、會議紀錄、摘要與待辦可接進同一個協作入口 |
| Sheet / Base | 小團隊可先建立輕量客戶、庫存、採購與訂單工作台 |
| OpenAPI | agent 可透過受控 scope 操作文件、訊息、行事曆及其他已授權資源 |
| Bot 平台 | 事件訂閱、訊息發送、互動卡片與可用範圍讓人機協作可落在既有群組 |

### 2.1 Sheet / Base 作為輕量營運工具

未導入完整 ERP 的團隊可以先用 Lark Base 管理客戶、商品、庫存、採購與銷售資料，用 Sheet 做試算與報表。agent 可透過 Lark API 讀寫這些結構化資料、產出報告、協助查詢與更新；導入 ERP 後，仍可按資料主體選擇 Base 或 ERP。

## 3. Web workbench：研究、草稿與 project context

Web workbench 是正式工作台。它支援長任務的 stream 回應、圖片與檔案輸入、來源整理、研究 artifact、project context 與草稿。

Web workbench 保存 session 與工作中的內容；需要長期保留、交接或 review 的結果，應輸出成 Markdown、資料檔或程式碼並提交到指定 Git repo。需要人類決策、付款、登入、送信或其他對外 action 時，應把摘要與明確 action 帶回 Lark。

## 4. 工作型態與成果

| 工作型態 | 主要入口 | 典型工作 | 結果 |
|---|---|---|---|
| 一次性行動 | Lark | 報價、ERP、文件、採購、回信、短暫處理 | 可審核的 action、draft 或 result |
| Web research | Web workbench | 查閱、比價、研究、來源整理、長對話 | 來源清單、結論與 research artifact |
| Knowledge context | Web workbench + Git | 流程、FAQ、專案知識、可重用規則 | 可檢索且可 review 的知識 artifact |
| Project context | Web workbench | research、dev、it 等上下文分流 | project log、task、code 或 infra context |

## 5. 功能情境

### 5.1 Web research：查閱、比價、來源整理

使用者可以在 Web workbench 要求研究二手 Mac mini M4 16G/512 行情、比較多家 RAM 供應商報價，或讀取 PDF 報價單與截圖找出條款差異。

- 整理來源、價格區間、交期、付款條件、風險與待確認事項。
- 研究過程以 stream 回傳，圖片、表格、PDF 與截圖可留在同一工作上下文。
- 結果先形成 artifact，再選擇保存到 project、提交 Git，或回 Lark 給採購群摘要。
- 付款、登入、送信與建單等 action 不在 research 階段直接執行。

### 5.2 Knowledge context：把結果變成可重用規則

使用者可以要求把 RAM 採購研究整理成供應商評估規則、把 IT 排障寫成 runbook，或從 Lark 討論提取決策、待辦與風險。

知識至少應有來源、摘要、決策、版本、project 與權限邊界。IM 對話是事件流，不是主要知識庫；可重用內容應保存為乾淨結構，並可在需要時接本地 LLM 或私有檢索。權威知識的正本在 private Git，執行期以 mount／sync 提供讀取，見 [架構規格](architecture.md#21-權威知識的執行期掛載)。

### 5.3 Project routing：research、dev、it 分流

不同 project 有不同工具、文件、權限與預設工作模式：

- research：公開 research、比價與來源整理，預設不動內部系統。
- dev：程式碼、issue、PR、產品功能與技術設計。
- it：主機、Cloudflare、PVE、部署、服務排障；不混入公司業務知識。
- business / ops：報價、ERP、採購與客戶聯絡，採用較嚴格的資料與 action policy。

Project routing 同時是安全邊界、上下文品質控制及成本控制。同一資料域可以掛多個 runtime 入口，但 session 與（預設）browser 仍隔離。

### 5.4 工具邊界：只開需要的 tools

使用者應可預期：每個 project 只暴露所需的 shell、browser、MCP 與 skills，而不是全域工具池。

- 例：research project 預設無 ERP 寫入 MCP；business project 可開 ERP 讀寫但仍受 action policy 約束。
- 僅適用某一 runtime 的 skill 或儀式不得強加到其他 runtime。
- 細節見 [架構規格 · Tools surface](architecture.md#62-tools-surface-skills-與-mcp)。

### 5.5 即時查詢

agent 可以查 ERP、FileMaker、物流或公開網站，回答庫存、成本、訂單狀態、市場行情或入帳比對。關鍵資料應在回答時查詢來源，不依賴過期匯出或死 cache。

### 5.6 採購

典型流程是：從歷史報價找供應商、比較交期與條件、建立採購單草稿、草擬詢價信、整理廠商回覆，然後回 Lark 讓人審核。

agent 可完成研究、草稿與準備；實際送信、下單或付款必須依 action policy 取得明確批准。

### 5.7 銷售

agent 可從 ERP 或 Lark Base 讀取客戶折扣、庫存與歷史資料，建立報價草稿與 PDF，並放回群組供業務確認。人類確認後，可在同一個 browser session 開啟報價頁進行最終檢查與送出。

### 5.8 客戶與廠商聯絡

agent 可彙整 inbox 詢價、查訂單狀態、草擬回信、整理發票催款或先回覆收到訊息。標準流程是：查內部資料 → 草擬 → Lark 審核 → 確認後外發；過程要可追溯。

### 5.9 助理事務

可協助建週會、邀請人員、準備 OKR 表、整理月報、建立文件、管理待辦或搜尋行程。訂票、付款與其他需要真人輸入敏感資料的步驟，agent 會交給人類在同一 browser session 接手。

### 5.10 群組工作進度總結

agent 可把群組視為事件流，讀取當天或本週的討論、bot 執行紀錄與文件變更，產生討論重點、交辦清單、結果、耗時、未完成事項與週報。

群組訊息是重要事件來源，但正式的長期結論、作業紀錄與可回滾變更仍要輸出到 Git artifact；不能只依賴訊息歷史作為稽核或知識正本。

### 5.11 正式寫入後的驗證

對 ERP、後台或生產設定等正式寫入，使用者可預期 agent 會在**同一 project** 的 browser 或 API 做最小驗證後才回報完成；驗不了會明講哪段未驗證。禁止借用其他 project 的 browser 驗證本 project 的寫入。

## 6. 使用者可預期的 handoff

agent 遇到下列情況會向人類交接，而不是嘗試繞過：

1. captcha、OTP、2FA 或第一次登入。
2. 付款、下單、寄信、對外發文、正式資料寫入或其他需要批准的 action。
3. 權限、資料範圍或指令意圖不明。
4. 需要真人判斷商業條款、法律風險或敏感資料是否可以外送。

Browser 的 VNC 接手與 agent 的 CDP 操作必須指向同一個隔離 session，讓人完成必要步驟後 agent 可以續作。

### 6.1 執行失敗時的可預期行為

除人工決策外，基礎設施失敗也不應靜默吞掉：

| 情況 | 使用者可預期 |
|---|---|
| Runtime session 中斷 | 明確失敗摘要；支援 resume 時可續跑，否則需重開任務 |
| Browser／CDP 斷線 | 停止相關步驟，並提供正確 project 的接手入口 |
| 半套 Git 變更 | 不宣稱完成；附 branch／PR 狀態 |
| 寫入後驗證失敗 | 標明未驗證段落與建議人工檢查點 |

細節見 [架構規格 · 失敗與接手](architecture.md#111-失敗與接手)。

## 7. v1 範圍

### 7.1 v1 必做

- Ubuntu LTS、Docker、Node 20+。
- 已登入的首批 code agent CLI（Runtime Provider）。
- Lark bot 與 Web workbench 入口。
- 可由人接手的 BrowserProvider session。
- Project 隔離、Git-first 長期保存、最小 action policy。
- Project 級 tools allowlist（skills／MCP／shell／browser）。

### 7.2 v1 可選

- Orchestrator runtime（多 worker 互審）。
- Domain-shared browser profile。
- 進階併發／額度排隊策略。

### 7.3 不列入 v1 必做

- 完整管理後台與多租戶營運介面。
- 所有非首批 runtime 的正式支援保證。
- 完整本地 LLM 部署包、GPU／音訊。
- CLI 認證或 API key 生命週期管理。
- 排程／自主 cron 任務的完整產品化。

與架構規格的範圍清單應對齊；衝突時以 [architecture.md §13](architecture.md#13-範圍與暫不處理) 為準。
