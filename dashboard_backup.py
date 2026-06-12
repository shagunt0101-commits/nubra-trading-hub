import streamlit as st
import pandas as pd

from fetch_chain import get_chain
from pcr import calculate_pcr
from max_pain import calculate_max_pain
from streamlit_autorefresh import st_autorefresh




st.set_page_config(layout="wide")
st.caption("NUBRA WALO KI JAI HO8")

df, chain = get_chain()
if "previous_df" not in st.session_state:
    st.session_state.previous_df = df.copy()


st.session_state.previous_df = df.copy()

spot = chain.current_price / 100

pcr_data = calculate_pcr(df)
max_pain = calculate_max_pain(df)

st.title("Nubra Options Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Spot", round(spot, 2))
col2.metric("PCR", pcr_data["PCR"])
col3.metric("Max Pain", max_pain)

st.subheader("Option Chain")

st.dataframe(df)
from oi_heatmap import plot_oi

st.subheader("OI Distribution")

st.plotly_chart(
    plot_oi(df),
    use_container_width=True

)
ce = (
    df[df.type=="CE"]
    .sort_values("oi",ascending=False)
    .head(10)
)

pe = (
    df[df.type=="PE"]
    .sort_values("oi",ascending=False)
    .head(10)
)

left,right = st.columns(2)

left.subheader("Top Resistance")
left.dataframe(ce[["strike","oi","volume"]])

right.subheader("Top Support")
right.dataframe(pe[["strike","oi","volume"]])

from support_resistance import get_support_resistance
from iv_skew import iv_skew
from gex import calculate_gex

support,resistance = get_support_resistance(df)

st.subheader("Support")

st.write(support)

st.subheader("Resistance")

st.write(resistance)

skew = iv_skew(df)

st.subheader("IV Analysis")

st.write(skew)

st.subheader("Largest OI Build-up")

build_up = (
    df.sort_values(
        "oi_change",
        ascending=False
    )
    [["type","strike","oi_change","oi"]]
    .head(15)
)

st.dataframe(build_up)

st.subheader("Largest OI Unwinding")

unwind = (
    df.sort_values(
        "oi_change",
        ascending=True
    )
    [["type","strike","oi_change","oi"]]
    .head(15)
)

st.dataframe(unwind)

from market_outlook import market_outlook

outlook = market_outlook(
    spot,
    support,
    resistance,
    pcr_data["PCR"]
)

st.subheader("Market Outlook")
st.json(outlook)

from gex import calculate_gex

gex_df = calculate_gex(df)

st.subheader("Gamma Exposure")

top_gex = (
    gex_df.sort_values(
        "gex",
        ascending=False
    )
    [["strike","gex"]]
    .head(15)
)

st.dataframe(top_gex)

from signal_engine import generate_signals

signals = generate_signals(df)

st.subheader("Signal Engine")

for s in signals:
    st.success(s)

    from position_classifier import classify_positions

classified = classify_positions(df)

st.subheader("Position Classification")

st.dataframe(
    classified[
        [
            "type",
            "strike",
            "ltp_change",
            "oi_change",
            "position"
        ]
    ].sort_values(
        "oi_change",
        ascending=False
    )
)
from smart_money import smart_money_signals

st.subheader("Smart Money Signals")

signals = smart_money_signals(df)

st.dataframe(signals)

from probability import probability_engine

prob = probability_engine(
    spot,
    support,
    resistance
)

st.subheader("Probability Model")
st.json(prob)

from merged_chain import build_merged_chain

st.subheader("Professional Option Chain")

merged_df = build_merged_chain(df)

st.dataframe(
    merged_df[
        [
            "ce_oi",
            "ce_oi_change",
            "ce_volume",
            "ce_iv",
            "strike",
            "pe_iv",
            "pe_volume",
            "pe_oi_change",
            "pe_oi",
            "signal"
        ]
    ],
    use_container_width=True
)
from strategy_engine import suggest_strategy

strategy = suggest_strategy(
    spot,
    pcr_data["PCR"],
    support,
    resistance
)

st.subheader("Recommended Trade")

st.json(strategy)

from market_regime import market_regime

regime = market_regime(
    pcr_data["PCR"],
    spot,
    support,
    resistance
)

st.subheader("Market Regime")
st.json(regime)

from atm_iv import get_atm_iv
from expected_move import expected_move

atm_iv = get_atm_iv(
    df,
    spot
)

move = expected_move(
    spot,
    atm_iv
)

st.subheader("Expected Move")

st.json(move)
from strike_probabilities import (
    build_probability_table
)

prob_df = build_probability_table(
    df,
    spot,
    atm_iv
)

st.subheader(
    "Probability Of Touch"
)

st.dataframe(
    prob_df.sort_values(
        "probability_touch",
        ascending=False
    )
)
from volatility_scanner import volatility_signal

vol_signal = volatility_signal(
    atm_iv
)

st.subheader("Volatility Regime")

st.json(vol_signal)

from strategy_engine_v2 import suggest_strategy

strategy = suggest_strategy(
    spot,
    support,
    resistance,
    pcr_data["PCR"],
    move["expected_move"],
    vol_signal["volatility"]
)

