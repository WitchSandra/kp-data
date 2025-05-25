export default async function handler(req, res) {
  const response = await fetch(
    'https://raw.githubusercontent.com/WitchSandra/kp-data/main/docs/lunar_calendar.json'
  );

  if (!response.ok) {
    return res.status(500).json({ error: 'Ошибка при получении календаря' });
  }

  const data = await response.json();

  const today = new Date().toISOString().split('T')[0];

  const todayData = data.find(entry => entry.date === today);

  if (!todayData) {
    return res.status(404).json({ error: 'Нет данных для сегодняшней даты' });
  }

  const output = {
    current_date: todayData.date,
    phase_name: todayData.phase,
    moon_sign: todayData.zodiac,
    element: todayData.element,
    tip: todayData.tip,
    recommended_rituals: todayData.good,
    avoid_rituals: todayData.bad
  };

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.status(200).json(output);
}
