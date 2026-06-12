def evaluate_trade(
    spot,
    expiry_price,
    breakeven
):

    if expiry_price < breakeven:

        return "WIN"

    return "LOSS"