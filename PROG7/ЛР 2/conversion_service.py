"""
Сервис конвертации валют
Конвертирует суммы из одной валюты в другую
"""
import logging
from typing import Optional, Dict
from exchange_rate_service import ExchangeRateService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConversionService:
    """Сервис для конвертации валют"""
    
    def __init__(self):
        self.rate_service = ExchangeRateService()
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> Optional[Dict]:
        """
        Конвертирует сумму из одной валюты в другую
        
        Args:
            amount: Сумма для конвертации
            from_currency: Исходная валюта
            to_currency: Целевая валюта
        
        Returns:
            Словарь с результатами конвертации или None при ошибке
        """
        try:
            if amount < 0:
                return {
                    'error': 'Сумма не может быть отрицательной',
                    'success': False
                }
            
            exchange_rate = self.rate_service.get_exchange_rate(from_currency, to_currency)
            
            if exchange_rate is None:
                return {
                    'error': f'Не удалось получить курс обмена {from_currency}/{to_currency}',
                    'success': False
                }
            
            converted_amount = amount * exchange_rate
            
            return {
                'success': True,
                'amount': amount,
                'from_currency': from_currency.upper(),
                'to_currency': to_currency.upper(),
                'exchange_rate': round(exchange_rate, 6),
                'converted_amount': round(converted_amount, 2)
            }
            
        except Exception as e:
            logger.error(f"Ошибка при конвертации: {str(e)}")
            return {
                'error': f'Ошибка при конвертации: {str(e)}',
                'success': False
            }
    
    def batch_convert(self, conversions: list) -> list:
        """
        Выполняет множественную конвертацию
        
        Args:
            conversions: Список словарей с параметрами конвертации
                [{'amount': 100, 'from': 'USD', 'to': 'EUR'}, ...]
        
        Returns:
            Список результатов конвертации
        """
        results = []
        for conv in conversions:
            result = self.convert(
                conv.get('amount', 0),
                conv.get('from', 'USD'),
                conv.get('to', 'EUR')
            )
            results.append(result)
        return results

