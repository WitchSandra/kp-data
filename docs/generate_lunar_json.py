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
        return response.json()[0]
    return None

def generate_lunar_json(days=365):
    if already_updated_this_month():
        print("Календарь уже обновлён в этом месяце. Завершаем.")
        return

    today = datetime.utcnow()
    data = []

    for i in range(days):
        date = today + timedelta(days=i)
        timestamp = int(date.timestamp())
        moon_data = fetch_moon_phase(timestamp)
        if moon_data:
            phase = moon_data.get("Phase", "")
            entry = {
                "date": date.strftime("%Y-%m-%d"),
                "phase": phase,
                "phase_ru": translate_phase(phase),
                "illumination": moon_data.get("Illumination", ""),
                "magical_tip": generate_magical_tip(phase),
                "zodiac_sign": "",  # Добавим позже через другой API
                "ritual": generate_ritual(phase),
                "energy": generate_energy(phase),
                "focus": generate_focus(phase),
                "associated_rune": generate_rune(phase),
                "tarot_arcana": generate_tarot(phase)
            }
            data.append(entry)

    with open("docs/lunar_calendar.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_phase(phase):
    translations = {
        "New Moon": "Новолуние",
        "Waxing Crescent": "Растущий серп",
        "First Quarter": "Первая четверть",
        "Waxing Gibbous": "Почти полная растущая",
        "Full Moon": "Полнолуние",
        "Waning Gibbous": "Убывающая после полной",
        "Last Quarter": "Последняя четверть",
        "Waning Crescent": "Убывающий серп"
    }
    return translations.get(phase, phase)

def generate_magical_tip(phase):
    tips = {
        "New Moon": "Начинай новое. Время мечты и намерений.",
        "Waxing Crescent": "Расти. Заряжай амулеты. Действуй.",
        "First Quarter": "Преодолевай. Двигайся вперёд с силой.",
        "Waxing Gibbous": "Полируй идеи. Готовься к пику.",
        "Full Moon": "Магия на максимум. Явление истины.",
        "Waning Gibbous": "Отпускай. Делись, очищай.",
        "Last Quarter": "Рефлексия. Разбор ошибок.",
        "Waning Crescent": "Покой. Завершение. Уход в себя."
    }
    return tips.get(phase, "Магическое время.")

def generate_ritual(phase):
    rituals = {
        "New Moon": "Запиши желания на бумаге и зажги свечу намерения.",
        "Full Moon": "Очисти кристаллы, прими соляную ванну, наполни воду светом Луны.",
        "Waning Crescent": "Сожги негатив на бумаге. Отпускай прошлое."
    }
    return rituals.get(phase, "Проведи медитацию или настройку на энергию дня.")

def generate_energy(phase):
    levels = {
        "New Moon": "Начало. Тихая, но заряженная.",
        "Full Moon": "Сильная. Пиковая. Эмоциональная.",
        "Waning Crescent": "Низкая. Завершающая. Интровертная."
    }
    return levels.get(phase, "Умеренная. Энергия в балансе.")

def generate_focus(phase):
    focuses = {
        "New Moon": ["Планы", "Мечты", "Создание"],
        "Full Moon": ["Завершение", "Озарение", "Празднование"],
        "Waning Crescent": ["Отпускание", "Очистка", "Прощение"]
    }
    return focuses.get(phase, ["Работа с энергиями"])

def generate_rune(phase):
    runes = {
        "New Moon": "Феху (ᚠ)",
        "Full Moon": "Соулу (ᛋ)",
        "Waning Crescent": "Иса (ᛁ)"
    }
    return runes.get(phase, "")

def generate_tarot(phase):
    cards = {
        "New Moon": "Маг",
        "Full Moon": "Луна",
        "Waning Crescent": "Отшельник"
    }
    return cards.get(phase, "")

# Запуск
generate_lunar_json()
