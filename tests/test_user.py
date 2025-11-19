import requests
import allure
import random
import string
from utils.constants import BASE_URL, TEST_EMAIL, TEST_PASSWORD, TEST_NAME
from utils.helpers import random_email


@allure.epic("Authentication")
class TestAuth:
    @allure.title("Регистрация уникального пользователя")
    def test_create_unique_user(self):
        email = random_email()
        payload = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}

        with allure.step("Отправляем POST-запрос на /auth/register"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)
            data = response.json()

        with allure.step("Проверяем успешную регистрацию"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Регистрация уже существующего пользователя")
    def test_create_existing_user(self):
        payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD, "name": TEST_NAME}

        with allure.step("Пробуем зарегистрировать существующего пользователя"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)
            data = response.json()

        with allure.step("Проверяем ошибку 403 и сообщение"):
            assert response.status_code == 403
            assert data["success"] is False
            assert "User already exists" in data["message"]

    @allure.title("Авторизация с валидным пользователем")
    def test_login_valid_user(self):
        payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}

        with allure.step("Авторизуемся с валидными данными"):
            response = requests.post(f"{BASE_URL}/auth/login", json=payload)
            data = response.json()

        with allure.step("Проверяем успешный вход"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Авторизация с невалидным пользователем")
    def test_login_invalid_user(self):
        payload = {"email": "wrong@example.com", "password": "wrongpass"}

        with allure.step("Пробуем авторизоваться с неверными данными"):
            response = requests.post(f"{BASE_URL}/auth/login", json=payload)
            data = response.json()

        with allure.step("Проверяем ошибку 401"):
            assert response.status_code == 401
            assert data["success"] is False
            assert "incorrect" in data["message"]
