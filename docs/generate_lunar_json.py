import requests
import json
import os
import sys
from datetime import datetime, timedelta

def already_updated_this_month():
    try:
        with open("docs/lunar_calendar.json", encoding="utf-8") as f:
            data = json.load(f)
        first_entry = data[0]
        entry_month = first_entry["date"][:7]  # формат YYYY-MM
        current_month = datetime.utcnow().strftime("%Y-%m")
        return entry_month == current_month
    except Exception:
        return False

def fetch_moon_phase(timestamp):
    url = f"https://api.farmsense.net/v1/moonphases/?d={timestamp}"
    response = requests.get(url)
    if response.status_code == 200:
        parsed = response.json()
        if not parsed:
            print(f"[farmSense] Пустой ответ для {timestamp}")
        return parsed[0] if parsed else None
    else:
        print(f"[farmSense] Ошибка: {response.status_code}")
    return None

def fetch_zodiac_sign(date_str):
    astro_url = "https://api.astronomyapi.com/api/v2/bodies/positions/moon"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "latitude": 54.68,
        "longitude": 25.28,
        "elevation": 180,
        "from_date": date_str,
        "to_date": date_str
    }
    try:
        response = requests.post(
            astro_url,
            headers=headers,
            json=payload,
            auth=(os.getenv("ASTRO_API_ID"), os.getenv("ASTRO_API_SECRET"))
        )
        response.raise_for_status()
        data = response.json()
        zodiac = data["data"]["table"]["rows"][0]["cells"][0].get("zodiac", {}).get("name", "")
        print(f"🔭 Знак Зодиака для {date_str}: {zodiac}")
        return zodiac
    except Exception as e:
        sys.stderr.write(f"❌ Ошибка при получении Зодиака на {date_str}: {str(e)}\n")
    return ""

def translate_phase(phase):
    return phase  # временно возвращаем английский вариант, чтобы избежать ошибки

def generate_lunar_json(days=5):
    # Отключено временно для отладки
    # if already_updated_this_month():
    #     print("Календарь уже обновлён в этом месяце. Завершаем.")
    #     return

    today = datetime.utcnow()
    data = []

    for i in range(days):
        date = today + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        timestamp = int(date.timestamp())
        moon_data = fetch_moon_phase(timestamp)
        print(f"\n📅 {date_str}")
        if moon_data:
            phase = moon_data.get("Phase", "")
            illum = moon_data.get("Illumination", "")
            print(f"🌙 Фаза: {phase}, Освещённость: {illum}")
            zodiac = fetch_zodiac_sign(date_str)
            entry = {
                "date": date_str,
                "phase": phase,
                "phase_ru": translate_phase(phase),
                "illumination": illum,
                "magical_tip": generate_magical_tip(phase),
                "zodiac_sign": zodiac,
                "ritual": generate_ritual(phase),
                "energy": generate_energy(phase),
                "focus": generate_focus(phase),
                "associated_rune": generate_rune(phase),
                "tarot_arcana": generate_tarot(phase)
            }
            data.append(entry)
        else:
            print("⚠️ Нет данных о фазе Луны")

    if not data:
        print("⚠️ Данные для календаря не были сгенерированы. Файл не будет сохранён.")
        return

    with open("docs/lunar_calendar.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Запуск
generate_lunar_json()
