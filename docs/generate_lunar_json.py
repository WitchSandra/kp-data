import requests
import json
import os
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
        print(f"[astronomyapi] {response.status_code}: {response.text[:200]}")
        if response.status_code == 200:
            data = response.json()
            return data["data"]["table"]["rows"][0]["cells"][0]["zodiac"]["name"]
    except Exception as e:
        print(f"Zodiac fetch error: {e}")
    return ""

def generate_lunar_json(days=365):
    if already_updated_this_month():
        print("Календарь уже обновлён в этом месяце. Завершаем.")
        return

    today = datetime.utcnow()
    data = []

    for i in range(days):
        date = today + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        timestamp = int(date.timestamp())
        moon_data = fetch_moon_phase(timestamp)
        if moon_data:
            phase = moon_data.get("Phase", "")
            zodiac = fetch_zodiac_sign(date_str)
            entry = {
                "date": date_str,
                "phase": phase,
                "phase_ru": translate_phase(phase),
                "illumination": moon_data.get("Illumination", ""),
                "magical_tip": generate_magical_tip(phase),
                "zodiac_sign": zodiac,
                "ritual": generate_ritual(phase),
                "energy": generate_energy(phase),
                "focus": generate_focus(phase),
                "associated_rune": generate_rune(phase),
                "tarot_arcana": generate_tarot(phase)
            }
            data.append(entry)

    if not data:
        print("⚠️ Данные для календаря не были сгенерированы. Файл не будет сохранён.")
        return

    with open("docs/lunar_calendar.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# остальные функции translate_phase, generate_magical_tip и т.д. без изменений

# Запуск
generate_lunar_json()
