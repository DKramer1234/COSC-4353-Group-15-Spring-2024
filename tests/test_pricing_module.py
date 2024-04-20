import pytest
from website.pricing_module import PricingModule

@pytest.mark.parametrize("gallons, address", [
    (500, "4300 Martin Luther King Blvd, Houston, TX 77204"),
    (2000, "1600 Pennsylvania Avenue NW, Washington, DC 20500")
])
def test_pricing_module(client, gallons, address):
    price = PricingModule(client, gallons, address)
    total = gallons * price
    if gallons == 500 and "TX" in address:
        assert total == 157.9
    if gallons == 2000 and "TX" not in address:
        assert total == 495