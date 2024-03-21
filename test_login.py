import pytest
from flask import Flask, session
from website.auth import auth, login
from website.models import User

# Create a test Flask application
@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['TESTING'] = True
    app.register_blueprint(auth)

    return app

# Test login with valid credentials
def test_login_valid_credentials(client):
    # Create a test user
    test_user = User(username='test_user', password='test_password')
    # Save the user to the database
    test_user.save()

    # Send a POST request with valid credentials
    response = client.post('/login', data={'username': 'test_user', 'password': 'test_password'}, follow_redirects=True)

    # Check if the user is logged in
    assert 'user_id' in session
    assert session['user_id'] == test_user.id
    # Check if the flash message is displayed
    assert b'Logged in successfully!' in response.data

# Test login with invalid credentials
def test_login_invalid_credentials(client):
    # Send a POST request with invalid credentials
    response = client.post('/login', data={'username': 'invalid_user', 'password': 'invalid_password'}, follow_redirects=True)

    # Check if the user is not logged in
    assert 'user_id' not in session
    # Check if the flash message is displayed
    assert b'Incorrect password, try again.' in response.data

# Test login with missing credentials
def test_login_missing_credentials(client):
    # Send a POST request with missing credentials
    response = client.post('/login', follow_redirects=True)

    # Check if the user is not logged in
    assert 'user_id' not in session
    # Check if the flash message is displayed
    assert b'Username does not exist.' in response.data
