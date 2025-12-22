# Структура проекта

```
ЛР 2/
│
├── app.py                          # Главное приложение Flask с API эндпоинтами
├── exchange_rate_service.py         # Сервис получения курсов валют
├── conversion_service.py            # Сервис конвертации валют
├── analytics_service.py             # Сервис аналитики и графиков
│
├── requirements.txt                 # Python зависимости
├── Dockerfile                       # Конфигурация Docker образа
├── docker-compose.yml               # Docker Compose для локального тестирования
├── .dockerignore                    # Исключения для Docker
│
├── test_api.py                     # Скрипт для тестирования API
│
├── deploy.sh                        # Скрипт автоматического развертывания (Linux/Mac)
├── deploy.ps1                       # Скрипт автоматического развертывания (Windows)
│
├── README.md                        # Основная документация
├── DEPLOY_YANDEX_CLOUD.md          # Подробная инструкция по развертыванию
├── PROJECT_STRUCTURE.md             # Этот файл
│
└── .gitignore                       # Исключения для Git
```

## Описание файлов

### Основные сервисы

- **app.py** - Главное Flask приложение, объединяющее все микросервисы. Содержит:
  - API эндпоинты для всех сервисов
  - Многопроцессную обработку запросов
  - Обработку ошибок
  - Логирование

- **exchange_rate_service.py** - Сервис курсов валют:
  - Получение актуальных курсов через yfinance
  - Кеширование данных
  - Получение исторических данных

- **conversion_service.py** - Сервис конвертации:
  - Конвертация сумм между валютами
  - Пакетная конвертация

- **analytics_service.py** - Сервис аналитики:
  - Генерация графиков изменения курсов
  - Статистика по валютам

### Конфигурация

- **requirements.txt** - Все необходимые Python пакеты
- **Dockerfile** - Конфигурация для сборки Docker образа
- **docker-compose.yml** - Для локального запуска через Docker Compose
- **.dockerignore** - Файлы, исключаемые из Docker образа

### Развертывание

- **deploy.sh** - Bash скрипт для автоматического развертывания в Yandex Cloud
- **deploy.ps1** - PowerShell скрипт для автоматического развертывания в Yandex Cloud
- **DEPLOY_YANDEX_CLOUD.md** - Подробная инструкция по ручному развертыванию

### Тестирование

- **test_api.py** - Скрипт для автоматического тестирования всех API эндпоинтов

### Документация

- **README.md** - Основная документация проекта
- **PROJECT_STRUCTURE.md** - Описание структуры проекта

## Порядок работы с проектом

1. **Установка зависимостей**: `pip install -r requirements.txt`
2. **Локальный запуск**: `python app.py`
3. **Тестирование**: `python test_api.py`
4. **Сборка Docker образа**: `docker build -t currency-converter:latest .`
5. **Локальный запуск в Docker**: `docker-compose up`
6. **Развертывание в Yandex Cloud**: Используйте `deploy.ps1` или `deploy.sh`

