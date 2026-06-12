from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from nubra_python_sdk.marketdata.market_data import MarketData

nubra = InitNubraSdk(
    NubraEnv.PROD,
    env_creds=True
)

md = MarketData(nubra)

chain = md.option_chain("NIFTY")

print("\n=== TYPE ===")
print(type(chain))

print("\n=== DIR ===")
print(dir(chain))

print("\n=== MODEL DUMP KEYS ===")
try:
    print(chain.model_dump().keys())
except Exception as e:
    print("model_dump failed:", e)

print("\n=== ATTRIBUTES CHECK ===")
for attr in ["call", "ce", "pe"]:
    print(attr, "->", hasattr(chain, attr))