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


def fetch_moon_phase_openmeteo(date_str):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 54.6872,
        "longitude": 25.2797,
        "daily": "moon_phase",
        "timezone": "Europe/Vilnius",
        "start_date": date_str,
        "end_date": date_str
    }
    try:
        response = requests.get(url, params=params)
        print(f"🌐 OpenMeteo: {response.url}")
        if response.status_code == 200:
            data = response.json()
            phase_code = data["daily"]["moon_phase"][0]
            illumination = 0.0  # OpenMeteo не даёт освещённость
            return {
                "Phase": str(phase_code),
                "Illumination": illumination
            }
        else:
            print(f"❌ OpenMeteo Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ OpenMeteo Exception: {e}")
    return None


def determine_zodiac_from_angle(angle):
    zodiac_names = [
        "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
        "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
    ]
    index = int(angle // 30) % 12
    return zodiac_names[index]


def fetch_zodiac_sign_placeholder(date_str):
    return "Знак временно недоступен"


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
        print(f"\n📅 {date_str}")
        moon_data = fetch_moon_phase_openmeteo(date_str)
        if moon_data:
            phase = moon_data.get("Phase", "")
            illum = moon_data.get("Illumination", 0.0)
            print(f"🌙 Фаза: {phase}, Освещённость: {illum}")
            zodiac = fetch_zodiac_sign_placeholder(date_str)
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
