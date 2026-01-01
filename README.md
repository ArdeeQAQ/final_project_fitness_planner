# final_project_fitness_planner(增肌減脂智慧規劃助手)

這是一個專為 **Open WebUI** 設計的 Python 工具 (Tool/Function Calling)。它能讓您的 AI 模型具備精準的數學運算能力，根據使用者的身體數值，科學地計算 **BMR (基礎代謝率)**、**TDEE (每日總消耗熱量)**，並自動生成客製化的**飲食建議**與**一週訓練課表**。

## 特色功能

* **科學運算**：使用 Mifflin-St Jeor 公式計算 BMR，解決 LLM 模型不擅長數學運算的問題。
* **個性化目標設定**：
* **減脂 (Cut)**：熱量赤字 + 高蛋白。
* **增肌 (Bulk)**：熱量盈餘 + 強度訓練。
* **身體重組 (Recomp)**：維持熱量 + 體態調整。


* **智慧排程**：根據目標自動生成 Push/Pull/Legs 或全身性訓練的一週課表。
* **🛡️ 獨家防呆機制 (Crash-Proof)**：
* 自動偵測缺少的參數（如忘記輸入身高體重），自動帶入預設值並提示使用者。
* 防止 `NoneType` 錯誤導致的對話崩潰。
* 支援模糊語意輸入（如 "lose weight", "減肥", "變壯"）。


## 安裝與設定步驟
安裝︰
確保有安裝docker,openwebui

開啟docker後，run︰
```bash
docker start open-webui0
```

然後，
在瀏覽器打開︰
```bash
http://localhost:3000/
```

設定︰
* 新增空白工具： 進入 Open WebUI 介面，依序點擊 Workspace（工作區） > Tools（工具） > + Create Tool（建立工具）。
* 匯入程式碼： 將 main.py 檔案中的所有程式碼複製，貼上到工具的程式碼編輯區，然後點擊 Save（儲存）。
進入設定： 儲存完成後，在該工具旁尋找 "Valves" 或 "Settings"（設定） 的圖示。
輸入金鑰： 在設定欄位中，輸入您的 SPOTIFY_CLIENT_ID（Spotify 客戶端 ID）與 SPOTIFY_CLIENT_SECRET（Spotify 客戶端密鑰）。
開啟新對話： 回到聊天介面，開啟一個新的對話視窗。
啟用工具： 點擊輸入框旁邊的 + (Tools) 按鈕，並將 "Spotify" 工具切換為開啟狀態（Toggle on）。


## 🛠️ 安裝方式

此工具專門用於 **Open WebUI** 環境。

1. **開啟 Open WebUI**：
登入您的 Open WebUI 介面，點擊右上角頭像或選單，進入 **Workspace (工作區)**。
2. **建立新工具**：
* 選擇 **Tools** 標籤頁。
* 點擊 **"+" (Create Tool)** 按鈕。


3. **填寫設定**：
* **Name**: `Fitness_Planner` (建議使用此名稱，或自訂但不可包含空格)。
* **Description**: `Calculates fitness metrics (BMR, TDEE) and creates a workout plan based on user input.`
* **Toolkit Code**: 將 `fitness_planner.py` (或是我們最後完成的那段程式碼) 的內容完整複製貼上。


4. **啟用工具**：
* 儲存後回到聊天室 (Chat)。
* 在輸入框左側點擊 **工具設定 (板手圖示)**。
* 將 `Fitness_Planner` 設為啟用 (ON)。



##  如何使用 (Usage)

啟用工具後，您可以直接用自然語言與 AI 對話。

### 範例指令：

**1. 資訊完整的查詢 (最精準)**

> 「幫我規劃增肌菜單，我 28 歲，男生，身高 175 公分，體重 70 公斤，平常久坐。」

**2. 模糊查詢 (觸發防呆機制)**

> 「我想減肥，幫我排課表。」
> *(AI 會自動帶入預設數值計算，並提醒您補充正確資料)*

**3. 指定目標**

> 「我想要身體重組，每週運動 5 天，幫我算熱量。」

## 📋 參數說明 (Parameters)

工具會自動從您的對話中提取以下參數：

| 參數 | 說明 | 預設值 (若未提供) |
| --- | --- | --- |
| `weight_kg` | 體重 (公斤) | 70.0 |
| `height_cm` | 身高 (公分) | 173.0 |
| `age` | 年齡 | 25 |
| `gender` | 性別 (M/F) | "M" (男) |
| `activity_level` | 活動量 (sedentary/light/moderate/active) | "sedentary" (久坐) |
| `goal` | 目標 (cut/bulk/recomp) | "recomp" (維持) |

## ⚠️ 常見問題 (Troubleshooting)

**Q: 出現 `unsupported operand type(s) for *: 'int' and 'NoneType'` 錯誤？**
A: 這表示您使用的舊版程式碼沒有處理空值。請確保您使用的是最新版（包含 `is_estimated` 與 `if variable is None` 檢查邏輯）的程式碼。

**Q: 模型一直不呼叫工具，而是自己亂回答？**
A:

1. 請確認您使用的模型 (Model) 支援 **Function Calling** (例如 Llama 3, Mistral, Gemma 2, Qwen 2.5)。
2. 檢查工具的 **Description** 是否填寫正確，AI 依賴描述來判斷何時使用工具。

**Q: 可以修改訓練課表嗎？**
A: 可以。請修改程式碼中的 `workout_options` 字典與 `weekly_plan` 列表，即可自訂您喜歡的動作與循環。
