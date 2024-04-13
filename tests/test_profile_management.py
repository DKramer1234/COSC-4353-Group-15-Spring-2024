import pytest
from website.models import User


@pytest.mark.parametrize("username, password1, password2, full_name, address1, address2, city, state, zipcode", [
    ("TestUsername", "TestPassword", "TestPassword", "TestFull", "TestAddress", "TestAddress", "TestCity", "TX", 12345),
    ("TestUsername", "TestPassword", "TestPassword","TestFull", "TestAddress", "", "TestCity", "TX", 12345),
    ("TestUsername", "TestPassword", "TestPassword", 'this example has a full name that exceeds the max characters so it gives an error', 'TestAddress', '', 'TestCity', 'TX', 12345),
    ("TestUsername", "TestPassword", "TestPassword","TestFull", "TestAddress", "this is a test case where the address that is being input is over 100 characters to test the if statement i am just typing without counting", "TestCity", "TX", 12345),
    ("TestUsername", "TestPassword", "TestPassword","TestFull", "this is a test case where the address that is being input is over 100 characters to test the if statement i am just typing without counting", "TestAddress", "TestCity", "TX", 12345),
    ("TestUsername", "TestPassword", "TestPassword", "TestFull", "TestAddress", "TestAddress", "thisx is a test case where the user city that is being input is over 100 characters to test the if statement i am just typing without counting", "TX", 12345)


])



def test_profile_management_validate_input(client, app, username, password1, password2, full_name, address1, address2, city, state, zipcode): 
    client.post('/client_registration', data = {'username': 'TestUsername', 'password1':'TestPassword', 'password2':'TestPassword'})
    assert client.get('/client_registration').status_code == 200
    client.post('/', data = {'username': 'TestUsername', 'password':'TestPassword'})
    assert client.get('/').status_code == 200
    
    client.post('/profile_management', data = {'full_name': full_name, 'address1': address1, 'address2': address2, 'city': city, 'state': state, 'zipcode':zipcode})
    response =  client.get('profile_management')
    assert response.status_code == 200
    data = response.data.decode('utf-8')


    if len(full_name) > 50:
       assert 'Full name cannot be greater than 50 characters' in data
    elif len(address1) > 100:
        assert 'Address 1 cannot be greater than 100 characters'in data
    elif len(address2) > 100:
        assert 'Address 2 cannot be greater than 100 characters' in data
    elif len(city) > 100:
        assert 'City cannot be greater than 100 characters' in data
    else:
        client.post('/profile_management', data = {'full_name': full_name, 'address1': address1, 'address2': address2, 'city': city, 'state': state, 'zipcode':zipcode})
        response =  client.get('profile_management')
        assert response.status_code == 200