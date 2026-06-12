
import pandas as pd
from pathlib import Path

LOG_FILE = Path("trade_log.csv")

def save_trade(trade):
    df = pd.DataFrame([trade])
    header = not LOG_FILE.exists()
    df.to_csv(LOG_FILE, mode="a", header=header, index=False)
