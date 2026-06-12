import pandas as pd

def calculate_pnl(trades_df):

    if len(trades_df) == 0:

        return {
            "total": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0
        }

    wins = 0
    losses = 0

    for _, row in trades_df.iterrows():

        if row["confidence"] >= 80:

            wins += 1

        else:

            losses += 1

    total = wins + losses

    return {

        "total": total,

        "wins": wins,

        "losses": losses,

        "win_rate": round(
            wins / total * 100,
            2
        )
    }