export default async function handler(req, res) {
  const response = await fetch(
    'https://raw.githubusercontent.com/WitchSandra/kp-data/main/docs/lunar_calendar.json'
  );

  if (!response.ok) {
    return res.status(500).json({ error: 'Ошибка при получении календаря' });
  }

  const data = await response.json();

  const today = "2025-05-29";

  const todayData = data.find(entry => entry.date === today);

  if (!todayData) {
    return res.status(404).json({ error: 'Нет данных для сегодняшней даты' });
  }

  const output = {
    current_date: todayData.date || "Дата не указана",
    phase_name: todayData.phase || "Фаза Луны неизвестна",
    moon_sign: todayData.zodiac_sign || "Знак не определён",
    element: todayData.element || "Стихия не указана",
    tip: todayData.magical_tip || "Магический совет временно недоступен",
    recommended_rituals: todayData.ritual || "Ритуалы не предложены",
    avoid_rituals: todayData.avoid || "Нет противопоказаний"
  };

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.status(200).json(output);
}
