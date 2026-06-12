def gamma_exposure(df):

    df["gex"] = (
        df["gamma"]
        * df["oi"]
        * df["strike"]
    )

    return (
        df.groupby("strike")["gex"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )