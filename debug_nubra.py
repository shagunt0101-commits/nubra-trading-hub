from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv

nubra = InitNubraSdk(NubraEnv.PROD)

print(type(nubra))
print()
print(dir(nubra))