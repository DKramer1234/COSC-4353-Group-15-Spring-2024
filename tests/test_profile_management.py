import pytest
from website.models import User


@pytest.mark.parametrize("full_name, address1, address2, city, state, zipcode", [
    ("user name", "user address", "user address2", "user city", "st", "user zip"),
    ("user name", "user address", "", "user_city", "st", "user zip"),
    ("", "", "", "", "", ""),
    ("user name", "", "", "", "", ""),
    ('this example has a full name that exceeds the max characters so it gives an error', 'address1', '', 'city', 'state', 'zipcode'),
    ("user name", "address1", "this is a test case where the address that is being input is over 100 characters to test the if statement i am just typing without counting", "user city", "st", "zipcode"),
    ("user name", "this is a test case where the address that is being input is over 100 characters to test the if statement i am just typing without counting", "user address2", "user city", "st", "zipcode"),
    ("user name", "address1", "address2", "this is a test case where the user city that is being input is over 100 characters to test the if statement i am just typing without counting", "st", "zipcode")


])

def test_profile_management_validate_input(client, app, full_name, address1, address2, city, state, zipcode): 
    assert client.get('/profile_management').status_code == 200
    response = client.post('/profile_management',
        data={"full_name": full_name, 
              'address1': address1, 
              'address2': address2, 
              'city': city, 
              'state': state, 
              'zipcode': zipcode
              }
    )
    assert response.status_code ==200
    data = response.data.decode('utf-8')

    if len(full_name) > 50:
        assert "Full name cannot be greater than 50 characters" in data
    elif len(address1) > 100:
        assert 'Address 1 cannot be greater than 100 characters'in data
    elif len(address2) > 100:
        assert 'Address 2 cannot be greater than 100 characters' in data
    elif len(city) > 100:
        assert 'City cannot be greater than 100 characters' in data
    
