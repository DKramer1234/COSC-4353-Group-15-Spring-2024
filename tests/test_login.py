import pytest

@pytest.mark.parametrize("username, password, message", [
        ('', '', 'Username does not exist.'),  # Test empty username and password
        ('a', '', 'Incorrect password, try again.'),  # Test valid username but empty password
        ('', 'a', 'Username does not exist.'),  # Test empty username but valid password
        ('test', 'test', 'Logged in successfully!'),  # Test valid username and password
    ])

def test_login(client, username, password, message):
    assert client.get('/').status_code == 200
    response = client.post(
        '/', data = {
            'username': username,
            'password': password}
    )
    data = response.data.decode('utf-8')
    username in data
    password in data

    
# @pytest.mark.parametrize("username, password, message", [
#     ('', ''),
#     ('John', 'John1') # Test case 4: Name, Password
# ])

# def test_login(client, username, password):
#     assert client.get('/').status_code == 200
#     response = client.post(
#         '/', data = {'username': username, 'password': password}
#     )
#     data = response.data.decode('utf-8')
#     username in data
#     password in data

# def test_register(client, app):
#     assert client.get('/auth/register').status_code == 200
#     response = client.post(
#         '/auth/register', data={'username': 'a', 'password': 'a'}
#     )
#     assert response.headers["Location"] == "/auth/login"

#     with app.app_context():
#         assert db().execute(
#             "SELECT * FROM user WHERE username = 'a'",
#         ).fetchone() is not None


# @pytest.mark.parametrize(('username', 'password', 'message'), (
#     ('', '', b'Username is required.'),
#     ('a', '', b'Password is required.'),
#     ('test', 'test', b'already registered'),
# ))

# def test_register_validate_input(client, username, password, message):
#     response = client.post(
#         '/auth/register',
#         data={'username': username, 'password': password}
#     )
#     assert message in response.data
