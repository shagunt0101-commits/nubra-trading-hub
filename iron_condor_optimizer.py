from pop_engine import estimate_pop


def iron_condor(
    sell_pe,
    buy_pe,
    sell_ce,
    buy_ce,
    sell_pe_premium,
    buy_pe_premium,
    sell_ce_premium,
    buy_ce_premium,
    lot_size=65
):

    total_credit = (
        sell_pe_premium
        - buy_pe_premium
        + sell_ce_premium
        - buy_ce_premium
    )

    width = min(
        sell_pe - buy_pe,
        buy_ce - sell_ce
    )

    max_profit = total_credit * lot_size

    max_loss = (
        width - total_credit
    ) * lot_size

    return {
        "strategy": "Iron Condor",
        "sell_pe": sell_pe,
        "buy_pe": buy_pe,
        "sell_ce": sell_ce,
        "buy_ce": buy_ce,
        "credit": round(total_credit, 2),
        "max_profit": round(max_profit, 2),
        "max_loss": round(max_loss, 2)
    }


def optimize_iron_condor(
    df,
    spot,
    expected_move
):

    lower = spot - expected_move

    upper = spot + expected_move

    try:

        sell_pe = (
            df[
                (df["type"]=="PE")
                &
                (df["strike"]<lower)
            ]
            .sort_values(
                "strike",
                ascending=False
            )
            .iloc[0]
        )

        buy_pe = (
            df[
                (df["type"]=="PE")
                &
                (
                    df["strike"]
                    ==
                    sell_pe["strike"] - 100
                )
            ]
            .iloc[0]
        )

        sell_ce = (
            df[
                (df["type"]=="CE")
                &
                (df["strike"]>upper)
            ]
            .sort_values(
                "strike"
            )
            .iloc[0]
        )

        buy_ce = (
            df[
                (df["type"]=="CE")
                &
                (
                    df["strike"]
                    ==
                    sell_ce["strike"] + 100
                )
            ]
            .iloc[0]
        )

        trade = iron_condor(
            sell_pe["strike"],
            buy_pe["strike"],
            sell_ce["strike"],
            buy_ce["strike"],
            sell_pe["ltp"],
            buy_pe["ltp"],
            sell_ce["ltp"],
            buy_ce["ltp"]
        )

        trade["pop"] = estimate_pop(
            spot,
            (
                sell_ce["strike"]
                +
                sell_pe["strike"]
            ) / 2,
            expected_move
        )

        return trade

    except Exception as e:

        return {
            "error": str(e)
        }