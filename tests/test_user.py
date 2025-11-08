import requests
import random
import string
from utils.constants import BASE_URL, TEST_EMAIL, TEST_PASSWORD, TEST_NAME
from utils.helpers import random_email



def test_create_unique_user():
    email = random_email()
    payload ={"email": email, "password": TEST_PASSWORD, "name": TEST_NAME}
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert "accessToken" in data
    assert "refreshToken" in data

def test_create_existing_user():
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": TEST_NAME
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    data = response.json()

    if response.status_code == 403:
        assert data["success"] is False
        assert "User already exists" in data["message"]
    else:
        assert data["success"] is True

def test_login_valid_user():
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert "accessToken" in data
    assert "refreshToken" in data

def test_login_invalid_user():
    payload = {"email": "wrong@example.com", "password": "wrongpass"}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    data = response.json()

    assert response.status_code == 401
    assert data["success"] is False
    assert "incorrect" in data["message"]
