import requests
import allure
from utils.constants import BASE_URL, TEST_PASSWORD, TEST_EMAIL, TEST_NAME
from utils.helpers import random_email

@allure.epic("Orders")
class TestOrders:

    @allure.title("Создание заказа авторизованным пользователем с валидными ингредиентами")
    def test_create_order_authorized(self):
        with allure.step("Регистрируем нового пользователя"):
            email = random_email()
            reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
            reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data).json()
            token = reg_resp["accessToken"]

        with allure.step("Получаем ингредиенты"):
            ingredients_resp = requests.get(f"{BASE_URL}/ingredients").json()
            ingredient_ids = [item["_id"] for item in ingredients_resp["data"]]

        with allure.step("Создаём заказ"):
            payload = {"ingredients": ingredient_ids[:2]}
            response = requests.post(f"{BASE_URL}/orders", json=payload, headers={"Authorization": token})
            data = response.json()

        with allure.step("Проверяем успешное создание заказа"):
             assert response.status_code ==200
             assert data["success"] is True
             assert "number"in data["order"]
    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self):
        with allure.step("Берём любой ингредиент"):
            ingredients_resp = requests.get(f"{BASE_URL}/ingredients").json()
            ingredient_ids = [item["_id"] for item in ingredients_resp["data"]]

        with allure.step("Отправляем заказ без авторизации"):
            response = requests.post(f"{BASE_URL}/orders", json={"ingredients": ingredient_ids[:2]})
            data = response.json()

        with allure.step("Проверяем, что заказ успешно создан"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "order" in data
            assert "number" in data["order"]

    @allure.title("Создание заказа без списка ингредиентов")
    def test_create_order_no_ingredients(self):
        with allure.step("Регистрируем нового пользователя"):
            email = random_email()
            reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
            reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data).json()
            token = reg_resp["accessToken"]

        with allure.step("Отправляем заказ с пустым списком ингредиентов"):
            response = requests.post(f"{BASE_URL}/orders", json={"ingredients":[]}, headers={"Authorization": token})
            data = response.json()

        with allure.step("Проверяем ошибку 400"):
            assert response.status_code == 400
            assert data["success"] is False
            assert "Ingredient ids must be provided" in data["message"]

    @allure.title("Создание заказа с несуществующим ID ингредиента")
    def test_create_order_invalid_ingredient(self):
        with allure.step("Регистрируем нового пользователя"):
            email = random_email()
            reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
            reg_reps = requests.post(f"{BASE_URL}/auth/register", json=reg_data).json()
            token = reg_reps["accessToken"]

        with allure.step("Отправляем заказ с неверным ID"):
            response = requests.post(
                f"{BASE_URL}/orders", json={"ingredients": ["invalid_id_123"]},
                headers={"Authorization": token})

        with allure.step("Проверяем ошибку 500"):
            assert response.status_code == 500

