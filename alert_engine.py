def generate_alerts(board):

    alerts = []

    for _, row in board.iterrows():

        if (
            row["confidence"] >= 80
            and
            row["signal"] == "BUY"
        ):

            alerts.append(
                f"{row['type']} {row['strike']} "
                f"{row['flow']} "
                f"Confidence {row['confidence']}%"
            )

    return alerts