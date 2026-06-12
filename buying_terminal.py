
from target_engine import calculate_targets

def build_trade(row):

    ltp = float(row["ltp"])

    return {
        "strike": row["strike"],
        "type": row["type"],
        "entry": round(ltp, 2),
        "sl": round(ltp * 0.85, 2),
        "target1": round(ltp * 1.15, 2),
        "target2": round(ltp * 1.30, 2),
        "flow": row["flow"],
        "strength": row["strength"],
        "grade": row["grade"],
        "confidence": row["confidence"],
        "signal": row["signal"]
    }