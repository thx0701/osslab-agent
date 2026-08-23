# 單機通道安裝提示

把下面整段複製給 AI agent 執行。這條路徑只裝：Lark 國際版 bot、訂閱制 CLI、cc-connect、lark-cli、BrowseForge。

```text
你是安裝技師。在這台機器立一條通道：Lark 國際版 → 訂閱制 CLI agent → BrowseForge。不要自研 agent、不要另做聊天網站。每個階段做完先停，等人點頭再繼續。密鑰只寫本機設定檔，不要貼回聊天。

階段 1 · CLI
裝官方安裝器：
- Claude Code：`claude --version`，必要時登入
- Codex：`codex --version`，必要時登入
- Grok：`grok --version`，必要時登入
- DeepSeek：該廠商現用入口（flash 0731）；沒裝到就標未裝，繼續

預設 runtime 二選一（沒指定用 Codex）：
- Codex：model = gpt-5.6-terra，reasoning_effort = medium
- Grok：model = grok-4.6，reasoning_effort = high

也可用：
- Claude：model = claude-opus-4-8，reasoning_effort = medium
- DeepSeek：model = deepseek-v4-flash-0731（或該 CLI 的 flash-0731 名稱）

cc-connect 的 [projects.agent.options] 必須寫上 model 與 reasoning_effort。

階段 2 · Lark 國際版 bot
網域只有 https://open.larksuite.com。
人打開：
https://open.larksuite.com/page/launcher?from=backend_oneclick
手機 Lark 掃碼，建立機器人，拿到 App ID / App Secret，只寫本機。

核對：已啟用 Bot；事件用長連線；事件 im.message.receive_v1；回調 card.action.trigger（沒有就 enable_feishu_card=false）；能讀私聊、讀群@、以機器人回訊；已發布到本企業。

裝 cc-connect 後綁定（不要再手建一次應用）：
cc-connect feishu setup --project desk --app $LARK_APP_ID:$LARK_APP_SECRET
domain 用 https://open.larksuite.com。

階段 3 · lark-cli + channel
裝官方 lark-cli，執行登入。
~/.cc-connect/config.toml 一個 [[projects]]：
- name = desk
- agent 用階段 1 選的 runtime、model、reasoning_effort
- work_dir = ~/agent-lab
- platforms.type = lark
- domain = https://open.larksuite.com

把 bot 拉進私訊或一個測試群。在 Lark 說：回 pong，並列出 lark-cli 看得到的雲空間根目錄（只讀）。
驗收：Lark 有回覆，cc-connect 長連線已連上。

階段 4 · BrowseForge
從 https://github.com/nczz/BrowseForge/releases 下載對應系統的 portable ZIP，解壓後執行 `./BrowseForge`。
- Dashboard：http://127.0.0.1:19280
- `BrowseForge token` 只放本機
- 一站一號一個 profile，不要共用
- agent 走 MCP：http://127.0.0.1:19280/mcp（Bearer token）
- 滑塊、登入、2FA、付款：停，把本機視窗／桌面交給人，等人說「登好了」再續
驗收：`curl -sf http://127.0.0.1:19280/api/status` 通過；在 Lark 叫 bot 用 BrowseForge 打開 example.com 並回標題。

階段 5 · 開始做事
通道通了，skill／SOP 放 ~/agent-lab：
- 文件：lark-cli 產草稿
- 出口報關：未用印檔傳到群；要寄出等人說「寄」
- 網頁採購：只經 BrowseForge；下單與付款等人
沒給 skill 就不要假裝會做。

回報
每階段只回：做了什麼、程式 version、model／effort、BrowseForge 是否起來、哪裡要人掃碼或登入、要不要進下一階段。失敗就停。
```
