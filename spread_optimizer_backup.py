from strategy_pricer import (
    bear_call_spread
)

from pop_engine import (
    estimate_pop
)


def optimize_bear_call(
    df,
    spot,
    expected_move
):

    ce = (
        df[
            (df["type"] == "CE")
            &
            (df["strike"] > spot)
        ]
        .sort_values(
            "strike"
        )
    )

    results = []

    strikes = (
        ce["strike"]
        .tolist()
    )

    for sell_strike in strikes:

        buy_strike = (
            sell_strike + 100
        )

        try:

            sell_ltp = float(
                ce[
                    ce["strike"]
                    ==
                    sell_strike
                ]["ltp"].iloc[0]
            )

            buy_ltp = float(
                ce[
                    ce["strike"]
                    ==
                    buy_strike
                ]["ltp"].iloc[0]
            )

            trade = (
                bear_call_spread(
                    sell_strike,
                    buy_strike,
                    sell_ltp,
                    buy_ltp
                )
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