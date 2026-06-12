def confidence_score(row):

    score = 0

    score += min(
        row["volume_factor"] * 15,
        30
    )

    score += min(
        row["oi_velocity"] * 2,
        30
    )

    score += min(
        abs(row["delta"]) * 50,
        20
    )

    if row["ltp_change"] > 0:
        score += 20

    return round(
        min(score, 100),
        1
    )