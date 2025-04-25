<strong>💱 Валютный сервис на FastAPI </strong>

Асинхронный сервис на FastAPI для хранения и управления валютными балансами (RUB, USD, EUR) с поддержкой:

<li>API для получения/установки/изменения значений</li>

<li>расчёта общей суммы в рублях, долларах и евро</li>

<li>фоновым обновлением курса валют с сайта ЦБ РФ</li>

<li>гибкой настройки через аргументы командной строки</li>

<strong>📂 Структура проекта</strong>

<pre>
currency
    ├── base
    │     ├── __init__.py
    │     └── abstract.py    # Общий интерфейс валют
    ├── config               # Конфигурация приложения
    │     ├── __init__.py   
    │     └── config.py
    ├── core
    │     ├── __init__.py
    │     ├── api.py         # Содержит ручки
    │     ├── memory.py      # Хранилище валют
    │     └── rates.py       # Работает с API ЦБ РФ
    ├── schemas
    │     ├── __init__.py     
    │     └── schemas.py.py  # Pydantic-модели
    ├── .gitignore          
    ├── __init__.py
    ├── __main__.py          # Точка входа в приложение
    ├── app.py               # Инициализация и конфигурация приложения
    └── requirements.txt     # Зависимости проекта
</pre>

<strong>📦 Установка</strong>
<pre>
git clone https://github.com/NobodyNi/CurrencyService.git

cd your-repo

pip install -r requirements.txt
</pre>

<strong>▶️ Запуск</strong>
<pre>
python -m currency --rub 100 --usd 200 --eur 300 --period 1 --debug false
</pre>

<strong>Аргументы запуска:</strong>
<pre>
| Аргумент  |               Описание                  | По умолчанию |
|-----------|-----------------------------------------|--------------|
| `--rub`   |   Начальный баланс в рублях             | `0.0`        |
| `--usd`   |   Начальный баланс в долларах           | `0.0`        |
| `--eur`   |   Начальный баланс в евро               | `0.0`        |
| `--period`|   Период обновления курсов (мин.)       | `1`          |
| `--debug` |   Включить отладочный режим             | `true`       |
</pre>

### Аргумент `--debug`

Параметр `--debug` управляет включением или выключением отладочного режима. Поддерживаются следующие значения:

- **`1`, `true`, `True`, `y`, `Y`, `yes`** — включить отладочный режим (`True`)
- **`0`, `false`, `False`, `n`, `N`, `no`** — выключить отладочный режим (`False`)

<strong>🔗 Примеры запросов</strong>

<strong>Получить баланс валюты:</strong>
<pre>
GET /rub/get

{
  "name": "RUB",
  "value": 100
}
</pre>

<strong>Получить общую сумму:</strong>
<pre>
GET /amount/get

{
  "rub": 100,
  "usd": 200,
  "eur": 300,
  "rub-usd": 82.6549,
  "rub-eur": 94.3593,
  "usd-eur": 0.8759592324233011,
  "sum": "44938.77 rub / 543.69 usd / 476.25 eur"
}
</pre>

<strong>Установить новые значения:</strong>
<pre>
POST /amount/set
Content-Type: application/json

{
  "rub": 1000,
  "usd": 50,
  "eur": 30
}
</pre>

<strong>Изменить текущие значения:</strong>
<pre>
POST /modify
Content-Type: application/json

{
  "usd": 10,
  "rub": -10
}
</pre>