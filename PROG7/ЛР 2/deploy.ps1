# Скрипт для автоматизации развертывания в Yandex Cloud (PowerShell)
# Использование: .\deploy.ps1 -RegistryId <registry-id> [-ContainerName <container-name>]

param(
    [Parameter(Mandatory=$true)]
    [string]$RegistryId,
    
    [Parameter(Mandatory=$false)]
    [string]$ContainerName = "currency-converter"
)

$ErrorActionPreference = "Stop"

$ImageName = "cr.yandex/${RegistryId}/currency-converter:latest"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Развертывание Currency Converter в Yandex Cloud" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Registry ID: $RegistryId"
Write-Host "Container Name: $ContainerName"
Write-Host "Image: $ImageName"
Write-Host ""

# Шаг 1: Сборка образа
Write-Host "Шаг 1: Сборка Docker образа..." -ForegroundColor Yellow
docker build -t currency-converter:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка при сборке образа!" -ForegroundColor Red
    exit 1
}

# Шаг 2: Тегирование
Write-Host ""
Write-Host "Шаг 2: Тегирование образа..." -ForegroundColor Yellow
docker tag currency-converter:latest $ImageName

# Шаг 3: Проверка и настройка авторизации
Write-Host ""
Write-Host "Шаг 3: Проверка авторизации в Yandex Container Registry..." -ForegroundColor Yellow

# Проверяем, настроена ли авторизация
$authCheck = docker login cr.yandex 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Авторизация не настроена. Настраиваем..." -ForegroundColor Yellow
    Write-Host "Выполняем: yc container registry configure-docker" -ForegroundColor Yellow
    yc container registry configure-docker
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Ошибка при настройке авторизации!" -ForegroundColor Red
        Write-Host "Попробуйте выполнить вручную: yc container registry configure-docker" -ForegroundColor Yellow
        Write-Host "Или настройте OAuth токен вручную (см. DEPLOY_YANDEX_CLOUD.md)" -ForegroundColor Yellow
        exit 1
    }
}

# Шаг 4: Загрузка в YCR
Write-Host ""
Write-Host "Шаг 4: Загрузка образа в Yandex Container Registry..." -ForegroundColor Yellow
docker push $ImageName

if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка при загрузке образа!" -ForegroundColor Red
    Write-Host "Возможно, требуется настроить авторизацию:" -ForegroundColor Yellow
    Write-Host "  yc container registry configure-docker" -ForegroundColor White
    exit 1
}

# Шаг 5: Проверка существования контейнера
Write-Host ""
Write-Host "Шаг 4: Проверка существования контейнера..." -ForegroundColor Yellow
$containerExists = $false
try {
    yc serverless container get --name $ContainerName 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $containerExists = $true
        Write-Host "Контейнер $ContainerName уже существует. Обновление..." -ForegroundColor Green
    }
} catch {
    Write-Host "Создание нового контейнера $ContainerName..." -ForegroundColor Green
}

# Шаг 6: Создание или обновление контейнера
Write-Host ""
Write-Host "Шаг 5: Развертывание контейнера..." -ForegroundColor Yellow
if (-not $containerExists) {
    yc serverless container create --name $ContainerName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Ошибка при создании контейнера!" -ForegroundColor Red
        exit 1
    }
}

yc serverless container revision deploy `
    --container-name $ContainerName `
    --image $ImageName `
    --memory 1024MB `
    --cores 1 `
    --execution-timeout 60s `
    --environment PYTHONUNBUFFERED=1

if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка при развертывании ревизии!" -ForegroundColor Red
    exit 1
}

# Шаг 7: Проверка HTTP-триггера
Write-Host ""
Write-Host "Шаг 6: Проверка HTTP-триггера..." -ForegroundColor Yellow
$TriggerName = "${ContainerName}-trigger"

$triggerExists = $false
try {
    yc serverless trigger get --name $TriggerName 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $triggerExists = $true
        Write-Host "HTTP-триггер $TriggerName уже существует." -ForegroundColor Green
    }
} catch {
    Write-Host "Создание HTTP-триггера..." -ForegroundColor Green
}

if (-not $triggerExists) {
    yc serverless trigger create http `
        --name $TriggerName `
        --container-name $ContainerName `
        --container-path /
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Ошибка при создании триггера!" -ForegroundColor Red
        exit 1
    }
}

# Шаг 8: Получение URL
Write-Host ""
Write-Host "Шаг 7: Получение URL контейнера..." -ForegroundColor Yellow
try {
    $triggerInfo = yc serverless trigger get --name $TriggerName --format json | ConvertFrom-Json
    $triggerUrl = $triggerInfo.http.url
    
    if ($triggerUrl) {
        Write-Host ""
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host "Развертывание завершено успешно!" -ForegroundColor Green
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host "URL: $triggerUrl" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Тестирование:" -ForegroundColor Yellow
        Write-Host "curl $triggerUrl/health" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "Развертывание завершено, но не удалось получить URL." -ForegroundColor Yellow
        Write-Host "Проверьте триггер в консоли Yandex Cloud." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Не удалось получить информацию о триггере." -ForegroundColor Yellow
    Write-Host "Проверьте триггер в консоли Yandex Cloud." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Готово!" -ForegroundColor Green

