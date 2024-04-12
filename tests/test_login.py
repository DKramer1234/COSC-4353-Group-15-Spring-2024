import pytest
from website.models import User

def test_login_page(client):
    response = client.get("/")
    assert b"<title>Login</title>" in response.data

def test_verify_invalid_login(client):
    client.post("/login", data={'username': 'TestUsername', 'password': 'InvalidPassword'})
    response = client.get("/logout", follow_redirects = True)
    assert b"Login" in response.data
    assert response.status_code == 200

def test_user_registration(client, app):
    response = client.post("/client_registration", data = {'username': 'TestUsername', 'password1': 'TestPassword', 'password2': 'TestPassword'})
    
    with app.app_context():
        assert User.query.first().username == "TestUsername"
        assert User.query.first().check_password("TestPassword")

def test_client_registration_page(client):
    response = client.get("/client_registration")
    assert b"<title>Client Registration</title>" in response.data
    assert response.status_code == 200

def test_user_registration_case1(client, app):
    response = client.post("/client_registration", data = {'username': 'TestUsername', 'password1': 'TestPassword', 'password2': 'TestPassword'})

    with app.app_context():
        assert User.query.first().username == "TestUsername"
        assert User.query.first().check_password("TestPassword")