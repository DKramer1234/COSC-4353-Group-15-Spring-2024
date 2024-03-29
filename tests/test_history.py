
import pytest
# Assuming I have configured your Flask application and test client
# If not, you'll need to set up your Flask application and test client accordingly

def test_history_unauthenticated(client):
    # Test accessing the history page when not logged in
    response = client.get('/history')
    assert response.status_code == 302  # Should redirect to the login page

def test_history_authenticated(authenticated_client):
    # Test accessing the history page when logged in
    response = authenticated_client.get('/history')
    assert response.status_code == 200  # Should return a success status code
    assert b'Fuel Quote History' in response.data  # Check if the page contains expected content
