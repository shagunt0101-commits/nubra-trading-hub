import pandas as pd
from probability_touch import probability_of_touch

def build_probability_table(
    df,
    spot,
    atm_iv
):

    strikes = (
        df["strike"]
        .drop_duplicates()
        .sort_values()
    )

    rows = []

    for strike in strikes:

        prob = probability_of_touch(
            spot,
            strike,
            atm_iv
        )

        rows.append({
            "strike": strike,
            "probability_touch": prob
        })

    return pd.DataFrame(rows)