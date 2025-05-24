import requests
import json
import os
import sys
import base64
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

def determine_zodiac_from_angle(angle):
    zodiac_names = [
        "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
        "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
    ]
    index = int(angle // 30) % 12
    return zodiac_names[index]

def get_astro_auth_header():
    app_id = os.getenv("ASTRO_API_ID")
    app_secret = os.getenv("ASTRO_API_SECRET")
    if not app_id or not app_secret:
        raise ValueError("❌ Отсутствует ASTRO_API_ID или ASTRO_API_SECRET")
    token = f"{app_id}:{app_secret}"
    encoded_token = base64.b64encode(token.encode()).decode()
    return {"Authorization": f"Basic {encoded_token}"}

def fetch_zodiac_sign(date_str):
    try:
        lat = 54.6872
        lon = 25.2797
        url = "https://api.astronomyapi.com/api/v2/bodies/positions/moon"
        headers = get_astro_auth_header()
        params = {
            "latitude": lat,
            "longitude": lon,
            "from_date": date_str,
            "to_date": date_str,
            "elevation": 0
        }
        print(f"🌐 Запрос к AstronomyAPI: {url}")
        response = requests.get(url, headers=headers, params=params)
        print(f"🔁 Статус ответа: {response.status_code}")
        print(f"🧾 Ответ: {response.text}")
        response.raise_for_status()
        data = response.json()
        ra_hours = float(data['data']['table']['rows'][0]['cells'][0]['position']['equatorial']['rightAscension']['hours'])
        angle_degrees = ra_hours * 15
        zodiac = determine_zodiac_from_angle(angle_degrees)
        print(f"🔭 Знак Зодиака для {date_str}: {zodiac}")
        return zodiac
    except Exception as e:
        sys.stderr.write(f"❌ Ошибка при получении Зодиака на {date_str}: {str(e)}\n")
        return "Ошибка определения"

def translate_phase(phase):
    return phase  # временно возвращаем английский вариант, чтобы избежать ошибки

def generate_magical_tip(phase):
    return "Магический совет временно недоступен"

def generate_ritual(phase):
    return "Ритуал временно недоступен"

def generate_energy(phase):
    return "Энергия временно недоступна"

def generate_focus(phase):
    return ["Цель временно недоступна"]

def generate_rune(phase):
    return "Руна временно недоступна"

def generate_tarot(phase):
    return "Аркан временно недоступен"

def generate_lunar_json(days=5):
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
