class Config:
    # Основные настройки окружения
    BASE_URL = "https://www.kinopoisk.ru/"  # URL сайта
    API_BASE_URL = "https://api.kinopoisk.dev/"  # Замените на URL API
    
    # Данные пользователя
    USER_EMAIL = ""  # email
    USER_PASSWORD = ""  # Пароль
    # Токен для доступа к API
    AUTH_TOKEN = ""  # Токен API

    # Заголовки для API-запросов
    API_HEADERS = {
        "X-API-KEY": AUTH_TOKEN,
        "accept": "application/json"
    }

    # Путь к исполняемому файлу ChromeDriver.
    # Используется для автоматизации браузера через Selenium.
    # Значение None означает, что путь пока не определен.
    CHROME_DRIVER_PATH = None 

