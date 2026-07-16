# 架構規格

> WIP。這裡寫系統怎麼組、狀態放哪、權限怎麼卡；使用情境看 [功能規格](functionality.md)。

## 1. 怎麼拆責任

Claude Code、Codex 等 CLI 負責推理跟叫工具。osslab-agent 負責：訊息進哪個 project、session 怎麼掛、能用什麼工具、browser 誰用、什麼要人批、重要結果怎麼對回 Git。

幾個固定取捨：

- 不重寫 agent framework；CLI 當可換的 runtime process。  
- 日常優先吃訂閱制 CLI；本地模型／私有檢索當補充。  
- 長 session／stdio／process bridge，不賭一次性 `-p`。  
- Lark 管事件、通知、批准；能重用的東西進 Git。  
- Browser 是真 Chrome：AI 用 CDP，人用 VNC，同一 profile。  
- 規範與知識可共用；對話、browser 登入態、bot 身份、工作目錄必須分開。

多入口不是「同一個 agent 換皮」。驗收大致是：大家讀得到同一套已授權規範；A 的聊天不會出現在 B；A 的 cookie 不會串到 B；每個入口有自己的 bot、目錄、browser 接點（除非 project 明文允許共用 browser，見 §4）。

## 2. 長期真相：Git

程式、policy、playbook、研究結論、skill 定義，正本在 private Git（Forgejo／GitHub／Gitea 都行）。Lark 跟 Web 是工作面，不是 version control。

```text
Lark / Web / API
        ↓
project + runtime + browser
        ↓
branch → commit / PR → 人批
        ↓
private Git（可 review、可回滾）
```

實務上：

1. 重要結論、規則、code 要變成可 review 的變更。  
2. 重要 action 盡量對得回：request、repo、branch／PR、誰批的、結果。  
3. 對話、cache、下載暫存、browser profile、未定草稿是 runtime 狀態，不必每筆 commit。  
4. 不要每個對話開一個 repo；用 project repo 或專門的 knowledge／artifact repo。  
5. 密鑰、token、cookie、密碼、OAuth secret、可轉發的 invitation 永不進庫。

Git 是正本；機器上可以 read-only mount 或定期 sync 一份給 agent 讀。要改正本就走 branch／PR，不要靠「模型記得上次怎麼說」。

## 3. 狀態放哪

| 東西 | 正本 | 備註 |
|---|---|---|
| 要 review 的內容 | private Git | code、runbook、研究結論、skill |
| 機器上讀到的規範 | 同上，經 mount／sync | 執行期視圖 |
| 進行中對話／草稿 | session／Web | 要留再輸出 commit |
| 交辦與批准 | Lark + action 紀錄 | 事件流 |
| queue、cache、下載 | runtime | 可丟 |
| 密碼與 token | host secret／環境變數 | 不進 Git |

Web 可以當工作區，但「要不要長期留」聽 project 的 Git 規則。

## 4. Project

一個 project 大致綁：

```text
runtime + 工作目錄 + channel／bot 身份
+ 誰能做什麼 + browser 規則 + 工具白名單
+ 資料保留 + 哪些 action 要批
```

不是 UI 上的資料夾標籤。同一資料域可以掛多個 runtime（例如 Claude 跟 Codex 各一個入口），但各自 session；不能因此共用 cookie 或偷開對方工具。

**Browser 預設隔離。** 角色不同、客戶資料不同、高風險登入 → 各用各的 profile。  
**可以共用的情況：** 同一資料域、同一套資料規則、沒有跨客戶隔離需求，而且設定裡寫明。  
**不要共用：** 業務已登入的 bot 跟 research bot；不同客戶或不同權限域的 cookie／下載。

## 5. 資料怎麼走

```text
Lark 訊息                    Web 對話／圖／檔
        \                      /
         → channel → 選 project
                      ↓
              （可選）gateway
                      ↓
              session bridge（stream／stdio）
                      ↓
              runtime + 允許的工具
                      ↓
              browser（CDP／Playwright + VNC）
                      ↓
         ERP、信箱、電商、文件、網站…
```

產品路徑就是 channel → project → runtime session。前面可以再掛 webhook／auth gateway；不要假設一個 process 扛全部。

## 6. 元件

