"""
Главное приложение Flask с микросервисами
Использует многопроцессность для параллельной обработки запросов
"""
from flask import Flask, request, jsonify
from multiprocessing import Pool, cpu_count
import logging
from functools import wraps
import time
import os

from exchange_rate_service import ExchangeRateService
from conversion_service import ConversionService
from analytics_service import AnalyticsService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Инициализация сервисов
exchange_service = ExchangeRateService()
conversion_service = ConversionService()
analytics_service = AnalyticsService()

# Пул процессов для многопроцессности (ленивая инициализация)
_process_pool = None


def get_process_pool():
    """Получает или создает пул процессов"""
    global _process_pool
    if _process_pool is None:
        # Определяем количество процессов
        num_processes = max(2, min(cpu_count() - 1, 4))  # Ограничиваем до 4 процессов
        _process_pool = Pool(processes=num_processes)
        logger.info(f"Создан пул процессов: {num_processes} процессов")
    return _process_pool


def measure_time(func):
    """Декоратор для измерения времени выполнения"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        if isinstance(result, dict):
            result['execution_time'] = round(execution_time, 3)
        return result
    return wrapper


@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервиса"""
    return jsonify({
        'status': 'healthy',
        'service': 'Currency Converter API',
        'version': '1.0.0'
    }), 200


