
def classify_flow(row):
    ltp_change = row["ltp_change"]
    oi_change = row["oi_change"]

    if ltp_change > 0 and oi_change > 0:
        return "Long Build-up"
    elif ltp_change < 0 and oi_change > 0:
        return "Short Build-up"
    elif ltp_change > 0 and oi_change < 0:
        return "Short Covering"
    return "Long Unwinding"
