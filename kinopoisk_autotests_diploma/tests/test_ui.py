import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from config import Config

# Фикстура для инициализации и закрытия WebDriver
@pytest.fixture(scope="function")
def driver():
    """Фикстура, которая настраивает и закрывает браузер для каждого теста."""
    service = Service(Config.CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def perform_search(driver):
    """Фикстура, которая выполняет поиск 'Гарри Поттер' и возвращает WebDriver."""
    driver.get(Config.BASE_URL)
    search_bar = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, "kp_query"))
    )
    search_bar.send_keys("Гарри Поттер")
    search_bar.submit()
    return driver

@allure.suite("UI Tests")
@pytest.mark.ui
class TestUI:

    @allure.title("Проверка 1: Успешная авторизация с корректными данными")
    @allure.description("Тест проверяет, что пользователь может войти в систему с верным логином и паролем.")
    def test_successful_login(self, driver):
        """Проверка успешной авторизации пользователя."""
        driver.get(Config.BASE_URL)

        login_main_page_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Войти')]")))
        login_main_page_button.click()

        another_method_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Войти другим способом')]"))
        )
        another_method_button.click()

        mail_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Почта')]"))
        )
        mail_button.click()

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "passp-field-login"))
        )
        email_input.send_keys(Config.USER_EMAIL)
        
        login_form_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "passp:sign-in"))
        )
        login_form_button.click()

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "passp-field-passwd"))
        )
        password_input.send_keys(Config.USER_PASSWORD)
        
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "passp:sign-in"))
        )
        continue_button.click()
        
        profile_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-tid='15bd9013']"))
        )
        assert profile_element.is_displayed(), "Аватар профиля не найден, вход не выполнен."


    @allure.title("Проверка 2: Строка поиска доступна на главной странице")
    @allure.description("Тест проверяет, что поле поиска отображается на главной странице и активно.")
    def test_search_bar_is_available(self, driver):
        """Проверка наличия и доступности строки поиска."""
        driver.get(Config.BASE_URL)

        search_bar = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )

        assert search_bar.is_displayed(), "Строка поиска не отображается."
        assert search_bar.is_enabled(), "Строка поиска неактивна."


    @allure.title("Проверка 3: Поиск по полному названию фильма")
    @allure.description("Тест проверяет, что поиск по полному названию 'Гарри Поттер' возвращает релевантный результат.")
    def test_search_by_full_movie_name(self, perform_search):
        """Проверка поиска по полному названию фильма."""
        driver = perform_search
        
        movie_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".element.most_wanted"))
        )

        assert movie_result.is_displayed(), "Результат поиска по фильму 'Гарри Поттер' не найден."


    @allure.title("Проверка 4: Открытие страницы фильма по клику")
    @allure.description("Тест проверяет, что клик по постеру в результатах поиска открывает страницу фильма.")
    def test_open_movie_page_from_search(self, perform_search):
        """Проверка перехода на страницу фильма из результатов поиска."""
        driver = perform_search

        first_movie_link = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".element.most_wanted p.pic a"))
        )
        first_movie_link.click()
        
        movie_title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-tid='f22e0093']"))
    )
        assert movie_title_element.is_displayed(), "Заголовок фильма не найден, переход не выполнен."


    @allure.title("Проверка 5: На странице фильма отображается рейтинг")
    @allure.description("Тест проверяет, что на странице фильма есть рейтинг.")
    def test_movie_page_has_rating(self, driver):
        """Проверка наличия рейтинга на странице фильма."""
        driver.get(f"{Config.BASE_URL}film/689") 

        rating_element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-tid='939058a8']"))
        )

        assert rating_element.is_displayed(), "Рейтинг фильма не отображается на странице."

