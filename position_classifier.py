import pandas as pd

def classify_positions(df):

    if "oi_change" not in df.columns:
        return pd.DataFrame()

    result = df.copy()

    result["position"] = "Neutral"

    # Long Build-up
    result.loc[
        (result["ltp_change"] > 0) &
        (result["oi_change"] > 0),
        "position"
    ] = "Long Build-up"

    # Short Build-up
    result.loc[
        (result["ltp_change"] < 0) &
        (result["oi_change"] > 0),
        "position"
    ] = "Short Build-up"

    # Short Covering
    result.loc[
        (result["ltp_change"] > 0) &
        (result["oi_change"] < 0),
        "position"
    ] = "Short Covering"

    # Long Unwinding
    result.loc[
        (result["ltp_change"] < 0) &
        (result["oi_change"] < 0),
        "position"
    ] = "Long Unwinding"

    return result