def PricingModule(user, gallons_requested, delivery_address):
    price_per_gal = 1.5 # fixed price, units: $ / gal
    location_factor = 0.04
    # If Texas is in the delivery address
    if 'TX' in delivery_address:
        location_factor = 0.02
    rate_history = 0.0
    # If the client has previous submitted quotes
    if user.quotes:
        rate_history = 0.01
    gallons_requested_factor = 0.03
    if gallons_requested > 1000.0:
        gallons_requested_factor = 0.02
    profit_margin = 0.1 # fixed
    margin = price_per_gal * (location_factor - rate_history + gallons_requested_factor + profit_margin)
    return price_per_gal * margin
