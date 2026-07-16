# 功能規格

> WIP。這裡寫「人能幹嘛」；狀態、權限、部署細節看 [架構規格](architecture.md)。

## 1. 在解決什麼

辦公室雜事多半是：開瀏覽器、登系統、填表、複製貼上、回信——庫存、物流、訂單、採購、報價、客服。另一類是：查外面資料、比價、整理來源，結論之後還要給不同專案用。

三個入口：

1. **Lark** — 短任務、通知、審核、叫人進來。  
2. **Web 工作台** — 長對話、stream、圖／檔、研究與草稿。  
3. **Browser** — 已登入的真實系統；AI 走 CDP，人走 VNC，同一個 session。

模型跟工具決策交給 Claude Code、Codex 等 CLI。osslab-agent 管路由、session、project 上下文、能開哪些工具、什麼要批、browser 與人接手。

一人可以掛多個 bot；團隊也可以按角色或流程拆。規範跟知識可以共用，但對話、browser 登入態、bot 帳號、工作目錄要分開（見架構）。

## 2. Lark

v1 的行動與審核走 Larksuite：群、私訊、文件、Sheet／Base、信、日曆、Bot、卡片。

適合當**事件口**，不適合當唯一知識庫。交辦、通知、批准、接手摘要留在 Lark；長研究與可重用結論在 Web 做完，整理成檔案再進 Git。

沒有完整 ERP 的團隊，可以先用 Lark Base／Sheet 管客戶、庫存、採購；agent 用 Lark API 讀寫。之後上 ERP 再決定哪塊留 Base、哪塊搬家。

## 3. Web 工作台

長任務就開這裡，不是「順便有個 chat」。支援 stream、貼圖貼檔、研究草稿、依 project 分開上下文。

對話本身可以暫存；要交接、review、長期用的，輸出成 Markdown／資料／程式碼 commit 到指定 repo。需要人決定、付款、正式外發時，摘要跟要做的 action 拉回 Lark。

## 4. 工作怎麼落

| 型態 | 多半從哪進 | 結果長什麼樣 |
|---|---|---|
| 短行動 | Lark | 草稿、結果、或等人批的 action |
| 研究／比價 | Web | 來源、結論、研究筆記 |
| 沉澱規則 | Web + Git | runbook、FAQ、可 review 的知識 |
| 分 project | Web | 各自 log／code／infra 上下文 |

## 5. 情境（舉例，不是功能清單上限）

**研究／比價**  
在 Web 查行情、比供應商、讀 PDF／截圖。過程可以 stream；結果先當筆記，再決定 commit 或回 Lark 摘要。研究階段不做付款、送信、正式建單。

**沉澱**  
把採購研究寫成評估規則、把排障寫成 runbook、從群組討論抽出決策與待辦。至少要標來源、摘要、決策、版本、屬於哪個 project。群訊息不當長期正本。

**Project 分流**  
- research：公開資料為主，預設不動內部系統  
- dev：code、issue、PR、設計  
- it：主機、部署、排障，別跟業務資料混  
- business／ops：ERP、報價、採購、客戶；權限更嚴  

同一塊資料可以掛多個 runtime 入口，但 session 預設分開；browser 預設也分開。

**工具別全開**  
每個 project 只開需要的 shell、browser、MCP、skills。research 不必掛 ERP 寫入；某家 CLI 專用的 skill 別硬塞給所有 runtime。細節在架構。

**即時查詢**  
查 ERP、物流、公開網站等。該查當下來源，不要靠過期匯出裝準。

**採購**  
找歷史報價、比條件、建採購草稿、草擬詢價、整理回信 → 回 Lark 等人。送信、下單、付款要明確批准。

**銷售**  
從 ERP 或 Base 抓折扣與庫存，出報價草稿／PDF 回群。人確認後可在同一 browser 打開頁面做最後檢查再送。

**對外聯絡**  
整理 inbox、草擬回信、催款清單。流程是：查內部 → 草稿 → Lark 審 → 再外發。

**助理雜事**  
開會、文件、月報、待辦。訂票、付款、填敏感資料：人在同一 browser 接手。

**群組進度**  
把群當事件流，整理當日／當週討論與 bot 結果。週報可以，但正式結論與可回滾變更仍要進 Git。

**寫進正式系統之後**  
改 ERP／後台後，應用**同一個 project** 的 browser 或 API 做最小確認再回報「好了」；驗不了就講清楚哪段沒驗。別借隔壁 bot 的 browser 驗自己的寫入。

## 6. 什麼時候該把人叫進來

- captcha、OTP、2FA、第一次登入  
- 付款、下單、寄信、正式寫入等要批的動作  
- 權限或意圖搞不清  
- 條款、法務、敏感資料能不能外送，需要人判斷  

VNC 與 CDP 必須是同一個隔離 session。

另外，東西壞了也別裝沒事：CLI session 掛了要說清楚（能 resume 再續）；CDP 斷了就停 browser 步驟並給正確接手連結；Git 只推了一半就別說完成；寫入後驗不過就標未驗段落。

## 7. v1 範圍

**做：** Ubuntu LTS + Docker + Node 20+；已登好的首批 code agent CLI；Lark + Web 工作台；可人接手的 browser；project 隔離；結果進 Git；基本批准規則；tools 按 project 開。

**可選：** 多 worker 互審那種 orchestrator、少數 domain 共用 browser、比較完整的排隊／額度策略。

**先不做：** 大管理後台、多租戶、保證支援所有 CLI、整包本地 LLM、GPU／音訊、代管 CLI 登入、完整 cron 自主任務產品化。

範圍若跟架構文件衝突，以 [架構 §13](architecture.md#13-v1-做與不做) 為準。
