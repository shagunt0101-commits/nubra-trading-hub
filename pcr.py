def calculate_pcr(df):

    ce_oi = df[df.type=="CE"]["oi"].sum()
    pe_oi = df[df.type=="PE"]["oi"].sum()

    pcr = pe_oi / ce_oi

    return {
        "PCR": round(pcr,3),
        "CE_OI": int(ce_oi),
        "PE_OI": int(pe_oi)
    }