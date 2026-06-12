def bear_call_spread(
    sell_strike,
    buy_strike,
    sell_ltp,
    buy_ltp,
    lot_size=65
):

    credit = sell_ltp - buy_ltp

    width = buy_strike - sell_strike

    max_profit = credit * lot_size

    max_loss = (
        width - credit
    ) * lot_size

    rr = (
        max_profit / max_loss
        if max_loss > 0
        else 0
    )

    breakeven = (
        sell_strike + credit
    )

    return {
        "strategy":"Bear Call Spread",
        "sell_strike":sell_strike,
        "buy_strike":buy_strike,
        "credit":round(credit,2),
        "max_profit":round(max_profit,2),
        "max_loss":round(max_loss,2),
        "risk_reward":round(rr,2),
        "breakeven":round(breakeven,2)
    }