# Kasm 使用者身分、CDP 邊界與 VNC secret 輪替 plan

> 狀態：規劃中，尚未變更現行服務。這份 plan 的目標是把「誰正在使用哪一個 browser／agent」變成可驗證的事實，同時移除共用 VNC 密碼與可直接連線的 CDP 風險。

## 要解決的問題

目前的修改版 KasmVNC Chrome 是單一瀏覽器容器：Cloudflare Access 可以保護進入網站的入口，但它本身不會把 Access 的使用者身分帶進 standalone KasmVNC 的 session。若多個人都進同一個固定網址與容器，稽核結果只能知道有人進來，不能可靠回答「誰操作了哪個 browser、哪個 agent 是否能控制它」。

另一個要先處理的問題是 VNC 密碼目前以部署設定中的共用值存在；這種值不能長期留在 compose 檔，也不應當作人員身分。CDP 同樣不是給人直接登入的入口：它一旦被網路直接碰到，就等同把已登入瀏覽器的控制權交出去。

## 結論：採用兩層身分，不只靠一道登入牆

本 plan 建議採用下列對應，所有紀錄以不可變的身分 ID 為主，不以可更改的姓名或 email 當主鍵。

| 層次 | 身分／物件 | 用途 |
| --- | --- | --- |
| 人員 | Authentik OIDC `sub`，並連到 Lark 企業使用者 ID | 唯一識別同事，處理到職、離職與 email 更名。 |
| Kasm | Kasm 使用者與 Kasm session ID | 識別誰啟動、觀看與接手哪個 Chrome workspace。 |
| Agent | `agent_id` 與能力設定版本 | 識別哪個專屬 agent 可以做哪些事；設定只能由管理者以 Git 變更。 |
| 工作 | Lark task／訊息或 Base 記錄 ID | 識別任務從哪裡來、誰交辦、是否需要審核。 |
| 控制權 | 短效 `control_lease_id` | 只在指定任務期間允許 agent 控制指定 browser；使用者接手、鎖定 Vaultwarden 或 lease 到期就收回。 |

每次工作至少寫入：`principal_id`、`agent_id`、`browser_session_id`、`kasm_session_id`、`task_id`、開始／結束時間、授權決策與結果位置。內容本身仍留在 Lark／業務系統；這份對應只保存必要的可追溯性。

## 方案選擇

### A. 以完整 Kasm Workspaces 採用原生 OIDC（建議試點）

