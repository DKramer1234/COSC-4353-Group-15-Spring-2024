import pytest
from website import create_app, db 

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    def login(self, username='test', password='test'):
        return self._client.post(
            '/', data={'username': username, 'password': password})
    def logout(self):
        return self._client.get('/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()