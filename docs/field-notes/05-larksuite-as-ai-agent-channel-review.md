# 05 · 定案：LarkSuite 是 AI agent channel

> **命題**：AI agent 驅動的團隊，主 channel 用 **LarkSuite**。Slack vs Discord 只比 IM，缺 Mail／SSO／Base 軸心，對 agent 團隊不完整。
> **定案：採用。** 三方 review（Grok 4.5 · GPT-5.6-Luna · Kimi Code）一致。
> 價格與額度以 [Lark 官方方案](https://www.larksuite.com/en_us/pricing) 為準。

## 正（為什麼是 LarkSuite）

- **一個入口全包**：IM＋Mail＋文件＋Base／Forms＋審核＋企業身分同租戶。Slack／Discord 要外掛拼裝才能補上這一圈。
- **SSO 是主因**：Lark 企業帳號（Mail 立身分）→ Authentik OIDC → Cloudflare Access／NetBird／RustDesk／Termix 一條鏈。「SSO ≠ agent 權限」是刻意的分層治理（登入、授權、執行、稽核分開管），是優點不是缺口。
- **成本不是障礙**：Free 就能跑完整 agent channel，唯一實質限制是對話紀錄約半年；要長歷史 → Basic 約 USD $6／人／月，可逐人開通，相對 Slack 企業按人頭不算貴。
- **實作已完成**：cc-connect、lark-cli、專屬 agent、Mail／Base、SSO 鏈、人審核都已落地運行。README「測試上線中」是公開釋出語氣，不是架構沒做完。

## 反（代價與邊界）

- **「最佳」有範圍**：只針對「需要 Mail／Base／文件／企業身分／人審核的 agent 辦公營運團隊」，不主張 Lark 在所有 IM 場景勝出。Slack 的 App 生態／Connect、Discord 的社群／語音仍是各自強項。
- **供應商鎖定**：集中 workspace 降低整合摩擦，也提高平台依賴——要保留資料匯出與遷移策略。
- **免費層留痕短**：半年對話紀錄對需要稽核長史的團隊是硬限制，遲早要付 Basic。
- **額度未驗證**：Free／Basic 的 API、Mail、Base 額度依現行方案與地區而異，需按實際方案確認。
- **外部強制 Slack Connect 時**：Slack 當 sidecar 接入，不推翻內部主 channel。

## 結論

> Slack vs Discord 回答「人住哪個 IM」；本架構回答「agent 以誰的身分、在哪個可審核入口工作」。後者的答案是 **LarkSuite**——Free 起步、Basic ~$6 補長歷史、SSO＋Mail＋Base 同租戶已實作完成；Slack／Discord 只作外部協作與社群的 sidecar。

## 與本 repo

| 文件 | 角色 |
| --- | --- |
| [README](../../README.md) | 產品結論與工作流 |
| [02](02-lark-suite-and-sso.md) | SSO／Mail／Base |
| [03](03-agent-governance.md) | SSO ≠ agent 權限 |
| 本文 | **公開討論定案** |
