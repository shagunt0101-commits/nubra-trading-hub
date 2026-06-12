def probability_engine(
    spot,
    support,
    resistance
):

    nearest_support = support[0]
    nearest_resistance = resistance[0]

    range_width = (
        nearest_resistance -
        nearest_support
    )

    if range_width <= 0:
        return {
            "spot": spot,
            "support": nearest_support,
            "resistance": nearest_resistance,
            "expected_range": 0,
            "bullish_probability": 50,
            "bearish_probability": 50
        }

    bullish_probability = (
        (spot - nearest_support)
        / range_width
    ) * 100

    bearish_probability = (
        (nearest_resistance - spot)
        / range_width
    ) * 100

    bullish_probability = max(
        0,
        min(100, bullish_probability)
    )

    bearish_probability = max(
        0,
        min(100, bearish_probability)
    )

    return {
        "spot": round(spot, 2),
        "support": nearest_support,
        "resistance": nearest_resistance,
        "expected_range": round(range_width, 2),
        "bullish_probability": round(bullish_probability, 1),
        "bearish_probability": round(bearish_probability, 1)
    }