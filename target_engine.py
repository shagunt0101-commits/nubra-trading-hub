def calculate_targets(
    row,
    support_levels,
    resistance_levels,
    expected_move
):

    entry = float(row["ltp"])

    if row["type"] == "CE":

        sl = min(support_levels)

        target1 = max(
            [
                x for x in resistance_levels
                if x > row["strike"]
            ],
            default=row["strike"] + 50
        )

        target2 = (
            row["strike"]
            + expected_move
        )

    else:

        sl = max(resistance_levels)

        target1 = min(
            [
                x for x in support_levels
                if x < row["strike"]
            ],
            default=row["strike"] - 50
        )

        target2 = (
            row["strike"]
            - expected_move
        )

    return {
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "target1": round(target1, 2),
        "target2": round(target2, 2)
    }