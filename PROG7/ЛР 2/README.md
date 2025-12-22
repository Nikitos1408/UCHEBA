# Выполнил - Угарин Никита Александрович
# Конвертер валют - Микросервисная архитектура

Система микросервисов для конвертации валют с поддержкой аналитики и графиков изменения курсов.

## Архитектура

Система состоит из трех основных микросервисов:

1. **Сервис курсов валют** (`exchange_rate_service.py`)
   - Получает актуальные курсы валют из открытых источников (yfinance)
   - Поддерживает фиатные валюты (USD, EUR, GBP, JPY, CNY) и криптовалюты (BTC, ETH)
   - Кеширование данных для оптимизации

2. **Сервис конвертации** (`conversion_service.py`)
   - Конвертирует суммы из одной валюты в другую
   - Поддерживает пакетную конвертацию с использованием многопроцессности

3. **Сервис аналитики** (`analytics_service.py`)
   - Генерирует графики изменения курса валют
   - Предоставляет статистику по валютам

## Технологии

- **Flask** - веб-фреймворк (WSGI)
- **yfinance** - получение данных о курсах валют
- **matplotlib** - генерация графиков
- **multiprocessing** - многопроцессная обработка
- **Docker** - контейнеризация
- **Gunicorn** - WSGI HTTP сервер

## API Эндпоинты

### Проверка работоспособности
```
GET /health
```

### Получение курса обмена
```
GET /api/exchange-rate?from=USD&to=EUR
```

### Конвертация валют
```
POST /api/convert
Content-Type: application/json

{
    "amount": 100,
    "from": "USD",
    "to": "EUR"
}
```

### Пакетная конвертация (с многопроцессностью)
```
POST /api/batch-convert
Content-Type: application/json

{
    "conversions": [
        {"amount": 100, "from": "USD", "to": "EUR"},
        {"amount": 200, "from": "GBP", "to": "RUB"}
    ]
}
```

### Получение графика курса
```
GET /api/analytics/chart?currency=USD&days=30
```

### Получение статистики
```
GET /api/analytics/statistics?currency=USD&days=30
```

### Список поддерживаемых валют
```
GET /api/currencies
```

## Локальная установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск приложения

```bash
python app.py
```

Приложение будет доступно по адресу: `http://localhost:5000`

### 3. Тестирование API

```bash
python test_api.py
```


## Docker

### Сборка образа

```bash
docker build -t currency-converter:latest .
```

### Запуск контейнера
```bash
docker run -p 5000:5000 currency-converter:latest
```

### Проверка запущенного контейнера

```bash
# Просмотр запущенных контейнеров
docker ps
```

## Развертывание в Yandex Cloud

### Быстрое развертывание (автоматическое)

#### Windows (PowerShell):
```powershell
.\deploy.ps1 -RegistryId <ваш-registry-id>
```

1. **Проверка/создание Container Registry**
```bash
# Проверьте существующие реестры
yc container registry list

# Если реестра нет и есть права - создайте его
yc container registry create --name currency-converter-registry
```

2. **Настройка авторизации Docker**
```bash
# Настройка авторизации (ОБЯЗАТЕЛЬНО перед загрузкой образа!)
yc container registry configure-docker
```

3. **Подготовка Docker образа**
```bash
docker build -t currency-converter:latest .
docker tag currency-converter:latest cr.yandex/<registry-id>/currency-converter:latest
```

2. **Загрузка в Yandex Container Registry**
```bash
yc container registry configure-docker
docker push cr.yandex/<registry-id>/currency-converter:latest
```

3. **Создание Serverless Container**
```bash
yc serverless container create --name currency-converter
yc serverless container revision deploy \
  --container-name currency-converter \
  --image cr.yandex/<registry-id>/currency-converter:latest \
  --memory 1024MB \
  --cores 1 \
  --execution-timeout 60s
```

4. **Настройка HTTP-триггера**
```bash
yc serverless trigger create http \
  --name currency-converter-trigger \
  --container-name currency-converter \
  --container-path /
```

5. **Тестирование**
```bash
# Получите URL из вывода команды выше или через консоль
curl https://<container-id>.containers.yandexcloud.net/health
```

## Поддерживаемые валюты

- **Фиатные валюты**: USD, EUR, GBP, JPY, CNY, RUB
- **Криптовалюты**: BTC, ETH

## Многопроцессность

Система использует модуль `multiprocessing` для:
- Параллельной обработки пакетных запросов конвертации
- Оптимизации производительности при работе с несколькими запросами одновременно

Количество процессов настраивается автоматически на основе количества доступных CPU ядер.


