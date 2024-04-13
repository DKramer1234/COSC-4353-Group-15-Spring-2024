
import pytest

def test_history_unauthenticated(client):
    #Test accessing the history page when not logged in
    response = client.get('/history')
    assert response.status_code == 302  # Should redirect to the login page

def test_history_authenticated(client):
    # Test accessing the history page when logged in
    response = client.get('/history')
    assert response.status_code == 200  # Should return a success status code
    assert b'Fuel Quote History' in response.data  # Check if the page contains expected content
