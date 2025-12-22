#!/bin/bash

# Скрипт для автоматизации развертывания в Yandex Cloud
# Использование: ./deploy.sh <registry-id> [container-name]

set -e

REGISTRY_ID=$1
CONTAINER_NAME=${2:-currency-converter}

if [ -z "$REGISTRY_ID" ]; then
    echo "Ошибка: необходимо указать ID реестра контейнеров"
    echo "Использование: ./deploy.sh <registry-id> [container-name]"
    exit 1
fi

IMAGE_NAME="cr.yandex/${REGISTRY_ID}/currency-converter:latest"

echo "=========================================="
echo "Развертывание Currency Converter в Yandex Cloud"
echo "=========================================="
echo "Registry ID: $REGISTRY_ID"
echo "Container Name: $CONTAINER_NAME"
echo "Image: $IMAGE_NAME"
echo ""

# Шаг 1: Сборка образа
echo "Шаг 1: Сборка Docker образа..."
docker build -t currency-converter:latest .

# Шаг 2: Тегирование
echo ""
echo "Шаг 2: Тегирование образа..."
docker tag currency-converter:latest $IMAGE_NAME

# Шаг 3: Загрузка в YCR
echo ""
echo "Шаг 3: Загрузка образа в Yandex Container Registry..."
docker push $IMAGE_NAME

# Шаг 4: Проверка существования контейнера
echo ""
echo "Шаг 4: Проверка существования контейнера..."
if yc serverless container get --name $CONTAINER_NAME &>/dev/null; then
    echo "Контейнер $CONTAINER_NAME уже существует. Обновление..."
    UPDATE_EXISTING=true
else
    echo "Создание нового контейнера $CONTAINER_NAME..."
    UPDATE_EXISTING=false
fi

# Шаг 5: Создание или обновление контейнера
echo ""
echo "Шаг 5: Развертывание контейнера..."
if [ "$UPDATE_EXISTING" = false ]; then
    yc serverless container create --name $CONTAINER_NAME
fi

yc serverless container revision deploy \
    --container-name $CONTAINER_NAME \
    --image $IMAGE_NAME \
    --memory 1024MB \
    --cores 1 \
    --execution-timeout 60s \
    --environment PYTHONUNBUFFERED=1

# Шаг 6: Проверка HTTP-триггера
echo ""
echo "Шаг 6: Проверка HTTP-триггера..."
TRIGGER_NAME="${CONTAINER_NAME}-trigger"

if yc serverless trigger get --name $TRIGGER_NAME &>/dev/null; then
    echo "HTTP-триггер $TRIGGER_NAME уже существует."
else
    echo "Создание HTTP-триггера..."
    yc serverless trigger create http \
        --name $TRIGGER_NAME \
        --container-name $CONTAINER_NAME \
        --container-path /
fi

# Шаг 7: Получение URL
echo ""
echo "Шаг 7: Получение URL контейнера..."
TRIGGER_URL=$(yc serverless trigger get --name $TRIGGER_NAME --format json | jq -r '.http.url // empty')

if [ -n "$TRIGGER_URL" ]; then
    echo ""
    echo "=========================================="
    echo "Развертывание завершено успешно!"
    echo "=========================================="
    echo "URL: $TRIGGER_URL"
    echo ""
    echo "Тестирование:"
    echo "curl $TRIGGER_URL/health"
else
    echo ""
    echo "Развертывание завершено, но не удалось получить URL."
    echo "Проверьте триггер в консоли Yandex Cloud."
fi

