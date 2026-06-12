# inspect_market_constructor.py

from nubra_python_sdk.marketdata.market_data import MarketData
import inspect

print(inspect.signature(MarketData))
print()
print(inspect.signature(MarketData.__init__))