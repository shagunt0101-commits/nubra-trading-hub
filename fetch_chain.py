import pandas as pd
import os
from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from nubra_python_sdk.marketdata.market_data import MarketData
from nubra_python_sdk.refdata.instruments import InstrumentData

# Create SDK for NSE with OTP support
try:
    sdk_nse = InitNubraSdk(
        NubraEnv.PROD,
        env_creds=True
    )
except Exception as e:
    # If OTP is being requested, it will happen here
    # The user will see a prompt in the terminal
    print(f"SDK Initialization: {str(e)}")
    print("If OTP prompt appears, check the terminal/console window and enter the OTP there.")
    raise

market_nse = MarketData(sdk_nse)
instruments_data = InstrumentData(sdk_nse)

def get_available_fno_instruments():
    """Return FNO-enabled instruments - only NSE supported"""
    # Note: SENSEX (BSE) is not FNO-enabled in Nubra SDK
    fno_list = [
        "NIFTY",        # NSE
        "BANKNIFTY",    # NSE
        "FINNIFTY",     # NSE
    ]
    return fno_list

def get_exchange_for_instrument(instrument):
    """Return the appropriate exchange for the instrument"""
    nse_instruments = {"NIFTY", "BANKNIFTY", "FINNIFTY"}
    
    if instrument in nse_instruments:
        return "NSE", market_nse
    else:
        raise ValueError(f"Unknown or unsupported instrument: {instrument}")

def get_chain(instrument="NIFTY"):
    """Fetch option chain for the specified instrument"""
    exchange, market = get_exchange_for_instrument(instrument)
    
    # Fetch option chain without specifying expiry to get the nearest available
    try:
        option_chain_response = market.option_chain(
            instrument=instrument
        )
    except Exception as e:
        raise ValueError(f"Failed to fetch chain for {instrument} on {exchange}: {str(e)}")
    
    # Get available expiries and use the first one (nearest)
    available_expiries = option_chain_response.chain.all_expiries
    if not available_expiries:
        raise ValueError(f"No available expiries for {instrument} on {exchange}")
    
    nearest_expiry = available_expiries[0]
    print(f"Using {instrument} ({exchange}) expiry: {nearest_expiry}")
    
    # Fetch chain with the valid expiry
    chain = market.option_chain(
        instrument=instrument,
        expiry=nearest_expiry
    ).chain

    rows = []

    for ce in chain.ce:
        rows.append({
    "ref_id": ce.ref_id,
    "type":"CE",
    "strike":ce.strike_price/100,
    "oi":ce.open_interest or 0,
    "oi_change": (
        (ce.open_interest or 0)
        -
        (ce.previous_open_interest or 0)
    ),
    "volume":ce.volume or 0,
    "delta":ce.delta,
    "gamma":ce.gamma,
    "theta":ce.theta,
    "vega":ce.vega,
    "iv":ce.iv,
    "ltp":(ce.last_traded_price or 0)/100,
    "ltp_change": ce.last_traded_price_change or 0
})

    for pe in chain.pe:
        rows.append({
    "ref_id": pe.ref_id,
    "type":"PE",
    "strike":pe.strike_price/100,
    "oi":pe.open_interest or 0,
    "oi_change": (
        (pe.open_interest or 0)
        -
        (pe.previous_open_interest or 0)
    ),
    "volume":pe.volume or 0,
    "delta":pe.delta,
    "gamma":pe.gamma,
    "theta":pe.theta,
    "vega":pe.vega,
    "iv":pe.iv,
    "ltp":(pe.last_traded_price or 0)/100,
    "ltp_change": pe.last_traded_price_change or 0
    
})

    return pd.DataFrame(rows), chain

import streamlit as st

@st.cache_resource
def get_market():

    sdk = InitNubraSdk(
        NubraEnv.PROD,
        env_creds=True
    )

    return MarketData(sdk)

market = get_market()