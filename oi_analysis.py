import pandas as pd

df = pd.read_csv("nifty_option_chain.csv")

ce = df[df["type"] == "CE"]
pe = df[df["type"] == "PE"]

print("\nTOP 10 CE OI")
print(
    ce.sort_values("oi", ascending=False)
      [["strike", "oi", "volume"]]
      .head(10)
)

print("\nTOP 10 PE OI")
print(
    pe.sort_values("oi", ascending=False)
      [["strike", "oi", "volume"]]
      .head(10)
)