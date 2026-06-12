from pop_engine import estimate_pop


def bull_put_spread(
    sell_strike,
    buy_strike,
    sell_premium,
    buy_premium,
    lot_size=65
):

    credit = sell_premium - buy_premium

    width = sell_strike - buy_strike

    max_profit = credit * lot_size

    max_loss = (
        width - credit
    ) * lot_size

    breakeven = (
        sell_strike - credit
    )

    risk_reward = (
        max_profit / max_loss
        if max_loss > 0
        else 0
    )

    return {
        "strategy": "Bull Put Spread",
        "sell": f"{int(sell_strike)} PE",
        "buy": f"{int(buy_strike)} PE",
        "credit": round(credit, 2),
        "max_profit": round(max_profit, 2),
        "max_loss": round(max_loss, 2),
        "breakeven": round(breakeven, 2),
        "risk_reward": round(risk_reward, 2)
    }


def optimize_bull_put(
    df,
    spot,
    expected_move
):

    pe = (
        df[
            (df["type"] == "PE")
            &
            (df["strike"] < spot)
        ]
        .sort_values(
            "strike",
            ascending=False
        )
    )

    results = []

    strikes = pe["strike"].tolist()

    for sell_strike in strikes:

        buy_strike = (
            sell_strike - 100
        )

        try:

            sell_ltp = float(
                pe[
                    pe["strike"]
                    ==
                    sell_strike
                ]["ltp"].iloc[0]
            )

            buy_ltp = float(
                pe[
                    pe["strike"]
                    ==
                    buy_strike
                ]["ltp"].iloc[0]
            )

            trade = bull_put_spread(
                sell_strike,
                buy_strike,
                sell_ltp,
                buy_ltp
            )

            pop = estimate_pop(
                spot,
                trade["breakeven"],
                expected_move
            )

            trade["pop"] = pop

            trade["score"] = round(
                (
                    trade["risk_reward"]
                    * 40
                )
                +
                (
                    pop
                    * 0.6
                ),
                2
            )

            results.append(
                trade
            )

        except:
            pass

    results = sorted(
        results,
        key=lambda x:
        x["score"],
        reverse=True
    )

    return results