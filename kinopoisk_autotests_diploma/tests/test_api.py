import requests
from urllib.parse import urljoin
import pytest
import allure
from config import Config


@allure.suite("API Tests")
@pytest.mark.api
class TestAPI:

    @allure.title("API 1: Проверка доступности сервиса")
    @allure.description(
        "Тест проверяет, что базовый эндпоинт API отвечает со статусом 200 OK."
    )
    def test_api_is_up(self):
        url = Config.API_BASE_URL
        response = requests.get(url, headers=Config.API_HEADERS, timeout=10)
        assert response.status_code == 200, \
            f"API не отвечает, получен статус: {response.status_code}"

    @allure.title("API 2: Поиск фильма по названию 'Гарри Поттер'")
    @allure.description(
        "Тест проверяет, что поиск фильма 'Гарри Поттер' "
        "возвращает ожидаемый результат в формате JSON."
    )
    def test_search_movie_harry_potter(self):
        search_url = urljoin(Config.API_BASE_URL, "v1.4/movie/search")
        params = {"query": "Гарри Поттер"}
        response = requests.get(
            search_url, headers=Config.API_HEADERS, params=params, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "docs" in data, "В ответе API нет ключа 'docs'"
        assert len(data['docs']) > 0, \
            "Поиск не вернул результатов для 'Гарри Поттер'"
        first_movie = data['docs'][0]
        assert "Гарри Поттер" in first_movie['name'], \
            "Название фильма в результатах не соответствует запросу"

    @allure.title("API 3: Получение деталей фильма по ID")
    @allure.description(
        "Тест проверяет, что можно получить детали конкретного фильма "
        "по его ID."
    )
    def test_get_movie_details_by_id(self):
        search_url = urljoin(Config.API_BASE_URL, "v1.4/movie/search")
        params = {"query": "Гарри Поттер"}
        response = requests.get(
            search_url, headers=Config.API_HEADERS, params=params, timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data['docs']) > 0, \
            "Поиск не вернул результатов для 'Гарри Поттер'"
        movie_id = data['docs'][0]['id']
        url = urljoin(Config.API_BASE_URL, f"v1.4/movie/{movie_id}")
        response = requests.get(url, headers=Config.API_HEADERS, timeout=20)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == movie_id, "Получен неверный ID фильма"
        assert "Гарри Поттер" in data['name'], \
            "Получено неверное название фильма"

    @allure.title("API 4: Проверка обработки невалидного API токена")
    @allure.description(
        "Тест проверяет, что API возвращает ошибку 401/403 "
        "при использовании неверного токена."
    )
    def test_invalid_auth_token(self):
        search_url = urljoin(Config.API_BASE_URL, "v1.4/movie/search")
        invalid_headers = {
            "X-API-KEY": "some-invalid-token-12345",
            "accept": "application/json"
        }
        params = {"query": "тест"}
        response = requests.get(
            search_url, headers=invalid_headers, params=params, timeout=10
        )
        assert response.status_code in [401, 403], \
            f"Ожидался статус 401/403, получен {response.status_code}"

    @allure.title("API 5: Проверка обработки несуществующего эндпоинта")
    @allure.description(
        "Тест проверяет, что при обращении к несуществующему URL "
        "API возвращается статус 404."
    )
    def test_non_existent_endpoint(self):
        url = urljoin(Config.API_BASE_URL, "v1.4/some/nonexistent/path/12345")
        response = requests.get(url, headers=Config.API_HEADERS, timeout=10)
        assert response.status_code == 404, \
            f"Ожидался статус 404, получен {response.status_code}"
