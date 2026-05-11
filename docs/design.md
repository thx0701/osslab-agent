# osslab-agent — 團隊 + AI 同事協同作業架構

> [!NOTE]
> 🤝
> **osslab-agent 是什麼：這是利用各家類訂閱制 code 作為 agent(可合規使用訂閱制,減少AI API成本)**
> 但也可以串接本地LLM架構保留隱私的AI agent架構系統.
> 一套完整的 **「真人 + AI 同事在同一個工作群組裡協作」** 自架方案。AI 不是按鈕、不是聊天視窗，是**群裡的一位**，跟其他同事一樣有對話歷史、能 reply email、能查 ERP、能寫文件、能解 captcha 求救。
> **本 repo：**`thx0701/osslab-agent` · 自架部署腳本 + chrome 容器 image

# 1. 解決什麼問題

現代辦公室每天的雜事——**查資料**（包含高變動性資料如庫存 / 物流 / 訂單狀態）、**採購**、**銷售**、**客戶聯絡**、**跑助理事務**——絕大部分都是「打開瀏覽器、登入某個系統、填表單、複製貼上、回信」。

傳統做法：每人開一堆分頁手動切換，或寫一堆 RPA 腳本（脆弱、難維護、跑不起來時沒人懂）。

osslab-agent 的解法：**把 AI agent 變成群裡的同事**。它會用真實的 Chrome 操作各種系統，遇到驗證碼 / 2FA / 要刷信用卡求救，人類點兩下接手 5 秒搞定。

**單人也用、團隊也用——關鍵是「一人 N bot」都成立。**單人創業可以一個人配 N 個 bot——採購 bot、客服 bot、業務 bot、市場 bot——等於一個人就擁有一支 AI 助理小隊；團隊版同樣**每個業務角色 / 每個工作流配一個獨立 bot**，多個真人 + 多個 bot 共同進駐 Lark 群。**bot 數量跟人數沒綁**，採購 bot 一隻 vs 多隻、市場 bot 是不是要分海內外、業務 bot 要不要按客戶等級拆——你自己看工作流配。各 bot 各跑各的（一 bot ≡ 一 chrome 容器，登入 vault 隔離），但**所有交辦、操作、結果都在群裡可見**——誰在哪個時間交辦什麼、做到哪、結果如何，群訊息歷史就是全程的稽核紀錄。「每個人都擁有自己的真實 AI 助理（甚至好幾個）」這件事過去只有極少數高層才有，現在每個團隊成員都能擁有——這比起「集中式 AI 入口 + 共用對話視窗」是質變。

**不只外部系統。**除了 Odoo / WooCommerce / FileMaker 等外部 ERP / 電商，**Larksuite 自己的雲端文件 (Docx)、電子表格 (Sheet)、多維表格 (Base) 本身常常就是工作流主場**——很多小團隊根本還沒上 ERP，就用 Lark Base 當客戶 / 訂單 / 產品 / 庫存資料庫，AI agent 直接透過 lark-cli 讀寫這些 Base、寫 Docx 報告、跑 Sheet 試算，這些也算「真實同事」的日常工作。

**帳號架構也是長期戰。**多人、多角色、多 bot、多外部系統登入——怎麼配才不會亂、新人接手怎麼一鍵交接？分兩層配：**(1) 每個真人角色一組獨立身份，貫穿 Lark / Email / 密碼庫三件事**（例 `purchasing@yourdomain.com` 同時當 Lark 登入帳號 + 對外私有聯絡信箱 + Bitwarden vault master 帳號，一組通用三件事，新人接該角色只交接這一組）；**(2) 每個 bot 配一個獨立的 web CDP chrome 容器**（一 bot ≡ 一容器，CDP / KasmVNC port、登入 vault、cookie、profile 全隔離），真人或項目在自己對應的 bot 容器裡用該角色身份登入各系統。容器內建 Bitwarden 擴充（強制安裝、使用者卸不掉；推薦自架 Vaultwarden、open-source、256MB RAM 完全免費），帳號到密碼整套打包好。詳細策略表 + 公用收件匣應用方式見 §9.2。

