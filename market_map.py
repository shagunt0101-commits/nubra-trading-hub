def market_map(
    spot,
    support,
    resistance,
    expected_move
):

    return {
        "spot": spot,
        "nearest_support": support[0],
        "nearest_resistance": resistance[0],
        "upper_expected": (
            spot + expected_move
        ),
        "lower_expected": (
            spot - expected_move
        )
    }