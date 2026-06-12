from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv

try:
    nubra = InitNubraSdk(
        NubraEnv.PROD,   # Use PROD for your real account
        env_creds=True
    )

    print("Authentication Successful")
    print(type(nubra))

except Exception as e:
    print("Authentication Failed")
    print(e)