# 2. 為什麼選 Larksuite 當 AI 協同的關鍵 IM

osslab-agent 把 IM 平台抽象出來，**v1 鎖定 Larksuite (飛書國際版)**，因為它是當代最好的**免費 / 付費**「團隊協作 IM」：

| 能力 | 為什麼強 |
|---|---|
| **IM** | 群組 / 私訊 / 線程 / 視訊全包，介面比 Slack 直觀，比 Teams 輕 |
| **雲端文件** | Docx / Sheet / Base / Whiteboard / Slides 全套，多人即時協作不打架 |
| **免費 Email Server** | 自有網域信箱，整合在同一個 app 裡（這在現代 Team IM 裡幾乎絕跡） |
| **行事曆 / 會議** | 會議自動轉妙記、AI 摘要、待辦自動建 |
| **免費額度** | 20 人以下完全免費，免費 Email Server + 線上文件 100G 容量 新創 / 中小團隊零成本 |
| **OpenAPI** | 所有功能都有完整 API，這就是讓 AI agent 接管的入口 |
| **Bot 平台** | 事件訂閱（WebSocket long-link）、訊息發送、互動卡片、權限分級全都有，bot 能力在當代 IM 裡屬於頂級 |

## 2.1 Lark Sheet / Base 可直接作為輕量進銷存主場

Larksuite 不只是 IM 和文件工具，**Sheet（表格）與 Base（多維表格 / 多維表單）本身就能承接很多中小團隊的進銷存、客戶、訂單、產品、庫存資料管理**。對還沒導入完整 ERP 的團隊，可以先用 Lark Base 當資料庫，用 Sheet 做試算與報表，再讓 AI agent 透過 `lark-cli` 讀寫資料、產生報告、協助查詢與更新。

