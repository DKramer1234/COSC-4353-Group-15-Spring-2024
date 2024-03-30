import pytest
from flask import g, session
from website.models import User

@pytest.mark.parametrize("full_name, address1, address2, city, state, zipcode", [
    ("user name", "user address", "user address2", "user city", "st", "user zip"),
    ("user name", "user address", "", "user_city", "st", "user zip"),
    ("", "", "", "", "", ""),
    ("user name", "", "", "", "", "")
])

def test_profile_management_validate_input(client, full_name, address1, address2, city, state, zipcode): #, address2, city, state, zipcode):
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
    data = response.data.decode('utf-8')
    print(data)

    if len(full_name) > 50:
        assert "Full name cannot be greater than 50 characters" in data
    elif len(address1) > 100:
        assert 'Address 1 cannot be greater than 100 characters'in data
    elif len(address2) > 100:
        assert 'Address 2 cannot be greater than 100 characters' in data
    elif len(city) > 100:
        assert 'City cannot be greater than 100 characters' in data