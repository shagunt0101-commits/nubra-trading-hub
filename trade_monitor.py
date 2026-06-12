import pandas as pd

def monitor_trades(
    trades,
    option_chain
):

    if len(trades) == 0:

        return trades

    trades = trades.copy()

    current_prices = {}

    for _, row in option_chain.iterrows():

        key = (
            row["strike"],
            row["type"]
        )

        current_prices[key] = row["ltp"]

    current_ltp = []
    pnl = []
    pnl_pct = []
    status = []

    for _, trade in trades.iterrows():

        key = (
            trade["strike"],
            trade["type"]
        )

        ltp = current_prices.get(
            key,
            trade["entry"]
        )

        current_ltp.append(ltp)

        trade_pnl = (
            ltp
            -
            trade["entry"]
        )

        pnl.append(
            round(trade_pnl,2)
        )

        pnl_pct.append(
            round(
                trade_pnl
                /
                trade["entry"]
                * 100,
                2
            )
        )

        if ltp >= trade["target2"]:

            status.append(
                "TARGET2 HIT"
            )

        elif ltp >= trade["target1"]:

            status.append(
                "TARGET1 HIT"
            )

        elif ltp <= trade["sl"]:

            status.append(
                "SL HIT"
            )

        else:

            status.append(
                "OPEN"
            )

    trades["current_ltp"] = current_ltp
    trades["pnl"] = pnl
    trades["pnl_pct"] = pnl_pct
    trades["status"] = status

    return trades