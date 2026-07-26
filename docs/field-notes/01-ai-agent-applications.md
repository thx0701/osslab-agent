# 01 · 多人 AI agent 應用：人只用 Lark，複雜性留在後端

OSSLab-agent 不把 AI 做成另一個要下載、學習與維護的聊天網站。對團隊每一位同事而言，工作入口就是 Lark Suite：在群組、私訊、Mail、Base 與表單裡交辦，agent 把結果、草稿與需要確認的事項送回同一個地方。

## 多人同時用，也不共用狀態

多人使用不等於大家共用同一個 bot 帳密或瀏覽器。**每位同事都有自己的專屬 agent**，並以自己的 Lark 企業帳號作為 SSO 身分；後端依同事、群組與 project 把請求路由到對應 agent。瀏覽器登入態、bot identity、資料權限與工作目錄也按人分開，且每個 agent 的能力可依同事需求不同。

```text
同事 A 的 Lark 任務 → A 的專屬 agent ─┐
同事 B 的 Lark 任務 → B 的專屬 agent ─┼→ cc-connect + lark-cli + Agent Server → 工具／Chrome
部門群組的任務     → 指定專屬 agent ──┘                                         ↓
                                                                   結果、草稿、審核回 Lark
```

這讓採購、客服、業務、研究與 IT 能在同一個協作環境裡各自使用 agent，同時避免某一個人的對話、cookie 或內部資料意外帶到另一個工作流。

[lark-cli](https://github.com/larksuite/cli) 是 Lark 官方維護、為人員與 AI agent 設計的 CLI。它把 Messenger、Docs、Base、Sheets、Mail、Tasks 等常用工作面做成一致的命令與 agent skills，讓後端 agent 能以受控權限讀寫 Lark 資料、把結果送回正確的工作脈絡。

## 不只收訊息，也能處理工作信箱與表單

Lark Mail 是這個設計的重要原因。人員信箱與部門公用信箱都留在 Lark；在授權範圍內，agent 可以讀取新信、整理詢價、擷取待辦、比對附件、建立表單或草擬回覆。人不需要把 email 複製到另一個 AI 工具，對外寄送仍由人確認。

Lark Base／Forms 則讓工作不是只靠自由文字。客戶填表、同事填需求單或維修登錄後，資料會落到結構化欄位；agent 根據欄位做分類、比對、提醒、草稿或分派，再把結果回寫 Lark。這比從群組歷史猜測一段需求可靠得多。

## 工作如何落地

agent 不是只回答問題，而是依每位同事被授權的資料、工具與確認規則執行實際工作；結果、草稿與需要人決定的事項仍回到 Lark。

| 人在 Lark 裡交辦的事 | agent 在後端做什麼 | 回到 Lark 的結果 |
| --- | --- | --- |
| 「整理今天客服信箱的詢價」 | 讀取已授權信箱、分類、擷取需求與待確認事項 | 群組摘要、待辦或回覆草稿。 |
| 「這份表單的需求先分派」 | 讀取 Base 紀錄、依欄位規則整理與比對 | 更新欄位、建立待審核項目、通知負責群組。 |
| 「比較三家報價，先不要送信」 | 讀取附件／公開來源、比價、標示風險 | Lark Doc 或群組中的結論與草稿。 |
| 「查目前庫存或客戶狀態」 | 查 Base；若已啟用 ERP connector，再查 Odoo | 帶來源與時間點的查詢結果。 |
| 「幫我處理這個網站，但付款先叫我」 | 在隔離 Chrome 操作至需要判斷的步驟 | Lark 通知加上真人可接手的瀏覽器入口。 |

## agent 做到哪裡，人該在哪裡接手

agent 很適合完成重複而規則清楚的步驟：讀信、查表、整理附件、研究公開資料、比對差異、產出文件與草稿。每個專屬 agent 的 Chrome 使用對應同事的 Web 身分；第一次使用或 Vaultwarden 已鎖定時，**本人先在 [修改版 KasmVNC Chrome](../../docker/chrome/README.md) 解鎖 Vaultwarden**，agent 才能在同一個已解鎖的 browser session 協助操作。agent 不會取得主密碼。碰到 2FA、CAPTCHA、付款、對外承諾或例外判斷時，真人從 Lark 收到通知並接手。

這不是把責任交給 AI，而是把「查、整、寫、比」交給 AI，把「批准、承諾、付款、例外」留給人。流程因而可以自動化，又不會失去控制。

下一篇：[〈Lark Suite、Mail、Base 與 SSO：一個工作入口〉](02-lark-suite-and-sso.md)
