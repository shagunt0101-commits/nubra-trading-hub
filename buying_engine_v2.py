import pandas as pd


def option_buying_engine_v2(
    df,
    spot,
    support,
    resistance
):

    strikes = sorted(df["strike"].unique())

    atm = min(
        strikes,
        key=lambda x: abs(x - spot)
    )

    watchlist = [

        atm - 100,
        atm - 50,
        atm,

        atm + 50,
        atm + 100

    ]

    candidates = df[
        df["strike"].isin(
            watchlist
        )
    ].copy()

    candidates["oi_velocity"] = (
        candidates["oi_change"]
        /
        candidates["oi"].replace(0, 1)
    ) * 100

    avg_volume = max(
        candidates["volume"].mean(),
        1
    )

    candidates["volume_factor"] = (
        candidates["volume"]
        /
        avg_volume
    )

    candidates["flow"] = "Neutral"

    candidates.loc[
        (
            candidates["ltp_change"] > 0
        )
        &
        (
            candidates["oi_change"] > 0
        ),
        "flow"
    ] = "Long Build-up"

    candidates.loc[
        (
            candidates["ltp_change"] > 0
        )
        &
        (
            candidates["oi_change"] < 0
        ),
        "flow"
    ] = "Short Covering"

    candidates["score"] = (

        candidates["ltp_change"].abs() * 0.35

        +

        candidates["oi_velocity"].abs() * 0.25

        +

        candidates["volume_factor"] * 10 * 0.20

        +

        candidates["delta"].abs() * 100 * 0.20

    )

    candidates["confidence"] = (
        candidates["score"]
        .clip(
            upper=100
        )
        .round(1)
    )

    return candidates.sort_values(
        "score",
        ascending=False
    )