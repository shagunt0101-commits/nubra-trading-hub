
import pandas as pd
from pathlib import Path

LOG_FILE = Path("trade_log.csv")

def load_trades():
    if LOG_FILE.exists():
        return pd.read_csv(LOG_FILE)
    return pd.DataFrame()
