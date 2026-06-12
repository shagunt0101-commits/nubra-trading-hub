import pandas as pd

def calculate_strength(df):

    rows = []

    for strike in sorted(df["strike"].unique()):

        strike_df = df[df["strike"] == strike]

        ce = strike_df[
            strike_df["type"] == "CE"
        ]

        pe = strike_df[
            strike_df["type"] == "PE"
        ]

        ce_oi = ce["oi"].sum()
        ce_change = ce["oi_change"].sum()
        ce_vol = ce["volume"].sum()

        pe_oi = pe["oi"].sum()
        pe_change = pe["oi_change"].sum()
        pe_vol = pe["volume"].sum()

        resistance_score = (
            ce_oi * 0.4 +
            ce_change * 0.4 +
            ce_vol * 0.2
        )

        support_score = (
            pe_oi * 0.4 +
            pe_change * 0.4 +
            pe_vol * 0.2
        )

        rows.append({
            "strike": strike,
            "support_score": support_score,
            "resistance_score": resistance_score
        })

    return pd.DataFrame(rows)