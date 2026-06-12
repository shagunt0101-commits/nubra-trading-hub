def bear_call_spread(
    sell_strike,
    buy_strike,
    sell_premium,
    buy_premium,
    lot_size=75
):

    credit = sell_premium - buy_premium

    width = buy_strike - sell_strike

    max_profit = credit * lot_size

    max_loss = (
        width - credit
    ) * lot_size

    breakeven = (
        sell_strike + credit
    )

    risk_reward = (
        max_profit / max_loss
        if max_loss > 0
        else 0
    )

    return {
        "strategy": "Bear Call Spread",
        "sell": f"{int(sell_strike)} CE",
        "buy": f"{int(buy_strike)} CE",
        "credit": round(credit, 2),
        "max_profit": round(max_profit, 2),
        "max_loss": round(max_loss, 2),
        "breakeven": round(breakeven, 2),
        "risk_reward": round(risk_reward, 2)
    }