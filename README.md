# osslab-agent

> **狀態：WIP / draft.** 設計文稿先公開，部署腳本與 chrome 容器 image 陸續推上。

一套自架的「真人 + AI 同事在同一個工作群組裡協作」架構。AI 不是按鈕、不是聊天視窗，是群裡的一位——跟其他同事一樣有對話歷史，能 reply email、查 ERP、寫文件、解 captcha 求救。

- **v1 IM 平台**：Larksuite（飛書國際版），bot 即同事
- **執行體**：每個 bot 一個 Chrome 容器（CDP + KasmVNC），登入 vault / cookie / profile 完整隔離
- **訂閱制 code 當 agent**：可合規使用 Claude Code / 各家 CLI 訂閱，降低 AI API 成本；也可改接本地 LLM 走純私有
- **一人 N bot**：採購 bot、客服 bot、業務 bot……bot 數量跟人數沒綁，每個工作流配一個

## 文件

- 完整設計：[`docs/design.md`](docs/design.md)

## License

[Apache License 2.0](LICENSE)
