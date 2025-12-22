"""
Сервис аналитики валют
Предоставляет графики изменения курса валют
"""
import base64
import io
import logging
from typing import Optional, Dict
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')  # Используем backend без GUI
import matplotlib.pyplot as plt
from exchange_rate_service import ExchangeRateService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalyticsService:
    """Сервис для аналитики и визуализации курсов валют"""
    
    def __init__(self):
        self.rate_service = ExchangeRateService()
    
    def generate_chart(self, currency: str, days: int = 30) -> Optional[Dict]:
        """
        Генерирует график изменения курса валюты
        
        Args:
            currency: Валюта для анализа
            days: Количество дней для анализа
        
        Returns:
            Словарь с base64-encoded изображением графика или None при ошибке
        """
        try:
            historical_data = self.rate_service.get_historical_rates(currency, days)
            
            if historical_data is None:
                return {
                    'error': f'Не удалось получить исторические данные для {currency}',
                    'success': False
                }
            
            dates = historical_data['dates']
            rates = historical_data['rates']
            
            if not dates or not rates:
                return {
                    'error': 'Нет данных для построения графика',
                    'success': False
                }
            
            # Создаем график
            plt.figure(figsize=(12, 6))
            plt.plot(dates, rates, linewidth=2, marker='o', markersize=3)
            plt.title(f'Курс {currency.upper()} за последние {days} дней', fontsize=16, fontweight='bold')
            plt.xlabel('Дата', fontsize=12)
            plt.ylabel(f'Курс {currency.upper()} (RUB)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Конвертируем график в base64
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
            plt.close()
            
            # Вычисляем статистику
            if rates:
                min_rate = min(rates)
                max_rate = max(rates)
                avg_rate = sum(rates) / len(rates)
                current_rate = rates[-1]
                change = current_rate - rates[0] if len(rates) > 1 else 0
                change_percent = (change / rates[0] * 100) if rates[0] != 0 else 0
            else:
                min_rate = max_rate = avg_rate = current_rate = change = change_percent = 0
            
            return {
                'success': True,
                'currency': currency.upper(),
                'period_days': days,
                'chart_image': img_base64,
                'statistics': {
                    'current_rate': round(current_rate, 4),
                    'min_rate': round(min_rate, 4),
                    'max_rate': round(max_rate, 4),
                    'avg_rate': round(avg_rate, 4),
                    'change': round(change, 4),
                    'change_percent': round(change_percent, 2)
                },
                'data_points': len(rates)
            }
            
        except Exception as e:
            logger.error(f"Ошибка при генерации графика: {str(e)}")
            plt.close()
            return {
                'error': f'Ошибка при генерации графика: {str(e)}',
                'success': False
            }
    
    def get_statistics(self, currency: str, days: int = 30) -> Optional[Dict]:
        """
        Получает статистику по валюте без генерации графика
        
        Args:
            currency: Валюта для анализа
            days: Количество дней для анализа
        
        Returns:
            Словарь со статистикой или None при ошибке
        """
        try:
            historical_data = self.rate_service.get_historical_rates(currency, days)
            
            if historical_data is None:
                return {
                    'error': f'Не удалось получить исторические данные для {currency}',
                    'success': False
                }
            
            rates = historical_data['rates']
            
            if not rates:
                return {
                    'error': 'Нет данных для анализа',
                    'success': False
                }
            
            min_rate = min(rates)
            max_rate = max(rates)
            avg_rate = sum(rates) / len(rates)
            current_rate = rates[-1]
            change = current_rate - rates[0] if len(rates) > 1 else 0
            change_percent = (change / rates[0] * 100) if rates[0] != 0 else 0
            
            return {
                'success': True,
                'currency': currency.upper(),
                'period_days': days,
                'statistics': {
                    'current_rate': round(current_rate, 4),
                    'min_rate': round(min_rate, 4),
                    'max_rate': round(max_rate, 4),
                    'avg_rate': round(avg_rate, 4),
                    'change': round(change, 4),
                    'change_percent': round(change_percent, 2)
                },
                'data_points': len(rates)
            }
            
        except Exception as e:
            logger.error(f"Ошибка при получении статистики: {str(e)}")
            return {
                'error': f'Ошибка при получении статистики: {str(e)}',
                'success': False
            }

