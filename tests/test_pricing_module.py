import pytest
from website.pricing_module import PricingModule

def test_pricing_module():
    gallons = 100
    address = "4300 Martin Luther King Blvd, Houston, TX 77204"
    price = PricingModule(address)
    total = gallons * price
    assert total == 12050