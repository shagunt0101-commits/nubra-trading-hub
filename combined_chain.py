import pandas as pd

def build_combined_chain(df):

    ce = (
        df[df["type"] == "CE"]
        [
            [
                "strike",
                "oi",
                "oi_change",
                "position"
            ]
        ]
        .rename(
            columns={
                "oi": "ce_oi",
                "oi_change": "ce_oi_change",
                "position": "ce_position"
            }
        )
    )

    pe = (
        df[df["type"] == "PE"]
        [
            [
                "strike",
                "oi",
                "oi_change",
                "position"
            ]
        ]
        .rename(
            columns={
                "oi": "pe_oi",
                "oi_change": "pe_oi_change",
                "position": "pe_position"
            }
        )
    )

    merged = ce.merge(
        pe,
        on="strike",
        how="outer"
    )

    def net_signal(row):

        ce_change = row.get("ce_oi_change", 0)
        pe_change = row.get("pe_oi_change", 0)

        if pe_change > ce_change:
            return "Bullish"

        elif ce_change > pe_change:
            return "Bearish"

        return "Neutral"

    merged["net_signal"] = (
        merged.apply(
            net_signal,
            axis=1
        )
    )

    return merged.sort_values(
        "strike"
    )