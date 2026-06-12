import pandas as pd

rows = []

for ce in chain.chain.ce:
    rows.append({
        "type": "CE",
        "strike": ce.strike_price / 100,
        "ltp": (ce.last_traded_price or 0) / 100,
        "oi": ce.open_interest,
        "volume": ce.volume,
        "delta": ce.delta,
        "gamma": ce.gamma,
        "theta": ce.theta,
        "vega": ce.vega,
        "iv": ce.iv
    })

for pe in chain.chain.pe:
    rows.append({
        "type": "PE",
        "strike": pe.strike_price / 100,
        "ltp": (pe.last_traded_price or 0) / 100,
        "oi": pe.open_interest,
        "volume": pe.volume,
        "delta": pe.delta,
        "gamma": pe.gamma,
        "theta": pe.theta,
        "vega": pe.vega,
        "iv": pe.iv
    })

df = pd.DataFrame(rows)

print(df.head())