import requests
import pytest

BASE_URL = 'http://localhost:8000'

def test_register_user_success():
    payload = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    }
    response = requests.post(f'https://steph001.pythonanywhere.com/auth/register/', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['status'] == 'success'
    assert data['message'] == 'Registration successful'
    assert 'accessToken' in data['data']
    assert data['data']['user']['firstName'] == 'John'
    assert data['data']['user']['lastName'] == 'Doe'
    assert data['data']['user']['email'] == 'john.doe@example.com'
    assert data['data']['user']['phone'] == '09039672814'

def test_login_user_success():
    payload = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = requests.post(f'{BASE_URL}/auth/login/', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert data['message'] == 'Login successful'
    assert 'accessToken' in data['data']

def test_register_user_missing_fields():
    payload = {
        "firstName": "John",
        "lastName": "Doe"
    }
    response = requests.post(f'{BASE_URL}/auth/register/', json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['status'] == 'Bad request'
    assert 'errors' in data

# More test cases...
