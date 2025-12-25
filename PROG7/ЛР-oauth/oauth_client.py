from requests_oauthlib import OAuth2Session
import os

# Разрешаем HTTP для localhost (только для разработки!)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Получение credentials из переменных окружения
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
SCOPE = ["read:user"]  # выберите необходимые scopes

# Проверка наличия credentials
if not CLIENT_ID or not CLIENT_SECRET:
    print("Ошибка: CLIENT_ID и CLIENT_SECRET должны быть установлены в переменных окружения.")
    print("Для Windows PowerShell используйте:")
    print('  $env:CLIENT_ID="your_client_id"')
    print('  $env:CLIENT_SECRET="your_client_secret"')
    exit(1)

# Создание OAuth сессии и формирование URL авторизации
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
print("Перейдите по ссылке для авторизации:", authorization_url)
print("\nПосле авторизации скопируйте полный URL из адресной строки браузера.")

# Ввод URL перенаправления
redirect_response = input("\nВставьте полный URL перенаправления: ")

# Обмен авторизационного кода на access token
token = oauth.fetch_token(
    TOKEN_URL,
    authorization_response=redirect_response,
    client_secret=CLIENT_SECRET
)
print("\nТокен получен:", token)

# Использование токена для запроса защищённого ресурса
print("\nЗапрос информации о пользователе...")
r = oauth.get("https://api.github.com/user")
print("Ваши данные:", r.json())
