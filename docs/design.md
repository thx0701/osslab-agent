# osslab-agent 設計總覽

osslab-agent 是一套自架的訂閱制 AI agent 多入口架構。它把 Lark、cc web、可替換 code agent runtime、BrowserProvider 與人工接手接成一條可追溯的工作流。

原本的單一設計稿已拆成兩份主規格，避免功能需求與實作／安全決策互相混淆：

| 文件 | 回答的問題 |
|---|---|
| [功能規格](functionality.md) | 使用者能完成什麼工作、各入口如何 handoff、v1 包含哪些能力？ |
| [架構規格](architecture.md) | Project 如何路由、資料存在哪裡、如何 Git-first、如何登入／授權／批准，以及 browser 如何隔離？ |

## 讀取順序

1. 先讀功能規格，理解 Lark 行動層、cc web 工作台、research、採購、銷售、客服、助理與群組彙總等使用情境。
2. 再讀架構規格，理解 Git-first 長期真相、session 與 artifact 的區別、Project 模型、BrowserProvider、SSO 與 action policy。
3. 實作每個功能時，將 request、branch、commit / PR、approval 與結果關聯；可重用成果提交到指定私有 Git repo。

## 產品定位

本 repo 是可公開的 osslab-agent 產品與 deployment building blocks。OSSLab 現役的 Forgejo、Authentik、Lark、cc-connect、Kasm Chrome 與 BrowseForge 部署可作為 reference deployment，但不等於所有使用者都必須複製的拓撲或身份系統。

## License

本 repo 採 [MIT License](../LICENSE)。
