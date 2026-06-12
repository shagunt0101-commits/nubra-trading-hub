import streamlit as st
import pandas as pd
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="NUBRA TRADING HUB",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== ADVANCED CSS STYLING ====================
st.markdown(
    """
    <style>
    
    * {
        margin: 0;
        padding: 0;
    }
    
    .stApp {
        background-color: #0B1220;
        color: #E5E7EB;
    }
    
    /* Main Container */
    .main {
        background-color: #0B1220;
    }
    
    /* Cards & Metrics */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    div[data-testid="stMetricDelta"] {
        color: #10B981;
    }
    
    /* Terminal Cards */
    .terminal-card {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 1px solid #374151;
        border-left: 4px solid #06B6D4;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    .terminal-card h2 {
        color: #06B6D4;
        margin-bottom: 10px;
        font-size: 24px;
    }
    
    .terminal-card p {
        color: #9CA3AF;
        font-size: 14px;
    }
    
    /* Tabs */
    [role="tab"] {
        background-color: #1F2937 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        margin-right: 8px !important;
        color: #9CA3AF !important;
        font-weight: 500 !important;
    }
    
    [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #0891B2 !important;
    }
    
    /* Dividers */
    .stDivider {
        border-color: #374151;
        margin: 20px 0;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #F3F4F6;
    }
    
    h1 {
        border-bottom: 2px solid #06B6D4;
        padding-bottom: 12px;
        margin-bottom: 20px;
    }
    
    h2 {
        color: #06B6D4;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    h3 {
        color: #E5E7EB;
        margin-top: 20px;
        margin-bottom: 12px;
    }
    
    /* Data Frames */
    .stDataFrame {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 8px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0891B2 0%, #06B6D4 100%);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
    }
    
    /* Status Badges */
    .status-success {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid #10B981;
        color: #10B981;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        font-weight: 500;
    }
    
    .status-warning {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid #F59E0B;
        color: #F59E0B;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        font-weight: 500;
    }
    
    .status-error {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #EF4444;
        color: #EF4444;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        font-weight: 500;
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #06B6D4, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: #1F2937 !important;
        border: 1px solid #374151 !important;
        color: #E5E7EB !important;
        border-radius: 8px !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== IMPORTS ====================
try:
    from fetch_chain import get_chain
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
    st.error(f"❌ Import Error: {e}")
    st.stop()

# ==================== CACHE ====================
@st.cache_data(ttl=1)
def get_live():
    return get_chain()

@st.fragment(run_every="1s")
def show_clock():
    st.write(f"**⏰ LIVE • {datetime.now().strftime('%H:%M:%S')}**")

# ==================== HEADER ====================
st.markdown(
    """
    <div class="terminal-card">
    <h2>🏦 NUBRA TRADING HUB</h2>
    <p>Advanced Options Trading Terminal • Real-Time Analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)

show_clock()

# ==================== GET DATA ====================
try:
    df, chain = get_live()
    spot = (chain.current_price or 0) / 100
    best_ce, best_pe, board = option_buying_engine(df, spot)
    bias = market_bias(board)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ==================== TOP METRICS ====================
st.markdown("### 📊 Market Overview")
col1, col2, col3, col4 = st.columns(4)

col1.metric("📈 Spot Price", f"₹{spot:.2f}", 
    delta=f"{((spot - chain.current_price/100) * 100):+.2f}%")
col2.metric("🎯 Market Bias", bias)
col3.metric("📋 Total Options", len(df))
col4.metric("⚡ Signals", len(board))

st.divider()

# ==================== TABS ====================
tab_buying, tab_dashboard = st.tabs([
    "🚀 BUYING TERMINAL",
    "📊 OPTIONS DASHBOARD"
])

