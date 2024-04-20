def test_history_unauthenticated(client):
    #Test accessing the history page when not logged in
    client.get('/')
    assert client.get('/history', follow_redirects=True).status_code == 302

def test_history_authenticated(client):
    # Test accessing the history page when logged in
    client.get('/', data={'username': 'test', 'password': 'test'})
    assert client.get('/history', follow_redirects=True).status_code == 200
    response = client.get('/history')
    #assert response.status_code == 200  # Should return a success status code
    assert b'Fuel Quote History' in response.data  # Check if the page contains expected content
    client.get('/logout')
