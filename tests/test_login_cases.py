import pytest

@pytest.mark.parametrize("username, password, message", [
        ('', '', 'Username does not exist.'),  # Test empty username and password
        ('a', 'b', 'Incorrect password, try again.'),  # Test valid username but empty password
        ('', 'a', 'Username does not exist.'),  # Test empty username but valid password
        ('test', 'test', 'Logged in successfully!'),  # Test valid username and password
    ])

def test_login_cases(client, username, password, message):
    assert client.get('/').status_code == 200
    response = client.post(
        '/', data = {
            'username': username,
            'password': password,
            'message': message}
    )
    data = response.data.decode('utf-8')
    username in data
    password in data
    message in data