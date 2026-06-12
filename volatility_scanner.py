def volatility_signal(atm_iv):

    if atm_iv > 0.25:
        return {
            "volatility":"High",
            "preferred":"Option Selling"
        }

    elif atm_iv < 0.12:
        return {
            "volatility":"Low",
            "preferred":"Option Buying"
        }

    else:
        return {
            "volatility":"Normal",
            "preferred":"Spreads"
        }