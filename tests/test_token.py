import requests
import allure
from utils.helpers import random_email
from utils.constants import BASE_URL, TEST_PASSWORD, TEST_NAME

@allure.epic("Authentication")
class TestAuthToken:

    @allure.title("Обновление accessToken с помощью refreshToken")
    def test_refresh_token(self):
        with allure.step("Регистрируем нового пользователя"):
            email = random_email()
            reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
            reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
            reg_json = reg_resp.json()
            refresh_token = reg_json["refreshToken"]

        with allure.step("Обновляем accessToken"):
            response = requests.post(f"{BASE_URL}/auth/token", json={"token": refresh_token})
            data = response.json()

        with allure.step("Проверяем успешное обновление токена"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "accessToken" in data

    @allure.title("Выход пользователя с использованием refreshToken")
    def test_logout(self):
        with allure.step("Регистрируем пользователя и получаем refreshToken"):
            email = random_email()
            reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
            reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
            reg_json = reg_resp.json()
            refresh_token = reg_json["refreshToken"]

        with allure.step("Отправляем  logout"):
            response = requests.post(f"{BASE_URL}/auth/logout", json={"token": refresh_token})
            data = response.json()


        with allure.step("Проверяем успешный logout"):
            assert response.status_code == 200
            assert data["success"] is True
