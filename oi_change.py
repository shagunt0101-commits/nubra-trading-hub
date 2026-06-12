import pandas as pd

def calculate_oi_change(current_df, previous_df):

    merged = current_df.merge(
        previous_df[
            ["type", "strike", "oi"]
        ],
        on=["type", "strike"],
        how="left",
        suffixes=("", "_prev")
    )

    merged["oi_prev"] = (
        merged["oi_prev"]
        .fillna(0)
    )

    merged["oi_change"] = (
        merged["oi"] -
        merged["oi_prev"]
    )

    return merged