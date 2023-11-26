import pytest
import requests

@pytest.fixture
def api_url():
    return 'http://127.0.0.1:4000'

def test_multiple_requests(api_url):
    # Test Case 1
    payload = {'email': "my_email@gmail.com"}
    response = requests.post(api_url, json=payload)
    assert response.status_code == 201

    # Test Case 2
    payload = {'email': 'my_email.com'}
    response = requests.post(api_url, json=payload)
    assert response.status_code == 400

    # Test Case 3
    payload = {}
    response = requests.post(api_url, json=payload)
    assert response.status_code == 400
    
    # Test Case 4
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20iLCJleHAiOjE3MDEwMDU2OTEuNDk0OTQ3N30.fQCPN0l0GhYNU1H1DU5DmuhNYEiIma-ptxuMQjR8PaQ'}
    response = requests.get(api_url, headers=headers)
    assert response.status_code == 200

    # Test Case 4
    headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20iLCJleHAiOjE3MDEwMDU2OTEuNDk0OTQ3N30.fQCPN0l0GhYNU1H1DU5DmuhNYEiIma-ptxuMQjR8PaQ'}
    response = requests.get(api_url, headers=headers)
    assert response.status_code == 401