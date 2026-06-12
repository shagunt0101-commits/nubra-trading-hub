import pandas as pd

def build_merged_chain(df):

    ce = (
        df[df["type"]=="CE"]
        .copy()
        .rename(columns={
            "oi":"ce_oi",
            "oi_change":"ce_oi_change",
            "volume":"ce_volume",
            "iv":"ce_iv",
            "delta":"ce_delta",
            "gamma":"ce_gamma",
            "theta":"ce_theta",
            "vega":"ce_vega",
            "ltp":"ce_ltp"
        })
    )

    pe = (
        df[df["type"]=="PE"]
        .copy()
        .rename(columns={
            "oi":"pe_oi",
            "oi_change":"pe_oi_change",
            "volume":"pe_volume",
            "iv":"pe_iv",
            "delta":"pe_delta",
            "gamma":"pe_gamma",
            "theta":"pe_theta",
            "vega":"pe_vega",
            "ltp":"pe_ltp"
        })
    )

    merged = ce.merge(
        pe,
        on="strike",
        how="inner"
    )

    def classify(row):

        if (
            row["pe_oi_change"] > 0
            and
            row["ce_oi_change"] < 0
        ):
            return "🟢 Bullish Build-up"

        if (
            row["ce_oi_change"] > 0
            and
            row["pe_oi_change"] < 0
        ):
            return "🔴 Bearish Build-up"

        if (
            row["ce_oi_change"] > 0
            and
            row["pe_oi_change"] > 0
        ):
            return "🟡 Range Formation"

        return "⚪ Neutral"

    merged["signal"] = merged.apply(
        classify,
        axis=1
    )

    return merged