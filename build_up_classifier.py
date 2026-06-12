import pandas as pd

def classify_buildup(df):

    result = df.copy()

    result["buildup"] = "Neutral"

    # Long Build-up
    result.loc[
        (result["ltp"] > 0)
        &
        (result["oi_change"] > 0),
        "buildup"
    ] = "Long Build-up"

    # Short Covering
    result.loc[
        (result["ltp"] > 0)
        &
        (result["oi_change"] < 0),
        "buildup"
    ] = "Short Covering"

    return result