# osslab-agent

> **狀態：WIP / draft.** 設計文稿先公開，部署腳本與 chrome 容器 image 陸續推上。

自架的**訂閱制 AI agent 多入口協同架構**：Lark 交辦與審核、Web workbench 長研究與沉澱、BrowserProvider 操作真實系統（CDP + 人類 VNC 接手）。模型推理交給 Claude Code CLI、Codex CLI 等可替換 runtime；本專案負責 routing、session、project policy、tools、approval 與 browser 隔離。

AI 不是按鈕或單一聊天窗，而是能存在於不同 channel 的同事：可在 Lark 被 @，可在 Web workbench 做長研究並依 project 分流，可在隔離 browser 查 ERP、寫文件、回信，遇到 captcha／2FA／付款時請人接手同一 session。

## 核心差異

- **不是**再做 openclaw／harmes 式自研 agent framework。
- **是**把現成 CLI 訂閱方案當 Runtime Provider；長 session／stdio／process bridge，不依賴不穩定的一次性 `-p`。
- **共用**規範與權威知識；**隔離** session、browser profile、bot identity、work directory。
- **Git-first**：可重用結論進 private Git artifact；Lark 是事件與批准，不是長期知識庫。

## 核心分層

- **Lark 行動層**：短任務、通知、審核、人工介入。
- **Web workbench**：stream、圖片／檔案、research、project context、草稿。
- **Project routing**：research／dev／it／ops 等安全與上下文邊界。
- **Browser 執行層**：獨立 profile（預設）；CDP 給 agent、VNC 給人。

## Non-goals（v1）

- 完整多租戶營運後台、CLI 認證生命週期、完整本地 LLM 部署包。
- 以 IM 訊息流取代 version control。
- 保證所有第三方 code agent 的完整相容（僅契約相容的 Runtime Provider）。
- 強制複製 OSSLab 的主機／port／身份拓樸。

## 設計文件

建議閱讀順序：

1. [`docs/design.md`](docs/design.md) — 總覽與術語  
2. [`docs/functionality.md`](docs/functionality.md) — 使用者能完成什麼  
3. [`docs/architecture.md`](docs/architecture.md) — 狀態、安全、Runtime／Tools／Browser 契約  

## License

[MIT License](LICENSE)
