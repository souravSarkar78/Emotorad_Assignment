import pytest
import requests

@pytest.fixture
def api_url():
    return 'http://127.0.0.1:5000/identify'

def test_multiple_requests(api_url):
    # Test Case 1
    payload = {
                "email": "my_email1@gmail.com",
                "phoneNumber": "9876543210"
            }
    response = requests.post(api_url, json=payload)
    assert response.status_code == 200

    # Test Case 2
    payload = {
                "email": "my_email1@gmail.com",
                "phoneNumber": "9876543211"  # changed phone number
            }
    response = requests.post(api_url, json=payload)
    assert response.status_code == 200

    # Test Case 3
    payload = {
                "email": "my_email2@gmail.com",  # change email and phone both
                "phoneNumber": "9876543212"
            }
    response = requests.post(api_url, json=payload)
    assert response.status_code == 200

    # Test Case 4
    payload = {
                "email": "my_email1@gmail.com",  # overlap multiple contact info
                "phoneNumber": "9876543212"
            }
    response = requests.post(api_url, json=payload)
    assert response.status_code == 400

    # Test Case 5
    payload = {}
    response = requests.post(api_url, json=payload)
    assert response.status_code == 400