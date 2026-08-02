# 05 · 定案：LarkSuite 是 AI agent channel

> **命題**：AI agent 驅動的團隊，主 channel 用 **LarkSuite**。Slack vs Discord 只比 IM，缺 Mail／SSO／Base／審核軸心，對 agent 團隊不完整。
> **定案：採用。** 三方 review（Grok 4.5 · GPT-5.6-Luna · Kimi Code）一致。
> 價格與額度以 [Lark 官方方案](https://www.larksuite.com/en_us/pricing) 為準。

---

## 三方平台：強、弱、功能、特色

### LarkSuite（定案主 channel）

- **功能**：IM＋企業 Mail＋Docs／Sheets＋Base／Forms＋Tasks＋審核（approval），全部同一租戶、同一帳號體系。
- **強**：
  - agent 的工作物件（信、表、文件、任務、簽核）原生在同一入口，不用外掛拼裝。
  - 企業 Mail 帳號是身分起點 → **Authentik OIDC** → Cloudflare Access／NetBird／RustDesk／Termix 一條 SSO 鏈。
  - 成本曲線平：**Free 就能跑完整 agent channel**；要長留痕才上 Basic 約 **USD $6／人／月**，可逐人開通。
  - 「SSO ≠ agent 權限」分層治理（登入、授權、執行、稽核分開管），是刻意的治理設計。
- **弱**：
  - Free 對話紀錄只留**約半年**，需要稽核長史遲早要付 Basic。
  - App／bot 生態比 Slack 小；中文圈外的第三方整合較少。
  - 平台集中＝供應商鎖定，需保留資料匯出與遷移策略。
  - 各層 API／Mail／Base 額度依現行方案與地區而異，要按實際方案驗證。
- **特色**：不是聊天軟體加 bot，而是「人＋agent 共用的工作入口」——交辦、執行、草稿、人審核都回到同一處。

### Slack（外部協作 sidecar）

- **功能**：IM 為核心，App 目錄、Workflow Builder、Slack Connect（跨組織頻道）、Huddles 語音。
- **強**：App／整合生態最成熟；Connect 是跨公司協作的事實標準；企業治理（Enterprise Grid、DLP、eDiscovery）完整。
- **弱**：沒有內建企業 Mail、沒有可自動化的 Base／表單資料庫；文件、郵件、審核都要外接別家服務，agent 工作物件是拼裝的。企業方案按人頭計價，高於 Lark Basic。
- **免費留痕最短**：Free 只能看**最近 90 天**訊息與檔案，且 2024-08 起超過一年的資料滾動刪除——比 Lark Free 的約半年還短，升級也救不回已被刪的部分。
- **特色**：「人在哪上班」的 IM 霸主，外部廠商／客戶強制用 Slack 時無法拒絕——所以當 **sidecar** 接入，不當 agent 主 channel。

### Discord（社群／語音 sidecar）

- **功能**：頻道＋語音舞台＋bot／webhook API，社群權限角色制。
- **強**：語音與即時社群互動最強；bot 開發門檻低、社群生態活；免費層幾乎無人數限制、**訊息歷史無限期保留**（這點反而比 Lark Free 半年、Slack Free 90 天都長）。
- **弱**：沒有企業 Mail、沒有 Base／文件協作、沒有企業 SSO 身分生命週期；稽核、留痕、合規能力弱，不適合承載公司級 agent 艦隊。
- **特色**：是社群與語音場景的答案，不是企業工作入口——**不當公司 agent 主 channel**。

---

## 正（支持 LarkSuite 當主 channel）

- **一個入口全包**：IM＋Mail＋文件＋Base／Forms＋審核＋企業身分同租戶，Slack／Discord 要外掛才補得上這一圈。
- **SSO 是主因**：Mail 立身分、OIDC 延伸自架服務，帳密不散落、新人上手快。
- **成本不是障礙**：Free 起步、半年留痕是唯一實質限制、Basic ~$6 逐人補長史，相對 Slack 企業方案不算貴。
- **免費留痕三方比**：Slack Free 90 天＜**Lark Free 約半年**＜Discord Free 無限期——Lark 居中，但 Discord 的長留痕沒有企業治理可用。
- **實作已完成**：cc-connect、lark-cli、專屬 agent、Mail／Base、SSO 鏈、人審核都已落地運行；README「測試上線中」是公開釋出語氣，不是架構沒做完。

## 反（風險與邊界）

- **「最佳」有範圍**：只針對需要 Mail／Base／文件／企業身分／人審核的 agent 辦公營運團隊，不主張 Lark 在所有 IM 場景勝出。
- **供應商鎖定**：集中 workspace 降低摩擦也提高依賴，要留匯出與遷移策略。
- **Free 留痕短**：半年對話紀錄對要稽核長史的團隊是硬限制。
- **額度未驗證**：API／Mail／Base 額度依官方現行方案，需按實際開通確認。
- **外部強制 Slack Connect 時**：Slack 當 sidecar，不推翻內部主 channel。

---

## 結論

> Slack vs Discord 回答「人住哪個 IM」；本架構回答「agent 以誰的身分、在哪個可審核入口工作」。後者的答案是 **LarkSuite**——Free 起步、Basic ~$6 補長歷史、SSO＋Mail＋Base 同租戶已實作完成；Slack 作外部協作 sidecar、Discord 作社群語音 sidecar。

## 與本 repo

| 文件 | 角色 |
| --- | --- |
| [README](../../README.md) | 產品結論與工作流 |
| [02](02-lark-suite-and-sso.md) | SSO／Mail／Base |
| [03](03-agent-governance.md) | SSO ≠ agent 權限 |
| 本文 | **公開討論定案** |
