# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости для matplotlib и других библиотек
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения
COPY *.py .

# Создаем директорию для временных файлов
RUN mkdir -p /tmp

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Открываем порт
EXPOSE 5000

# Запускаем приложение с помощью gunicorn для production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]

