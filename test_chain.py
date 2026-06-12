from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from nubra_python_sdk.marketdata.market_data import MarketData

nubra = InitNubraSdk(
    NubraEnv.PROD,
    env_creds=True
)

md = MarketData(nubra)

print(
    md.option_chain(
        instrument="NIFTY"
    )
)