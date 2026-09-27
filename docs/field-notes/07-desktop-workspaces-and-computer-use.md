# 07 · 桌面工作台、Office 與 Computer Use：把操作放回正確層

桌面工作不是一種工具能包辦的工作。團隊任務、Office 檔案、已登入網站與一般桌面應用程式，各自有不同的操作入口。OSSLab-agent 仍以 Lark Suite 作為團隊協作與交辦入口；桌面軟體補上文件編輯、瀏覽器操作與圖形介面操作，不另建一個團隊聊天入口。本篇是角色與介面的架構示意，不是逐項部署清單；GenOffice、ego lite、ChatGPT 桌面版與 Cua 是依公開資料整理的代表工具。

## 桌面軟體的分層

```text
團隊工作：Lark 桌面版／Web → cc-connect + lark-cli + 專屬 agent／harness
                                      ├── GenOffice CLI／Skill／MCP → Office 本機檔案
                                      ├── ego-browser → ego lite 的 agent Space
                                      └── Cua Driver 等桌面 driver → 原生應用程式

個人桌面工作：ChatGPT 桌面版 Work／Codex + Computer Use → 核准的應用程式
```

| 工作面 | 代表工具 | 在架構中的角色與授權範圍 |
| --- | --- | --- |
| 團隊協作與人員入口 | [Lark Suite 桌面版](https://www.larksuite.com/download)／Web | 非開源的商用協作產品；群組、私訊、Mail、Docs、Base、表單與審核仍是團隊任務的共同脈絡。人員用 Lark 交辦、看進度、確認草稿與接手。 |
| Office 與本機文件 | [GenOffice](https://github.com/genspark-ai/genoffice/blob/main/docs/i18n/README.zh-TW.md) | 開源桌面辦公套件，repo 採 Apache-2.0（`ee/` 企業模組另有授權說明），支援原生 `.docx`、`.xlsx`、`.pptx`，也涵蓋 PDF、Markdown 與 HTML。檔案編輯與轉換在本機完成；內建 `genoffice` CLI、agent skill 與 MCP，讓 agent 以文件層級操作，而不必模擬滑鼠逐格編輯。AI 請求則送往使用者設定的服務商。 |
| 網站與登入態 | [ego lite](https://github.com/citrolabs/ego-lite) | 面向人員與 agent 共用的瀏覽器。agent 透過 `ego-browser` skill 在獨立 Space 執行網站任務，人員可繼續使用自己的分頁。GitHub repo 內容採 MIT 授權；README 說明瀏覽器應用程式另行下載，兩者的散佈與授權範圍應分開看。它負責瀏覽器，不是完整的跨應用程式桌面控制層。 |
| 跨應用程式 GUI | [ChatGPT 桌面版 Work／Codex + Computer Use](https://learn.chatgpt.com/docs/computer-use) | OpenAI 專有桌面產品提供整合好的 Computer Use 工作流，可在支援地區的 macOS／Windows 操作使用者核准的應用程式；需要作業系統畫面與輔助使用權限，敏感動作可要求人確認。它適合沒有 CLI、MCP 或應用程式 API 可用的 GUI 工作。 |
| 可自行組裝的桌面操作層 | [Cua Driver（trycua/cua）](https://github.com/trycua/cua) | Cua Driver 核心採 MIT 授權，可透過 MCP／CLI 接入不同 agent harness，在 macOS、Windows 與 Linux 操作原生應用程式。Cua 專案也提供隔離桌面與 Sandbox 元件；代管 Fleets 是另外的雲端服務。選用擴充元件時仍須另核對其授權。 |

## 模型、Harness 與 Computer Use 不是同一層

Computer Use 是 agent 操作電腦的一種能力，不等於特定模型或單一桌面程式。模型理解任務並提出下一步；harness 維持任務上下文、工具、執行狀態與回報；桌面 driver 提供畫面觀察和輸入操作，執行環境負責帳號、檔案與權限邊界。

OpenAI 的 ChatGPT 桌面版把 Work／Codex 與 Computer Use 整合成可直接使用的專有工作台。若要自行建構，OpenAI [Computer Use API 文件](https://developers.openai.com/api/docs/guides/tools-computer-use)說明由應用程式提供執行環境、執行模型要求的動作並回傳畫面；官方也公開了採 MIT 授權的 [Computer Use 範例程式](https://github.com/openai/openai-cua-sample-app)。這個範例展示 API 整合與執行迴圈，不是 ChatGPT 桌面應用程式或 GPT 模型的原始碼，也不提供正式桌面產品的作業系統隔離與動作審核機制。

若目標是開源、可接既有 agent 的跨應用程式桌面操作面，Cua Driver 比 `ego lite` 更接近；若目標是 OpenAI 提供的成品工作台，則使用 ChatGPT 桌面版的 Computer Use。兩條路徑都需要 harness 明確限制可操作的應用程式和動作，將購買、送出、刪除、改權限等高影響步驟留給人確認，並在任務結束後核對實際結果。

## 依任務選操作面

| 任務 | 優先入口 | 原因 |
| --- | --- | --- |
| 查詢、建立或編輯 Office 檔案 | GenOffice CLI／Skill／MCP | 能直接讀寫文件結構、公式與投影片內容，操作結果也較容易檢視。 |
| 操作登入中的網站 | 經核准的 browser skill／browser 工具 | 網站元素和登入工作階段比全桌面截圖更直接；操作範圍也可限制在瀏覽器。 |
| 處理只能透過 GUI 使用的桌面程式 | Computer Use 與桌面 driver | 以畫面或無障礙樹理解目前狀態，完成後重新觀察以確認結果。 |
| 對外送出或影響資料的操作 | 先準備草稿，交由人確認 | 模型能操作介面不代表它有權完成不可逆或對外承諾。 |

把工作入口、檔案操作、瀏覽器和一般 GUI 拆開後，團隊可以維持 Lark 中既有的協作與審核脈絡，同時讓 agent 使用最合適的本機工具。需要真人判斷時，任務回到 Lark 或可見的桌面工作階段接手。

上一篇：[〈06 · 隱私脫敏 gateway 架構〉](06-privacy-masking-gateway.md)
