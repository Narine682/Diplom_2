import requests
from utils.helpers import random_email
from utils.constants import BASE_URL, TEST_PASSWORD, TEST_NAME

def test_refresh_token():
    email = random_email()
    reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
    reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data).json()

    refresh_token = reg_resp["refreshToken"]

    response = requests.post(f"{BASE_URL}/auth/token", json={"token": refresh_token})
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert "accessToken" in data

def test_logout():
    email = random_email()
    reg_data = {"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
    reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data).json()

    refresh_token = reg_resp["refreshToken"]

    response = requests.post(f"{BASE_URL}/auth/logout", json={"token": refresh_token})
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
