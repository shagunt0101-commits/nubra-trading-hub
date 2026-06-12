def iv_skew(df):

    ce = df[df["type"] == "CE"]["iv"].mean()
    pe = df[df["type"] == "PE"]["iv"].mean()

    return {
        "CE_IV": round(float(ce), 2),
        "PE_IV": round(float(pe), 2),
        "Skew": round(float(pe - ce), 2)
    }