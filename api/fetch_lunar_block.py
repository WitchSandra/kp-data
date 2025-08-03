import requests
import json

# Настройки
latitude = 55.7
longitude = 21.1
start_date = "2025-08-01"
end_date = "2026-12-31"
timezone = "Europe/Vilnius"

# Формируем URL запроса к Open-Meteo
url = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    f"&start_date={start_date}&end_date={end_date}"
    f"&daily=sunrise,sunset,moonrise,moonset,moon_phase"
    f"&timezone={timezone}"
)

# Запрос
response = requests.get(url)
data = response.json()

# Обработка
daily = data["daily"]
calendar = {}

for i, date in enumerate(daily["time"]):
    calendar[date] = {
        "sunrise": daily["sunrise"][i],
        "sunset": daily["sunset"][i],
        "moonrise": daily["moonrise"][i],
        "moonset": daily["moonset"][i],
        "moon_phase": round(daily["moon_phase"][i], 3)
    }

# Сохраняем в файл
with open("docs/lunar_calendar.json", "w", encoding="utf-8") as f:
    json.dump(calendar, f, ensure_ascii=False, indent=2)

print("✅ Файл lunar_calendar.json успешно создан")
