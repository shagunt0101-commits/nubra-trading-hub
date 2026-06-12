from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv

sdk = InitNubraSdk(
    NubraEnv.PROD,
    env_creds=True
)

print("LOGIN SUCCESS")