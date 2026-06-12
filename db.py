import streamlit as st
import pandas as pd

from fetch_chain import get_chain
from pcr import calculate_pcr
from max_pain import calculate_max_pain
from master_selector import choose_strategy

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="Nubra Options Dashboard")
st.title("🏔️ Nubra Options Dashboard")
st.caption("NUBRA WALO KI JAI HO")

# ─── Core Data Fetch ────────────────────────────────────────────────────────
df, chain = get_chain()

if "previous_df" not in st.session_state:
    st.session_state.previous_df = df.copy()
st.session_state.previous_df = df.copy()

spot      = chain.current_price / 100
pcr_data  = calculate_pcr(df)
max_pain  = calculate_max_pain(df)

# ─── Top Metrics Bar ────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Spot",     round(spot, 2))
col2.metric("PCR",      pcr_data["PCR"])
col3.metric("Max Pain", max_pain)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# 1. OPTION CHAIN
# ════════════════════════════════════════════════════════════════════════════
with st.expander("📋 Option Chain", expanded=True):

    st.dataframe(df, use_container_width=True)

    from oi_heatmap import plot_oi
    st.subheader("OI Distribution")
    st.plotly_chart(plot_oi(df), use_container_width=True)

    ce = df[df.type == "CE"].sort_values("oi", ascending=False).head(10)
    pe = df[df.type == "PE"].sort_values("oi", ascending=False).head(10)

    left, right = st.columns(2)
    left.subheader("🔴 Top Resistance (CE)")
    left.dataframe(ce[["strike", "oi", "volume"]], use_container_width=True)

    right.subheader("🟢 Top Support (PE)")
    right.dataframe(pe[["strike", "oi", "volume"]], use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# 2. PROFESSIONAL MERGED CHAIN
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🔗 Professional Option Chain (Merged)"):

    from merged_chain import build_merged_chain
    merged_df = build_merged_chain(df)

    st.dataframe(
        merged_df[[
            "ce_oi", "ce_oi_change", "ce_volume", "ce_iv",
            "strike",
            "pe_iv", "pe_volume", "pe_oi_change", "pe_oi",
            "signal"
        ]],
        use_container_width=True
    )

# ════════════════════════════════════════════════════════════════════════════
# 3. SUPPORT & RESISTANCE
# ════════════════════════════════════════════════════════════════════════════
with st.expander("📐 Support & Resistance"):

    from support_resistance import get_support_resistance
    support, resistance = get_support_resistance(df)

    col_s, col_r = st.columns(2)
    with col_s:
        st.subheader("Support")
        st.write(support)
    with col_r:
        st.subheader("Resistance")
        st.write(resistance)

    st.divider()

    from strength_engine import calculate_strength
    strength_df = calculate_strength(df)

    best_support    = strength_df.sort_values("support_score",    ascending=False).iloc[0]
    best_resistance = strength_df.sort_values("resistance_score", ascending=False).iloc[0]

    m1, m2 = st.columns(2)
    m1.metric("Strongest Support",    best_support["strike"])
    m2.metric("Strongest Resistance", best_resistance["strike"])

    t1, t2 = st.columns(2)
    with t1:
        st.subheader("Top Support Levels")
        st.dataframe(
            strength_df.sort_values("support_score", ascending=False).head(10)[["strike", "support_score"]],
            use_container_width=True
        )
    with t2:
        st.subheader("Top Resistance Levels")
        st.dataframe(
            strength_df.sort_values("resistance_score", ascending=False).head(10)[["strike", "resistance_score"]],
            use_container_width=True
        )

# ════════════════════════════════════════════════════════════════════════════
# 4. OI BUILD-UP & UNWINDING
# ════════════════════════════════════════════════════════════════════════════
with st.expander("📊 OI Build-up & Unwinding"):

    bu_col, uw_col = st.columns(2)

    with bu_col:
        st.subheader("🔺 Largest OI Build-up")
        build_up = (
            df.sort_values("oi_change", ascending=False)
            [["type", "strike", "oi_change", "oi"]]
            .head(15)
        )
        st.dataframe(build_up, use_container_width=True)

    with uw_col:
        st.subheader("🔻 Largest OI Unwinding")
        unwind = (
            df.sort_values("oi_change", ascending=True)
            [["type", "strike", "oi_change", "oi"]]
            .head(15)
        )
        st.dataframe(unwind, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# 5. IV & VOLATILITY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
with st.expander("📈 IV & Volatility Analysis"):

    from iv_skew import iv_skew
    from atm_iv import get_atm_iv
    from expected_move import expected_move
    from volatility_scanner import volatility_signal

    skew    = iv_skew(df)
    atm_iv  = get_atm_iv(df, spot)
    move    = expected_move(spot, atm_iv)
    vol_signal = volatility_signal(atm_iv)

    st.subheader("IV Skew")
    st.write(skew)

    st.subheader("Volatility Regime")
    st.json(vol_signal)

    st.subheader("Expected Move")
    st.json(move)

    st.subheader("Probability of Touch")
    from strike_probabilities import build_probability_table
    prob_df = build_probability_table(df, spot, atm_iv)
    st.dataframe(
        prob_df.sort_values("probability_touch", ascending=False),
        use_container_width=True
    )

# ════════════════════════════════════════════════════════════════════════════
# 6. MARKET REGIME & OUTLOOK
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🌐 Market Regime & Outlook"):

    from market_outlook import market_outlook
    from market_regime import market_regime
    from market_regime_v2 import market_regime_v2
    from market_map import market_map
    from probability import probability_engine

    # need support/resistance and strength_df from earlier sections
    # (already computed above)
    top_call_oi_change = df[df["type"] == "CE"]["oi_change"].max()
    top_put_oi_change  = df[df["type"] == "PE"]["oi_change"].max()

    outlook = market_outlook(spot, support, resistance, pcr_data["PCR"])
    regime1 = market_regime(pcr_data["PCR"], spot, support, resistance)
    regime2 = market_regime_v2(
        pcr_data["PCR"],
        best_support["support_score"],
        best_resistance["resistance_score"],
        top_call_oi_change,
        top_put_oi_change
    )
    map_data = market_map(spot, support, resistance, move["expected_move"])
    prob     = probability_engine(spot, support, resistance)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Market Outlook")
        st.json(outlook)
        st.subheader("Market Regime")
        st.json(regime1)
    with c2:
        st.subheader("Market Regime V2")
        st.json(regime2)
        st.subheader("Market Map")
        st.json(map_data)

    st.subheader("Probability Model")
    st.json(prob)

# ════════════════════════════════════════════════════════════════════════════
# 7. SIGNALS & SMART MONEY
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🎯 Signal Engine & Smart Money"):

    from signal_engine import generate_signals
    from smart_money import smart_money_signals
    from institutional_flow import institutional_flow

    signals = generate_signals(df)
    st.subheader("Signal Engine")
    for s in signals:
        st.success(s)

    st.subheader("Smart Money Signals")
    sm_signals = smart_money_signals(df)
    st.dataframe(sm_signals, use_container_width=True)

    st.subheader("Institutional Flow Scanner")
    flow_df = institutional_flow(df)
    st.dataframe(
        flow_df.sort_values("oi_change", ascending=False).head(25),
        use_container_width=True
    )

# ════════════════════════════════════════════════════════════════════════════
# 8. POSITION CLASSIFICATION
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🗂️ Position Classification"):

    from position_classifier import classify_positions
    from combined_chain import build_combined_chain

    classified = classify_positions(df)

    st.subheader("Classified Positions")
    st.dataframe(
        classified[["type", "strike", "ltp_change", "oi_change", "position"]]
        .sort_values("oi_change", ascending=False),
        use_container_width=True
    )

    st.subheader("Institutional Combined Chain")
    combined = build_combined_chain(classified)
    st.dataframe(
        combined[["ce_oi_change", "ce_position", "strike", "pe_oi_change", "pe_position", "net_signal"]],
        use_container_width=True
    )

# ════════════════════════════════════════════════════════════════════════════
# 9. MOMENTUM FLOW SCANNER
# ════════════════════════════════════════════════════════════════════════════
with st.expander("⚡ Momentum Flow Scanner"):

    from momentum_tracker import momentum_tracker
    mom_df = momentum_tracker(df)

    st.subheader("All Momentum Signals")
    st.dataframe(
        mom_df[[
            "type", "strike", "ltp", "ltp_change", "oi_change",
            "volume", "delta", "flow_signal", "scalp_signal",
            "confidence", "momentum_score"
        ]].head(30),
        use_container_width=True
    )

    long_col, short_col = st.columns(2)

    momentum_longs  = mom_df[mom_df["scalp_signal"] == "MOMENTUM LONG"]
    momentum_shorts = mom_df[mom_df["scalp_signal"] == "MOMENTUM SHORT"]

    with long_col:
        st.subheader("📗 Momentum Long Opportunities")
        st.dataframe(
            momentum_longs[["type", "strike", "ltp", "volume", "delta", "confidence", "momentum_score"]].head(15),
            use_container_width=True
        )
        if len(momentum_longs) > 0:
            best_long = momentum_longs.iloc[0]
            st.success(
                f"**BEST MOMENTUM LONG**\n\n"
                f"Strike: {best_long['strike']}  |  Type: {best_long['type']}\n\n"
                f"Confidence: {best_long['confidence']}%  |  Score: {round(best_long['momentum_score'], 2)}"
            )

    with short_col:
        st.subheader("📕 Momentum Short Opportunities")
        st.dataframe(
            momentum_shorts[["type", "strike", "ltp", "volume", "delta", "confidence", "momentum_score"]].head(15),
            use_container_width=True
        )
        if len(momentum_shorts) > 0:
            best_short = momentum_shorts.iloc[0]
            st.error(
                f"**BEST MOMENTUM SHORT**\n\n"
                f"Strike: {best_short['strike']}  |  Type: {best_short['type']}\n\n"
                f"Confidence: {best_short['confidence']}%  |  Score: {round(best_short['momentum_score'], 2)}"
            )

# ════════════════════════════════════════════════════════════════════════════
# 10. TRADE CANDIDATES
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🏹 Trade Candidates"):

    from trade_candidates import trade_candidates
    candidate_df = trade_candidates(df, spot)

    st.dataframe(
        candidate_df[["type", "strike", "oi", "oi_change", "volume", "score"]].head(20),
        use_container_width=True
    )

# ════════════════════════════════════════════════════════════════════════════
# 11. STRATEGY ENGINE
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🧠 Strategy Engine"):

    from strategy_engine import suggest_strategy as suggest_v1
    from strategy_engine_v2 import suggest_strategy as suggest_v2
    from option_mathematician import option_mathematician

    strategy_v1 = suggest_v1(spot, pcr_data["PCR"], support, resistance)
    strategy_v2 = suggest_v2(
        spot, support, resistance,
        pcr_data["PCR"], move["expected_move"], vol_signal["volatility"]
    )
    recommendation = option_mathematician(
        spot, pcr_data["PCR"], support, resistance,
        vol_signal["volatility"], move["expected_move"]
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Recommended Trade (V1)")
        st.json(strategy_v1)
    with c2:
        st.subheader("AI Strategy (V2)")
        st.json(strategy_v2)

    st.subheader("Option Mathematician")
    st.json(recommendation)

# ════════════════════════════════════════════════════════════════════════════
# 12. SPREAD OPTIMIZER
# ════════════════════════════════════════════════════════════════════════════
with st.expander("📉 Spread Optimizer"):

    from strike_selector import select_bear_call_strikes
    from strategy_pricer import bear_call_spread
    from spread_optimizer import optimize_bear_call
    from bull_put_optimizer import optimize_bull_put
    from iron_condor_optimizer import optimize_iron_condor

    # Bear Call
    strike_selection = select_bear_call_strikes(df, spot)
    sell_strike = strike_selection["sell_strike"]
    buy_strike  = strike_selection["buy_strike"]

    sell_ltp = float(df[(df["type"] == "CE") & (df["strike"] == sell_strike)]["ltp"].iloc[0])
    buy_ltp  = float(df[(df["type"] == "CE") & (df["strike"] == buy_strike)]["ltp"].iloc[0])

    pricing   = bear_call_spread(sell_strike, buy_strike, sell_ltp, buy_ltp)
    optimized = optimize_bear_call(df, spot, move["expected_move"])
    bull_puts = optimize_bull_put(df, spot, move["expected_move"])
    condor    = optimize_iron_condor(df, spot, move["expected_move"])

    st.subheader("Auto Strike Selection")
    st.json(strike_selection)

    col_sell, col_buy = st.columns(2)
    col_sell.metric("Sell Strike LTP", sell_ltp, f"CE {sell_strike}")
    col_buy.metric("Buy Strike LTP",   buy_ltp,  f"CE {buy_strike}")

    st.subheader("Strategy Pricing")
    st.json(pricing)

    st.subheader("Expected Move")
    st.write(move["expected_move"])

    bc_col, bp_col, ic_col = st.columns(3)
    with bc_col:
        st.subheader("Bear Call Spreads")
        st.dataframe(optimized[:10], use_container_width=True)
    with bp_col:
        st.subheader("Bull Put Spreads")
        st.dataframe(bull_puts[:10], use_container_width=True)
    with ic_col:
        st.subheader("Iron Condor")
        st.json(condor)

# ════════════════════════════════════════════════════════════════════════════
# 13. MASTER STRATEGY SELECTOR & LEADERBOARD
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🏆 Master Strategy Selector & Leaderboard", expanded=True):

    from confidence_engine import calculate_confidence
    from strategy_leaderboard import build_leaderboard
    from trade_logger import log_trade

    best_trade = choose_strategy(pcr_data["PCR"], optimized[0], bull_puts[0])
    best_trade["confidence"] = calculate_confidence(
        pcr_data["PCR"],
        best_trade["trade"]["pop"],
        best_trade["trade"]["risk_reward"]
    )

    leaderboard = build_leaderboard(optimized[0], bull_puts[0], condor)

    st.subheader("Strategy Leaderboard")
    st.dataframe(leaderboard, use_container_width=True)

    st.subheader("Top Ranked Strategy")
    st.json(leaderboard[0])

    st.subheader("Master Strategy Selector")
    st.json(best_trade)

    st.success(
        f"**View:** {best_trade['market_view']}\n\n"
        f"**Strategy:** {best_trade['trade']['strategy']}\n\n"
        f"**POP:** {best_trade['trade']['pop']}%  |  "
        f"**R:R:** {best_trade['trade']['risk_reward']}  |  "
        f"**Confidence:** {best_trade['confidence']}"
    )

    if st.button("💾 Save Recommendation"):
        log_trade(best_trade["trade"])
        st.success("Trade Saved ✅")

# ════════════════════════════════════════════════════════════════════════════
# 14. TRADE SCANNER
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🔍 Trade Scanner"):

    from trade_scanner import trade_scanner
    scanner = trade_scanner(
        spot, pcr_data["PCR"], support, resistance,
        vol_signal["volatility"], move["expected_move"]
    )

    for trade in scanner:
        st.json(trade)

# ════════════════════════════════════════════════════════════════════════════
# 15. SYSTEM HEALTH & DATA QUALITY
# ════════════════════════════════════════════════════════════════════════════
with st.expander("🩺 System Health & Data Quality"):

    h1, h2, h3 = st.columns(3)
    h1.metric("Rows",          len(df))
    h2.metric("Max OI Change", f"{int(df['oi_change'].abs().max()):,}")
    h3.metric("Max LTP Change", round(df["ltp_change"].abs().max(), 2))

    st.subheader("Market Summary")
    summary = {
        "Spot":          round(spot, 2),
        "PCR":           pcr_data["PCR"],
        "Expected Move": move["expected_move"],
        "Volatility":    vol_signal["volatility"],
        "Support":       support[:3],
        "Resistance":    resistance[:3],
    }
    st.json(summary)