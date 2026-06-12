def option_mathematician(
    spot,
    pcr,
    support,
    resistance,
    volatility,
    expected_move
):

    support_level = support[0]
    resistance_level = resistance[0]

    # Bullish

    if pcr > 1:

        return {
            "view": "Bullish",
            "strategy": "Bull Put Spread",
            "sell_strike": support_level,
            "buy_strike": support_level - 100,
            "confidence": 80,
            "reason": [
                "PCR Bullish",
                "Support Holding"
            ]
        }

    # Bearish

    if pcr < 0.7:

        return {
            "view": "Bearish",
            "strategy": "Bear Call Spread",
            "sell_strike": resistance_level,
            "buy_strike": resistance_level + 100,
            "confidence": 80,
            "reason": [
                "PCR Bearish",
                "Resistance Active"
            ]
        }

    # Neutral

    return {
        "view": "Neutral",
        "strategy": "Iron Condor",
        "sell_pe": support_level,
        "sell_ce": resistance_level,
        "confidence": 70,
        "reason": [
            "Range Bound",
            "No Directional Edge"
        ]
    }