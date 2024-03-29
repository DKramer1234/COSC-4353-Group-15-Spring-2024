import pytest

# Assuming I have configured your Flask application and test client
# If not, you'll need to set up your Flask application and test client accordingly

def test_history(client):
    # Sending a GET request to the /history endpoint
    response = client.get('/history')
    
    # Checking if the status code of the response is 200
    assert response.status_code == 200
