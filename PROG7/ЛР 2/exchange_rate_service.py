"""
Сервис курсов валют
Получает актуальные курсы валют из открытых источников
"""
import yfinance as yf
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging
import ssl
import urllib3

# Отключаем предупреждения о небезопасных запросах (для разработки)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка SSL контекста для более гибкой работы
# ВНИМАНИЕ: Это отключает проверку SSL сертификатов для разработки
# В production следует использовать правильные сертификаты
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    # Для старых версий Python
    pass


class ExchangeRateService:
    """Сервис для получения курсов валют"""
    
    # Словарь соответствия валют для yfinance
    CURRENCY_PAIRS = {
        'USD': 'USDRUB=X',
        'EUR': 'EURRUB=X',
        'GBP': 'GBPRUB=X',
        'JPY': 'JPYRUB=X',
        'CNY': 'CNYRUB=X',
        'BTC': 'BTC-RUB',
        'ETH': 'ETH-RUB',
    }
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 минут
    
    def get_rate_from_yfinance(self, currency: str) -> Optional[float]:
        """Получает курс валюты через yfinance"""
        try:
            if currency == 'RUB':
                return 1.0
            
            ticker = self.CURRENCY_PAIRS.get(currency.upper())
            if not ticker:
                logger.warning(f"Валюта {currency} не поддерживается")
                return None
            
            # Проверяем кеш
            cache_key = f"{currency}_{datetime.now().strftime('%Y%m%d%H%M')}"
            if cache_key in self.cache:
                cached_data = self.cache[cache_key]
                if datetime.now() - cached_data['timestamp'] < timedelta(seconds=self.cache_timeout):
                    return cached_data['rate']
            
            # Получаем данные с обработкой ошибок
            try:
                ticker_obj = yf.Ticker(ticker)
                # Используем более длительный период для надежности
                data = ticker_obj.history(period="5d", interval="1d")
                
                if data.empty:
                    # Пробуем получить данные за больший период
                    data = ticker_obj.history(period="1mo")
                
                if not data.empty:
                    rate = float(data['Close'].iloc[-1])
                    self.cache[cache_key] = {
                        'rate': rate,
                        'timestamp': datetime.now()
                    }
                    return rate
                else:
                    logger.warning(f"Пустые данные для {currency}, пробуем альтернативный метод")
                    # Пробуем альтернативный метод
                    return self.get_rate_from_ecb(currency)
                    
            except Exception as yf_error:
                logger.warning(f"Ошибка yfinance для {currency}: {str(yf_error)}, пробуем альтернативный метод")
                # Пробуем альтернативный метод
                return self.get_rate_from_ecb(currency)
            
        except Exception as e:
            logger.error(f"Ошибка при получении курса {currency}: {str(e)}")
            # В крайнем случае пробуем альтернативный метод
            return self.get_rate_from_ecb(currency)
    
    def get_rate_from_ecb(self, currency: str) -> Optional[float]:
        """Получает курс валюты через API Европейского центрального банка"""
        try:
            if currency == 'RUB':
                return 1.0
            
            # Используем альтернативный API для получения курсов
            # exchangerate-api.com - бесплатный API без ключа
            url = "https://api.exchangerate-api.com/v4/latest/EUR"
            
            # Настройка сессии с обработкой SSL
            session = requests.Session()
            session.verify = False  # Отключаем проверку SSL для совместимости
            
            response = session.get(url, timeout=10, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                
                if currency.upper() == 'EUR':
                    return 1.0
                
                # Конвертируем через EUR
                eur_to_currency = rates.get(currency.upper())
                eur_to_rub = rates.get('RUB')
                
                if eur_to_currency and eur_to_rub:
                    return eur_to_rub / eur_to_currency
            
            return None
            
        except requests.exceptions.SSLError as e:
            logger.warning(f"SSL ошибка при получении курса через ECB для {currency}: {str(e)}")
            # Пробуем альтернативный метод
            return self._get_rate_alternative(currency)
        except Exception as e:
            logger.error(f"Ошибка при получении курса через ECB для {currency}: {str(e)}")
            return None
    
    def _get_rate_alternative(self, currency: str) -> Optional[float]:
        """Альтернативный метод получения курса через другой API"""
        try:
            # Используем fixer.io или другой бесплатный API
            # Для простоты используем статические курсы как fallback
            fallback_rates = {
                'USD': 90.0,  # Примерный курс (должен быть обновлен)
                'EUR': 98.0,
                'GBP': 114.0,
                'JPY': 0.6,
                'CNY': 12.5,
            }
            
            rate = fallback_rates.get(currency.upper())
            if rate:
                logger.info(f"Использован fallback курс для {currency}: {rate}")
                return rate
            
            return None
        except Exception as e:
            logger.error(f"Ошибка в альтернативном методе для {currency}: {str(e)}")
            return None
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Получает курс обмена между двумя валютами"""
        try:
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            
            if from_currency == to_currency:
                return 1.0
            
            # Получаем курсы относительно RUB
            from_rate = self.get_rate_from_yfinance(from_currency)
            to_rate = self.get_rate_from_yfinance(to_currency)
            
            # Если не удалось получить через yfinance, пробуем альтернативный метод
            if from_rate is None:
                from_rate = self.get_rate_from_ecb(from_currency)
            if to_rate is None:
                to_rate = self.get_rate_from_ecb(to_currency)
            
            if from_rate is None or to_rate is None:
                logger.error(f"Не удалось получить курсы для {from_currency} или {to_currency}")
                return None
            
            # Конвертируем from_currency -> RUB -> to_currency
            exchange_rate = to_rate / from_rate
            return exchange_rate
            
        except Exception as e:
            logger.error(f"Ошибка при расчете курса {from_currency}/{to_currency}: {str(e)}")
            return None
    
    def get_historical_rates(self, currency: str, days: int = 30) -> Optional[Dict]:
        """Получает исторические данные курса валюты"""
        try:
            if currency == 'RUB':
                return {'dates': [], 'rates': []}
            
            ticker = self.CURRENCY_PAIRS.get(currency.upper())
            if not ticker:
                return None
            
            try:
                ticker_obj = yf.Ticker(ticker)
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                
                # Пробуем получить данные с разными параметрами
                data = ticker_obj.history(start=start_date, end=end_date)
                
                if data.empty:
                    # Пробуем получить данные за больший период
                    data = ticker_obj.history(period=f"{min(days, 60)}d")
                
                if data.empty:
                    logger.warning(f"Не удалось получить исторические данные для {currency}")
                    return None
                
                dates = [date.strftime('%Y-%m-%d') for date in data.index]
                rates = [float(rate) for rate in data['Close'].values]
                
                return {
                    'dates': dates,
                    'rates': rates,
                    'currency': currency.upper()
                }
            except Exception as yf_error:
                logger.warning(f"Ошибка yfinance при получении исторических данных для {currency}: {str(yf_error)}")
                # Возвращаем пустые данные вместо None для совместимости
                return {
                    'dates': [],
                    'rates': [],
                    'currency': currency.upper()
                }
            
        except Exception as e:
            logger.error(f"Ошибка при получении исторических данных для {currency}: {str(e)}")
            return None