Kasm **Workspaces** 是完整的多使用者平台，原生支援 OIDC、群組與 attribute mapping；它不是目前 standalone `kasmweb/chrome`／KasmVNC 容器加幾個環境變數就能取得的功能。官方的 [OIDC 設定文件](https://www.kasmweb.com/docs/latest/guide/oidc.html) 可作為 Authentik 串接依據。

在這個方案中，Lark 是人員帳號來源，Authentik 作為 OIDC IdP；Cloudflare Access 仍保留在外層保護公開網址。兩者使用同一個 Authentik 登入 session，第二次導向應是既有 session 的無感確認，而不是要求同事維護第二份帳密。

優點是 Kasm 原生知道登入者、workspace 與 session，使用者能從自己的 Kasm 入口啟動或接回 Chrome。代價是要新增完整 Kasm Workspaces 的控制面、資料庫與維運流程，且 agent 仍不可直接「因為知道網址」取得 CDP；必須由下述 control lease 把它綁到特定使用者與任務。

### B. 保留 standalone KasmVNC，新增 browser session broker

broker 驗證 Cloudflare Access 的 JWT，將 Authentik 使用者映射到專屬 agent，為每人建立獨立 Chrome 容器、volume 與短效控制權。它較輕，但所有使用者／session 管理、審計與回收邏輯都必須由 OSSLab 自行實作。

這是可行的過渡方案，卻不是「Kasm 原生 OIDC」。在「同事要看得見自己使用的 Kasm、並清楚辨識誰用誰」是硬需求時，**先做 A 的平行試點較合適**；B 只在不需要 Kasm 使用者入口、而瀏覽器純粹是 agent 後端資源時採用。

## 執行順序

### Phase 0：先收斂現有風險，不改工作流程

1. 盤點所有 Chrome 容器的 CDP port、VNC public path 與對應 agent，建立不含密碼的清冊。
2. 停止將 CDP 發佈到主機的所有網卡。CDP 只能存在於容器私有網路或 loopback，且只允許經過受驗證的 agent control broker；不得透過公開網域、LAN port 或固定 URL 直接連線。
3. 將 VNC 密碼由 compose 移出：部署時從受管 secret 注入容器的受限檔案或短效啟動憑證，原始碼、Git、`docker compose config` 輸出與一般日誌都不得出現值。Vaultwarden 是使用者網站登入資料庫，**不是**部署用 VNC secret 的儲存位置。
4. 新 secret 成功注入後，立刻輪替既有共用 VNC 密碼並使舊值失效；輪替必須留下時間、操作者與受影響容器的紀錄，但不記錄 secret 本身。
5. 保留現行 VNC 服務作為回復路徑，直到試點的驗收條件全數通過。

Phase 0 的完成標準：任何未授權的 LAN／公開來源都無法取得 CDP；Git 與 compose 不再含 VNC 密碼；舊密碼不能再連線。

### Phase 1：不動正式入口的 Kasm Workspaces OIDC 試點

1. 在獨立環境部署完整 Kasm Workspaces，不取代現有 standalone KasmVNC；先以少量測試帳號與一個 Chrome workspace 驗證。
2. 在 Authentik 建立專用 OIDC application／provider，將不可變的 `sub`、受驗證 email 與必要群組傳給 Kasm。Lark 使用者與 Authentik `sub` 的對照需由受控的同步或管理流程建立，不接受僅靠輸入 email 自行認領帳號。
3. Kasm 依群組授予 workspace；預設每位使用者只能啟動自己的 Chrome session，禁止共用預設帳號與共用 browser profile。
4. Cloudflare Access 維持為公開邊界；Access 與 Kasm 都轉向同一 Authentik session。試點應從不符合任何內網 bypass 的外部網路測試，確認確實走 Lark／Authentik SSO。
5. 每個 browser profile／volume 以 `principal_id` 隔離。Vaultwarden extension 可預先安裝，但仍由本人每次 session 解鎖；agent 不取得 Vaultwarden 主密碼。

Phase 1 的完成標準：測試者以自己的 Lark 帳號登入後，Kasm 的 audit/session 可辨識其 `principal_id`；另一位測試者無法開啟或沿用前者的 browser profile。

### Phase 2：把 Lark 任務、Kasm session 與 agent 綁起來

1. 建立 agent control broker。它只接受經驗證的 Lark 任務與已建立的 Kasm session，不接受任意 CDP URL、container name 或 browser port。
2. broker 驗證 `Lark 使用者 → Authentik principal_id → Kasm session owner → agent_id` 是同一位授權對象後，才簽發只對一個 browser session 與一件任務有效的短效 control lease。
3. agent 透過私有連線取得該 lease 的 CDP bridge；lease 到期、任務結束、使用者按下「接手」、Kasm session 結束或 Vaultwarden 重新鎖定時，broker 立即撤銷控制。
4. 對外寄信、付款、刪除、改權限與新登入等高風險動作，broker 必須要求 Lark 的人工核准；核准 ID 與 task ID 一起寫入稽核紀錄。
5. Lark 回報訊息附上可理解的狀態，例如「Agent 正在你的 Chrome 工作階段處理，隨時可接手」，但不暴露 CDP／VNC 端點或 secret。

Phase 2 的完成標準：管理者能由一筆 Lark 任務追到唯一 agent 與 Kasm session；不同使用者／agent 的 lease 無法交叉控制 browser；使用者接手後 agent 控制立即失效。

### Phase 3：驗收、遷移與回復

以 `thx0701` 進行外網驗收：登入 Lark／Authentik、啟動自己的 Kasm Chrome、解鎖 Vaultwarden、在 Lark 交辦低風險任務、確認 agent 只取得該 session 的短效控制權，最後由使用者接手並驗證控制權被撤銷。先不測試付款、寄正式信或其他不可逆動作。

確認後再分批邀請其他同事；每批皆驗證 profile 隔離、稽核對應、CDP 不可直連與 secret 輪替流程。若有任何一項失敗，保留舊服務作為暫時回復路徑，修正試點後再重測；不把未完成的試點直接切換成正式入口。

## 明確的決策與邊界

- 採用完整 Kasm Workspaces 原生 OIDC 試點，不把 OIDC 硬塞進 standalone KasmVNC Chrome 容器。
- Cloudflare Access 是外層入口保護；Kasm OIDC 是 Kasm 內部使用者／session 身分；agent control broker 是工作授權。三者缺一不可，也不能互相取代。
- 不共用 VNC 密碼、Kasm 帳號、Chrome profile、browser session 或 CDP endpoint。
- 不將 VNC 密碼、OIDC client secret、Cloudflare token、CDP URL 或使用者憑證寫入 Git、文件、Lark 訊息或 log。
- 若完整 Kasm Workspaces 的維運成本最後不合理，才退回 standalone + broker；但仍必須完成同一套 `principal_id → agent → browser → task` 對應與 CDP／secret 邊界。
