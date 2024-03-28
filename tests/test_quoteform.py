import pytest

@pytest.mark.parametrize("gallons, date, price, total", [
    ('50', '2024-06-03', '120.5', '6025.0'),    # Test case 1: 50 gallons, specific date
    ('', '2024-06-03', '', ''),                 # Test case 2: No gallons, specific date
    ('50', '', '', '',),                        # Test case 3: 50 gallons, no date
    ('', '', '', '',)                           # Test case 4: Neither gallons nor date
])
def test_quoteform_validate_input(client, gallons, date, price, total):
    assert client.get('/quoteform').status_code == 200
    response = client.post(
        '/quoteform', data={'gallons': gallons, 'date': date, 'price': price, 'total': total}
    )
    data = response.data.decode('utf-8')
    assert gallons in data
    assert date in data
    assert price in data
    assert total in data