- **多維表格 / 多維表單功能強大**：可用表格、看板、日曆、表單等視圖管理資料，適合把客戶、商品、庫存、採購、銷售流程先結構化。
- **進銷存可先用現成模板起步**：[Inventory Stock Sheet Template](https://www.larksuite.com/zh_tw/blog/inventory-stock-sheet-template)
- **教學參考**：[飛書多維表格 / 進銷存相關教學](https://www.feishu.cn/content/article/7582519149600017604)

這也是 osslab-agent 選 Larksuite 的關鍵原因之一：很多工作流不一定要先接 Odoo / FileMaker，**Lark Sheet + Base 就可以先成為團隊的第一版作業系統**，AI agent 直接在同一個 Lark workspace 裡讀寫資料、更新文件、產生報表。

# 3. 應用範圍（範例，不是規範）

## 3.1 查資料（含高變動性資料）

```
@bot 倉庫 Mac mini M4 16G/512 剩幾台？最便宜成本多少？@bot 客戶 ABC 上週訂單跑到哪一步？查 Odoo + 物流追蹤@bot 蝦皮 / FB Marketplace 同款 iPhone 15 Pro 256G 現在大概什麼價位？@bot 銀行帳戶今天有沒有客戶 ABC 的匯款入帳？金額對不對？
```

- AI 開 Odoo / FileMaker 即時撈內部資料、開瀏覽器看公開行情
- 關鍵：**不靠死的 cache，每次都查最新**，避免「資料庫匯出時是準的、AI 回答時已經過期」

## 3.2 採購

```
@bot 客戶要 10 台 Mac mini M4 16G/512，找供應商 A、B 過去 3 個月報價歷史，建採購單草稿在 Odoo@bot 寫封詢價信給廠商 XYZ：RAM 16G x100，cc 我，先丟草稿不要直接送出@bot 廠商 ABC 昨天那封報價回信整理重點貼出來，跟我們上次採購價比一下
```

- AI 在群裡 @採購：「需求 X x10，建議供應商 A/B 報價歷史 yyy」
- 確認後 AI 在 Odoo 建採購單草稿、寫 email 跟廠商詢價、把回信整理回群

## 3.3 銷售

```
@bot 打一張報價單給張先生（聯絡人 C001），項目跟上次一樣 Mac mini M4 16G/512 x10，PDF 直接寄到他信箱@bot 沒 ERP 也行：用 Lark Base「客戶聯絡人」表抓 Allen Wu 的 email + 折扣率，套 Lark Doc 報價單模板寄出@bot 客戶 ABC 報 10 台，從 Lark Base 抓他的歷史折扣，建好草稿丟回群讓我審
```

- AI 從 Lark Base / ERP 抓客戶歷史折扣、查庫存、建報價單、出 PDF、丟回群
- 業務確認 → 一鍵打開報價單頁面（同個容器、同個登入 session），人類審完按送出

## 3.4 客戶 / 廠商聯絡（Email + IM）

```
@bot 把今天 inbox 客戶詢價的信整理清單貼到本群@bot 客戶 ABC 剛才那封問訂單狀態的信，查到狀態後草擬回信丟給我審@bot 廠商發票催款信幫我列一份本月還沒付的清單@bot 客戶 XYZ 的 Lark 私訊我來不及回，幫我先回「明早 9 點前回覆」
```

- AI 從內部系統查狀態 → 草擬回信 → 在 Lark 群丟給人類審核 → 確認後送出
- 所有過程留在群組訊息，可審計可重播

## 3.5 助理事務（會議 / 報表 / 待辦 / 雜事）

```
@bot 明天下午 3 點開週會，邀  /  / 我，準備 OKR 進度表，建會議文件@bot 整理本月銷售 top 10，貼到「月報」doc，ping 老闆@bot 幫我買 6/15 台北→東京華航直飛經濟艙，行李 23kg，刷卡那段我會在頁面手動填@bot 我下班前還沒結的待辦清一遍，沒做完的順延到明天
```

- 建會議 / 拉表 / 寫文件 / 訂機票 / 管 OKR — 一句話搞定
- 會中飛書妙記自動錄音 / 轉文字 / AI 摘要、會後 AI 把待辦建進每個負責人的清單

## 3.6 群組工作進度總結（meta-application）

這個應用最特別：**AI 看的不是外部系統，而是*****群組訊息歷史本身***。它讀今天 / 本週群裡所有人的對話、各 bot 的執行紀錄、文件變更，整理成結構化進度報告 — 過去要人手翻訊息、抓重點，現在一句話。

```
@bot 總結今天本群討論重點 + 各 bot 執行狀況，貼到「日報」doc@bot 把本週各業務的訂單成交、客戶聯絡、未處理事項列成週報@bot 整理今天 09:00-18:00 群裡 @bot 的所有請求清單、結果和耗時@bot 過去 3 天我交辦了哪些事？哪些還沒回？條列出來
```

> [!NOTE]
> 💡
> 把 IM 群當成**事件流（event stream）**，AI 是這條 stream 的觀察者兼整理者。所有對話、決策、AI 操作紀錄都留在群裡 — **可審計、可重播、可彙總**。

# 4. 為什麼這套組合能做到上面這些 — Larksuite + lark-cli + Claude Code + CDP + KasmVNC = 質變

看完應用範圍你大概會問：「這些事 AI 早就能做了，有什麼特別？」關鍵是**五件事的化學反應**：Larksuite 把 IM、Email、雲端文件、行事曆、任務、視訊全塞在同一套 OpenAPI 後面；lark-cli 把這套 OpenAPI 包成 shell 指令，AI agent 一句話就能用，不用你自己拼 IMAP / Calendar / Doc 等十幾個 SDK；Claude Code 在外面接 MCP（Playwright MCP server）負責決策跟工具調用；MCP 透過 **CDP（Chrome DevTools Protocol）**直接驅動 Chrome 容器，沒 OpenAPI 的網站也能進得去；最後 **KasmVNC web VNC 把同一個 Chrome 容器再以 web 推送出來**——AI 跟真人**共用同一個瀏覽器、同一個登入 session、同一份 cookie**，AI 跑到一半遇到要刷信用卡、過 hCaptcha、解 2FA、第一次登入新網站，人類從 Mac / iPad / 手機隨便一台打開 web VNC 接手 5 秒搞定，搞完 AI 接著做不會 session 斷。這正是其他自動化方案最常缺的最後一塊拼圖：headless puppeteer / 純 RPA 腳本卡關時只能 fail，這套方案**卡關時就求救人類，人類處理完 AI 無縫接續**。五件事疊起來，AI agent 才能像個真同事一樣讀 inbox、寫回信、改文件、查 ERP、訂機票，而不是「按一個按鈕跳出來的助理」——它是**群裡的一位**，能 mention、能 reply、能等人類審完再送出。

本版本**只支援 Claude Code（Anthropic 官方 CLI）**，搭配個人或團隊 Claude 訂閱制即可使用——不需要你自己管 API key、不需要 Bedrock / Vertex 帳單。

架構天生支援**多人 + AI 同事在同一個 Lark 群組裡協作**：多個真人 @ 同一個 bot、多個 bot 互相 @、單人單 bot 也能跑——人多 / 人少都能用。所有對話、AI 操作紀錄留在 Lark 群裡，**可審計、可重播**；cc-connect 後台同時保留每個 session 的詳細日誌、工具呼叫紀錄、stdin/stdout，雙重溯源——出問題能查、回顧誰在哪一步指示 AI 做了什麼，跟翻人類同事的訊息歷史一樣自然。

# 5. 技術架構

從一條 Lark 訊息到網頁實際被點擊，經過幾層 daemon 跟 protocol：

```
Lark 群組訊息  ↓ WebSocket long-link (Lark 即時推送 / cc-connect 內建 client)cc-connect (bridge daemon, systemd --user)  ↓ spawn subprocess + JSONL stdio (ACP-like 協議)Claude Code agent (claude CLI; 一個 bot 一個 session 進程)  ↓ MCP protocol (stdio transport)Playwright MCP server (npx @playwright/mcp; Claude 喚起時 spawn)  ↓ CDP over HTTP / WebSocketchrome 容器 (kasmweb/chrome 改造版, --remote-debugging-port)  ↓ DOM 操作 / 鍵盤滑鼠事件 — 跟人手一樣網頁 (Lark 後台 / Email / Odoo / WooCommerce / FileMaker / 任何系統)
```

**各元件的角色 + 誰提供：**

| 元件 | 角色 | 提供方 |
|---|---|---|
| **Larksuite + 開放平台** | 團隊工作台（IM / Docs / Mail / Calendar），建 bot、開 scope、訂事件、WebSocket 推訊息 | 外部（免費 / 付費） |
| **cc-connect** | Lark 訊息 ↔ Claude Code session 的 bridge daemon（[chenhg5/cc-connect](https://github.com/chenhg5/cc-connect)） | 外部 npm |
| **Claude Code** | Anthropic 官方 CLI（用個人 / 團隊訂閱合法使用）— 真正的 AI agent 大腦 | 外部（建議訂閱制） |
| **lark-cli** | Lark API 的 CLI 封裝（agent 操作 Lark 的工具箱） | 外部 npm |
| **Playwright MCP** | 把 CDP 包成 MCP tool，Claude 透過它 navigate / click / fill / screenshot | 外部 npm |
| **chrome 容器** | AI + 人共用的瀏覽器（中文輸入、CDP 對外、登入持久化、web VNC、Bitwarden） | ✅ **本 repo**（ghcr.io image） |
| **osslab-agent CLI** | 把上述全部串起來的安裝 / 卸載腳本 | ✅ **本 repo**（npm package） |

> [!NOTE]
> 🧠
> **每個 bot 獨立 session 進程**——多 bot 同時跑互不干擾、登入狀態 volume 隔離。

# 6. Chrome 容器（本 repo 的真心力作）

> [!NOTE]
> 🐳
> **整套架構最容易被低估、但其實最關鍵的一塊。**「AI 用的瀏覽器」必須跟「人也能接手用的瀏覽器」**是同一台** — 才能無縫切換、共用登入、人類隨時介入解 captcha。這需要在 `kasmweb/chrome` 上做一輪精雕細琢的 patch。

## 6.1 為什麼選 Kasm + 自製 patch（vs RustDesk / NoVNC / Guacamole）

| 項目 | 優勢 |
|---|---|
| **中文輸入順暢** | 實測**比 RustDesk 在 Linux 桌面好太多**（RustDesk 切不了輸入法、注音卡頓）。fcitx-chewing + ui-classic + xdotool 注入 — Mac/Win/iPad 都打得出注音 |
| **輕量** | 單容器閒置 ~700 MB RAM、CPU < 2%；Image 共用 5.24 GB，多 bot 不重複佔空間 |
| **真.瀏覽器** | 完整 Chrome（不是 puppeteer headless），帳號 cookie / 擴充 / 書籤都跟人類用的一樣 |
| **Web 多端進入** | KasmVNC HTTPS — Mac Chrome / Windows Edge / iPad Safari + 軟鍵盤 / 藍牙鍵盤都實測過，**不需要裝任何 client** |
| **登入持久化** | volume 掛 user 目錄，cookie / Bitwarden vault / 擴充設定全留，重啟容器不用重登 |
| **CDP 對外** | 解掉 Chrome 138+ 強制 9222 綁 127.0.0.1 的限制（socat 轉 9223），AI agent 從容器外就能 control |

## 6.2 內建 Bitwarden — 密碼管理是長期戰

> [!NOTE]
> 🔐
> **每個 chrome 容器都預先強制安裝 Bitwarden 擴充功能。**這樣團隊共用 vault：
> - 所有 bot 用同一個密碼庫（人類同事也共用）— 帳號集中管理、權限分級
> - 新人入職 / 離職 / 改密碼，從 Bitwarden 後台一動作搞定
> - 未來會擴充：AI agent 主動透過 Bitwarden API 取認證填表，免去人類複製貼上
> - 容器層次強制安裝（Chrome managed policy）— 使用者卸不掉，安全合規

## 6.3 真人介入機制

實際使用 AI agent 操作網頁時，**遇到三類情況人類接手 5 秒搞定**：

1. **Captcha**（hCaptcha / Cloudflare / Google reCAPTCHA）
2. **OTP / 2FA**（簡訊驗證碼、Bitwarden Authenticator 取碼）
3. **第一次登入**（每個網站第一次 cookie 還沒存）

機制：AI 在 Lark 群提示「需要人工介入」+ 附 web VNC 連結 → 人類點開 → 解掉 → AI 繼續 — 整個過程跟「同事問你密碼是什麼」差不多自然。

👉 容器內部技術細節（Dockerfile / autostart / fcitx 設定）見 [Kasm Chrome Bot 容器：從零搭建指南](https://byo9fekr2o.sg.larksuite.com/docx/RAIwdKsj5or9F1xN8e4l5dCXgFf)

# 7. 資安設定方向

> [!NOTE]
> 💡
> AI agent 能做事是雙面刃——能查 ERP、能寄 email，意思是**權限沒切好就能闖禍**。本架構的資安主要從兩個面向控管：Larksuite 後台 + chrome 容器密碼策略。

## 7.1 Larksuite 後台：bot 權限分級（誰能 @ bot）

Larksuite 後台可以設定 bot：

- **哪些群組能加**——預設不要全公司開放，只把 bot 加進真正需要它的群（採購群 / 銷售群 / 客服群分開），跟人類「誰能進什麼群」一樣的邏輯
- **哪些用戶能 @**——可在 bot 程式裡白名單檢查 sender_id，非白名單成員 @ 會被忽略，避免 stage / external 用戶亂打
- **事件 scope 最小化**——只訂閱真正需要的事件（im.message.receive_v1 / mail.user.received 等），不要全開
- **OpenAPI scope 最小化**——bot 用的 app token 只開必要的 scope（例：只送 IM 不能讀 contact），權限漏洞範圍可控

## 7.2 Chrome 容器：密碼管理兩種策略

每個 bot 對應一個 chrome 容器，登入狀態 volume 隔離。密碼怎麼存看你的資安政策：

> [!NOTE]
> 🔓
> **不存密碼，但用 Bitwarden 管理器**
> Chrome 不開「自動儲存密碼」，但 Bitwarden 擴充正常掛著。每次需要新登入時人類 web VNC 進去用 Bitwarden auto-fill，cookie 留下、密碼**不留在容器裡**。安全度高、但每個新網站第一次得人手介入。

> [!NOTE]
> 🔒
> **長期儲存於容器**
> Chrome 內建密碼儲存 + Bitwarden vault 都長期保存，cookie + 密碼同步在 volume 裡，重啟容器不用重登。最方便、但容器若被攻破密碼一次外洩；建議搭配 Bitwarden vault master password + 2FA、容器主機加防火牆。

視團隊資安政策跟便利性需求調整。一般工作流推薦**「不存密碼但用 Bitwarden 管理器」**——平衡點最好。

# 8. Quick Start

> [!NOTE]
> 🚀
> **前提條件**：Ubuntu LTS 主機 + Docker + Node 20+ + 已設定好的 Claude Code（`claude login` 完成）

```
# 跟著 wizard 互動完成（約 3 分鐘）npx osslab-agent init
```

腳本會引導你：

1. 偵測環境（Linux / Docker / Node / claude CLI）
2. 安裝 cc-connect + lark-cli + 跑 `lark-cli auth login`
3. 選 bot 名稱、自動分配 port
4. 填 Lark App ID/Secret（自動驗證）
5. 設 KasmVNC 密碼
6. 自動 `docker pull` chrome image、起容器、註冊 systemd

跑完打開 VNC、登入 Lark / Google / 各種網站，把 bot 加進你的 Lark 群組，@它說 hi。

👉 完整安裝規格見 [osslab-agent v1 安裝腳本規格](https://byo9fekr2o.sg.larksuite.com/docx/WtrhdMjLho2ipyxhln2lsAwbgLb)

> [!NOTE]
> ⚡
> **💡 最快建 Lark App 的方式（2026 新增）**
> 傳統流程要去開發者後台手動建 App、勾 scope、設 callback、生 secret——對新手不友善，跳坑跳不完。改走 **Lark 官方一鍵 launcher**：
> 1. 打開 [https://open.larksuite.com/page/launcher?from=backend_oneclick](https://open.larksuite.com/page/launcher?from=backend_oneclick)
> 2. 選頭像 + 填名稱（例 `採購助手` / `業務助手`）
> 3. 點「**立即創建**」（截圖下方）→ 自動完成應用配置（scope / callback / 事件訂閱模板都自動帶好）
> 4. 拿到 `App ID` / `App Secret` 後填回 wizard step 4 即可
> **對應上面的 step 4「填 Lark App ID/Secret」**——這條 launcher 是現在能找到最快、最少踩坑的取得方式。

![Lark 智能体应用一键 launcher 截图（填名稱→立即創建 即可拿 App ID/Secret）](docs/assets/img_1778392141449_0.jpg)

*Lark 智能体应用一键 launcher 截图（填名稱→立即創建 即可拿 App ID/Secret）*

# 9. 部署單位：一 bot ≡ 一 KasmVNC chrome 容器

> [!NOTE]
> 🤖
> **核心原則：每個 bot 對應一個獨立的 chrome 容器**——volume / 登入 vault / CDP / VNC port 全部隔離。多 bot 才是主要擴展方式，**不是「多人共用一個 bot」**。

## 9.1 多 bot：每個業務角色 / 工作流一個 bot

採購 bot 用採購帳號登 Odoo、客服 bot 用客服信箱、市場 bot 跑公開資料查詢——各跑各的、互不干擾，每個 bot 的登入狀態 / cookie / vault 都在自己的 volume。要加新 bot 就重跑 `npx osslab-agent init` 走一遍 wizard。

## 9.2 帳號架構：分兩層（真人角色 vs bot 容器）

實務上要分清楚「**真人角色身份**」跟「**bot 容器配置**」是兩件事：

- **真人角色（採購 / 客服 / 業務 / 市場...）**：一組獨立身份，貫穿 **Lark / Email / 密碼庫**三件事。新人接該角色 → 只交接這一組。
- **bot**：每個 bot 配一個**獨立的 web CDP chrome 容器**——CDP port、KasmVNC port、profile volume、cookie / vault 全隔離。真人在自己對應 bot 的容器裡，用該角色身份登入各系統。

| 層級 / 用途 | 怎麼配 |
|---|---|
| **真人角色 — 私有 email + Lark 登入** | 例 `purchasing@yourdomain.com` = 團隊角色名 + 公司網域。**只有負責該角色的人類看得到**，同時當 Lark 登入帳號、密碼重置信箱、Bitwarden master 帳號、敏感系統的對外身份。一組通用三件事。 |
| **真人角色 — Lark 公用 email（共享收件匣）** | 適合**長期對外聯絡**（例 `sales@yourdomain.com`）——多個真人 + bot 共用收信信箱，但**發信時切不同寄件者 + 不同簽名檔**，對客戶看起來像各自獨立的同事。Lark 內建「公用郵箱」原生支援。 |
| **真人角色 — Bitwarden vault 登入** | 直接用上面那組「私有 email」當 vault 帳號——Lark / 收信 / 密碼庫三件事用同一組身份，零記憶負擔。 |
| **bot — web CDP chrome 容器** | 每個 bot 一個獨立 kasmweb chrome 容器：CDP port（AI 用 Playwright MCP 透過 CDP 操作）+ KasmVNC port（真人用 web 接管）+ 自己的 volume（profile / cookie / 下載檔案 / vault 解鎖狀態）。真人用**自己的角色身份**進這個容器登 ERP、登銀行、登信箱，所有密碼存進容器內建的 Bitwarden。bot 之間 cookie / 登入 vault 完全隔離，不會互相污染。 |

> [!NOTE]
> 💰
> **密碼Bitwarden 要錢嗎？**看你的規模：
> - **個人 Free**：單人無限裝置 / 無限 vault items / 2FA — 完全免費，小團隊或單人創業夠用
> - **Teams Organization**：約 $4/user/month — 共享 collection、權限分級、稽核日誌
> - **Enterprise**：約 $6/user/month — 加 SSO、進階稽核、SCIM
> - **自架 Vaultwarden（強烈推薦）**：開源的 Bitwarden server reimplementation，本機 docker 起一隻 image，所有官方 Bitwarden client（Chrome 擴充 / iOS / Android / CLI）正常連接、**完全免費**，最小規格 256MB RAM 跑得動。osslab-agent 整體就是「自架 + 開源優先」，密碼管理推薦這條路。

# 10. 不在 scope 內

- 非 Ubuntu OS（v1 只測過 Ubuntu LTS）
- Web 管理後台（v2 計畫）
- 非 Claude Code 的 AI agent（Gemini CLI / Codex / 開源模型，v2+ 計畫）
- GPU 加速 / 音訊（kasmweb base 有，但本專案沒驗證）
- Claude Code 認證 / API key 管理（使用者自行 `claude login`）

# 11. License & Credits

- **本 repo**（osslab-agent + chrome 容器薄層）：Apache-2.0
- **Base image**：[kasmweb/chrome](https://hub.docker.com/r/kasmweb/chrome) by Kasm Technologies（自帶 license）
- **cc-connect** / **lark-cli** / **Claude Code**：各自 license，本 repo 不重新分發

# 12. 相關專案

- **Larksuite / 飛書**：[larksuite.com](https://www.larksuite.com)
- **lark-cli**：[github.com/larksuite/cli](https://github.com/larksuite/cli)
- **cc-connect**：[github.com/chenhg5/cc-connect](https://github.com/chenhg5/cc-connect)
- **Claude Code**：[docs.anthropic.com/claude/docs/claude-code](https://docs.anthropic.com/claude/docs/claude-code)
- **Playwright MCP**：[github.com/microsoft/playwright](https://github.com/microsoft/playwright)
- **kasmweb base image**：[hub.docker.com/r/kasmweb/chrome](https://hub.docker.com/r/kasmweb/chrome)
- **Bitwarden**：[bitwarden.com](https://bitwarden.com)
