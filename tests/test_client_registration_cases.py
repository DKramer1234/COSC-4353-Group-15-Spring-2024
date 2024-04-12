import pytest
from website.models import User

@pytest.mark.parametrize("username, password1, password2", [
    ("", "", ""),
    ("TestUsername", "", ""),
    ("", "TestPassword", ""),
    ("", "", "TestPassword"),
    ("", "TestPassword", "TestPassword"),
    ("TestUsername", "", "TestPassword"),
    ("TestUsername", "TestPassword", ""),
    ("TestUsername", "TestPassword", "TestPassword"),
    ("TestUsername", "TestPassword", "!TestPassword")])

def test_user_registration_cases(client, app, username, password1, password2):
    assert client.get('/client_registration').status_code == 200
    response = client.post('/client_registration',
        data = {'username': username,
                'password1': password1,
                'password2': password2})
    
    assert response.status_code == 200
    data = response.data.decode('utf-8')

    if len(username) < 4:
        assert "Username must be greater than 3 characters." in data
