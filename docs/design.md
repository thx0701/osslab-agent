# osslab-agent 設計總覽

osslab-agent 是一套自架的訂閱制 AI agent 多入口架構。它把 Lark、Web workbench、可替換 code agent runtime、BrowserProvider 與人工接手接成一條可追溯的工作流。

原本的單一設計稿已拆成兩份主規格，避免功能需求與實作／安全決策互相混淆：

| 文件 | 回答的問題 |
|---|---|
| [功能規格](functionality.md) | 使用者能完成什麼工作、各入口如何 handoff、v1 包含哪些能力？ |
| [架構規格](architecture.md) | Project 如何路由、資料存在哪裡、如何 Git-first、如何登入／授權／批准，以及 browser 如何隔離？ |

## 讀取順序

1. 先讀功能規格：Lark 行動層、Web workbench、research、採購、銷售、客服、助理、工具邊界與 handoff。
2. 再讀架構規格：Shared vs Isolated、Git-first、Runtime Provider、Tools surface、BrowserProvider、action policy、失敗與額度。
3. 實作時將 request、branch、commit／PR、approval 與結果關聯；可重用成果提交到指定私有 Git repo。

## 產品定位

本 repo 是可公開的 osslab-agent 產品與 deployment building blocks。

| 是 | 不是 |
|---|---|
| 訂閱制 code agent CLI 的多入口協同層 | 再做一套 openclaw／harmes 式自研 agent framework |
| channel routing、session、project policy、browser、approval | 模型調度核心或取代 Claude Code／Codex 等 CLI |
| Git-first 的長期真相與可 review artifact | 以 IM 訊息流當唯一知識庫 |
| BrowserProvider（AI CDP + 人類 VNC 同一 session） | 純 headless RPA 或另開遠端桌面取代登入態 |

OSSLab 現役的 Forgejo、Authentik、Lark、cc-connect、Kasm Chrome 與 BrowseForge 部署可作為 **reference deployment**，但不等於所有使用者都必須複製的拓撲或身份系統。概念對可替換元件見 [architecture.md §12.1](architecture.md#121-reference-deployment-對照)。

## 術語

| 術語 | 含義 |
|---|---|
| Web workbench | 產品內長任務工作台；reference 可對應 cc-connect 類 web channel |
| Project | 部署與安全單位：runtime + work_dir + channel identity + browser + tools + policies |
| Runtime Provider | 可替換的 code agent process 契約 |
| BrowserProvider | 隔離 browser profile + CDP + VNC 接手 |
| Action policy | 讀取／草稿／可回滾／外發／高風險的批准階梯 |

## License

本 repo 採 [MIT License](../LICENSE)。
