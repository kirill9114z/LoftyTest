# Weather CLI

Консольное приложение для получения текущей погоды по названию города через OpenWeatherMap API.

## Установка

**1. Клонируй репозиторий**
```bash
git clone https://github.com/<твой-username>/<название-репо>.git
cd <название-репо>
```

**2. Установи зависимости**
```bash
pip install -r requirements.txt
```

**3. Создай файл `.env` на основе примера**
```bash
cp .env.example .env
```

Открой `.env` и вставь свой API-ключ от [openweathermap.org](https://openweathermap.org):
```
API_KEY=твой_ключ_здесь
LIMITS_PER_MIN=60
```

## Запуск

```bash
python weather.py <название города>
```

**Пример:**
```bash
python weather.py Frankfurt
```

## Структура проекта

```
├── weather.py        # точка входа
├── config.py         # загрузка настроек из .env
├── storage.py        # кеш координат городов (storage.json)
├── .env.example      # пример файла с переменными окружения
├── requirements.txt  # зависимости
└── README.md
```
