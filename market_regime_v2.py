def market_regime_v2(
    pcr,
    strongest_support,
    strongest_resistance,
    top_call_oi_change,
    top_put_oi_change
):

    score = 0
    reasons = []

    if pcr < 0.9:
        score -= 25
        reasons.append(
            "PCR Bearish"
        )

    elif pcr > 1.1:
        score += 25
        reasons.append(
            "PCR Bullish"
        )

    if top_call_oi_change > top_put_oi_change:
        score -= 25
        reasons.append(
            "Call Writing Dominant"
        )

    else:
        score += 25
        reasons.append(
            "Put Writing Dominant"
        )

    if strongest_resistance > strongest_support:
        score -= 20
        reasons.append(
            "Resistance Stronger"
        )

    else:
        score += 20
        reasons.append(
            "Support Stronger"
        )

    if score <= -20:

        view = "Bearish"

    elif score >= 20:

        view = "Bullish"

    else:

        view = "Neutral"

    confidence = min(
        100,
        abs(score) + 50
    )

    return {
        "view": view,
        "confidence": confidence,
        "reasons": reasons
    }