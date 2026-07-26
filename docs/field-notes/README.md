# osslab-agent 的實際工作筆記

這不是功能清單，也不是把尚未上線的構想當成現況。這四篇文章說明 osslab-agent 為什麼從我們已經在用的工作方式出發：Lark Suite 作為協作與身分入口、訂閱制 code agent 做推理與工具決策、隔離的瀏覽器負責登入後的實際操作，而人類保留審核與接手權。

| 文章 | 要回答的問題 |
| --- | --- |
| [01 · AI agent 應用](01-ai-agent-applications.md) | AI 怎麼真的進入工作，而不是停在聊天展示？ |
| [02 · Lark Suite 與 SSO](02-lark-suite-and-sso.md) | 為何 Lark 是工作入口，也是登入入口？ |
| [03 · 管理與治理](03-agent-governance.md) | 多個 agent 怎麼分工、授權、審核與留痕？ |
| [04 · 自架平台與 IT 維護](04-open-source-it-operations.md) | 身分、VPN、Git、ERP、密碼庫與維護服務怎麼組成一個可維護的底座？ |

完整的元件與通訊架構仍在 [`../design.md`](../design.md)；這裡只說明設計背後的實際工作情境與邊界。
