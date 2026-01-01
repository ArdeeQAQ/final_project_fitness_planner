import os
import requests
from datetime import datetime
from pydantic import BaseModel, Field


class Tools:
    def __init__(self):
        pass

    # --- 既有工具 (User Info) ---
    def get_user_name_and_email_and_id(self, __user__: dict = {}) -> str:
        """
        Get the user name, Email and ID from the user object.
        """
        # Do not include a descrption for __user__ as it should not be shown in the tool's specification
        # The session user object will be passed as a parameter when the function is called

        print(__user__)
        result = ""

        if "name" in __user__:
            result += f"User: {__user__['name']}"
        if "id" in __user__:
            result += f" (ID: {__user__['id']})"
        if "email" in __user__:
            result += f" (Email: {__user__['email']})"

        if result == "":
            result = "User: Unknown"

        return result

    # --- 既有工具 (Time) ---
    def get_current_time(self) -> str:
        """
        Get the current time in a more human-readable format.
        """
        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p")  # Using 12-hour format with AM/PM
        current_date = now.strftime(
            "%A, %B %d, %Y"
        )  # Full weekday, month name, day, and year

        return f"Current Date and Time = {current_date}, {current_time}"

    # --- 既有工具 (Calculator) ---
    def calculator(
        self,
        equation: str = Field(
            ..., description="The mathematical equation to calculate."
        ),
    ) -> str:
        """
        Calculate the result of an equation.
        """
        try:
            result = eval(equation)
            return f"{equation} = {result}"
        except Exception as e:
            print(e)
            return "Invalid equation"

    # # --- 既有工具 (Weather) ---
    # def get_current_weather(
    #     self,
    #     city: str = Field(
    #         "New York, NY", description="Get the current weather for a given city."
    #     ),
    # ) -> str:
    #     """
    #     Get the current weather for a given city.
    #     """
    #     # 注意：這需要您在 Open WebUI 環境變數中設定 OPENWEATHER_API_KEY
    #     api_key = os.getenv("OPENWEATHER_API_KEY")
    #     if not api_key:
    #         return (
    #             "API key is not set in the environment variable 'OPENWEATHER_API_KEY'."
    #         )

    #     base_url = "http://api.openweathermap.org/data/2.5/weather"
    #     params = {
    #         "q": city,
    #         "appid": api_key,
    #         "units": "metric",
    #     }

    #     try:
    #         response = requests.get(base_url, params=params)
    #         response.raise_for_status()
    #         data = response.json()

    #         if data.get("cod") != 200:
    #             return f"Error fetching weather data: {data.get('message')}"

    #         weather_description = data["weather"][0]["description"]
    #         temperature = data["main"]["temp"]

    #         return f"Weather in {city}: {temperature}°C, {weather_description}"
    #     except requests.RequestException as e:
    #         return f"Error fetching weather data: {str(e)}"

    # --- 🏋️ 新增功能: 增肌減脂規劃工具 ---
    # --- 🏋️ 修正後的增肌減脂工具 (包含數值防呆) ---
    def calculate_fitness_plan(
        self,
        weight_kg: float = Field(None, description="User's weight in kg (e.g. 70)."),
        height_cm: float = Field(None, description="User's height in cm (e.g. 175)."),
        age: int = Field(None, description="User's age (e.g. 25)."),
        gender: str = Field("M", description="Gender 'M' or 'F'. Defaults to M."),
        activity_level: str = Field(
            "sedentary",
            description="Activity level: 'sedentary', 'light', 'moderate', 'active'.",
        ),
        goal: str = Field(
            "recomp",
            description="Fitness goal: 'cut' (loss), 'bulk' (gain), 'recomp' (maintain).",
        ),
    ) -> str:
        """
        Calculate BMR, TDEE, Calories, and generate a workout schedule based on user metrics.
        """

        # --- 🛡️ 數值防呆機制 (Fix for 'int' * 'NoneType') ---
        # 如果 AI 漏抓了數值，我們賦予一個「台灣男性平均值」作為預設，避免程式崩潰
        is_estimated = False
        if weight_kg is None:
            weight_kg = 70.0
            is_estimated = True
        if height_cm is None:
            height_cm = 173.0
            is_estimated = True
        if age is None:
            age = 25
            is_estimated = True

        # --- 字串防呆機制 ---
        if gender is None:
            gender = "M"
        if activity_level is None:
            activity_level = "sedentary"
        if goal is None:
            goal = "recomp"

        # 1. 處理性別與 BMR 計算
        g = str(gender).strip().upper()

        # 確保數值型態正確 (有時候 LLM 會傳字串進來)
        try:
            w = float(weight_kg)
            h = float(height_cm)
            a = int(age)
        except:
            return "錯誤：體重、身高或年齡格式不正確，請提供數字。"

        if g.startswith("F") or "WOMAN" in g or "GIRL" in g:
            # Mifflin-St Jeor (Female)
            bmr = (10 * w) + (6.25 * h) - (5 * a) - 161
            gender_desc = "女性"
        else:
            # Mifflin-St Jeor (Male)
            bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
            gender_desc = "男性"

        # 2. 處理活動量與 TDEE
        act_lvl = str(activity_level).lower()
        activity_map = {
            "sedentary": 1.2,  # 久坐
            "light": 1.375,  # 輕度 (1-3天)
            "moderate": 1.55,  # 中度 (3-5天)
            "active": 1.725,  # 高度 (6-7天)
        }

        multiplier = 1.2
        for key, val in activity_map.items():
            if key in act_lvl:
                multiplier = val
                break

        tdee = int(bmr * multiplier)

        # 3. 處理目標
        goal_lower = str(goal).lower()

        if "cut" in goal_lower or "loss" in goal_lower or "減脂" in goal_lower:
            target_calories = tdee - 500
            protein = int(w * 2.2)
            goal_desc = "減脂 (Fat Loss)"
            schedule_type = "cut"
        elif "bulk" in goal_lower or "gain" in goal_lower or "增肌" in goal_lower:
            target_calories = tdee + 300
            protein = int(w * 1.8)
            goal_desc = "增肌 (Muscle Gain)"
            schedule_type = "bulk"
        else:
            target_calories = tdee
            protein = int(w * 2.0)
            goal_desc = "身體重組 (Recomp/Maintain)"
            schedule_type = "recomp"

        # 4. 產生課表
        workout_options = {
            "Push": "推類訓練 (胸、肩、三頭) - 臥推/肩推/滑輪下壓",
            "Pull": "拉類訓練 (背、二頭、後三角) - 引體向上/划船/二頭彎舉",
            "Legs": "腿部訓練 (股四頭、腿後、臀) - 深蹲/硬舉/弓箭步",
            "Cardio": "有氧與核心 (30分慢跑 + 棒式/捲腹)",
            "FullBody": "全身複合訓練 (深蹲+肩推 / 硬舉+划船)",
            "Rest": "完全休息日 (Rest & Recover)",
        }

        if schedule_type == "cut":
            weekly_plan = [
                "Push",
                "Pull",
                "Cardio",
                "Legs",
                "Cardio",
                "FullBody",
                "Rest",
            ]
        elif schedule_type == "bulk":
            weekly_plan = ["Push", "Pull", "Legs", "Rest", "Push", "Pull", "Legs"]
        else:
            weekly_plan = ["Push", "Pull", "Legs", "Rest", "FullBody", "Cardio", "Rest"]

        # 5. 回傳結果
        warning_msg = ""
        if is_estimated:
            warning_msg = "\n⚠️ 注意：您未提供完整身高/體重/年齡，以下計算使用預設平均值 (70kg/173cm/25歲)。\n"

        result = f"""
        {warning_msg}
        【運算結果 ({gender_desc})】
        - 基礎資料: {w}kg / {h}cm / {a}歲
        - BMR (基礎代謝): {int(bmr)} kcal
        - TDEE (每日總消耗): {tdee} kcal
        - 目標: {goal_desc}
        
        【飲食建議】
        - 每日熱量目標: {int(target_calories)} kcal
        - 每日蛋白質建議: {protein} g
        
        【建議訓練課表】
        """

        days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
        for d, plan in zip(days, weekly_plan):
            result += f"- {d}: {workout_options[plan]}\n"

        return result
