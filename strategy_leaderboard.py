def build_leaderboard(
    bear_trade,
    bull_trade,
    condor_trade
):

    rows = []

    if "score" in bear_trade:
        rows.append(bear_trade)

    if "score" in bull_trade:
        rows.append(bull_trade)

    if "pop" in condor_trade:

        condor_trade["score"] = round(
            condor_trade["pop"] * 0.6,
            2
        )

        rows.append(condor_trade)

    rows = sorted(
        rows,
        key=lambda x: x["score"],
        reverse=True
    )

    for i, row in enumerate(rows):
        row["rank"] = i + 1

    return rows