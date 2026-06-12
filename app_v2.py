import streamlit as st
import pandas as pd
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Nubra Trading Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLING ====================
st.markdown("""
<style>
.stApp { 
    background-color:#0B1220;
}
div[data-testid="stMetric"] {
    background:#111827;
    border:1px solid #374151;
    border-radius:12px;
    padding:12px;
}
.terminal-card {
    background:#111827;
    border:1px solid #374151;
    border-radius:15px;
    padding:15px;
    margin-bottom:10px;
}
.status-active {
    color: #10b981;
    font-weight: bold;
}
.status-alert {
    color: #ef4444;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==================== IMPORTS ====================
try:
    from fetch_chain import get_chain, get_available_fno_instruments
    from pcr import calculate_pcr
    from max_pain import calculate_max_pain
    from buying_engine import option_buying_engine
    from buying_terminal import build_trade
    from market_bias import market_bias
    from paper_trade import save_paper_trade
    from trade_journal import load_journal
    from pnl_tracker import calculate_pnl
    from oi_heatmap import plot_oi
    from support_resistance import get_support_resistance
    from iv_skew import iv_skew
    from gex import calculate_gex
except Exception as e:
    st.error(f"⚠️ Import Error: {e}")
    st.stop()

# ==================== SIDEBAR CONTROLS ====================
st.sidebar.markdown("### ⚙️ CONTROLS")

# Get available instruments
available_instruments = get_available_fno_instruments()

# Initialize session state if not exists
if "selected_instrument" not in st.session_state:
    st.session_state.selected_instrument = available_instruments[0]

# Reset if the saved instrument is no longer available
if st.session_state.selected_instrument not in available_instruments:
    st.session_state.selected_instrument = available_instruments[0]

selected_instrument = st.sidebar.selectbox(
    "Select Instrument",
    options=available_instruments,
    index=available_instruments.index(st.session_state.selected_instrument),
    key="selected_instrument"
)

st.sidebar.markdown(f"**Selected:** `{selected_instrument}`")

# ==================== CACHE ====================
@st.cache_data(ttl=1)
def get_live(instrument):
    return get_chain(instrument)

@st.fragment(run_every="1s")
def show_clock():
    st.markdown(f"**⏰ {datetime.now().strftime('%H:%M:%S')}**")

# ==================== MAIN TITLE ====================
col_title, col_clock = st.columns([0.85, 0.15])
with col_title:
    st.markdown(
        f"""
        <div class="terminal-card">
        <h2>🚀 NUBRA PRO TRADING HUB</h2>
        <p><span class="status-active">● LIVE</span> | Instrument: <code>{selected_instrument}</code></p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_clock:
    show_clock()

# ==================== CREATE TABS ====================
tab_setup, tab_price, tab_signals, tab_monitor, tab_journal, tab_chain = st.tabs([
    "⚙ Setup",
    "📈 Price Action",
    "⚡ Signals",
    "🎯 Monitor",
    "📒 Journal",
    "📊 Chain Data"
])

# ==================== GET DATA ====================
try:
    df, chain = get_live(selected_instrument)
    spot = (chain.current_price or 0) / 100

    best_ce, best_pe, board = option_buying_engine(df, spot)
    bias = market_bias(board)
    support, resistance = get_support_resistance(df)
    pcr_data = calculate_pcr(df)
    max_pain = calculate_max_pain(df)

except Exception as e:
    st.error(f"❌ Error fetching data: {str(e)}")
    st.stop()

# ==================== KEY METRICS ====================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Spot", f"₹{spot:.2f}")
col2.metric("Bias", bias)
col3.metric("PCR", f"{pcr_data['PCR']:.2f}")
col4.metric("Max Pain", f"₹{max_pain}")
col5.metric("Signals", len(board))

# ==================== TAB 1: SETUP ====================
with tab_setup:
    st.subheader(f"📊 {selected_instrument} Market Structure")
    
    left, middle, right = st.columns(3)
    
    with left:
        st.markdown("### Market Bias")
        st.metric("Current", bias)
        
        if len(support) > 0:
            st.metric("Major Support", f"₹{support[0]:.2f}")
    
    with middle:
        st.markdown("### Price Levels")
        st.metric("Current Price", f"₹{spot:.2f}")
        
        if len(resistance) > 0:
            st.metric("Major Resistance", f"₹{resistance[0]:.2f}")
    
    with right:
        st.markdown("### Analytics")
        st.metric("PCR Ratio", f"{pcr_data['PCR']:.2f}")
        st.metric("Max Pain", f"₹{max_pain}")

# ==================== TAB 2: PRICE ACTION ====================
with tab_price:
    st.subheader(f"🎯 {selected_instrument} Momentum Radar")
    
    if len(board) > 0:
        radar_df = board[[
            "type", "strike", "flow", "strength", 
            "confidence", "score", "grade"
        ]].sort_values("confidence", ascending=False).head(20)
        
        st.dataframe(radar_df, use_container_width=True, height=400)
    else:
        st.info("No momentum signals detected")

# ==================== TAB 3: SIGNALS ====================
with tab_signals:
    st.subheader(f"⚡ Signal Engine - {selected_instrument}")
    
    high_conf = board[board["confidence"] >= 70].sort_values(["confidence", "score"], ascending=False)
    
    if len(high_conf) > 0:
        best = high_conf.iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("✅ BEST SETUP FOUND")
            st.markdown(f"""
            **Strike:** {best['strike']}  
            **Type:** {best['type']}  
            **Grade:** {best['grade']}  
            **Confidence:** {best['confidence']:.1f}%  
            **Flow:** {best['flow']}
            """)
        
        with col2:
            if best['type'] == 'CE':
                if len(best_ce) > 0:
                    trade = build_trade(best_ce.iloc[0])
                    st.info(f"""
                    **Entry:** ₹{trade['entry']:.2f}  
                    **SL:** ₹{trade['sl']:.2f}  
                    **Target1:** ₹{trade['target1']:.2f}  
                    **Target2:** ₹{trade['target2']:.2f}  
                    **R:R:** 1:{(trade['target1']-trade['entry'])/(trade['entry']-trade['sl']):.2f}
                    """)
            else:
                if len(best_pe) > 0:
                    trade = build_trade(best_pe.iloc[0])
                    st.warning(f"""
                    **Entry:** ₹{trade['entry']:.2f}  
                    **SL:** ₹{trade['sl']:.2f}  
                    **Target1:** ₹{trade['target1']:.2f}  
                    **Target2:** ₹{trade['target2']:.2f}  
                    **R:R:** 1:{(trade['target1']-trade['entry'])/(trade['entry']-trade['sl']):.2f}
                    """)
    else:
        st.info("⏳ Waiting for high-confidence signals (>70%)")

# ==================== TAB 4: MONITOR ====================
with tab_monitor:
    st.subheader(f"🎯 Trade Monitor - {selected_instrument}")
    
    left, right = st.columns(2)
    
    with left:
        st.markdown("### 🚀 CALL (CE) Setup")
        if len(best_ce) > 0:
            ce_trade = build_trade(best_ce.iloc[0])
            st.success(f"""
            **Strike:** ₹{ce_trade['strike']}  
            **Entry:** ₹{ce_trade['entry']:.2f}  
            **Stop Loss:** ₹{ce_trade['sl']:.2f}  
            **Target 1:** ₹{ce_trade['target1']:.2f}  
            **Target 2:** ₹{ce_trade['target2']:.2f}  
            **Confidence:** {ce_trade['confidence']:.1f}%  
            **Grade:** {ce_trade['grade']}
            """)
            if st.button("💾 Save CE Trade", key="save_ce"):
                save_paper_trade(ce_trade)
                st.success("✅ CE Trade Saved!")
        else:
            st.info("No CE setup")
    
    with right:
        st.markdown("### 🔻 PUT (PE) Setup")
        if len(best_pe) > 0:
            pe_trade = build_trade(best_pe.iloc[0])
            st.warning(f"""
            **Strike:** ₹{pe_trade['strike']}  
            **Entry:** ₹{pe_trade['entry']:.2f}  
            **Stop Loss:** ₹{pe_trade['sl']:.2f}  
            **Target 1:** ₹{pe_trade['target1']:.2f}  
            **Target 2:** ₹{pe_trade['target2']:.2f}  
            **Confidence:** {pe_trade['confidence']:.1f}%  
            **Grade:** {pe_trade['grade']}
            """)
            if st.button("💾 Save PE Trade", key="save_pe"):
                save_paper_trade(pe_trade)
                st.success("✅ PE Trade Saved!")
        else:
            st.info("No PE setup")

# ==================== TAB 5: JOURNAL ====================
with tab_journal:
    st.subheader(f"📒 Trading Journal - {selected_instrument}")
    
    trades = load_journal()
    
    if not trades.empty:
        stats = calculate_pnl(trades)
        
        a, b, c, d = st.columns(4)
        a.metric("Total Trades", stats["total"])
        b.metric("Wins", stats["wins"])
        c.metric("Losses", stats["losses"])
        d.metric("Win Rate %", f"{stats['win_rate']:.1f}%")
        
        st.divider()
        st.dataframe(trades, use_container_width=True, height=400)
    else:
        st.info("📌 No trades in journal yet")

# ==================== TAB 6: CHAIN DATA ====================
with tab_chain:
    st.subheader(f"📊 Full Option Chain - {selected_instrument}")
    
    # OI Distribution
    st.markdown("### 🔥 Open Interest Distribution")
    try:
        st.plotly_chart(plot_oi(df), use_container_width=True)
    except:
        st.warning("Could not load OI heatmap")
    
    st.divider()
    
    # Top Strikes
    ce = df[df.type == "CE"].sort_values("oi", ascending=False).head(15)
    pe = df[df.type == "PE"].sort_values("oi", ascending=False).head(15)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📈 Top Call Resistance")
        st.dataframe(ce[["strike", "oi", "volume", "iv"]], use_container_width=True)
    
    with col2:
        st.markdown("### 📉 Top Put Support")
        st.dataframe(pe[["strike", "oi", "volume", "iv"]], use_container_width=True)
    
    st.divider()
    
    # Full Chain
    st.markdown("### 📋 Complete Option Chain")
    st.dataframe(df, use_container_width=True, height=600)
