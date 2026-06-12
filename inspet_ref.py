from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv

nubra = InitNubraSdk(
    NubraEnv.PROD,
    env_creds=True
)

print(type(nubra.DF_REF_DATA_NSE))
print(nubra.DF_REF_DATA_NSE.head())
print(nubra.DF_REF_DATA_NSE.columns.tolist())