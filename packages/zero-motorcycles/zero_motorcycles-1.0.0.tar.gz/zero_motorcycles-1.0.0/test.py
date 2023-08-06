from zero_motorcycles import Zero

zero_client = Zero(username="email", password="password")

# Get units
zero_client.get_units()

# Get last transmit data for a specific unit
zero_client.get_last_transmit(123456)

# Get subscription expiration
zero_client.get_expiration_date(123456)
