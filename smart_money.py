import pandas as pd

def smart_money_signals(df):

    signals = []

    top_oi_change = (
        df.sort_values(
            "oi_change",
            ascending=False
        )
        .head(20)
    )

    for _, row in top_oi_change.iterrows():

        if row["type"] == "PE":
            signals.append({
                "signal": "Bullish Build-up",
                "strike": row["strike"],
                "oi_change": row["oi_change"]
            })

        if row["type"] == "CE":
            signals.append({
                "signal": "Bearish Build-up",
                "strike": row["strike"],
                "oi_change": row["oi_change"]
            })

    return pd.DataFrame(signals)