# ==================== TAB 1: BUYING TERMINAL ====================
with tab_buying:
    
    st.markdown(
        """
        <div class="terminal-card">
        <h2>🚀 Option Buying Engine</h2>
        <p>Real-time trade recommendations with advanced filtering</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    try:
        # ---- MARKET STRUCTURE ----
        st.markdown("### ⚙️ Market Structure")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Bias Direction", bias, delta="Current")
        
        support, resistance = get_support_resistance(df)
        if len(support) > 0:
            col2.metric("🔻 Support", f"₹{support[0]:.2f}")
        if len(resistance) > 0:
            col3.metric("🔺 Resistance", f"₹{resistance[0]:.2f}")
        
        st.divider()
        
        # ---- BEST TRADES ----
        st.markdown("### 💰 Best Trade Setup")
        
        left, right = st.columns(2)
        
        with left:
            st.markdown(
                """
                <div class="terminal-card" style="border-left-color: #10B981;">
                <h3>📈 BEST CALL (CE)</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if len(best_ce) > 0:
                ce_trade = build_trade(best_ce.iloc[0])
                
                col1, col2 = st.columns(2)
                col1.metric("Strike", f"₹{ce_trade['strike']}")
                col2.metric("Entry", f"₹{ce_trade['entry']:.2f}")
                
                col1, col2 = st.columns(2)
                col1.metric("SL", f"₹{ce_trade['sl']:.2f}")
                col2.metric("Target 1", f"₹{ce_trade['target1']:.2f}")
                
                col1, col2 = st.columns(2)
                col1.metric("Target 2", f"₹{ce_trade['target2']:.2f}")
                col2.metric("Confidence", f"{ce_trade['confidence']:.1f}%")
                
                st.markdown(
                    f"""
                    <div class="status-success">
                    📊 Flow: {ce_trade['flow']}<br>
                    ⭐ Grade: {ce_trade['grade']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button("💾 Save CE Trade", key="ce_button"):
                    save_paper_trade(ce_trade)
                    st.success("✅ CE Trade Saved!")
            else:
                st.info("No suitable CALL setup found")
        
        with right:
            st.markdown(
                """
                <div class="terminal-card" style="border-left-color: #EF4444;">
                <h3>📉 BEST PUT (PE)</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if len(best_pe) > 0:
                pe_trade = build_trade(best_pe.iloc[0])
                
                col1, col2 = st.columns(2)
                col1.metric("Strike", f"₹{pe_trade['strike']}")
                col2.metric("Entry", f"₹{pe_trade['entry']:.2f}")
                
                col1, col2 = st.columns(2)
                col1.metric("SL", f"₹{pe_trade['sl']:.2f}")
                col2.metric("Target 1", f"₹{pe_trade['target1']:.2f}")
                
                col1, col2 = st.columns(2)
                col1.metric("Target 2", f"₹{pe_trade['target2']:.2f}")
                col2.metric("Confidence", f"{pe_trade['confidence']:.1f}%")
                
                st.markdown(
                    f"""
                    <div class="status-warning">
                    📊 Flow: {pe_trade['flow']}<br>
                    ⭐ Grade: {pe_trade['grade']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button("💾 Save PE Trade", key="pe_button"):
                    save_paper_trade(pe_trade)
                    st.success("✅ PE Trade Saved!")
            else:
                st.info("No suitable PUT setup found")
        
        st.divider()
        
        # ---- MOMENTUM SIGNALS ----
        st.markdown("### ⚡ Momentum Signals")
        radar = board[board["confidence"] >= 50].sort_values(
            ["confidence", "score"], 
            ascending=False
        ).head(10)
        
        if len(radar) > 0:
            st.dataframe(
                radar[[
                    "type", "strike", "flow", "strength", 
                    "confidence", "score", "grade"
                ]],
                use_container_width=True
            )
        else:
            st.info("No high-confidence signals at the moment")
        
        st.divider()
        
        # ---- TRADE JOURNAL ----
        st.markdown("### 📒 Trade Journal & PnL")
        
        journal = load_journal()
        if not journal.empty:
            stats = calculate_pnl(journal)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Trades", stats.get("total", 0))
            col2.metric("✅ Wins", stats.get("wins", 0))
            col3.metric("❌ Losses", stats.get("losses", 0))
            col4.metric("Win Rate", f"{stats.get('win_rate', 0):.1f}%")
            
            st.dataframe(journal, use_container_width=True)
        else:
            st.info("📌 No trades in journal yet. Start by saving a trade!")
    
    except Exception as e:
        st.error(f"❌ Error in Buying Terminal: {str(e)}")

# ==================== TAB 2: OPTIONS DASHBOARD ====================
with tab_dashboard:
    
    st.markdown(
        """
        <div class="terminal-card">
        <h2>📊 Options Analysis Dashboard</h2>
        <p>Comprehensive market data, OI analysis, and Greeks</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    try:
        pcr_data = calculate_pcr(df)
        max_pain = calculate_max_pain(df)
        
        # ---- KEY METRICS ----
        st.markdown("### 📈 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Spot", f"₹{spot:.2f}")
        col2.metric("PCR Ratio", f"{pcr_data['PCR']:.2f}")
        col3.metric("Max Pain", f"₹{max_pain}")
        col4.metric("Data Points", len(df))
        
        st.divider()
        
        # ---- OPTION CHAIN ----
        st.markdown("### 📋 Option Chain Data")
        st.dataframe(df, use_container_width=True, height=300)
        
        st.divider()
        
        # ---- OI HEATMAP ----
        st.markdown("### 🔥 Open Interest Distribution")
        try:
            st.plotly_chart(plot_oi(df), use_container_width=True)
        except:
            st.warning("Could not load OI heatmap")
        
        st.divider()
        
        # ---- TOP CE & PE ----
        st.markdown("### 💪 Top Resistance & Support")
        ce = df[df.type == "CE"].sort_values("oi", ascending=False).head(10)
        pe = df[df.type == "PE"].sort_values("oi", ascending=False).head(10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Top Resistance (CE)")
            st.dataframe(
                ce[["strike", "oi", "volume", "iv"]],
                use_container_width=True
            )
        
        with col2:
            st.subheader("📉 Top Support (PE)")
            st.dataframe(
                pe[["strike", "oi", "volume", "iv"]],
                use_container_width=True
            )
        
        st.divider()
        
        # ---- SUPPORT & RESISTANCE LEVELS ----
        st.markdown("### 🎯 Support & Resistance Levels")
        try:
            support, resistance = get_support_resistance(df)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔻 Support Levels")
                st.write(support)
            
            with col2:
                st.subheader("🔺 Resistance Levels")
                st.write(resistance)
        except:
            st.warning("Could not calculate levels")
        
        st.divider()
        
        # ---- IV SKEW ----
        st.markdown("### 📊 IV Skew Analysis")
        try:
            skew = iv_skew(df)
            st.write(skew)
        except:
            st.info("IV analysis pending...")
        
        st.divider()
        
        # ---- OI CHANGES ----
        st.markdown("### 📈 Largest OI Build-up")
        buildup = df.sort_values("oi_change", ascending=False)[
            ["type", "strike", "oi_change", "oi"]
        ].head(15)
        st.dataframe(buildup, use_container_width=True)
        
        st.divider()
        
        st.markdown("### 📉 Largest OI Unwinding")
        unwind = df.sort_values("oi_change", ascending=True)[
            ["type", "strike", "oi_change", "oi"]
        ].head(15)
        st.dataframe(unwind, use_container_width=True)
        
        st.divider()
        
        # ---- GEX ----
        st.markdown("### ⚡ Gamma Exposure (GEX)")
        try:
            gex = calculate_gex(df)
            st.write(gex)
        except:
            st.info("GEX calculation pending...")
    
    except Exception as e:
        st.error(f"❌ Error in Dashboard: {str(e)}")

# ==================== FOOTER ====================
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #6B7280; font-size: 12px; margin-top: 30px;">
    <p>🏦 NUBRA Trading Hub • Advanced Options Terminal • Real-Time Market Data</p>
    <p>Last Updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%H:%M:%S %d-%m-%Y")),
    unsafe_allow_html=True
)
