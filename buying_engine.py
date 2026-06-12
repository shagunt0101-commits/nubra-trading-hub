import pandas as pd

from flow_engine import classify_flow
from confidence_engine import confidence_score
from institutional_engine import institutional_flag


def momentum_strength(score):

    if score >= 90:
        return "EXPLOSIVE"

    elif score >= 75:
        return "STRONG"

    elif score >= 60:
        return "MODERATE"

    return "WEAK"


def option_buying_engine(
    df,
    spot
):

    strikes = sorted(
        df["strike"].unique()
    )

    atm = min(
        strikes,
        key=lambda x: abs(x - spot)
    )

    watch = [
        atm - 100,
        atm - 50,
        atm,
        atm + 50,
        atm + 100
    ]

    candidates = df[
        df["strike"].isin(watch)
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

    candidates["score"] = (
        candidates["ltp_change"].abs() * 0.35
        +
        candidates["oi_velocity"].abs() * 0.25
        +
        candidates["volume_factor"] * 10 * 0.25
        +
        candidates["delta"].abs() * 100 * 0.15
    )

    candidates["signal"] = "WAIT"

    candidates.loc[
        (
            candidates["ltp_change"] > 0
        )
        &
        (
            candidates["oi_change"] > 0
        ),
        "signal"
    ] = "BUY"

    candidates["flow"] = (
        candidates.apply(
            classify_flow,
            axis=1
        )
    )

    candidates["confidence"] = (
        candidates.apply(
            confidence_score,
            axis=1
        )
    )

    candidates["institutional"] = (
        candidates.apply(
            institutional_flag,
            axis=1
        )
    )

    candidates["strength"] = (
        candidates["score"]
        .apply(momentum_strength)
    )
    candidates["grade"] =(
        candidates.apply(
        setup_grade,
        axis=1
    )
)
    candidates["radar_score"] = (

    candidates["confidence"] * 0.4

    +

    candidates["score"] * 0.3

    +

    candidates["oi_velocity"] * 0.15

    +

    candidates["volume_factor"] * 10 * 0.15

)
    elite = candidates[

    candidates["institutional"]

].sort_values(

    "radar_score",

    ascending=False

)

    candidates["burst"] = (
        (candidates["volume_factor"] > 3)
        &
        (candidates["oi_velocity"] > 5)
        &
        (candidates["ltp_change"] > 10)
    )

    candidates = candidates.sort_values(
        "score",
        ascending=False
    )

    best_ce = (
        candidates[
            candidates["type"] == "CE"
        ]
        .head(1)
    )

    best_pe = (
        candidates[
            candidates["type"] == "PE"
        ]
        .head(1)
    )

    return (
        best_ce,
        best_pe,
        candidates
    )

def setup_grade(row):

    if (
        row["confidence"] >= 90
        and row["strength"] == "EXPLOSIVE"
        and row["flow"] in [
            "Long Build-up",
            "Short Covering"
        ]
    ):
        return "A+"

    elif row["confidence"] >= 75:
        return "A"

    elif row["confidence"] >= 60:
        return "B"

    return "AVOID"
