import pandas as pd
from pathlib import Path

def load_journal():

    file = Path(
        "paper_trades.csv"
    )

    if file.exists():

        return pd.read_csv(file)

    return pd.DataFrame()