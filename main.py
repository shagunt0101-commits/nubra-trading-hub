from fetch_chain import get_chain
from pcr import calculate_pcr
from max_pain import calculate_max_pain
from support_resistance import support_resistance
from gamma_exposure import gamma_exposure

df, chain = get_chain()

print("\nSPOT")
print(chain.current_price/100)

print("\nPCR")
print(calculate_pcr(df))

print("\nMAX PAIN")
print(calculate_max_pain(df))

print("\nSUPPORT / RESISTANCE")
print(support_resistance(df))

print("\nTOP GEX")
print(gamma_exposure(df))