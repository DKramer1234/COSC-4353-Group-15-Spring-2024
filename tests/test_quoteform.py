import pytest
from website.models import User, Quote
from flask_login import current_user

@pytest.mark.parametrize("gallons, date, address, price, total", [
    ('50', '2024-06-03', "TestAddress, TestAddress2, TestCity, TX, 33333", '120.5', '6025.0'),         # Test case 1: Base case
    ('', '2024-06-03', "TestAddress, TestAddress2, TestCity, TX, 33333", '', ''),                      # Test case 2: No gallons
    ('50', '', "TestAddress, TestAddress2, TestCity, TX, 33333", '', ''),                              # Test case 3: No date
    ('', '', "TestAddress, TestAddress2, TestCity, TX, 33333", '', ''),                                # Test case 4: No gallons and date
    ('50', '2024-06-03', '', '', ''),                                                                  # Test case 5: No address
])
def test_quoteform_validate_input(client, gallons, date, address, price, total):
    client.post('/', data={'username': 'test', 'password': 'test'})
    assert client.get('/quoteform', follow_redirects=True).status_code == 200
    response = client.post(
        '/quoteform', data={'gallons': gallons, 'date': date, 'address': address, 'price': price, 'total': total}, follow_redirects=True
    )
    data = response.data.decode('utf-8')
    if gallons == '' and date == '':
        assert 'Enter an amount for fuel volume (gallons) and choose a delivery date' in data
    elif gallons == '':
        assert 'Enter an amount for fuel volume (gallons)' in data
    elif date == '':
        assert 'Choose a delivery date' in data
    elif len(address) == 0:
        assert 'Save your delivery address in Profile Management' in data
    elif price != '' and total != '':
        assert gallons in data
        assert date in data
        assert address in data
        assert price in data
        assert total in data
        assert float(gallons) * float(price) == float(total)
    client.get('/logout')

'''def test_address2_check(client):
    client.post('/', data={'username': 'test', 'password': 'test'})
    assert client.get('/profile_management', follow_redirects=True).status_code == 200
    response = client.post('/profile_management',
        data={"full_name": 'TestName', 'address1': 'TestAddress', 'city': 'TestCity', 'state': 'TestCity', 'zipcode': '33333'}, follow_redirects=True
    )
    assert client.get('/quoteform', follow_redirects=True).status_code == 200
    response = client.post(
        '/quoteform', data={'gallons': '50', 'date': '2024-06-03', 'address': "TestAddress, TestCity, TX, 33333", 'price': '120.5', 'total': '6025.0'}, follow_redirects=True
    )
    data = response.data.decode('utf-8')
    assert 'TestAddress2' not in data
    assert client.get('/profile_management', follow_redirects=True).status_code == 200
    response = client.post('/profile_management',
        data={"full_name": 'TestName', 'address1': 'TestAddress', 'address2': 'TestAddress2', 'city': 'TestCity', 'state': 'TestCity', 'zipcode': '33333'}, follow_redirects=True
    )'''

'''def test_quoteform_quote_submission(client, app):
    with app.app_context():
        pre_submission_quote_count = User.query???
        response = client.post('/quoteform', data={
            'gallons': '100',
            'date': '2024-06-03',
            'address': "Some Address",
            'price': '2.5',
            'total': '250.0'
        })
    # still working on this'''