"""
Скрипт для тестирования API конвертера валют
"""
import requests
import json
import base64
import sys

BASE_URL = "http://localhost:5000"


def test_health():
    """Тест проверки работоспособности"""
    print("\n=== Тест: Проверка работоспособности ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_get_currencies():
    """Тест получения списка валют"""
    print("\n=== Тест: Получение списка валют ===")
    response = requests.get(f"{BASE_URL}/api/currencies")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_exchange_rate():
    """Тест получения курса обмена"""
    print("\n=== Тест: Получение курса обмена ===")
    response = requests.get(f"{BASE_URL}/api/exchange-rate?from=USD&to=EUR")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_convert():
    """Тест конвертации валют"""
    print("\n=== Тест: Конвертация валют ===")
    data = {
        "amount": 100,
        "from": "USD",
        "to": "EUR"
    }
    response = requests.post(
        f"{BASE_URL}/api/convert",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Request: {json.dumps(data, indent=2, ensure_ascii=False)}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_batch_convert():
    """Тест пакетной конвертации"""
    print("\n=== Тест: Пакетная конвертация ===")
    data = {
        "conversions": [
            {"amount": 100, "from": "USD", "to": "EUR"},
            {"amount": 200, "from": "GBP", "to": "RUB"},
            {"amount": 50, "from": "EUR", "to": "USD"}
        ]
    }
    response = requests.post(
        f"{BASE_URL}/api/batch-convert",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Request: {json.dumps(data, indent=2, ensure_ascii=False)}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_statistics():
    """Тест получения статистики"""
    print("\n=== Тест: Получение статистики ===")
    response = requests.get(f"{BASE_URL}/api/analytics/statistics?currency=USD&days=30")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_chart():
    """Тест получения графика"""
    print("\n=== Тест: Получение графика ===")
    response = requests.get(f"{BASE_URL}/api/analytics/chart?currency=USD&days=30")
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get('success'):
        # Сохраняем график в файл
        chart_image = result.get('chart_image')
        if chart_image:
            img_data = base64.b64decode(chart_image)
            with open('test_chart.png', 'wb') as f:
                f.write(img_data)
            print(f"График сохранен в test_chart.png")
        
        # Выводим статистику без изображения
        result_display = {k: v for k, v in result.items() if k != 'chart_image'}
        print(f"Response: {json.dumps(result_display, indent=2, ensure_ascii=False)}")
        return True
    else:
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return False


def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print("Запуск тестов API конвертера валют")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Get Currencies", test_get_currencies),
        ("Get Exchange Rate", test_exchange_rate),
        ("Convert Currency", test_convert),
        ("Batch Convert", test_batch_convert),
        ("Get Statistics", test_statistics),
        ("Get Chart", test_chart),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nОшибка в тесте {name}: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Результаты тестирования:")
    print("=" * 60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nПройдено: {passed}/{total}")
    
    return passed == total


if __name__ == "__main__":
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
        print(f"Используется базовый URL: {BASE_URL}")
    
    success = run_all_tests()
    sys.exit(0 if success else 1)

