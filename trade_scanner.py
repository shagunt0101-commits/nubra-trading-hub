def trade_scanner(
    spot,
    pcr,
    support,
    resistance,
    volatility,
    expected_move
):

    trades = []

    # Bearish setup
    if pcr < 0.9:

        trades.append({
            "rank": 1,
            "strategy": "Bear Call Spread",
            "sell_strike": resistance[0],
            "buy_strike": resistance[0] + 100,
            "confidence": 85,
            "reason": [
                "PCR Bearish",
                "Strong Resistance",
                "Call Writing"
            ]
        })

    # Bullish setup
    if pcr > 1.1:

        trades.append({
            "rank": 1,
            "strategy": "Bull Put Spread",
            "sell_strike": support[0],
            "buy_strike": support[0] - 100,
            "confidence": 85,
            "reason": [
                "PCR Bullish",
                "Strong Support",
                "Put Writing"
            ]
        })

    # Neutral setup
    if 0.9 <= pcr <= 1.1:

        trades.append({
            "rank": 1,
            "strategy": "Iron Condor",
            "confidence": 75,
            "reason": [
                "Balanced PCR",
                "Range Bound"
            ]
        })

    return trades