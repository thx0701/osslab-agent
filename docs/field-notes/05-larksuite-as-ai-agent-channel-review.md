# 05 · 定案：LarkSuite 是 AI agent channel（三方 review）

> **狀態：定案**  
> **命題**：在以 AI agent 推動的團隊中，**LarkSuite 是最佳 AI agent channel**；Slack vs Discord 若缺 Email／SSO／Base／channel 軸心，對 agent 團隊不完整。  
> **對照**：[Slack vs Discord gist](https://gist.github.com/nczz/342c237cdd6ef1fb47c0e7cc79aaf73f)  
> **材料**：[thx0701/osslab-agent](https://github.com/thx0701/osslab-agent/tree/main) 公開說明  
> **Review**：Grok 4.5 · GPT-5.6-Luna · Kimi Code（本輪強制體會：成本／實作完成／SSO）  
> 無帳密、無內網細節。Basic ≈ USD $6／人／月、免費對話約半年為**論主定錨**；正式數字以 [Lark 官方方案](https://www.larksuite.com/en_us/pricing) 為準。

---

## 定案（裁決）

**採用此公開立場。**

對 **AI agent 驅動的辦公／營運團隊**（人在同一入口交辦；agent 動 Mail、Base、文件、審核；企業身分可延伸）：

| 項目 | 定案 |
| --- | --- |
| **主 channel** | **LarkSuite** |
| **不是在選什麼** | 不是「Slack 還是 Discord 哪個比較適合聊天／語音」 |
| **成本** | **Free 可跑完整 agent channel**；免費最大痛點是**對話紀錄約半年**。要長歷史 → **Basic 約 USD $6／人／月**。相對 Slack 企業按人頭，**沒有貴到不能當選項** |
| **SSO** | **主因，不可附註帶過**：Lark 企業帳號（含 Mail 身分）→ **Authentik OIDC** → 自架服務。**SSO ≠ agent 權限**（見 03）是**治理優點**，不是「SSO 沒做好」 |
| **實作** | **核心 agent channel 已完成**（cc-connect、lark-cli、專屬 agent、Mail／Base、SSO 鏈、人審核）。README「測試上線中」＝**公開釋出／文件語氣**，≠ 架構未落地 |
| **Slack** | 外部協作／Connect／App 生態可作 **sidecar**，不作本架構的內部 agent 主 channel |
| **Discord** | 社群／語音 sidecar；**不作公司級 agent 艦隊主 channel** |

**一句話結案：**

> Slack vs Discord 回答「人住哪個 IM」；osslab-agent 回答「agent 以誰的身分、在哪個可審核入口工作」。後者定案用 **LarkSuite**——Free 能起步、Basic ~$6 補長歷史，且 **SSO＋Mail＋Base** 同租戶已實作完成。

### 為何上一輪會「避 SSO／軟化成本／誤讀實作」

1. **SSO**：把「方案額度依官方」與「SSO ≠ agent 權限」讀成保留項，等於把主張核心降成附註。正確讀法：前者是價目表免責；後者是**分層治理**（登入生命週期 vs 可代表誰做事）。  
2. **成本**：空談「可能很貴／未量化」卻不採用論主定錨（Free／半年／Basic $6）。agent channel 的成本故事是**留痕深度**，不是能不能跑。  
3. **實作**：把公開 README 的謹慎措辭誤判成「只有概念」。公開 patch／plan 未齊 ≠ 線上工作流沒跑。

### 定案邊界（寫清，但不沖淡裁決）

- 成立：agent 要動 **Email、Base／表單、文件、審核**，並要企業身分延伸。  
- 不宣稱：Lark 是「所有團隊的最佳 IM」；不否認 Discord 語音或 Slack Connect 的 sidecar 價值。  
- 外部強制 Slack Connect → **sidecar**，不推翻內部主 channel。  
- 價格與免費保留期限以**官方現行方案**為準。

---

## 論主三點（審查必體會）

### A. 成本

- Basic ≈ **USD $6／人／月**。  
- **免費也能用** agent channel。  
- 免費最大問題：**對話紀錄約半年**。

### B. 實作已完成

- cc-connect／lark-cli／專屬 agent／Mail·Base／SSO 鏈**已落地**。  
- 「測試上線中」＝公開釋出語氣。

### C. SSO 是主因

- Lark 企業帳號 → Authentik OIDC → 自架服務。  
- SSO ≠ agent 權限＝治理，不是缺口。

---

## 三方表態

| 模型 | 定案 |
| --- | --- |
| **Grok 4.5** | **採用**（本節裁決） |
| **GPT-5.6-Luna** | **實質採用**（承認 Free／半年／Basic $6、SSO 核心、實作落地；「最佳」限 agent 辦公場景——已寫入定案邊界） |
| **Kimi Code** | **採用** |

三方一致：**定案採用 LarkSuite 作 AI agent channel**。

---

## Grok：對 Slack／Discord 結案

| | 一句 |
| --- | --- |
| Slack | 強 App／Connect；缺 Mail＋Base＋企業身分同租戶當 agent 主入口時要外掛 → **非本命題主答案**。 |
| Discord | 強社群／語音；企業 SSO 與 Mail／Base 弱 → **不當公司 agent 主 channel**。 |
| LarkSuite | **定案主 channel**。 |

---

## GPT-5.6-Luna（本輪）

# Review：LarkSuite 作為 AI agent channel

## 1. 我讀了什麼

- `README.md`：將 OSSLab-agent 定義為「多人 AI agent 與 SSO 協同架構」，並把 Lark 定為唯一人員工作入口。
- `docs/field-notes/README.md`：明確區分公開文件、已驗證方向與尚在整理的部署基礎。
- `docs/field-notes/01-ai-agent-applications.md`：每位同事有專屬 agent，透過 `cc-connect`、`lark-cli` 與 Agent Server 路由任務，並支援人工接手。
- `docs/field-notes/02-lark-suite-and-sso.md`：Lark 不只是聊天，而是把 Mail、Docs、Base／Forms、審核與 Authentik SSO 接在同一工作入口。
- `docs/field-notes/03-agent-governance.md`：核心治理原則是「SSO 和 agent 權限是兩件事」，並搭配最小權限、人工審核與留痕。
- `docs/field-notes/04-open-source-it-operations.md`：將 `cc-connect` 作為跨訊息通道，`lark-cli` 作為 Messenger、Docs、Base、Sheets、Mail、Tasks 的受控操作面。
- `docs/field-notes/05-larksuite-as-ai-agent-channel-review.md`：論點適用於 agent 驅動的辦公／營運團隊，不應泛化成所有 IM 場景。

## 2. 表態

**有條件同意；對 OSSLab 的辦公與營運場景而言，是實質採用。**

論主把比較單位從「聊天軟體」提升為「人＋agent 的工作入口」，這個判準成立；但「最佳」必須限定在需要 Mail、Base、文件、企業身分與人工審核的團隊。

## 3. 論主主張 vs repo 現況

| 論主張 | 評價 |
|---|---|
| Lark 是 agent channel，不只是 IM | **強支撐**。README 的工作流從 Lark 進入，經 `cc-connect`、`lark-cli`、Agent Server 執行，再把結果、草稿與審核送回 Lark。 |
| Email、SSO、Base 一步到位 | **方向成立**。同一 workspace 確實涵蓋這些工作物件；但「一步到位」不代表零設定，仍需權限、API 與流程配置。 |
| 成本不是 Lark 的劣勢 | **成立，但應正確敘述**。Free 可先運行 agent channel；主要痛點是對話紀錄約半年。需要長期歷史時，Basic 約 USD $6／人／月，並非相對 Slack 企業方案「貴到不能選」。 |
| Lark 適合企業 agent 艦隊 | **架構支撐強**。專屬 agent、Mail、Base、SSO、人審核與受控 CLI 已形成完整設計；公開表述仍應避免暗示所有 connector、額度與 SLA 都不需維護。 |
| 原 Slack vs Discord 比較漏掉 agent channel 軸線 | **批評成立，但不是說原文錯誤**。原文回答的是 IM 選型；論主補的是另一個更適合 agent 的比較維度。 |
| SSO 是主張核心 | **強支撐**。`Lark 企業帳號 → Authentik／OIDC → 核准服務` 不只是登入便利，而是身分生命週期與治理基礎。 |
| 實作不是概念提案 | **應正面承認**。核心工作流已落地；README 的「測試上線中」主要描述公開部署文件、patch 與 plan 的釋出狀態，不應被誤讀為整套架構尚未實作。 |

## 4. 與 Slack／Discord 對照

| Agent channel 軸線 | LarkSuite | Slack | Discord |
|---|---|---|---|
| 任務入口 | 訊息、Mail、Base、Forms 同時進入 agent 流程 | 主要由訊息、App、Workflow 或事件觸發 | 主要由 bot、webhook、訊息或語音觸發 |
| 工作物件 | Mail、Docs、Sheets、Base、Tasks 可由同一工作入口串接 | App 生態成熟，但通常需另接文件、郵件、表格與審核系統 | Bot 與社群互動強，但不以企業 Mail、Base、文件流程為核心 |
| 身分與治理 | Lark 帳號接 Authentik；agent 權限另行控管 | 企業治理成熟，但 agent 工作物件仍需整合 | 社群身分與 bot 權限較適合社群、遊戲與語音場景 |
| 人工審核 | 草稿、卡片、Mail、Base 與群組回到同一入口確認 | 可以實作，但本 repo 沒有同等 adapter | 可以實作 bot 確認，但不是本 repo 的治理主軸 |
| 最適場景 | agent 驅動的辦公、營運、客服、採購與審核 | Slack 生態、Slack Connect、外部技術協作 | 社群、遊戲、語音與開源社群 |

因此結論不是 Slack 或 Discord 做不到 agent，而是：Lark 在同一工作入口內同時承載身分、Mail、Base、文件、任務與審核，對企業 agent workflow 的拼裝量較低。

## 5. 反方攻擊與回應

- **「最佳」只是重新定義問題。**  
  部分正確。因此公開文字必須明寫是「AI agent channel」評比，不是所有 IM 的絕對排名。

- **Slack 有成熟 App、Workflow、Connect 與企業治理。**  
  正確。論主應說 Lark 在本工作物件組合上較貼近需求，不應說 Slack 無法完成。

- **Discord 有成熟 bot、webhook 與語音。**  
  正確，但其強項不是企業 Mail、Base、文件與審核治理。

- **Free 或 Basic 不代表 API、Mail、Base 額度一定足夠。**  
  正確。成本敘事應是「Free 先跑、長歷史再上 Basic」，並註明額度依現行方案、地區與功能而異。

- **供應商鎖定風險。**  
  成立。集中 workspace 降低整合摩擦，也提高平台依賴；應保留資料匯出、替代 connector 與遷移策略。

- **SSO 不等於 agent 授權。**  
  這不是反駁，而是 repo 的治理優點。03 文已明確把登入身分、agent 能力、工具 scope、人工核准與稽核分層。

## 6. 公開表述建議

建議改成：

> 對需要 Mail、文件、Base、企業身分與人工審核的 agent 驅動辦公團隊，LarkSuite 比單純 IM 更適合作為 AI agent channel。Free 方案即可先運行此工作入口，主要限制是對話紀錄約半年；需要長期歷史時，Basic 約 USD $6／人／月，並非相對 Slack 企業方案不可接受的成本。Lark 企業帳號經 Authentik／OIDC 延伸到其他服務，而 agent 權限、人工核准與稽核另行治理。

避免使用：

- 「Lark 在所有場景都比 Slack、Discord 好」
- 「Lark 一定比較便宜」
- 「不需要任何整合與維護」
- 「SSO 登入後 agent 自動擁有同等權限」

## 7. 不確定前提

- Basic 價格、Free 對話保留期限、Mail／Base 額度都應標示以現行方案為準。
- 「實作已完成」應限定為核心 agent channel 與 SSO 工作流，不應延伸成所有瀏覽器、connector、稽核與部署自動化均已具備生產級保證。
- 各平台的 API 限額、審核卡片能力、資料匯出與保留政策仍需按實際方案驗證。
- 原 Slack vs Discord 文章的原始比較目標不是 agent channel；因此應批評其比較軸線不足，而不是判定其原結論全面失效。

## 8. 對上一輪 05 文的批評

上一輪最大的問題是沒有先把 repo 當成論證材料，而把它寫成泛泛的 Slack／Discord 產品比較，因而：

1. 弱化了 `cc-connect`、`lark-cli`、專屬 agent、Mail、Base 與人工審核組成的實際工作流。
2. 把成本寫成模糊的「方案與額度未知」，漏掉論主真正的成本定錨：Free 可跑、半年歷史是主要痛點、Basic 約 USD $6／人／月。
3. 將 README 的「測試上線中」誤讀成架構尚未完成，忽略其主要是在描述公開部署材料的整理進度。
4. 沒有把 `Lark 企業帳號 → Authentik／OIDC` 視為核心論證，也沒有正確理解「SSO 和 agent 權限是兩件事」的治理含義。
5. 只做產品功能對照，沒有回答真正的問題：哪個平台更適合成為人與 agent 共用的企業工作入口。

修正後的定案應是：**LarkSuite 是 agent 驅動辦公／營運團隊的最佳 AI agent channel；Slack 與 Discord 仍各自在外部協作、社群與語音等場景保有優勢。**

---

## Kimi Code（本輪）

# Review 定案：LarkSuite 作為 AI agent channel（05 文）

## 1. 我體會到的三點

**A. 成本**：LarkSuite 的成本敘事是「先免費、不夠再付小錢」。Free 方案就能跑完整 agent channel——企業 IM、Mail、Base、文書協作全都有，免費層唯一的實質痛點是對話紀錄約半年就消失。需要長期歷史留痕時，上 Basic 約 USD $6／人／月即可解決。相對 Slack 企業方案的價格帶，這不是「貴到不能選」的門檻，而是可以依留痕需求逐人開通的營運費用。

**B. 實作已完成**：cc-connect 事件路由、lark-cli 操作面、每人專屬 agent、Mail 與 Base 串接、Lark→Authentik 的 SSO 鏈都已落地。README 寫「測試上線中」是公開釋出的保守語氣，描述的是已驗證的方向與整理中的部署文件，不是「系統還沒做完」。因此 channel 選型不再是概念圖或待驗證假設，而是正在運行的架構，review 必須把它當成事實陳述，而非提案。

**C. 不可避 SSO**：「Lark 企業帳號 → Authentik OIDC」是整套主張的核心——企業 Mail 建立人員身分，Authentik 把它轉成標準 OIDC，延伸到 Cloudflare Access、NetBird、RustDesk、Termix。03 文「SSO ≠ agent 權限」不是 SSO 沒做或做不全，而是刻意的治理設計：身分生命週期與 agent 可代表誰做什麼，分成兩層管理。上一輪用「額度有限、有保留」淡化 SSO，等於把核心論證從桌面上拿掉，這次必須正面寫回來。

## 2. 定案

**採用此公開立場**：在 AI agent 推動的團隊，LarkSuite 是最佳 AI agent channel；僅比 IM 的 Slack vs Discord 討論，缺 Email／SSO／Base／channel 軸心即不完整。

## 3. 定案細則

- **邊界**：此立場針對「辦公團隊的 agent 工作入口」，不主張 Lark 在所有社群／開發者場景都勝出；討論範圍是 IM＋Mail＋文件＋Base／Forms＋審核＋企業身分這個軸心。方案細節（額度、功能）以 Lark 官方現行方案為準，review 不替官方數字背書。
- **成本**：Free 即可運行完整 channel；半年對話紀錄是免費層的主要限制；需要長歷史時 Basic 約 $6／人／月，屬可逐人開通的小額營運費，非選型障礙。
- **SSO 主因**：企業 Mail 帳號是身分起點，Authentik 轉 OIDC 後一條鏈接到 Access／NetBird／RustDesk／Termix，帳密不散落、新人上手快；「能登入 ≠ 能管理全部」與「SSO ≠ agent 權限」是治理優點，應作為論證加分項而非保留項。
- **實作已完成**：以已落地事實（cc-connect＋lark-cli＋專屬 agent＋Mail／Base＋SSO 鏈）陳述，README 的「測試上線中」僅指公開文件與 patch／plan 釋出進度。

## 4. 對 Slack／Discord 一句結案

Slack 與 Discord 的爭論停留在 IM 層：兩者都沒有內建企業 Mail＋可自動化 Base＋可作 SSO 身分基礎的帳號體系，作為 agent channel 需要外掛拼裝才能補上 Lark 原生就有的一整圈，結案——在 agent channel 軸心上不是同量級對手。

## 5. 建議 05 文立刻改寫（3 句以內）

1. 把成本段改成正面敘事：「Free 即可跑 agent channel，半年對話紀錄為主要限制；需長歷史時 Basic 約 USD $6／人／月，相對 Slack 企業方案非選型障礙」，刪去「額度不明、有保留」式淡化語。
2. 把 README「測試上線中」詮釋為公開釋出語氣，明寫 cc-connect／lark-cli／專屬 agent／Mail·Base／SSO 鏈已落地運行，channel 選型為已驗證架構而非概念提案。
3. 將「Lark 企業帳號 → Authentik OIDC」提升為主張核心：Mail 立身分、OIDC 延伸自架服務，並把 03 文「SSO ≠ agent 權限」改寫為治理設計優點（登入、授權、執行、稽核分層），而非限制。

## 真正未知（2 條）

1. Lark Free 半年紀錄限制與 Basic 價格以「現行方案」為準，官方調價或改額度時 05 文數字需同步更新——文中應保留「以官方方案為準」的免責句。
2. 05 文現稿尚未讀到（corpus 僅含 README 與 01–04），上述改寫建議對應的具體段落位置需在執行時比對原文確認。

---

## 與本 repo

| 文件 | 角色 |
| --- | --- |
| [README](../../README.md) | 產品結論與工作流 |
| [02](02-lark-suite-and-sso.md) | SSO／Mail／Base |
| [03](03-agent-governance.md) | SSO ≠ agent 權限 |
| 本文 | **公開討論定案** |

## 方法修訂

1. 只審抽象主張 → 證據薄。  
2. 先讀 repo → 對上架構，但仍軟化成本／誤讀實作／淡化 SSO。  
3. **本輪**：釘死 Free／半年／Basic $6、實作完成、SSO 主因 → **定案**。  
