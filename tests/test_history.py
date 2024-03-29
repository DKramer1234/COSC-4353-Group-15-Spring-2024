import pytest

def test_history(client):
    assert client.get('/history').status_code == 200