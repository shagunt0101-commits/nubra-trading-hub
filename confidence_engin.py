def confidence_score(row):

    score = 0

    if row["volume_factor"] > 2:
        score += 25

    if row["oi_velocity"] > 2:
        score += 25

    if abs(row["delta"]) > 0.40:
        score += 25

    if row["ltp_change"] > 0:
        score += 25

    return min(score, 100)