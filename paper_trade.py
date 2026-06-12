import pandas as pd
from datetime import datetime
from pathlib import Path

FILE = Path("paper_trades.csv")

def save_paper_trade(trade):

    row = {
        "time": datetime.now(),
        "strike": trade["strike"],
        "type": trade["type"],
        "entry": trade["entry"],
        "sl": trade["sl"],
        "target1": trade["target1"],
        "target2": trade["target2"],
        "grade": trade["grade"],
        "confidence": trade["confidence"]
    }

    df = pd.DataFrame([row])

    header = not FILE.exists()

    df.to_csv(
        FILE,
        mode="a",
        header=header,
        index=False
    )