# osslab-agent

> WIP / draft。先放設計，部署腳本跟 chrome image 之後再補。

自架一套東西：用 **Claude Code / Codex 這類訂閱制 CLI** 當 agent，前面接 Lark 跟 web 對話，後面接可登入的 Chrome（AI 用 CDP，人用 VNC 接手）。

不做新的 agent framework。CLI 負責想與調工具；這邊負責把訊息路由到哪個 bot／project、session 怎麼掛、browser 怎麼隔離、什麼動作要人批、長結果怎麼進 Git。

## 大概長這樣

- **Lark**：短交辦、通知、審核、人進來接手。
- **Web 工作台**：長研究、貼圖貼檔、草稿；不是附屬聊天窗。
- **Project**：不同工作（research / dev / it / 業務）分開工具、目錄、browser。
- **Chrome**：預設一人一 profile；captcha、2FA、付款時人從 VNC 進同一個 session。

規範、runbook、可重用結論放 private Git。Lark 訊息流不拿來當長期知識庫。

## v1 先不做

管理後台、多租戶、幫你管 CLI 登入／API key、整包本地 LLM、保證每家 code agent 都能接。也不要求別人抄 OSSLab 那套主機拓樸。

## 文件

1. [docs/design.md](docs/design.md) — 怎麼讀、東西放哪  
2. [docs/functionality.md](docs/functionality.md) — 能幹嘛  
3. [docs/architecture.md](docs/architecture.md) — 怎麼接、資料放哪、權限怎麼切  

## License

[MIT](LICENSE)
