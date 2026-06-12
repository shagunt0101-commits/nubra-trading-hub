import streamlit as st
import pandas as pd

from fetch_chain import get_chain
from pcr import calculate_pcr
from max_pain import calculate_max_pain
from streamlit_autorefresh import st_autorefresh
from master_selector import choose_strategy


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

from market_regime_v2 import (
    market_regime_v2
)

top_call_oi_change = (
    df[df["type"]=="CE"]
    ["oi_change"]
    .max()
)

top_put_oi_change = (
    df[df["type"]=="PE"]
    ["oi_change"]
    .max()
)

regime = market_regime_v2(
    pcr_data["PCR"],
    best_support["support_score"],
    best_resistance["resistance_score"],
    top_call_oi_change,
    top_put_oi_change
)

st.subheader(
    "Market Regime V2"
)

st.json(regime)

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

    from bull_put_optimizer import (
    optimize_bull_put
)

bull_puts = optimize_bull_put(
    df,
    spot,
    move["expected_move"]
)

best_trade = choose_strategy(
    pcr_data["PCR"],
    optimized[0],
    bull_puts[0]
)

st.subheader(
    "Master Strategy Selector"
)

st.json(best_trade)

st.success(
    f"""
    VIEW: {best_trade['market_view']}

    STRATEGY:
    {best_trade['trade']['strategy']}

    POP:
    {best_trade['trade']['pop']}%

    RR:
    {best_trade['trade']['risk_reward']}
    """
)

st.success(
    f"""
    Market View: {best_trade['market_view']}

    Recommended Strategy:
    {best_trade['trade']['strategy']}
    """
)

st.subheader(
    "Bull Put Optimizer"
)

st.dataframe(
    bull_puts[:10]
)
from iron_condor_optimizer import optimize_iron_condor


condor = optimize_iron_condor(
    df,
    spot,
    move["expected_move"]
)

st.subheader(
    "Iron Condor Optimizer"
)

st.json(condor)

st.subheader(
    "Best Bull Put"

)

st.json(
    bull_puts[0]
)


from master_selector import (
    choose_strategy
)

best_trade = choose_strategy(
    pcr_data["PCR"],
    optimized[0],
    bull_puts[0]
)

st.subheader(
    "Master Strategy Selector"
)

st.json(best_trade)

from confidence_engine import (
    calculate_confidence
)

best_trade["confidence"] = (
    calculate_confidence(
        pcr_data["PCR"],
        best_trade["trade"]["pop"],
        best_trade["trade"]["risk_reward"]
    )
)

from strategy_leaderboard import (
    build_leaderboard
)

leaderboard = build_leaderboard(
    optimized[0],
    bull_puts[0],
    condor
)

st.subheader(
    "Strategy Leaderboard"
)

st.dataframe(leaderboard)

st.subheader(
    "Top Ranked Strategy"
)

st.json(
    leaderboard[0]
)

from trade_logger import (
    log_trade
)

if st.button(
    "Save Recommendation"
):
    log_trade(
        best_trade["trade"]
    )

    st.success(
        "Trade Saved"
    )

    
from momentum_tracker import (
    momentum_tracker
)

mom_df = momentum_tracker(df)

st.subheader(
    "Momentum Flow Scanner"
)

st.dataframe(
    mom_df[
        [
            "type",
            "strike",
            "ltp",
            "ltp_change",
            "oi_change",
            "volume",
            "delta",
            "flow_signal",
            "scalp_signal",
            "confidence",
            "momentum_score"
        ]
    ].head(30),
    use_container_width=True
)

st.subheader(
    "Momentum Long Opportunities"
)

momentum_longs = (
    mom_df[
        mom_df["scalp_signal"]
        ==
        "MOMENTUM LONG"
    ]
)

st.dataframe(
    momentum_longs[
        [
            "type",
            "strike",
            "ltp",
            "volume",
            "delta",
            "confidence",
            "momentum_score"
        ]
    ].head(15),
    use_container_width=True
)

st.subheader(
    "Momentum Short Opportunities"
)

momentum_shorts = (
    mom_df[
        mom_df["scalp_signal"]
        ==
        "MOMENTUM SHORT"
    ]
)

st.dataframe(
    momentum_shorts[
        [
            "type",
            "strike",
            "ltp",
            "volume",
            "delta",
            "confidence",
            "momentum_score"
        ]
    ].head(15),
    use_container_width=True
)

if len(momentum_longs) > 0:

    best_long = momentum_longs.iloc[0]

    st.success(
        f"""
        BEST MOMENTUM LONG

        Strike: {best_long['strike']}

        Type: {best_long['type']}

        Confidence: {best_long['confidence']}%

        Score: {round(best_long['momentum_score'],2)}
        """
    )

if len(momentum_shorts) > 0:

    best_short = momentum_shorts.iloc[0]

    st.error(
        f"""
        BEST MOMENTUM SHORT

        Strike: {best_short['strike']}

        Type: {best_short['type']}

        Confidence: {best_short['confidence']}%

        Score: {round(best_short['momentum_score'],2)}
        """
    )

    mom_df = momentum_tracker(df)

st.write(mom_df.columns.tolist())