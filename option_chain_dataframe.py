import pandas as pd

from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from nubra_python_sdk.marketdata.market_data import MarketData

# Login
sdk = InitNubraSdk(NubraEnv.PROD)

# Market Data Client
market = MarketData(sdk)

# Option Chain
chain_wrapper = market.option_chain(
    instrument="NIFTY",
    expiry="20260609"
)

chain = chain_wrapper.chain

print("Spot:", chain.current_price / 100)
print("ATM :", chain.at_the_money_strike / 100)

rows = []

for ce in chain.ce:
    rows.append({
        "type": "CE",
        "strike": ce.strike_price / 100,
        "ltp": (ce.last_traded_price or 0) / 100,
        "oi": ce.open_interest or 0,
        "volume": ce.volume or 0,
        "delta": ce.delta,
        "gamma": ce.gamma,
        "theta": ce.theta,
        "vega": ce.vega,
        "iv": ce.iv
    })

for pe in chain.pe:
    rows.append({
        "type": "PE",
        "strike": pe.strike_price / 100,
        "ltp": (pe.last_traded_price or 0) / 100,
        "oi": pe.open_interest or 0,
        "volume": pe.volume or 0,
        "delta": pe.delta,
        "gamma": pe.gamma,
        "theta": pe.theta,
        "vega": pe.vega,
        "iv": pe.iv
    })

df = pd.DataFrame(rows)

print("\nRows:", len(df))
print(df.head())

df.to_csv("nifty_option_chain.csv", index=False)

print("\nSaved -> nifty_option_chain.csv")