| 元件 | 幹嘛 |
|---|---|
| Lark | 事件、通知、Bot、文件、卡片 |
| Web 工作台 | 長對話、檔案、project 工作區、草稿 |
| channel／session bridge | 把人與訊息綁到正確 project／session |
| Runtime | 推理、叫工具、產出變更與摘要 |
| 工具（skill／MCP／shell…） | 按 project 開；見下 |
| private Git | 正本、review、回滾 |
| BrowserProvider | profile、CDP、VNC |
| 本地 LLM／檢索 | 可選 |
| osslab-agent CLI | 安裝與串起來 |

### Runtime 要對上什麼

「可替換」不是寫個產品名就好，至少要講清楚：

- session 怎麼起、怎麼停、能不能 resume  
- stream 怎麼吐進度、tool call、錯誤  
- 工作目錄跟 env（例如 CDP port）怎麼注入  
- 這個 session 看得到哪些工具  
- 斷線、額度用完、auth 過期時怎麼回報  

v1 以訂閱制 code agent CLI 為主。多 worker 互審那種 orchestrator 可以接，但是加分項，不是每個 runtime 預設都有；接了也一樣要遵守 session／工具／browser 隔離。

### 工具

工具是 project 邊界，不是全站外掛市場。

- 白名單：shell、browser、哪些 MCP、哪些 skill、哪些外部 API  
- skill 跟 policy 正本在 Git，機器上怎麼掛是部署問題  
- 某 runtime 專用的流程／skill 不要硬套到全部  
- MCP 的密鑰只放 host secret；掛了要掛得穩，掛不起來要看得出  

跨 project 不要默默繼承比較大的權限。

## 7. 身份、權限、批准

三件事別混：

1. **登入產品的是誰**（OIDC 等）  
2. **這個身份能進哪些 project、讀哪些資料、用哪些工具**  
3. **這一筆外發／下單／正式寫入有沒有人批**  

支援標準 OIDC。OSSLab 參考部署用 Authentik、上游可接 Lark；你也可以接自己的 IdP。Lark 的 bot secret、人員 web 登入、Git SSH／PAT，各走各的，不要用「有登入 Lark」就自動變 admin。

稽核時再分三個角色：

- **Identity** — 誰在用產品  
- **Git operator** — 誰 push／開 PR（人、bot、CI）  
- **Approver** — 誰批這個 action  

群組裡回一句「好」可以當批准，但要綁定那次 request 跟那一版內容／commit，舊同意不能套新動作。Bot 可以當 Git operator，高風險動作不能自己批自己。

### 批准大致怎麼切

| 類型 | 例子 | 預設 | 至少留下 |
|---|---|---|---|
| 讀 | 查狀態、公開研究 | 直接做 | request、來源、結果摘要 |
| 草稿 | md、信稿、code 草稿 | 直接做 | session 產物或 branch |
| 可回滾內部 | branch、PR、草稿資料 | 看 project | repo、branch、PR、驗證 |
| 外發／營運寫入 | 寄信、正式建單 | 要批 | 誰批、何時、結果、驗證 |
| 高風險 | 付款、刪資料、改權限、正式部署 | 二次確認或既定流程 | action 紀錄與怎麼救 |

### 寫完要驗

改 ERP、電商後台、prod 設定之後，用**同一個 project** 的 browser 或 API 做最小確認再講完成。借別人的 browser 驗、或驗不了卻說好了，都不算。

## 8. Browser

BrowserProvider 是執行資源，不是登入身份本身。每個 project 要寫清：用哪家實作、profile 怎麼隔離、CDP／Playwright 怎麼接、VNC 怎麼進、能登哪些站、下載與 cookie 留多久。

預設可以是改過的 Kasm Chrome：完整 Chrome、profile 持久、CDP、web VNC、中文輸入、可選 Bitwarden。也要能換 BrowseForge 這類已有的 profile 隔離方案，不要鎖死一個 image。

人接手多半是 captcha、2FA、第一次登入、付款。Agent 在原 channel 丟**正確 project** 的 VNC 連結；人做完，同一個 session 繼續。

Kasm 參考實作在意的點：Mac／Win／iPad 上 VNC 能打中文；image 共用、profile 分 volume；CDP 不要裸奔到未授權網路；Bitwarden 可強制裝，解不解锁、存不存密碼仍看 project 規則。