st.subheader("AI Strategy")

st.json(strategy)

from institutional_flow import institutional_flow
flow_df = institutional_flow(df)

st.subheader("Institutional Flow Scanner")

st.dataframe(
    flow_df.sort_values(
        "oi_change",
        ascending=False
    ).head(25)
)
from trade_candidates import trade_candidates

candidate_df = trade_candidates(
    df,
    spot
)

st.subheader(
    "Top Tradeable Strikes"
)

st.dataframe(
    candidate_df[
        [
            "type",
            "strike",
            "oi",
            "oi_change",
            "volume",
            "score"
        ]
    ].head(20)
)
from option_mathematician import (
    option_mathematician
)
recommendation = option_mathematician(
    spot,
    pcr_data["PCR"],
    support,
    resistance,
    vol_signal["volatility"],
    move["expected_move"]
)

st.subheader(
    "Option Mathematician"
)

st.json(recommendation)

from combined_chain import (
    build_combined_chain
)

combined = build_combined_chain(
    classified
)

st.subheader(
    "Institutional Combined Chain"
)

st.dataframe(
    combined[
        [
            "ce_oi_change",
            "ce_position",
            "strike",
            "pe_oi_change",
            "pe_position",
            "net_signal"
        ]
    ]
)

from strength_engine import calculate_strength

strength_df = calculate_strength(df)

st.subheader(
    "Support / Resistance Strength"
)

st.dataframe(
    strength_df.sort_values(
        "resistance_score",
        ascending=False
    ).head(15)
)

best_support = (
    strength_df
    .sort_values(
        "support_score",
        ascending=False
    )
    .iloc[0]
)

best_resistance = (
    strength_df
    .sort_values(
        "resistance_score",
        ascending=False
    )
    .iloc[0]
)

st.metric(
    "Strongest Support",
    best_support["strike"]
)

st.metric(
    "Strongest Resistance",
    best_resistance["strike"]
)

st.subheader("Top Support Levels")

top_support = (
    strength_df
    .sort_values(
        "support_score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_support[
        [
            "strike",
            "support_score"
        ]
    ]
)

st.subheader("Top Resistance Levels")

top_resistance = (
    strength_df
    .sort_values(
        "resistance_score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_resistance[
        [
            "strike",
            "resistance_score"
        ]
    ]
)

from market_map import market_map

map_data = market_map(
    spot,
    support,
    resistance,
    move["expected_move"]
)

st.subheader("Market Map")

st.json(map_data)

st.subheader("System Health")

st.write("Rows:", len(df))
st.write("Spot:", spot)
st.write("PCR:", pcr_data["PCR"])

st.write(
    "Max OI Change:",
    df["oi_change"].abs().max()
)

st.write(
    "Max LTP Change:",
    df["ltp_change"].abs().max()
)

st.subheader("Data Quality")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Rows",
    len(df)
)

col2.metric(
    "Max OI Change",
    f"{int(df['oi_change'].abs().max()):,}"
)

col3.metric(
    "Max LTP Change",
    round(
        df["ltp_change"].abs().max(),
        2
    )
)

from trade_scanner import trade_scanner

scanner = trade_scanner(
    spot,
    pcr_data["PCR"],
    support,
    resistance,
    vol_signal["volatility"],
    move["expected_move"]
)

st.subheader("Trade Scanner")

for trade in scanner:
    st.json(trade)

    st.subheader("Market Summary")

summary = {
    "Spot": round(spot, 2),
    "PCR": pcr_data["PCR"],
    "Expected Move": move["expected_move"],
    "Volatility": vol_signal["volatility"],
    "Support": support[:3],
    "Resistance": resistance[:3]
}

st.json(summary)

from strike_selector import (
    select_bear_call_strikes
)

strike_selection = (
    select_bear_call_strikes(df,spot)
)

st.subheader(
    "Auto Strike Selection"
)

st.json(strike_selection)

sell_strike = strike_selection["sell_strike"]
buy_strike = strike_selection["buy_strike"]

sell_ltp = float(
    df[
        (df["type"] == "CE")
        &
        (df["strike"] == sell_strike)
    ]["ltp"].iloc[0]
)

buy_ltp = float(
    df[
        (df["type"] == "CE")
        &
        (df["strike"] == buy_strike)
    ]["ltp"].iloc[0]
)

st.subheader("Selected Premiums")

st.write(
    "Sell",
    sell_strike,
    "CE:",
    sell_ltp
)

st.write(
    "Buy",
    buy_strike,
    "CE:",
    buy_ltp
)
from strategy_pricer import bear_call_spread

pricing = bear_call_spread(
    sell_strike,
    buy_strike,
    sell_ltp,
    buy_ltp
)

st.subheader("Strategy Pricing")

st.json(pricing)

from spread_optimizer import (
    optimize_bear_call
)

optimized = (
    optimize_bear_call(
        df,
        spot,
        move["expected_move"]
    )
)

st.subheader(
    "Spread Optimizer"
)

st.dataframe(
    optimized[:10]
)

st.subheader(
    "Best Spread"
)

st.json(
    optimized[0]
)
st.write("Expected Move:", move["expected_move"])

if optimized:
    st.json(optimized[0])