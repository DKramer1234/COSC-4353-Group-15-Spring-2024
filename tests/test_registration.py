import pytest

@pytest.mark.parametrize("username, password1, password2", [
    ('', '', ''),
    ('a', '', ''),
    ('', 'a', ''),
    ('test', 'test', 'test')
])

def test_login(client, username, password1, password2):
    assert client.get('/client_registration').status_code == 200
    response = client.post(
        '/', data = {'username': username, 'password1': password1, 'password2': password2}
    )
    data = response.data.decode('utf-8')
    username in data
    password1 in data
    password2 in data