## 9. 密碼怎麼放

兩種都支援，預設建議前者：

1. **Browser 不存密碼**，人用密碼管理器 autofill，cookie 可留。新站第一次要人進。  
2. **密碼／vault 長期在隔離 volume**。方便，主機與 vault 防護要更嚴。  

Agent 不准讀出、印出 vault 內容，也不准把 secret commit 進 Git。以後若接 vault API，再另定權限與稽核。

**真人角色**（信箱、Lark、vault 帳號）跟 **bot 的 browser 設定**（CDP、VNC、volume）是兩層。交接角色、換密碼、重建 container 可以分開做；不要把「採購這個人」跟「採購那個 chrome volume」當成同一個帳號概念。

## 10. 資料邊界（建議切法）

- research：公開資料、比價  
- dev：code、issue、PR  
- it：infra、部署、排障  
- business／ops：ERP、報價、客戶；更嚴  

敏感內容優先本地；真要送外部模型就先摘要或遮。Lark bot 的事件 scope、OpenAPI scope、能進哪些群，能小就小。

## 11. 併發、額度、掛了怎麼辦

多 bot 吃訂閱，日常痛點是同時 session 數跟 rate limit。

- 每個 project 可限 concurrent；滿了就排隊或拒，並講清楚。  
- 額度用完可以降級：排隊、換已授權的其他 runtime、或只准讀／草稿。  
- 短 Lark 任務是否插隊長研究，由部署決定。

掛掉時：

- runtime 死了 → 能 resume 就 resume，否則在原 channel 講失敗，不要裝成功。  
- CDP 斷了 → 停 browser 步驟，給正確 VNC。  
- Lark webhook 重送 → request 要能幂等，同一 action 別外發兩次。  
- Git 推一半 → 附 branch／PR 狀態，別回「做完了」。  
- 寫入後驗不過 → 標哪段沒驗。

## 12. 安裝（v1 預期）

環境：Ubuntu LTS、Docker、Node 20+、已登好的 code agent CLI。

大致步驟：查環境 → 裝 channel router／Lark CLI／browser → 選 Lark 和／或 Web → 建 project（runtime、目錄、工具、browser）→ 設 App／OIDC，secret 只進 host → 起 browser 與 VNC → 註冊 service → 用低風險流程走一輪 request → PR → 批准。

### 參考部署怎麼對

| 概念 | 你可能用什麼 |
|---|---|
| private Git | Forgejo／GitHub／Gitea |
| 登入 | Authentik 或任意 OIDC |
| IM | Lark（其他之後再接） |
| Web 工作台 | 產品自己的；參考實作可對 cc-connect 類 |
| router | cc-connect 那類 bridge，前面可加 gateway |
| browser | Kasm Chrome、BrowseForge… |
| runtime | Claude Code、Codex、或其他對得上 §6 的 |

OSSLab 現況只是其中一種拼法。

### Lark App

要 App ID／Secret、callback／事件訂閱、最小 scope。一鍵 launcher 只是省事，scope 跟 secret 保管還是要檢查。Secret 不進 example config、commit、issue、聊天、截圖。

![Lark 建 App launcher 示意（不是唯一路徑）](assets/img_1778392141449_0.jpg)

## 13. v1 做與不做

**做：** Ubuntu LTS + Docker + Node 20+；Lark + Web；至少一種 CLI runtime 與 browser；project 隔離；Git 當正本；基本批准與寫入後驗證；tools 按 project 白名單。

**可選：** orchestrator runtime、domain 共用 browser、比較完整的排隊 UI。

**不做（v1）：** 非 Ubuntu、大管理後台／多租戶、保證支援所有 CLI、整包本地 LLM、GPU／音訊、代管 CLI 登入與 API key 生命週期、跨產品 SCIM 自動提權、完整 cron 自主任務產品、獨立大 audit DB（先用 Git + action 紀錄湊）。

## 14. License 與相關專案

本 repo 的薄層 MIT。Kasm、cc-connect、Lark CLI、Claude Code、Codex、Playwright、Bitwarden 各走原授權，這裡不重新打包它們。

相關：Larksuite／飛書、Lark CLI、cc-connect、Claude Code、Codex CLI、Playwright、Kasm Chrome、Bitwarden。
