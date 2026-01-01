# final_project_fitness_planner(增肌減脂智慧規劃助手)

這是一個專為 **Open WebUI** 設計的 Python 工具 (Tool/Function Calling)。它能讓您的 AI 模型具備精準的數學運算能力，根據使用者的身體數值，科學地計算 **BMR (基礎代謝率)**、**TDEE (每日總消耗熱量)**，並自動生成客製化的**飲食建議**與**一週訓練課表**。

## 特色功能

* **科學運算**：使用 Mifflin-St Jeor 公式計算 BMR，解決 LLM 模型不擅長數學運算的問題。
* **個性化目標設定**：
* **減脂 (Cut)**：熱量赤字 + 高蛋白。
* **增肌 (Bulk)**：熱量盈餘 + 強度訓練。
* **身體重組 (Recomp)**：維持熱量 + 體態調整。


* **智慧排程**：根據目標自動生成 Push/Pull/Legs 或全身性訓練的一週課表。
* **防呆機制 (Crash-Proof)**：
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



## 使用範例 (Usage Examples)
* 啟用後，您可以直接用自然語言與 AI 對話，模型會自動判斷該呼叫哪個工具。
* 
* 情境 A：計算熱量與營養
* 用戶：「我今年 25 歲，男生，175 公分 75 公斤，想要減脂，一週運動 3 天，幫我算營養素。」
* 
* AI 回應：呼叫 calculate_daily_macros，回傳精準的 TDEE、赤字熱量與蛋白質攝取量。
* 
* AI 回應：呼叫 lookup_fatsecret_official，從資料庫撈取真實數據回報。
* 
* 情境 B：安排課表
* 用戶：「我一週想練 5 天，想變壯，幫我排課表。」
* 
* AI 回應：呼叫 get_weekly_workout_schedule，生成 PPL (推拉腿) 課表。
* 
* 情境 C：查詢詳細動作
* 用戶：「那胸部要怎麼練？給我詳細菜單。」
* 
* AI 回應：呼叫 get_detailed_body_part_routine，列出臥推、夾胸等動作的組數。
* 
* 情境 D：查詢成大健身房
* 用戶：「今天成大健身房有開嗎？」
* 
* AI 回應：呼叫 get_ncku_gym_schedule，爬取學校公告並結合當前時間判斷開放狀態。


<img width="1015" height="1174" alt="image" src="https://github.com/user-attachments/assets/b5ae29e3-d9e0-4676-a3ae-12fc2c98d116" />

