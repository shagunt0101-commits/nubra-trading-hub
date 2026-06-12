import pandas as pd
import os
from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from nubra_python_sdk.marketdata.market_data import MarketData
from nubra_python_sdk.refdata.instruments import InstrumentData

# Global variables for SDK
sdk_nse = None
market_nse = None
instruments_data = None
_initialized = False

def initialize_sdk_with_otp(otp=None):
    """Initialize SDK with optional OTP"""
    global sdk_nse, market_nse, instruments_data, _initialized
    
    if _initialized and sdk_nse is not None:
        return True, "SDK already initialized"
    
    try:
        if otp:
            os.environ["OTP"] = otp
        
        sdk_nse = InitNubraSdk(
            NubraEnv.PROD,
            env_creds=True
        )
        market_nse = MarketData(sdk_nse)
        instruments_data = InstrumentData(sdk_nse)
        _initialized = True
        return True, "SDK initialized successfully"
    
    except Exception as e:
        error_msg = str(e)
        # Check if it's asking for OTP
        if "otp" in error_msg.lower() or "OTP" in error_msg or "Enter OTP" in error_msg:
            return False, f"OTP Required: Please check your phone for the OTP message."
        return False, f"Initialization Error: {error_msg}"

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
    global market_nse
    
    if market_nse is None:
        raise RuntimeError("SDK not initialized. Please verify OTP first.")
    
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