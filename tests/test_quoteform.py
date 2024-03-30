import pytest

@pytest.mark.parametrize("gallons, date, address, price, total", [
    ('50', '2024-06-03', "4300 Martin Luther King Blvd, Houston, TX 77204", '120.5', '6025.0'),                       # Test case 1: Base case
    ('', '2024-06-03', "4300 Martin Luther King Blvd, Houston, TX 77204", '', ''),                                    # Test case 2: No gallons
    ('50', '', "4300 Martin Luther King Blvd, Houston, TX 77204", '', ''),                                            # Test case 3: No date
    ('', '', "4300 Martin Luther King Blvd, Houston, TX 77204", '', ''),                                              # Test case 4: No gallons and date
    ('50', '2024-06-03', '', '', ''),                                                                                 # Test case 5: No address
])
def test_quoteform_validate_input(client, gallons, date, address, price, total):
    assert client.get('/quoteform').status_code == 200
    response = client.post(
        '/quoteform', data={'gallons': gallons, 'date': date, 'address': address, 'price': price, 'total': total}
    )
    data = response.data.decode('utf-8')
    if gallons == '' and date == '':
        assert 'Enter an amount for fuel voluem (gallons) and choose a delivery date' in data
    elif gallons == '':
        assert 'Enter an amount for fuel volume (gallons)' in data
    elif date == '':
        assert 'Choose a delivery date' in data
    assert gallons in data
    assert date in data
    assert address in data
    assert price in data
    assert total in data
    if gallons and price:
        assert float(gallons) * float(price) == float(total)

# TO-DO: ONCE WE HAVE A DB, TEST IF SUBMITTED QUOTE WAS SUCCESSFULLY COMMITTED TO DB.