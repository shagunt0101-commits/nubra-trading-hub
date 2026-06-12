def build_trade(
    row,
    support,
    resistance
):

    ltp = float(
        row["ltp"]
    )

    if row["type"] == "CE":

        target1 = min(
            resistance
        )

        target2 = (
            target1 + 50
        )

    else:

        target1 = max(
            support
        )

        target2 = (
            target1 - 50
        )

    return {

        "strike":
        row["strike"],

        "type":
        row["type"],

        "entry":
        round(
            ltp,
            2
        ),

        "sl":
        round(
            ltp * 0.85,
            2
        ),

        "target1":
        target1,

        "target2":
        target2,

        "confidence":
        row["confidence"],

        "flow":
        row["flow"]
    }