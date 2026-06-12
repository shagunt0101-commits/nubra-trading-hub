from nubra_python_sdk.marketdata.market_data import MarketData
import inspect

print("current_price:")
print(inspect.signature(MarketData.current_price))

print("\nquote:")
print(inspect.signature(MarketData.quote))

print("\noption_chain:")
print(inspect.signature(MarketData.option_chain))

print("\nhistorical_data:")
print(inspect.signature(MarketData.historical_data))