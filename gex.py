def calculate_gex(df):

    df = df.copy()

    df["gex"] = (
        df["gamma"].fillna(0)
        * df["oi"].fillna(0)
    )

    return (
        df.groupby("strike", as_index=False)
        .agg(
            gex=("gex", "sum"),
            oi=("oi", "sum")
        )
    )