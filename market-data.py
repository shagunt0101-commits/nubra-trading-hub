from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv

nubra = InitNubraSdk(
    NubraEnv.PROD,
    env_creds=True
)

for item in dir(nubra):
    if any(x in item.lower() for x in [
        "market",
        "quote",
        "option",
        "chain",
        "data",
        "order",
        "trade",
        "portfolio",
        "position",
        "instrument",
        "realtime"
    ]):
        print(item)