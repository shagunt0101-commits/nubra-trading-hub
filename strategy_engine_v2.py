def suggest_strategy(
    spot,
    support,
    resistance,
    pcr,
    expected_move,
    volatility
):

    support_level = support[0]
    resistance_level = resistance[0]

    # Bullish

    if (
        pcr > 1
        and
        spot > support_level
    ):

        return {
            "strategy":"Bull Put Spread",
            "confidence":80,
            "sell_strike":support_level,
            "buy_strike":support_level - 100,
            "view":"Bullish"
        }

    # Bearish

    if (
        pcr < 0.7
        and
        spot < resistance_level
    ):

        return {
            "strategy":"Bear Call Spread",
            "confidence":80,
            "sell_strike":resistance_level,
            "buy_strike":resistance_level + 100,
            "view":"Bearish"
        }

    # Range

    if volatility == "High":

        return {
            "strategy":"Iron Condor",
            "confidence":75,
            "sell_pe":support_level,
            "sell_ce":resistance_level,
            "view":"Range Bound"
        }

    return {
        "strategy":"Wait",
        "confidence":50,
        "view":"No Edge"
    }