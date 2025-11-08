import requests
from utils.constants import BASE_URL, TEST_PASSWORD, TEST_EMAIL, TEST_NAME
from utils.helpers import random_email


def test_create_order_authorized():
    email = random_email()
    reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
    reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data).json()

    token = reg_resp["accessToken"]
    headers = {"Authorization": token}

    payload = {"ingredients": ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]}

    response = requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)
    data = response.json()

    assert response.status_code ==200
    assert data["success"] is True
    assert "order" in data
    assert "number" in data["order"]

def test_create_order_unauthorized():
    response = requests.post(f"{BASE_URL}/orders",
                             json={"ingredients": ["60d3b41abdacab0026a733c6"]})
    assert response.status_code == 401

def test_create_order_no_ingredients():
    email = random_email()
    reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
    reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data).json()

    token = reg_resp["accessToken"]
    headers = {"Authorization": token}

    response = requests.post(f"{BASE_URL}/orders", json={"ingredients": []}, headers=headers)
    data = response.json()

    assert response.status_code == 400
    assert data["success"] is False
    assert "Ingredient ids must be provided" in data["message"]

def test_create_order_invalid_ingredient():
    email = random_email()
    reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
    reg_reps = requests.post(f"{BASE_URL}/auth/register", json=reg_data).json()

    token = reg_reps["accessToken"]
    headers = {"Authorization": token}
    response = requests.post(
        f"{BASE_URL}/orders", json={"ingredients": ["invalid_id"]}, headers=headers
    )
    assert response.status_code == 500

