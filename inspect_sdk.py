from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv

nubra = InitNubraSdk(
    NubraEnv.PROD,
    env_creds=True
)

print(dir(nubra))