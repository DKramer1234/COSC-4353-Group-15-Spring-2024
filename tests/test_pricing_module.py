import pytest
from flask import json
from website.pricing_module import PricingModule

@pytest.mark.parametrize("gallons, address", [
    (500, "4300 Martin Luther King Blvd, Houston, TX 77204"),
    (2000, "1600 Pennsylvania Avenue NW, Washington, DC 20500")
])
def test_pricing_module(client, gallons, address):
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    date = '2024-08-03'
    client.post('/', data={'username': 'test', 'password': 'test'})
    assert client.get('/quoteform', follow_redirects=True).status_code == 200
    response = client.post(
        '/quoteform', data={'gallons': gallons, 'date': date, 'address': address}, headers=headers, follow_redirects=True
    )
    data = json.loads(response.data.decode('utf-8'))
    if gallons == 500 and "TX" in address:
        assert '157.9' in data
    if gallons == 2000 and "TX" not in address:
        assert '495' in data