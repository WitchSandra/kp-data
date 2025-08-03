import requests
import json
from datetime import datetime

# Координаты (можно изменить на свои)
latitude = 55.7
longitude = 21.1

# Даты диапазона (5 лет)
start_date = "2025-01-01"
end_date = "2029-12-31"

# Ссылка API OpenMeteo
url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={latitude}&longitude={longitude}"
    f"&start_date={start_date}&end_date={end_date}"
    "&daily=moon_phase"
    "&timezone=auto"
)

# Запрос
response = requests.get(url)
data = response.json()

# Проверка
if "daily" not in data or "time" not in data["daily"]:
    print("Ошибка: нет данных в ответе API")
    exit(1)

# Обработка в формат словаря по датам
calendar = {}
for i, date in enumerate(data["daily"]["time"]):
    phase_value = data["daily"]["moon_phase"][i]
    calendar[date] = {
        "phase_code": phase_value  # от 0.0 до 1.0
    }

# Сохранение
with open("docs/lunar_calendar.json", "w", encoding="utf-8") as f:
    json.dump(calendar, f, ensure_ascii=False, indent=2)

print(f"✅ lunar_calendar.json создан: {len(calendar)} дней")

