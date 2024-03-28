import pytest

@pytest.mark.parametrize("gallons, date", [
    ('50', '2024-06-03'),  # Test case 1: 50 gallons, specific date
    ('', '2024-06-03'),    # Test case 2: No gallons, specific date
    ('', '')               # Test case 3: Neither gallons nor date
])
def test_quoteform(client, gallons, date):
    assert client.get('/quoteform').status_code == 200
    response = client.post(
        '/quoteform', data={'gallons': gallons, 'date': date}
    )
    data = response.data.decode('utf-8')
    gallons in data
    date in data