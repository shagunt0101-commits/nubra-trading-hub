from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from nubra_python_sdk.marketdata.market_data import MarketData

nubra = InitNubraSdk(
    NubraEnv.PROD,
    env_creds=True
)

md = MarketData(nubra)

oc = md.option_chain("NIFTY")

print("\nTOP LEVEL KEYS")
print(oc.model_dump().keys())

print("\nCHAIN TYPE")
print(type(oc.chain))

print("\nCHAIN DIR")
print(dir(oc.chain))

print("\nCHAIN DUMP")
try:
    print(oc.chain.model_dump().keys())
except Exception as e:
    print(e)