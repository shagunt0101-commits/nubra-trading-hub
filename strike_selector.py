def select_bear_call_strikes(df, spot):

    ce = df[
        (df["type"] == "CE")
        &
        (df["strike"] > spot)
    ].copy()

    ce["score"] = (
        ce["oi_change"] * 0.6
        +
        ce["volume"] * 0.4
    )

    ce = ce.sort_values(
        "score",
        ascending=False
    )

    sell_strike = float(
        ce.iloc[0]["strike"]
    )

    buy_strike = sell_strike + 100

    return {
        "sell_strike": sell_strike,
        "buy_strike": buy_strike,
        "score": int(
            ce.iloc[0]["score"]
        )
    }