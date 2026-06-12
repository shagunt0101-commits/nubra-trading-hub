def choose_strategy(
    pcr,
    bear_trade,
    bull_trade
    
):

    score = {
        "Bearish": 0,
        "Bullish": 0
    }

    if pcr < 0.9:
        score["Bearish"] += 40

    elif pcr > 1.1:
        score["Bullish"] += 40

    score["Bearish"] += bear_trade["score"]
    score["Bullish"] += bull_trade["score"]

    if score["Bearish"] > score["Bullish"]:

        return {
            "market_view": "Bearish",
            "confidence": round(
                score["Bearish"],
                1
            ),
            "trade": bear_trade
        }

    return {
        "market_view": "Bullish",
        "confidence": round(
            score["Bullish"],
            1
        ),
        "trade": bull_trade

    
    }