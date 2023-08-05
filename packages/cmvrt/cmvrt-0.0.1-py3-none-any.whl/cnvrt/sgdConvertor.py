
def convert_to_sgd(amount, currency):
    sgd_rate = {"USD": 1.33, "EUR": 1.49, "JPY": 0.012, "GBP": 1.64} # exchange rates as of 29th March 2023
    if currency in sgd_rate:
        sgd_amount = amount * sgd_rate[currency]
        return sgd_amount
    else:
        return None

