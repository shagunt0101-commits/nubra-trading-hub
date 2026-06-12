def institutional_flag(row):

    return (

        row["volume_factor"] > 1.5

        and

        row["oi_velocity"] > 2

        and

        abs(row["delta"]) > 0.35

        and

        row["confidence"] >= 70

    )