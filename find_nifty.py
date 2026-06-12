from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv

nubra = InitNubraSdk(
    NubraEnv.PROD,
    env_creds=True
)

df = nubra.DF_REF_DATA_NSE

nifty = df[
    df["stock_name"].astype(str).str.contains(
        "NIFTY",
        case=False,
        na=False
    )
]

print(nifty[
    [
        "ref_id",
        "stock_name",
        "expiry",
        "strike_price",
        "option_type",
        "lot_size"
    ]
].head(30))