@app.route('/api/exchange-rate', methods=['GET'])
@measure_time
def get_exchange_rate():
    """
    Получение курса обмена между двумя валютами
    
    Query parameters:
        from: Исходная валюта (обязательно)
        to: Целевая валюта (обязательно)
    """
    try:
        from_currency = request.args.get('from', '').upper()
        to_currency = request.args.get('to', '').upper()
        
        if not from_currency or not to_currency:
            return jsonify({
                'error': 'Параметры "from" и "to" обязательны',
                'success': False
            }), 400
        
        rate = exchange_service.get_exchange_rate(from_currency, to_currency)
        
        if rate is None:
            return jsonify({
                'error': f'Не удалось получить курс обмена {from_currency}/{to_currency}',
                'success': False
            }), 404
        
        return jsonify({
            'success': True,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'exchange_rate': round(rate, 6)
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка в get_exchange_rate: {str(e)}")
        return jsonify({
            'error': f'Внутренняя ошибка сервера: {str(e)}',
            'success': False
        }), 500


@app.route('/api/convert', methods=['POST'])
@measure_time
def convert_currency():
    """
    Конвертация суммы из одной валюты в другую
    
    JSON body:
        {
            "amount": 100,
            "from": "USD",
            "to": "EUR"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Требуется JSON body',
                'success': False
            }), 400
        
        amount = float(data.get('amount', 0))
        from_currency = data.get('from', '').upper()
        to_currency = data.get('to', '').upper()
        
        if amount <= 0:
            return jsonify({
                'error': 'Сумма должна быть положительным числом',
                'success': False
            }), 400
        
        if not from_currency or not to_currency:
            return jsonify({
                'error': 'Параметры "from" и "to" обязательны',
                'success': False
            }), 400
        
        result = conversion_service.convert(amount, from_currency, to_currency)
        
        if not result.get('success'):
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except ValueError:
        return jsonify({
            'error': 'Неверный формат суммы',
            'success': False
        }), 400
    except Exception as e:
        logger.error(f"Ошибка в convert_currency: {str(e)}")
        return jsonify({
            'error': f'Внутренняя ошибка сервера: {str(e)}',
            'success': False
        }), 500


@app.route('/api/batch-convert', methods=['POST'])
@measure_time
def batch_convert_currency():
    """
    Множественная конвертация с использованием многопроцессности
    
    JSON body:
        {
            "conversions": [
                {"amount": 100, "from": "USD", "to": "EUR"},
                {"amount": 200, "from": "GBP", "to": "RUB"}
            ]
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'conversions' not in data:
            return jsonify({
                'error': 'Требуется JSON body с полем "conversions"',
                'success': False
            }), 400
        
        conversions = data.get('conversions', [])
        
        if not conversions:
            return jsonify({
                'error': 'Список конвертаций не может быть пустым',
                'success': False
            }), 400
        
        # Используем многопроцессность для параллельной обработки
        # Для небольших списков используем обычную обработку
        if len(conversions) <= 2:
            results = []
            for conv in conversions:
                result = conversion_service.convert(
                    conv.get('amount', 0),
                    conv.get('from', 'USD'),
                    conv.get('to', 'EUR')
                )
                results.append(result)
        else:
            # Для больших списков используем multiprocessing
            def process_conversion(conv):
                # Создаем новый экземпляр сервиса в каждом процессе
                service = ConversionService()
                return service.convert(
                    conv.get('amount', 0),
                    conv.get('from', 'USD'),
                    conv.get('to', 'EUR')
                )
            
            process_pool = get_process_pool()
            results = process_pool.map(process_conversion, conversions)
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка в batch_convert_currency: {str(e)}")
        return jsonify({
            'error': f'Внутренняя ошибка сервера: {str(e)}',
            'success': False
        }), 500


@app.route('/api/analytics/chart', methods=['GET'])
@measure_time
def get_currency_chart():
    """
    Получение графика изменения курса валюты
    
    Query parameters:
        currency: Валюта для анализа (обязательно)
        days: Количество дней для анализа (по умолчанию 30)
    """
    try:
        currency = request.args.get('currency', '').upper()
        days = int(request.args.get('days', 30))
        
        if not currency:
            return jsonify({
                'error': 'Параметр "currency" обязателен',
                'success': False
            }), 400
        
        if days <= 0 or days > 365:
            return jsonify({
                'error': 'Количество дней должно быть от 1 до 365',
                'success': False
            }), 400
        
        result = analytics_service.generate_chart(currency, days)
        
        if not result.get('success'):
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except ValueError:
        return jsonify({
            'error': 'Неверный формат параметра days',
            'success': False
        }), 400
    except Exception as e:
        logger.error(f"Ошибка в get_currency_chart: {str(e)}")
        return jsonify({
            'error': f'Внутренняя ошибка сервера: {str(e)}',
            'success': False
        }), 500


@app.route('/api/analytics/statistics', methods=['GET'])
@measure_time
def get_currency_statistics():
    """
    Получение статистики по валюте
    
    Query parameters:
        currency: Валюта для анализа (обязательно)
        days: Количество дней для анализа (по умолчанию 30)
    """
    try:
        currency = request.args.get('currency', '').upper()
        days = int(request.args.get('days', 30))
        
        if not currency:
            return jsonify({
                'error': 'Параметр "currency" обязателен',
                'success': False
            }), 400
        
        if days <= 0 or days > 365:
            return jsonify({
                'error': 'Количество дней должно быть от 1 до 365',
                'success': False
            }), 400
        
        result = analytics_service.get_statistics(currency, days)
        
        if not result.get('success'):
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except ValueError:
        return jsonify({
            'error': 'Неверный формат параметра days',
            'success': False
        }), 400
    except Exception as e:
        logger.error(f"Ошибка в get_currency_statistics: {str(e)}")
        return jsonify({
            'error': f'Внутренняя ошибка сервера: {str(e)}',
            'success': False
        }), 500


@app.route('/api/currencies', methods=['GET'])
def get_supported_currencies():
    """Получение списка поддерживаемых валют"""
    currencies = list(exchange_service.CURRENCY_PAIRS.keys()) + ['RUB']
    return jsonify({
        'success': True,
        'currencies': sorted(currencies)
    }), 200


@app.errorhandler(400)
def bad_request(error):
    """Обработка ошибок 400, включая попытки HTTPS на HTTP порт"""
    error_description = str(error)
    
    # Проверяем, не является ли это попыткой HTTPS подключения
    if 'Bad request version' in error_description or 'request version' in error_description.lower():
        logger.warning("Обнаружена попытка HTTPS подключения к HTTP серверу. Используйте http:// вместо https://")
        return jsonify({
            'error': 'Сервер работает только по HTTP. Используйте http://localhost:5000 вместо https://',
            'success': False,
            'hint': 'Убедитесь, что вы используете http:// (не https://) в адресной строке'
        }), 400
    
    return jsonify({
        'error': f'Неверный запрос: {error_description}',
        'success': False
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Эндпоинт не найден',
        'success': False
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Внутренняя ошибка сервера',
        'success': False
    }), 500


@app.before_request
def log_request_info():
    """Логирование информации о запросе для отладки"""
    # Логируем только первые несколько байт для безопасности
    if request.method == 'GET' and len(request.data) > 0:
        # Проверяем, не является ли это SSL handshake
        if len(request.data) > 0 and request.data[0:1] == b'\x16':
            logger.warning("Обнаружен SSL/TLS handshake на HTTP порту. Клиент пытается использовать HTTPS.")
            logger.warning("Используйте http://localhost:5000 (не https://)")


@app.teardown_appcontext
def close_process_pool(error):
    """Закрывает пул процессов при завершении приложения"""
    global _process_pool
    if _process_pool is not None:
        _process_pool.close()
        _process_pool.join()
        _process_pool = None


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Запуск приложения Currency Converter API")
    logger.info("=" * 60)
    logger.info(f"Доступно процессоров: {cpu_count()}")
    logger.info("")
    logger.info("ВАЖНО: Приложение работает только по HTTP (не HTTPS)")
    logger.info("Используйте следующий адрес для доступа:")
    logger.info("  http://localhost:5000")
    logger.info("")
    logger.info("НЕ используйте https:// - это вызовет ошибку 400")
    logger.info("=" * 60)
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        # Закрываем пул процессов при завершении
        if _process_pool is not None:
            _process_pool.close()
            _process_pool.join()

