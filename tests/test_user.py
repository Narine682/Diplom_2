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
        """Проверяет, что можно зарегистрировать уникального пользователя"""
        email = random_email()
        payload = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}

        with allure.step("Отправляем POST-запрос на /auth/register"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)
            data = response.json()

        with allure.step("Проверяем, что регистрация успешна"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Регистрация уже существующего пользователя")
    def test_create_existing_user(self):
        """Проверяет, что регистрация с существующим email возвращает ошибку"""
        payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD, "name": TEST_NAME}

        with allure.step("Отправляем POST-запрос на /auth/register для существующего пользователя"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)
            data = response.json()

        with allure.step("Проверяем, что сервер возвращает 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert data["success"] is False
            assert "User already exists" in data["message"]

    @allure.title("Авторизация с валидным пользователем")
    def test_login_valid_user(self):
        """Проверяет успешный вход с существующим пользователем"""
        payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}

        with allure.step("Отправляем POST-запрос на /auth/login"):
            response = requests.post(f"{BASE_URL}/auth/login", json=payload)
            data = response.json()

        with allure.step("Проверяем успешный вход"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Авторизация с невалидным пользователем")
    def test_login_invalid_user(self):
        """Проверяет вход с неправильным email или паролем"""
        payload = {"email": "wrong@example.com", "password": "wrongpass"}

        with allure.step("Отправляем POST-запрос на /auth/login"):
            response = requests.post(f"{BASE_URL}/auth/login", json=payload)
            data = response.json()

        with allure.step("Проверяем, что сервер возвращает 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert data["success"] is False
            assert "incorrect" in data["message"]
